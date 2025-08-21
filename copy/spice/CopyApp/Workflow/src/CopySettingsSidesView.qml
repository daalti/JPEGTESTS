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

SettingsComboBoxViewModel
{
    id : root
    property var menuNode:null
    property var pushMenuItem : null
    property var resourceModel : null 
    property string titleId:""
    property string enumType : ""
    property string valueResource:""
    property string constraint:""
    property string permissionId: ""
    property string cp_copy_sides_permission_id: "ea01cb1c-841e-47b7-a448-a83772b4d51b"
    property QtObject menuResourceInstance: _menuResource
    property Component controlModelComponent : ComboBoxModel{}
    objectName: menuNode ? menuNode["id"]+ "MenuComboBox": "MenuComboBox"
    readonly property QtObject menuDelegateProperties : MenuDelegateProperties{}
    property QtObject validator: null
    property QtObject scanValidator: null
    property bool isDuplexConstrained: false
    property bool isSimplexConstrained: false
    property bool isScanDuplexConstrained: false
    property SpiceLocObject constrainedMessageForComboboxEntries: SpiceLocObject{}
    property bool isScanSimplexConstrained: false
    property url menuDynamicUrl: ""
    property bool isNodeOnLeftPanel: false
    property var resourceInstance: null

    onMenuNodeChanged: {
        if(menuNode){
            controlModel.textObject.stringId =  Qt.binding(function(){return menuNode.titleId})
            console.log(menuNode.displayDependencies)
            console.log(menuNode.titleId)
            let dataObj = _templatesData.valueMapFromList("menuComboBox", menuNode["id"])
            const dict = (dataObj === null) ? null : dataObj.asMap()
            if(dict !== null)
            {
                if(dict.hasOwnProperty("valueResource"))
                {
                    menuDelegateProperties.valueResource_ = dict["valueResource"]
                }
            }
            DelegateApplier.createDelegates(menuNode)
            if(resourceModel)
            {
                menuDelegateProperties.dataModel = resourceModel
                updateData()
                setCurrentIndex()
            }
            else if(menuDynamicUrl)
            {
                let future = _resourceStore.subscribe(menuDynamicUrl, true)
                future.resolved.connect(function(){
                                            menuDelegateProperties.dataModel = future.get()
                                            updateData()
                                            setCurrentIndex()
                                        })
            }
            controlModel.updateModel.connect(populateModel)
        }
    }

    function updateData(){
        menuDelegateProperties.dataModel.data.dest.print.plexModeChanged.connect(setCurrentIndex);
        menuDelegateProperties.dataModel.data.src.scan.plexModeChanged.connect(setCurrentIndex);
        let obj = _qmlUtils.parseMenuResourceEntry(menuDelegateProperties.valueResource_)
        let propArray = obj[1]
        root.menuDelegateProperties.modelPath = propArray
        root.menuDelegateProperties.field = propArray.pop()
        root.menuDelegateProperties.propertyModel =SpicePropertyValueFromModel.findPropertyValueFromModelForPropertyArray(menuDelegateProperties.dataModel,propArray)
        updateConstraint()
    }

    function updateConstraint()
    {
        if (root.menuDelegateProperties.constraint !== '') {
            let fut = _resourceStore.subscribe(root.menuDelegateProperties.constraint)
            fut.resolved.connect(constraintGet)
        }
        else if(root.menuDelegateProperties.dataModel.constraint)  {
            createResolver(root.menuDelegateProperties.dataModel.constraint)
        }
    }

    function constraintGet(future)
    {
        let constraintModel = future.get()
        let constraintObject = constraintModel.data
        createResolver(constraintObject)
    }
    function createResolver(constraintObject)
    {
        //root.menuDelegateProperties.resolverComp = Qt.createComponent("qrc:/ConstraintResolver.qml")
        if(root.menuDelegateProperties.constrainedResolver)
        {
            root.menuDelegateProperties.constrainedResolver.destroy()
        }
        root.menuDelegateProperties.constrainedResolver = root.menuDelegateProperties.resolverComp.createObject(root, {"dataModel":root.menuDelegateProperties.dataModel.data, "constraintModel":constraintObject})
        root.validator = root.menuDelegateProperties.constrainedResolver.validatorObjectFor(root.menuDelegateProperties.field, root.menuDelegateProperties.propertyModel)

        // connect constraint for scan plex mode
        let obj = _qmlUtils.parseMenuResourceEntry("data.src.scan.plexMode")
        let propArray = obj[1]
        let scanField = propArray.pop()
        let scanPropertyModel =SpicePropertyValueFromModel.findPropertyValueFromModelForPropertyArray(menuDelegateProperties.dataModel,propArray)
        root.scanValidator = root.menuDelegateProperties.constrainedResolver.validatorObjectFor(scanField, scanPropertyModel)
    }

    onValidatorChanged: {
        if(validator === null)
        {
            controlModel.constrained = false
            updateConstraint()
        }
        else
        {
            if(validator.disabled && validator.disabled.value == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
            {
                controlModel.constrained = true
                controlModel.constrainedMessage.text = validator.disabled.message
            }
            for(let i=0 ; i < validator.options.count ; i++)
            {
                if(validator.options.get(i).seValue == "simplex")
                {
                    let simplexOption = validator.options.get(i)
                    if(simplexOption.disabled && simplexOption.disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
                    {
                        isSimplexConstrained = true
                        constrainedMessageForComboboxEntries.stringId = simplexOption.messageId
                    }
                    else { isSimplexConstrained = false }
                }
                else if(validator.options.get(i).seValue == "duplex")
                {
                    let duplexOption = validator.options.get(i)
                    if(duplexOption.disabled && duplexOption.disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
                    {
                        isDuplexConstrained = true
                        constrainedMessageForComboboxEntries.stringId = duplexOption.messageId
                    }
                    else { isDuplexConstrained = false }
                }
                
            }
        }
    }

    onScanValidatorChanged: {
        if(scanValidator === null)
        {
            updateConstraint()
        }
        else
        {
            for(let i=0 ; i < scanValidator.options.count ; i++)
            {
                if(scanValidator.options.get(i).seValue == "simplex")
                {
                    let simplexOption = scanValidator.options.get(i)
                    if(simplexOption.disabled && simplexOption.disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
                    {
                        isScanSimplexConstrained = true
                        constrainedMessageForComboboxEntries.stringId = simplexOption.messageId
                        
                    }
                    else { isScanSimplexConstrained = false }
                               
                }
                else if(scanValidator.options.get(i).seValue == "duplex")
                {
                    let duplexOption = scanValidator.options.get(i)
                    if(duplexOption.disabled && duplexOption.disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
                    {
                        isScanDuplexConstrained = true
                        constrainedMessageForComboboxEntries.stringId = duplexOption.messageId
                    }
                    else { isScanDuplexConstrained = false }
                   
                }
                
            }
        }
    }

    function populateModel() {
        unpopulateModel()
        addComboBoxButton("Copy1to1Sided", "StringIds.c1To1Sided", Glossary_1_PlexMode.PlexMode.simplex, Glossary_1_PlexMode.PlexMode.simplex)
        addComboBoxButton("Copy1to2Sided", "StringIds.c1To2Sided", Glossary_1_PlexMode.PlexMode.simplex, Glossary_1_PlexMode.PlexMode.duplex)
        addDuplexComboBoxButton("Copy2to1Sided", "StringIds.c2To1Sided", Glossary_1_PlexMode.PlexMode.duplex, Glossary_1_PlexMode.PlexMode.simplex)
        addDuplexComboBoxButton("Copy2to2Sided", "StringIds.c2To2Sided", Glossary_1_PlexMode.PlexMode.duplex, Glossary_1_PlexMode.PlexMode.duplex)
        console.log(root.controlModel.model.count)
        setCurrentIndex()
        root.controlModel.selected.connect(function (val)
        {
            let value =  root.controlModel.model.get(val).value
            setSides(value)
        })
        
    }

    function unpopulateModel() {
        for(let i = root.controlModel.model.count-1 ; i >= 0 ; i--)
        {
            let res = root.controlModel.model.takeAt(i)
            res.destroy();
        }
        if(!root.controlModel.model.isEmpty())
        {
             root.controlModel.model.clear()
        }
    }

    function setDuplexBinding(plexMode, pagesFlipUpEnabled) {
        if(plexMode == Glossary_1_PlexMode.PlexMode.simplex)
        {
            menuDelegateProperties.dataModel.data.dest.data.print.data.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.oneSided
        }
        else
        {
            if(pagesFlipUpEnabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
            {
                menuDelegateProperties.dataModel.data.dest.data.print.data.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.twoSidedShortEdge
            }
            else
            {
                menuDelegateProperties.dataModel.data.dest.data.print.data.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.twoSidedLongEdge
            }
        }
        console.debug("sidesSettingView: duplexBinding is " + menuDelegateProperties.dataModel.data.dest.data.print.data.duplexBinding)
    }

    function setSides(value){
        let enumVal1, enumVal2;
        console.log("modify the sides ",value)
        if (value == "Copy1to1Sided"){
            enumVal1 = Glossary_1_PlexMode.PlexMode.simplex
            enumVal2 = Glossary_1_PlexMode.PlexMode.simplex
        }
        else if (value == "Copy1to2Sided"){
            enumVal1 = Glossary_1_PlexMode.PlexMode.simplex
            enumVal2 = Glossary_1_PlexMode.PlexMode.duplex
        }
        else if (value == "Copy2to1Sided"){
            enumVal1 = Glossary_1_PlexMode.PlexMode.duplex
            enumVal2 = Glossary_1_PlexMode.PlexMode.simplex
        }
        else if (value == "Copy2to2Sided"){
            enumVal1 = Glossary_1_PlexMode.PlexMode.duplex
            enumVal2 = Glossary_1_PlexMode.PlexMode.duplex
        }

        menuDelegateProperties.dataModel.data.src.data.scan.data.plexMode = enumVal1;
        menuDelegateProperties.dataModel.data.dest.data.print.data.plexMode = enumVal2;
        setDuplexBinding(menuDelegateProperties.dataModel.data.dest.data.print.data.plexMode, menuDelegateProperties.dataModel.data.src.data.scan.data.pagesFlipUpEnabled)
        _resourceStore.modify(menuDelegateProperties.dataModel)
    }

    function setCurrentIndex() {
        if(menuDelegateProperties.dataModel.data.src.scan.plexMode == Glossary_1_PlexMode.PlexMode.simplex && menuDelegateProperties.dataModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.simplex)
        {
            controlModel.currentIndex = 0
            controlModel.selectedValue.stringId = "StringIds.c1To1Sided"
        }
        else if(menuDelegateProperties.dataModel.data.src.scan.plexMode == Glossary_1_PlexMode.PlexMode.simplex && menuDelegateProperties.dataModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.duplex)
        {
            controlModel.currentIndex = 1
            controlModel.selectedValue.stringId = "StringIds.c1To2Sided"
        }
        else if(menuDelegateProperties.dataModel.data.src.scan.plexMode == Glossary_1_PlexMode.PlexMode.duplex && menuDelegateProperties.dataModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.simplex)
        {
            controlModel.currentIndex = 2
            controlModel.selectedValue.stringId = "StringIds.c2To1Sided"
        }
        else if(menuDelegateProperties.dataModel.data.src.scan.plexMode == Glossary_1_PlexMode.PlexMode.duplex && menuDelegateProperties.dataModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.duplex)
        {
            controlModel.currentIndex = 3
            controlModel.selectedValue.stringId = "StringIds.c2To2Sided"
        }

    }
    function addComboBoxButton(objName, buttonStrId, enumVal1, enumVal2){
        let locControlModel   =  controlModelComponent.createObject(root,
                                                   {
                                                       "objectName": objName,
                                                       "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": buttonStrId}),
                                                       "checked": ((menuDelegateProperties.dataModel.data.src.data.scan.data.plexMode == enumVal1) && (menuDelegateProperties.dataModel.data.dest.data.print.data.plexMode == enumVal2)) ? true : false,
                                                       "visible" : true,
                                                       "value": objName
                                                   })
        root.controlModel.model.append(locControlModel)
        if(objName == "Copy1to1Sided")
        {
            console.log("ryu copy1to1Sided constraint")
            locControlModel.constrained = Qt.binding(function() {return root.isSimplexConstrained || root.isScanSimplexConstrained})
            locControlModel.constrainedMessage = Qt.binding(function() {return root.constrainedMessageForComboboxEntries})
            locControlModel.permissionId = Qt.binding(function() {return root.cp_copy_sides_permission_id})
        }
        else if(objName == "Copy1to2Sided")
        {
            locControlModel.constrained = root.isDuplexConstrained || root.isScanSimplexConstrained
            root.controlModel.model.get(root.controlModel.model.count -1).constrained = Qt.binding(function() {return root.isDuplexConstrained || root.isScanSimplexConstrained})
            root.controlModel.model.get(root.controlModel.model.count -1).constrainedMessage = Qt.binding(function() {return root.constrainedMessageForComboboxEntries})
        }
    }

    function addDuplexComboBoxButton(objName, buttonStrId, enumVal1, enumVal2){
        let locControlModel   =  controlModelComponent.createObject(root,
                                                   {
                                                       "objectName": objName,
                                                       "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": buttonStrId}),
                                                       "checked": ((menuDelegateProperties.dataModel.data.src.data.scan.data.plexMode == enumVal1) && (menuDelegateProperties.dataModel.data.dest.data.print.data.plexMode == enumVal2)) ? true : false,
                                                       "value": objName
                                                   })
        locControlModel.visible = Qt.binding(function(){return (_stateMachine.isDuplexSupported);})
        root.controlModel.model.append(locControlModel)
        if(objName == "Copy2to2Sided")
        {
            locControlModel.constrained = root.isDuplexConstrained || root.isScanDuplexConstrained
            root.controlModel.model.get(root.controlModel.model.count -1).constrained = Qt.binding(function() {return root.isDuplexConstrained || root.isScanDuplexConstrained})
            root.controlModel.model.get(root.controlModel.model.count -1).constrainedMessage = Qt.binding(function() {return root.constrainedMessageForComboboxEntries})
        }
        else if (objName == "Copy2to1Sided")
        {
            locControlModel.constrained = root.isScanDuplexConstrained || root.isSimplexConstrained
            root.controlModel.model.get(root.controlModel.model.count -1).constrained = Qt.binding(function() {return root.isScanDuplexConstrained || root.isSimplexConstrained})
            root.controlModel.model.get(root.controlModel.model.count -1).constrainedMessage = Qt.binding(function() {return root.constrainedMessageForComboboxEntries})
            locControlModel.permissionId = Qt.binding(function() {return root.cp_copy_sides_permission_id})
        }
    }

    Component.onDestruction: {
        if(menuDelegateProperties.constrainedResolver)
        {
            menuDelegateProperties.constrainedResolver.destroy()
        } 
        if(menuDelegateProperties.dataModel){
            console.log("copy setting side disconnect")
            menuDelegateProperties.dataModel.data.dest.print.plexModeChanged.disconnect(setCurrentIndex);
            menuDelegateProperties.dataModel.data.src.scan.plexModeChanged.disconnect(setCurrentIndex);
        }
        controlModel.updateModel.disconnect(populateModel)
        unpopulateModel()
    }

    Component.onCompleted: {
        console.log("copy_sides completed")
    }
    
}
