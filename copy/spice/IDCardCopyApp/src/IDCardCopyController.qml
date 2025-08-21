import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

QtObject {
    id: idCardCopyController
    objectName: "idCardCopyController"

    function getSelfUrl()
    {
        let url = ""
        if(_stateMachine.ticketModel){
              for(let i = 0; i < _stateMachine.ticketModel.data.links.count; ++i){
                   if(_stateMachine.ticketModel.data.links.get(i).rel === "self"){
                        url =  _stateMachine.ticketModel.data.links.get(i).href
                        break
                    }
                }
            }
       return url
    }

    function getTicketModel(){
        return _stateMachine.ticketModel
    }

    function isCopyColorPrintSupported() {
        if (_stateMachine.isColorPrintSupported){
            console.log("function isCopyColorPrintSupported() : supported");
            return true
        }
        else{
            console.log("function isCopyColorPrintSupported() : not supported");
            return false
        }
    }

    function checkJobConcurrency()
    {
        if(_jobConcurrencySupported){
            console.log("Set job concurrency supported true")
            _stateMachine.isConcurrent = true
        }
        else{
            console.log("Set job concurrency is not supported")
            _stateMachine.isConcurrent = false
        }
    }

    function findValidatorForConstraint( propertyPointer )
    {
        console.debug("propertyPointer is " + propertyPointer);

        let validator = null;

        if (_stateMachine.ticketModel.constraint != null){
            for(var i = 0; i < _stateMachine.ticketModel.constraint.data.validators.count; i++)
            {
                if(_stateMachine.ticketModel.constraint.data.validators.at(i).data.propertyPointer == propertyPointer)
                {
                    validator = _stateMachine.ticketModel.constraint.data.validators.at(i);
                    console.debug("Find propertyPointer from validators : " + validator.propertyPointer);
                }
            }
        }

        return validator;

    }

    ///////////////////////////////////////////////////////////////////////////////
    // JobManagement - Create
    ///////////////////////////////////////////////////////////////////////////////

    function requestDefaultCopyTicketByREQUEST_AND_WAIT_state()
    {
        // all creating and subscribe call are handled in walkupapp controller
        _stateMachine.href = "defaults/copy"
        walkupController.initiate(_stateMachine.href)
    }

    function updateTicketValueForIDCardCopy() {
        _stateMachine.ticketModel.data.src.data.scan.data.scanCaptureMode = "idCard"
        _stateMachine.ticketModel.data.src.data.scan.data.plexMode = "simplex"
        _stateMachine.ticketModel.data.dest.data.print.data.plexMode = "simplex"
        _stateMachine.ticketModel.data.src.data.scan.data.mediaSource = "flatbed";
        updateCdmTicketModel()
    }

    function requestTicketFailSlot(future) {
        console.assert("ERROR request default Copy ticket Fail");
        _stateMachine.submitEvent("quitRequested");
    }

    function printTicketModel( ticketModel )
    {

        console.log("====================ticketModel====================");
        if( ticketModel )
        {
            console.log("ticketModel:" + ticketModel);
            console.log("ticketModel.ticketId:" + ticketModel.data.ticketId );
            console.log("ticketModel.ncopies:" + ticketModel.data.dest.data.print.data.copies );
            console.log("ticketModel.settings_color:" + _qmlUtils.getEnumValueAsString(ticketModel.data.src.data.scan.data,"colorMode") + " :" + ticketModel.data.src.data.scan.data.colorMode);
            console.log("ticketModel.settings_input_sides:" + _qmlUtils.getEnumValueAsString(ticketModel.data.src.data.scan.data,"plexMode") + " :" + ticketModel.data.src.data.scan.data.plexMode);
            console.log("ticketModel.settings_size:" + _qmlUtils.getEnumValueAsString(ticketModel.data.src.data.scan.data, "mediaSize") + " :" + ticketModel.data.src.data.scan.data.mediaSize );
            console.log("ticketModel.settings_resolution:" + _qmlUtils.getEnumValueAsString(ticketModel.data.src.data.scan.data,"resolution") + " :" + ticketModel.data.src.data.scan.data.resolution);
            console.log("ticketModel.settings_tray:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data,"mediaSource") + " :" + ticketModel.data.dest.data.print.data.mediaSource);
            console.log("ticketModel.settings_output_sides:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "plexMode") + " :" + ticketModel.data.dest.data.print.data.plexMode);
            console.log("ticketModel.settings_collate:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "collate") + " :" + ticketModel.data.dest.data.print.data.collate);
            console.log("ticketModel.settings_output_media_type:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "mediaType") + " :" + ticketModel.data.dest.data.print.data.mediaType);
            console.log("ticketModel.settings_print_quality:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "printQuality") + " :" + ticketModel.data.dest.data.print.data.printQuality);
            console.log("ticketModel.settings_duplex_binding:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "duplexBinding") + " :" + ticketModel.data.dest.data.print.data.duplexBinding);
        }
        else
        {
            console.log("ticketModel: NULL, NOT DEFINED!" );
        }
        console.log("=================================================");

    }

    function updateCdmTicketModel()
    {
        if(_stateMachine.ticketModel)
        {
            console.log("updating CDM ticketmodel based on _stateMachine.ticketModel:" + _stateMachine.ticketModel +
                        " in resource_: " + _resourceStore);

            let future = _resourceStore.modify(_stateMachine.ticketModel)
            console.log("waiting for Modify result " + future);
            future.resolved.connect((future) => {

                                        if(typeof _stateMachine != "undefined")
                                        {

                                            printTicketModel( _stateMachine.ticketModel );
                                            console.log("ticket Modify Resolved " + future + " status " + future.status);
                                            console.log("setting ticketId in state machine");
                                            _stateMachine.ticketId = _stateMachine.ticketModel.data.ticketId
                                        }
                                        
                                    });
            future.rejected.connect((future) => {
                                        console.log("ticket Modify Failed " + future + " error " + future.error);
                                        if (typeof rejectedFunc !== "undefined")
                                        {
                                            rejectedFunc(future)
                                        }
                                    });

        }
        else
        {
            console.log("ERROR cannot be update because _stateMachine.ticketModel is not defined");
        }
    }

    function printJobInfoModel( jobInfoModel )
    {
        console.log("-----------------jobInfoModel-----------------------------");
        if( jobInfoModel )
        {
            console.log("jobInfoModel: " + jobInfoModel);
            console.log("jobInfoModel.jobId: " + jobInfoModel.data.jobId);
            console.log("jobInfoModel.state: " + jobInfoModel.data.state);
            console.log("jobInfoModel.ticketId: " + jobInfoModel.data.ticketId);
            console.log("jobInfoModel.jobType: " + jobInfoModel.data.jobType);
            console.log("jobInfoModel.userName: " + jobInfoModel.data.userName);
            console.log("jobInfoModel.fullyQualifiedName: " + jobInfoModel.data.fullyQualifiedName);
        }
        else
        {
            console.log("jobInfoModel: NULL, NOT DEFINED!" );
        }
        console.log("------------------------------------------------------------");
    }

    function getMediaConfiguration() {
        let future = _resourceStore.get("/cdm/media/v1/configuration")

        future.resolved.connect((future) => {
                                    console.log("media configuration resolved " + future.get());
                                    _stateMachine.mediaConfiguration = future.get();
                                });

        future.rejected.connect((future) => {
                                    console.log("media configuration rejected ERROR:" + future.error);
                                    console.info("quitting app..")
                                    _stateMachine.submitEvent("quitRequested");
                                });
    }

    function subscribeScannerStatus(){
        let future = _resourceStore.subscribe("/cdm/scan/v1/status")

        future.resolved.connect((future) => {
                                    console.log("scanner status resolved " + future.get());
                                    _stateMachine.scannerStatus = future.get();
                                    _stateMachine.scannerState = _stateMachine.scannerStatus.data.scannerState
                                    if(_stateMachine.scannerState == "Idle" || _stateMachine.scannerState == Scan_1_ScannerStatusType.ScannerStatusType.Idle){
                                        _stateMachine.isScannerIdle = true
                                    }
                                    else {
                                        _stateMachine.isScannerIdle = false
                                    }
                                    console.log("scanner status: version " + _stateMachine.scannerStatus.data.version);
                                    console.log("scanner status state " + _stateMachine.scannerStatus.data.scannerState);
                                    console.log("scanner status error " + _stateMachine.scannerStatus.data.scannerError);
                                    _stateMachine.scannerStatus.data.scannerStateChanged.connect(scannerStateChanged);
                                    if (_stateMachine.scannerStatus.data.flatbed)
                                    {   
                                        console.log("scanner flatbed flavor: " + _stateMachine.scannerStatus.data.flatbed.data.flavor);
                                        console.log("scanner flatbed status: " + _stateMachine.scannerStatus.data.flatbed.data.state);
                                        console.log("scanner flatbed errorType: " + _stateMachine.scannerStatus.data.flatbed.data.errorType);
                                    }
                                    _stateMachine.scannerStatus.data.flatbed.stateChanged.connect(updateScannerStatus);
                                    
                                    if (_stateMachine.scannerStatus.data.adf)
                                    {   
                                        console.log("scanner adf flavor: " + _stateMachine.scannerStatus.data.adf.data.flavor);
                                        console.log("scanner adf status: " + _stateMachine.scannerStatus.data.adf.data.state);
                                        console.log("scanner adf errorType: " + _stateMachine.scannerStatus.data.adf.data.errorType);
                                    }
                                    _stateMachine.scannerStatus.data.adf.stateChanged.connect(updateScannerStatus);
                                    updateScannerMediaSource()
                                });

        future.rejected.connect((future) => {
                                    console.error("scanner status rejected ERROR:" + future.error);
                                    rejectedFunc();
                                });
    }

    function unsubscribeScannerStatus(){
        if(_stateMachine.scannerStatus){
            console.log("scanner status disconnect");       
            _stateMachine.scannerStatus.data.scannerStateChanged.disconnect(scannerStateChanged);
            _stateMachine.scannerStatus.data.flatbed.data.stateChanged.disconnect(updateScannerStatus);
            _stateMachine.scannerStatus.data.adf.data.stateChanged.disconnect(updateScannerStatus); 
            _resourceStore.unsubscribe(_stateMachine.scannerStatus)                   
        }

    }

    function updateScannerStatus(){
        if(_stateMachine.scannerStatus){

            console.log("Scanner state changed")
            console.log(_stateMachine.scannerStatus.data.scannerState)
            _stateMachine.scannerState = _stateMachine.scannerStatus.data.scannerState

            if(_stateMachine.scannerState == "Idle" || _stateMachine.scannerState == Scan_1_ScannerStatusType.ScannerStatusType.Idle){
                updateScannerMediaSource()
                _stateMachine.isScannerIdle = true
            }
            else {
                _stateMachine.isScannerIdle = false
            }
        }
    }

    function updateScannerMediaSource()
    {
        //choose the scanner source according to the scanner status to avoid mismatch
        let adfAvailable = false;
        if (_stateMachine.scannerStatus.data.adf && _stateMachine.scannerStatus.data.adf.data)
        {
            console.log("scanner adf available with state:" + _qmlUtils.getEnumValueAsString(_stateMachine.scannerStatus.data.adf.data,"state") + 
                            " :" + _stateMachine.scannerStatus.data.adf.data.state + " while ScannerAdfLoaded is " + 
                            Scan_1_ScanAdfStateType.ScanAdfStateType.ScannerAdfLoaded + 
                            " (" + _qmlUtils.getValueFromStringifiedEnum("dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType", "ScannerAdfLoaded") + ")" );
            adfAvailable = true;
        }
        if (adfAvailable && _stateMachine.scannerStatus.data.adf.data.state == Scan_1_ScanAdfStateType.ScanAdfStateType.ScannerAdfLoaded){
            _stateMachine.isFlatbedLoaded = false
        }
        else {
            _stateMachine.isFlatbedLoaded = true
        }
    }

    function scannerStateChanged(){
        if(_stateMachine.scannerStatus){
            console.log("Scanner state changed")
            console.log(_stateMachine.scannerStatus.data.scannerState)
            _stateMachine.scannerState = _stateMachine.scannerStatus.data.scannerState
            if(_stateMachine.scannerState == "Idle" || _stateMachine.scannerState == Scan_1_ScannerStatusType.ScannerStatusType.Idle){
                _stateMachine.isScannerIdle = true
            }
            else {
                _stateMachine.isScannerIdle = false
            }
        }
    }

    function clearJobInfo(){
        if(typeof _stateMachine != "undefined" && _stateMachine.jobInfoModel){
            if(_stateMachine.isJobInfoSubscribed){
                console.log("Unsubscribe jobInfo")
                _stateMachine.jobInfoModel.data.stateChanged.disconnect(_stateMachine.processJobState);
            }
        }
    }

    function printerStatusResolved(future)
    {
        if(typeof _stateMachine != "undefined")
        {
            _stateMachine.printStatusModel = future.get();

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
            _stateMachine.printStatusModel.data.printerStateChanged.connect(_stateMachine.printerStateChanged);

        }
        
    }

    function subscribeToPrinterStatus(){
        let future = _resourceStore.subscribe("/cdm/print/v2/status");
        future.resolved.connect(printerStatusResolved);
    }

    function unsubscribeToPrinterStatus(){
        if(typeof _stateMachine != "undefined" && _stateMachine.printStatusModel){
            _stateMachine.printStatusModel.data.printerStateChanged.disconnect(_stateMachine.printerStateChanged);
            _resourceStore.unsubscribe(_stateMachine.printStatusModel);
        }
    }
}
