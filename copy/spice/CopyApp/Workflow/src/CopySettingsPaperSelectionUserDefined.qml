import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0
import QtQml.Models 2.15


MenuTextImageBranch
{
    id:paperSelectionView
    objectName: "copyPaperSelection"
    property ISpiceModel resourceModel: null;
    property ISpiceModel mediaPropertyConfigurationModel: null;
    property QtObject checkCopyOptionAvailability: CheckCopyMoreOptionAvailability{}
    property QtObject mediaUtility: MediaUtility{}

    function textString() 
    {
        var typeValue = [
            { 
                "type" : "dune::spice::glossary_1::MediaSize::MediaSize",
                "value": resourceModel.data.dest.print.mediaSize,
                "option": "copy_mediaSize",
                "propertyPointer":"src/scan/mediaSize"
            },
            { 
                "type" : "dune::spice::mediaProfile_1::MediaFamily::MediaFamily",
                "value": resourceModel.data.dest.print.mediaFamily,
                "option": "copy_mediaFamily",
                "propertyPointer":"dest/print/mediaFamily"
            },  
            { 
                "type" : "dune::spice::glossary_1::MediaType::MediaType",
                "value": resourceModel.data.dest.print.mediaType,
                "option": "copy_paperType",
                "propertyPointer":"src/scan/mediaType"
            },
            { 
                "type" : "dune::spice::glossary_1::MediaSourceId::MediaSourceId",
                "value": resourceModel.data.dest.print.mediaSource,
                "option": "copy_paperSource",
                "propertyPointer":"src/scan/mediaSource"
            }
        ]

        var textArray = []
        typeValue.forEach(function(element) {
            if(checkCopyOptionAvailability.checkAvailability(element.option) && _stateMachine.controller.findValidatorForConstraint(element.propertyPointer)!=null) 
            {
                textArray.push(textForValue(element.type, element.value)) 
            }
        })

        return textArray.join(", ")
    }

    function textForValue(type, value)
    {
        //MediaProfile_1_MediaFamily.MediaFamily.unknown is translated as "StringIds.cUnknown," but in the copy component, it has been used as "cAny". 
        if(type === "dune::spice::mediaProfile_1::MediaFamily::MediaFamily" && value == MediaProfile_1_MediaFamily.MediaFamily.unknown )
        {
            return _qmlUtils.createSpiceLoc( paperSelectionView ,{"stringId":"StringIds.cAny"}).text
        }
        else if(type === "dune::spice::glossary_1::MediaType::MediaType")
        {
            if(paperSelectionView.mediaUtility.isUserDefinedMediaType(resourceModel.data.dest.print.mediaType.toString()) === true
                &&  paperSelectionView.mediaPropertyConfigurationModel.data != null)
            {
               let usdName = paperSelectionView.mediaPropertyConfigurationModel.data.userDefinedName.toString()
               return _qmlUtils.createSpiceLoc( paperSelectionView ,{"text":usdName}).text
            }
        }
        else if(type === "dune::spice::glossary_1::MediaSize::MediaSize" && value == Glossary_1_MediaSize.MediaSize.any )
        {
            // "any" of "dest/print/mediaSize" should be shown as "Match Original Size" in Enterprise Copy.
            return _qmlUtils.createSpiceLoc( paperSelectionView ,{"stringId":"StringIds.cMatchOriginalSize"}).text
        }
        return _qmlUtils.createSpiceLoc( paperSelectionView ,{"stringId":_propertyMap.cStringIDForEnum(type, value)}).text
    }


    function recomputeValue(){

        console.log("PaperSelection Value Changed")
        if(paperSelectionView.mediaUtility.isUserDefinedMediaType(resourceModel.data.dest.print.mediaType.toString()) === true)
        {
            let cdmEndPoint = paperSelectionView.mediaUtility.convertToCDMString(resourceModel.data.dest.print.mediaType.toString())
            let future = _resourceStore.subscribe("/cdm/mediaProperty/v2/mediaConfigs/"+cdmEndPoint, true)
            future.resolved.connect(function(){
                                        paperSelectionView.mediaPropertyConfigurationModel = future.get()
                                        paperSelectionView.controlModel.secondInfoText.text = textString()
                                        })
        }
        else
        {
            paperSelectionView.controlModel.secondInfoText.text = textString()
        }
    }

    function setConstraint(){
        if(paperSelectionView.controlModel && 
           paperSelectionView.controlModel.validator && 
           paperSelectionView.controlModel.validator.disabled && 
           paperSelectionView.controlModel.validator.disabled.value == Glossary_1_FeatureEnabled.FeatureEnabled.true_) {
            console.log("PaperSelection is constrained")
            paperSelectionView.constrainedMessage = _qmlUtils.createSpiceLoc(root, { "stringId": "StringIds.cMessageNotAllowModifySettings", "params": ["StringIds.cPaperSelectTitle"] });
        }       
    }

    function setValue(){

        recomputeValue()
        setConstraint()
        paperSelectionView.controlModel.validatorChanged.connect(setConstraint)
        resourceModel.data.dest.print.mediaSizeChanged.connect(recomputeValue)
        resourceModel.data.dest.print.mediaTypeChanged.connect(recomputeValue)
        resourceModel.data.dest.print.mediaSourceChanged.connect(recomputeValue)
        resourceModel.data.dest.print.mediaFamilyChanged.connect(recomputeValue)
    }

    Component.onCompleted: {
        Qt.callLater(setValue)
    }

    Component.onDestruction: {
        console.log("copy paper selection disconnect")
        resourceModel.data.dest.print.mediaSizeChanged.disconnect(recomputeValue)
        resourceModel.data.dest.print.mediaTypeChanged.disconnect(recomputeValue);
        resourceModel.data.dest.print.mediaSourceChanged.disconnect(recomputeValue);
        resourceModel.data.dest.print.mediaFamilyChanged.disconnect(recomputeValue);
        paperSelectionView.controlModel.validatorChanged.disconnect(setConstraint);
    }
}