import QtQuick
import QtQuick.Controls

Rectangle {
    id: terminalRoot
    color: NexusTheme.isDark ? "#0A0D14" : "#F8FAFC"

    property var history: [
        { type: "sys", text: "NEXUS OS Kernel 6.12.8-nexus • Wayland (KWin 6)" },
        { type: "sys", text: "Connected to nexus-aid daemon at http://localhost:11430/v1" },
        { type: "prompt", text: "nexus@workstation:~/Projects/nexus-os (main) $" },
        { type: "out", text: "Type 'help' to view available system and developer commands." }
    ]

    Column {
        anchors.fill: parent
        anchors.margins: 14
        spacing: 4

        // Output history
        Flickable {
            id: flick
            width: parent.width
            height: parent.height - 34
            contentWidth: width
            contentHeight: historyCol.implicitHeight
            clip: true

            Column {
                id: historyCol
                width: parent.width
                spacing: 3

                Repeater {
                    model: terminalRoot.history

                    delegate: Text {
                        width: historyCol.width
                        text: modelData.text
                        font.family: NexusTheme.fontFamilyMono
                        font.pixelSize: 12
                        color: {
                            if (modelData.type === "sys") return NexusTheme.secondaryText;
                            if (modelData.type === "prompt") return NexusTheme.accent;
                            if (modelData.type === "err") return NexusTheme.error;
                            return NexusTheme.primaryText;
                        }
                        wrapMode: Text.Wrap
                    }
                }
            }

            onContentHeightChanged: flick.contentY = Math.max(0, contentHeight - height)
        }

        // Prompt input line
        Row {
            width: parent.width
            height: 26
            spacing: 6

            Text {
                text: "nexus@dev:~$ "
                font.family: NexusTheme.fontFamilyMono
                font.pixelSize: 12
                font.bold: true
                color: NexusTheme.accent
                anchors.verticalCenter: parent.verticalCenter
            }

            TextInput {
                id: cmdInput
                width: parent.width - 120
                font.family: NexusTheme.fontFamilyMono
                font.pixelSize: 12
                color: NexusTheme.primaryText
                selectByMouse: true
                anchors.verticalCenter: parent.verticalCenter
                focus: true

                onAccepted: {
                    var cmd = text.trim();
                    if (cmd === "") return;

                    var newHist = [].concat(terminalRoot.history);
                    newHist.push({ type: "prompt", text: "nexus@dev:~$ " + cmd });

                    if (cmd === "help") {
                        newHist.push({ type: "out", text: "Available commands: help, clear, uname, cargo build, podman ps, ollama ps, nexus-ai" });
                    } else if (cmd === "clear") {
                        newHist = [];
                    } else if (cmd === "uname" || cmd === "uname -a") {
                        newHist.push({ type: "out", text: "Linux nexus-workstation 6.12.8-nexus x86_64 GNU/Linux" });
                    } else if (cmd === "podman ps") {
                        newHist.push({ type: "out", text: "CONTAINER ID  IMAGE                     STATUS         PORTS\n4a81c20e      quay.io/fedora/dev:41     Up 2 hours     0.0.0.0:3000->3000/tcp\n91e2fa01      docker.io/library/postgres Up 4 hours    0.0.0.0:5432->5432/tcp" });
                    } else if (cmd === "ollama ps") {
                        newHist.push({ type: "out", text: "NAME                  ID            SIZE      PROCESSOR    UNTIL\nqwen2.5-coder:7b      d6350f24      4.7 GB    100% GPU     14m42s" });
                    } else if (cmd === "nexus-ai") {
                        newHist.push({ type: "out", text: "NEXUS AI Core: Active\nEndpoint: http://localhost:11430/v1\nLoaded: qwen2.5-coder:7b (VRAM: 4.2GB / 8GB)" });
                    } else if (cmd === "cargo build") {
                        newHist.push({ type: "out", text: "   Compiling nexus-aid v0.1.0\n   Compiling nexus-spotlight v0.1.0\n    Finished dev [unoptimized + debuginfo] target(s) in 2.14s" });
                    } else {
                        newHist.push({ type: "err", text: "Command not found: " + cmd + ". Type 'help' for options." });
                    }

                    terminalRoot.history = newHist;
                    text = "";
                }
            }
        }
    }
}
