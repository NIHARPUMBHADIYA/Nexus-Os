import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../../design-system/qml"

Rectangle {
    id: root
    color: NexusTheme.background

    property string selectedCategory: "all"
    property string searchQuery: ""
    property var activeModalPackage: null
    property bool showDetailModal: false

    // Fallback data if bridge is not attached
    property var categoriesData: (typeof softwareCenterBridge !== "undefined" && softwareCenterBridge.categoriesList) ? softwareCenterBridge.categoriesList : [
        {"id": "all", "name": "All Categories", "icon": "🌐"},
        {"id": "ai_dev", "name": "AI Development", "icon": "🧠"},
        {"id": "editors", "name": "IDEs and Editors", "icon": "💻"},
        {"id": "languages", "name": "Programming Languages", "icon": "🔤"},
        {"id": "web_dev", "name": "Web Development", "icon": "🕸️"},
        {"id": "mobile_dev", "name": "Mobile Development", "icon": "📱"},
        {"id": "databases", "name": "Databases", "icon": "🗄️"},
        {"id": "devops", "name": "DevOps", "icon": "🔄"},
        {"id": "cloud", "name": "Cloud", "icon": "☁️"},
        {"id": "security", "name": "Cybersecurity", "icon": "🛡️"},
        {"id": "robotics", "name": "Robotics", "icon": "🦾"},
        {"id": "embedded", "name": "Embedded Systems", "icon": "📟"},
        {"id": "gamedev", "name": "Game Development", "icon": "🎮"},
        {"id": "design", "name": "Design", "icon": "🎨"},
        {"id": "productivity", "name": "Productivity", "icon": "⚡"}
    ]

    property var packagesData: (typeof softwareCenterBridge !== "undefined" && softwareCenterBridge.packagesList) ? softwareCenterBridge.packagesList : [
        { "id": "godot", "name": "Godot Engine 4", "category": "gamedev", "description": "Innovative 2D and 3D cross-platform game engine.", "version": "4.3.0", "maintainer": "Godot Foundation", "license": "MIT", "icon": "🤖", "backend": "flatpak", "size_mb": 115, "installed": true, "favorite": true, "backend_info": {"name": "Flatpak (Flathub)", "icon": "🧊"} },
        { "id": "wireshark", "name": "Wireshark", "category": "security", "description": "The world's foremost network protocol analyzer.", "version": "4.4.3", "maintainer": "Wireshark Foundation", "license": "GPLv2+", "icon": "🦈", "backend": "dnf", "size_mb": 110, "installed": true, "favorite": true, "backend_info": {"name": "Native RPM (DNF)", "icon": "📦"} },
        { "id": "rust", "name": "Rust Toolchain", "category": "languages", "description": "Empowering everyone to build reliable and efficient software.", "version": "1.85.0", "maintainer": "The Rust Project", "license": "MIT / Apache-2.0", "icon": "🦀", "backend": "dnf", "size_mb": 180, "installed": true, "favorite": true, "backend_info": {"name": "Native RPM (DNF)", "icon": "📦"} },
        { "id": "podman", "name": "Podman Containers", "category": "devops", "description": "Daemonless, rootless container engine.", "version": "5.3.1", "maintainer": "Red Hat", "license": "Apache-2.0", "icon": "🦭", "backend": "dnf", "size_mb": 120, "installed": true, "favorite": false, "backend_info": {"name": "Native RPM (DNF)", "icon": "📦"} },
        { "id": "blender", "name": "Blender 3D Suite", "category": "design", "description": "Free and open source 3D creation suite.", "version": "4.3.2", "maintainer": "Blender Foundation", "license": "GPLv3", "icon": "🎨", "backend": "flatpak", "size_mb": 450, "installed": false, "favorite": false, "backend_info": {"name": "Flatpak (Flathub)", "icon": "🧊"} }
    ]

    property var statsData: (typeof softwareCenterBridge !== "undefined" && softwareCenterBridge.stats) ? softwareCenterBridge.stats : {
        "total_packages": 28, "installed_count": 8, "favorites_count": 6, "categories_count": 15
    }

    Connections {
        target: (typeof softwareCenterBridge !== "undefined") ? softwareCenterBridge : null
        function onPackagesChanged() { root.packagesData = softwareCenterBridge.packagesList; }
        function onStatsChanged() { root.statsData = softwareCenterBridge.stats; }
    }

    Row {
        anchors.fill: parent

        // 1. LEFT SIDEBAR: Categories & Navigation
        Rectangle {
            width: 240
            height: parent.height
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1

            Column {
                anchors.fill: parent
                anchors.margins: 14
                spacing: 6

                // App Brand
                Row {
                    spacing: 10
                    Text { text: "🛍️"; font.pixelSize: 22; anchors.verticalCenter: parent.verticalCenter }
                    Column {
                        Text { text: "Software Center"; font.pixelSize: 14; font.bold: true; color: NexusTheme.primaryText }
                        Text { text: "Developer Ecosystem"; font.pixelSize: 10; color: NexusTheme.secondaryText }
                    }
                }

                Item { width: 1; height: 10 }

                // Quick Filters
                Rectangle {
                    width: parent.width
                    height: 32
                    radius: NexusTheme.radiusSmall
                    color: root.selectedCategory === "all" ? NexusTheme.accentSubtle : "transparent"
                    border.color: root.selectedCategory === "all" ? NexusTheme.accent : "transparent"
                    border.width: 1
                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        spacing: 10
                        Text { text: "🌐"; font.pixelSize: 13; anchors.verticalCenter: parent.verticalCenter }
                        Text { text: "All Packages (" + root.statsData.total_packages + ")"; font.pixelSize: 11; font.bold: root.selectedCategory === "all"; color: root.selectedCategory === "all" ? NexusTheme.accent : NexusTheme.primaryText; anchors.verticalCenter: parent.verticalCenter }
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            root.selectedCategory = "all";
                            if (typeof softwareCenterBridge !== "undefined") softwareCenterBridge.selectCategory("all");
                        }
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 32
                    radius: NexusTheme.radiusSmall
                    color: root.selectedCategory === "installed_view" ? NexusTheme.successSubtle : "transparent"
                    border.color: root.selectedCategory === "installed_view" ? NexusTheme.success : "transparent"
                    border.width: 1
                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        spacing: 10
                        Text { text: "✅"; font.pixelSize: 13; anchors.verticalCenter: parent.verticalCenter }
                        Text { text: "Installed (" + root.statsData.installed_count + ")"; font.pixelSize: 11; font.bold: root.selectedCategory === "installed_view"; color: root.selectedCategory === "installed_view" ? NexusTheme.success : NexusTheme.primaryText; anchors.verticalCenter: parent.verticalCenter }
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            root.selectedCategory = "installed_view";
                            if (typeof softwareCenterBridge !== "undefined") softwareCenterBridge.selectCategory("installed_view");
                        }
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 32
                    radius: NexusTheme.radiusSmall
                    color: root.selectedCategory === "favorites_view" ? NexusTheme.accentSubtle : "transparent"
                    border.color: root.selectedCategory === "favorites_view" ? NexusTheme.accent : "transparent"
                    border.width: 1
                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        spacing: 10
                        Text { text: "⭐"; font.pixelSize: 13; anchors.verticalCenter: parent.verticalCenter }
                        Text { text: "Favorites (" + root.statsData.favorites_count + ")"; font.pixelSize: 11; font.bold: root.selectedCategory === "favorites_view"; color: root.selectedCategory === "favorites_view" ? NexusTheme.accent : NexusTheme.primaryText; anchors.verticalCenter: parent.verticalCenter }
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            root.selectedCategory = "favorites_view";
                            if (typeof softwareCenterBridge !== "undefined") softwareCenterBridge.selectCategory("favorites_view");
                        }
                    }
                }

                Item { width: 1; height: 10 }
                Text { text: "CATEGORIES"; font.pixelSize: 10; font.bold: true; color: NexusTheme.secondaryText }

                // Category Items ScrollView
                ScrollView {
                    width: parent.width
                    height: parent.height - 240
                    clip: true

                    Column {
                        width: parent.width - 10
                        spacing: 2

                        Repeater {
                            model: root.categoriesData

                            delegate: Rectangle {
                                width: parent.width
                                height: 30
                                radius: NexusTheme.radiusSmall
                                visible: modelData.id !== "all"
                                color: root.selectedCategory === modelData.id ? NexusTheme.secondaryBackground : "transparent"
                                border.color: root.selectedCategory === modelData.id ? NexusTheme.accent : "transparent"
                                border.width: 1

                                Row {
                                    anchors.fill: parent
                                    anchors.leftMargin: 10
                                    spacing: 8
                                    Text { text: modelData.icon; font.pixelSize: 12; anchors.verticalCenter: parent.verticalCenter }
                                    Text {
                                        text: modelData.name
                                        font.pixelSize: 11
                                        color: root.selectedCategory === modelData.id ? NexusTheme.accent : NexusTheme.secondaryText
                                        anchors.verticalCenter: parent.verticalCenter
                                    }
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        root.selectedCategory = modelData.id;
                                        if (typeof softwareCenterBridge !== "undefined") softwareCenterBridge.selectCategory(modelData.id);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // 2. RIGHT MAIN VIEW: Header, Search, and Packages Grid
        Rectangle {
            width: parent.width - 240
            height: parent.height
            color: NexusTheme.background

            Column {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 16

                // Top Search Bar
                Row {
                    width: parent.width
                    spacing: 16

                    Rectangle {
                        width: Math.min(420, parent.width - 200)
                        height: 38
                        radius: NexusTheme.radiusSmall
                        color: NexusTheme.surface
                        border.color: NexusTheme.border
                        border.width: 1

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 12
                            anchors.rightMargin: 12
                            spacing: 8

                            Text { text: "🔍"; font.pixelSize: 14; anchors.verticalCenter: parent.verticalCenter }

                            TextInput {
                                id: searchInput
                                anchors.verticalCenter: parent.verticalCenter
                                width: parent.width - 40
                                font.pixelSize: 12
                                color: NexusTheme.primaryText
                                clip: true

                                Text {
                                    anchors.verticalCenter: parent.verticalCenter
                                    text: "Search packages, tools, languages, databases..."
                                    font.pixelSize: 12
                                    color: NexusTheme.secondaryText
                                    visible: !searchInput.text
                                }

                                onTextChanged: {
                                    root.searchQuery = searchInput.text;
                                    if (typeof softwareCenterBridge !== "undefined") {
                                        softwareCenterBridge.search(searchInput.text);
                                    }
                                }
                            }
                        }
                    }

                    Item { width: Math.max(10, parent.width - 700); height: 1 }

                    // Safety Architecture Pill
                    Rectangle {
                        height: 38
                        width: 250
                        radius: NexusTheme.radiusPill
                        color: NexusTheme.surface
                        border.color: NexusTheme.border
                        border.width: 1

                        Row {
                            anchors.centerIn: parent
                            spacing: 8
                            Text { text: "🛡️"; font.pixelSize: 13 }
                            Text {
                                text: "Polkit Verified • Multi-Backend"
                                font.pixelSize: 11
                                font.bold: true
                                color: NexusTheme.secondaryText
                            }
                        }
                    }
                }

                // Packages Grid / List ScrollView
                ScrollView {
                    width: parent.width
                    height: parent.height - 70
                    clip: true

                    Column {
                        width: parent.width - 16
                        spacing: 10

                        Repeater {
                            model: root.packagesData

                            delegate: Rectangle {
                                width: parent.width
                                height: 84
                                radius: NexusTheme.radiusMedium
                                color: NexusTheme.surface
                                border.color: modelData.installed ? NexusTheme.success : NexusTheme.border
                                border.width: 1

                                Row {
                                    anchors.fill: parent
                                    anchors.leftMargin: 18
                                    anchors.rightMargin: 18
                                    spacing: 16

                                    Text {
                                        text: modelData.icon || "📦"
                                        font.pixelSize: 28
                                        anchors.verticalCenter: parent.verticalCenter
                                    }

                                    Column {
                                        anchors.verticalCenter: parent.verticalCenter
                                        spacing: 3
                                        width: Math.max(250, parent.width - 480)

                                        Row {
                                            spacing: 8
                                            Text {
                                                text: modelData.name
                                                font.pixelSize: 14
                                                font.bold: true
                                                color: NexusTheme.primaryText
                                            }

                                            // Backend Badge
                                            Rectangle {
                                                height: 18
                                                width: backendLabel.implicitWidth + 10
                                                radius: NexusTheme.radiusPill
                                                color: NexusTheme.secondaryBackground
                                                border.color: NexusTheme.border
                                                border.width: 1
                                                anchors.verticalCenter: parent.verticalCenter
                                                Text {
                                                    id: backendLabel
                                                    anchors.centerIn: parent
                                                    text: (modelData.backend_info ? modelData.backend_info.icon + " " + modelData.backend_info.name : modelData.backend).toUpperCase()
                                                    font.pixelSize: 9
                                                    font.bold: true
                                                    color: NexusTheme.secondaryText
                                                }
                                            }

                                            // Installed Badge
                                            Rectangle {
                                                height: 18
                                                width: instBadge.implicitWidth + 10
                                                radius: NexusTheme.radiusPill
                                                color: modelData.installed ? NexusTheme.successSubtle : NexusTheme.secondaryBackground
                                                border.color: modelData.installed ? NexusTheme.success : NexusTheme.border
                                                border.width: 1
                                                anchors.verticalCenter: parent.verticalCenter
                                                Text {
                                                    id: instBadge
                                                    anchors.centerIn: parent
                                                    text: modelData.installed ? "INSTALLED v" + modelData.version : "v" + modelData.version
                                                    font.pixelSize: 9
                                                    font.bold: true
                                                    color: modelData.installed ? NexusTheme.success : NexusTheme.secondaryText
                                                }
                                            }
                                        }

                                        Text {
                                            text: modelData.description
                                            font.pixelSize: 11
                                            color: NexusTheme.secondaryText
                                            elide: Text.ElideRight
                                            width: parent.width
                                        }

                                        Text {
                                            text: modelData.maintainer + " • License: " + modelData.license + " • Size: " + modelData.size_mb + " MB"
                                            font.pixelSize: 10
                                            color: NexusTheme.secondaryText
                                        }
                                    }

                                    Item { width: 10; height: 1 }

                                    // Action Buttons Strip
                                    Row {
                                        anchors.verticalCenter: parent.verticalCenter
                                        spacing: 8

                                        // Favorite Star Button
                                        Rectangle {
                                            width: 32
                                            height: 32
                                            radius: NexusTheme.radiusSmall
                                            color: NexusTheme.secondaryBackground
                                            border.color: NexusTheme.border
                                            border.width: 1

                                            Text {
                                                anchors.centerIn: parent
                                                text: modelData.favorite ? "⭐" : "☆"
                                                font.pixelSize: 14
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    if (typeof softwareCenterBridge !== "undefined") {
                                                        softwareCenterBridge.toggleFavorite(modelData.id);
                                                    }
                                                }
                                            }
                                        }

                                        // Details Button
                                        Rectangle {
                                            width: 65
                                            height: 32
                                            radius: NexusTheme.radiusSmall
                                            color: NexusTheme.secondaryBackground
                                            border.color: NexusTheme.border
                                            border.width: 1

                                            Text {
                                                anchors.centerIn: parent
                                                text: "Details"
                                                font.pixelSize: 11
                                                color: NexusTheme.primaryText
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    root.activeModalPackage = modelData;
                                                    root.showDetailModal = true;
                                                }
                                            }
                                        }

                                        // Install / Uninstall Action Button
                                        Rectangle {
                                            width: 85
                                            height: 32
                                            radius: NexusTheme.radiusSmall
                                            color: modelData.installed ? NexusTheme.errorSubtle : NexusTheme.accentSubtle
                                            border.color: modelData.installed ? NexusTheme.error : NexusTheme.accent
                                            border.width: 1

                                            Text {
                                                anchors.centerIn: parent
                                                text: modelData.installed ? "Remove" : "Install"
                                                font.pixelSize: 11
                                                font.bold: true
                                                color: modelData.installed ? NexusTheme.error : NexusTheme.accent
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                cursorShape: Qt.PointingHandCursor
                                                onClicked: {
                                                    if (typeof softwareCenterBridge !== "undefined") {
                                                        if (modelData.installed) {
                                                            softwareCenterBridge.uninstallPackage(modelData.id);
                                                        } else {
                                                            softwareCenterBridge.installPackage(modelData.id, "");
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // Modal: Detailed Package Inspector
    Rectangle {
        anchors.fill: parent
        color: "#80000000"
        visible: root.showDetailModal

        Rectangle {
            anchors.centerIn: parent
            width: 620
            height: 480
            radius: NexusTheme.radiusLarge
            color: NexusTheme.surface
            border.color: NexusTheme.border
            border.width: 1

            Column {
                anchors.fill: parent
                anchors.margins: 24
                spacing: 14

                Row {
                    width: parent.width
                    Text { text: root.activeModalPackage ? root.activeModalPackage.icon : "📦"; font.pixelSize: 28; anchors.verticalCenter: parent.verticalCenter }
                    Item { width: 12; height: 1 }
                    Column {
                        anchors.verticalCenter: parent.verticalCenter
                        Text { text: root.activeModalPackage ? root.activeModalPackage.name : ""; font.pixelSize: 16; font.bold: true; color: NexusTheme.primaryText }
                        Text { text: root.activeModalPackage ? ("Maintainer: " + root.activeModalPackage.maintainer) : ""; font.pixelSize: 11; color: NexusTheme.secondaryText }
                    }
                    Item { width: Math.max(10, parent.width - 400); height: 1 }
                    Text {
                        text: "✕"
                        font.pixelSize: 18
                        color: NexusTheme.secondaryText
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: root.showDetailModal = false
                        }
                    }
                }

                Text {
                    text: root.activeModalPackage ? (root.activeModalPackage.long_description || root.activeModalPackage.description) : ""
                    font.pixelSize: 12
                    color: NexusTheme.primaryText
                    wrapMode: Text.Wrap
                    width: parent.width
                }

                // Metadata Details Box
                Rectangle {
                    width: parent.width
                    height: 90
                    radius: NexusTheme.radiusSmall
                    color: NexusTheme.secondaryBackground
                    border.color: NexusTheme.border
                    border.width: 1

                    Grid {
                        anchors.fill: parent
                        anchors.margins: 12
                        columns: 2
                        spacing: 10

                        Text { text: "Version: " + (root.activeModalPackage ? root.activeModalPackage.version : ""); font.pixelSize: 11; color: NexusTheme.secondaryText }
                        Text { text: "License: " + (root.activeModalPackage ? root.activeModalPackage.license : ""); font.pixelSize: 11; color: NexusTheme.secondaryText }
                        Text { text: "Size: " + (root.activeModalPackage ? (root.activeModalPackage.size_mb + " MB") : ""); font.pixelSize: 11; color: NexusTheme.secondaryText }
                        Text { text: "Backend: " + (root.activeModalPackage ? root.activeModalPackage.backend.toUpperCase() : ""); font.pixelSize: 11; color: NexusTheme.secondaryText }
                    }
                }

                Text { text: "Prerequisite System Dependencies:"; font.pixelSize: 11; font.bold: true; color: NexusTheme.primaryText }

                Text {
                    text: (root.activeModalPackage && root.activeModalPackage.dependencies) ? root.activeModalPackage.dependencies.join(", ") : "Standard C runtime (glibc)"
                    font.pixelSize: 11
                    font.family: NexusTheme.fontFamilyMono
                    color: NexusTheme.accent
                }

                Item { width: 1; height: 10 }

                // Action Buttons
                Row {
                    width: parent.width
                    spacing: 12

                    Rectangle {
                        width: 120
                        height: 36
                        radius: NexusTheme.radiusSmall
                        color: (root.activeModalPackage && root.activeModalPackage.installed) ? NexusTheme.errorSubtle : NexusTheme.accentSubtle
                        border.color: (root.activeModalPackage && root.activeModalPackage.installed) ? NexusTheme.error : NexusTheme.accent
                        border.width: 1

                        Text {
                            anchors.centerIn: parent
                            text: (root.activeModalPackage && root.activeModalPackage.installed) ? "Uninstall Package" : "Install Package"
                            font.pixelSize: 11
                            font.bold: true
                            color: (root.activeModalPackage && root.activeModalPackage.installed) ? NexusTheme.error : NexusTheme.accent
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                if (typeof softwareCenterBridge !== "undefined" && root.activeModalPackage) {
                                    if (root.activeModalPackage.installed) {
                                        softwareCenterBridge.uninstallPackage(root.activeModalPackage.id);
                                    } else {
                                        softwareCenterBridge.installPackage(root.activeModalPackage.id, "");
                                    }
                                    root.showDetailModal = false;
                                }
                            }
                        }
                    }

                    Rectangle {
                        width: 100
                        height: 36
                        radius: NexusTheme.radiusSmall
                        color: NexusTheme.secondaryBackground
                        border.color: NexusTheme.border
                        border.width: 1

                        Text {
                            anchors.centerIn: parent
                            text: "Close"
                            font.pixelSize: 11
                            color: NexusTheme.primaryText
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: root.showDetailModal = false
                        }
                    }
                }
            }
        }
    }
}
