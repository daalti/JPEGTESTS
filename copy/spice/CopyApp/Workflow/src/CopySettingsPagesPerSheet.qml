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
    id: root
    objectName: "copySettingPagesPerSheet"
    property ISpiceModel ticketModel: null;
    property ISpiceModel constraintModel: null;
    property string enumType: "dune::spice::jobTicket_1::PagesPerSheet::PagesPerSheet"

    onConstraintModelChanged:
    {
        // Force update of text and constraint message
        textString()
    }

    function textString(){
        let value = _menuResource.enumStringFromValue("dune::spice::jobTicket_1::PagesPerSheet::PagesPerSheet", ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet)
        if (value == "oneUp"){
            let stringId = _qmlUtils.createSpiceLoc( root ,{"stringId":
                                                         _propertyMap.cStringIDForEnum("dune::spice::jobTicket_1::PagesPerSheet::PagesPerSheet",
                                                         ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet)})
            root.controlModel.secondInfoText = stringId
            root.controlModel.secondIcon = "qrc:/images/Glyph/PagesPerSheetOneUp.json"
            console.log("PagesPerSheet Option is " + stringId)
        }
        if (value == "twoUp"){
            let stringId = _qmlUtils.createSpiceLoc( root ,{"stringId":
                                                         _propertyMap.cStringIDForEnum("dune::spice::jobTicket_1::PagesPerSheet::PagesPerSheet",
                                                         ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet)})
            root.controlModel.secondInfoText = stringId
            root.controlModel.secondIcon = "qrc:/images/Glyph/PagesPerSheetTwoUp.json"
            console.log("PagesPerSheet Option is " + stringId)
        }
        if (value == "fourUp"){
            var numberUpPresentationDirection = ticketModel.data.pipelineOptions.imageModifications.numberUpPresentationDirection;
            if (numberUpPresentationDirection == JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toRightToBottom){
                let fourRightThenDownText = _qmlUtils.createSpiceLoc( root ,{stringId: _propertyMap.cStringIDForEnum(enumType, "fourRightThenDown")});
                root.controlModel.secondInfoText = fourRightThenDownText
                root.controlModel.secondIcon = "qrc:/images/Glyph/PagesPerSheetOrderZ.json"
                console.log("PagesPerSheet Option is " + fourRightThenDownText)
            }
            else if (numberUpPresentationDirection == JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toBottomToRight){
                let fourDownThenRightText = _qmlUtils.createSpiceLoc( root ,{stringId: _propertyMap.cStringIDForEnum(enumType, "fourDownThenRight")});
                root.controlModel.secondInfoText = fourDownThenRightText
                root.controlModel.secondIcon = "qrc:/images/Glyph/PagesPerSheetOrderN.json"
                console.log("PagesPerSheet Option is " + fourDownThenRightText)
            }
        }

        let validator = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/imageModifications/pagesPerSheet");
        if(validator && validator.disabled && validator.disabled.message)
        {
            root.controlModel.constrainedMessage = _qmlUtils.createSpiceLoc( root ,{"text":validator.disabled.message})
        }
    }

    function connectValue(){
        ticketModel = _stateMachine.ticketModel
        root.constraintModel = _stateMachine.constraintModel
        textString()
        ticketModel.data.pipelineOptions.imageModifications.pagesPerSheetChanged.connect(textString);
        ticketModel.data.pipelineOptions.imageModifications.numberUpPresentationDirectionChanged.connect(textString);
    }

    Component.onCompleted: {
        Qt.callLater(connectValue)
    }
    Component.onDestruction: {
        console.log(" copy setting resize disconnect")
        ticketModel.data.pipelineOptions.imageModifications.pagesPerSheetChanged.disconnect(textString);
        ticketModel.data.pipelineOptions.imageModifications.numberUpPresentationDirectionChanged.disconnect(textString);
    }
}
