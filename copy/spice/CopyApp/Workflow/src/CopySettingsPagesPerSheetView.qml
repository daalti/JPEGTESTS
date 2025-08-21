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
    objectName: "copy_pagesPerSheetView"
    header: SpiceLocObject {stringId: "StringIds.cPagesPerSheet"}

    property ISpiceModel ticketModel: null;

    // Properties used by pattern
    property QtObject menuResourceInstance: _menuResource
    property var pushMenuItem : null
    property var resourceModel : null
    property string valueResource:""
    property string constraint:""
    property string menuDynamicUrl: ""
    property string titleId:""
    property string enumType : "dune::spice::jobTicket_1::PagesPerSheet::PagesPerSheet"
    property string node:""
    property string imageBorderMessage: ""
    property bool isStampEnabled: false
    property bool imageBorderEnabled: false
    property bool pagesPerSheetUpdate: false
    property QtObject copySettingsHelper : CopySettingsHelper{}

    ButtonGroup {
        id: pagesPerSheetGroup
    }

    Component {
        id: radioButtonModelComponents
        RadioButtonModel {}
    }

    Component {
        id: radioButtonListViewModels
        SettingsRadioButtonViewModel{}        
    }

    Component {
        id: checkboxModelComponent
        CheckboxModel {}
    }

    Component {
        id: checkboxListViewModels
        SettingsCheckBoxViewModel{}
    }

    onNodeChanged: {
        if(node != ""){
            setImageBorderConstraint()
            let PagesPerSheetConstraint = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/imageModifications/pagesPerSheet");
            let imageBorderConstraint = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/imageModifications/imageBorder");

            if(PagesPerSheetConstraint)
            {
                for(var j=0; j< PagesPerSheetConstraint.options.count ; j++){
                    let constraintValue = PagesPerSheetConstraint.options.get(j).seValue
                    var stringId = _propertyMap.cStringIDForEnum(enumType, constraintValue)
                    console.log(constraintValue)
                    
                    if(constraintValue === "oneUp"){
                        addRadioButton("oneUp", stringId, JobTicket_1_PagesPerSheet.PagesPerSheet.oneUp, JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toBottomToLeft, 0, "qrc:/images/Glyph/PagesPerSheetOneUp.json")
                    }
                    else if (constraintValue === "twoUp"){
                        addRadioButton("twoUp", stringId, JobTicket_1_PagesPerSheet.PagesPerSheet.twoUp, JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toBottomToLeft, 1, "qrc:/images/Glyph/PagesPerSheetTwoUp.json")
                    }
                    else if(constraintValue === "fourUp"){   
                        addRadioButton("fourRightThenDown", _propertyMap.cStringIDForEnum(enumType, "fourRightThenDown"), JobTicket_1_PagesPerSheet.PagesPerSheet.fourUp, JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toRightToBottom, 2, "qrc:/images/Glyph/PagesPerSheetOrderZ.json")
                        addRadioButton("fourDownThenRight", _propertyMap.cStringIDForEnum(enumType, "fourDownThenRight"), JobTicket_1_PagesPerSheet.PagesPerSheet.fourUp, JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toBottomToRight, 3, "qrc:/images/Glyph/PagesPerSheetOrderN.json")
                    }
                }
                if(imageBorderConstraint){
                    addChcekBoxMenu("AddPageBorders", _propertyMap.cStringIDForEnum(enumType, "addPageBordersUCase"))
                }
            }
            else
            {
                console.warn("Pages per sheet constraint is null, not expected behavior occurs here. This must to be controlled at CopySettings.json level")
            }
            console.debug("Pages per sheet Component Start")
        }
    }

    function addRadioButton(objName, buttonStrId, enumVal1, enumVal2, enumVal, icon)
    {
        let validator = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/imageModifications/pagesPerSheet");
        let isEnabled = _stateMachine.controller.isSettingEnabled("pipelineOptions/imageModifications/pagesPerSheet")
        let message = ""

        if(validator && validator.disabled && validator.disabled.message)
        {
            message = validator.disabled.message
        }
        let radioButtonModel = radioButtonModelComponents.createObject(rowList,
                                                   {
                                                        "objectName": objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": buttonStrId }),
                                                        "checked": ((ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet == enumVal1) && (ticketModel.data.pipelineOptions.imageModifications.numberUpPresentationDirection == enumVal2)) ? true : false,
                                                        "clickable" : false,
                                                        "value": enumVal,
                                                        "enabled": isEnabled,
                                                        "constrained": !isEnabled,
                                                        "constrainedMessage": _qmlUtils.createSpiceLoc( root ,{"text":message}),
                                                        "icon": icon,
                                                        "buttonGroup": pagesPerSheetGroup
                                                   })
        
        radioButtonModel.clicked.connect(function()
        {   
            setPagesPerSheet(objName)
            pagesPerSheetUpdate  = !pagesPerSheetUpdate
            console.log("Modify resourceModel")
        })

        rowList.append(radioButtonListViewModels.createObject(rowList,
                                                    {
                                                        "controlModel": radioButtonModel,
                                                        "objectName" :  "ComboBoxOptions" + objName
                                                    }));
    }

    function addChcekBoxMenu(objName, buttonStrId)
    {
        let checkboxModel = checkboxModelComponent.createObject(rowList,
                                                    {
                                                        "objectName" : objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root , {"stringId": buttonStrId }),
                                                        "checked": ticketModel.data.pipelineOptions.imageModifications.imageBorder == JobTicket_1_ImageBorder.ImageBorder.defaultLineBorder ? true : false
                                                    });
        checkboxModel.constrained = Qt.binding(function() { return imageBorderEnabled ? false : true })
        checkboxModel.constrainedMessage.text = Qt.binding(function() { return imageBorderMessage })
        checkboxModel.onCheckedChanged.connect(function(){
            if(checkboxModel.checked)
            {
                ticketModel.data.pipelineOptions.imageModifications.imageBorder = JobTicket_1_ImageBorder.ImageBorder.defaultLineBorder
            }
            else
            {
                ticketModel.data.pipelineOptions.imageModifications.imageBorder = JobTicket_1_ImageBorder.ImageBorder.noBorder
            }
            _resourceStore.modify(ticketModel)
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

    function setPagesPerSheet(value){
        let enumVal1, enumVal2;
        console.log("modify the sides ",value)
        if (value == "oneUp"){
            enumVal1 = JobTicket_1_PagesPerSheet.PagesPerSheet.oneUp
            enumVal2 = JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toBottomToLeft
            ticketModel.data.pipelineOptions.imageModifications.imageBorder = JobTicket_1_ImageBorder.ImageBorder.noBorder
        }
        else if (value == "twoUp"){
            enumVal1 = JobTicket_1_PagesPerSheet.PagesPerSheet.twoUp
            enumVal2 = JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toBottomToLeft
        }
        else if (value == "fourRightThenDown"){
            enumVal1 = JobTicket_1_PagesPerSheet.PagesPerSheet.fourUp
            enumVal2 = JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toRightToBottom
        }
        else if (value == "fourDownThenRight"){
            enumVal1 = JobTicket_1_PagesPerSheet.PagesPerSheet.fourUp
            enumVal2 = JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toBottomToRight
        }

        ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet = enumVal1
        ticketModel.data.pipelineOptions.imageModifications.numberUpPresentationDirection = enumVal2
        _resourceStore.modify(ticketModel)
    }

    function setImageBorderConstraint() {
        let pagesPerSheet = _menuResource.enumStringFromValue("dune::spice::jobTicket_1::PagesPerSheet::PagesPerSheet", ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet)
        let isOneUp = (pagesPerSheet === "oneUp")
        
        if (isOneUp && isStampEnabled) {
            imageBorderEnabled = false
            imageBorderMessage = _qmlUtils.createSpiceLoc(root ,{"stringId": _propertyMap.cStringIDForEnum(enumType, "addPageBorderConstraint")}).text
        }
        else if (!isOneUp && isStampEnabled) {
            imageBorderEnabled = false
            imageBorderMessage = _qmlUtils.createSpiceLoc(root ,{"stringId": "StringIds.cFeatureCurrentNotAvailable"}).text
        }
        else if (isOneUp && !isStampEnabled) {
            imageBorderEnabled = false
            imageBorderMessage = _qmlUtils.createSpiceLoc(root ,{"stringId": _propertyMap.cStringIDForEnum(enumType, "addPageBorderConstraint")}).text
        }
        else {
            imageBorderEnabled = true
            imageBorderMessage = ""
        }
    }

    Component.onCompleted: {
        ticketModel = _stateMachine.ticketModel
        isStampEnabled = copySettingsHelper.isStampEnabled()
        pagesPerSheetUpdateChanged.connect(setImageBorderConstraint)
        console.log(" copy setting pagesPerSheet view disconnect")
    }

    Component.onDestruction: {
        pagesPerSheetUpdateChanged.disconnect(setImageBorderConstraint)
    }
}