import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

RadioButtonListLayout
{
    id: resizeSettingView
    objectName: "copyResizeSettingView"
    header: SpiceLocObject {stringId: "StringIds.cOutputScale"}
    property string resizeSelected: "";
    property string customValue: ""
    property bool customEnterd: false

    property ISpiceModel ticketModel: null;
    CopyController{
        id: copyController
    }

    function resizeText()
    {
        let sideText = (_qmlUtils.createSpiceLoc( resizeSettingView,{stringId: "StringIds.cNone"}));
        let setStringID = "StringIds.cNone"

        if(ticketModel.data.pipelineOptions.scaling.scaleToFitEnabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
        {
            sideText = (_qmlUtils.createSpiceLoc( resizeSettingView,{stringId: "StringIds.cFitToPage"}));
            setStringID = "StringIds.cFitToPage";
        }
        else
        {
            if(ticketModel.data.pipelineOptions.scaling.xScalePercent == 91 && ticketModel.data.pipelineOptions.scaling.yScalePercent == 91)
            {
                sideText = (_qmlUtils.createSpiceLoc( resizeSettingView,{stringId: "StringIds.cFullPageLetter"}));
                setStringID = "StringIds.cFullPageLetter";
            }
            else if(ticketModel.data.pipelineOptions.scaling.xScalePercent == 72 && ticketModel.data.pipelineOptions.scaling.yScalePercent == 72)
            {
                sideText = (_qmlUtils.createSpiceLoc( resizeSettingView,{stringId: "StringIds.cLegalToLetter"}));
                setStringID = "StringIds.cLegalToLetter";

            }
            else if(ticketModel.data.pipelineOptions.scaling.xScalePercent == 94 && ticketModel.data.pipelineOptions.scaling.yScalePercent == 94)
            {
                sideText = (_qmlUtils.createSpiceLoc( resizeSettingView,{stringId: "StringIds.cLettertoA4"}));
                setStringID = "StringIds.cLettertoA4";
            }
            else if (ticketModel.data.pipelineOptions.scaling.xScalePercent == 100 && ticketModel.data.pipelineOptions.scaling.yScalePercent == 100)
            {
                sideText = (_qmlUtils.createSpiceLoc( resizeSettingView,{stringId: "StringIds.cNone"}));
                setStringID = "StringIds.cNone";
            }
            else
            {
                resizeSettingView.customEnterd = true
                var customText = ticketModel.data.pipelineOptions.scaling.xScalePercent;
                console.log("Custom text in the Keyboard " + customText)
                sideText = (_qmlUtils.createSpiceLoc( resizeSettingView,{stringId: "StringIds.cCustomPara", "params": [customText]}));
                setStringID = "StringIds.cCustomPara";
            }
        }
        return setStringID;
    }

    function setScaleValue(buttonStrId){
        if(buttonStrId == "StringIds.cNone")
        {
            ticketModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            ticketModel.data.pipelineOptions.scaling.xScalePercent = 100
            ticketModel.data.pipelineOptions.scaling.yScalePercent = 100
        }
        else if(buttonStrId == "StringIds.cFitToPage")
        {
            ticketModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.true_
            ticketModel.data.pipelineOptions.scaling.xScalePercent = 100
            ticketModel.data.pipelineOptions.scaling.yScalePercent = 100
        }
        else if(buttonStrId == "StringIds.cFullPageLetter")
        {
            ticketModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            ticketModel.data.pipelineOptions.scaling.xScalePercent = 91
            ticketModel.data.pipelineOptions.scaling.yScalePercent = 91
        }
        else if(buttonStrId == "StringIds.cLegalToLetter")
        {
            ticketModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            ticketModel.data.pipelineOptions.scaling.xScalePercent = 72
            ticketModel.data.pipelineOptions.scaling.yScalePercent = 72
        }
        else if(buttonStrId == "StringIds.cLettertoA4")
        {
            ticketModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            ticketModel.data.pipelineOptions.scaling.xScalePercent = 94
            ticketModel.data.pipelineOptions.scaling.yScalePercent = 94
        }
    }

    function addRadioButtonWithKeyboard(objName, buttonStrId){
        options.append(radioComponent.createObject(null,
                                                   {
                                                       "objectName": objName,
                                                       "checked":  resizeSelected == buttonStrId ? true : false,
                                                       "buttonGroup": copyResizeGroup
                                                   }))
        options.at(options.size() - 1).textObject.text = Qt.binding(function() { return resizeSettingView.customValue;})
        options.at(options.size() - 1).buttonGroup.buttons[options.size() - 1].clicked.connect(function(val)
        {
            resizeSettingView.customEnterd = true
            console.debug("CopySettingsResizeView.qml addRadioButtonWithKeyboard")
            _stack.push("qrc:/CopyApp/CopyCustomSizeKeyboardView.qml", {"ticketModel": ticketModel})
            
        })
    }

    function addRadioButton(objName, buttonStrId){
        options.append(radioComponent.createObject(null,
                                                   {
                                                       "objectName": objName,
                                                       "textObject": _qmlUtils.createSpiceLoc( resizeSettingView,{stringId: buttonStrId}),
                                                       "checked":  resizeSelected == buttonStrId ? true : false,
                                                       "buttonGroup": copyResizeGroup
                                                   }))
        options.at(options.size() - 1).buttonGroup.buttons[options.size() - 1].clicked.connect(function(val)
        {
            console.debug("CopySettingsResizeView.qml")
            setScaleValue(buttonStrId)
            console.debug("X scale is " + ticketModel.data.pipelineOptions.scaling.xScalePercent + " Y scale is " + ticketModel.data.pipelineOptions.scaling.yScalePercent)
            _resourceStore.modify(ticketModel)
            resizeSettingView.viewDone()
        })
    }

    Component {
        id: radioComponent
        RadioButtonModel {
            property string event: ""
            onClicked: {
                if (event)
                {
                    submitEvent(event)
                }
            }
        }
    }

    ButtonGroup {
        id: copyResizeGroup
    }

    function recomputeCustomValue(){
        if (resizeSettingView.customEnterd){
            resizeSettingView.customValue = _qmlUtils.createSpiceLoc( resizeSettingView,{stringId: "StringIds.cCustomPara", "params": [ticketModel.data.pipelineOptions.scaling.xScalePercent]}).text
            console.log(resizeSettingView.customValue)
        }
        else{
            resizeSettingView.customValue = _qmlUtils.createSpiceLoc( resizeSettingView,{stringId: "StringIds.cCustomPara", "params": [100]}).text
        }
        
    }
    Component.onCompleted: {

        ticketModel = copyController.getTicketModel()
        resizeSelected = resizeText()
        recomputeCustomValue()
        console.debug("Resize Component Start")
        addRadioButton("None", "StringIds.cNone")
        addRadioButtonWithKeyboard("Custom", "StringIds.cCustomPara")
        addRadioButton("FitToPage", "StringIds.cFitToPage")
        addRadioButton("FullPageA4ToLetter", "StringIds.cFullPageLetter")
        addRadioButton("LegalToLetter", "StringIds.cLegalToLetter")
        addRadioButton("LetterToA4", "StringIds.cLettertoA4")

        ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.connect(recomputeCustomValue)
    }

    Component.onDestruction: {
        console.log(" copy setting resize view disconnect")
        ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.disconnect(recomputeCustomValue);
    }

}
