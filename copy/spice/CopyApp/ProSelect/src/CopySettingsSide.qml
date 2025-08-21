import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0

MenuNameValue
{
    id: copySettingsSidesNameValue
    objectName: "copyPaperSelection"
    property ISpiceModel ticketModel: null;
    property QtObject copyControllerfunctions : CopyController{}


    function textString()
    {
        return _qmlUtils.createSpiceLoc( copySettingsSidesNameValue , {"stringId":convertSideText()}).text
    }

    function convertSideText() {
        //ticketModel = copyControllerfunctions.getTicketModel()
        var sideText = "StringIds.c1To1Sided";

        if(ticketModel.data.src.scan.plexMode == Glossary_1_PlexMode.PlexMode.simplex && ticketModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.simplex)
        {
            sideText = "StringIds.c1To1Sided";
        }
        else if(ticketModel.data.src.scan.plexMode == Glossary_1_PlexMode.PlexMode.simplex && ticketModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.duplex)
        {
            sideText = "StringIds.c1To2Sided";
        }
        else if(ticketModel.data.src.scan.plexMode == Glossary_1_PlexMode.PlexMode.duplex && ticketModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.simplex)
        {
            sideText = "StringIds.c2To1Sided";
        }
        else if(ticketModel.data.src.scan.plexMode == Glossary_1_PlexMode.PlexMode.duplex && ticketModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.duplex)
        {
            sideText = "StringIds.c2To2Sided";
        }
        else
        {
            // _stateMachine.copyControllerfunctions.printTicketModel(_stateMachine.ticketModel);        
            // console.error("Ticket value is wrong. inputPlexMode " + _stateMachine.ticketModel.data.src.data.scan.data.inputPlexMode + " outputPlexMode " + _stateMachine.ticketModel.data.dest.data.print.data.plexMode);
            sideText = "StringIds.cUnknown";
        }

        return sideText;
    }

    function recomputeValue(){
        copySettingsSidesNameValue.valueButton.textObject.text = textString()
    }

    Component.onCompleted: {
        ticketModel = copyControllerfunctions.getTicketModel()
        ticketModel.data.dest.print.plexModeChanged.connect(recomputeValue)
        ticketModel.data.src.scan.plexModeChanged.connect(recomputeValue)
    }
    Component.onDestruction: {
        console.log("copy setting side disconnect")
        ticketModel.data.dest.print.plexModeChanged.disconnect(recomputeValue);
        ticketModel.data.src.scan.plexModeChanged.disconnect(recomputeValue);
    }
}
