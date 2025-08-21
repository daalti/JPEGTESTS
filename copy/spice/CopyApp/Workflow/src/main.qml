import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxToastSystem 1.0
import walkupApp 1.0 as WalkupApp
import walkupcontroller 1.0
import "qrc:/QuickSetsUtils.js" as QuickSetsUtils
import "qrc:/imports/spiceuxToastSystem/SpiceToastUtils.js" as SpiceToastUtils

SpiceApplication {

    id: root
    objectName: "CopyApp"

    property bool smallVersion: Global.breakpoint <= Global.BreakPoint.S
    property real numberOfCopiesFromWidget:1
    property bool isAutoStartJobFromWidget:false
    property bool resetEvent: false
    property bool isDefaultQuicksetShown: true
    isViewRequired: _stateMachine.isOneTouchQuickSet ? _stateMachine.isPreviewRequired() : true
    // QtObject that helps to report user activity.
    // Created dynamically for the products that want it.
    property QtObject activityTracker: null
    property string prioritySessionId: ""; 

    property var walkupController : WalkupControllerMain{
        defaultTicketReference: "defaults/copy"
        forceDefaultTicketCloning: _stateMachine.isPageSensorflow() ? true : false
        onTicketCreated:{
            console.log("ticket created")
            var highestPriorityModeSessionId = _stateMachine.controller.getHighestPriorityModeSessionId();
            walkupController.priorityModeSessionId = highestPriorityModeSessionId;
            if(_stateMachine.isAdfCapabilities()){
                _stateMachine.controller.updateScannerMediaSource()
            }
            if (_stateMachine.isMdfCapabilities() && _stateMachine.isPageSensorflow()){
                _stateMachine.setTicketAsMultipage()
            }
            _stateMachine.submitEvent("ev.ticketReceived");
        }

        onTicketSubscribed:{
            console.log("ticket subscribed")
            _stateMachine.menuResourceModel = _stateMachine.ticketModel
            _stateMachine.controller.connectEachDataChange()
            _stateMachine.isEditSettingsActionEnabled = true
            _stateMachine.isTicketSubscribed = true
        }

        onJobSubscribed:{
                console.log("copyApp jobSubscribed completed")
                _stateMachine.isJobSubscribed = true
                _stateMachine.jobInfoModel.data.stateChanged.connect( _stateMachine.processJobState);
        }

        onJobReady:{
            console.log("Job Ready")
            _stateMachine.isJobInReadyState = true
            _stateMachine.submitEvent("ev.jobInitialized");
        }

        onPreviewProcessed:{
            _stateMachine.previewJobId = _stateMachine.jobInfoModel.data.jobId
            _stateMachine.inPreviewState = true
            _stateMachine.previewReady = false
        }

        onProcessing:{
            if(_stateMachine.isJobAutoStart)
            {
                _stateMachine.jobInProgress = true
                if(!_stateMachine.isLaunchedFromWidget)
                {
                    _stateMachine.toastHandle.showToast("StringIds.cStringEllipsis", { params: ["StringIds.cStarting"], timeout: _stateMachine.toastTimeout })
                }
                _stateMachine.inPreviewState = false;
                _stateMachine.submitEvent("quitRequested")
            }
            else
            {
                console.log("Job Processing")  
                _stateMachine.jobInProgress = true
                if(_stateMachine.isConcurrent && !_stateMachine.isPageSensorflow()){
                    _stateMachine.toastHandle.showToast("StringIds.cStringEllipsis", { params: ["StringIds.cStarting"], timeout: _stateMachine.toastTimeout })
                }
                _stateMachine.isJobSubscribed = false
                _stateMachine.submitEvent("ev.copy.progress") 
            }       
        }

        onJobStartFailed:{
            console.log("Job started failed")
            _stateMachine.submitEvent("quitRequested")

        }

        onTicketRefreshed:{
            if(_stateMachine.quicksetSelectionUpdate)
            {
                console.log("Quickset Switched")
                _stateMachine.metricUnitSelected = ""
                 _stateMachine.quicksetSelectionUpdate = false
                _stateMachine.menuResourceModel = _stateMachine.ticketModel
                    if(_stateMachine.isPageSensorflow()) {
                        _stateMachine.showToastSettingUpdatedBettwenPages()
                        Qt.callLater(function(){_stateMachine.quicksetsSwitchingDisabled = false;})
                    }
                    if(_stateMachine.ticketModel.constraint) {
                        _stateMachine.constraintModel = _stateMachine.ticketModel.constraint
                    }
                    _stateMachine.submitEvent("ev.quickset.switched") 
            }
        }

        onOneTouchJobStarted:{
            if(!_stateMachine.isPreviewRequired())
            {
                console.log("One Touch Job Started")
                _stateMachine.jobInProgress = true
                _stateMachine.toastHandle.showToast("StringIds.cStringEllipsis", { params: ["StringIds.cStarting"], timeout: _stateMachine.toastTimeout })
                _stateMachine.inPreviewState = false;
                _stateMachine.submitEvent("quitRequested");
            }    
        }

        onOneTouchJobFailed:{
            console.log("One Touch Job Failed")
            _stateMachine.submitEvent("quitRequested");
        }

        onWalkupfailure:{
            console.log("walkupController failure",msg)
            _stateMachine.submitEvent("quitRequested");
        }    
    }

    _stateMachine: SpiceStateMachine {
        property var ticketModel: walkupController.ticketModel;
        property ISpiceModel jobInfoModel: walkupController.jobModel;
        property ISpiceModel priorityModeSessionModel: null;
        property string priorityModeSessionId: root.prioritySessionId
        property ISpiceModel priorityInterruptModeSessionModel: null;
        property QtObject constraint: null;
        property ISpiceModel constraintModel: null;
        property bool isConcurrent : _jobConcurrencySupported
        property bool quicksetsSupported : false
        //----Widget properties, they are set in doStart----------
        property bool isJobAutoStart: false
        property bool isLaunchedFromWidget: false
        property bool isLaunchedFromWidgetOptions: false
        property bool isMediaLoadedBeforeEntry:false
        property string ticketModelIdFromWidget: ""
        property string jobTicketUrl: ""
        property bool isTicketSubscribed: false
        property string metricUnitSelected: ""

        property int inputMediaSourceSelected: 0
        //-------------------
        property string selectedQuicksetId: "";

        // isSelectedQuicksetByDefault is used to select a quickset in case of not having a default quickset
        property bool isSelectedQuicksetByDefault: false;

        
        //hasBeenToastShownForLastSettingChangesAfterLastScan is used to notify the user that a setting for scanning between pages has been changed.
        // It is displayed only once shown after every page is acquired if settings are changed.
        property bool hasBeenToastShownForLastSettingChangesAfterLastScan:true;

        //This clone ticket is used to clone ticketModel, taking a snapshot and use it for current jobInfoModel to be scanned/copied
        property ISpiceModel lastTicketClone: null;

        // Temporal ticket model used in resourceStore operations. Its main purpose is to keep a reference to the shared model
        // provided by resourceStore, this way, the model doesn't get unintentionally unallocated while 
        // waiting for the resourceStore future to finish.
        property ISpiceModel tmpTicketModel: null;

        property QtObject activityTracker: root.activityTracker;

        //State machine configurations defined by Capabilities request
        //This capabalities request is on WIP by Om
        //Next setting could be adf, mdf, copyglass, gsb, pagedetected, home, whatever we decide
        //But it will be set during capabilities request info and determines blocks of state machine
        property string configCapabilityScannerType : "" //by now adf/mdf...could be COPY_GLASS,PAGE_DETEC,...
        property string selectedStateMachineFlow: ""
        //Also pending investigation by Anuradha about define enum for use in state machine
        readonly property string capabilityMdf: "mdf";
        readonly property string capabilityAdf: "adf";
        readonly property string pageSensorFlow: "pageSensorFlow";
        readonly property string nonPageSensorFlow: "nonPageSensorFlow";
        readonly property string defaultQuicksetName: "Default";
        //By default we select the mixed content quickset
        readonly property string defaultQuicksetId: "61b72f38-1945-11ed-bf29-87d40f139a32";
        property bool isPrePreviewConfigurable: _prePreviewConfigurable
        property int previewConfiguration: 0
        property bool oneTouchWithoutPreview: !isPreviewRequired() && isJobAutoStart
        property bool isLaunchedFromQuickset: false
        
        function isPreviewRequired()
        {
            return previewConfiguration == JobTicket_1_ManualUserOperations_ImagePreviewConfiguration.ImagePreviewConfiguration.enable;
        }

        function isMdfCapabilities()
        {
            return configCapabilityScannerType === capabilityMdf;
        }

        function isAdfCapabilities()
        {
            return configCapabilityScannerType === capabilityAdf;
        }

        function isPageSensorflow()
        {
            return selectedStateMachineFlow === pageSensorFlow
        }

        function isNonPageSensorflow()
        {
            return selectedStateMachineFlow === nonPageSensorFlow
        }

        //this property rules the ui state machine based on current job state
        property int currentJobState: JobManagement_1_State.State._undefined_;

        //States properties that configures the behaviour of LandingView.
        //their values are defined in each state of state machine
        //Valid for all state machines of all products sharing same landing view
        /*THIS QPROPERTIES ARE TEMPORAL SOLUTION FOR STATE MACHINE BASED ON BLOCKS. BUT THEY SHOULD BE CHANGED BY MODEL (OR ANY METHOD) AND  DIRECTLY BINDED TO LANDING CONTROLLER*/
        property bool isEditSettingsActionEnabled: false;
        property string mainActionButtonType: controller.evaluateMainActionButtonState();   //Rules strings and signals
        property bool isMainActionButtonEnabled: false;
        property bool isInitialAction: isPageSensorflow() ? mainActionButtonType == "START" : mainActionButtonType == "COPY"
        property bool isVisiblePrePreviewTextAndImage: isJobAutoStart ? false : true;

        property bool newTicket: false ;
        property string ticketId: "";

        property ISpiceModel copyConfiguration: null;
        property bool isCopyConfigSubscriptionRequired: _isCopyConfigSubscriptionRequired;
        property bool isCopyPermissionsConfigurable: _isCopyPermissionsConfigurable;
        property bool isJobDirect: copyConfiguration != null ? copyConfiguration.data.copyMode == Copy_1_Configuration_CopyMode.CopyMode.printWhileScanning : false
        
        property ISpiceModel scannerStatus: _scannerStatusModel;
        property bool isScanMediaLoaded: false;
        property bool isFlatbedLoaded: false;
        property bool isMultiPagePreviewSupported: _multiPagePreviewSupported
        property int toastTimeout: 5000
        property bool quicksetsSwitchingDisabled: false
        //Transform isScanMediaLoaded to events
        onIsScanMediaLoadedChanged:
        {
            if( isScanMediaLoaded )
            {
                console.log("Media has been loaded");
                if(_stateMachine.isPageSensorflow())
                {
                    _stateMachine.submitEvent("ev.mediaLoaded");
                }
            }
            else
            {
                console.log("Media has been unloaded");
                if(_stateMachine.isPageSensorflow())
                {
                    _stateMachine.submitEvent("ev.mediaUnloaded");
                }
            }
        }

        property bool firstScan: true;

        // InteractiveSummary required properties
        property var summaryList: _copyInteractiveSummaryList
        property var copyResourceInstance: _copySettingsResource
        property ISpiceModel menuResourceModel: null

        // True when the cdm reports the media as ejectable.
        property bool isEjectableByScanStatus: false;
        property bool isEjectActionAllowedByStMachine: false;
        property bool isStopScanButtonEnabled: false;
        property bool isCancelJobButtonVisible: false;

        property bool jobInProgress: false;
        property ISpiceModel defaultTicketModel: null;
        property bool isTicketModelChanged: false
        property bool isTicketIdSubscribeReady:false
        property int customResize: 100
        property ISpiceModel mediaConfiguration: null;

        property QtObject controller : CopyControllerWorkflow{}
        property QtObject scanAppController : null
        property QtObject toastHandle : WalkupApp.ToastHandle{}
        property QtObject cancelJobController: CancelJobController {}
        property bool resizeCustomSelect: false;
        property string resizeSelected: "";
        property string jobState: ""
        property string scannerState: ""

        property bool isOneTouchQuickSet : false;
        property bool quickSetVisibility :false;
        property string newQuickSetName:""
        property bool newQuickSetStartInstantly:false
        property SpiceLocObject quickSetSelected: SpiceLocObject{}
        property string quickSetPermissionIdSelected : ""
        property QQmlObjectListModel quicksetListUnderAppModel: QQmlObjectListModel{}
        property QQmlObjectListModel quicksetListAsRadioButton: QQmlObjectListModel{}
        property QQmlObjectListRolesModel quicksetListModelList: QQmlObjectListRolesModel{}
        property string quicksetId : ""
        property bool quicksetRadioButtonChecked : false
        property bool isJobSubscribed: false;
        property ISpiceModel quickSetsModel: null;
        property ISpiceModel quickSetsModelOfFirstIndex: null;
        property ISpiceModel quickSetsSpecificToApp: null;
        property bool quicksetSelectionUpdate : false
        property bool quicksetsEnabled: true
        property QtObject quicksetController: null

        // To check whether the scanner is idle or not 
        property bool isScannerIdle: false
        property bool isJobInReadyState: false
        property bool inPreviewState: false
        property bool previewReady: true
        property string previewJobId: "";
        property bool isDuplexSupported: false
        property bool isColorPrintSupported: true
        property bool previewComponentControl: false
        property ISpiceModel printStatusModel: null
        property bool isPrinterIdle: true
        property bool areWaitingForPreviews: false
        property bool jobCancelNeeded: true

        // Variable that holds the stamp contents
        property var stampTopLeftContents: []
        property var stampTopCenterContents: []
        property var stampTopRightContents: []
        property var stampBottomLeftContents: []
        property var stampBottomCenterContents: []
        property var stampBottomRightContents: []

        // Variable that stores the display order of Stamp Content
        property var stampTopLeftOrder: []
        property var stampTopCenterOrder: []
        property var stampTopRightOrder: []
        property var stampBottomLeftOrder: []
        property var stampBottomCenterOrder: []
        property var stampBottomRightOrder: []

        // Variable to notify when a Stamp Ticket has been changed.
        property bool stampContentUpdate : false

        url: "qrc:/CopyApp/copyApp.scxml"
        stack: root.applicationWindow.stack

        stateConfiguration: [
            { "name":   "GET_CONFIGURATIONS",                  "url": copyLandingView                                                              }  
        ]

        onTicketModelChanged: {
            console.log("ticketModel: " + _stateMachine.ticketModel);

            if(_stateMachine.ticketModel)
            {
                console.log("ticketModel: " + _stateMachine.ticketModel.data.url);
                if(isPageSensorflow()) 
                {
                    showToastSettingUpdatedBettwenPages()
                    Qt.callLater(function(){_stateMachine.quicksetsSwitchingDisabled = false;})
                }
                if(_stateMachine.ticketModel.constraint) 
                {
                    _stateMachine.constraintModel = _stateMachine.ticketModel.constraint
                }
            }
        }
        onIsScannerIdleChanged: {
            console.log("scanner state changed", _stateMachine.isScannerIdle)
            console.log("scanner state", _stateMachine.scannerState)
        }

        onIsJobInReadyStateChanged: {
            console.log("JobInReady state changed ", _stateMachine.isJobInReadyState)
        }

        onQuicksetSelectionUpdateChanged: {
            if(_stateMachine.quicksetListUnderAppModel)
            {
                for(let i=0 ; i<_stateMachine.quicksetListUnderAppModel.size(); i++){
                    if( _stateMachine.selectedQuicksetId == _stateMachine.quicksetListUnderAppModel.at(i).quickSetId){
                        _stateMachine.quicksetListUnderAppModel.at(i).checked = true;
                        break;
                    }
                }
            }   
        }

        function setupInitialFields()
        {
            if(!_stateMachine.isLaunchedFromQuickset && _stateMachine.isNonPageSensorflow()){
                _stateMachine.previewConfiguration = _stateMachine.ticketModel.data.pipelineOptions.data.manualUserOperations.data.imagePreviewConfiguration
            }
            if(_stateMachine.isLaunchedFromWidget){
                console.log("Launch from widget")
                if(_stateMachine.isDefaultQuicksetShown)
                {
                    _stateMachine.isTicketModelChanged = true
                }
                if(_stateMachine.isLaunchedFromWidgetOptions)
                {
                    console.log("Update the ticket with widget fields")
                    if(_stateMachine.isTicketSubscribed){
                        _stateMachine.updateJobTicketWithWidgetFields()
                    }
                    else{
                        console.log("Ticket not subscribed we'll modify the ticket post subscription")
                        walkupController.onTicketSubscribed.connect(callUpdateJobTicket)
                        function callUpdateJobTicket()
                        {
                            console.log("Updating the ticket with widget fields post subscription")
                            _stateMachine.updateJobTicketWithWidgetFields()
                            walkupController.onTicketSubscribed.disconnect(callUpdateJobTicket)
                        }
                    }
                }
                else{
                    _stateMachine.updateJobTicketWithWidgetFields()
                }
            }
        }

        function switchQuickset(quicksetRef){
            walkupController.switchQuickset(quicksetRef)
        }
        
        function showToastSettingUpdatedBettwenPages()
        {    
            if (!_stateMachine.hasBeenToastShownForLastSettingChangesAfterLastScan)
            {
                _stateMachine.hasBeenToastShownForLastSettingChangesAfterLastScan = true;
                var params= [(_qmlUtils.createSpiceLoc( root ,{"stringId": "StringIds.cNewSettingsScan"})).text]
                ToastSystem.createToast("StringIds.cStringEllipsis", params, SpiceToast.SpiceToastState.INFORMATION, "JobQueueApp", 5000, "qrc:/images/Glyph/Info.json")
                console.log("Toast setting updated bettwen pages shown");
            }
        }
        
        function updateMdfState()
        {
            _stateMachine.isScanMediaLoaded = ( _stateMachine.scannerStatus.data.mdf.data.state == Scan_1_ScanMediaPathStateType.ScanMediaPathStateType.loaded );

            console.log("isScanMediaLoadedChanged: " + _stateMachine.isScanMediaLoaded + " state " + Number(_stateMachine.scannerStatus.data.mdf.data.state));                                                
        }

        function updateMdfEjectableState()
        {
            // Don't use === here.
            _stateMachine.isEjectableByScanStatus = ( _stateMachine.scannerStatus.data.mdf.data.ejectable == Glossary_1_FeatureEnabled.FeatureEnabled.true_ );

            console.log("ejectableChangedOnConnect: mdf.data.ejectable = " + Number(_stateMachine.scannerStatus.data.mdf.data.ejectable));
            console.log("ejectableChangedOnConnect: isEjectableByScanStatus? " + (_stateMachine.isEjectableByScanStatus? "yes" : "no"));
        }

        function getSetDestinationReadyStringId()
        {
            // Jam msg has more priority than paper text
            if (_stateMachine.scannerStatus && _stateMachine.scannerStatus.data.scannerError == Scan_1_ScanErrorType.ScanErrorType.jam)
            {
                return _propertyMap.cStringIDForString("ConstrainedCopyPrimaryButtonMessage", "paperJam");
            }

            return "StringIds.cInsertPageInScanner";
        }

        function getMainActionButtonStringIdForPrePreview()
        {
            if(_stateMachine.isMdfCapabilities()){
                return "StringIds.cStart";
            }
            else{
                return "StringIds.cCopy";
            }
        }
        
        function getDefaultPreviewConfiguration()
        {
           _stateMachine.controller.getDefaultPreviewConfiguration()
        }

        function subscribeStateChanged(){
            console.log("subscribeStateChanged")
            if(typeof _stateMachine != "undefined" && _stateMachine.jobInfoModel)
            {
                console.log("Job Subscription: obtained state " + _stateMachine.jobInfoModel.data.state);
                console.log("Job Subscription: obtained state " + _stateMachine.jobInfoModel.data.jobId);
                processJobState();
            }
            
        }

        function printerStateChanged()
        {
            let printStatus = _stateMachine.printStatusModel.data.printerState;
            console.log("printerStatusResolved: " + printStatus);
            if(printStatus == Print_2_Status_PrinterState.PrinterState.stopped || printStatus == "stopped")
            {
                _stateMachine.isPrinterIdle = false;
            }
            else
            {
                _stateMachine.isPrinterIdle = true;
            }
        }
        
        function readyTostartCopyJob()
        {
            if(_stateMachine.isPageSensorflow() && jobInfoModel.data.state == JobManagement_1_State.State.processing)
            {
                return true;
            }
            else if(_stateMachine.isNonPageSensorflow())
            {
                return _stateMachine.isJobInReadyState;
            }
        }

        function startCopy()
        {
             console.log("Start Copy")
            if(_stateMachine.jobInfoModel && _stateMachine.isPrinterIdle && _stateMachine.readyTostartCopyJob()){
                _stateMachine.isJobInReadyState = false
                console.log("job is in ready state....check scanner")
                checkScannerState()
            }    
            else {
                console.log("Job is not ready")
                if(!!_statusCenter && !!_statusCenter.dashboard)
                {
                    _statusCenter.changeDashboardState("EXPANDED")
                }
                else
                {
                    SpiceToastUtils.launchAppIfPermitted("AlertStatusApp", _applicationEngine)
                }
                _stateMachine.submitEvent("ev.copy.failed")
            }
        }

        function checkScannerState(){
            console.log(_stateMachine.scannerState)
            console.log("Check scanner state it should be Idle")
            if(_stateMachine.scannerState == "Idle" || _stateMachine.scannerState == Scan_1_ScannerStatusType.ScannerStatusType.Idle ){
                startJob()
            }
            else {
                _stateMachine.isJobInReadyState = true
                console.log("Scanner is busy")
                if(_stateMachine.isOneTouchQuickSet){
                    _stateMachine.submitEvent("quitRequested")
                }else{
                    _stateMachine.submitEvent("ev.copy.failed")
                }
            }
        }

        function startJob()
        {
            _stateMachine.previewJobId = ""
            _stateMachine.inPreviewState = false
            _stateMachine.controller.printTicketModel( _stateMachine.ticketModel );
            _stateMachine.controller.updateScannerMediaSource()
            _stateMachine.controller.disconnectEachDataChange()
            _stateMachine.controller.checkAndUpdateInputOutputMediaSize(_stateMachine.ticketModel)
            _stateMachine.isEditSettingsActionEnabled = false
            _stateMachine.cancelJobController.lastJobId = _stateMachine.jobInfoModel.data.jobId
            walkupController.startJob();
            _stateMachine.tmpTicketModel = null;
        }

        function processJobState(){
            if(_stateMachine.jobInfoModel){
                
                _stateMachine.currentJobState = _stateMachine.jobInfoModel.data.state

                if(_stateMachine.jobInfoModel.data.state == JobManagement_1_State.State.ready){
                    _stateMachine.isJobInReadyState = true
                    console.log("submit currentAppJobReady")
                }
                else{
                    _stateMachine.isJobInReadyState = false
                }
                _stateMachine.submitEvent("ev.jobStateChanged");
                console.log("jobInfoModel updated state ",_stateMachine.jobInfoModel.data.state)
            }  
        }

        function requestCopyJobTicket()
        {
            if(root.launchFrom == SpiceApplication.LaunchFromApp.QUICKSETAPP)
            {
                root.href = _stateMachine.quicksetController.getHrefDetailsFromModal(root.selectedShortcutModel)
                console.log("requestCopyJobTicket using href: "+ root.href );
                walkupController.initiate(root.href)
            }
            else if(isPageSensorflow() && quicksetsSupported && root.launchFrom == SpiceApplication.LaunchFromApp.HOME ){//Ticket creation for PageSensorFlow
            console.log("createTicketModel: PageSensorFlow");
            _stateMachine.controller.ticketReferenceForPageSensorFlow(walkupController.initiate)
            }
            else
            {
                walkupController.initiate(root.href)
            }
            console.log("ticket href",root.href)
                 //all the create and subscribe calls are made in walkupController

        }

        function requestAutoJobTicket()
        {
            if(root.launchFrom == SpiceApplication.LaunchFromApp.QUICKSETAPP)
            {
                root.href = _stateMachine.quicksetController.getHrefDetailsFromModal(root.selectedShortcutModel)
                console.log("requestCopyJobTicket using href: "+ root.href );        
            } 
            else
            {    
                root.href = "defaults/copy"
            }  
            walkupController.startOneTouchJobs(root.href,isPreviewRequired())  
        }

        function refreshJob()
        {
            var highestPriorityModeSessionId = _stateMachine.controller.getHighestPriorityModeSessionId();
            walkupController.priorityModeSessionId = highestPriorityModeSessionId;
            if(root.launchFrom == SpiceApplication.LaunchFromApp.WIDGET)
            {
               walkupController.refreshJob("defaults/copy")            
            }
            else
            {
                _stateMachine.controller.ticketReferenceForPageSensorFlow(walkupController.refreshJob)
            }
        }
        
        function completeJob()
        { 
            _stateMachine.jobInfoModel.data.stateChanged.disconnect(subscribeStateChanged);
            walkupController.startJob(true)
        }

        function excuteOneTouchJobAndExit()
        {
            if(inPreviewState)
            {
                completeJob()
            }
            else
            {
                requestAutoJobTicket()
            }
        }
        
        function isAutoStart(autoStart)
        {
            if (autoStart == true) 
            {
                return Glossary_1_FeatureEnabled.FeatureEnabled.true_;
            }
            else 
            {
                return Glossary_1_FeatureEnabled.FeatureEnabled.false_;
            }
        }

        //This funtion only set future.get received, emit event and print ticket
        
        function startPreview()
        {
            console.log("Start Preview")
            _stateMachine.cancelJobController.lastJobId = _stateMachine.jobInfoModel.data.jobId
            if(_stateMachine.isConcurrent){
                _stateMachine.toastHandle.showToast("StringIds.cStringEllipsis", { params: ["StringIds.cStarting"], timeout: _stateMachine.toastTimeout})
            }
            walkupController.startPreview()

        }

        function setTicketAsMultipage()
        {
            _stateMachine.controller.setTicketAsMultipage( _stateMachine.ticketModel );
        }

        function onResetEvent(){
            console.log("On Reset Event statmachine")
            return false
        }
        // This function should be in the controller
        // But it is used in doQuit and the controller can already be deleted.
        function isTicketMultipage()
        {
            let isMultipage = _stateMachine.ticketModel !== null &&
                              _stateMachine.ticketModel.data.src.data.scan.data.scanCaptureMode ==
                              JobTicket_1_ScanCaptureMode.ScanCaptureMode.jobBuild;

            return isMultipage;
        }

        // Tell the state machine if it should wait to get a preview.
        function requiresPreview()
        {
            return true;
        }

        function isConstrained()
        {
            return isPageSensorflow() && !isScanMediaLoaded
        }

        function onCancelPreviewJob()
        {
            _stateMachine.inPreviewState = false;
            _stateMachine.previewComponentControl = false;
            _stateMachine.jobInfoModel.data.stateChanged.disconnect( _stateMachine.processJobState);
            walkupController.initiate("/cdm/jobTicket/v1/tickets/"+_stateMachine.ticketModel.data.ticketId)
        }

        function updateJobTicketWithWidgetFields(){
            console.log("Updating copy job ticket with widget number of copies")
            _stateMachine.ticketModel.data.dest.data.print.data.copies = root.numberOfCopiesFromWidget;
            _stateMachine.controller.updateJobTicket()
        }

        function isJobOutOfScopeOfTheWorkflow()
        {
            // Return true if current job state is completed or cancelling.
            return (_stateMachine.currentJobState == JobManagement_1_State.State.completed || _stateMachine.currentJobState == JobManagement_1_State.State.cancelProcessing);
        }

        function forceUpdateJobTicket()
        {
            console.log("Force job ticket update")
            _stateMachine.controller.updateJobTicket()
        }

    }

    property Component copyLandingView :Component{
        CopyLandingView{
            property int totalImageCount: previewComponentHandler ? previewComponentHandler.totalImage : 0
            isActionButtonConstrained: _stateMachine.isMdfCapabilities() && !_stateMachine.isScanMediaLoaded && _stateMachine.isInitialAction
            detailQuicksetListModel:_stateMachine.quicksetListUnderAppModel
            quicksetsEnabled:_stateMachine.quicksetsEnabled
            isDetailPanelVisible: !_stateMachine.isJobAutoStart
            isPreviewPanelVisible: _scanPreviewSupported

            detailTitleText: {
                                if(_stateMachine.quicksetListUnderAppModel && _stateMachine.quicksetListUnderAppModel.count){
                                    return _qmlUtils.createSpiceLoc( root ,{"stringId":"StringIds.cDefaultsAndQuickSets"})
                                }else{
                                    return null
                                }
            }
            isQuickSetSaveButtonVisible : _stateMachine.isTicketModelChanged && root.isDefaultQuicksetShown

            // Cancel is not allowed when is acquiring and scanner allow to stop current page, only apply to pageSensor flows
            // For rest of scanners, isStopScanButtonEnabled will be false always
            isStopScanButtonEnabled : _stateMachine.isStopScanButtonEnabled            
            isCancelButtonVisible: _stateMachine.cancelJobController.jobInProgress && _stateMachine.isCancelJobButtonVisible && _stateMachine.isNonPageSensorflow()
            isAJobInProgress: _stateMachine.cancelJobController.jobInProgress
            actionButtonConstraintMessageId: _stateMachine.getSetDestinationReadyStringId();
            mainActionButtonStringIdForPrePreview: _stateMachine.getMainActionButtonStringIdForPrePreview()
            //Main button properties
            isMainActionButtonEnabled: _stateMachine.isPageSensorflow() ? _stateMachine.isMainActionButtonEnabled : _stateMachine.isScannerIdle && _stateMachine.isJobInReadyState

            onIsMainActionButtonEnabledChanged: 
            {
                console.log("Copy button : "        + _stateMachine.isMainActionButtonEnabled);
                console.log("ScannerIdle : "        + _stateMachine.isScannerIdle);
                console.log("isJobInReadyState : "  +  _stateMachine.isJobInReadyState);
            }

            mainActionButtonType: _stateMachine.mainActionButtonType

            // Interacitve Summary Properties 
            menuResourceModel: _stateMachine.menuResourceModel
            jobTicketUrl: _stateMachine.jobTicketUrl
            copyResourceInstance: _stateMachine.copyResourceInstance
            summaryList: _stateMachine.summaryList
            previewJobId: _stateMachine.previewJobId;

            isEditSettingsActionEnabled: _stateMachine.isEditSettingsActionEnabled

            isEjectButtonVisible: _stateMachine.isEjectableByScanStatus &&
                                _stateMachine.isEjectActionAllowedByStMachine; 
            isMultiPagePreviewSupported: _stateMachine.isMultiPagePreviewSupported;

            isVisiblePrePreviewTextAndImage: _stateMachine.isVisiblePrePreviewTextAndImage;
            prePreviewMessageForMdf: _stateMachine.controller.getPrepreviewMessageForMdf()
            isImageEditingSupported: _previewEditSupported
            isDiscardPagesSupported: _discardPagesSupported

            previewConfiguration: _stateMachine.previewConfiguration
            inputMediaSourceSelected: _stateMachine.inputMediaSourceSelected
            //Capture signals event from view and transform them to statemachine events
            onCopyButtonClicked:{
                console.log("Copy button clicked");
                if(_stateMachine.isPageSensorflow())
                {
                    _stateMachine.toastHandle.showToast("StringIds.cStringEllipsis", { params: [_propertyMap.cStringIDForString("jobQueue", "progressJobQueue")], timeout: _stateMachine.toastTimeout })
                }
                _stateMachine.submitEvent("ev.copyButtonClicked");
                
            }

            isPageAdded: _stateMachine.isScanMediaLoaded 

            onStartButtonClicked:{
                console.log("Start button clicked");
                _stateMachine.submitEvent("ev.startPreview");
            }

            onDoneButtonClicked:{
                console.log("Done button clicked");
                if(_stateMachine.isPageSensorflow())
                {
                    if(_stateMachine.isLaunchedFromWidget || _stateMachine.isOneTouchQuickSet)
                    {
                        if(_stateMachine.isTicketMultipage())
                        {
                            walkupController.startJob(true)
                        }
                        _stateMachine.inPreviewState = false;
                    }
                    else
                    {
                        _stateMachine.submitEvent("ev.copyButtonClicked");
                    }
                }
                else
                {
                    _stateMachine.submitEvent("ev.copyButtonClicked");
                }
            }

            onMoreSettingsButtonClicked:{
                    applicationStack.pushModal("qrc:/CopyApp/CopySettingsView.qml")
            }

            onPreviewButtonClicked:{
                _stateMachine.submitEvent("ev.startPreview");
            }

            onEjectButtonClicked:{
                _stateMachine.controller.ejectActionExecution(_stateMachine.scannerStatus);
            }

            onRefreshPreviewButtonClicked: {
                _stateMachine.isTicketModelChanged = false
            }

            onCancelButtonClicked: {
                _stateMachine.cancelJobController.cancelButtonClicked()
                _stateMachine.submitEvent("ev.cancelButtonClicked")
            }

            onStopScanButtonClicked:{
                function stopScanFutureResolved(future)
                {
                    console.log("showing resolve dialog")
                    if(_stateMachine.scannerStatus.data.scannerState != Scan_1_ScannerStatusType.ScannerStatusType.Testing || 
                                        _stateMachine.scannerStatus.data.mdf.data.ejectable == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
                    {
                        // Force enable stop scan to false, this will avoid double clicks or delay message about finish of acquisition
                        _stateMachine.isStopScanButtonEnabled = false
                    }
                    else
                    {
                        console.log("Current state of scanner not need to show stop scan dialog, because current state of scanner resolve situation.")
                    }
                }

                if(_stateMachine.controller && _stateMachine.jobInfoModel && _stateMachine.jobInfoModel.data)
                {
                    _stateMachine.controller.stopScanThruJobTicket(_stateMachine.jobInfoModel.data , stopScanFutureResolved );
                }
                else
                {
                    console.warn("Tried to stop a scan, when no job is available")
                }
            }

            onSaveQuicksetButtonClicked:{
                applicationStack.pushModal("qrc:/CopyApp/QuickSetSaveTicketChanged.qml")
            }

            property Item discardDialog: null
            onDiscardPageButtonClicked:
            {
                //Params received from signal discardButtonClicked(int pageNumber, string discardPageIdString )
                console.log("onDiscardButtonClicked pageNumber:" + pageNumber + " discardPageIdString:" + discardPageIdString);

                //Slots
                function sucessDiscardPage() { console.log("sucessDiscardPage page#" + pageNumber + " pageId:" + discardPageIdString); }
                function failDiscardPage()   { console.log("failDiscardPage   page#" + pageNumber + " pageId:" + discardPageIdString); }

                discardDialog = _stack.push("qrc:/ScanApp/DiscardPageDialog.qml",{
                    "pageNumber": pageNumber,
                    "pageId": discardPageIdString,
                    "jobName": "",
                    "jobId": _stateMachine.scanAppController.getLastJobId()
                })

                discardDialog.discardPageConfirmed.connect(function(pageId, jobId)
                {
                    console.log("discardDialog discardPageConfirmed pageId:" + pageId  + " jobId:" + jobId);
                    _stateMachine.scanAppController.discardPageByIds( jobId, pageId, sucessDiscardPage,failDiscardPage );
                });
            }

            onPreviewReady: {
                _stateMachine.submitEvent("ev.previewReady");
            }
        }
    }

    function doStart()
    {
        root.href = "defaults/copy"
        _stateMachine.controller.setWalkupAppCapabilities();
        for (let section = 0; section < _deviceShortcutsJobTypeSupported.count; section++){
            if(_deviceShortcutsJobTypeSupported.get(section) == Shortcut_1_JobType.JobType.copy)
            {
                _stateMachine.quicksetsSupported = true
                let comp = Qt.createComponent("qrc:/CopyApp/CopyQuicksetController.qml")
                if (comp.status == Component.Ready) {
                    _stateMachine.quicksetController = comp.createObject(_stateMachine, {
                        "applicationName": root.applicationName,
                        "href": root.href })
                    _stateMachine.quicksetController.appId = Qt.binding(function(){return (root.appId);});
                }
            }
        }
        _stateMachine.selectedQuicksetId = _stateMachine.defaultQuicksetName
         //TO-DO remove this once Default PreviewConfiguration is forceUpdated on Defaults jupiter. 
        if(_stateMachine.isPageSensorflow())
        {
            _stateMachine.previewConfiguration = JobTicket_1_ManualUserOperations_ImagePreviewConfiguration.ImagePreviewConfiguration.enable
        }
        else
        {
            _stateMachine.previewConfiguration = JobTicket_1_ManualUserOperations_ImagePreviewConfiguration.ImagePreviewConfiguration.optional
        }
        
        if(root.launchFrom == SpiceApplication.LaunchFromApp.QUICKSETAPP)
        {
            _stateMachine.quicksetController.isThisOnTouchFromQuickSetApp(root.selectedShortcutModel.action,Shortcut_1_Action.Action.execute)
            _stateMachine.selectedQuicksetId = root.appId;
            _stateMachine.isLaunchedFromQuickset = true;
            console.log("Selected quickset id", _stateMachine.selectedQuicksetId)
        }
        
        if(root.launchFrom == SpiceApplication.LaunchFromApp.WIDGET)
        {
            console.log("doStart LaunchFromApp.WIDGET ticket href: " + root.href + " autoStartJob:" + root.isAutoStartJobFromWidget);

            _stateMachine.isLaunchedFromWidget = true;
            _stateMachine.isJobAutoStart = root.isAutoStartJobFromWidget;
            _stateMachine.isLaunchedFromWidgetOptions = !root.isAutoStartJobFromWidget;
            _stateMachine.ticketModelIdFromWidget = root.href;
        }
        _stateMachine.start();
        _stateMachine.controller.subscribeToScannerStatus();
        _stateMachine.isMediaLoadedBeforeEntry =  _stateMachine.isScanMediaLoaded
        doStartActionThatCapabilitiesRequiered()
    }

    // This function is used to execute do start functionalities after capabalities
    // We have to make sure that the pageSensorflow has been loaded and this is done after initializing the machine.
    function doStartActionThatCapabilitiesRequiered()
    {
        if( _stateMachine.isPageSensorflow() )
        {
            root.activityTracker = Qt.createQmlObject('import Activity 1.0; ActivityTracker{}',root,"dynamicActivityTracker");
        }
        else if( _stateMachine.isAdfCapabilities() )
        {
            _stateMachine.controller.subscribeToPrinterStatus()
        }

        if (root.launchFrom == SpiceApplication.LaunchFromApp.QUICKSETAPP)
        {
            if( _stateMachine.isOneTouchQuickSet == true )
            {
                _stateMachine.isJobAutoStart = true; // For the state machine.
            }
            if (_stateMachine.isOneTouchQuickSet !== true)
            {
                _stateMachine.quicksetController.initializeQuickSetView("CopyApp")
                _stateMachine.quicksetController.getCopyAppQuicksets()
            }
        }
        else if (root.launchFrom == SpiceApplication.LaunchFromApp.WIDGET)
        {
            console.log("Copy App launched from widget with default quickset id:" + root.appId);

            if(_stateMachine.isNonPageSensorflow())
            {
                _stateMachine.quickSetSelected.stringId = "StringIds.cDefault"
            }
            else //For Page Sensor Flow
            {
                if (!_stateMachine.isJobAutoStart)
                {
                    // Enable quicksets for the app.
                    // Don't select any quickset, start with default ticket settings.    
    
                    _stateMachine.quicksetController.initializeQuickSetView("CopyApp")
                }
            }
            if(_stateMachine.quicksetsSupported)
            {
                _stateMachine.quicksetController.getCopyAppQuicksets()
            }
        }
        else
        {
            if(_stateMachine.isNonPageSensorflow())
            {
                _stateMachine.quickSetSelected.stringId = "StringIds.cDefault"
            }
            else
            {
                console.log("Copy App launch quickset id", _stateMachine.defaultQuicksetId)
                root.appId = _stateMachine.defaultQuicksetId
                if(_stateMachine.quicksetsSupported)
                {
                    _stateMachine.selectedQuicksetId = root.appId
                    _stateMachine.quicksetController.initializeQuickSetView("CopyApp")
                }
            }
            if(_stateMachine.quicksetsSupported)
            {
                _stateMachine.quicksetController.getCopyAppQuicksets()
            }
        }
        _stateMachine.cancelJobController.subscribeJobQueue("copy");
    }

    function doQuit()
    {
        _stateMachine.controller.exitInterruptPriorityModeSession();
        if(_stateMachine.jobInfoModel)
        {
            _stateMachine.jobInfoModel.data.stateChanged.disconnect( _stateMachine.processJobState);
        }    
        walkupController.close(_stateMachine.jobCancelNeeded)    
        if(_stateMachine.isMdfCapabilities())
        {
            console.log("doQuitfor for mdf");

            // Here we are checking if we have a multipage job unfinished when quitting the app.
            // This probably should be on the state machine but this doQuit is processed before the scripts on the state machine.
            // So we are adding this logic here.

            // Order matters. We first disconnect qml signals so the unsubscribe doesn't trigger them.
            // Then we unsubscribe jobInfoModel and finish the multiPage job if needed.
            // This way we won't receive updates of the jobInfoModel when changing its state.
            // Unsubscribe and disconnect from Job if app closed while action: jobStateChange
            if(_stateMachine.constraintModel){
                _resourceStore.unsubscribe(_stateMachine.constraintModel)
            }
            
            if( activityTracker != null )
            {
                activityTracker.unreserveUserActivity();
            }

            //Unsubscribe and disconnect from scannerStatus: State and Eject
            _stateMachine.scannerStatus.data.mdf.ejectableChanged.disconnect(_stateMachine.updateMdfEjectableState);
            _stateMachine.scannerStatus.data.mdf.stateChanged.disconnect(_stateMachine.updateMdfState);
            _stateMachine.scannerStatus.data.scannerStateChanged.disconnect( _stateMachine.controller.updateScannerState )

            //Preventive asignation for garbage collector
            _stateMachine.ticketModel = null;
            _stateMachine.jobInfoModel = null;
            _stateMachine.lastTicketClone = null;
            _stateMachine.scannerStatus= null;
            _stateMachine.constraintModel = null;
            _stateMachine.tmpTicketModel = null;
        }
        else if(_stateMachine.isAdfCapabilities())
        {
            _stateMachine.controller.unsubscribeToPrinterStatus();
            _stateMachine.controller.unsubscribeScannerStatus();
            if(_stateMachine.constraintModel){
                _resourceStore.unsubscribe(_stateMachine.constraintModel)
            }
            console.log("Unsubscribing jobTicket")
        }
        _stateMachine.cancelJobController.unsubscribeJobQueue();
        _stateMachine.controller.disconnectEachDataChange()
        
        if (_stateMachine.quickSetsModel){
            _stateMachine.quickSetsModel.destroy()
            _stateMachine.quickSetsModel = null
        }
        if(_stateMachine.tmpTicketModel){
            _stateMachine.tmpTicketModel.destroy()
        }
        if(_stateMachine.isCopyConfigSubscriptionRequired)
        {
            _stateMachine.controller.unsubscribeToCopyConfiguration();
        }
    }

    Component.onDestruction: {
        if (_stateMachine.quicksetListUnderAppModel)
        {
            console.log("Destructing")
            _stateMachine.quicksetListUnderAppModel.destroy()
            _stateMachine.quicksetListUnderAppModel = null
        }
        if (_stateMachine.quicksetListAsRadioButton)
        {
            console.log("Destructing")
            _stateMachine.quicksetListAsRadioButton.destroy()
            _stateMachine.quicksetListAsRadioButton = null
        }
        if (_stateMachine.quicksetListModelList)
        {
            console.log("Destructing")
            _stateMachine.quicksetListModelList.destroy()
            _stateMachine.quicksetListModelList = null
        }
        if(_stateMachine.quickSetsSpecificToApp)
        {
            console.log("Destructing")
            _stateMachine.quickSetsSpecificToApp.destroy()
            _stateMachine.quickSetsSpecificToApp = null
        }
        //set value to null
        _stateMachine.copyResourceInstance = null
        _stateMachine.summaryList = null

    }

    function onResetEvent(){
        console.log("On Reset Event")
        resetEvent = true
        handleApplicationQuit()
        return _stateMachine.inPreviewState
    }

    function handleApplicationQuit()
    {
        if(_stateMachine.inPreviewState)
        {
            console.log("HandleApplication quit")
            let cancelJobWarningPrompt
            if(resetEvent == true){
                cancelJobWarningPrompt = _stack.pushModal("qrc:/ScanApp/CancelJobWarningPrompt.qml", {"isResetEvent" : true}) 
                resetEvent = false
            }else{
                cancelJobWarningPrompt = _stack.pushModal("qrc:/ScanApp/CancelJobWarningPrompt.qml", {"isResetEvent" : false}) 
            }
            cancelJobWarningPrompt.promptResponse.connect(function(cancelJob){
                                                                if(cancelJob == true){
                                                                    _applicationEngine.quitApplication(root.applicationName)
                                                                }else{
                                                                    _stack.pop()
                                                                }
                                                            })
        }
        else
        {
            _applicationEngine.quitApplication(root.applicationName)
        }
    }

    function quit()
    {
        handleApplicationQuit()
    }
}
