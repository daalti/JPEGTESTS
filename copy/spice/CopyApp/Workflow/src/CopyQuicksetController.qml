import QtQuick 2.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import "qrc:/QuickSetsUtils.js" as QuickSetsUtils

QtObject
{
    id: root
    property bool isDefaultQuicksetShown: true
    // \brief The application name
    property string applicationName;
    property string href;
    property string appId;
    property string cp_copy_load_quicksets: "a72db125-b0fd-484f-a1e4-feebd45495b2"

    onAppIdChanged: {
        console.log("appId changed")
    }

    property Component radioComponent: Component {
        RadioButtonModel {
            property bool pinProtected:false
            property string permissionId:""
            property string quickSetId: ""
        }
    }
    
    property QtObject quickSetListGroup: ButtonGroup {}

    function getCopyAppQuicksets(){
        
        QuickSetsUtils.getupdatedTheQuickSetView(refreshTheQuickSetsList)
    }

    function isThisOnTouchFromQuickSetApp(action, execute){
        QuickSetsUtils.isThisOnTouchFromQuickSetApp(action, execute)
    }

    function getHrefDetailsFromModal(quickSetModel) {
        if (quickSetModel) {
            for (let j = 0; j < quickSetModel.links.count; j++) {
                let link = quickSetModel.links.get(j);
                if (link.rel === "shortcut") {
                    return link.href
                }
            }
        }
    }

    function initializeQuickSetView(appName) {
        if(_stateMachine.quicksetsSupported) {

            let conf = QuickSetsUtils.getSourceAndDestinationDetails(appName)
            QuickSetsUtils.getAttributesToDisplay(root.appId, //ShortcutId
                                                 root.href,  // href link
                                                 _stateMachine, // Handle QuickSet related property
                                                 Shortcut_1_Type.Type.singleJob,conf); // its only for single Job
        }
        else {
            _stateMachine.quickSetVisibility = false
            _stateMachine.isTicketModelChanged = false
        }
    }

    function addQuickSetRadioButton(quickSetsListItemModel){
       let quicksetRadioObject = radioComponent.createObject(_stateMachine.quicksetListUnderAppModel,
                                                {
                                                    "objectName": quickSetsListItemModel ? quickSetsListItemModel.id : "Default",
                                                    "textObject": QuickSetsUtils.getStringToDisplay(quickSetsListItemModel),
                                                    "checked": quickSetsListItemModel ? _stateMachine.selectedQuicksetId == quickSetsListItemModel.id : _stateMachine.selectedQuicksetId == _stateMachine.defaultQuicksetName,
                                                    "icon": quickSetsListItemModel && _copyQuicksetIconList[quickSetsListItemModel.id] !== undefined ? _copyQuicksetIconList[quickSetsListItemModel.id] : "qrc:/images/Graphics/UserCreatedQuickset.json",
                                                    "variation": SpiceRadioButton.Type.Variation2,
                                                    "pinProtected": quickSetsListItemModel ? quickSetsListItemModel.pinProtected == Glossary_1_FeatureEnabled.FeatureEnabled.true_ : false,
                                                    "permissionId": quickSetsListItemModel ? root.cp_copy_load_quicksets : "",
                                                    "buttonGroup": quickSetListGroup,
                                                    "enabled": !_stateMachine.quicksetsSwitchingDisabled,
                                                    "quickSetId": quickSetsListItemModel ? quickSetsListItemModel.id : _stateMachine.defaultQuicksetName
                                                })
        _stateMachine.quicksetListUnderAppModel.append(quicksetRadioObject)
        quicksetRadioObject.enabled = Qt.binding(function(){ return !_stateMachine.quicksetsSwitchingDisabled })
        _stateMachine.quicksetListUnderAppModel.at(_stateMachine.quicksetListUnderAppModel.size() - 1).clicked.connect(function(val)
        {
            if(quickSetsListItemModel == null && _stateMachine.selectedQuicksetId != _stateMachine.defaultQuicksetName){
                _stateMachine.submitEvent("ev.quicksetSelectionChanged")
                _stateMachine.selectedQuicksetId = _stateMachine.defaultQuicksetName
                _stateMachine.quickSetSelected.stringId = "StringIds.cDefault"
                let conf = QuickSetsUtils.getSourceAndDestinationDetails(root.applicationName)
                console.log("getDefault Quickset")
                _stateMachine.quicksetSelectionUpdate = true
                _stateMachine.switchQuickset("defaults/copy")
            }
            else if(quickSetsListItemModel != null && _stateMachine.selectedQuicksetId != quickSetsListItemModel.id){ 
                _stateMachine.submitEvent("ev.quicksetSelectionChanged")
                /*update the shortcut id on selection, 
                this will be used to display the list in landing page*/
                _stateMachine.selectedQuicksetId = quickSetsListItemModel.id
                root.appId = quickSetsListItemModel.id; 
                if(quickSetsListItemModel.permissionId)
                    _stateMachine.quickSetPermissionIdSelected = quickSetsListItemModel.permissionId
                
                // check for pin protected quickset
                // Currently not for copy
                if (quickSetsListItemModel.pinProtected == Glossary_1_FeatureEnabled.FeatureEnabled.true_){
                    console.log("pin quickset")
                    console.log(quickSetsListItemModel.pinProtected)
                    _stateMachine.quicksetId = quickSetsListItemModel.id
                    // Since a pin promt is shown, we do not need to limit the swap speed.
                    // Also since it can be canceled we need to reenable this without changing

                    // This should be set when pin quickset is supported
                    //_stateMachine.quicksetsSwitchingDisabled = false
                    _stateMachine.submitEvent("ev.pin_quickset")
                }
                else
                {
                    QuickSetsUtils.setQuicksetSelectedName(_stateMachine, quickSetsListItemModel)

                    let href = ""
                    for(let j = 0; j < quickSetsListItemModel.links.count; j++) {
                            let link = quickSetsListItemModel.links.get(j);
                            if(link.rel === "shortcut") {
                                href=link.href
                                break;
                            }
                        }
                    let conf = QuickSetsUtils.getSourceAndDestinationDetails(root.applicationName)
                    console.log("quickset href",href)
                    _stateMachine.switchQuickset(href)
                }
            }
            else{
                console.log("Same quickset is clicked")
            }

        let item = _stack.nextItemInFocusChain(true)
        item.forceActiveFocus()
        })
    }

    function addViewAllQuickSetRadioButton(quickSetsListItemModel){
        
        let viewModel = radioComponent.createObject(_stateMachine.quicksetListUnderAppModel,
                                                {
                                                    "objectName": "ViewAll",
                                                    "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": "StringIds.cViewAll"}),
                                                    "checked": false,
                                                    "icon": "qrc:/images/Glyph/ExternalLinkSmall.json",
                                                    "variation": SpiceRadioButton.Type.Variation2,
                                                    "buttonGroup": quickSetListGroup
                                                });
        _stateMachine.quicksetListUnderAppModel.append(viewModel)

        _stateMachine.quicksetListUnderAppModel.at(_stateMachine.quicksetListUnderAppModel.size() - 1).clicked.connect(function(val)
        {
            
            if(!smallVersion){        
                updateTheQuickSetsRadioButtonList();
            }
            else{
                loadListOfQuickset();
            }
            
            // Dont select the view all radio button after pressing it.

            viewModel.checked = false;
            _stack.pushModal("qrc:/CopyApp/QuickSetListInApp.qml",
                {
                    "quickSetsModel":  _stateMachine.quickSetsModel,
                    "quicksetListUnderAppModel":_stateMachine.quicksetListAsRadioButton,
                    "quicksetModelList":_stateMachine.quicksetListModelList
                });
        })
    }



    function refreshTheQuickSetsList(future){
        if( !_stateMachine || _stateMachine.isOneTouchQuickSet == true ){
            return;
        }
         console.log("refreshTheQuickSetsList")

       // QuickSetsUtils.isCheckedVisibleInList(ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET,_stateMachine.quickSetsRespectiveAppModel)
        if(future)
        {
            _stateMachine.quickSetsSpecificToApp = future.get();
        }
            
        if(_stateMachine.quickSetsSpecificToApp && _stateMachine.quickSetsSpecificToApp.data.shortcuts)
        {
            let quickSetsList = _stateMachine.quickSetsSpecificToApp.data.shortcuts;
            _stateMachine.quicksetListUnderAppModel.clear()
            quickSetListGroup.buttons.length = 0            
            _stateMachine.quicksetListAsRadioButton.clear();
            _stateMachine.quicksetListModelList.clear();
                
            if(quickSetsList.count > 0)
            {
                // We only want to add the default quickset in case it is not page sensor flow
                root.isDefaultQuicksetShown = _stateMachine.isNonPageSensorflow();
                if(root.isDefaultQuicksetShown)
                {
                    addQuickSetRadioButton(null);
                }

                //Add quickset list (custom and/or factory)
                for (let count = 0; count < quickSetsList.count; count++)
                {
                    console.log("quickset radio")
                    let quickSetsPrivateModel = quickSetsList.get(count);
                    addQuickSetRadioButton(quickSetsPrivateModel)
                    
                    if(!smallVersion)
                    {
                        addQuickSetRadioButtonToList(quickSetsPrivateModel);
                    }
                    else
                    { 
                        addQuickSetList(quickSetsPrivateModel);
                    }
                }

                addViewAllQuickSetRadioButton(null);
            }
        }
    }

    function addQuickSetRadioButtonToList(quickSetsListItemModel){
        _stateMachine.quicksetListAsRadioButton.append(radioComponent.createObject(_stateMachine.quicksetListAsRadioButton,
                                                {
                                                    "objectName": quickSetsListItemModel ? quickSetsListItemModel.id : "Default",
                                                    "textObject": QuickSetsUtils.getStringToDisplay(quickSetsListItemModel),
                                                    "checked":  quickSetsListItemModel ? _stateMachine.selectedQuicksetId == quickSetsListItemModel.id : _stateMachine.selectedQuicksetId == _stateMachine.defaultQuicksetName,
                                                    "icon": quickSetsListItemModel && _copyQuicksetIconList[quickSetsListItemModel.id] !== undefined ? _copyQuicksetIconList[quickSetsListItemModel.id] : "qrc:/images/Graphics/UserCreatedQuickset.json",
                                                    "variation": SpiceRadioButton.Type.Variation2,
                                                    "pinProtected": quickSetsListItemModel ? quickSetsListItemModel.pinProtected == Glossary_1_FeatureEnabled.FeatureEnabled.true_ : false,
                                                    "permissionId": quickSetsListItemModel ? root.cp_copy_load_quicksets : "",
                                                    "buttonGroup": quickSetListGroup
                                                }))

        _stateMachine.quicksetListAsRadioButton.at(_stateMachine.quicksetListAsRadioButton.size() - 1).clicked.connect(function(val)
        {

            _stateMachine.selectedQuicksetId = quickSetsListItemModel.id
           
            root.appId = quickSetsListItemModel.id;
            if(quickSetsListItemModel.permissionId)
                _stateMachine.quickSetPermissionIdSelected = quickSetsListItemModel.permissionId
            
            // check for pin protected quickset
            // Currently not for copy
            if (quickSetsListItemModel.pinProtected == Glossary_1_FeatureEnabled.FeatureEnabled.true_){
                console.log("pin quickset")
                console.log(quickSetsListItemModel.pinProtected)
                _stateMachine.quicksetId = quickSetsListItemModel.id
                _stateMachine.submitEvent("ev.pin_quickset")
            }
            else
            {
                QuickSetsUtils.setQuicksetSelectedName(_stateMachine, quickSetsListItemModel)
                updateSelectedQuicksetOnLanding(quickSetsListItemModel)
                let href = ""
                for(let j = 0; j < quickSetsListItemModel.links.count; j++) {
                        let link = quickSetsListItemModel.links.get(j);
                        if(link.rel === "shortcut") {
                            href=link.href
                            break;
                        }
                    }
                let conf = QuickSetsUtils.getSourceAndDestinationDetails(root.applicationName)
                console.log("quickset href",_stateMachine.href)
                _stateMachine.switchQuickset(href)
                _stack.pop()
            }

        })

        // Select a quickset in case we don't have the default quickset
        if (_stateMachine.isPageSensorflow() && !_stateMachine.isSelectedQuicksetByDefault && _stateMachine.quicksetListAsRadioButton.count>0 && quickSetsListItemModel.id == root.appId)
        {
            QuickSetsUtils.setQuicksetSelectedName(_stateMachine, quickSetsListItemModel)
            var href = ""
            for(let j = 0; j < quickSetsListItemModel.links.count; j++) {
                    let link = quickSetsListItemModel.links.get(j);
                    if(link.rel === "shortcut") {
                        href=link.href
                        break;
                    }
                }
            let conf = QuickSetsUtils.getSourceAndDestinationDetails(root.applicationName)
            _stack.pop()
            _stateMachine.isSelectedQuicksetByDefault=true;
        }
    }


    function updateTheQuickSetsRadioButtonList(future){
        console.log("updateTheQuickSetsRadioButtonList")
        if(_stateMachine.quickSetsSpecificToApp && _stateMachine.quickSetsSpecificToApp.data.shortcuts){
            let quickSetsList1 = _stateMachine.quickSetsSpecificToApp.data.shortcuts;
            _stateMachine.quicksetListAsRadioButton.clear();
            for (let count = 0; count < quickSetsList1.count; count++){
                let quickSetsPrivateModel1 = quickSetsList1.get(count);
                addQuickSetRadioButtonToList(quickSetsPrivateModel1)
            }
        }
    }
    
    property Component qsListComponent: Component{
        ListViewModel {
            property SpiceLocObject textToDisplay: SpiceLocObject{}
            property bool pinProtected:false
            property string permissionId:""
            lined:true
            blocks:QQmlObjectListModel {
                RowBlockInfoModel {
                    imageTextModel: ImageTextModel{
                        images: ["qrc:/images/Glyph/Copy.json"]
                        contentsTexts: createContentText(textToDisplay)
                        imagesOrientation: Qt.AlignLeft
                    }
                }
            }
        }
    }

    function createContentText(textToDisplay){
        
        let contentsTexts = _qmlUtils.createCollection(root)
        contentsTexts.append(textToDisplay);
        return contentsTexts

    }

    function addQuickSetList(quickSetsListItemModel){
 
        _stateMachine.quicksetListModelList.append(qsListComponent.createObject(_stateMachine.quicksetListModelList,
                                                {
                                                    "objectName": quickSetsListItemModel ? quickSetsListItemModel.id : "Default",
                                                    "textToDisplay" : QuickSetsUtils.getStringToDisplay(quickSetsListItemModel),
                                                    "pinProtected": quickSetsListItemModel ? quickSetsListItemModel.pinProtected == Glossary_1_FeatureEnabled.FeatureEnabled.true_ : false,
                                                    "permissionId": quickSetsListItemModel ? root.cp_copy_load_quicksets : ""
                                                }))  
        _stateMachine.quicksetListModelList.at(_stateMachine.quicksetListModelList.size() - 1).clicked.connect(function(val)
        {
            _stateMachine.selectedQuicksetId = quickSetsListItemModel.id
            root.appId = quickSetsListItemModel.id;
            if(quickSetsListItemModel.permissionId)
                _stateMachine.quickSetPermissionIdSelected = quickSetsListItemModel.permissionId
            
            // check for pin protected quickset
            // Currently not for copy
            if (quickSetsListItemModel.pinProtected == Glossary_1_FeatureEnabled.FeatureEnabled.true_){
                console.log("pin quickset")
                console.log(quickSetsListItemModel.pinProtected)
                _stateMachine.quicksetId = quickSetsListItemModel.id
                _stateMachine.submitEvent("ev.pin_quickset")
            }
            else
            {
                QuickSetsUtils.setQuicksetSelectedName(_stateMachine, quickSetsListItemModel)
                updateSelectedQuicksetOnLanding(quickSetsListItemModel)
                let href = ""
                for(let j = 0; j < quickSetsListItemModel.links.count; j++) {
                        let link = quickSetsListItemModel.links.get(j);
                        if(link.rel === "shortcut") {
                            href=link.href
                            break;
                        }
                    }
                _stateMachine.switchQuickset(href)
                _stack.pop()
            }

        })                                                                                                         
    }

    function loadListOfQuickset(){
        
        console.log("loadListOfQuickset")
         if(_stateMachine.quickSetsSpecificToApp && _stateMachine.quickSetsSpecificToApp.data.shortcuts){
            let quickSetsList = _stateMachine.quickSetsSpecificToApp.data.shortcuts;
            _stateMachine.quicksetListModelList.clear();
            for (let count = 0; count < quickSetsList.count; count++){
                let quickSetsPrivateModel = quickSetsList.get(count);
                addQuickSetList(quickSetsPrivateModel)
            }
        }
    }

    function updateSelectedQuicksetOnLanding(quickSetsListItemModel){
        for(let i=0 ; i<_stateMachine.quicksetListUnderAppModel.size(); i++){
            if(quickSetsListItemModel.id == _stateMachine.quicksetListUnderAppModel.at(i).quickSetId){
                _stateMachine.quicksetListUnderAppModel.at(i).checked = true
                break
            }
        }
    }
    
}