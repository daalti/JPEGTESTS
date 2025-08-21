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
    id: copySettingsFoldTextImageBranch
    objectName: "copySettingsfold"
    property ISpiceModel ticketModel: null;
    property ISpiceModel constraintModel: null;

    onConstraintModelChanged:
    {
        // Force update of text and constraint message
        textString()
    }

    function textString(){
        copySettingsFoldTextImageBranch.controlModel.secondInfoText = _qmlUtils.createSpiceLoc( copySettingsFoldTextImageBranch ,{"stringId":
                                                        _propertyMap.cStringIDForString("CopyFoldOption",
                                                        ticketModel.data.dest.print.foldOption.toString())})
    }

    function connectValue(){
      
        ticketModel = _stateMachine.ticketModel

        copySettingsFoldTextImageBranch.constraintModel = _stateMachine.constraintModel
        textString()
        ticketModel.data.dest.print.foldOptionChanged.connect(textString);
    }

    Component.onCompleted: {
        Qt.callLater(connectValue)
    }
    Component.onDestruction: {
        ticketModel.data.dest.print.foldOptionChanged.disconnect(textString);
    }
}
