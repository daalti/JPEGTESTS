import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import "qrc:/QuickSetsUtils.js" as QuickSetsUtils


RadioButtonListLayout
{
    id: quickSetListView
    objectName: "QuickSetListView"
    property string appName : ""
    property bool radioButtonChecked : false
    property ISpiceModel quickSetsModel: null;
    property ISpiceModel quickSetsModelOfFirstIndex: null;
    header: SpiceLocObject {stringId: "StringIds.cDefaultsAndQuickSets"}


    function getStringToDisplay(quickSetsListItemModel){
        if(quickSetsListItemModel == null){
            if(_stateMachine.quickSetSelected.stringId === "StringIds.cDefault")
                quickSetListView.radioButtonChecked = true

            else
                quickSetListView.radioButtonChecked = false

            return _qmlUtils.createSpiceLoc( quickSetListView , {"stringId": "StringIds.cDefault"})

        }

        if(quickSetsListItemModel.title)
        {

            if(quickSetsListItemModel.title == _stateMachine.quickSetSelected.text )
                quickSetListView.radioButtonChecked = true

            else
                quickSetListView.radioButtonChecked = false

            return _qmlUtils.createSpiceLoc( quickSetListView , {"text": quickSetsListItemModel.title})

        }
        else if(quickSetsListItemModel.titleId){

            if(_stateMachine.quickSetSelected.stringId == quickSetsListItemModel.titleId)
                quickSetListView.radioButtonChecked = true

            else
                quickSetListView.radioButtonChecked = false

            return _qmlUtils.createSpiceLoc( quickSetListView , {"stringId": quickSetsListItemModel.titleId})

        }
        else{
            if(quickSetsListItemModel.id == _stateMachine.quickSetSelected.text )
                quickSetListView.radioButtonChecked = true
            else
                quickSetListView.radioButtonChecked = false

            return _qmlUtils.createSpiceLoc( quickSetListView , {"text": quickSetsListItemModel.id})

        }

    }

    function addRadioButton(quickSetsListItemModel){

        options.append(radioComponent.createObject(options,
                                                   {
                                                       "objectName": quickSetsListItemModel ? quickSetsListItemModel.title : "Default",
                                                       "textObject": quickSetListView.getStringToDisplay(quickSetsListItemModel),
                                                       "checked": quickSetListView.radioButtonChecked,
                                                       "buttonGroup": quickSetListGroup
                                                   }))
        options.at(options.size() - 1).buttonGroup.buttons[options.size() - 1].clicked.connect(function(val)
        {
            if(quickSetsListItemModel == null){
                _stateMachine.quickSetSelected.stringId = "StringIds.cDefault"
                let conf = QuickSetsUtils.getSourceAndDestinationDetails(quickSetListView.appName)
                QuickSetsUtils.getDefaultTicketModel(_stateMachine, ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET, conf)
            }
            else {

                QuickSetsUtils.setQuicksetSelectedName(_stateMachine, quickSetsListItemModel)

                if(quickSetsListItemModel.permissionId)
                    _stateMachine.quickSetPermissionIdSelected = quickSetsListItemModel.permissionId
                
                // check for pin protected quickset
                if (quickSetsListItemModel.pinProtected == Glossary_1_FeatureEnabled.FeatureEnabled.true_){
                    console.log("pin quickset")
                    console.log(quickSetsModel.pinProtected)
                    _stateMachine.quicksetId = quickSetsListItemModel.id
                    _stateMachine.handlePinProtected()
                }
                else
                {
                    var href = ""
                    for(let j = 0; j < quickSetsListItemModel.links.count; j++) {
                            let link = quickSetsListItemModel.links.get(j);
                            if(link.rel === "shortcut") {
                                href=link.href
                                break;
                            }
                        }
                    let conf = QuickSetsUtils.getSourceAndDestinationDetails(quickSetListView.appName)
                    QuickSetsUtils.getTicketModelFromQuickSetSelected(href,
                                                                    _stateMachine,
                                                                    ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET,
                                                                    conf, "ev.back")
                }
            }
        })
    }




    Component {
        id: radioComponent
        RadioButtonModel {
        }
    }

    ButtonGroup {
        id: quickSetListGroup
    }

    Component.onCompleted: {

        if (typeof _stateMachine.isDefaultRequired !== 'undefined'){
            if (_stateMachine.isDefaultRequired == true){
                addRadioButton(null) // add default option in quickSet list
            }
        }
        else{
            addRadioButton(null)
        }

        initializeTheView(updateTheQuickSetsList);
    }

    function updateTheQuickSetsList(future){
        quickSetsModel = future.get();
        if(quickSetsModel && quickSetsModel.data.shortcuts){
            let quickSetsList = quickSetsModel.data.shortcuts;
            for (var count = 0; count < quickSetsList.count; count++){
                let quickSetsPrivateModel = quickSetsList.get(count);
                addRadioButton(quickSetsPrivateModel)
            }
        }
    }

    function initializeTheView(updateTheQuickSet) {
        let conf = QuickSetsUtils.getSourceAndDestinationDetails(quickSetListView.appName)

        let future = _resourceStore.get("/cdm/shortcut/v1/shortcuts?type=singleJob&source="+conf.source+"&destination="+conf.destination)
        future.resolved.connect((future) => {
                                    updateTheQuickSet(future)
                                });

        future.rejected.connect((future) => {
                                    requestQuickSetsListFailure(future)
                                });

    }

    function refreshTheQuickSetsList(){
        options.removeAt(0,options.count);
        quickSetListGroup.buttons.length = 0
        isCheckedVisibleInList()

        if (typeof _stateMachine.isDefaultRequired !== 'undefined'){
            if (_stateMachine.isDefaultRequired == true){
                addRadioButton(null) // add default option in quickSet list
            }
        }
        else{
            addRadioButton(null)
        }
        if(quickSetsModel && quickSetsModel.data.shortcuts){
            let quickSetsList = quickSetsModel.data.shortcuts;
            for (var count = 0; count < quickSetsList.count; count++){
                let quickSetsPrivateModel = quickSetsList.get(count);
                addRadioButton(quickSetsPrivateModel)
            }

        }
    }

    function isCheckedVisibleInList(){

        let fFound = false
        if(_stateMachine.quickSetSelected.stringId === "StringIds.cDefault"){
            return
        }
        if(quickSetsModel && quickSetsModel.data.shortcuts){
            let quickSetsList = quickSetsModel.data.shortcuts;
            for (var count = 0; count < quickSetsList.count; count++){
                let quickSetsPrivateModel = quickSetsList.get(count);
                quickSetsModelOfFirstIndex = quickSetsList.get(0); // copy first quickset and use it when none is checked
                if(quickSetsPrivateModel.title)
                {
                    if(quickSetsPrivateModel.title == _stateMachine.quickSetSelected.text )
                        fFound = true
                    else
                        fFound = false
                }
                else if(quickSetsPrivateModel.titleId){
                    if(_stateMachine.quickSetSelected.stringId == quickSetsPrivateModel.titleId)
                        fFound = true
                    else
                        fFound = false
                }
                else{
                    if(quickSetsPrivateModel.id == _stateMachine.quickSetSelected.text )
                        fFound = true
                    else
                        fFound = false
                }

                if(fFound == true)
                    break;
            }
        }

        if(fFound == false){
            if(quickSetsModelOfFirstIndex.titleId){
                _stateMachine.quickSetSelected.stringId = quickSetsModelOfFirstIndex.titleId
            }
            else if(quickSetsModelOfFirstIndex.title){
                _stateMachine.quickSetSelected.text = quickSetsModelOfFirstIndex.title

            }
            else
                _stateMachine.quickSetSelected.text = quickSetsModelOfFirstIndex.id


            let conf = QuickSetsUtils.getSourceAndDestinationDetails(quickSetListView.appName)
            QuickSetsUtils.getTicketModelFromQuickSetSelected(href,
                                                              _stateMachine,
                                                              ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET,
                                                              conf, "")
        }
    }

    function requestQuickSetsListFailure(future){
        var error = future.error;
        console.log("QuickSetsList Failure: " + error);
    }
}
