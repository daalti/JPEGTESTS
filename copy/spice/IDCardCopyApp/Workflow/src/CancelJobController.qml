import QtQuick 2.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0

// This job controller can be use in other WalkUpApp Also
// It can be put in a common place, So that other WalkUpApp can access it too
QtObject {
    id: jobcontroller
    property ISpiceModel jobQueueModel: null;
    property int runningJobQueueCount: 0
    property string jobType: ""
    signal refreshJobTicketAndJobInfoModel();
    //This LastJobId is used to keep the track of the job started from the application
    // we will be checking the lastJobId in jobQueue and if it is available
    // we will set the jobInProgress , which can be BINDED with cancelJob Visibility
    property string lastJobId: ""
    property bool isLastJobIdValid: false
    property bool jobInProgress: false

    signal jobAddedInJobQueue;
    
    function requestFailure(future) { console.warn("Failure: " + future.get()); }

    function subscribeJobQueue(type){
        jobcontroller.jobType = type
        console.log("Job Controller: subscribeJobQueue", jobcontroller.jobType);

        let future = _resourceStore.subscribe("/cdm/jobManagement/v1/queue");
        future.resolved.connect(connectJobQueueDataChanged);
        future.rejected.connect(requestFailure);
    }

    function connectJobQueueDataChanged(future) {
        jobQueueModel = future.get();
        jobQueueModel.data.jobList.countChanged.connect(fillActiveJobsList);
        fillActiveJobsList();
    }

    function fillActiveJobsList(){
        console.log("Active job list changed")
        console.log("Active job list lastjobId", lastJobId)
        console.log("fillActiveJobsList jobInProgress before checking", jobInProgress)
        if(jobQueueModel){
            let jobData;
            let noOfJob = 0;
            let lastJobIdPresent = false;
            for(let i =0; i< jobQueueModel.data.jobList.count; i++){
                jobData = jobQueueModel.data.jobList.get(i)

                if(jobData.jobType == jobcontroller.jobType){
                    noOfJob++;
                }
                console.log(jobData.jobId)
                console.log(jobcontroller.lastJobId)

                if(jobData.jobId == jobcontroller.lastJobId){
                    console.log("fillActiveJobsList jobID is available")
                    lastJobIdPresent = true
                    jobcontroller.jobInProgress = true
                    jobcontroller.jobAddedInJobQueue()
                }
            }
            if(!lastJobIdPresent){
                // the job was in progress and it has been removed, The ticket need to be refreshed
                if(jobcontroller.jobInProgress)
                {
                    //trigger signal job is cancelled from external application refresh the jobticket
                    console.log("refreshJobTicketAndJobInfoModel")
                    refreshJobTicketAndJobInfoModel()
                }
                console.log("fillActiveJobsList LastjobId is not present")
                jobcontroller.jobInProgress = false
            }
            console.log("fillActiveJobsList jobInProgress after checking", jobInProgress)
            jobcontroller.runningJobQueueCount = noOfJob
            console.log("Active noOfJob is", jobcontroller.runningJobQueueCount)
        }
    }

    function unsubscribeJobQueue(){
        console.log("Unsubscribe jobQueue")
        if(jobQueueModel){
            jobQueueModel.data.jobList.countChanged.disconnect(fillActiveJobsList);
        } 
    }


    function cancelButtonClicked(){
        if(jobcontroller.runningJobQueueCount > 1){
            console.log("Show Status App")
            if(!!_statusCenter) 
            {
                _statusCenter.changeDashboardState("EXPANDED")
            }
            else
            {
                _applicationEngine.startApplication("JobQueueApp")
            }

        }
        else{
            jobcontroller.cancelJob()
        }
    }

    function cancelJob(){
        if(jobcontroller.lastJobId != ""){
            console.log("fillActiveJobsList in cancelJob", jobcontroller.lastJobId)
            let jobInfoModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_JOB);
            jobInfoModel.data.url = "/cdm/jobManagement/v1/jobs/" + jobcontroller.lastJobId
            jobInfoModel.data.state = JobManagement_1_State.State.cancelProcessing;

            let future = _resourceStore.modify(jobInfoModel);
            jobcontroller.jobInProgress = false
                future.resolved.connect((future) => {
                                        console.log("fillActiveJobsList job is canceled")
                                        
                                    });
                
                future.rejected.connect((future) => {
                                        console.log("fillActiveJobsList job is not canceled")
                                    });
        }
    }
}