import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

SystemProgress {
    id: copyingProgressView
    objectName: "CopyingProgress"

    title: SpiceLocObject {stringId: "StringIds.cCopying"}

    onClicked: {
        console.log("queryJobResolved: State created, starting...");
        _stateMachine.jobInfoModel.data.state = JobManagement_1_State.State.cancelProcessing;
        let jobResponse = _resourceStore.modify(_stateMachine.jobInfoModel);
        jobResponse.resolved.connect(cancelJobResolved);
        jobResponse.rejected.connect(cancelJobResolvedFailed);
        _stateMachine.continuousCopy = false ;
        jobPollingTimeout.stop();
    }


    StackView.onActivating: {
        console.log("Activating the COPY_PROGRESS view, _stateMachine.jobInfoModel updated")
    }

    Timer{
        id: jobPollingTimeout
        objectName: "copyJobPollingTimeout"
        running: false
        interval: 1000
        repeat: true
        onTriggered: {
            console.log("copyProgressView timeout: re-query the data")
            let jobResponse = _resourceStore.get(_stateMachine.jobInfoModel.data.url);
            jobResponse.resolved.connect(getJobResolved);
            jobResponse.rejected.connect(getJobResolvedFailed);
            console.log("requesting job info for " + _stateMachine.jobInfoModel.data.url + " future " + jobResponse);
        }
    }

    Component.onCompleted: {
        console.log("CopyProgressView onCompleted")

        //jobPollingTimeout.running = true;

        //query job status. 
        //Need to keep get till jobs/{jobId} support dynamic url subscription
        let jobInfoResponse = _resourceStore.subscribe(_stateMachine.jobInfoModel.data.url);
        jobInfoResponse.resolved.connect(subscribeJobResolved);
        jobInfoResponse.rejected.connect(subscribeJobResolvedFailed);
        console.log("subscribed to job info for " + _stateMachine.jobInfoModel.data.url + " future " + jobInfoResponse);

    }

    function getJobResolved(future)
    {
        console.log("getJobResolved-->")
        _stateMachine.jobInfoModel = future.get();
        queryJobResolved(future)
        console.log("getJobResolved<--")
    }

    function getJobResolvedFailed(future)
    {
        console.log("getJobResolvedFailed-->")
        queryJobResolvedFailed(future)
        console.log("getJobResolvedFailed<--")
    }

    function subscribeJobResolved(future)
    {
        console.log("subscribeJobResolved-->")
        _stateMachine.jobInfoModel = future.get();
        _stateMachine.jobInfoModel.data.state.connect(function(){
            console.log("Job Subscription: obtained state " + _stateMachine.jobInfoModel.data.state);
            processJobState();
            });
        queryJobResolved(future)
        console.log("subscribeJobResolved<--")
    }

    function subscribeJobResolvedFailed(future)
    {
        console.log("subscribeJobResolvedFailed-->")
        queryJobResolvedFailed(future)
        console.log("subscribeJobResolvedFailed<--")
    }

    function queryJobResolved(future) {
        console.log("queryJobResolved: " + future + " status " + future.status);
        console.log("queryJobResolved: obtained " + _stateMachine.jobInfoModel);
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
            jobPollingTimeout.stop();
            _stateMachine.submitEvent("ev.cancel.clicked");
            _stateMachine.newTicket = true ;
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
                jobStartResponse.rejected.connect(startJobResolvedFailed);
            }
            else if (_stateMachine.jobInfoModel.data.state == JobManagement_1_State.State.created)
            {
                console.log("queryJobResolved: State created, initializing...");
                _stateMachine.jobInfoModel.data.state = JobManagement_1_State.State.initializeProcessing;
                let jobInitializeResponse = _resourceStore.modify(_stateMachine.jobInfoModel);
                jobInitializeResponse.resolved.connect(queryJobResolved);
                jobInitializeResponse.rejected.connect(queryJobResolvedFailed);
            }
            else if (_stateMachine.jobInfoModel.data.state == JobManagement_1_State.State.completed)
            {
                console.log("Job completed. Progress to the done view");
                jobPollingTimeout.stop();
                _stateMachine.submitEvent("ev.copy.done")
            }
            else
            {
                console.log("queryJobResolved: State unhandled");
            }
    }

    function startJobResolved(future) {
        console.log("startJobResolved: " + future + " status " + future.status);
        console.log("startJobResolved: obtained " + _stateMachine.jobInfoModel);
        console.log("startJobResolved: obtained jobId " + _stateMachine.jobInfoModel.data.jobId);
        console.log("startJobResolved: obtained state " + _stateMachine.jobInfoModel.data.state);

        //ToDo wait for the job to finish or keep polling?
    }

    function cancelJobResolved(future) {
        console.log("cancelJobResolved: " + future + " status " + future.status);
        console.log("cancelJobResolved: obtained " + _stateMachine.jobInfoModel);
        console.log("cancelJobResolved: obtained jobId " + _stateMachine.jobInfoModel.data.jobId);
        console.log("cancelJobResolved: obtained state " + _stateMachine.jobInfoModel.data.state);

        console.log("returning to the main copy page")
        //return to the job submission screen
        _stateMachine.submitEvent("ev.cancel.clicked");
        _stateMachine.newTicket = true ;
    }

    function cancelJobResolvedFailed(future) {
        console.log("cancelJobResolvedFailed: " + future);
        let error = future.error;
        console.log("cancelJobResolvedFailed: job create rejected " + error);
        if (error == IResourceStore.OperationResult.ERROR_RESOURCE_NOT_FOUND)
        {
            //job not found - exit workflow!
            console.log("ERROR! jobId not found. Exit the workflow");
            _stateMachine.submitEvent("ev.cancel.clicked");
            _stateMachine.newTicket = true ;
        }
    }


    function startJobResolvedFailed(future) {
        console.log("startJobResolvedFailed: " + future);
        let error = future.error;
        console.log("startJobResolvedFailed: job create rejected " + error);
        if (error == IResourceStore.OperationResult.ERROR_RESOURCE_NOT_FOUND)
        {
            //job not found - exit workflow!
            console.log("ERROR! jobId not found. Exit the workflow");
            jobPollingTimeout.stop();
            _stateMachine.submitEvent("ev.cancel.clicked");
            _stateMachine.newTicket = true ;
        }
    }

    function queryJobResolvedFailed(future) {
        console.log("queryJobResolvedFailed: " + future);
        let error = future.error;
        console.log("queryJobResolvedFailed: job query rejected " + error);
        if (error == IResourceStore.OperationResult.ERROR_RESOURCE_NOT_FOUND)
        {
            //job not found - exit workflow!
            console.log("ERROR! jobId not found. Exit the workflow");
            jobPollingTimeout.stop();
            _stateMachine.submitEvent("ev.cancel.clicked")
            _stateMachine.newTicket = true ;
        }
    }

}
