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
    id: sidesSettingView
    objectName: "sidesSettingView"
    header: SpiceLocObject {stringId: "StringIds.cSides"}
    property ISpiceModel ticketModel: null;
    CopyController{
        id: copyController
    }

    function setDuplexBinding(plexMode, pagesFlipUpEnabled) {
        if(plexMode == Glossary_1_PlexMode.PlexMode.simplex)
        {
            ticketModel.data.dest.data.print.data.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.oneSided
        }
        else
        {
            if(pagesFlipUpEnabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
            {
                ticketModel.data.dest.data.print.data.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.twoSidedShortEdge
            }
            else
            {
                ticketModel.data.dest.data.print.data.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.twoSidedLongEdge
            }
        }
        console.debug("sidesSettingView: duplexBinding is " + ticketModel.data.dest.data.print.data.duplexBinding)
    }

    function addRadioButton(objName, buttonStrId, enumVal1, enumVal2){
        options.append(radioComponent.createObject(null,
                                                   {
                                                       "objectName": objName,
                                                       "textObject": _qmlUtils.createSpiceLoc(sidesSettingView ,{"stringId": buttonStrId}),
                                                       "checked": ((ticketModel.data.src.data.scan.data.plexMode == enumVal1) && (ticketModel.data.dest.data.print.data.plexMode == enumVal2)) ? true : false,
                                                       "buttonGroup": copySideGroup
                                                   }))
        options.at(options.size() - 1).buttonGroup.buttons[options.size() - 1].clicked.connect(function(val)
        {
            ticketModel.data.src.data.scan.data.plexMode = enumVal1;
            ticketModel.data.dest.data.print.data.plexMode = enumVal2;
            setDuplexBinding(ticketModel.data.dest.data.print.data.plexMode, ticketModel.data.src.data.scan.data.pagesFlipUpEnabled)
            _resourceStore.modify(ticketModel)
            sidesSettingView.viewDone()
        })
    }

    Component {
        id: radioComponent
        RadioButtonModel {
        }
    }

    ButtonGroup {
        id: copySideGroup
    }

    Component.onCompleted: {
        ticketModel = copyController.getTicketModel()
        // ui team have not updated what media sizes are available yet
        addRadioButton("Copy1to1Sided", "StringIds.c1To1Sided", Glossary_1_PlexMode.PlexMode.simplex, Glossary_1_PlexMode.PlexMode.simplex)
        addRadioButton("Copy1to2Sided", "StringIds.c1To2Sided", Glossary_1_PlexMode.PlexMode.simplex, Glossary_1_PlexMode.PlexMode.duplex)
        addRadioButton("Copy2to1Sided", "StringIds.c2To1Sided", Glossary_1_PlexMode.PlexMode.duplex, Glossary_1_PlexMode.PlexMode.simplex)
        addRadioButton("Copy2to2Sided", "StringIds.c2To2Sided", Glossary_1_PlexMode.PlexMode.duplex, Glossary_1_PlexMode.PlexMode.duplex)
    }
}
