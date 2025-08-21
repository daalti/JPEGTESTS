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
    objectName: "copySettingBooklet"
    property ISpiceModel ticketModel: null;
    property ISpiceModel constraintModel: null;
    property QtObject copySettingsHelper : CopySettingsHelper{}

    onConstraintModelChanged:
    {
        // Force update of text and constraint message
        textString();
    }

    function textString(){
        if(ticketModel.data.dest.print.bookletMakerOption == JobTicket_1_BookletMakerOptions.BookletMakerOptions.saddleStitch)
        {
            root.controlModel.secondInfoText = _qmlUtils.createSpiceLoc( 
                root ,{"stringId": _propertyMap.cStringIDForString("CopyBookletMakerOption","saddleStitch")})
        }
        else
        {
            let enumType = "dune::spice::jobTicket_1::Booklet::Booklet"
            let value = ticketModel.data.pipelineOptions.imageModifications.bookletFormat == JobTicket_1_BookletFormat.BookletFormat.leftEdge ? true : false;
            let stringId = _qmlUtils.createSpiceLoc( root ,{"stringId": _propertyMap.cStringIDForString(enumType, value ? "bookletFormatOn" : "bookletFormatOff")})
            root.controlModel.secondInfoText = stringId;
            console.log("booklet format is " + stringId);
        }
    }

    function connectValue(){
        ticketModel = _stateMachine.ticketModel
        root.constraintModel = _stateMachine.constraintModel
        textString()
        ticketModel.data.pipelineOptions.imageModifications.bookletFormatChanged.connect(textString);
        ticketModel.data.dest.print.bookletMakerOptionChanged.connect(textString);
    }

    Component.onCompleted: {
        Qt.callLater(connectValue)
    }
    Component.onDestruction: {
        console.log(" copy setting bookletFormat disconnect")
        ticketModel.data.pipelineOptions.imageModifications.bookletFormatChanged.disconnect(textString);
        ticketModel.data.dest.print.bookletMakerOptionChanged.disconnect(textString);
    }
}
