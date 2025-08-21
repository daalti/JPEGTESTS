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

    function enablePageFlipUp(){
        console.log("Enabled")
        //TODO: uncomment it when Menu Framework support enable for workflow
        //copyPageFlipUp.enabled = controller.isDuplexing()
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

    function connectPageFlipUp(){
        ticketModel = _stateMachine.ticketModel
        ticketModel.data.src.scan.pagesFlipUpEnabledChanged.connect(pageFlipUpChangedValue)
    }


    Component.onCompleted: {
        Qt.callLater(connectPageFlipUp)
    }

    Component.onDestruction: {
        console.log("copy page flip up disconnect")
        ticketModel.data.src.scan.pagesFlipUpEnabledChanged.disconnect(pageFlipUpChangedValue);
    }
}
