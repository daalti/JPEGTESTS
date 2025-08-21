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
    objectName: "copyFoldView"
    header: SpiceLocObject {stringId: _propertyMap.valueMap("FinisherFoldOption").asMap()["fold"]}
    property var pushMenuItem : null
    property var resourceModel : null
    property string titleId:""
    property string enumType : ""
    property string valueResource:""
    property string constraint:""
    property string menuDynamicUrl: ""
    property string node: ""

    property QtObject menuResourceInstance: _menuResource

    Component {
        id: controlModelComponents
        RadioButtonModel{}        
    }

    Component {
        id: sliderModelComponent
        SpinBoxModel{}
    }

    Component {
        id: radioButtonListViewModels
        SettingsRadioButtonViewModel{
        }  
    }

    Component {
        id: radioButtonListViewSubordinateModels
        SettingsRadioButtonViewModel{
            lined:false
            isSubordinate: true
        }  
    }

    Component {
        id : spinBoxViewModel

        SettingsSpinBoxViewModel {
            id : root
            controlModel : SpinBoxModel {}
            visible : controlModel.visible
            isSubordinate : true
            clickable : false
            lined : false
            description.text : controlModel.description !== null ? controlModel.description.text : ""
            property var imagePath : ""
            property string infoText : ""
            blocks : QQmlObjectListModel {
                RowBlockComponentModel {
                    fillWidth : true
                    alignment : Qt.AlignLeft
                    componentList : ObjectModel {
                        SpiceTextImage  {
                            Layout.fillWidth: true
                            imagesOrientation: Qt.AlignLeft
                            imagesAlignMiddle: false
                            images : [imagePath]
                            contentsTexts: QQmlObjectListModel{
                                SpiceLocObject{
                                    stringId : "StringIds.cMaximumSheetsPerSet"
                                }
                            }
                        }
                    }
                }
                RowBlockComponentModel {
                    id : comonentBlock
                    fillWidth : true
                    alignment : Qt.AlignRight
                    componentList : ObjectModel {
                        SpiceSpinBox {
                            id : menuSpiceSpinBox
                            objectName : controlModel.objectName === "" ? (controlModel.textObject === null ? "" : controlModel.textObject.text) : controlModel.objectName
                            value : controlModel.value
                            from : controlModel.from
                            to : controlModel.to
                            decimals : controlModel.decimals
                            stepSize : controlModel.stepSize
                            spinboxText : controlModel.spinboxText
                            Component.onCompleted : {
                                SpiceBinding.twoWayBinding(menuSpiceSpinBox, "value", controlModel)
                            }
                            Component.onDestruction : {
                                SpiceBinding.destroyTwoWayBinding(menuSpiceSpinBox, "value", controlModel)
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

    footer: SpiceFooter {
        anchors {left: parent.left; right: parent.right;}
        rightBlockModel: QQmlViewListModel {
            SpiceButton {
                id: doneButton
                objectName: "doneButton"
                type: SpiceButton.Type.Primary
                Layout.alignment: Qt.AlignRight
                textObject: SpiceLocObject {
                    stringId: "StringIds.cDoneButton"
                }
                onClicked: {
                    _window.postViewEvent(QmlUtils.ViewEventType.Back)
                }
            }
        }
    }

    function addRadioButton(objName, buttonStrId, valueIndex, isLined)
    {
        let validator = _stateMachine.controller.findValidatorForConstraint("dest/print/foldOption")
        let isConstrained = false
        let message = ""

        for (let index =0 ; index < validator.options.count ;index++ )
        {
            let value = validator.options.get(index).seValue
            if((objName === "V-fold" && value === "vInwardTop")
                    || (objName === "C-fold" && value === "cInwardTop"))
            {
                if(validator.options.get(index).disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
                {
                   isConstrained = true
                   message = validator.options.get(index).message
                   break
                }
            }
        }

        let locControlModel = controlModelComponents.createObject(rowList,
                                                   {
                                                        "objectName": objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": buttonStrId}),
                                                        "icon": getIconImage(objName),
                                                        "checked": foldOptionCheckValue(objName),
                                                        "clickable" : true,
                                                        "value": valueIndex,
                                                        "constrained": isConstrained,
                                                        "constrainedMessage": _qmlUtils.createSpiceLoc( root ,{"text":message}),
                                                        "buttonGroup": copyFoldGroup
                                                   })

        locControlModel.clicked.connect(function(val)
        {
            if(foldOptionCheckValue(objName))
            {
                return
            }
            setFoldOptionValue(objName)
            reArrangeSubOptions(objName)
            _resourceStore.modify(resourceModel)
        })

        rowList.append(radioButtonListViewModels.createObject(rowList,
                                                                {"controlModel": locControlModel ,
                                                                "objectName" : objName + "Row",
                                                                "lined" : isLined
                                                                }))
    }

    function addRadioButtonSubOrdinateVFold(objName, buttonStrId, valueIndex, isLined)
    {
        let validator = _stateMachine.controller.findValidatorForConstraint("dest/print/foldOption")
        let isEnabled = _stateMachine.controller.isSettingEnabled("dest/print/foldOption")
        let message = ""

        if(validator && validator.disabled && validator.disabled.message)
        {
            message = validator.disabled.message
        }

        let locControlModel = controlModelComponents.createObject(rowList,
                                                   {
                                                        "objectName": objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": buttonStrId}),
                                                        "icon": getIconImage(objName),
                                                        "checked": _menuResource.enumStringFromValue("dune::spice::jobTicket_1::FoldOptions::FoldOptions", resourceModel.data.dest.print.foldOption) == objName ? true : false,
                                                        "clickable" : true,
                                                        "value": valueIndex,
                                                        "enabled": isEnabled,
                                                        "constrained": !isEnabled,
                                                        "constrainedMessage": _qmlUtils.createSpiceLoc( root ,{"text":message}),
                                                        "buttonGroup": copyVFoldOptionGroup
                                                   })

        locControlModel.clicked.connect(function(val)
        {
            setFoldOptionValue(objName)
            _resourceStore.modify(resourceModel)
        })

        rowList.append(radioButtonListViewSubordinateModels.createObject(rowList,
                                                                {"controlModel": locControlModel ,
                                                                "objectName" : objName + "Row",
                                                                "lined" : isLined
                                                                }))
    }  
    
    function addRadioButtonSubOrdinateCFold(objName, buttonStrId, valueIndex)
    {
        let validator = _stateMachine.controller.findValidatorForConstraint("dest/print/foldOption")
        let isEnabled = _stateMachine.controller.isSettingEnabled("dest/print/foldOption")
        let message = ""

        if(validator && validator.disabled && validator.disabled.message)
        {
            message = validator.disabled.message
        }

        let locControlModel = controlModelComponents.createObject(rowList,
                                                   {
                                                        "objectName": objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": buttonStrId}),
                                                        "icon": getIconImage(objName),
                                                        "checked": _menuResource.enumStringFromValue("dune::spice::jobTicket_1::FoldOptions::FoldOptions", resourceModel.data.dest.print.foldOption) == objName ? true : false,
                                                        "clickable" : true,
                                                        "value": valueIndex,
                                                        "enabled": isEnabled,
                                                        "constrained": !isEnabled,
                                                        "constrainedMessage": _qmlUtils.createSpiceLoc( root ,{"text":message}),
                                                        "buttonGroup": copyCFoldOptionGroup
                                                   })

        locControlModel.clicked.connect(function(val)
        {
            setFoldOptionValue(objName)
            _resourceStore.modify(resourceModel)
        })

        rowList.append(radioButtonListViewSubordinateModels.createObject(rowList,
                                                                {"controlModel": locControlModel ,
                                                                "objectName" : objName + "Row"
                                                                }))
    }  

    function addSliderButton(objName){ 
        
        let sheetsConstraint
        let sheetsResourceModel

        if(objName === "C-fold")
        {
            sheetsConstraint = "dest/print/sheetsPerFoldSet/cFoldSheets"
            sheetsResourceModel = resourceModel.data.dest.print.sheetsPerFoldSet.cFoldSheets
        }
        else if(objName === "V-fold")
        {
            sheetsConstraint = "dest/print/sheetsPerFoldSet/vFoldSheets"
            sheetsResourceModel = resourceModel.data.dest.print.sheetsPerFoldSet.vFoldSheets
        }
        let validatorFoldSheets = _stateMachine.controller.findValidatorForConstraint(sheetsConstraint);

        let minValue = validatorFoldSheets.data.min.data.value
        let maxValue = validatorFoldSheets.data.max.data.value
        let stepValue = validatorFoldSheets.data.step.data.value

        let spinModel =  sliderModelComponent.createObject(rowList,
                                                   {
                                                       "objectName": objName,
                                                       "infoText.stringId": "StringIds.cMaximumSheetsPerSet",
                                                       "isSubordinate": true,
                                                       "from": minValue,
                                                       "to": maxValue,
                                                       "stepSize": stepValue,
                                                       "value":  sheetsResourceModel,
                                                       "spinboxText": _qmlUtils.createSpiceLoc(root, {"stringId": "StringIds.cKeyPadRangeWithLabel","params": [_qmlUtils.createSpiceLoc(root, {"stringId": "StringIds.cMaximum"}),minValue, maxValue]})
                                                   })

        spinModel.onValueChanged.connect(function(val)
        {
            if(objName === "C-fold")
            {
                resourceModel.data.dest.print.sheetsPerFoldSet.cFoldSheets = spinModel.value
            }
            else if(objName === "V-fold")
            {
                resourceModel.data.dest.print.sheetsPerFoldSet.vFoldSheets = spinModel.value
            }
            _resourceStore.modify(resourceModel)
        })

        rowList.append(spinBoxViewModel.createObject(rowList,
                                                                {"controlModel": spinModel ,
                                                                   "objectName" : objName + "SpinRow"
                                                                }))
    }

    function setFoldOptionValue(objectName)
    {
        switch(objectName)
        {
            case "none":
                resourceModel.data.dest.print.foldOption = "none";
                break;
            case "C-fold":
                resourceModel.data.dest.print.foldOption = "cInwardTop";
                break;
            case "V-fold":
                resourceModel.data.dest.print.foldOption = "vInwardTop";
                break;
            case "cInwardTop":
                resourceModel.data.dest.print.foldOption = "cInwardTop";
                break;
            case "cInwardBottom":
                resourceModel.data.dest.print.foldOption = "cInwardBottom";
                break;
            case "cOutwardTop":
                resourceModel.data.dest.print.foldOption = "cOutwardTop";
                break;
            case "cOutwardBottom":
                resourceModel.data.dest.print.foldOption = "cOutwardBottom";
                break;
            case "vInwardTop":
                resourceModel.data.dest.print.foldOption = "vInwardTop";
                break;
            case "vOutwardTop":
                resourceModel.data.dest.print.foldOption = "vOutwardTop";
                break;
        }
    }

    function foldOptionCheckValue(objectName)
    {
        let retValue = false

        if(objectName === "C-fold")
        {
            switch(resourceModel.data.dest.print.foldOption.toString())
            {
                case "cInwardTop":
                case "cInwardBottom":
                case "cOutwardTop":
                case "cOutwardBottom": 
                    retValue = true
                    break;
            }
        }
        else if(objectName === "V-fold")
        {
            switch(resourceModel.data.dest.print.foldOption.toString())
            {
                case "vInwardTop":
                case "vInwardBottom":
                case "vOutwardTop":
                case "vOutwardBottom": 
                    retValue = true
                    break;
            }
        }

        if(resourceModel.data.dest.print.foldOption.toString() === objectName)
        {
            retValue = true
        }
        return retValue
    }

    Component {
        id: radioComponent
        RadioButtonModel {
        }
    }

    ButtonGroup {
        id: copyFoldGroup
    }

    ButtonGroup {
        id: copyVFoldOptionGroup
    }

    ButtonGroup {
        id: copyCFoldOptionGroup
    }

    function getIconImage(objName)
    {
        let iconImage;

        if(resourceModel.data.src.scan.contentOrientation.toString() === "portrait")
        {
            if(objName === 'none')
            {
                iconImage = "qrc:/images/Glyph/NoFoldPortrait.json";
            }
            else if(objName === 'V-fold' || objName === 'vInwardTop' || objName === 'vInwardBottom')
            {
                iconImage = "qrc:/images/Glyph/VFoldInward.json"
            }
            else if(objName === 'vOutwardTop'|| objName === 'vOutwardBottom')
            {
                iconImage = "qrc:/images/Glyph/VFoldOutward.json"
            }
            else if(objName === 'C-fold' || objName === 'cInwardTop')
            {
                iconImage = "qrc:/images/Glyph/CFoldInwardTop.json"
            }
            else if(objName === 'cInwardBottom')
            {
                iconImage = "qrc:/images/Glyph/CFoldInwardBottom.json"
            }
            else if(objName === 'cOutwardTop')
            {
                iconImage = "qrc:/images/Glyph/CFoldOutwardTop.json"
            }
            else if(objName === 'cOutwardBottom')
            {
                iconImage = "qrc:/images/Glyph/CFoldOutwardBottom.json"
            }
        }
        else
        {
            if(objName === 'none')
            {
                iconImage = "qrc:/images/Glyph/NoFoldLandscape.json";
            }
            else if(objName === 'V-fold'|| objName === 'vInwardTop' || objName === 'vInwardBottom')
            {
                iconImage = "qrc:/images/Glyph/VFoldInwardRight.json"
            }
            else if(objName === 'vOutwardTop'|| objName === 'vOutwardBottom')
            {
                iconImage = "qrc:/images/Glyph/VFoldOutwardRight.json"
            }
            else if(objName === 'C-fold' || objName === 'cInwardTop')
            {
                iconImage = "qrc:/images/Glyph/CFoldInwardLeft.json"
            }
            else if(objName === 'cInwardBottom')
            {
                iconImage = "qrc:/images/Glyph/CFoldInwardRight.json"
            }
            else if(objName === 'cOutwardTop')
            {
                iconImage = "qrc:/images/Glyph/CFoldOutwardLeft.json"
            }
            else if(objName === 'cOutwardBottom')
            {
                iconImage = "qrc:/images/Glyph/CFoldOutwardRight.json"
            }
        }
        return iconImage
    }

    function reArrangeSubOptions(objectName)
    {
        rowList.removeAt(0, rowList.count)
        addMainFoldOptions()
    }

    function addSubOptionsforCFold(){

        addSliderButton("C-fold")
        addRadioButtonSubOrdinateCFold("cInwardTop", _propertyMap.cStringIDForString("FinisherFoldOption", "cInwardTop"), true, 0)
        addRadioButtonSubOrdinateCFold("cInwardBottom", _propertyMap.cStringIDForString("FinisherFoldOption", "cInwardBottom"), true, 1)
        addRadioButtonSubOrdinateCFold("cOutwardTop",_propertyMap.cStringIDForString("FinisherFoldOption", "cOutwardTop"), true, 2)    
        addRadioButtonSubOrdinateCFold("cOutwardBottom", _propertyMap.cStringIDForString("FinisherFoldOption", "cOutwardBottom"), true, 3)
    }
    
    function addSubOptionsforVFold(){
        addSliderButton("V-fold")
        addRadioButtonSubOrdinateVFold("vInwardTop", _propertyMap.cStringIDForString("FinisherFoldOption", "vInwardTop"), 0, false)
        addRadioButtonSubOrdinateVFold("vOutwardTop", _propertyMap.cStringIDForString("FinisherFoldOption", "vOutwardTop"), 1, true)
    }

    function addMainFoldOptions(){
        
        let validator = _stateMachine.controller.findValidatorForConstraint("dest/print/foldOption")
        addRadioButton("none", "StringIds.cNone", 0, true)

        if(validator.options.count > 1)
        {
            for (let index =0 ; index < validator.options.count;index++ )
            {
                if(validator.options.get(index).seValue === "vInwardTop")
                {
                    if(foldOptionCheckValue("V-fold"))
                    {
                        addRadioButton("V-fold", _propertyMap.cStringIDForString("FinisherFoldOption", "vFold"), 1, false)
                        addSubOptionsforVFold()
                    }
                    else
                    {
                        addRadioButton("V-fold", _propertyMap.cStringIDForString("FinisherFoldOption", "vFold"), 1, true)
                    }
                }
                else if(validator.options.get(index).seValue === "cInwardTop")
                {
                    if(foldOptionCheckValue("C-fold"))
                    {
                        addRadioButton("C-fold", _propertyMap.cStringIDForString("FinisherFoldOption", "cFold"), 2, false)
                        addSubOptionsforCFold()
                    }
                    else
                    {
                        addRadioButton("C-fold", _propertyMap.cStringIDForString("FinisherFoldOption", "cFold"), 2, true)
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        console.log(" copy setting Fold view connect")
    }

    onNodeChanged: {
        if(node != ""){
            console.debug("Fold Component Start")
            addMainFoldOptions()
        }
    }

    Component.onDestruction: {
        console.log(" copy setting Fold view disconnect")
    }
}
