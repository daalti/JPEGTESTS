import QtQuick 2.15
import QtQml 2.15
//import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
//import QtQml.Models 2.15

//import "qrc:/SpiceBinding.js" as SpiceBinding
import "qrc:/UnitsUtils.js" as UnitsUtils
import "qrc:/ResourceStoreConnectionBinding.js" as ResourceStoreBinding
/*
In this control, MenuComboBox.qml is reimplemented. 
    1. create a derived QML of MenuComboBoxCustomReplaceText.qml
    2  reimplement initControl(),call CDM and get models 
    3. fill mediaMap : mediaMap.set(Number(ENUM VALUE as a number),replacement text)
    4  call to postInitControl()
*/

//Custom SettingsComboBoxViewModel
MenuComboBoxCustomReplaceText
{
    id : root

    property var systemConfigModel: null
    property var mediaSizeConfiguration: null
    property SpiceLocObject mediaNameLoaded: SpiceLocObject { stringId: "StringIds.cPaperNotLoaded" }
    property bool isMetricInInches: (systemConfigModel && systemConfigModel.data && systemConfigModel.data.displayUnitOfMeasure == System_1_UnitsOfMeasurement.UnitsOfMeasurement.imperial)?true:false
    
    //CUSTOM HELPER FUNCTIONS

    function getSizeInfo(modelData)
    {
        if(isSourceIdTray(modelData))
        {
            return _qmlUtils.createSpiceLoc( root , {"stringId": _propertyMap.cStringIDForEnum("dune::spice::glossary_1::MediaSize::MediaSize", _qmlUtils.convertfbsExtendedCharsetEnumValueToCppEnumValue(modelData.currentMediaSize.toString())) }).text
        }
        else
        {

            let isContinuous=false
            if( modelData.inputType == Glossary_1_MediaInput_InputType.InputType.continuousRoll ) isContinuous=true

            if(modelData.currentMediaLength>0 && modelData.currentMediaWidth>0 && !isContinuous)
            {
                return generateWidthHeigthText(
                    generateWidthValue(modelData.currentMediaWidth, modelData.currentResolution), 
                    generateWidthValue(modelData.currentMediaLength, modelData.currentResolution)
                    ).text
            }
            return generateWidthText(generateWidthValue(modelData.currentMediaWidth, modelData.currentResolution)).text
        }
    }

    function generateWidthText(width)
    {
        if (width === 0)
        {
            return _qmlUtils.createSpiceLoc( root , {"stringId": "StringIds.cAuto"})
        }
        else
        {
            if (isMetricInInches)
            {
                return _qmlUtils.createSpiceLoc( root , {"stringId": "StringIds.cParamInches", "params": [parseInt(width) | 0]})
                
            }
            else
            {
                return _qmlUtils.createSpiceLoc( root, {"stringId": "StringIds.cParamMM", "params": [parseInt(width) | 0]})
            }
        }
    }

    function generateWidthHeigthText(width , heigth)
    {
        let value = parseInt(width)
        let rightString = generateWidthText(heigth)
        value =value +" x "+ rightString.text
        rightString.destroy()
        return _qmlUtils.createSpiceLoc( root , {"text":  value})
    }

    function isSourceIdRoll(modelData)
    {
        switch(modelData.mediaSourceId.toString())
        {
            case "main_dash_roll":
            case "roll":
            case "roll_dash_1":
            case "roll_dash_2":
            case "roll_dash_3":
            case "roll_dash_4":
            case "roll_dash_5": 
            case "roll_dash_6": 
              return true
              break;
            default:
             return false
        }
    }

    function isSourceIdTray(modelData)
    {
        switch(modelData.mediaSourceId.toString())
        {
            case "main":
            case "alternate":
            case "tray_dash_1":
            case "tray_dash_2":
            case "tray_dash_3":
            case "tray_dash_4":
            case "tray_dash_5": 
            case "tray_dash_6": 
              return true
              break;
            default:
             return false
        }
    }

    function generateWidthValue(width, resolution )
    {
        if (isMetricInInches)
        {
            return parseFloat(Math.round(UnitsUtils.dpiToInch(width, resolution)))  
        }
        else
        {
            return parseFloat(Math.round(UnitsUtils.dpiToMm(width, resolution)))
        }
    }
    

    function generateMediaTypeText(input)
    {
        let loaded = false;
        let mediaCustomIdLoaded = ""

        let isMediaLoaded = false
        let isMediaCustom = false
        let currentMediaName = ""
        let currentMediaSize = ""
        let isRoll=isSourceIdRoll(input)

        //let mediaNameLoadedStringId 
        //empty media loaded
        if(input.stateReason == Media_1_DeviceStateReason.DeviceStateReason.empty)
        {
            loaded = false;
        }
        //custom media loaded
        else if(input.currentMediaType == Glossary_1_MediaType.MediaType.custom)
        {
            currentMediaName = input.currentMediaName;
            mediaCustomIdLoaded = input.currentMediaCustomId;

            currentMediaSize = getSizeInfo(input)
            isMediaCustom = true;
            isMediaLoaded = true;
            loaded = true;

        }
        //other mediaType loaded
        else
        {
            let stringIdtxt = _propertyMap.cStringIDForEnum("dune::spice::glossary_1::MediaType::MediaType", input.currentMediaType);
            mediaNameLoaded.stringId = (stringIdtxt != null || stringIdtxt != undefined ? stringIdtxt : "StringIds.cUndefined");

            mediaCustomIdLoaded = "";


            currentMediaSize = getSizeInfo(input)
            isMediaCustom = false;
            isMediaLoaded = true;
            loaded = true;
        }

        if(!loaded)
        {
            
            mediaNameLoaded.stringId = "StringIds.cPaperNotLoaded";

            
            mediaCustomIdLoaded = "";
            isMediaCustom = false;
            isMediaLoaded = false;
            return ' (' + mediaNameLoaded.text + ')'
        }
        else
        {
            let mediaName="" 
            if(isMediaCustom)  mediaName = currentMediaName
            else  mediaName = mediaNameLoaded.text

            if(mediaName != "") return ' (' + mediaName + ' , ' + currentMediaSize + ')'
            else return ' (' + currentMediaSize + ')'
        }
            
    }

    function setNewComboBoxTextMap()
    {
        //create text replacement map
        let mediaInputsList = mediaSizeConfiguration.data.inputs
        for(let idx = 0; idx < mediaInputsList.count; ++idx)
        {
            let mediaInput = mediaInputsList.get(idx);
            if( isSourceIdRoll(mediaInput) /*|| isSourceIdTray(mediaInput)*/ ) //maybe we need to add tray in the future
            {
                let enumType=root.controlModel.enumType // "dune::spice::glossary_1::MediaSourceId::MediaSourceId"
                //root.controlModel.enumType
                let mediaSourceIdStringId = _propertyMap.cStringIDForEnum(enumType, mediaInput.mediaSourceId)
                //original combobox text
                let text = _qmlUtils.createSpiceLoc( root , {"stringId": mediaSourceIdStringId }).text
                let paperTypeInfo=generateMediaTypeText(mediaInput)
                text += paperTypeInfo
                //set replacement value
                mediaMap.set(Number(mediaInput.mediaSourceId),text)
            }
        }
        //super postInitControl
        postInitControl()
    }

    //reimplement custom control init
    function initControl()
    {
        ResourceStoreBinding.handleFuture(()=> _resourceStore.get("/cdm/system/v1/configuration")).then((response) => {
            systemConfigModel = response
            if(systemConfigModel && mediaSizeConfiguration)
            {
                setNewComboBoxTextMap()
            }
        }).catch((future) =>  {
            console.log("System config GET rejected", future.error);
            });

        ResourceStoreBinding.handleFuture(()=>  _resourceStore.subscribe("/cdm/media/v1/configuration")).then((response) => {
            mediaSizeConfiguration = response

            // signals connected inside the for loop are not working, so 
            // countChanged signal is used instead
            mediaSizeConfiguration.data.inputs.onCountChanged.connect(evalModel) 

            let mediaInputsList = mediaSizeConfiguration.data.inputs
            for(let idx = 0; idx < mediaInputsList.count; ++idx)
            {
                let mediaInput = mediaInputsList.get(idx);
                mediaInput.onStateReasonChanged.connect(evalModel)
                mediaInput.onCurrentMediaTypeChanged.connect(evalModel)
                mediaInput.onMediaSourceIdChanged.connect(evalModel)
                mediaInput.onCurrentMediaWidthChanged.connect(evalModel)
                mediaInput.onCurrentResolutionChanged.connect(evalModel)
            }

            if(systemConfigModel && mediaSizeConfiguration)
            {
               setNewComboBoxTextMap()
            }
        }).catch((future) =>  {
            console.log("media configuration GET rejected ERROR:" + future.error);
        });
    }

    function evalModel()
    {
        if(root.systemConfigModel && root.mediaSizeConfiguration)
        {
            Qt.callLater(setNewComboBoxTextMap)   
        }
    }
   
    Component.onDestruction: {
        if(systemConfigModel)
        {
            systemConfigModel.destroy()
        } 
        if(mediaSizeConfiguration) 
        {
            mediaSizeConfiguration.data.inputs.onCountChanged.disconnect(evalModel)
            
            let mediaInputsList = mediaSizeConfiguration.data.inputs
            for(let idx = 0; idx < mediaInputsList.count; ++idx)
            {
                let mediaInput = mediaInputsList.get(idx);
                mediaInput.onStateReasonChanged.disconnect(evalModel)
                mediaInput.onCurrentMediaTypeChanged.disconnect(evalModel)
                mediaInput.onMediaSourceIdChanged.disconnect(evalModel)
                mediaInput.onCurrentMediaWidthChanged.disconnect(evalModel)
                mediaInput.onCurrentResolutionChanged.disconnect(evalModel)
            }
            _resourceStore.unsubscribe(mediaSizeConfiguration.data)
            mediaSizeConfiguration.destroy()
        }
    }
}
