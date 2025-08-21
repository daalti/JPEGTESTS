import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0

MenuSwitch
{
    id: copyPageFlipUp
    objectName: "copyPageFlipUp"
    property ISpiceModel ticketModel: null;
    property QtObject copyControllerfunctions : CopyController{}

    function enablePageFlipUp(){
        copyPageFlipUp.enabled = copyControllerfunctions.isDuplexing()
    }

    function pageFlipUpChangedValue(){
        if(ticketModel.data.src.scan.pagesFlipUpEnabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_){
            ticketModel.data.dest.print.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.twoSidedShortEdge
        }
        else{
            ticketModel.data.dest.print.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.twoSidedLongEdge
        }

        _resourceStore.modify(ticketModel)
    }


    Component.onCompleted: {
        ticketModel = copyControllerfunctions.getTicketModel()
        enablePageFlipUp()
        ticketModel.data.dest.print.plexModeChanged.connect(enablePageFlipUp)
        ticketModel.data.src.scan.plexModeChanged.connect(enablePageFlipUp)
        ticketModel.data.src.scan.pagesFlipUpEnabledChanged.connect(enablePageFlipUp)
    }

    Component.onDestruction: {
        console.log("copy page flip up disconnect")
        ticketModel.data.dest.print.plexModeChanged.disconnect(enablePageFlipUp);
        ticketModel.data.src.scan.plexModeChanged.disconnect(enablePageFlipUp);
        ticketModel.data.src.scan.pagesFlipUpEnabledChanged.disconnect(enablePageFlipUp);
    }
}
