import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQml.Models 2.15
import "qrc:/SpiceBinding.js" as SpiceBinding

SpiceListView
{
    id: root
    objectName: "copyResizeView"
    header: SpiceLocObject {stringId: "StringIds.cSides"}
    property var pushMenuItem : null
    property var resourceModel : null
    property int xScaleMin: 0
    property int xScaleMax: 0
    property int xScaleStep: 0
    property string titleId:""
    property string enumType : ""
    property string valueResource:""
    property string constraint:""
    property string menuDynamicUrl: ""
    property string node:""

    property QtObject menuResourceInstance: _menuResource

    Component {
        id: controlModelComponents
        RadioButtonModel{}        
    }

    Component {
        id: sliderModelComponent
        SpinBoxModel {
            property int scalePercentSpinModel: value
        }
    }

    Component {
        id: radioButtonListViewModels
        SettingsRadioButtonViewModel{}
        
    }

    Component {
        id: spinBoxViewModel
        
        SettingsViewModel{
            id : root
            controlModel : SpinBoxModel {}
            visible : controlModel.visible
            clickable: false
            lined: true
            description :  SpiceLocObject { text: controlModel.description !== null ? controlModel.description.text : ""}
            blocks: QQmlObjectListModel {
                RowBlockComponentModel {
                    id: comonentBlock1
                    componentType: ControlModel.NodeType.Radio
                    alignment: Qt.AlignLeft
                    componentList: ObjectModel {
                        SpiceRadioButton {
                            id: spiceRadioButton
                            objectName: "customRadioButton"
                            checked: controlModel.checked
                            textObject: controlModel.infoText
                            buttonGroup: copyResizeGroup
                            constrained: controlModel.constrained
                            constrainedMessage: controlModel.constrainedMessage
                            Component.onCompleted: {
                                SpiceBinding.twoWayBinding(spiceRadioButton, "checked", controlModel)
                            }
                            onClicked: {
                                controlModel.clicked(controlModel)
                            }

                            Component.onDestruction: {
                                SpiceBinding.destroyTwoWayBinding(spiceRadioButton, "checked", controlModel)
                            }
                        }
                    }
                }
                RowBlockComponentModel {
                    id: comonentBlock
                    fillWidth: true
                    alignment: Qt.AlignRight
                    componentList: ObjectModel {
                        SpiceSpinBox {
                            id : menuSpiceSpinBox
                            objectName: controlModel.objectName === "" ? (controlModel.textObject === null ? "" : controlModel.textObject.text) : controlModel.objectName
                            value: controlModel.value
                            from: controlModel.from
                            to: controlModel.to
                            Component.onCompleted: {
                                SpiceBinding.twoWayBinding(menuSpiceSpinBox,"value",controlModel)
                            }
                            Component.onDestruction: {
                                SpiceBinding.destroyTwoWayBinding(menuSpiceSpinBox,"value",controlModel)
                            }
                        }
                    }
                }
            }
        }

    }

    Component {
        id: comboBoxListComponents
        ComboBoxListModel{}
    }

    Component {
        id: checkboxModelComponent
        CheckboxModel {}
    }

    Component {
        id: checkboxListViewModels
        SettingsCheckBoxViewModel{
            isSubordinate: true
        }
    }

    function setScaleValue(value){
        resourceModel.data.pipelineOptions.scaling.scaleSelection = value
        if(value == "none")
        {
            resourceModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            resourceModel.data.pipelineOptions.scaling.xScalePercent = 100
            resourceModel.data.pipelineOptions.scaling.yScalePercent = 100
        }
        else if(value == "fitToPage")
        {
            resourceModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.true_
            resourceModel.data.pipelineOptions.scaling.xScalePercent = 100
            resourceModel.data.pipelineOptions.scaling.yScalePercent = 100
        }
        else if(value == "fullPage")
        {
            resourceModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            resourceModel.data.pipelineOptions.scaling.xScalePercent = 91
            resourceModel.data.pipelineOptions.scaling.yScalePercent = 91
        }
        else if(value == "legalToLetter")
        {
            resourceModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            resourceModel.data.pipelineOptions.scaling.xScalePercent = 72
            resourceModel.data.pipelineOptions.scaling.yScalePercent = 72
        }
        else if(value == "letterToA4")
        {
            resourceModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            resourceModel.data.pipelineOptions.scaling.xScalePercent = 94
            resourceModel.data.pipelineOptions.scaling.yScalePercent = 94
        }
        else if(value == "a4ToLetter")
        {
            resourceModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            resourceModel.data.pipelineOptions.scaling.xScalePercent = 91
            resourceModel.data.pipelineOptions.scaling.yScalePercent = 91
        }
        else{
            console.log("Resize not selected")
        }
    }

    function addRadioButton(objName, buttonStrId, isLined = true)
    {
        let locControlModel = controlModelComponents.createObject(rowList,
                                                   {
                                                        "objectName": objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": buttonStrId}),
                                                        "clickable" : true,
                                                        "constrained": !isEnabled(objName),
                                                        "constrainedMessage": _qmlUtils.createSpiceLoc( root ,{"text":message(objName)}),
                                                        "buttonGroup": copyResizeGroup
                                                   })
        locControlModel.checked = Qt.binding(function(){return _menuResource.enumStringFromValue("dune::spice::jobTicket_1::scaling::ScaleSelection::ScaleSelection", resourceModel.data.pipelineOptions.scaling.scaleSelection) == objName ? true : false})
        locControlModel.clicked.connect(function(val)
        {
            if(locControlModel.checked){
                console.log("Modify resourceModel")
                setScaleValue(objName)
                _resourceStore.modify(resourceModel)
            }
        })

        rowList.append(radioButtonListViewModels.createObject(rowList,
                                                                {"controlModel": locControlModel ,
                                                                   "objectName" : objName + "Row",
                                                                   "lined" : isLined
                                                                }))
    }

    function addSliderButton(objName, buttonStrId){
        let spinModel   =  sliderModelComponent.createObject(rowList,
                                                   {
                                                       "objectName": objName,
                                                       "infoText.stringId": "StringIds.cCustomPara",
                                                       "infoText.params": [resourceModel.data.pipelineOptions.scaling.xScalePercent],
                                                       "checked": _menuResource.enumStringFromValue("dune::spice::jobTicket_1::scaling::ScaleSelection::ScaleSelection", resourceModel.data.pipelineOptions.scaling.scaleSelection) == objName ? true : false,
                                                       "clickable" : true,
                                                       "from": root.xScaleMin,
                                                        "to": root.xScaleMax,
                                                        "stepSize": root.xScaleStep,
                                                        "value":  resourceModel.data.pipelineOptions.scaling.xScalePercent,
                                                        "constrained" : !isEnabled(objName),
                                                        "constrainedMessage": _qmlUtils.createSpiceLoc( root ,{"text":message(objName)}) 
                                                   })

        spinModel.checked = Qt.binding(function(){
            return _menuResource.enumStringFromValue("dune::spice::jobTicket_1::scaling::ScaleSelection::ScaleSelection", resourceModel.data.pipelineOptions.scaling.scaleSelection) == objName ? true : false
        })

        spinModel.clicked.connect(function(val)
        {
            console.log("Modify resourceModel")
            resourceModel.data.pipelineOptions.scaling.scaleSelection = spinModel.objectName
            resourceModel.data.pipelineOptions.scaling.xScalePercent = spinModel.value
            resourceModel.data.pipelineOptions.scaling.yScalePercent = spinModel.value
            _resourceStore.modify(resourceModel)
        })

        spinModel.onValueChanged.connect(function(val)
        {
            
            console.log("Modify resourceModel")
            spinModel.infoText.params = [spinModel.scalePercentSpinModel]
            if(spinModel.checked){
                console.log("Modify resourceModel")
                resourceModel.data.pipelineOptions.scaling.scaleSelection = spinModel.objectName
                resourceModel.data.pipelineOptions.scaling.xScalePercent = spinModel.value
                resourceModel.data.pipelineOptions.scaling.yScalePercent = spinModel.value
                _resourceStore.modify(resourceModel)
            }
        })

        rowList.append(spinBoxViewModel.createObject(rowList,
                                                                {"controlModel": spinModel ,
                                                                   "objectName" : objName + "Row"
                                                                }))
    }

    function addComboBoxRadioButton(scaleSelectionConstraintOption, buttonStrId, constraintUrl, propertyModel, constraintEnumType){
        let isSettingEnabled = _stateMachine.controller.isSettingEnabled(constraintUrl)
        let validator = _stateMachine.controller.findValidatorForConstraint(constraintUrl);
        let message = ""
        if(validator && validator.disabled && validator.disabled.message)
        {
            message = validator.disabled.message
        }
        if(scaleSelectionConstraintOption.disabled)
        {
            isSettingEnabled = isSettingEnabled && 
                              !(scaleSelectionConstraintOption.disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
            if (scaleSelectionConstraintOption.message) 
                message = scaleSelectionConstraintOption.message
        }
        let objName = scaleSelectionConstraintOption.seValue
        let comboBoxListModel   =  comboBoxListComponents.createObject(rowList,
                                                   {
                                                       "objectName": objName,
                                                       "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": buttonStrId}),
                                                       "checked": _menuResource.enumStringFromValue("dune::spice::jobTicket_1::scaling::ScaleSelection::ScaleSelection", resourceModel.data.pipelineOptions.scaling.scaleSelection) === objName ? true : false,
                                                       "infoText.stringId" : buttonStrId,
                                                       "enabled": isSettingEnabled,
                                                       "constrained": !isSettingEnabled,
                                                       "constrainedMessage.text": message
                                                   })
        comboBoxListModel.clicked.connect(function(val)
        {
            console.log("combobox changed")
            setScaleValue(objName)
            _resourceStore.modify(resourceModel)
        })
        let  customLfpComponent = Qt.createComponent("qrc:/CopyApp/CopySettingsResizeRadioCombobox.qml") 
        rowList.append(customLfpComponent.createObject(rowList,
                                                                {"controlModel": comboBoxListModel ,
                                                                   "objectName" : objName + "Row",
                                                                   "constraintEnumType" : constraintEnumType,
                                                                   "constraintUrl" : constraintUrl,
                                                                   "propertyModel":propertyModel,
                                                                   "resourceModel": resourceModel
                                                                }))

    }

    function addChcekBoxMenu(objName, buttonStrId, message, checkedItem, constraintItem)
    {
        let checkboxModel = checkboxModelComponent.createObject(rowList,
                                                    {
                                                        "objectName" : objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root , {"stringId": buttonStrId }),
                                                        "visible": isSupported(), 
                                                        "checked": checkedItem == Glossary_1_FeatureEnabled.FeatureEnabled.true_ ? true : false,
                                                        "constrainedMessage": _qmlUtils.createSpiceLoc( root ,{"text": _qmlUtils.createSpiceLoc(root ,{"stringId": message}).text}),
                                                    });
        checkboxModel.constrained = Qt.binding(function(){return resourceModel.data.pipelineOptions.scaling.scaleSelection == constraintItem ? false : true})
        checkboxModel.onCheckedChanged.connect(function(){
            if(checkboxModel.checked)
            {
                resourceModel.data.pipelineOptions.scaling.fitToPageIncludeMargin = Glossary_1_FeatureEnabled.FeatureEnabled.true_
            }
            else
            {
                resourceModel.data.pipelineOptions.scaling.fitToPageIncludeMargin = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            }
            _resourceStore.modify(resourceModel)
        });

        checkboxModel.onConstrainedChanged.connect(function(){
            if(checkboxModel.constrained)
            {
                checkboxModel.checked = false
            }
        });

        rowList.append(checkboxListViewModels.createObject(rowList,
                                                        {
                                                            "objectName" : "CheckBoxOptions" + objName,
                                                            "controlModel": checkboxModel
                                                        }));
    }

    function isSupported()
    { 
        let validator = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/scaling/fitToPageIncludeMargin");

        for(var j=0; j< validator.options.count ; j++){
            let constraintValue = validator.options.get(j)
            if( constraintValue.hasOwnProperty("disabled") && (constraintValue.disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_) )
            {
                return false;
            }
        }
        return true;
    }

    function isEnabled(scaleSelectionValue)
    {
        let validator = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/scaling/scaleSelection");
        let enabled = true;

        if(validator)
        {
            for(let j=0; j < validator.options.count ; j++)
            {
                let constraintValue = validator.options.get(j).seValue
                if(constraintValue == scaleSelectionValue){
                    enabled = validator.options.get(j).disabled == Glossary_1_FeatureEnabled.FeatureEnabled._undefined_ || validator.options.get(j).disabled == Glossary_1_FeatureEnabled.FeatureEnabled.false_
                }
            }
        }
        return enabled;
    }

    function message(scaleSelectionValue)
    {
        let validator = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/scaling/scaleSelection");
        let constrainedMessage = "";

        if(validator)
        {
            for(let j=0; j < validator.options.count ; j++)
            {
                let constraintValue = validator.options.get(j).seValue
                if(constraintValue == scaleSelectionValue){
                    let enabled = validator.options.get(j).disabled == Glossary_1_FeatureEnabled.FeatureEnabled._undefined_ || validator.options.get(j).disabled == Glossary_1_FeatureEnabled.FeatureEnabled.false_
                    if(!enabled && validator.options.get(j).message)
                    {
                        constrainedMessage = validator.options.get(j).message;
                    }
                }
            }
        }
        return constrainedMessage;
    }

    Component {
        id: radioComponent
        RadioButtonModel {
        }
    }

    ButtonGroup {
        id: copyResizeGroup
    }

    onNodeChanged: {
        if(node != ""){
            enumType = "dune::spice::jobTicket_1::scaling::ScaleSelection::ScaleSelection"
            if(_stateMachine.isNonPageSensorflow()){
                _stateMachine.constraintModel = resourceModel.constraint
            }
            let validatorForXScale = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/scaling/xScalePercent");
            if(validatorForXScale != null)
            {
                xScaleMin = validatorForXScale.data.min.data.value;
                xScaleMax = validatorForXScale.data.max.data.value;
                xScaleStep = validatorForXScale.data.step.data.value;
            }
            else
            {
                console.error("validatorForXScale is null.")
                xScaleMin = 25;
                xScaleMax = 400;
                xScaleStep = 1;
            }
            let scaleSelectionConstraint = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/scaling/scaleSelection");

            if(scaleSelectionConstraint)
            {
                for(var j=0; j< scaleSelectionConstraint.options.count ; j++){
                    let constraintValue = scaleSelectionConstraint.options.get(j).seValue
                    var stringId = _propertyMap.cStringIDForEnum(enumType, constraintValue)
                    console.log(constraintValue)
                    if(constraintValue === "fitToPage"){
                        addRadioButton(constraintValue, stringId, !isSupported())
                        if(isSupported()){
                            let constrainedMessage = _propertyMap.cStringIDForEnum("fitToPageIncludeMargin","OutputScaleConstraint")
                            addChcekBoxMenu("fitToPageIncludeMargin", "StringIds.cAutoIncludeMargins", constrainedMessage, resourceModel.data.pipelineOptions.scaling.fitToPageIncludeMargin, JobTicket_1_Scaling_ScaleSelection.ScaleSelection.fitToPage)
                        }
                    }
                    else if (constraintValue === "custom"){
                        addSliderButton(constraintValue, stringId)
                    }
                    else if(constraintValue === "scaleToOutput")
                    {   
                        addComboBoxRadioButton(scaleSelectionConstraint.options.get(j), stringId, "pipelineOptions/scaling/scaleToOutput", resourceModel.data.pipelineOptions.scaling.scaleToOutput, "dune::spice::glossary_1::MediaSourceId::MediaSourceId")
                    }
                    else if(constraintValue === "standardSizeScaling")
                    {
                        addComboBoxRadioButton(scaleSelectionConstraint.options.get(j), stringId, "pipelineOptions/scaling/scaleToSize", resourceModel.data.pipelineOptions.scaling.scaleToSize, "dune::spice::glossary_1::MediaSize::MediaSize")
                    }
                    else{
                        addRadioButton(constraintValue, stringId)
                    }
                }
            }
            else
            {
                console.warn("Scale selection constraint is null, not expected behavior occurs here. This must to be controlled at CopySettings.json level")
            }
            
            console.debug("Resize Component Start")
        }
    }

    Component.onDestruction: {
        console.log(" copy setting resize view disconnect")
    }
}
