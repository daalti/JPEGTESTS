import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

SpiceListView {
    id:root
    objectName: "copy_mediaSizeMenuSelectionList"

    header: SpiceLocObject {stringId: "StringIds.cSize"}

    property QtObject locControlModel : RadioButtonModel{}
    property QQmlObjectListModel controlModelList : QQmlObjectListModel{}

    property ISpiceModel ticketModel: null;

    // Properties used by pattern
    property QtObject menuResourceInstance: _menuResource
    property var pushMenuItem : null
    property var resourceModel : null
    property string valueResource:""
    property string constraint:""
    property string menuDynamicUrl: ""
    property bool customEnterd: false
    property var eventHandler: null
    property string node:""
    property bool autoSelectFirst:false
    property var menuNode

    property bool isCustomExisted: false
    property var customEnumVal: null
    property var customMessage: null
    property bool customIsEnabled: false

    ButtonGroup {
        id: mediaSizeGroup
    }

    Component {
        id: controlModelComponents
        RadioButtonModel {}
    }

    Component {
        id: radioButtonListViewModels
        SettingsRadioButtonViewModel{}        
    }

    onNodeChanged : {
        console.log("onNodeChanged root.node is " + root.node)
        addRadioIconButton(root.customEnumVal)
    }

    function addRadioIconButton(enumVal){
        if(isCustomExisted)
        {
            let rightPanelNodes = menuResourceInstance.getChildren(root.node);
            let rightChild = rightPanelNodes[0]
            let comp = Qt.createComponent(rightChild.delegate)

            if (comp.status === Component.Ready) {
                let enumValAsString = _menuResource.enumStringFromValue("dune::spice::glossary_1::MediaSize::MediaSize", enumVal)
                let menuRadioIconBranchObject = comp.createObject(rowList,
                {
                    "objectName" : enumValAsString + "copy_mediaSize",
                    "pushMenuItem": root.pushMenuItem,
                    "resourceModel": resourceModel,
                    "menuDynamicUrl": menuDynamicUrl,
                    "menuNode": rightChild,
                    "resourceInstance" : menuResourceInstance
                })

                rowList.append(menuRadioIconBranchObject)
            }
        }
    }

    function addRadioButton(enumVal, message, isEnabled=true){
        let enumValAsString = _menuResource.enumStringFromValue("dune::spice::glossary_1::MediaSize::MediaSize", enumVal)
        console.log("Adding radio button: " + enumValAsString + "enable: " + isEnabled)

        let displayedMediaSize = null
        if(enumVal == Glossary_1_MediaSize.MediaSize.any)
        {
            console.log("any")
            displayedMediaSize = _qmlUtils.createSpiceLoc( root  , {"stringId": "StringIds.cMatchOriginalSize"})
        }
        else
        {
            displayedMediaSize = _qmlUtils.createSpiceLoc( root  , {"stringId": _propertyMap.cStringIDForEnum("dune::spice::glossary_1::MediaSize::MediaSize", enumVal)})
        }

        root.locControlModel = controlModelComponents.createObject(root.controlModelList,
                                                    {
                                                        "objectName": enumValAsString,
                                                        "textObject": displayedMediaSize,
                                                        "value": enumVal,                                                        
                                                        "constrained": !isEnabled,
                                                        "constrainedMessage": _qmlUtils.createSpiceLoc( root  , {"text":message}),
                                                        "checkable": true, // Checkable is a property from Qt directly, that cause always user click, select the radio button, but this is not the expected functionality here
                                                        "buttonGroup": mediaSizeGroup
                                                    })
        root.locControlModel.checked = Qt.binding(function(){return (ticketModel.data.dest.print.mediaSize == enumVal )})
        root.controlModelList.append(root.locControlModel)
        if(isEnabled)
        {
            if(autoSelectFirst)
            {
                modifyValueOnCdm(enumVal)
                autoSelectFirst = false;
            }
            // Create connection to clicked only when is enabled
            root.controlModelList.at(root.controlModelList.size() -1).clicked.connect(function(val)
            {
                console.log("Modify ticketModel on output media size with value: " + enumValAsString)
                setRadioButtonValue(enumVal)
                _window.postViewEvent(QmlUtils.ViewEventType.Back)
            })
        }

        rowList.append(radioButtonListViewModels.createObject(rowList,
        {
            "controlModel": root.controlModelList.get(root.controlModelList.size() - 1),
            "objectName" : enumValAsString + "copy_mediaSize"
        }))
    }

    function setRadioButtonValue(checkedValue)
    {
        console.log("setRadioButtonValue checkedValue is " + checkedValue)
        
        modifyValueOnCdm(checkedValue)
    }

    function modifyValueOnCdm(checkedValue)
    {
        ticketModel.data.dest.print.mediaSize = checkedValue
        _resourceStore.modify(ticketModel)
    }

    function fillRadioButtons()
    {
        console.log("fillRadioButtons")
        rowList.clear()
        root.controlModelList.clear()

        let validator = _stateMachine.controller.findValidatorForConstraint("dest/print/mediaSize");
        if(validator)
        {
            for(let j=0; j < validator.options.count ; j++)
            {
                let constraintValue = _qmlUtils.getValueFromStringifiedEnum("dune::spice::glossary_1::MediaSize::MediaSize", validator.options.get(j).seValue)                                 
                console.log("Constraint to be added: " + _menuResource.enumStringFromValue("dune::spice::glossary_1::MediaSize::MediaSize", constraintValue))

                // When disabled is false, the setting is currently enabled
                let enabled = validator.options.get(j).disabled == Glossary_1_FeatureEnabled.FeatureEnabled._undefined_ || validator.options.get(j).disabled == Glossary_1_FeatureEnabled.FeatureEnabled.false_
                let message = ""
                if(!enabled && validator.options.get(j).message)
                {
                    message = validator.options.get(j).message
                }

                // Avoid add custom or any here, is supported as an option, but is not set on this field
                
                if(constraintValue == Glossary_1_MediaSize.MediaSize.custom)
                {
                    root.isCustomExisted = true
                    root.customEnumVal = constraintValue
                    root.customMessage = message
                    root.customIsEnabled = enabled
                    console.log("constraintValue(custom) is " + constraintValue)
                    if(root.node)
                    {
                        addRadioIconButton(constraintValue)
                    }
                }
                else if(constraintValue != Glossary_1_MediaSize.MediaSize._undefined_ &&
                    constraintValue != Glossary_1_MediaSize.MediaSize.anycustom)
                {
                    console.log("constraintValue is " + constraintValue)
                    addRadioButton(constraintValue, message, enabled)
                }   
            }
        }
        else
        {
            console.warn("copySettingPaperSizeView -> No constraints for value when options must to be added.")
        }
    }

    Component.onCompleted: {
        ticketModel = _stateMachine.ticketModel

        // Force select first if there is no option selected.
        if(ticketModel.data.dest.print.mediaSize == Glossary_1_MediaSize.MediaSize.any)
        {
            autoSelectFirst = true;
        }

        fillRadioButtons()
    }
}