import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxToastSystem 1.0
import "qrc:/QuickSetsUtils.js" as QuickSetsUtils

SpiceApplication {

    id: root
    objectName: "CopyApp"
    _stateMachine: SpiceStateMachine {

        /* WORKAROUND: This 2 properties no used but need for avoid broken code from
          common qml like progresView used in another product */
        property bool jobInProgress: false;
        property bool continuousCopy: false;
        property SpiceLocObject quickSetSelected: SpiceLocObject{}
        property string quickSetPermissionIdSelected : ""
        property ISpiceModel ticketModel: null;
        property ISpiceModel defaultTicketModel: null;
        property bool isTicketModelChanged: false
        property string newQuickSetName:""
        property bool newQuickSetStartInstantly:false
        property bool isTicketIdSubscribeReady:false
        property string ticketId: ""
        property int customResize: 100
        property ISpiceModel jobInfoModel: null;
        property ISpiceModel mediaConfiguration: null;
        property ISpiceModel scannerStatus: null;
        property bool quickSetVisibility :false;
        property QtObject copyControllerfunctions : CopyController{}
        property bool resizeCustomSelect: false;
        property string resizeSelected: "";
        property bool isOneTouchQuickSet : false;
        property string jobState: ""
        property string scannerState: ""
        property bool isScannerIdle: true
        property string menuDynamicUrl: ""
        property QtObject constraint: null;
        property bool isJobSubscribed: false;
        property bool isTicketSubscribed: false;

        // This property is added for the fix in gtest 
        // TODO: Need to remove it, 
        property QtObject cancelJobController: QtObject{
                                                    property string lastJobId: ""
                                                }


        url: "qrc:/CopyApp/copyApp.scxml"
        stack: root.applicationWindow.stack

        stateConfiguration: [
            { "name": "COPY_LANDING",                     "url": copyLandingView },
            { "name": "SELECT_SETTINGS",                  "url": "qrc:/CopyApp/CopyMenuView.qml" },
            { "name": "LIST_QUICKSETS",                   "url": copyQuickSetListView,  "args": { "appName":"CopyApp" } },
            { "name": "QUICKSETSAVE_OPTIONS",             "url": copyQuickSetSaveOptionsView, "args":{ "appName":"CopyApp" } },
            { "name": "QUICKSETSAVE_ENTERNAME",           "url": copyQuickSetEnterNewName},
            { "name": "QUICKSETSAVE_ASNEW",               "url": copyQuickSetSaveNewView}

        ]

        onTicketModelChanged: function ticketModelUpdate() {
            console.log("Ticket model changed: " + ticketModel)
        }

        function subscribeStateChanged(){
            console.log("Job Subscription: obtained state " + _stateMachine.jobInfoModel.data.state);
            processJobState();
        }

        function startCopy()
        {
            console.log("Start Copy")
            if((_stateMachine.jobInfoModel && _stateMachine.jobState == "ready") || _stateMachine.isOneTouchQuickSet){
                console.log("job is in ready state....check scanner")
                checkScannerState()
            }
            else {
                _stateMachine.showToastMessagePrinterIsBusy()
            }
        }

        function dismissToast()
        {
            if (!_stateMachine.isOneTouchQuickSet)
            {
                console.log("Toast dismissed")
                ToastSystem.toastDismissed();
            }
        }

        function checkScannerState(){
            console.log(_stateMachine.scannerState)
            console.log("Check scanner state it should be Idle")
            if(_stateMachine.scannerState == "Idle"){
                syncTicket()
            }
            else {
                _stateMachine.showToastMessagePrinterIsBusy()
            }
        }


        function syncTicket()
        {
            copyControllerfunctions.printTicketModel( _stateMachine.ticketModel );
    
            if (_stateMachine.isOneTouchQuickSet)
            {
                startOneTouchJob()
            }
            else
            {
                copyControllerfunctions.cloneCopyTicketstate();
            }
        }

        function startOneTouchJob() {
            console.log("CreateJob starts")
            copyControllerfunctions.createJob(_stateMachine.ticketModel.data.ticketId)
        }

        function showToastMessagePrinterIsBusy(){
            ToastSystem.showMessage(ToastSystem.createSpiceLoc({"stringId": "StringIds.cBusyPleaseWait"}), ToastSystem.ToastState.INFORMATION,3000)
            _stateMachine.submitEvent("ev.copy.failed")
        }

        function jobNotReady(){
            showToastMessagePrinterIsBusy()
        }

        function startJobFailed(future) {
            QuickSetsUtils.submit_event_basedOnAppLanuch_point("ev.copy.failed")
        }

        function subscribeJobResolved(future)
        {
            console.log("subscribeJobResolved-->")
            if(_stateMachine.jobInfoModel){
                _stateMachine.isJobSubscribed = true
            _stateMachine.jobInfoModel = future.get();
            copyControllerfunctions.printJobInfoModel(_stateMachine.jobInfoModel)
            processJobState();
            _stateMachine.jobInfoModel.data.stateChanged.connect(subscribeStateChanged);
            _stateMachine.copyControllerfunctions.intializeJob(future);
            }
            console.log("subscribeJobResolved<--")
        }

        function subscribeJobResolvedFailed(future)
        {
            console.log("subscribeJobResolvedFailed-->")
            console.log("queryJobResolvedFailed: " + future);
            let error = future.error;
            console.log("queryJobResolvedFailed: job query rejected " + error);
            if (error == IResourceStore.OperationResult.ERROR_RESOURCE_NOT_FOUND)
            {
                //job not found - exit workflow!
                console.log("ERROR! jobId not found. Exit the workflow");
            }
            console.log("subscribeJobResolvedFailed<--")
        }


        function processJobState()
        {
            if(_stateMachine.jobInfoModel){
                _stateMachine.jobState = _stateMachine.jobInfoModel.data.state

                console.log("jobInfoModel updated state",_stateMachine.jobState)

            }  
        }

        function startJobResolved(future) {
            if(_stateMachine.jobInfoModel){
                ToastSystem.showMessage(ToastSystem.createSpiceLoc({"stringId": "StringIds.cCopyingMessage", "params": [1, _stateMachine.ticketModel.data.dest.data.print.data.copies]}), ToastSystem.ToastState.INFORMATION,4000)
                console.log("startJobResolved: " + future + " status " + future.status);
                console.log("startJobResolved: obtained " + _stateMachine.jobInfoModel);
                console.log("startJobResolved: obtained jobId " + _stateMachine.jobInfoModel.data.jobId);
                console.log("startJobResolved: obtained state " + _stateMachine.jobInfoModel.data.state);
                _stateMachine.jobInProgress = true
                _stateMachine.jobInfoModel.data.stateChanged.disconnect(subscribeStateChanged);
                _resourceStore.unsubscribe(_stateMachine.jobInfoModel)
                _stateMachine.jobInfoModel = null
                _stateMachine.jobState = ""
                _stateMachine.copyControllerfunctions.createJob(_stateMachine.ticketModel.data.ticketId)
                _stateMachine.submitEvent("ev.copy.progress")
            }
        }

        function startJobResolvedFailed(future) {
            console.log("startJobResolvedFailed: " + future);
            let error = future.error;
            console.log("startJobResolvedFailed: job create rejected " + error);
            if (error == IResourceStore.OperationResult.ERROR_RESOURCE_NOT_FOUND)
            {
                console.log("ERROR! jobId not found. Exit the workflow");
                _stateMachine.jobInProgress = false;
            }
        }

        function oneTouchCreateJobResolved(future){
            _stateMachine.jobInProgress = true
            console.log("createJobResolved: " + future)
            ToastSystem.showMessage(ToastSystem.createSpiceLoc({"stringId": "StringIds.cStarting"}), ToastSystem.ToastState.INFORMATION,3000)
            _stateMachine.submitEvent("quitRequested");
        }

    }

    Component
    {
        id: copyLandingView
        CopyLandingView{}
    }

    Component {
        id: copyQuickSetListView
        QuickSetListView {}
    }

    Component {
        id: copyQuickSetSaveOptionsView
        QuickSetSaveOptionsView {}
    }
    Component {
        id: copyQuickSetSaveNewView
        QuickSetSaveNewView {}
    }
    Component {
        id: copyQuickSetEnterNewName
        QuickSetEnterNewName {}
    }

    function doStart() {
        _stateMachine.start();
        _stateMachine.copyControllerfunctions.initializeQuickSetView("CopyApp")
        _stateMachine.copyControllerfunctions.getMediaConfiguration();
        _stateMachine.copyControllerfunctions.subscribeScannerStatus();
        if(root.launchFrom == SpiceApplication.LaunchFromApp.QUICKSETAPP){
            QuickSetsUtils.isThisOnTouchFromQuickSetApp(root.selectedShortcutModel.action,Shortcut_1_Action.Action.execute)
        }

    }

    function doQuit(){
        // unsubscribe scanner status
        _stateMachine.copyControllerfunctions.unsubscribeScannerStatus();
        if(!_stateMachine.isOneTouchQuickSet && _stateMachine.ticketModel){
            console.log("Unsubscribing jobTicket")
            // unsubscribe ticketModel and cancel the job
            _resourceStore.unsubscribe(_stateMachine.ticketModel);
            _stateMachine.copyControllerfunctions.clearJobInfo();
        }
    }
}
