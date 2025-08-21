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

SpiceApplication {

    id: root
    objectName: "IDCardCopyApp"
    _stateMachine: SpiceStateMachine {

        property bool jobInProgress: false;
        property ISpiceModel ticketModel: null;
        property string ticketId: ""
        property ISpiceModel jobInfoModel: null;
        property ISpiceModel mediaConfiguration: null;
        property QtObject idCardCopyControllerfunctions : IDCardCopyController{}
        property string menuDynamicUrl: ""

        Timer {
            id: jobPollingTimeout
            objectName: "copyJobPollingTimeout"
            running: false
            interval: 1000
            repeat: false
            onTriggered: {
                console.log("copyProgressView timeout: re-query the data from " + _stateMachine.jobInfoModel.data.url)
                console.log("requesting job info for " + _stateMachine.jobInfoModel.data.url);
                let jobResponse = _resourceStore.get(_stateMachine.jobInfoModel.data.url);
                jobResponse.resolved.connect(_stateMachine.subscribeJobResolved);
                jobResponse.rejected.connect(_stateMachine.subscribeJobResolvedFailed);
                console.log("request future " + jobResponse);
            }
        }


        url: "qrc:/IDCardCopyApp/idCardCopyApp.scxml"
        stack: root.applicationWindow.stack

        stateConfiguration: [
            { "name": "ID_CARD_COPY_LANDING",               "url": "qrc:/IDCardCopyApp/IDCardCopyLandingView.qml"},
            { "name": "ID_CARD_COPY_OPTIONS",               "url": "qrc:/IDCardCopyApp/IDCardCopyAppMenuView.qml"},
            { "name": "ID_CARD_COPY_STARTING",              "url": "qrc:/IDCardCopyApp/IDCardCopyStartView.qml"}
        ]

        onJobInProgressChanged: function jobInProgressUpdate() {
                if (!_stateMachine.jobInProgress) {
                    console.log("Job finished")
                    //console.log("Job finished, nullifying the job model")
                    //_stateMachine.jobInfoModel.data.stateChanged.disconnect(subscribeStateChanged);
                    _stateMachine.jobInfoModel = null;
                    jobPollingTimeout.stop();
                    
                }
        }

        function startCopy()
        {
            idCardCopyControllerfunctions.printTicketModel( _stateMachine.ticketModel );
            idCardCopyControllerfunctions.updateCdmTicketModel(cloneAndCreateJob, startJobFailed);
        }

        function cloneAndCreateJob(future) {
            console.log("clone and create job ticket")
            idCardCopyControllerfunctions.cloneCopyTicketstate(_stateMachine.ticketModel.data.ticketId)
            idCardCopyControllerfunctions.createJob(_stateMachine.ticketModel.data.ticketId, startProgress, startJobFailed)
        }

        function startProgress(future) {
            ToastSystem.showMessage(ToastSystem.createSpiceLoc({"stringId": "StringIds.cCopyingMessage", "params": [1, _stateMachine.ticketModel.data.dest.data.print.data.copies]}), ToastSystem.ToastState.INFORMATION,60000)
            jobPollingTimeout.running = true;
            jobPollingTimeout.repeat = true;
            _stateMachine.jobInProgress = true;
        }

        function subscribeJobResolved(future)
        {
            console.log("subscribeJobResolved-->")
            _stateMachine.jobInfoModel = future.get();
            queryJobResolved(future)
            console.log("subscribeJobResolved<--")
        }

        function subscribeJobResolvedFailed(future)
        {
            console.log("subscribeJobResolvedFailed-->")
            jobResolvedFailed(future)
            console.log("subscribeJobResolvedFailed<--")
        }

        function queryJobResolved(future) {
            console.log("queryJobResolved: " + future + " status " + future.status);
            console.log("queryJobResolved: obtained " + _stateMachine.jobInfoModel);
            if (_stateMachine.jobInfoModel)
            {
                console.log("queryJobResolved: obtained jobId " + _stateMachine.jobInfoModel.data.jobId);
                console.log("queryJobResolved: obtained state " + _stateMachine.jobInfoModel.data.state);
                
                if (_stateMachine.jobInfoModel.data !== undefined)
                {
                    processJobState();
                }
                else
                {
                    //job not found - exit workflow!
                    console.log("ERROR! jobId not found. Exit the workflow");
                    jobPollingTimeout.running = false;
                    _stateMachine.jobInProgress = false;
                    dismissToast()
                    _stateMachine.submitEvent("ev.idcardcopy.failed")
                }
            }
            else
            {
                console.warn("_stateMachine.jobInfoModel is NULL")
                jobPollingTimeout.running = false;
                _stateMachine.jobInProgress = false;
                dismissToast()
                _stateMachine.submitEvent("ev.idcardcopy.failed")
            }
        }

        function startJobResolved(future) {
            console.log("startJobResolved: " + future + " status " + future.status);
            console.log("startJobResolved: obtained " + _stateMachine.jobInfoModel);
            console.log("startJobResolved: obtained jobId " + _stateMachine.jobInfoModel.data.jobId);
            console.log("startJobResolved: obtained state " + _stateMachine.jobInfoModel.data.state);
            jobPollingTimeout.interval = 1000;
            jobPollingTimeout.running = true;
        }

        function jobResolvedFailed(future) {
            console.log("jobResolvedFailed: " + future);
            let error = future.error;
            console.log("jobResolvedFailed: job create rejected " + error);
            if (error == IResourceStore.OperationResult.ERROR_RESOURCE_NOT_FOUND)
            {
                //job not found - exit workflow!
                console.log("ERROR! jobId not found. Exit the workflow");
                // TODO enable the copy button again
                _stateMachine.jobInProgress = false;
                jobPollingTimeout.running = false;
                dismissToast()
            }
        }

        function processJobState()
        {
                //ToDo, for some reason "===" comparison doesn't work for this type
                if (_stateMachine.jobInfoModel.data.state == JobManagement_1_State.State.ready)
                {
                    console.log("queryJobResolved: State ready, starting...");
                    _stateMachine.jobInfoModel.data.state = JobManagement_1_State.State.startProcessing;
                    let jobStartResponse = _resourceStore.modify(_stateMachine.jobInfoModel);
                    jobStartResponse.resolved.connect(startJobResolved);
                    jobStartResponse.rejected.connect(jobResolvedFailed);
                }
                else if (_stateMachine.jobInfoModel.data.state == JobManagement_1_State.State.created)
                {
                    console.log("queryJobResolved: State created, initializing...");
                    _stateMachine.jobInfoModel.data.state = JobManagement_1_State.State.initializeProcessing;
                    let jobInitializeResponse = _resourceStore.modify(_stateMachine.jobInfoModel);
                    jobInitializeResponse.resolved.connect(queryJobResolved);
                    jobInitializeResponse.rejected.connect(jobResolvedFailed);
                }
                else if (_stateMachine.jobInfoModel.data.state == JobManagement_1_State.State.completed)
                {
                    console.log("Job completed. Progress to the done view");
                    dismissToast()
                    
                    if(_stateMachine.jobInfoModel.data.completionState == JobManagement_1_JobCompletionState.JobCompletionState.success)
                    {
                        ToastSystem.showMessage(ToastSystem.createSpiceLoc({"stringId": "StringIds.cCopyCompleteMessage"}), ToastSystem.ToastState.INFORMATION,1000)
                        console.log("Job completed with success. Progress to the done view");
                    }
                    else if(_stateMachine.jobInfoModel.data.completionState == JobManagement_1_JobCompletionState.JobCompletionState.failed)
                    {
                        console.log("Job completed with failed. Progress to the done view");
                    }
                    else if(_stateMachine.jobInfoModel.data.completionState == JobManagement_1_JobCompletionState.JobCompletionState.cancelled)
                    {
                        console.log("Job completed with canceled. Progress to the done view");
                        ToastSystem.showMessage(ToastSystem.createSpiceLoc({"stringId": "StringIds.cCopyCanceledMessage"}), ToastSystem.ToastState.INFORMATION,1000)
                    }
                    else
                    {
                        console.log("Unknown scan job completion status: "+_stateMachine.jobInfoModel.data.completionState)
                    }
                    _stateMachine.jobInProgress = false;
                    jobPollingTimeout.running = false;
                    jobPollingTimeout.repeat = false;
                    _stateMachine.submitEvent("ev.idcardcopy.done")
                }
                else
                {
                    console.log("queryJobResolved: State unhandled " + _stateMachine.jobInfoModel.data.state);
                    dismissToast()
                    ToastSystem.showMessage(ToastSystem.createSpiceLoc({"stringId": "StringIds.cCopyingMessage", "params": [1, _stateMachine.ticketModel.data.dest.data.print.data.copies]}), ToastSystem.ToastState.INFORMATION,60000)
                }
        }

        function startJobFailed(future) {
            _stateMachine.submitEvent("ev.idcardcopy.failed")
        }

        function dismissToast()
        {
            console.log("Toast dismissed")
            ToastSystem.toastDismissed();
        }

    }

    function doStart() {
        console.log("IDCardCopyApp Start");
        // starting the fsm
        _stateMachine.start();
        _stateMachine.idCardCopyControllerfunctions.getMediaConfiguration();
    }

    function doQuit() {
        if(_stateMachine.jobInProgress){
            _stateMachine.dismissToast()
        }
    }

}
