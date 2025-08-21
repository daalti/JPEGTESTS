import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0
import QtQml.Models 2.15


MenuTextImageBranch
{
    id:paperSizeSelection
    objectName: "copy_mediaSizeSettingsTextImage"
    property ISpiceModel resourceModel: null;
    property QtObject checkCopyOptionAvailability: CheckCopyMoreOptionAvailability{}

    function textString() 
    {
        var typeValue = [
            { 
                "type" : "dune::spice::glossary_1::MediaSize::MediaSize",
                "value": resourceModel.data.dest.print.mediaSize,
                "option": "copy_mediaSize",
                "propertyPointer":"src/scan/mediaSize"
            }
        ]

        var textArray = []
        typeValue.forEach(function(element) {               
            if(checkCopyOptionAvailability.checkAvailability(element.option) && _stateMachine.controller.findValidatorForConstraint(element.propertyPointer)!=null) 
            { 
                textArray.push(textForValue(element.type, element.value)) 
            }
        })

        return textArray.join(", ")
    }

    function textForValue(type, value)
    {
        if(type === "dune::spice::glossary_1::MediaSize::MediaSize" && value == Glossary_1_MediaSize.MediaSize.any )
        {
            // "any" of "dest/print/mediaSize" should be shown as "Match Original Size" in Enterprise Copy.
            return _qmlUtils.createSpiceLoc( paperSizeSelection ,{"stringId":"StringIds.cMatchOriginalSize"}).text
        }
        return _qmlUtils.createSpiceLoc( paperSizeSelection ,{"stringId":_propertyMap.cStringIDForEnum(type, value)}).text
    }

    function recomputeValue(){
        console.log("copy paper size selection value changed")
        paperSizeSelection.controlModel.secondInfoText.text = textString()
    }

    function setValue(){
        recomputeValue()
        resourceModel.data.dest.print.mediaSizeChanged.connect(recomputeValue)
    }

    Component.onCompleted: {
        Qt.callLater(setValue)
    }

    Component.onDestruction: {
        console.log("copy paper size selection disconnect")
        resourceModel.data.dest.print.mediaSizeChanged.disconnect(recomputeValue)
    }
}
