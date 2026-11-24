import QtQuick
import QtQuick.Controls

Rectangle {
    id: editorRoot
    color: NexusTheme.isDark ? "#0D1117" : "#FFFFFF"

    Column {
        anchors.fill: parent
        spacing: 0

        // File Tab Bar
        Rectangle {
            width: parent.width
            height: 34
            color: NexusTheme.secondaryBackground
            border.color: NexusTheme.border
            border.width: 1

            Row {
                anchors.fill: parent
                anchors.leftMargin: 8

                Rectangle {
                    width: 140
                    height: 34
                    color: editorRoot.color
                    border.color: NexusTheme.border
                    border.width: 1

                    Row {
                        anchors.centerIn: parent
                        spacing: 6
                        Text { text: "🦀"; font.pixelSize: 12 }
                        Text { text: "main.rs"; font.pixelSize: 12; font.family: NexusTheme.fontFamilyMono; color: NexusTheme.primaryText }
                    }
                }
            }
        }

        // Code Editor Viewport
        Row {
            width: parent.width
            height: parent.height - 34 - 24

            // Line numbers column
            Rectangle {
                width: 44
                height: parent.height
                color: NexusTheme.secondaryBackground

                Column {
                    anchors.fill: parent
                    anchors.topMargin: 10
                    spacing: 4

                    Repeater {
                        model: 16
                        delegate: Text {
                            text: (index + 1)
                            font.pixelSize: 12
                            font.family: NexusTheme.fontFamilyMono
                            color: NexusTheme.tertiaryText
                            anchors.right: parent.right
                            anchors.rightMargin: 8
                        }
                    }
                }
            }

            // Code Text Area
            Flickable {
                width: parent.width - 44
                height: parent.height
                contentWidth: width
                contentHeight: codeText.implicitHeight + 20
                clip: true

                TextEdit {
                    id: codeText
                    width: parent.width - 20
                    anchors.margins: 10
                    font.family: NexusTheme.fontFamilyMono
                    font.pixelSize: 12
                    color: NexusTheme.primaryText
                    text: "// NEXUS OS AI Core Entrypoint\nuse tokio::net::TcpListener;\nuse nexus_aid::config::NexusAIConfig;\n\n#[tokio::main]\nasync fn main() -> anyhow::Result<()> {\n    tracing::info!(\"Initializing NEXUS OS AI Core...\");\n    let config = NexusAIConfig::default();\n    \n    // Start OpenAI-compatible reverse proxy\n    nexus_aid::proxy::start_proxy(config).await?;\n    Ok(())\n}"
                    wrapMode: TextEdit.NoWrap
                    selectByMouse: true
                }
            }
        }

        // Bottom Status Bar
        Rectangle {
            width: parent.width
            height: 24
            color: NexusTheme.secondaryBackground
            border.color: NexusTheme.border
            border.width: 1

            Row {
                anchors.fill: parent
                anchors.leftMargin: 12
                anchors.rightMargin: 12
                spacing: 16

                Text { text: "Rust • UTF-8 • LF"; font.pixelSize: 11; font.family: NexusTheme.fontFamilyMono; color: NexusTheme.secondaryText; anchors.verticalCenter: parent.verticalCenter }
                Item { width: 10; height: 1 }
                Text { text: "Spaces: 4 • Ln 1, Col 1"; font.pixelSize: 11; font.family: NexusTheme.fontFamilyMono; color: NexusTheme.secondaryText; anchors.verticalCenter: parent.verticalCenter }
            }
        }
    }
}
