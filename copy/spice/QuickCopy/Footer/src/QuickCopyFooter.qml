import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQml.Models 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0


RowLayout{
    id: copyQuickFooter
    objectName: "copyQuickFooter"
    Layout.fillWidth: true
    Layout.alignment: Qt.AlignRight
    spacing: Global.breakpoint <= Global.BreakPoint.S ? SpiceSpacerViewConstants.sp4_height : SpiceSpacerViewConstants.sp5_height
    

    property QtObject copyController: QuickCopyController {};
    property int numberOfCopiesMin: 1
    property int numberOfCopiesMax: 999
    property int numberOfCopies: quickCopySpinBox.value
    property bool copyButtonEnabled: true

    signal copyClicked(int numberOfCopies);

    SpiceSpinBox{
        id: quickCopySpinBox
        objectName: "quickCopySpinBox"
        Layout.alignment: Qt.AlignRight
        value: copyQuickFooter.numberOfCopies
        from: copyQuickFooter.numberOfCopiesMin
        to: copyQuickFooter.numberOfCopiesMax
        permissionId:"ef92c290-8fa5-4403-85bc-f6becc86b787"
        variation: Global.breakpoint <= Global.BreakPoint.S ? SpiceSpinBox.Variation.Compact : SpiceSpinBox.Variation.Basic
    }

    // // Right aligned, Quick Copy Buttonr
    SpiceButton{
        id: copyButton
        objectName: "QuickCopyButton"
        Layout.alignment: Qt.AlignRight
        Layout.rightMargin: Global.breakpoint <= Global.BreakPoint.S ? SpiceSpacerViewConstants.sp4_height : SpiceSpacerViewConstants.sp5_height
        enabled: copyQuickFooter.copyButtonEnabled
        permissionId:"ef92c290-8fa5-4403-85bc-f6becc86b787" 
        type: SpiceButton.Type.Primary
        variation:SpiceButton.ButtonVariation.VariationOne
        textObject.stringId:Global.breakpoint <= Global.BreakPoint.S ? "" : "StringIds.cQuickCopy"
        icon:Global.breakpoint < Global.BreakPoint.S?"":"qrc:/images/Glyph/InstantLaunch.json"
        onClicked:{
            console.log("Quick copy Button clicked")
            copyQuickFooter.copyClicked(numberOfCopies)
        }
    }

    function resetNumberOfCopies()
    {
        console.log("quick copy footer resetNumberOfCopies")
        quickCopySpinBox.value = 1
    }


    Component.onCompleted: {
        console.log("quick copy footer completed")
        _inactivityTimer.fired.connect(resetNumberOfCopies)
        _resetSession.fired.connect(resetNumberOfCopies)
        copyQuickFooter.numberOfCopiesMax = Qt.binding(function(){return copyQuickFooter.copyController.numberOfCopiesMax})
        copyQuickFooter.numberOfCopiesMin = Qt.binding(function(){return copyQuickFooter.copyController.numberOfCopiesMin})
        copyQuickFooter.copyButtonEnabled = Qt.binding(function(){return copyQuickFooter.copyController.copyEnabled})
        copyQuickFooter.copyClicked.connect(function(val)
        {
            console.log("Quick Copy, Copy Button Clicked, ncopies:" + val);
            copyController.numCopies = val
            copyController.startCopy()
        });
        copyController.subscribeScannerStatus()
        copyController.getConstraintModel()
    }

    Component.onDestruction: {
        _inactivityTimer.fired.disconnect(resetNumberOfCopies)
        _resetSession.fired.disconnect(resetNumberOfCopies)
        copyController.unsubscribeScannerStatus()
    }
}