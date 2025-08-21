import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0

MenuNameValue
{
    id: copySettingResize
    objectName: "copySettingResize"
    property ISpiceModel ticketModel: null;
    property QtObject copyControllerfunctions : CopyController{}

    function textString()
    {
        var sideText = (_qmlUtils.createSpiceLoc( copySettingResize ,{stringId: "StringIds.cNone"})).text;
        let setStringID = "StringIds.cNone"

        if(ticketModel.data.pipelineOptions.scaling.scaleToFitEnabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
        {
            sideText = (_qmlUtils.createSpiceLoc( copySettingResize ,{stringId: "StringIds.cFitToPage"})).text;
            setStringID = "StringIds.cFitToPage";
        }
        else
        {
            if(ticketModel.data.pipelineOptions.scaling.xScalePercent == 91)
            {
                sideText = (_qmlUtils.createSpiceLoc( copySettingResize ,{stringId: "StringIds.cFullPageLetter"})).text;
                setStringID = "StringIds.cFullPageLetter";
            }
            else if(ticketModel.data.pipelineOptions.scaling.xScalePercent == 72)
            {
                sideText = (_qmlUtils.createSpiceLoc( copySettingResize ,{stringId: "StringIds.cLegalToLetter"})).text;
                setStringID = "StringIds.cLegalToLetter";

            }
            else if(ticketModel.data.pipelineOptions.scaling.xScalePercent == 94)
            {
                sideText = (_qmlUtils.createSpiceLoc( copySettingResize ,{stringId: "StringIds.cLettertoA4"})).text;
                setStringID = "StringIds.cLettertoA4";
            }
            else if (ticketModel.data.pipelineOptions.scaling.xScalePercent == 100)
            {
                sideText = (_qmlUtils.createSpiceLoc( copySettingResize ,{stringId: "StringIds.cNone"})).text;
                setStringID = "StringIds.cNone";
            }
            else
            {
                var customText = ticketModel.data.pipelineOptions.scaling.xScalePercent;
                console.log("Custom text in the Keyboard " + customText)
                sideText = (_qmlUtils.createSpiceLoc( copySettingResize ,{stringId: "StringIds.cCustomPara", "params": [customText]})).text;
                setStringID = "StringIds.cCustomPara";
            }
        }
        return sideText;
    }

    function recomputeValue(){
        copySettingResize.valueButton.textObject.text = textString()
    }

    Component.onCompleted: {
        ticketModel = copyControllerfunctions.getTicketModel()
        ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.connect(recomputeValue)
        ticketModel.data.pipelineOptions.scaling.scaleToFitEnabledChanged.connect(recomputeValue)
    }

    Component.onDestruction: {
        console.log(" copy setting resize disconnect")
        ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.disconnect(recomputeValue);
        ticketModel.data.pipelineOptions.scaling.scaleToFitEnabledChanged.disconnect(recomputeValue);
    }

}
