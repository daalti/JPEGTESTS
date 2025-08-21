import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQuick.Layouts 1.15
import QtQml.Models 2.15
import security 1.0
import inactivityTimeout 1.0

SpiceGridLayout {
    id: smallScreenCopyQuickWidget
    objectName: "CopyWidget"
    property int numberOfCopiesMin
    property int numberOfCopiesMax
    property int numberOfCopies:1
    signal copyClicked(int numberOfCopies);
    signal settingClicked(int numberOfCopies);
    property bool copyButtonEnabled: false
    property bool copybuttonConstrained :false
    property QQmlObjectListModel widgetInfoText:QQmlObjectListModel{}
    property QQmlObjectListModel widgetProperty: QQmlObjectListModel{}
    property SpiceLocObject copyConstrainedMessage: SpiceLocObject{
        stringId: "StringIds.cInsertPageInScanner"
    }
    onCopyButtonEnabledChanged: {
        console.log("copy button enabled changed", copyButtonEnabled)
    }

    width: parent.width
    height: parent.height
    topMargin: Global.rem
    bottomMargin: Global.rem
    leftMargin: Global.rem
    rightMargin: Global.rem
    gutterHorizontal:0.5 * Global.rem
    gutterVertical: 0.5 * Global.rem

    maxItemsPerRow: 2
    behavior: SpiceGridLayout.Behavior.Fluid
    Layout.fillWidth: true

    items: ObjectModel {
        //spiceSpinBox will need textfield only mode later on to support XS display(Waiting on view framework for this feature)
        SpiceSpinBox {
            Layout.alignment: Qt.AlignLeft
            width: content.width
            id : copyWidgetSpinBox
            objectName: "copyWidgetSpinBox"
            value: smallScreenCopyQuickWidget.numberOfCopies
            from: smallScreenCopyQuickWidget.numberOfCopiesMin
            to: smallScreenCopyQuickWidget.numberOfCopiesMax
            enabled: copyWidgetStartButton._permitted
            variation: Global.breakpoint > Global.BreakPoint.XS ? SpiceSpinBox.Variation.Basic : SpiceSpinBox.Variation.Compact
            onValueChanged: {
                console.log("Number of Copies changed")
                smallScreenCopyQuickWidget.numberOfCopies = value
            }
        }

        RowLayout {
            id: copyButtonsRow
            spacing: 0
            Layout.alignment: Qt.AlignRight
            SpiceButton {
                id: copyWidgetSettingsButton
                objectName: "copyWidgetSettingsButton"
                icon: "qrc:/images/Glyph/PrintMode.json"
                Layout.alignment: Qt.AlignLeft
                type: SpiceButton.Type.Secondary
                flat: true
                enabled: copyWidgetStartButton._permitted
                visible: Global.breakpoint === Global.BreakPoint.S 
                variation: SpiceButton.ButtonVariation.VariationOne
                
                onClicked: {
                    smallScreenCopyQuickWidget.settingClicked(numberOfCopies)
                    copyWidgetSpinBox.value = 1
                }
            }
            SpiceSpacer {
                enabled: copyWidgetSettingsButton.enabled
                visible: enabled
                type: SpiceSpacer.Type.SP2
            }
            SpiceButton { 
                id: copyWidgetStartButton
                objectName: "copyWidgetStartButton"
                Layout.alignment: Qt.AlignRight
                textObject: SpiceLocObject{stringId: "StringIds.cCopy"}
                enabled: smallScreenCopyQuickWidget.copyButtonEnabled
                type: SpiceButton.Type.Primary
                variation: SpiceButton.ButtonVariation.VariationOne
                permissionId:"ef92c290-8fa5-4403-85bc-f6becc86b787"
                onClicked: {
                    console.log("Copy Action button Clicked !!!")
                    if(smallScreenCopyQuickWidget.copybuttonConstrained)
                    {
                        _stack.pushModal("qrc:/components/SpiceConstraintMessage.qml",{"message": smallScreenCopyQuickWidget.copyConstrainedMessage.text})
                    }
                    else
                    {
                        smallScreenCopyQuickWidget.copyClicked(smallScreenCopyQuickWidget.numberOfCopies)
                    }
                } 
            }
        }
    }

    Component.onCompleted: {
        console.log("quick copy widget completed")
        _inactivityTimer.fired.connect(resetNumberOfCopies)
    }

    Component.onDestruction: {
        _inactivityTimer.fired.disconnect(resetNumberOfCopies)
    }

    function resetNumberOfCopies()
    {
        console.log("quick copy widget resetNumberOfCopies")
        copyWidgetSpinBox.value = 1
    }
}
