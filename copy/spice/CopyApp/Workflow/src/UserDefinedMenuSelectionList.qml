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
import "qrc:/menu/MenuDelegateApplier.js" as DelegateApplier
import "qrc:/SpicePropertyValueFromModel.js" as SpicePropertyValueFromModel

SpiceListView
{
    id : root
    property string node:""
    property var pushMenuItem : null
    property string titleId:""
    property string enumType : ""
    property QtObject menuResourceInstance: _menuResource
    property  var resourceModel : null
    property var eventHandler: null
    property Component radioButtonListViewModel : Component{ SettingsRadioButtonViewModel{} }
    property var validator: null
    property var menuDynamicUrl : ""
    readonly property QtObject menuDelegateProperties : MenuDelegateProperties{}
    property QtObject mediaUtility: MediaUtility{}
    property ISpiceModel mediaConfigurationModel: null

    /*!
         \brief Indicates whether the selected item should be shown first on the screen
         Ths is useful for long list that take time loading
         use TemplateData.json to indicate the flag to true
    */
    property bool showSelectedFirst: false

    /*!
         \brief Indicates that we are going to populateModel for speed optimization and
         we dont wont the data to be changed to show selected item at first
         In this case if selected item is beyond the visible delegate it wont be shown
    */
    property bool speedOptmizeNotSelection: false

    property string valueresource
    property QObjectListModel updatedModel: QObjectListModel{}

    objectName: node ? node + "MenuSelectionList": "MenuSelectionList"

    onNodeChanged: {
        let dataObj = _templatesData.valueMapFromList("menuSelections", node)
        const dict = (dataObj === null) ? null : dataObj.asMap()
        for (const [key, val] of Object.entries(dict)) {
            if (root.hasOwnProperty(key)) {
                root[key] = val
            }
        }

        if (_qmlUtils.testStringId(titleId)) {
            root.viewTitle = _qmlUtils.createSpiceLoc( root , {stringId: titleId})
        }

        if(dict !== null)
        {

            if (dict.hasOwnProperty("valueResource")) {
                menuDelegateProperties.valueResource_  = dict["valueResource"]
            }

            if(dict.hasOwnProperty("constraint")){
                menuDelegateProperties.constraint = dict["constraint"]
            }

            if(dict.hasOwnProperty("showSelectedFirst")){
                root.showSelectedFirst = dict["showSelectedFirst"]
            }

            if(dict.hasOwnProperty("speedOptmizeNotSelection")){
                root.speedOptmizeNotSelection = dict["speedOptmizeNotSelection"]
            }
        }

        DelegateApplier.getResource()
    }

    onValidatorChanged:{
        if(root.validator != null)
        {
            valueresource = getValueResource()
            for(let j = 0; j < root.validator.options.count ; j++)
            {
                updatedModel.append(root.validator.options.get(j))
            }
            if(showSelectedFirst || speedOptmizeNotSelection)
            {
                getSelectedValue()
                root.rowModel = updatedModel
            }
            else
            {
                let future = _resourceStore.subscribe("/cdm/mediaProperty/v2/mediaConfigs", true)
                future.resolved.connect(function(){
                                            root.mediaConfigurationModel = future.get()
                                            populateFullModel()
                                        })
                future.rejected.connect(function(){
                                            console.log("Failed to subscribe /cdm/mediaProperty/v2/mediaConfigs")
                                            populateFullModel()
                                        })
            }
        }
    }
    function getValue(modeldata)
    {
        let value
        if( modeldata.seValue !== "")
        {
            value = modeldata.seValue
        }
        else if(modeldata.sValue !== "")
        {
            value = modeldata.sValue
        }
        else
        {
            value = modeldata.iValue
        }

        return value
    }

    function getSelectedValue()
    {
        let valueIndex = -1
        for (let index =0 ; index < root.validator.options.count ;index++ )
        {
            let value = getValue(root.validator.options.get(index))

            let constraintValue = _qmlUtils.convertfbsExtendedCharsetEnumValueToCppEnumValue(value.toString())
            if(valueresource === constraintValue)
            {
                valueIndex = index
            }
        }
        if(showSelectedFirst && valueIndex !== -1)
        {
            updatedModel.move(valueIndex,0)
        }

    }

    function getValueResource()
    {
        let currentStringValue = _menuResource.enumStringFromValue(enumType, menuDelegateProperties.value)
        return currentStringValue
    }

    function populateModel(modelData, index)
    {
        return populateSingleModel(modelData, index)
    }

    function populateSingleModel(modelData, index)
    {
        let valueIndex = -1
        let value = getValue(modelData)
        let disabled =  modelData.disabled && modelData.disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_
        let message_ = (modelData.message) ? modelData.message : ""
        let constrainedMessage = null
        if(message_ !== "")
        {
            constrainedMessage = _qmlUtils.createSpiceLoc( root , {text : message_})
        }
        let constraintValue = _qmlUtils.convertfbsExtendedCharsetEnumValueToCppEnumValue(value.toString())
        var stringId = _propertyMap.cStringIDForEnum(enumType, constraintValue)
        let rdModel
        var testVal = "User defined 1"
        if(valueresource === constraintValue)
        {
            if (root.mediaUtility.isUserDefinedMediaType(constraintValue.toString()) === true)
            {
                let userDefName = getuserDefinedName(constraintValue.toString())
                let userDefNameSpiceLoc = _qmlUtils.createSpiceLoc( root , {"text": userDefName})
                rdModel = radioButtonListViewModel.createObject(null,{"node" : node ,  "objectName" : constraintValue + node ,"controlModel.objectName": "MenuValue" + constraintValue, "controlModel.selectedIndex" : index ,   "controlModel.checked": true , "controlModel.textObject":userDefNameSpiceLoc , "controlModel.constraintValue" : value , "controlModel.constrained" : disabled , "controlModel.constrainedMessage" : constrainedMessage})
            }
            else
            {
                rdModel = radioButtonListViewModel.createObject(null,{"node" : node ,  "objectName" : constraintValue + node ,"controlModel.objectName": "MenuValue" + constraintValue, "controlModel.selectedIndex" : index ,   "controlModel.checked": true , "controlModel.textObject.stringId":stringId , "controlModel.constraintValue" : value , "controlModel.constrained" : disabled , "controlModel.constrainedMessage" : constrainedMessage})
            }
            valueIndex = index
            root._indexPosition = index
        }
        else
        {
            if (root.mediaUtility.isUserDefinedMediaType(constraintValue.toString()) === true)
            {
                let userDefName = getuserDefinedName(constraintValue.toString())
                let userDefNameSpiceLoc = _qmlUtils.createSpiceLoc( root , {"text": userDefName})
                rdModel = radioButtonListViewModel.createObject(null,{"node" : node ,  "objectName" : constraintValue + node ,"controlModel.objectName": "MenuValue" + constraintValue, "controlModel.visible" : true  , "controlModel.selectedIndex" : index , "controlModel.textObject":userDefNameSpiceLoc , "controlModel.constraintValue" : value , "controlModel.constrained" : disabled , "controlModel.constrainedMessage" : constrainedMessage})
            }
            else
            {
                rdModel = radioButtonListViewModel.createObject(null,{"node" : node ,  "objectName" : constraintValue + node ,"controlModel.objectName": "MenuValue" + constraintValue, "controlModel.visible" : true  , "controlModel.selectedIndex" : index , "controlModel.textObject.stringId":stringId , "controlModel.constraintValue" : value , "controlModel.constrained" : disabled , "controlModel.constrainedMessage" : constrainedMessage})
            }
        }

        rdModel.controlModel.clicked.connect((selectedModel) =>
                                             {
                                                 if(valueIndex != selectedModel.selectedIndex && valueIndex !== -1)
                                                 {
                                                     rdModel.controlModel.checked = false
                                                 }

                                                 if(typeof(selectedModel.constraintValue) == "string" )
                                                 {
                                                    menuDelegateProperties.propertyModel[menuDelegateProperties.field] =  _qmlUtils.getValueFromStringifiedEnum(enumType , selectedModel.constraintValue)
                                                 }
                                                 else
                                                 {
                                                    menuDelegateProperties.propertyModel[menuDelegateProperties.field] =   selectedModel.constraintValue
                                                 }
                                                 _resourceStore.modify(menuDelegateProperties.dataModel)
                                                 _window.postViewEvent(QmlUtils.ViewEventType.Back)

                                             })
        return rdModel
    }
    function populateFullModel()
    {
        for(let j = 0; j < root.validator.options.count; j++  )
        {
            let disabled = root.validator.options.get(j).disabled && root.validator.options.get(j).disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_
            if (!disabled)
            {
                root.rowList.append(populateSingleModel(root.validator.options.get(j),j))
            }
        }
    }

    function getuserDefinedName(mediaTypeId)
    {
        if (root.mediaConfigurationModel && root.mediaConfigurationModel.data)
        {
            for (let i = 0 ; i < root.mediaConfigurationModel.data.mediaConfigs.count ; ++i)
            {
                if (root.mediaConfigurationModel.data.mediaConfigs.get(i).mediaType.toString() === mediaTypeId.toString())
                {
                    let userDefName = root.mediaConfigurationModel.data.mediaConfigs.get(i).userDefinedName
                    return userDefName
                }
            }
        }
        console.log("  getuserDefinedName return empty ")
        return " "
    }

    Component.onCompleted: {
        // This should prevent _resourceStore.modify being interupt and crash when RTL triggered during language change
        root.LayoutMirroring.enabled = Global.rtl
    }

}