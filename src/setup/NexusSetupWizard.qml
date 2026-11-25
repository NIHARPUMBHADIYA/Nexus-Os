import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../design-system/qml"

Rectangle {
    id: root
    width: 680
    height: 640
    color: NexusTheme.background
    radius: NexusTheme.radiusLarge
    border.color: NexusTheme.border
    border.width: 1

    property bool isSuccess: false
    property string createdUser: ""

    Connections {
        target: setupBridge
        function onSetupCompleted(username) {
            root.createdUser = username
            root.isSuccess = true
            closeTimer.start()
        }
    }

    Timer {
        id: closeTimer
        interval: 2200
        repeat: false
        onTriggered: {
            if (typeof setupWindow !== "undefined" && setupWindow.close) {
                setupWindow.close()
            } else {
                Qt.quit()
            }
        }
    }

    // Background Subtle Radial Gradient Effect
    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        color: "transparent"
        opacity: 0.15

        Rectangle {
            width: 320
            height: 320
            radius: 160
            color: NexusTheme.accent
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: -80
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 36
        spacing: 20

        // =====================================================================
        // HEADER / LOGO SECTION
        // =====================================================================
        RowLayout {
            Layout.fillWidth: true
            spacing: 16

            Rectangle {
                width: 52
                height: 52
                radius: NexusTheme.radiusMedium
                color: NexusTheme.accentSubtle
                border.color: NexusTheme.accent
                border.width: 1.5

                Text {
                    anchors.centerIn: parent
                    text: "⚡"
                    font.pixelSize: 26
                }
            }

            ColumnLayout {
                spacing: 2

                Text {
                    text: "NEXUS OS 2026.1"
                    font.pixelSize: 20
                    font.weight: Font.Bold
                    color: NexusTheme.textPrimary
                }

                Text {
                    text: root.isSuccess ? "Setup Complete" : "First-Boot Local Account Setup"
                    font.pixelSize: 13
                    color: NexusTheme.textSecondary
                }
            }

            Item { Layout.fillWidth: true }

            NexusBadge {
                text: "Fedora 41"
                variant: "subtle"
            }
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: NexusTheme.border
        }

        // =====================================================================
        // SUCCESS VIEW
        // =====================================================================
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: root.isSuccess
            alignment: Qt.AlignCenter
            spacing: 16

            Rectangle {
                Layout.alignment: Qt.AlignHCenter
                width: 72
                height: 72
                radius: 36
                color: NexusTheme.success
                opacity: 0.9

                Text {
                    anchors.centerIn: parent
                    text: "✓"
                    font.pixelSize: 36
                    font.weight: Font.Bold
                    color: "#FFFFFF"
                }
            }

            Text {
                Layout.alignment: Qt.AlignHCenter
                text: "Welcome, " + root.createdUser + "!"
                font.pixelSize: 22
                font.weight: Font.Bold
                color: NexusTheme.textPrimary
            }

            Text {
                Layout.alignment: Qt.AlignHCenter
                text: "Your administrator account has been created successfully.\nStarting NEXUS OS Aether Desktop..."
                font.pixelSize: 14
                horizontalAlignment: Text.AlignHCenter
                color: NexusTheme.textSecondary
            }

            NexusProgress {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 260
                indeterminate: true
            }
        }

        // =====================================================================
        // ACCOUNT CREATION FORM (Visible when not success)
        // =====================================================================
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: !root.isSuccess
            spacing: 14

            Text {
                text: "Create Your Local Administrator Account"
                font.pixelSize: 16
                font.weight: Font.DemiBold
                color: NexusTheme.textPrimary
            }

            Text {
                text: "Configure the local user credentials for your developer workstation."
                font.pixelSize: 12
                color: NexusTheme.textSecondary
            }

            // Error Banner
            Rectangle {
                Layout.fillWidth: true
                height: errorTextLabel.text !== "" ? 38 : 0
                visible: errorTextLabel.text !== ""
                radius: NexusTheme.radiusSmall
                color: NexusTheme.isDark ? "#3B1818" : "#FEE2E2"
                border.color: NexusTheme.error
                border.width: 1

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 8

                    Text {
                        text: "⚠"
                        color: NexusTheme.error
                        font.pixelSize: 14
                    }

                    Text {
                        id: errorTextLabel
                        Layout.fillWidth: true
                        text: setupBridge ? setupBridge.errorMessage : ""
                        color: NexusTheme.error
                        font.pixelSize: 12
                        elide: Text.ElideRight
                    }
                }
            }

            // Form Inputs Grid
            GridLayout {
                Layout.fillWidth: true
                columns: 2
                rowSpacing: 10
                columnSpacing: 16

                // Full Name
                Text {
                    text: "Full Name"
                    font.pixelSize: 13
                    font.weight: Font.Medium
                    color: NexusTheme.textPrimary
                }
                NexusInput {
                    id: fullNameInput
                    Layout.fillWidth: true
                    placeholderText: "e.g. Nihar Pumbhadiya"
                    onTextChanged: {
                        if (usernameInput.text === "" || usernameInput.focus === false) {
                            var parts = text.trim().toLowerCase().split(" ")
                            if (parts.length > 0 && parts[0].length > 0) {
                                usernameInput.text = parts[0].replace(/[^a-z0-9_-]/g, "")
                            }
                        }
                    }
                }

                // Username
                Text {
                    text: "Username"
                    font.pixelSize: 13
                    font.weight: Font.Medium
                    color: NexusTheme.textPrimary
                }
                NexusInput {
                    id: usernameInput
                    Layout.fillWidth: true
                    placeholderText: "e.g. nihar"
                }

                // Password
                Text {
                    text: "Password"
                    font.pixelSize: 13
                    font.weight: Font.Medium
                    color: NexusTheme.textPrimary
                }
                NexusInput {
                    id: passwordInput
                    Layout.fillWidth: true
                    isPassword: true
                    placeholderText: "Enter a strong password"
                }

                // Confirm Password
                Text {
                    text: "Confirm Password"
                    font.pixelSize: 13
                    font.weight: Font.Medium
                    color: NexusTheme.textPrimary
                }
                NexusInput {
                    id: confirmPasswordInput
                    Layout.fillWidth: true
                    isPassword: true
                    placeholderText: "Re-enter your password"
                }
            }

            // Options Checklist
            RowLayout {
                Layout.fillWidth: true
                spacing: 12
                Layout.topMargin: 4

                CheckBox {
                    id: adminCheck
                    checked: true
                    text: "Grant Administrator (sudo) privileges"
                    palette.windowText: NexusTheme.textPrimary
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 12

                CheckBox {
                    id: autologinCheck
                    checked: true
                    text: "Log in automatically without asking for password on boot"
                    palette.windowText: NexusTheme.textPrimary
                }
            }

            Item { Layout.fillHeight: true }

            // Action Buttons
            RowLayout {
                Layout.fillWidth: true
                spacing: 12

                NexusButton {
                    text: "Skip & Use Default Live User"
                    variant: "ghost"
                    size: "md"
                    onClicked: {
                        if (typeof setupWindow !== "undefined" && setupWindow.close) {
                            setupWindow.close()
                        } else {
                            Qt.quit()
                        }
                    }
                }

                Item { Layout.fillWidth: true }

                NexusButton {
                    text: "Create Account & Start NEXUS OS"
                    variant: "primary"
                    size: "lg"
                    loading: setupBridge ? setupBridge.isLoading : false
                    onClicked: {
                        if (setupBridge) {
                            setupBridge.createAccount(
                                fullNameInput.text,
                                usernameInput.text,
                                passwordInput.text,
                                confirmPasswordInput.text,
                                adminCheck.checked,
                                autologinCheck.checked
                            )
                        }
                    }
                }
            }
        }
    }
}
