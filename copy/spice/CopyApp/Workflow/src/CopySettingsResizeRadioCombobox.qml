import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import QtQml.Models 2.15
import spiceuxLayouts 1.0
import spiceuxComponents 1.0
import spiceuxTemplates 1.0
import "qrc:/SpiceBinding.js" as SpiceBinding
import "qrc:/UnitsUtils.js" as UnitsUtils


SettingsViewModel{
    id: root
    controlModel : ComboBoxListModel {}
    visible : controlModel.visible
    clickable: false
    description :  SpiceLocObject { text: controlModel.description !== null ? controlModel.description.text : ""}
    lined: true
    property var constraintUrl : null
    property var constraintEnumType : null
    property var propertyModel: null
    property QtObject locComboBoxModel : null
    property ISpiceModel mediaSizeConfiguration : null
    property ISpiceModel resourceModel : null
    property ISpiceModel systemConfigModel: null

    blocks: QQmlObjectListModel {
        RowBlockComponentModel {
            id: componentBlock
            componentType: ControlModel.NodeType.Radio
            alignment: Qt.AlignLeft
            componentList: ObjectModel {
                SpiceRadioButton {
                    id: spiceRadioButton
                    objectName: root.objectName + "RadioButton"
                    textObject: controlModel.infoText
                    checked: controlModel.checked
                    buttonGroup: copyResizeGroup
                    constrained: root.controlModel.constrained
                    constrainedMessage: root.controlModel.constrainedMessage
                    Component.onCompleted: {
                        SpiceBinding.twoWayBinding(spiceRadioButton, "checked", controlModel)
                    }
                    onClicked: {
                        controlModel.clicked(controlModel)
                    }
                }
            }
        }

        RowBlockComponentModel {
            id: componentBlock4
            fillWidth: false
            alignment: Qt.AlignRight
            minWidth : 20 * Global.rem
            componentList: ObjectModel {
                SpiceComboBox {
                    id: comboBox
                    objectName: root.objectName + "ComboBox"
                    width : 20 * Global.rem
                    currentIndex: root.controlModel.currentIndex
                    constrained: root.controlModel.constrained
                    constrainedMessage: root.controlModel.constrainedMessage
                    infoText: SpiceLocObject {text: root.controlModel.selectedValue.text}
                    model:{
                        return root.controlModel.model;
                    }

                    Component.onCompleted: {
                        Qt.callLater(setCurrentIndexBinding);
                    }

                    onActivated: {
                        root.controlModel.selected(index)
                    }
                }
            }
        }
    }

    function setCurrentIndexBinding(){
        SpiceBinding.twoWayBinding(comboBox,"currentIndex",root.controlModel)
    }

    function getSizeInfo(modelData)
    {
        if(isSourceIdTray(modelData))
        {
            return _qmlUtils.createSpiceLoc( root , {"stringId": _propertyMap.cStringIDForEnum("dune::spice::glossary_1::MediaSize::MediaSize", _qmlUtils.convertfbsExtendedCharsetEnumValueToCppEnumValue(modelData.currentMediaSize.toString())) }).text
        }
        else
        {
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
            let currentDisplayUnit = getCurrentDisplayUnit()
            if (currentDisplayUnit === System_1_UnitsOfMeasurement.UnitsOfMeasurement.metric)
            {
                return _qmlUtils.createSpiceLoc( root, {"stringId": "StringIds.cParamMM", "params": [parseInt(width) | 0]})
            }
            else
            {
                return _qmlUtils.createSpiceLoc( root , {"stringId": "StringIds.cParamInches", "params": [parseInt(width) | 0]})
            }
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

    function getCurrentDisplayUnit()
    {
        let currentDisplayUnit = Number(System_1_UnitsOfMeasurement.UnitsOfMeasurement.metric)

        if (systemConfigModel && systemConfigModel.data)
        {
            currentDisplayUnit = Number(_qmlUtils.getValueFromStringifiedEnum("dune::spice::system_1::UnitsOfMeasurement::UnitsOfMeasurement", systemConfigModel.data.displayUnitOfMeasure))
        }
        else
        {
            console.log("getCurrentDisplayUnit: system configuration model not found")
        }

        return currentDisplayUnit
    }

    function generateWidthValue(width, resolution = 1000, toDpi = false)
    {
        let currentDisplayUnit = getCurrentDisplayUnit()
        if (currentDisplayUnit === System_1_UnitsOfMeasurement.UnitsOfMeasurement.metric)
        {
            if (toDpi)
            {
                return parseFloat(Math.round(UnitsUtils.mmToDpi(width, resolution)))
            }
            else
            {
                return parseFloat(Math.round(UnitsUtils.dpiToMm(width, resolution)))
            }
        }
        else
        {
            if (toDpi)
            {
                return parseFloat(Math.round(UnitsUtils.inchToDpi(width, resolution)))
            }
            else
            {
                return parseFloat(Math.round(UnitsUtils.dpiToInch(width, resolution)))
            }
        }
    }

    function createStandardSizesModel(){
        let validators = _stateMachine.controller.findValidatorForConstraint(root.constraintUrl)

        if (validators)
        {
            for(var index=0; index< validators.options.count ; index++){
                let scaleConstraintValue = _qmlUtils.convertfbsExtendedCharsetEnumValueToCppEnumValue(validators.options.get(index).seValue)
                let valueDisabled = validators.options.get(index).disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_
                let constrainedMessage = validators.options.get(index).message
                let constraintStringId = _propertyMap.cStringIDForEnum(constraintEnumType, scaleConstraintValue)
                let constraintValue = _qmlUtils.getValueFromStringifiedEnum(constraintEnumType, validators.options.get(index).seValue);
                let enumValAsString = _menuResource.enumStringFromValue(constraintEnumType, constraintValue)
   
                let text = _qmlUtils.createSpiceLoc( root , {"stringId": constraintStringId }).text

                if(constraintUrl.includes("scaleToOutput"))
                {
                    let mediaInputsList = root.mediaSizeConfiguration.data.inputs
                    for(var idx = 0; idx < mediaInputsList.count; ++idx)
                    {
                        var mediaInput = mediaInputsList.get(idx);

                        if(mediaInput.mediaSourceId.toString() == scaleConstraintValue)
                        {
                            text = text.concat(" (", getSizeInfo(mediaInput), ")")
                        }
                    }
                }

                let component = Qt.createComponent("qrc:/components/models/ComboBoxModel.qml")
                locComboBoxModel= component.createObject(
                            root.controlModel.model, {
                                "objectName": enumValAsString,
                                "textObject.text": text,
                                "constrained": valueDisabled,
                                "constrainedMessage": _qmlUtils.createSpiceLoc( root ,{"text":constrainedMessage}),
                                "visible" : true,
                                "clickable" : true,
                                "value": index
                            })
                root.controlModel.model.append(locComboBoxModel)
                if(constraintValue == propertyModel){
                    root.controlModel.currentIndex = index
                }
            }
            root.controlModel.selected.connect(modify)
        }
        else
        {
            console.warn("There is no validator related with " + root.objectName +" is an error if occurs at this moment")
        }                
    }

    function modify(val)
    {
        propertyModel = root.controlModel.model.get(val).objectName;
        if(root.constraintUrl.includes("scaleToOutput")){
          resourceModel.data.pipelineOptions.scaling.scaleToOutput = propertyModel
        }else{
          resourceModel.data.pipelineOptions.scaling.scaleToSize = propertyModel
        }
        _resourceStore.modify(resourceModel);
    }

    function setCurrentIndex() {
        console.log("setCurrentIndex",propertyModel)
        for( let index = 0 ; index < root.controlModel.model.size() ; index ++) {
            if(root.controlModel.model.get(index).value === propertyModel){
                root.controlModel.currentIndex = index
                break;
            }
        }
    }

    function getMediaSizeConfiguration() { 
        let ticketResponse = _resourceStore.get("/cdm/media/v1/configuration")

        ticketResponse.resolved.connect((future) => {
                                    console.log("media configuration resolved " + future.get());
                                    root.mediaSizeConfiguration = future.get();
                                    createStandardSizesModel();
                                });

        ticketResponse.rejected.connect((future) => {
                                    console.log("media configuration rejected ERROR:" + future.error);
                                });
    }

    function getSystemConfiguration(){
        let future = _resourceStore.get("/cdm/system/v1/configuration")

        future.resolved.connect((future) => {
            systemConfigModel = future.get();
            console.log("getSystemConfiguration: system config get")
        })

        future.rejected.connect((future) => {
            console.log("System config GET rejected");
            })
    }

    function updateConstraintModel(){
        if(resourceModel)
        {
            resourceModel.constraint.validators.rowsInserted.connect(validatorChanged)
        }
        else if(menuDynamicUrl)
        {
            let future = _resourceStore.subscribe(menuDynamicUrl, true)
            future.resolved.connect(function(){
                                        resourceModel = future.get();
                                        resourceModel.constraint.validators.rowsInserted.connect(validatorChanged)
                                    })
        }
    }

    function unpopulateModel() {
        for(var i=0; i < root.controlModel.model.count ; i++)
        {
            let res = root.controlModel.model.takeAt(i)
            res.destroy();
        }

        if(!root.controlModel.model.isEmpty())
        {
            root.controlModel.model.clear()
        }
    }
   
    function validatorChanged(){
        unpopulateModel();
        createStandardSizesModel();
    }

    Component.onCompleted: {
        console.log("CopySettingsResizeRadioCombobox: Component.onCompleted ");
        
        if(root.constraintUrl.includes("scaleToOutput"))
        {
            getSystemConfiguration();
            updateConstraintModel();
            getMediaSizeConfiguration();
        }else{
            createStandardSizesModel();
        }
        console.log(root.controlModel.currentIndex)
        propertyModelChanged.connect(setCurrentIndex)
    }

    Component.onDestruction: {
       if(root.constraintUrl.includes("scaleToOutput")){
          resourceModel.constraint.validators.rowsInserted.disconnect(validatorChanged);
       }
       
       propertyModelChanged.disconnect(setCurrentIndex);
    }
}