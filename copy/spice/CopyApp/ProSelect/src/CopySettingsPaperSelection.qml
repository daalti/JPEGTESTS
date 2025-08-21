import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0

MenuNameValue
{
    id:paperSelectionView
    objectName: "copyPaperSelection"
    property ISpiceModel ticketModel: null;
    property QtObject copyControllerfunctions : CopyController{}

    function textString()
    {
        var typeValue = [
            { 
                "type" : "dune::spice::glossary_1::MediaSize::MediaSize",
                "value": ticketModel.data.dest.print.mediaSize
            },
            { 
                "type" : "dune::spice::glossary_1::MediaType::MediaType",
                "value": ticketModel.data.dest.print.mediaType
            },
            { 
                "type" : "dune::spice::glossary_1::MediaSourceId::MediaSourceId",
                "value": ticketModel.data.dest.print.mediaSource
            }
        ]

        return (
            textForValue(typeValue[0].type, typeValue[0].value) + ", "+
            textForValue(typeValue[1].type, typeValue[1].value) + ", "+
            textForValue(typeValue[2].type, typeValue[2].value)
        )
    }

    function textForValue(type, value)
    {
        return _qmlUtils.createSpiceLoc( paperSelectionView ,{"stringId":_propertyMap.cStringIDForEnum(type, value)}).text
    }

    function recomputeValue(){
        console.log("call paper selection view connect connect")
        paperSelectionView.valueButton.textObject.text = textString()
    }

    Component.onCompleted: {
        ticketModel = copyControllerfunctions.getTicketModel()
        ticketModel.data.dest.print.mediaTypeChanged.connect(recomputeValue)
        ticketModel.data.dest.print.mediaSourceChanged.connect(recomputeValue)
    }

    Component.onDestruction: {
        console.log("copy paper selection disconnect")
        ticketModel.data.dest.print.mediaTypeChanged.disconnect(recomputeValue);
        ticketModel.data.dest.print.mediaSourceChanged.disconnect(recomputeValue);
    }
}
