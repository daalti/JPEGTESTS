import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0
import QtQml.Models 2.15

MenuTextImageBranch
{
    id: copySettingsSidesTextImageBranch
    objectName: "copySettingResize"
    property ISpiceModel ticketModel: null;
    property ISpiceModel constraintModel: null;

    onConstraintModelChanged:
    {
        // Force update of text and constraint message
        textString()
    }

    function textString(){
        let value = _menuResource.enumStringFromValue("dune::spice::jobTicket_1::scaling::ScaleSelection::ScaleSelection", ticketModel.data.pipelineOptions.scaling.scaleSelection)
        if (value == "custom"){
            var customText = ticketModel.data.pipelineOptions.scaling.xScalePercent;
            console.log("Custom text in the output scale " + customText)
            let sideText = (_qmlUtils.createSpiceLoc( copySettingsSidesTextImageBranch ,{stringId: "StringIds.cCustomPara", "params": [customText]}));
            copySettingsSidesTextImageBranch.controlModel.secondInfoText = sideText
        }
        else {
            let stringId = _qmlUtils.createSpiceLoc( copySettingsSidesTextImageBranch ,{"stringId":
                                                         _propertyMap.cStringIDForEnum("dune::spice::jobTicket_1::scaling::ScaleSelection::ScaleSelection",
                                                         ticketModel.data.pipelineOptions.scaling.scaleSelection)})
            copySettingsSidesTextImageBranch.controlModel.secondInfoText = stringId
        }

        let validator = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/scaling/scaleSelection");
        // TO-DO Remove the Constraints handling once the MenuTextImageBranch implements the constraints handling
        if(validator && validator.disabled && validator.disabled.value == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
        {
            copySettingsSidesTextImageBranch.controlModel.constrained = true
            copySettingsSidesTextImageBranch.controlModel.constrainedMessage = _qmlUtils.createSpiceLoc( copySettingsSidesTextImageBranch ,{"text":validator.disabled.message})
        }
        else
        {
            copySettingsSidesTextImageBranch.controlModel.constrained = false
        }
    }

    function connectValue(){
        ticketModel = _stateMachine.ticketModel
        copySettingsSidesTextImageBranch.constraintModel = _stateMachine.constraintModel
        textString()
        ticketModel.data.pipelineOptions.scaling.scaleSelectionChanged.connect(textString);
        ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.connect(textString);
    }

    Component.onCompleted: {
        Qt.callLater(connectValue)
    }
    Component.onDestruction: {
        console.log(" copy setting resize disconnect")
        ticketModel.data.pipelineOptions.scaling.scaleSelectionChanged.disconnect(textString);
        ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.disconnect(textString);
    }
}
