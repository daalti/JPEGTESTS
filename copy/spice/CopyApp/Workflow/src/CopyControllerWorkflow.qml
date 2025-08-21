import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import "qrc:/ResourceStoreConnectionBinding.js" as ResourceStoreBinding


QtObject {
    id: copyController
    objectName: "copyController"

    function getSelfUrl()
    {
        let url = ""
        console.log("getSelfUrl")
        if(_stateMachine.ticketModel)
        {
            for(let i = 0; i < _stateMachine.ticketModel.data.links.count; ++i)
            {
                if(_stateMachine.ticketModel.data.links.get(i).rel === "self")
                {
                    url =  _stateMachine.ticketModel.data.links.get(i).href
                    break
                }
            }
        }
        console.log("getSelfUrl:"+url)
        return url
    }

    function getTicketModel(){
        return _stateMachine.ticketModel
    }

    function checkAndUpdateInputOutputMediaSize(ticketModel){
        if (ticketModel.data.dest.data.print.data.mediaSize == Glossary_1_MediaSize.MediaSize.any)
        {
            if (ticketModel.data.src.data.scan.data.mediaSize != Glossary_1_MediaSize.MediaSize.any)
            {
                ticketModel.data.dest.data.print.data.mediaSize = ticketModel.data.src.data.scan.data.mediaSize;
                _resourceStore.modify(ticketModel)
            }
        }
    }

    function connectEachDataChange()
    {
        if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
            _stateMachine.jobTicketUrl = _stateMachine.ticketModel.data.url
        }
        if(_stateMachine.isPageSensorflow()) { connectUISettingDataChange() }
        else{ connectEachDataChangeNonPageSensor() }
    }

    function disconnectEachDataChange()
    {
        if(_stateMachine.isPageSensorflow()) { disconnectUISettingDataChange() }
        else { disconnectEachDataChangeNonPageSensor() }
    }

    function connectEachDataChangeNonPageSensor(){
        if(_stateMachine.ticketModel){
            console.info("[CopyController] connectEachDataChangeNonPageSensor")

            // Scan options
            _stateMachine.ticketModel.data.src.data.scan.data.contentTypeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.mediaTypeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.mediaSizeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.colorModeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.plexModeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.pagesFlipUpEnabledChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.edgeToEdgeScanChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.autoDeskewChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.scanCaptureModeChanged.connect(ticketChangeHandler)

            // Pipeline options
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.exposureChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.backgroundColorRemovalChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.backgroundNoiseRemovalChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.pagesPerSheetChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.numberUpPresentationDirectionChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.imageBorderChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.autoPaperColorRemovalChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.autoPaperColorRemovalLevelChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.autoToneChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.autoToneLevelChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.blankPageSuppressionEnabledChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.promptForAdditionalPagesChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.bookletFormatChanged.connect(ticketChangeHandler)

            // Stamp options
            _stateMachine.stampContentUpdateChanged.connect(ticketChangeHandler)
            const stampSections = [
                "stampTopLeft",
                "stampTopCenter",
                "stampTopRight",
                "stampBottomLeft",
                "stampBottomCenter",
                "stampBottomRight"
            ];

            stampSections.forEach(section => {
                const sectionData = _stateMachine.ticketModel.data.pipelineOptions.data[section].data;
                sectionData.textColorChanged.connect(ticketChangeHandler);
                sectionData.textFontChanged.connect(ticketChangeHandler);
                sectionData.textSizeChanged.connect(ticketChangeHandler);
                sectionData.startingPageChanged.connect(ticketChangeHandler);
                sectionData.startingNumberChanged.connect(ticketChangeHandler);
                sectionData.numberOfDigitsChanged.connect(ticketChangeHandler);
                sectionData.pageNumberingStyleChanged.connect(ticketChangeHandler);
                sectionData.whiteBackgroundChanged.connect(ticketChangeHandler);
            });

            // Print options
            _stateMachine.ticketModel.data.dest.data.print.data.duplexBindingChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSizeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaTypeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSourceChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.printQualityChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.printingOrderChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.rotateChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaFamilyChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.collateChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.copiesChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.plexModeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.printMarginsChanged.connect(ticketChangeHandler)

            // Output scale options
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.xScalePercentChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.yScalePercentChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.scaleSelectionChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.scaleToOutputChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.scaleToSizeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.fitToPageIncludeMarginChanged.connect(ticketChangeHandler)

            //watermark options
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.watermarkTypeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.watermarkIdChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.customTextChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.textFontChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.textSizeChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.textColorChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.onlyFirstPageChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.rotate45Changed.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.backgroundColorChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.backgroundPatternChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.darknessChanged.connect(ticketChangeHandler)
        }
    }

    function disconnectEachDataChangeNonPageSensor(){
        if(_stateMachine.ticketModel){
            console.info("[CopyController] disconnectEachDataChangeNonPageSensor")

            // Scan options
            _stateMachine.ticketModel.data.src.data.scan.data.contentTypeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.mediaTypeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.mediaSizeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.colorModeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.plexModeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.pagesFlipUpEnabledChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.edgeToEdgeScanChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.autoDeskewChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.src.data.scan.data.scanCaptureModeChanged.disconnect(ticketChangeHandler)

            // Pipeline options
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.exposureChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.backgroundColorRemovalChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.backgroundNoiseRemovalChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.pagesPerSheetChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.numberUpPresentationDirectionChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.imageBorderChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.autoPaperColorRemovalChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.autoPaperColorRemovalLevelChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.autoToneChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.autoToneLevelChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.blankPageSuppressionEnabledChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.promptForAdditionalPagesChanged.connect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.bookletFormatChanged.disconnect(ticketChangeHandler)

            // Stamp options
            _stateMachine.stampContentUpdateChanged.disconnect(ticketChangeHandler)
            const stampSections = [
                "stampTopLeft",
                "stampTopCenter",
                "stampTopRight",
                "stampBottomLeft",
                "stampBottomCenter",
                "stampBottomRight"
            ];

            stampSections.forEach(section => {
                const sectionData = _stateMachine.ticketModel.data.pipelineOptions.data[section].data;
                sectionData.textColorChanged.disconnect(ticketChangeHandler);
                sectionData.textFontChanged.disconnect(ticketChangeHandler);
                sectionData.textSizeChanged.disconnect(ticketChangeHandler);
                sectionData.startingPageChanged.disconnect(ticketChangeHandler);
                sectionData.startingNumberChanged.disconnect(ticketChangeHandler);
                sectionData.numberOfDigitsChanged.disconnect(ticketChangeHandler);
                sectionData.pageNumberingStyleChanged.disconnect(ticketChangeHandler);
                sectionData.whiteBackgroundChanged.disconnect(ticketChangeHandler);
            });

            // Print options
            _stateMachine.ticketModel.data.dest.data.print.data.duplexBindingChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSizeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaTypeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSourceChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.printQualityChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.printingOrderChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.rotateChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaFamilyChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.collateChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.copiesChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.plexModeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.dest.data.print.data.printMarginsChanged.disconnect(ticketChangeHandler)

            // Output scale options
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.xScalePercentChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.yScalePercentChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.scaleSelectionChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.scaleToOutputChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.scaleToSizeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.scaling.data.fitToPageIncludeMarginChanged.disconnect(ticketChangeHandler)

            //watermark options
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.watermarkTypeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.watermarkIdChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.customTextChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.textFontChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.textSizeChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.textColorChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.onlyFirstPageChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.rotate45Changed.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.backgroundColorChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.backgroundPatternChanged.disconnect(ticketChangeHandler)
            _stateMachine.ticketModel.data.pipelineOptions.data.watermark.data.darknessChanged.disconnect(ticketChangeHandler)
        }
    }

    function ticketChangeHandler()
    {
        if(_stateMachine)
        {
            console.info("[CopyController] ticketChangeHandler isTicketModelChanged = true")
            _stateMachine.isTicketModelChanged = true
        }
    }

    function exitInterruptPriorityModeSession()
    {
        if( _stateMachine.priorityInterruptModeSessionModel != null )
        {
            let id = _stateMachine.priorityInterruptModeSessionModel.data.priorityModeSessionId;//saved to be printed after model destruction

            let destructionRequest = _resourceStore.destroyResource(_stateMachine.priorityInterruptModeSessionModel);
            console.log("Request exitInterruptPriorityModeSession - Exit Interrupt Priority Mode sessionId:" + id);

            destructionRequest.resolved.connect((future) => {
                                        console.log("exitInterruptPriorityModeSession - Future SUCCESS sessionId:" + id);
                                    });
            destructionRequest.rejected.connect((future) => {
                                        console.log("exitInterruptPriorityModeSession - Future FAIL sessionId:" + id);
                                    });
                                    
            _stateMachine.priorityInterruptModeSessionModel = null;
        }
        else
        {
            console.log("exitInterruptPriorityModeSession - Future NO EXEC priorityInterruptModeSessionModel IS NULL");
        }
    }


    function enterInterruptPriorityModeSession( postAction, errorCallback)
    {
        console.assert( _stateMachine.priorityInterruptModeSessionModel == null ); //Only one object Interrupt session must exist

        _stateMachine.priorityInterruptModeSessionModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_PRIORITY_MODE_SESSION);
        _stateMachine.priorityInterruptModeSessionModel.data.applicationId = root.appId
        _stateMachine.priorityInterruptModeSessionModel.data.behavior = "interruptAndBlockNonUrgentJobs"

        let creationReponse = _resourceStore.create("/cdm/jobManagement/v1/priorityModeSessions", _stateMachine.priorityInterruptModeSessionModel);
        
        console.log("Request enterInterruptPriorityModeSession root.appId:" + root.appId);

        if(typeof errorCallback === "undefined")
        {
            errorCallback = function(future) {
                console.log("enterInterruptPriorityModeSession - Future FAIL sessionId:" + future.error);
                _stateMachine.priorityInterruptModeSessionModel = null;
            }
        }
        creationReponse.resolved.connect((future) => {
                                        _stateMachine.priorityInterruptModeSessionModel = future.get();
                                        console.log("enterInterruptPriorityModeSession - Future SUCCESS" );
                                        if (typeof postAction === "function") {
                                            postAction();
                                        }
                                    });
        creationReponse.rejected.connect(errorCallback)
    }

    function getHighestPriorityModeSessionId()
    {

        if( _stateMachine.priorityInterruptModeSessionModel != null )
        {
            return _stateMachine.priorityInterruptModeSessionModel.data.priorityModeSessionId;
        }
        else
        {
            return _stateMachine.priorityModeSessionId;
        }
    }

    function printTicketModel( ticketModel, titleMessage )
    {
        let title = titleMessage === undefined ? "" : titleMessage;

        console.log("===== ticketModel =======" + title + "=============");
        if( ticketModel )
        {
            console.log("ticketModel:" + ticketModel);
            console.log("ticketModel.ticketId:" + ticketModel.data.ticketId );
            console.log("ticketModel.ncopies:" + ticketModel.data.dest.data.print.data.copies );
            console.log("ticketModel.settings_color:" + _qmlUtils.getEnumValueAsString(ticketModel.data.src.data.scan.data,"colorMode") + " :" + ticketModel.data.src.data.scan.data.colorMode);
            console.log("ticketModel.settings_input_sides:" + _qmlUtils.getEnumValueAsString(ticketModel.data.src.data.scan.data,"plexMode") + " :" + ticketModel.data.src.data.scan.data.plexMode);
            console.log("ticketModel.settings_size:" + _qmlUtils.getEnumValueAsString(ticketModel.data.src.data.scan.data, "mediaSize") + " :" + ticketModel.data.src.data.scan.data.mediaSize );
            console.log("ticketModel.settings_resolution:" + _qmlUtils.getEnumValueAsString(ticketModel.data.src.data.scan.data,"resolution") + " :" + ticketModel.data.src.data.scan.data.resolution);
            console.log("ticketModel.settings_scanner_source:" + _qmlUtils.getEnumValueAsString(ticketModel.data.src.data.scan.data, "mediaSource") + " :" + ticketModel.data.src.data.scan.data.mediaSource);
            console.log("ticketModel.settings_tray:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data,"mediaSource") + " :" + ticketModel.data.dest.data.print.data.mediaSource);
            console.log("ticketModel.settings_output_sides:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "plexMode") + " :" + ticketModel.data.dest.data.print.data.plexMode);
            console.log("ticketModel.settings_collate:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "collate") + " :" + ticketModel.data.dest.data.print.data.collate);
            console.log("ticketModel.settings_output_media_type:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "mediaType") + " :" + ticketModel.data.dest.data.print.data.mediaType);
            console.log("ticketModel.settings_print_quality:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "printQuality") + " :" + ticketModel.data.dest.data.print.data.printQuality);
            console.log("ticketModel.settings_duplex_binding:" + _qmlUtils.getEnumValueAsString(ticketModel.data.dest.data.print.data, "duplexBinding") + " :" + ticketModel.data.dest.data.print.data.duplexBinding);
            console.log("ticketModel.settings_pagesPersheet:" + _qmlUtils.getEnumValueAsString(ticketModel.data.pipelineOptions.data.imageModifications.data, "pagesPerSheet") + " :" + ticketModel.data.pipelineOptions.data.imageModifications.data);
        }
        else
        {
            console.log("ticketModel: NULL, NOT DEFINED!" );
        }
        console.log("=================================================");

    }

    function printJobInfoModel( jobInfoModel, titleMessage )
    {
        let title = titleMessage === undefined ? "" : titleMessage;

        console.log("-----------------jobInfoModel------" + title + "------------------------");
        if( jobInfoModel )
        {
            console.log("jobInfoModel: " + jobInfoModel);
            console.log("jobInfoModel.jobId: " + jobInfoModel.data.jobId);
            console.log("jobInfoModel.state: " + jobInfoModel.data.state);
            console.log("jobInfoModel.ticketId: " + jobInfoModel.data.ticketId);
            console.log("jobInfoModel.jobType: " + jobInfoModel.data.jobType);
            console.log("jobInfoModel.userName: " + jobInfoModel.data.userName);
            console.log("jobInfoModel.fullyQualifiedName: " + jobInfoModel.data.fullyQualifiedName);
            console.log("jobInfoModel.priorityModeSessionId: " + jobInfoModel.data.priorityModeSessionId);
        }
        else
        {
            console.log("jobInfoModel: NULL, NOT DEFINED!" );
        }
        console.log("------------------------------------------------------------");
    }

    function handleRequestFailure(future) {
        if (typeof _stateMachine != "undefined")
        {
            console.log("handleRequestFailure: message " + future.error);
            console.assert(0,"ERROR request for "+ future + " failed error " + future.error);
            _stateMachine.submitEvent("quitRequested");
        }
        
    }

    function unsubscribeScannerStatus(){
        if(_stateMachine.scannerStatus){
            console.log("scanner status disconnect");       
            _stateMachine.scannerStatus.data.scannerStateChanged.disconnect(updateScannerState);
            _stateMachine.scannerStatus.data.flatbed.data.stateChanged.disconnect(updateScannerMediaSource);
            if(_stateMachine.scannerStatus.data.adf)
            {
                _stateMachine.scannerStatus.data.adf.data.stateChanged.disconnect(updateScannerMediaSource);  
            }           
        }

    }

    function updateScannerMediaSource()
    {
        //choose the scanner source according to the scanner status to avoid mismatch
        let adfAvailable = false;
        let flatbedAvailable = false;
        let inputMediaSource = Scan_1_ScanAdfStateType.ScanAdfStateType._undefined_;
                
        if (_stateMachine.scannerStatus.data.adf && _stateMachine.scannerStatus.data.adf.data)
        {
            console.log("scanner adf available with state:" + _qmlUtils.getEnumValueAsString(_stateMachine.scannerStatus.data.adf.data,"state") + 
                            " :" + _stateMachine.scannerStatus.data.adf.data.state + " while ScannerAdfLoaded is " + 
                            Scan_1_ScanAdfStateType.ScanAdfStateType.ScannerAdfLoaded + 
                            " (" + _qmlUtils.getValueFromStringifiedEnum("dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType", "ScannerAdfLoaded") + ")" );
            adfAvailable = true;
        }
        if (_stateMachine.scannerStatus.data.flatbed && _stateMachine.scannerStatus.data.flatbed.data)
        {
            console.log("scanner flatbed available with state:" + _qmlUtils.getEnumValueAsString(_stateMachine.scannerStatus.data.flatbed.data,"state") + 
                " :" + _stateMachine.scannerStatus.data.flatbed.data.state);
            flatbedAvailable = true;
        }


        if (adfAvailable && _stateMachine.scannerStatus.data.adf.data.state == Scan_1_ScanAdfStateType.ScanAdfStateType.ScannerAdfLoaded
            //these types should be equivalent
            //_stateMachine.scannerStatus.data.adf.data.state == _qmlUtils.getValueFromStringifiedEnum("dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType", "ScannerAdfLoaded")
        )
        {
            _stateMachine.inputMediaSourceSelected = Glossary_1_ScanMediaSourceId.ScanMediaSourceId.adf
            inputMediaSource = "adf";
            _stateMachine.isFlatbedLoaded = false
        }
        else if (flatbedAvailable)
        {
            _stateMachine.inputMediaSourceSelected = Glossary_1_ScanMediaSourceId.ScanMediaSourceId.flatbed
            inputMediaSource = "flatbed";
            _stateMachine.isFlatbedLoaded = true
        }

        console.log("scanner source selected:" + inputMediaSource);

        if (_stateMachine.ticketModel && _qmlUtils.getEnumValueAsString(_stateMachine.ticketModel.data.src.data.scan.data,"mediaSource") != inputMediaSource && !_stateMachine.inPreviewState){
            _stateMachine.ticketModel.data.src.data.scan.data.mediaSource = inputMediaSource
            console.log("Updating scannerStatus and inputMediaSource")
            Qt.callLater(updateJobTicket)
        }
    }

    function updateJobTicket(){
        if(_stateMachine.ticketModel){
            console.log("Updating JobTicket")
            ResourceStoreBinding.handleFuture(()=> _resourceStore.modify(_stateMachine.ticketModel)).then((future) => { 
                console.log("ticket Modify Resolved ");
                // This condition is to avoid a SE when the widget copy app is open and closed fastly
                if(!!_stateMachine)
                {
                    _stateMachine.submitEvent("ev.ticketupdated");
                }
                else
                {
                    console.log("updateJobTicket submitEvent cannot be done");
                }
            }).catch((future) => {
                handleRequestFailure(future)
            })
        }
        else
        {
            console.log("updateJobTicket Updating JobTicket cannot be done");
        }
    }

    function updateScannerState(){
        console.log("New Scanner state " + scannerStateToString(_stateMachine.scannerStatus.data.scannerState));
        _stateMachine.scannerState = _stateMachine.scannerStatus.data.scannerState
        let event = ""
        if( _stateMachine.scannerStatus.data.scannerState == Scan_1_ScannerStatusType.ScannerStatusType.Idle )
        {
            _stateMachine.isScannerIdle = true
            event = "ev.scannerStateIdle"
        }
        else if( _stateMachine.scannerStatus.data.scannerState == Scan_1_ScannerStatusType.ScannerStatusType.Processing )
        {
            _stateMachine.isScannerIdle = false
            event = "ev.scannerStateProcessing"
        }
        else
        {
            // FSM should advance when the scanner state is not processing. (in ACQUIRING state)
            event = "ev.scannerStateFinishedProcessing"
        }
            _stateMachine.submitEvent(event)
        
    }
    
    function jobStateToString(state)
    {
        let stateString;

        switch ( Number( state ) )
        {
        case JobManagement_1_State.State.created:
            stateString =  "Created";
            break;
        case JobManagement_1_State.State.ready:
            stateString =  "Ready";
            break;
        case JobManagement_1_State.State.processing:
            stateString =  "Processing";
            break;
        case JobManagement_1_State.State.startProcessing:
            stateString =  "Processing";
            break;
        case JobManagement_1_State.State.initializeProcessing:
            stateString =  "Initializing";
            break;
        case JobManagement_1_State.State.cancelProcessing:
            stateString =  "Canceling";
            break;
        case JobManagement_1_State.State.resumeProcessing:
            stateString =  "Resuming";
            break;
        case JobManagement_1_State.State.pauseProcessing:
            stateString =  "Pausing";
            break;
        case JobManagement_1_State.State.waiting:
            stateString =  "Pending";
            break;
        case JobManagement_1_State.State.paused:
            stateString =  "Paused";
            break;
        case JobManagement_1_State.State.completed:
            stateString =  "Completed";
            break;
        default:
            stateString =  "Unknown";
            break;
        }

        return stateString;
    }

    function ejectActionExecution( scannerStatus )
    {
        console.assert( scannerStatus !== null );
        console.assert( scannerStatus.data.mdf.ejectable !== null );

        scannerStatus.data.mdf.state = Scan_1_ScanMediaPathStateType.ScanMediaPathStateType.ejectProcessing;
        scannerStatus.data.mdf.ejectable = Glossary_1_FeatureEnabled.FeatureEnabled.false_;
        let ejectResponse = _resourceStore.modify(_stateMachine.scannerStatus);
        ejectResponse.resolved.connect((future) => { console.info("ejectResponse: status request Resolved OK " + future);});
        ejectResponse.rejected.connect(handleRequestFailure)
    }

    function scannerStateToString(state)
    {
        let stateString = "";

        switch ( Number( state ) )
        {
            case Scan_1_ScannerStatusType.ScannerStatusType.Idle:
                stateString = "Idle";
                break;
            case Scan_1_ScannerStatusType.ScannerStatusType.Processing:
                stateString =  "Processing";
                break;
            case Scan_1_ScannerStatusType.ScannerStatusType.Down:
                stateString = "Down";
                break;
            case Scan_1_ScannerStatusType.ScannerStatusType.Testing:
                stateString = "Testing";
                break;
            case Scan_1_ScannerStatusType.ScannerStatusType.Stopped:
                stateString = "Stopped";
                break;
            default:
                stateString = "Unkown scanner state value. State is " + Number(state);
        }

        return stateString;
    }

    function subscribeToCopyConfiguration()
    {
        let response = _resourceStore.subscribe("/cdm/copy/v1/configuration");

        response.resolved.connect((future) => {
            console.log("cdm/copy/v1/configuration resolved");
            _stateMachine.copyConfiguration = future.get();            
            if(_stateMachine.copyConfiguration.data.allowInterrupt == Glossary_1_FeatureEnabled.FeatureEnabled.true_) {
                //create priority mode session before starting the inception flow, to be optimized
                handleInitialInterruptMode();
            }
            else {
                _stateMachine.submitEvent("ev.configurationsResolved");
            }
            _stateMachine.copyConfiguration.data.allowInterruptChanged.connect(handleAllowInterruptChanged);
        });

        response.rejected.connect((future) => {
            console.log("cdm/copy/v1/configuration rejected: " + future.error)
            _stateMachine.submitEvent("quitRequested")
        });
    }

    function unsubscribeToCopyConfiguration()
    {
        if(!!_stateMachine.copyConfiguration)
        {
            _resourceStore.unsubscribe(_stateMachine.copyConfiguration);
            _stateMachine.copyConfiguration.data.allowInterruptChanged.disconnect(handleAllowInterruptChanged);
        }
    }

    function subscribeToScannerStatus(){
        if(_stateMachine.scannerStatus)
        {
            _stateMachine.scannerStatus.data.scannerStateChanged.connect(updateScannerState);
            if (_stateMachine.scannerStatus.data.mdf && _stateMachine.scannerStatus.data.mdf.data)
            {
                _stateMachine.inputMediaSourceSelected = Glossary_1_ScanMediaSourceId.ScanMediaSourceId.mdf
                _stateMachine.updateMdfState()
                _stateMachine.scannerStatus.data.mdf.stateChanged.connect(_stateMachine.updateMdfState);

                updateScannerState()

                _stateMachine.updateMdfEjectableState();
                _stateMachine.scannerStatus.data.mdf.ejectableChanged.connect( _stateMachine.updateMdfEjectableState )
                
                if(!_stateMachine.isScanMediaLoaded)
                {
                    _stateMachine.firstScan = false;
                }

            }
            else 
            {
                console.log( "scanStatusResponse: No mdf" );
                updateScannerState()
                console.log("scanner status: version " + _stateMachine.scannerStatus.data.version);
                console.log("scanner status state " + _stateMachine.scannerStatus.data.scannerState);
                console.log("scanner status error " + _stateMachine.scannerStatus.data.scannerError);

                if (_stateMachine.scannerStatus.data.adf)
                {   
                    console.log("scanner adf flavor: " + _stateMachine.scannerStatus.data.adf.data.flavor);
                    console.log("scanner adf status: " + _stateMachine.scannerStatus.data.adf.data.state);
                    console.log("scanner adf errorType: " + _stateMachine.scannerStatus.data.adf.data.errorType);
                    if(_stateMachine.scannerStatus.data.adf.duplexSupported == Glossary_1_FeatureEnabled.FeatureEnabled.true_){
                        console.log("scanner adf duplex supported")
                        _stateMachine.isDuplexSupported = true
                    }
                    else{
                        console.log("scanner adf duplex not supported")
                        _stateMachine.isDuplexSupported = false
                    }
                    _stateMachine.scannerStatus.data.adf.stateChanged.connect(_stateMachine.controller.updateScannerMediaSource);
                }
                if (_stateMachine.scannerStatus.data.flatbed)
                {   
                    console.log("scanner flatbed flavor: " + _stateMachine.scannerStatus.data.flatbed.data.flavor);
                    console.log("scanner flatbed status: " + _stateMachine.scannerStatus.data.flatbed.data.state);
                    console.log("scanner flatbed errorType: " + _stateMachine.scannerStatus.data.flatbed.data.errorType);
                    _stateMachine.scannerStatus.data.flatbed.stateChanged.connect(_stateMachine.controller.updateScannerMediaSource);
                }
            }
            
                
        }
        else
        {
            console.assert("Scanner Model is not available")
        }
    }
    
    function setWalkupAppCapabilities()
    {
        setScannerCapability()

        // setStatMeachine Flow

        if(_stateMachine.isAdfCapabilities() ||(_stateMachine.isMdfCapabilities() && !_stateMachine.isConcurrent))
        {
            _stateMachine.selectedStateMachineFlow = _stateMachine.nonPageSensorFlow
        }
        else if(_stateMachine.isMdfCapabilities() && _stateMachine.isConcurrent)
        {
            _stateMachine.selectedStateMachineFlow = _stateMachine.pageSensorFlow
            let component = Qt.createComponent("qrc:/ScanApp/ScanAppController.qml")
            _stateMachine.scanAppController = component.createObject(copyController)
        }
        else
        {
            console.warn("StateMachineflowPath not known");
        }
    }

    function setScannerCapability()
    {
        if (_stateMachine.scannerStatus)
        {
            if (_stateMachine.scannerStatus.data.adf && _stateMachine.scannerStatus.data.adf.data)
            {
                _stateMachine.configCapabilityScannerType  = _stateMachine.capabilityAdf;
            }
            else if(_stateMachine.scannerStatus.data.mdf && _stateMachine.scannerStatus.data.mdf.data)
            {
                _stateMachine.configCapabilityScannerType =  _stateMachine.capabilityMdf;
            }
            else if(_stateMachine.scannerStatus.data.flatbed && _stateMachine.scannerStatus.data.flatbed.data)
            {
                console.log("Scanner is flatbed, similar to ADF")
                _stateMachine.configCapabilityScannerType =  _stateMachine.capabilityAdf;
            }
        }
        else{
            console.assert("ERROR: ScannerStatus not found");
        }
    }

    function getPrepreviewMessageForMdf()
    {
            let prePreviewPageInserted = _qmlUtils.createCollection(copyController)
            prePreviewPageInserted.append(_qmlUtils.createSpiceLoc(copyController ,{"stringId": _propertyMap.valueMap("PrepreviewPagesensor").asMap()["CopyToStartJob"]}))
            let prePreviewPageInsertMessage = _qmlUtils.createCollection(copyController)
            prePreviewPageInsertMessage.append(_qmlUtils.createSpiceLoc(copyController ,{"stringId": _propertyMap.valueMap("PrepreviewPagesensor").asMap()["CopyOptionsToScan"]}))
            return _stateMachine.isScanMediaLoaded ? prePreviewPageInserted : prePreviewPageInsertMessage
    }

    function isSettingEnabled(settingCDMPath)
    {
        let settingEnabled = true;

        // Dont allow directly use of the edit settings currently used only for jupiter
        if(_stateMachine.isPageSensorflow() && _stateMachine.isEditSettingsActionEnabled != undefined && !_stateMachine.isEditSettingsActionEnabled)
        {
            console.log("Ignoring isSettingEnabled.");
            return false;
        }

        let validator = findValidatorForConstraint(settingCDMPath);

        // Check if lock constraint is enabled.
        if(validator != null && validator.disabled != null)
        {
            settingEnabled = (validator.disabled.value === Glossary_1_FeatureEnabled.FeatureEnabled.false_);
        }

        console.log("isSettingEnabled ", settingCDMPath, settingEnabled);

        // If the validator is null or doesn't have a disabled property, then enable the setting.
        return settingEnabled;
    }

    function findValidatorForConstraint( propertyPointer )
    {
        console.debug("propertyPointer is:", propertyPointer, this);

        let validator = null;
        
        if(_stateMachine.constraintModel && _stateMachine.constraintModel.data.validators)
        {
            for(var i = 0; i < _stateMachine.constraintModel.data.validators.count; i++)
            {
                if(_stateMachine.constraintModel.data.validators.at(i).data.propertyPointer == propertyPointer)
                {
                    validator = _stateMachine.constraintModel.data.validators.at(i);
                    console.debug("Find propertyPointer from validators : " + validator.propertyPointer);
                    break;
                }
            }
        }

        return validator;
    }
    /*======================================================================
    PLEASE MAINTEIN ALL BELOW FUNCTIONS OF CONTROLLER AS DISCOUPLED AS WE CAN.
    BELOW FUNTIONS ARE BASIC, REUSBLE AND AUTONOMOUS FOR EVERY PRODUCT, IN EVERY MOMENT,
    IN EVERY APP.

            SO PLEASE DONT MODIFY THEM FOR CONCRETE PRODUCT NEEDS
    ======================================================================

    - This controller is shared among all UX. Each UX have a different scxml stateMachine file,
        so different properties are defined in each UX stateMachine, or maybe some UXs can use
        another different system to .scxml. So please:
            * Avoid references to _stateMachine
            * Avoid use properties of _stateMachine, eg: _stateMachine.scannerState
            * Avoid emit statemachine events, becausean event is particular of a concrete stateMAchine
    - Avoid concatenated lambda function. For avoiding concatenated lambda functions for executing several
        asynchronous actions please create states in state machine, an asynch action by state if needed

    - Please use params on Controller functions
    - Please use return values
    - Please use console.assert instead big if-else statements that can mask error
    - Please use console.assert to define prerequisites for doing functions correctly working
    - Please dont modify functions for concrete products needs, create a
        new one that use exist function and increase the complexicity
    ======================================================================*/

    /***************************CONSTANTS********************************/
    readonly property string scan_status_url: "/cdm/scan/v1/status";
    readonly property string job_ticket_url: "/cdm/jobTicket/v1/tickets";
    readonly property string job_management_url: "/cdm/jobManagement/v1/jobs"
    //Next const is used for copy ticket creation in ticketModel.data.ticketReference = "defaults/copy";
    readonly property string copy_ticket_reference: "defaults/copy"
    readonly property string clone_ticket_reference: "/cdm/jobTicket/v1/tickets/" //+ticketId
    readonly property string subscribe_constraints_url: "/cdm/jobTicket/v1/tickets/%1/constraints" // %1:ticketId

     //maybe ticketClone is not needed and we obtained from future

    function setTicketAsMultipage( ticketModel )
    {
        console.log("setCopyTicketAsMultipage -- Enter");

        // It can happen that doQuit is executed and then this function.
        // If we enter and exit the app really fast on MFP.
        if( ticketModel != null )
        {
            ticketModel.data.src.data.scan.data.scanCaptureMode = JobTicket_1_ScanCaptureMode.ScanCaptureMode.jobBuild;
            if(_stateMachine.isMultiPagePreviewSupported){
                ticketModel.data.pipelineOptions.data.generatePreview = Glossary_1_FeatureEnabled.FeatureEnabled.true_;
            }
            
            let modificationResponse = _resourceStore.modify(ticketModel);

            modificationResponse.rejected.connect((future) => { console.error("setTicketAsMultipage REJECTED " + future.error);});
        }
    }

    function printPatching( jobInfoModel, patchToState)
    {
        console.log("=======EXECUTIN PATCHING=============================================")
        console.log("== jobInfoModel:"  + jobInfoModel);
        if(jobInfoModel)
        {
             console.log("== jobId: " + jobInfoModel.data.jobId);
            console.log("== PATCHING from: " + jobStateToString(jobInfoModel.data.state) +
                                " to: " + jobStateToString(patchToState));
        }
    }

    function stopScanThruJobTicket(jobData, successCallback = null, errorCallback = null) 
    {
        console.log("stopScanThruJobTicket: stopScan")

        let jobOperationModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_JOB_OPERATION)
        jobOperationModel.data.state = JobManagement_1_JobOperation_State.State.processing;
        jobOperationModel.data.url = "/cdm/jobManagement/v1/jobs/" + jobData.jobId + "/stopScan"

        let futureStopScan = _resourceStore.modify(jobOperationModel);
        
        futureStopScan.resolved.connect((futureStopScanInternal) => 
        {
            if (successCallback) 
            {
                successCallback(futureStopScanInternal.get());
            }
            else 
            {
                console.log("stopScan - No callback registered for success");
            }
        })

        futureStopScan.rejected.connect((futureStopScanInternal) => 
        {
            if (errorCallback) 
            {
                errorCallback();
            }
            else 
            {
                console.log(" stopScan - Error in CDM operation. Error: ", futureStopScanInternal.error);
            }
        })
    }

    function connectUISettingDataChange(){
        // Add here the new settings connect to notify changes in UI and show toat in scans between pages
        console.log("connectUISettingDataChange enter ");
        console.assert(_stateMachine.isPageSensorflow());

        if(_stateMachine.ticketModel)
        {
            // Scan options
            _stateMachine.ticketModel.data.src.data.scan.data.contentTypeChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.mediaTypeChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.colorModeChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.resolutionChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.invertColorsChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.pipelineOptions.data.manualUserOperations.data.autoReleaseChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.blackBackgroundChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.backgroundColorRemovalLevelChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.blackEnhancementLevelChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.src.data.scan.data.scanAcquisitionsSpeedChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.autoDeskewChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);

            // Print options
            _stateMachine.ticketModel.data.dest.data.print.data.copiesChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.dest.data.print.data.printQualityChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaDestinationChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.printMarginsChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.printingOrderChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.rotateChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaFamilyChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.collateChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            // ... output scale
            _stateMachine.ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.scaling.yScalePercentChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleSelectionChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleToOutputChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleToSizeChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)

            // ... output size: media source/size/positioning/orientation
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.outputCanvasMediaIdChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.outputCanvasMediaSizeChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.outputCanvasAnchorChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.outputCanvasOrientationChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages)

            // ... paper selection
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSourceChanged.connect(_stateMachine.showToastSettingUpdatedBettwenPages);
        }
    }

    function disconnectUISettingDataChange(){

        console.log("disconnectUISettingDataChange enter ");
        // Todo An assert would be better but it has given an intermittent problem, a bug has been created to investigate the change.(Jira DUNE-106680)
        if(_stateMachine.ticketModel)
        {
            // Scan options
            _stateMachine.ticketModel.data.src.data.scan.data.contentTypeChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.mediaTypeChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.colorModeChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.resolutionChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.invertColorsChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.pipelineOptions.data.manualUserOperations.data.autoReleaseChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.blackBackgroundChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.backgroundColorRemovalLevelChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.blackEnhancementLevelChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.src.data.scan.data.scanAcquisitionsSpeedChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.src.data.scan.data.autoDeskewChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);

            // Print options
            _stateMachine.ticketModel.data.dest.data.print.data.copiesChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
            _stateMachine.ticketModel.data.dest.data.print.data.printQualityChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaDestinationChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.printMarginsChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.rotateChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.mediaFamilyChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.printingOrderChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.dest.data.print.data.collateChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            // ... output scale
            _stateMachine.ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.scaling.yScalePercentChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleSelectionChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleToOutputChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleToSizeChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)

            // ... output size: media source/size/positioning/orientation
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.outputCanvasMediaIdChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.outputCanvasMediaSizeChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.outputCanvasAnchorChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.outputCanvasOrientationChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages)

            // ... paper selection
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSourceChanged.disconnect(_stateMachine.showToastSettingUpdatedBettwenPages);
        }
        else
        {
            console.log("disconnectUISettingDataChange ticketModel is empty when disconected");
        }
    }

    function printerStatusResolved(future)
    {
        if(_stateMachine)
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

    function unsubscribeToPrinterStatus(){
        if(_stateMachine.printStatusModel){
            console.log("printer status disconnect");       
            _stateMachine.printStatusModel.data.printerStateChanged.disconnect(_stateMachine.printerStateChanged);
            _resourceStore.unsubscribe(_stateMachine.printStatusModel)
        }
    }
    function subscribeToPrinterStatus(){
        let future = _resourceStore.subscribe("/cdm/print/v2/status");
        future.resolved.connect(printerStatusResolved);
    }
    
    function evaluateMainActionButtonState()
    {
        let mainActionButtonType = "COPY";
        if(_stateMachine.isPageSensorflow())
        {
            if(_stateMachine.isPreviewRequired() && !_stateMachine.inPreviewState )
            {
                mainActionButtonType = "START";
            }
            else
            {
                mainActionButtonType = _stateMachine.isJobDirect ? "DONE" : "COPY"
            }
        }
        else
        {
            if(_stateMachine.isPreviewRequired() && !_stateMachine.inPreviewState )
            {
                mainActionButtonType = "PREVIEW";
            }
            else {
                mainActionButtonType = "COPY"
            }
        }
        return mainActionButtonType
    }

    function getDefaultPreviewConfiguration()
    {
        console.log("getDefaultPreviewConfiguration")
        let future = _resourceStore.get("/cdm/jobTicket/v1/configuration/defaults/copy"); 
        future.resolved.connect((future) => {
                                                console.log("getDefaultPreviewConfiguration resolved");
                                                let defaultSettings = future.get();
                                                //to be decided if previewConfig has to be from defaults or ticket specific.
                                                _stateMachine.previewConfiguration = defaultSettings.data.pipelineOptions.data.manualUserOperations.data.imagePreviewConfiguration
                                                _stateMachine.submitEvent("ev.configurationsResolved");
                                            })
        future.rejected.connect(handleRequestFailure)
    }

    function ticketReferenceForPageSensorFlow(initiate){
        let response = _resourceStore.get("/cdm/shortcut/v1/shortcuts/" + root.appId );
        let reference = "";
        response.resolved.connect((future) => {
            let shortcut = future.get();
            console.log("ticketReferenceForPageSensorFlow: shortcut: " + shortcut);
            for( let i = 0; i < shortcut.data.links.count; i++ )
            {
                if(shortcut.data.links.get(i).rel == "shortcut")
                {
                    reference = shortcut.data.links.get(i).href;
                    console.log("ticketReferenceForPageSensorFlow: reference: " + reference);
                }
            }
            if( reference == "" )
            {
                reference = "defaults/copy"
            }
            initiate(reference);   
             
             
        });
    }

    function handleInitialInterruptMode()
    {
        console.log("handleInitialInterruptMode")
        enterInterruptPriorityModeSession(postAction , postAction)

        function postAction(future)
        {
            _stateMachine.submitEvent("ev.configurationsResolved");
        }
    }

    function handleAllowInterruptChanged()
    {
        let isInterruptCopyEnabled = _stateMachine.copyConfiguration.data.allowInterrupt == Glossary_1_FeatureEnabled.FeatureEnabled.true_
        console.log("handleAllowInterruptChanged:" + isInterruptCopyEnabled);

        if(isInterruptCopyEnabled)
        {
            console.assert(_stateMachine.priorityInterruptModeSessionModel == null); 
            enterInterruptPriorityModeSession(postAction)

            function postAction(future)
            {
                if(_stateMachine.priorityInterruptModeSessionModel == null )
                {
                    console.log("[warn]enterInterruptPriorityModeSession - Future warning: priorityModeSessionModel == null");
                }
                else
                {
                    _stateMachine.refreshJob();
                    console.log("enterInterruptPriorityModeSession - Future SUCCESS: sessionId:" + _stateMachine.priorityInterruptModeSessionModel.data.priorityModeSessionId );
                }
            }
        }
        else
        {                
            exitInterruptPriorityModeSession();
        }
        
    }
}
