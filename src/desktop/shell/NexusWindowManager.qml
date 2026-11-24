import QtQuick

QtObject {
    id: windowManager

    // Active workspace index (0: Code, 1: AI/Models, 2: DevOps, 3: Web)
    property int currentWorkspace: 0
    readonly property var workspaceNames: ["Code", "AI / Models", "DevOps", "Web"]

    // Windows model array:
    // [{ id: "win-1", title: "Terminal", appType: "terminal", icon: "⌨", x: 80, y: 80, width: 720, height: 480, isMinimized: false, isMaximized: false, isActive: true, zIndex: 1, workspace: 0 }]
    property var windows: []

    // Next window ID counter and top Z-index
    property int _nextId: 1
    property int _topZIndex: 10

    // Currently active / focused window
    property string activeWindowId: ""

    // Desktop notification list
    property var notifications: [
        { id: 1, variant: "info", title: "NEXUS AI Core Online", message: "Local model router ready at http://localhost:11430/v1", time: "Just now" },
        { id: 2, variant: "success", title: "Workspace Synced", message: "Repository nexus-os up to date on branch main", time: "2m ago" }
    ]

    signal windowOpened(string windowId, string appType)
    signal windowClosed(string windowId)
    signal windowFocused(string windowId)
    signal workspaceChanged(int newIndex)

    function switchWorkspace(index) {
        if (index >= 0 && index < workspaceNames.length && index !== currentWorkspace) {
            currentWorkspace = index;
            // De-focus windows not on current workspace
            var updated = [];
            var foundActive = false;
            for (var i = 0; i < windows.length; i++) {
                var w = Object.assign({}, windows[i]);
                if (w.workspace === currentWorkspace && !w.isMinimized && !foundActive) {
                    w.isActive = true;
                    activeWindowId = w.id;
                    foundActive = true;
                } else if (w.workspace !== currentWorkspace) {
                    w.isActive = false;
                }
                updated.push(w);
            }
            if (!foundActive) activeWindowId = "";
            windows = updated;
            workspaceChanged(index);
        }
    }

    function openApp(appType, title, icon, defaultW, defaultH) {
        var w = defaultW || 740;
        var h = defaultH || 500;

        // Check if an instance of this app already exists on current workspace
        for (var i = 0; i < windows.length; i++) {
            if (windows[i].appType === appType && windows[i].workspace === currentWorkspace) {
                var existingId = windows[i].id;
                restoreWindow(existingId);
                focusWindow(existingId);
                return existingId;
            }
        }

        // Create new window
        _topZIndex++;
        var newId = "win-" + (_nextId++);
        var offsetX = 60 + ((windows.length * 28) % 200);
        var offsetY = 60 + ((windows.length * 28) % 150);

        var newWin = {
            id: newId,
            title: title || appType,
            appType: appType,
            icon: icon || "💻",
            x: offsetX,
            y: offsetY,
            width: w,
            height: h,
            prevX: offsetX,
            prevY: offsetY,
            prevW: w,
            prevH: h,
            isMinimized: false,
            isMaximized: false,
            isActive: true,
            zIndex: _topZIndex,
            workspace: currentWorkspace
        };

        var list = [];
        for (var j = 0; j < windows.length; j++) {
            var item = Object.assign({}, windows[j]);
            item.isActive = false;
            list.push(item);
        }
        list.push(newWin);
        windows = list;
        activeWindowId = newId;

        windowOpened(newId, appType);
        return newId;
    }

    function closeWindow(windowId) {
        var list = [];
        for (var i = 0; i < windows.length; i++) {
            if (windows[i].id !== windowId) {
                list.push(windows[i]);
            }
        }
        windows = list;
        if (activeWindowId === windowId) {
            // Focus highest remaining window on current workspace
            var topWin = null;
            for (var j = 0; j < windows.length; j++) {
                if (windows[j].workspace === currentWorkspace && !windows[j].isMinimized) {
                    if (!topWin || windows[j].zIndex > topWin.zIndex) {
                        topWin = windows[j];
                    }
                }
            }
            if (topWin) {
                focusWindow(topWin.id);
            } else {
                activeWindowId = "";
            }
        }
        windowClosed(windowId);
    }

    function focusWindow(windowId) {
        _topZIndex++;
        var list = [];
        for (var i = 0; i < windows.length; i++) {
            var w = Object.assign({}, windows[i]);
            if (w.id === windowId) {
                w.isActive = true;
                w.zIndex = _topZIndex;
                w.isMinimized = false;
            } else {
                w.isActive = false;
            }
            list.push(w);
        }
        windows = list;
        activeWindowId = windowId;
        windowFocused(windowId);
    }

    function minimizeWindow(windowId) {
        var list = [];
        for (var i = 0; i < windows.length; i++) {
            var w = Object.assign({}, windows[i]);
            if (w.id === windowId) {
                w.isMinimized = true;
                w.isActive = false;
            }
            list.push(w);
        }
        windows = list;
        if (activeWindowId === windowId) {
            activeWindowId = "";
        }
    }

    function maximizeWindow(windowId) {
        var list = [];
        for (var i = 0; i < windows.length; i++) {
            var w = Object.assign({}, windows[i]);
            if (w.id === windowId) {
                w.prevX = w.x;
                w.prevY = w.y;
                w.prevW = w.width;
                w.prevH = w.height;
                w.isMaximized = true;
            }
            list.push(w);
        }
        windows = list;
        focusWindow(windowId);
    }

    function restoreWindow(windowId) {
        var list = [];
        for (var i = 0; i < windows.length; i++) {
            var w = Object.assign({}, windows[i]);
            if (w.id === windowId) {
                if (w.isMaximized) {
                    w.x = w.prevX;
                    w.y = w.prevY;
                    w.width = w.prevW;
                    w.height = w.prevH;
                    w.isMaximized = false;
                }
                w.isMinimized = false;
            }
            list.push(w);
        }
        windows = list;
        focusWindow(windowId);
    }

    function updateWindowGeometry(windowId, newX, newY, newW, newH) {
        var list = [];
        for (var i = 0; i < windows.length; i++) {
            var w = Object.assign({}, windows[i]);
            if (w.id === windowId) {
                w.x = newX;
                w.y = newY;
                w.width = newW;
                w.height = newH;
            }
            list.push(w);
        }
        windows = list;
    }

    function isAppRunning(appType) {
        for (var i = 0; i < windows.length; i++) {
            if (windows[i].appType === appType) {
                return true;
            }
        }
        return false;
    }

    function addNotification(variant, title, message) {
        var item = {
            id: Date.now(),
            variant: variant || "info",
            title: title || "Notification",
            message: message || "",
            time: "Just now"
        };
        var notifs = [item].concat(notifications);
        notifications = notifs;
    }

    function clearNotifications() {
        notifications = [];
    }
}
