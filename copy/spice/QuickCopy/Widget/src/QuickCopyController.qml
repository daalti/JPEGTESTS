import QtQuick 2.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxToastSystem 1.0
import "qrc:/SpicePropertyValueFromModel.js" as SpicePropertyValueFromModel

QtObject {
    id: quickCopyController
    objectName: "quickCopyController"
    property ISpiceModel ticketModel: null;
    property ISpiceModel jobInfoModel: null;
    property int numCopies: 1;
    property string inputMediaSource: "";
    property ISpiceModel scannerStatus: _scannerStatusModel;
    property bool isScanMediaLoaded:false
    property string scannerState: "";
    property bool copyEnabled: false;
    property SpiceLocObject propertyA : null
    property SpiceLocObject propertyB : null
    property SpiceLocObject propertyC : null
    property SpiceLocObject propertyD : null
    property int numberOfCopiesMin: 1
    property int numberOfCopiesMax: 999
    property QQmlObjectListModel widgetProperty: QQmlObjectListModel{}
    property QQmlObjectListModel widgetInfoText:QQmlObjectListModel{}
    property ISpiceModel printStatusModel: null
    property bool isPrinterIdle: true

    property ISpiceModel shortcut: null
    property SpiceLocObject copyConstrainedMessage:SpiceLocObject{
        stringId: "StringIds.cInsertPageInScanner"
    }
    property Component asyncOperationWrapper: AsyncOperationWrapper{}
    function showToastMessage(stringId, timeout = 3000){
        //by default below are the image details, if change needed pls provide iconPath and imgSource
        //iconPath: "qrc:/images/Glyph/ChevronUp.json"
        //imgSource: "qrc:/images/Status/ProgressBarCircleIndeterminateStatic.json"
            let params= [(_qmlUtils.createSpiceLoc( null ,{"stringId": stringId})).text]
        ToastSystem.createToast("StringIds.cStringEllipsis",params,SpiceToast.SpiceToastState.INFORMATION,"JobQueueApp",timeout)
    }


    function startCopy(){
        if ((quickCopyController.scannerState == "Idle" || quickCopyController.scannerState == Scan_1_ScannerStatusType.ScannerStatusType.Idle) && quickCopyController.isPrinterIdle){
            quickCopyController.copyEnabled = false
            quickCopyController.requestCloneCopyJobTicket()
        }
        else {
            console.log("Scanner is busy")
            if(!quickCopyController.isPrinterIdle)
            {
                console.log("Printer is busy")
                _statusCenter.changeDashboardState("EXPANDED")
            }
            else
            {
                //TODO: Copy button should be disabled, disabling it
                quickCopyController.copyEnabled = false
            }
            
        }
    }

    function canBeOpenedCopyApp( isAutoStartJob)
    {
        //autoStart requieres media previously loaded
        if(isAutoStartJob && copyController.inputMediaSource == "mdf" && !root.copyController.isScanMediaLoaded)
        {
            _stack.pushModal("qrc:/components/SpiceConstraintMessage.qml",{"message": quickCopyController.copyConstrainedMessage.text})
            return false;
        }

        return true;
    }

    //It returns true if aplicationStart has been requiredto appEngine, or false if conditions to open app aren't satisfied
    function startApplication(numberOfCopies, isAutoStartJob )
    {

        let canBeCopyAppOpened = canBeOpenedCopyApp( isAutoStartJob );

        if( canBeCopyAppOpened )
        {
            console.log("Copy Widget, Opening Copy app copies:" + numberOfCopies + " autoStartJob:" + isAutoStartJob );
            _applicationEngine.startApplication("CopyApp", {launchFrom:SpiceApplication.LaunchFromApp.WIDGET,
                                                            appId:"cedab422-33b3-4638-b6a1-604e54525215",
                                                            isAutoStartJobFromWidget: isAutoStartJob,
                                                            numberOfCopiesFromWidget:numberOfCopies,
                                                            href:"defaults/copy"});

            return true;
        }
        else
        {
            return false;
        }

    }

    ///////////////////////////////////////////////////////////////////////////////
    // JobManagement - Create
    ///////////////////////////////////////////////////////////////////////////////
    function requestCloneCopyJobTicket()
    {
        console.log(" Creating clone jobTicket");
        //requesting the ticket
        ticketModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET);
        ticketModel.data.ticketReference = "defaults/copy";

        let future = asyncOperationWrapper.createObject(quickCopyController, {"asyncOperation":()=> _resourceStore.create("/cdm/jobTicket/v1/tickets", ticketModel)})
        future.resolved.connect(requestTicketSuccess)
        future.rejected.connect(requestTicketFailSlot);
    }

    function checkInputOutputMediaSize(ticketModel){
        if (ticketModel.data.dest.data.print.data.mediaSize == Glossary_1_MediaSize.MediaSize.any)
        {
            if (ticketModel.data.src.data.scan.data.mediaSize != Glossary_1_MediaSize.MediaSize.any)
            {
                ticketModel.data.dest.data.print.data.mediaSize = ticketModel.data.src.data.scan.data.mediaSize;
            }
        }
    }
    /*
        Slot used by REQUEST_AND_WAIT_FOR_TICKET state when requesting ticket model usign requestDefaultCopyTicketWithSlots
        has been successfully done. It sets ticketModel received to stateMachine.ticketModel and emits ticket.received event
        for state transition
    */
    function requestTicketSuccess(future) {
        console.log(" Ticket Request Success");
        ticketModel = future.get();
        checkInputOutputMediaSize(ticketModel)
        updateJobTicket(ticketModel)
    }

    function requestTicketFailSlot(future) {
        console.assert(" ERROR request default Copy ticket Fail");
        copyEnabled = true;
    }

    function updateJobTicket(ticketModel){
        if(ticketModel){
            console.log(" ENTRY")
            ticketModel.data.dest.data.print.data.copies = numCopies
            ticketModel.data.src.data.scan.data.mediaSource = inputMediaSource

            let future = asyncOperationWrapper.createObject(quickCopyController, {"asyncOperation":()=> _resourceStore.modify(ticketModel)})
            future.resolved.connect((future)=> {
                console.log(" ticket Modify Resolved " + future + " status " + future.status);
                createDefaultJob(ticketModel.data.ticketId)
            });
            future.rejected.connect((future) => {
                console.log(" ticket Modify Failed " + future + " error " + future.error);
                copyEnabled = true;
            });
        }
        else {
            console.log("Error: copy ticket was null");
            copyEnabled = true;
        }
    }

    function createDefaultJob(ticketId) {
        console.log("createJob: ENTER id:" + ticketId );
        jobInfoModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_JOB);
        console.log("createJob: jobInfoModel = ", jobInfoModel);
        jobInfoModel.data.ticketId = ticketId;
        jobInfoModel.data.autoStart = Glossary_1_FeatureEnabled.FeatureEnabled.true_;
        console.log("autoStart set true");

        let future = asyncOperationWrapper.createObject(quickCopyController, {"asyncOperation":()=> _resourceStore.create("/cdm/jobManagement/v1/jobs", jobInfoModel)})

        future.resolved.connect((future) => {
            if(_jobConcurrencySupported){    
                quickCopyController.showToastMessage("StringIds.cStarting")
            }
            printJobInfoModel(jobInfoModel)
            printTicketModel(ticketModel)
            jobInfoModel.destroy()
            ticketModel.destroy()
            quickCopyController.jobInfoModel = null
            quickCopyController.ticketModel = null
        })
        future.rejected.connect((future) => {
            console.log("createJob: failedFunc not exist!")
            copyEnabled = true;
            jobInfoModel = null;
        })
    }

    function subscribeScannerStatus(){
        if(scannerStatus)
        {
            scannerState = scannerStatus.data.scannerState
            if (quickCopyController.scannerState == "Idle" || quickCopyController.scannerState == Scan_1_ScannerStatusType.ScannerStatusType.Idle){
                quickCopyController.copyEnabled = true
            }
            else {
                quickCopyController.copyEnabled = false
            }
            console.log("scanner status: version " + scannerStatus.data.version);
            console.log("scanner status state " + scannerStatus.data.scannerState);
            console.log("scanner status error " + scannerStatus.data.scannerError);
            scannerStatus.data.scannerStateChanged.connect(updateScannerStatus);

            if (scannerStatus.data.mdf)
            {   
                console.log("scanner mdf flavor: " + scannerStatus.data.mdf.data.flavor);
                console.log("scanner mdf status: " + scannerStatus.data.mdf.data.state);
                console.log("scanner mdf errorType: " + scannerStatus.data.mdf.data.errorType);
                updateMdfState()
                scannerStatus.data.mdf.stateChanged.connect(updateMdfState)
            }

            if (scannerStatus.data.flatbed)
            {   
                console.log("scanner flatbed flavor: " + scannerStatus.data.flatbed.data.flavor);
                console.log("scanner flatbed status: " + scannerStatus.data.flatbed.data.state);
                console.log("scanner flatbed errorType: " + scannerStatus.data.flatbed.data.errorType);
                scannerStatus.data.flatbed.stateChanged.connect(updateScannerMediaSource);
            }
            
            if (scannerStatus.data.adf)
            {   
                console.log("scanner adf flavor: " + scannerStatus.data.adf.data.flavor);
                console.log("scanner adf status: " + scannerStatus.data.adf.data.state);
                console.log("scanner adf errorType: " + scannerStatus.data.adf.data.errorType);
                scannerStatus.data.adf.stateChanged.connect(updateScannerMediaSource);
            }
            updateScannerMediaSource()
        }
        else{
            console.error("scanner status was not found" )
        }
    }
     function updateMdfState()
    {
        isScanMediaLoaded = (scannerStatus.data.mdf.data.state == Scan_1_ScanMediaPathStateType.ScanMediaPathStateType.loaded );

        console.log("isScanMediaLoadedChanged: " + isScanMediaLoaded + " state " + Number(scannerStatus.data.mdf.data.state));                                                
    }
    function unsubscribeScannerStatus(){
        if(scannerStatus){
            console.log("scanner status disconnect");       
            scannerStatus.data.scannerStateChanged.disconnect(updateScannerStatus);

            if(scannerStatus.data.mdf){   
                scannerStatus.data.mdf.stateChanged.disconnect(updateMdfState)
            }
            if(scannerStatus.data.flatbed){
                scannerStatus.data.flatbed.data.stateChanged.disconnect(updateScannerMediaSource);
            }
            if(scannerStatus.data.adf){
                scannerStatus.data.adf.data.stateChanged.disconnect(updateScannerMediaSource);
            } 
        }
    }

    function updateScannerStatus(){
        if(scannerStatus){

            console.log("Scanner state changed")
            console.log(scannerStatus.data.scannerState)
            scannerState = scannerStatus.data.scannerState
            if (quickCopyController.scannerState == "Idle" || quickCopyController.scannerState == Scan_1_ScannerStatusType.ScannerStatusType.Idle){
                quickCopyController.copyEnabled = true
                console.log("Scanner Idle, enabling copy")
            }
            else {
                quickCopyController.copyEnabled = false
            }
        }
    }

    function updateScannerMediaSource()
    {
        //choose the scanner source according to the scanner status to avoid mismatch
        console.log("Updating Scanner Media Source");
        let adfAvailable = false;
        let flatbedAvailable = false;
        let mdfAvailable = false;
        inputMediaSource = Scan_1_ScanAdfStateType.ScanAdfStateType._undefined_;
        if (scannerStatus.data.adf && scannerStatus.data.adf.data)
        {
            console.log("scanner adf available with state:" + _qmlUtils.getEnumValueAsString(scannerStatus.data.adf.data,"state") + 
                            " :" + scannerStatus.data.adf.data.state + " while ScannerAdfLoaded is " + 
                            Scan_1_ScanAdfStateType.ScanAdfStateType.ScannerAdfLoaded + 
                            " (" + _qmlUtils.getValueFromStringifiedEnum("dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType", "ScannerAdfLoaded") + ")" );
            adfAvailable = true;
        }
        if (scannerStatus.data.flatbed && scannerStatus.data.flatbed.data)
        {
            console.log("scanner flatbed available with state:" + _qmlUtils.getEnumValueAsString(scannerStatus.data.flatbed.data,"state") + 
                " :" + scannerStatus.data.flatbed.data.state);
            flatbedAvailable = true;
        }
        if (scannerStatus.data.mdf && scannerStatus.data.mdf.data) 
        {
            console.log("scanner mdf available with state:" + _qmlUtils.getEnumValueAsString(scannerStatus.data.mdf.data,"state") + 
                            " :" + scannerStatus.data.mdf.data.state);
            mdfAvailable = true;
        }


        if (adfAvailable && scannerStatus.data.adf.data.state == Scan_1_ScanAdfStateType.ScanAdfStateType.ScannerAdfLoaded
            //these types should be equivalent
            //scannerStatus.data.adf.data.state == _qmlUtils.getValueFromStringifiedEnum("dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType", "ScannerAdfLoaded")
        )
        {
            inputMediaSource = "adf";
        }
        else if (flatbedAvailable)
        {
            inputMediaSource = "flatbed";
        }
        else if (mdfAvailable)
        {
            inputMediaSource = "mdf";
        }
        

        console.log("scanner source selected:" + inputMediaSource);
    }

    function printTicketModel(ticket)
    {
        console.log("====================ticketModel====================");
        if(ticket)
        {
            console.log("ticketModel:" + ticket);
            console.log("ticketModel.ticketId:" + ticket.data.ticketId );
            console.log("ticketModel.ncopies:" + ticket.data.dest.data.print.data.copies );
            console.log("ticketModel.settings_color:" + _qmlUtils.getEnumValueAsString(ticket.data.src.data.scan.data,"colorMode") + " :" + ticketModel.data.src.data.scan.data.colorMode);
            console.log("ticketModel.settings_input_sides:" + _qmlUtils.getEnumValueAsString(ticket.data.src.data.scan.data,"plexMode") + " :" + ticketModel.data.src.data.scan.data.plexMode);
            console.log("ticketModel.settings_size:" + _qmlUtils.getEnumValueAsString(ticket.data.src.data.scan.data, "mediaSize") + " :" + ticketModel.data.src.data.scan.data.mediaSize );
            console.log("ticketModel.settings_resolution:" + _qmlUtils.getEnumValueAsString(ticket.data.src.data.scan.data,"resolution") + " :" + ticketModel.data.src.data.scan.data.resolution);
            console.log("ticketModel.settings_scanner_source:" + _qmlUtils.getEnumValueAsString(ticket.data.src.data.scan.data, "mediaSource") + " :" + ticketModel.data.src.data.scan.data.mediaSource);
            console.log("ticketModel.settings_tray:" + _qmlUtils.getEnumValueAsString(ticket.data.dest.data.print.data,"mediaSource") + " :" + ticketModel.data.dest.data.print.data.mediaSource);
            console.log("ticketModel.settings_output_sides:" + _qmlUtils.getEnumValueAsString(ticket.data.dest.data.print.data, "plexMode") + " :" + ticketModel.data.dest.data.print.data.plexMode);
            console.log("ticketModel.settings_collate:" + _qmlUtils.getEnumValueAsString(ticket.data.dest.data.print.data, "collate") + " :" + ticketModel.data.dest.data.print.data.collate);
            console.log("ticketModel.settings_output_media_type:" + _qmlUtils.getEnumValueAsString(ticket.data.dest.data.print.data, "mediaType") + " :" + ticketModel.data.dest.data.print.data.mediaType);
            console.log("ticketModel.settings_print_quality:" + _qmlUtils.getEnumValueAsString(ticket.data.dest.data.print.data, "printQuality") + " :" + ticketModel.data.dest.data.print.data.printQuality);
            console.log("ticketModel.settings_duplex_binding:" + _qmlUtils.getEnumValueAsString(ticket.data.dest.data.print.data, "duplexBinding") + " :" + ticketModel.data.dest.data.print.data.duplexBinding);
            console.log("ticketModel.settings_pagesPersheet:" + _qmlUtils.getEnumValueAsString(ticket.data.pipelineOptions.data.imageModifications.data, "pagesPerSheet") + " :" + ticketModel.data.pipelineOptions.data.imageModifications.data);
        }
        else
        {
            console.log("ticketModel: NULL, NOT DEFINED!" );
        }
        console.log("=================================================");
    }

    function printJobInfoModel(jobInfo)
    {
        console.log("-----------------jobInfoModel-----------------------------");
        if(jobInfoModel)
        {
            console.log("jobInfoModel: " + jobInfo);
            console.log("jobInfoModel.jobId: " + jobInfo.data.jobId);
            console.log("jobInfoModel.state: " + jobInfo.data.state);
            console.log("jobInfoModel.ticketId: " + jobInfo.data.ticketId);
            console.log("jobInfoModel.jobType: " + jobInfo.data.jobType);
            console.log("jobInfoModel.userName: " + jobInfo.data.userName);
            console.log("jobInfoModel.fullyQualifiedName: " + jobInfo.data.fullyQualifiedName);
        }
        else
        {
            console.log("jobInfoModel: NULL, NOT DEFINED!" );
        }
        console.log("------------------------------------------------------------");
    }

    function getConstraintModel(){
        let future = asyncOperationWrapper.createObject(quickCopyController, {"asyncOperation":()=> _resourceStore.get("/cdm/jobTicket/v1/configuration/defaults/copy/constraints")})
        future.resolved.connect((future) => {
            console.log("Default constraints Request Success");
            setNumberOfCopies(future.get());
        })
        future.rejected.connect((future) => {
            console.log("ERROR request copy default constraints Fail error = ",future.error);
        });

    }

    function setNumberOfCopies(constraint){
        let validator = null;

        for(let i = 0; i < constraint.data.validators.count; i++)
        {
            if(constraint.data.validators.at(i).data.propertyPointer == "dest/print/copies")
            {
                validator = constraint.data.validators.at(i);
                console.debug("Find propertyPointer from validators : " + validator.propertyPointer);
            }
        }

        if(validator){
            console.log("Set number of Copies")
            numberOfCopiesMin = validator.min.value
            numberOfCopiesMax = validator.max.value
        }

    }

    // Set Non-interactive summary Property of Copy Quick Widget
    // Reading Node from csf file and finding valueResource and enumtype from _templatesData
    function setPropertiesOfWidget(ticketModel, widgetSummary){

        let valueResource_;
        let enumType;
        let modelPath;

        for(let i =0; i< widgetSummary.length; i++){
            let dataObj = _templatesData.valueMapFromList("menuSelections", widgetSummary[i]) ?
                             _templatesData.valueMapFromList("menuSelections", widgetSummary[i]) : _templatesData.valueMapFromList("menuComboBox", widgetSummary[i]) ?
                             _templatesData.valueMapFromList("menuComboBox", widgetSummary[i]) :_templatesData.valueMapFromList("menuTextImageBranches", widgetSummary[i])

            if (dataObj){

                //fetch data from  dataObj
                const dict = dataObj.asMap()
                if (dict!=null && dict.hasOwnProperty("valueResource")) {
                    valueResource_  = dict["valueResource"]
                }
                if(dict!=null && dict.hasOwnProperty("enumType")){
                    enumType = dict["enumType"]
                }
                if(dict!=null && dict.hasOwnProperty("type")){
                    enumType = dict["type"]
                }
                if(dict!=null && dict.hasOwnProperty("titleId")){
                    widgetInfoText.append(_qmlUtils.createSpiceLoc( quickCopyController ,{"stringId": dict["titleId"]}))
                }
                else if(dict!=null && dict.hasOwnProperty("infoText")){
                    widgetInfoText.append(_qmlUtils.createSpiceLoc( quickCopyController ,{"stringId": dict["infoText"]}))
                }
                // get stringId from ticketModel and ValueResource
                let obj = _qmlUtils.parseMenuResourceEntry(valueResource_)
                let propArray = obj[1]
                let field = propArray.pop()
                modelPath = propArray
                let model_ = SpicePropertyValueFromModel.findPropertyValueFromModelForPropertyArray(ticketModel, modelPath)
                let value= model_[field]
                console.log(_propertyMap.cStringIDForEnum(enumType, value))
                widgetProperty.append(_qmlUtils.createSpiceLoc( quickCopyController ,{"stringId": (_propertyMap.cStringIDForEnum(enumType, value))}))
            }
        }
        console.log("Size of widget summary", widgetProperty.size())

        getConstraintModel()
    }

    function printerStatusResolved(future)
    {
        quickCopyController.printStatusModel = future.get();

        let printStatus = quickCopyController.printStatusModel.data.printerState;
        console.log("printerStatusResolved: " + printStatus);
        if(printStatus == Print_2_Status_PrinterState.PrinterState.stopped || printStatus == "stopped")
        {
            quickCopyController.isPrinterIdle = false;
        }
        else
        {
            quickCopyController.isPrinterIdle = true;
        }
        quickCopyController.printStatusModel.data.printerStateChanged.connect(quickCopyController.printerStateChanged);
    }

    function unsubscribeToPrinterStatus(){
        if(quickCopyController.printStatusModel){
            console.log("printer status disconnect");       
            quickCopyController.printStatusModel.data.printerStateChanged.disconnect(quickCopyController.printerStateChanged);
            _resourceStore.unsubscribe(quickCopyController.printStatusModel)
        }
    }
    function subscribeToPrinterStatus(){
        let future = asyncOperationWrapper.createObject(quickCopyController, {"asyncOperation":()=> _resourceStore.subscribe("/cdm/print/v2/status")})
        future.resolved.connect((printerStatusResolved))
        future.rejected.connect((future) => {
            console.log("Failed to subscribe to printer status", future.error);
        });
    }

    function printerStateChanged()
    {
        let printStatus = quickCopyController.printStatusModel.data.printerState;
        console.log("printerStatusResolved: " + printStatus);
        if(printStatus == Print_2_Status_PrinterState.PrinterState.stopped || printStatus == "stopped")
        {
            quickCopyController.isPrinterIdle = false;
        }
        else
        {
            quickCopyController.isPrinterIdle = true;
        }
    }
}
