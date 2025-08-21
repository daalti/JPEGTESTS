import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import walkupcontroller 1.0
import walkupApp 1.0 as WalkupApp

SpiceApplication {

    id: root
    objectName: "IDCardCopyApp"
    
    property var walkupController : WalkupControllerMain{
            onTicketSubscribed:{
                console.log("WalkupControllerMain::onTicketCreated Ticket created")

                _stateMachine.idCardCopyControllerfunctions.printTicketModel( _stateMachine.ticketModel );
                _stateMachine.submitEvent("ev.ticket.received");
                _stateMachine.idCardCopyControllerfunctions.updateTicketValueForIDCardCopy()

                _stateMachine.isEditButtonEnabled = true
                _stateMachine.ticketModelForSettings = _stateMachine.ticketModel
                console.log("Printitng the ticketModel after the updating the ticket values for IDCardCopy")
                _stateMachine.idCardCopyControllerfunctions.printTicketModel( _stateMachine.ticketModel );
                _stateMachine.idCardCopyControllerfunctions.printJobInfoModel(_stateMachine.jobInfoModel);

            }

            onJobSubscribed:{
                console.log("WalkupControllerMain::onJobSubscribed Job created and initialized")

                if(_stateMachine.jobInfoModel && _stateMachine.jobInfoModel.data){
                    _stateMachine.isJobInfoSubscribed = true
                    _stateMachine.processJobState();
                    _stateMachine.jobInfoModel.data.stateChanged.connect(_stateMachine.processJobState);
                }
            }

            onJobReady:{
                console.log("WalkupControllerMain::onJobReady Job Ready")
                _stateMachine.isJobInReadyState = true
            }

            onProcessing:{
                console.log("WalkupControllerMain::onProcessing Job Processing")
                if(_stateMachine.isConcurrent){
                    _stateMachine.toastHandle.showToast("StringIds.cStringEllipsis", { params: ["StringIds.cStarting"], timeout: _stateMachine.toastTimeout })
                }
                _stateMachine.jobInProgress = true
                _stateMachine.isJobInfoSubscribed = false
                _stateMachine.jobState = JobManagement_1_State.State._undefined_
                _stateMachine.submitEvent("ev.idcardcopy.done")
            }

            onWalkupfailure:{
                console.log("Error: Unable to perform the job due to ", msg)
                _stateMachine.submitEvent("quitRequested");
            }
    }
    
    _stateMachine: SpiceStateMachine {

        property bool jobInProgress: false;
        property ISpiceModel ticketModel: walkupController.ticketModel;
        property ISpiceModel ticketModelForSettings: null;
        property string ticketId: ""
        property ISpiceModel jobInfoModel: walkupController.jobModel;
        property ISpiceModel scannerStatus: _scannerStatusModel;
        property string scannerState: ""
        property bool isScannerIdle: false
        property int jobState: JobManagement_1_State.State._undefined_
        property QtObject idCardCopyControllerfunctions : IDCardCopyController{}
        property QtObject toastHandle : WalkupApp.ToastHandle{}
        property QtObject jobcontroller: CancelJobController{}
        property var summaryList: _idCopyinteractiveSummaryList
        property string menuDynamicUrl: ""
        property string animationPath: { _qmlUtils.getWorkflowResourceUrl("InstructionIdCardCopy", "animations") }
        property bool isJobInReadyState: false
        property bool isColorPrintSupported: true
        property bool isConcurrent: true
        property ISpiceModel printStatusModel: null
        property bool isPrinterIdle: true
        property bool isEditButtonEnabled: false
        property string href: ""
        property bool cancelJobWhileQuitingApp: true

        property bool isJobInfoSubscribed: false
        url: "qrc:/IDCardCopyApp/IDCardCopyApp.scxml"
        stack: root.applicationWindow.stack

        stateConfiguration: [
            { "name": "ID_CARD_COPY_LANDING",               "url": idCardCopyLandingView},
            { "name": "ID_CARD_COPY_OPTIONS",               "url": "qrc:/IDCardCopyApp/IDCardCopySettings.qml",      "modal": true},
            { "name": "ID_CARD_COPY_STARTING",              "url": "qrc:/IDCardCopyApp/IDCardCopyAppStartingView.qml", "modal": true}
        ]

        onIsScannerIdleChanged: {
            console.log("scanner state changed", _stateMachine.isScannerIdle)
            console.log("scanner state", _stateMachine.scannerState)
        }

        onIsJobInReadyStateChanged: {
            console.log("JobInReady state changed ", _stateMachine.isJobInReadyState)
        }

        function startCopy()
        {
            console.log("Start Copy")
            if((_stateMachine.isJobInReadyState && _stateMachine.isPrinterIdle)){
                console.log("job is in ready state....check scanner")
                _stateMachine.isJobInReadyState = false
                if(_stateMachine.jobInfoModel){
                    _stateMachine.jobcontroller.lastJobId = _stateMachine.jobInfoModel.data.jobId
                }
                _stateMachine.jobInfoModel.data.stateChanged.disconnect(_stateMachine.processJobState);
                walkupController.startJob();
                _stateMachine.idCardCopyControllerfunctions.printTicketModel( _stateMachine.ticketModel );
            }
            else {
                console.log("Job is not ready")
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


        function processJobState(){
            if(_stateMachine.jobInfoModel){
                _stateMachine.jobState = _stateMachine.jobInfoModel.data.state
                if(_stateMachine.jobState == JobManagement_1_State.State.ready){
                    _stateMachine.isJobInReadyState = true
                }
                console.log("jobInfoModel updated state",_stateMachine.jobState)
            }  
        }

        function startJobResolvedFailed() {
            // console.log("startJobResolvedFailed: " + future);
            let error = ""
            console.log("startJobResolvedFailed: job create rejected " + error);
            if (error == IResourceStore.OperationResult.ERROR_RESOURCE_NOT_FOUND)
            {
                console.log("ERROR! jobId not found. Exit the workflow");
                _stateMachine.jobInProgress = false;
            }
        }

        function startJobFailed(future) {
            _stateMachine.submitEvent("ev.idcardcopy.failed")
        }

    }

    Component{
        id: idCardCopyLandingView
        IDCardCopyAppLandingView{
            copyButtonEnabled: _stateMachine.isScannerIdle && _stateMachine.isJobInReadyState
            isCancelButtonVisible: _stateMachine.jobcontroller.jobInProgress && _jobConcurrencySupported
            animationPath: _stateMachine.animationPath
            isEditButtonEnabled: _stateMachine.isEditButtonEnabled
            onCancelButtonClicked: {
                //Call jobController canceljobButton clicked method
                // it will check whethter to open the StatusApp or the cancelJob
                _stateMachine.jobcontroller.cancelButtonClicked()
            }
        }
    }

    function doStart() {
        console.log("IDCardCopyApp Start");
        // starting the fsm
        _stateMachine.start();
        if(_jobConcurrencySupported)
        {
            _stateMachine.jobcontroller.subscribeJobQueue("copy");
        }
        _stateMachine.idCardCopyControllerfunctions.checkJobConcurrency();
        _stateMachine.idCardCopyControllerfunctions.scannerStateChanged();
        _stateMachine.scannerStatus.data.scannerStateChanged.connect(_stateMachine.idCardCopyControllerfunctions.scannerStateChanged);
        _stateMachine.idCardCopyControllerfunctions.subscribeToPrinterStatus()
    }

    function doQuit() {
        console.log("IDCardCopyApp Quit");
        _stateMachine.idCardCopyControllerfunctions.clearJobInfo();
        // WalkupController is responsible for cancelling the job while quitting the app
        walkupController.close(_stateMachine.cancelJobWhileQuitingApp);
        if(_jobConcurrencySupported)
        {
            _stateMachine.jobcontroller.unsubscribeJobQueue();
        }
        _stateMachine.idCardCopyControllerfunctions.unsubscribeToPrinterStatus()
        _stateMachine.scannerStatus.data.scannerStateChanged.disconnect(_stateMachine.idCardCopyControllerfunctions.scannerStateChanged);
    }
}
