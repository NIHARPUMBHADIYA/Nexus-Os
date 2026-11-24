import QtQuick

Item {
    id: root

    property string variant: "linear" // "linear", "spinner"
    property real value: 0.5 // 0.0 to 1.0
    property bool indeterminate: false
    property color progressColor: NexusTheme.accent
    property int spinnerSize: 32

    implicitWidth: variant === "linear" ? 220 : spinnerSize
    implicitHeight: variant === "linear" ? 8 : spinnerSize

    // Linear Progress Bar
    Rectangle {
        visible: root.variant === "linear"
        anchors.fill: parent
        radius: height / 2
        color: NexusTheme.secondaryBackground
        border.color: NexusTheme.border
        border.width: 1
        clip: true

        Rectangle {
            id: barFill
            visible: !root.indeterminate
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            width: parent.width * Math.min(Math.max(root.value, 0.0), 1.0)
            radius: height / 2
            color: root.progressColor

            Behavior on width {
                NumberAnimation { duration: NexusTheme.durationNormal; easing.type: Easing.OutQuad }
            }
        }

        // Indeterminate wave
        Rectangle {
            id: waveFill
            visible: root.indeterminate
            width: parent.width * 0.35
            height: parent.height
            radius: height / 2
            color: root.progressColor

            SequentialAnimation on x {
                loops: Animation.Infinite
                running: root.variant === "linear" && root.indeterminate && !NexusTheme.reducedMotion
                NumberAnimation { from: -waveFill.width; to: root.width; duration: 1200; easing.type: Easing.InOutQuad }
            }
        }
    }

    // Circular Spinner
    Item {
        visible: root.variant === "spinner"
        anchors.fill: parent

        Rectangle {
            anchors.fill: parent
            radius: width / 2
            color: "transparent"
            border.color: NexusTheme.border
            border.width: 3
        }

        Rectangle {
            width: parent.width
            height: parent.height
            radius: width / 2
            color: "transparent"
            border.color: root.progressColor
            border.width: 3
            clip: true

            Rectangle {
                width: parent.width
                height: parent.height / 2
                color: NexusTheme.background
            }
        }

        RotationAnimation on rotation {
            loops: Animation.Infinite
            from: 0
            to: 360
            duration: 1000
            running: root.variant === "spinner" && !NexusTheme.reducedMotion
        }
    }
}
