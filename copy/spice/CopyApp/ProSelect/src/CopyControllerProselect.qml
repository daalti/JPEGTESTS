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

    function toShowResolutionSetting()
    {
        if (_stateMachine.scannerStatus.data.mdf){
            return true
        }
        else {
            return false
        }
    }

    function getConstraintUrl()
    {
        let url = ""
        if(_stateMachine.ticketModel){
              for(let i = 0; i < _stateMachine.ticketModel.data.links.count; ++i){
                   if(_stateMachine.ticketModel.data.links.get(i).rel === "constraints"){
                        url =  _stateMachine.ticketModel.data.links.get(i).href
                        break
                    }
                }
            }
        console.log(url)
       return url
    }

    function getTicketModel(){
        return _stateMachine.ticketModel
    }

    function isOutputScaleEnabled(){
        if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null){
            if(_stateMachine.ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet == JobTicket_1_PagesPerSheet.PagesPerSheet.oneUp){
                return true
            }
            else{
                return false
            }
        }

        return true
    }

    function isCollateEnabled(){
        if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null){
            if(_stateMachine.isAdfCapabilities()){
                return !_stateMachine.isFlatbedLoaded
            }
            else{
                return true
            }
        }

        return true
    }

    function isPagesPerSheetEnabled(){
        if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null){
            let value = _menuResource.enumStringFromValue("dune::spice::jobTicket_1::scaling::ScaleSelection::ScaleSelection", _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleSelection)
            if(value == "none"){
                return true
            }
            else{
                return false
            }
        }

        return true
    }

    function isDuplexing() {
        if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null){
            if(_stateMachine.ticketModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.simplex){
                return false
            }
            else{
                return true
            }
        }

        return false
    }

    function isCopyColorPrintSupported() {
        if (_stateMachine.isColorPrintSupported){
            console.log("function isColorModeSupported() : supported");
            return true
        }
        else{
            return false
        }
    }
    
    function cloneJobTicket(successSlot){
        if(!_stateMachine.isOneTouchQuickSet){
                console.log("Unsubscribing jobTicket")
                _resourceStore.unsubscribe(_stateMachine.ticketModel);
        }

        _stateMachine.tmpTicketModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET);

        _stateMachine.tmpTicketModel.data.ticketReference = "/cdm/jobTicket/v1/tickets/" + _stateMachine.ticketModel.data.ticketId;

        let ticketResponse = _resourceStore.create("/cdm/jobTicket/v1/tickets", _stateMachine.tmpTicketModel)

        ticketResponse.resolved.connect((future) => {
                                        console.log("Ticket cloned")
                                        //Delete auxiliary ticket model
                                        _stateMachine.tmpTicketModel = null;
                                        successSlot(future)
                                    });
        ticketResponse.rejected.connect((future) => {
                                        //Delete auxiliary ticket model
                                        _stateMachine.tmpTicketModel = null;
                                        console.assert("cloneTicket: failedFunc not exist!")
                                    });
    }

    ///////////////////////////////////////////////////////////////////////////////
    // JobManagement - Create
    ///////////////////////////////////////////////////////////////////////////////
    function requestCloneCopyJobTicket()
    {
        console.log("create Default CopyTicket ");

        //requesting the ticket
        _stateMachine.tmpTicketModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET);

        if(root.launchFrom == SpiceApplication.LaunchFromApp.QUICKSETAPP)
        {
            root.href = QuickSetsUtils.getHrefDetailsFromModal(root.selectedShortcutModel)
            _stateMachine.tmpTicketModel.data.ticketReference = root.href;

            console.log("requestCloneCopyJobTicket using href: "+root.href );
        }
        else
        {
            _stateMachine.tmpTicketModel.data.ticketReference = "defaults/copy";
        }

        let ticketResponse = _resourceStore.create("/cdm/jobTicket/v1/tickets", _stateMachine.tmpTicketModel)

        ticketResponse.resolved.connect(requestTicketSuccess);
        ticketResponse.rejected.connect(requestTicketFailSlot);
    }

    /*
        Slot used by REQUEST_AND_WAIT_FOR_TICKET state when requesting ticket model usign requestDefaultCopyTicketWithSlots
        has been successfully done. It sets ticketModel received to stateMachine.ticketModel and emits ticket.received event
        for state transition
    */
    function requestTicketSuccess(future) {
        if(_stateMachine){
            console.log("requestTicketSuccess");
            _stateMachine.ticketModel = future.get();
            _stateMachine.isTicketModelChanged = false; // ignore tracking OnTicketModelChanged at this state
            console.log("requestTicketSuccess is one touch? : ",_stateMachine.isOneTouchQuickSet)
            printTicketModel(_stateMachine.ticketModel);
            
            if(_stateMachine.isOneTouchQuickSet){
                
                updateScannerMediaSource()
            }
            else{
                _stateMachine.menuDynamicUrl = getSelfUrl()
            }
            if(_stateMachine.isLaunchedFromWidgetOptions){
                console.log("Launch from widget")
                _stateMachine.updateJobTicketWithWidgetFields()
            }

            //UPDATE APP TICKETMODEL
            let ticketResponse = _resourceStore.subscribe(_stateMachine.ticketModel.data.url, true);

            ticketResponse.resolved.connect( (subscriptionFuture) => {
                                    _stateMachine.ticketModel = subscriptionFuture.get();
                                    
                                    if(_stateMachine.isLaunchedFromWidgetOptions)
                                    {
                                        _stateMachine.isTicketModelChanged = true
                                        _stateMachine.updateJobTicketWithWidgetFields()
                                    }
                                    console.log("requestCopyTicketAndSubscribeSuccessSlot - Subscription Done");

                                    //PRINT RECEIVED TICKET
                                    _stateMachine.copyControllerfunctions.printTicketModel( _stateMachine.ticketModel, "ticket on createCopyTicketAndSubscribeSuccessSlot" );
                                    _stateMachine.isTicketIdSubscribeReady = true
                                    //EVENT OF RECEPTION
                                    _stateMachine.submitEvent("ev.ticketReceived");
                                });

            ticketResponse.rejected.connect((future) => {
                                    console.log("requestCopyTicketAndSubscribeSuccessSlot error" + future.error);
                                });
        }
        
    }

    function subscribeForDataChange(bindEachDataChange){
        console.log(" subscribe for each Data Change");
        if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
             
                let future = _resourceStore.subscribe("/cdm/jobTicket/v1/tickets/" + _stateMachine.ticketModel.data.ticketId, true)
                future.resolved.connect((future) => {
                                            if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
                                                _stateMachine.ticketModel = future.get();
                                                _stateMachine.isEditSettingsActionEnabled = true
                                                _stateMachine.menuDynamicUrl = getSelfUrl()
                                                bindEachDataChange( future );
                                            }
                                        });
                future.rejected.connect((future) => {
                                            if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
                                                console.log("getCurrentSendTicket Failed " + future + " error " + future.error);
                                            }
                                        });
        }
    }    

    function connectEachDataChange(future){
        if(_stateMachine.ticketModel){
            _stateMachine.ticketModel.data.src.data.scan.data.colorModeChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.duplexBindingChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSizeChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.mediaTypeChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSourceChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.printQualityChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.src.data.scan.data.mediaSizeChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.printingOrderChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.rotateChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.mediaFamilyChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.collateChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.copiesChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.src.data.scan.data.contentTypeChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.src.data.scan.data.plexModeChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.plexModeChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.src.data.scan.data.pagesFlipUpEnabledChanged.connect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.exposureChanged.connect(function(){_stateMachine.isTicketModelChanged = true;})
            _stateMachine.ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.connect(function(){_stateMachine.isTicketModelChanged = true;})
            _stateMachine.ticketModel.data.pipelineOptions.scaling.yScalePercentChanged.connect(function(){_stateMachine.isTicketModelChanged = true;})
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.pagesPerSheetChanged.connect(function(){_stateMachine.isTicketModelChanged = true;})
            _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleSelectionChanged.connect(function(){_stateMachine.isTicketModelChanged = true;})
            _stateMachine.isTicketIdSubscribeReady = false

        }
        
    }
        
    

    function disconnectEachDataChange(){
        if(_stateMachine.ticketModel){
            _stateMachine.ticketModel.data.src.data.scan.data.colorModeChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.duplexBindingChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSizeChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.mediaTypeChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.mediaSourceChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.printQualityChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.src.data.scan.data.mediaSizeChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.rotateChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.mediaFamilyChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.printingOrderChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.collateChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.copiesChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.src.data.scan.data.contentTypeChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.src.data.scan.data.plexModeChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.dest.data.print.data.plexModeChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.src.data.scan.data.pagesFlipUpEnabledChanged.disconnect(function(){ _stateMachine.isTicketModelChanged = true;});
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.exposureChanged.disconnect(function(){_stateMachine.isTicketModelChanged = true;})
            _stateMachine.ticketModel.data.pipelineOptions.scaling.xScalePercentChanged.disconnect(function(){_stateMachine.isTicketModelChanged = true;})
            _stateMachine.ticketModel.data.pipelineOptions.scaling.yScalePercentChanged.disconnect(function(){_stateMachine.isTicketModelChanged = true;})
            _stateMachine.ticketModel.data.pipelineOptions.data.imageModifications.data.pagesPerSheetChanged.disconnect(function(){_stateMachine.isTicketModelChanged = true;})
            _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleSelectionChanged.disconnect(function(){_stateMachine.isTicketModelChanged = true;})

        }
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

    function constraintDataReady( future )
    {
        if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
            console.log("Constraint Data READY:", future);
            if (_stateMachine) {
                _stateMachine.constraintModel = future.get().data;
            }
        }
    }
    function subscribeForConstraint( ticketId)
    {
        console.log("Subscribe Constraint for ticketId: ", ticketId);
        let constraintFuture = _resourceStore.subscribe("/cdm/jobTicket/v1/tickets/" + ticketId + "/constraints")
        constraintFuture.resolved.connect(constraintDataReady)

        console.debug('subscribing to constraint data')
    }

    function requestTicketFailSlot(future) {
        console.assert("ERROR request default Copy ticket Fail");
        _stateMachine.submitEvent("quitRequested");
    }

    function cloneCopyTicketstate()
    {
        if(_stateMachine.jobInfoModel && _stateMachine.jobState == "ready") {
            if(!_stateMachine.isOneTouchQuickSet){
                console.log("Unsubscribing jobTicket")
                _stateMachine.copyControllerfunctions.disconnectEachDataChange()
                _resourceStore.unsubscribe(_stateMachine.ticketModel);
            }

            _stateMachine.tmpTicketModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET);

            _stateMachine.tmpTicketModel.data.ticketReference = "/cdm/jobTicket/v1/tickets/" + _stateMachine.ticketModel.data.ticketId;

            let ticketResponse = _resourceStore.create("/cdm/jobTicket/v1/tickets", _stateMachine.tmpTicketModel)
            
            ticketResponse.resolved.connect((future) => {
                                        console.log("Ticket cloned")
                                        if(_stateMachine.ticketModel){
                                            _stateMachine.isEditSettingsActionEnabled = false
                                            _stateMachine.ticketModel = future.get();
                                            startJob();
                                            
                                            //Delete auxiliary ticket model
                                            _stateMachine.tmpTicketModel = null;

                                            printTicketModel( _stateMachine.ticketModel );
                                            
                                            subscribeForDataChange(connectEachDataChange)
                                        }
                                        
                                    });
            ticketResponse.rejected.connect((future) => {
                                            //Delete auxiliary ticket model     
                                            _stateMachine.tmpTicketModel = null;
                                            console.assert("cloneTicket: failedFunc not exist!")
                                    });
        }
        else {
            _stateMachine.jobNotReady()
        }

    }
    
    function createDefaultCopyTicket()
    {

        if (_stateMachine.ticketModel !== null)
        {
            console.warn("WARNING! overwriting the previous ticket " + _stateMachine.ticketModel)
            console.warn("WARNING! overwriting the previous ticket " + _stateMachine.ticketModel.data)

        }

        console.log("Creating default ticketModel");

        //requesting the ticket
        _stateMachine.ticketModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET);

        _stateMachine.ticketModel.data.ticketReference = "defaults/copy";

        let ticketResponse = _resourceStore.create("/cdm/jobTicket/v1/tickets", _stateMachine.ticketModel)

        ticketResponse.resolved.connect((future) => {
                                    console.log("ticket resolved " + future.get());
                                    console.log("Succesfully created ticket model:");
                                    _stateMachine.menuDynamicUrl = getSelfUrl()
                                    _stateMachine.copyControllerfunctions.printTicketModel( _stateMachine.ticketModel );
                                    subscribeForConstraint( _stateMachine.ticketModel.data.ticketId);
                                    if ( _stateMachine.continuousCopy )
                                    {
                                        _stateMachine.copyControllerfunctions.createJob(_stateMachine.ticketModel.data.ticketId);
                                    }

                                });

        ticketResponse.rejected.connect((future) => {
                                    console.log("ticketResolveFailed rejected ERROR:" + future.error);
                                    console.info("quitting app..")
                                    _stateMachine.submitEvent("quitRequested");
                                });
    }

    function enterPriorityModeSession()
    {
        _stateMachine.priorityModeSessionModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_PRIORITY_MODE_SESSION);

        _stateMachine.priorityModeSessionModel.data.applicationId = root.appId
        _stateMachine.priorityModeSessionModel.data.behavior = "blockNonPriorityJobs"

        let future = _resourceStore.create("/cdm/jobManagement/v1/priorityModeSessions", _stateMachine.priorityModeSessionModel);
        console.log("Requested create priority mode sessions, waiting for response! " + future);

        future.resolved.connect((future) => {
                                    _stateMachine.priorityModeSessionModel = future.get();
                                    _stateMachine.priorityModeSessionId = _stateMachine.priorityModeSessionModel.data.priorityModeSessionId;
                                    console.log("Entered priority mode session!");
                                });
        future.rejected.connect((future) => {
                                    console.log("Couldn't enter priority mode!");
                                });
    }

    function exitPriorityModeSession()
    {
        if (_stateMachine.priorityModeSessionModel != null){
            _stateMachine.priorityModeSessionModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_PRIORITY_MODE_SESSION);
            _stateMachine.priorityModeSessionModel.url = "/cdm/jobManagement/v1/priorityModeSessions/" + _stateMachine.priorityModeSessionId;

            let future = _resourceStore.destroyResource(_stateMachine.priorityModeSessionModel);
            console.log("Requested destroy priority mode session, waiting for response! " + future);

            future.resolved.connect((future) => {
                                        console.log("Exited priority mode session successfully!");
                                    });
            future.rejected.connect((future) => {
                                        console.log("Couldn't exit priority mode!");
                                    });
        }
    }

    function createJob(ticketId) {
        if (ticketId){
            console.log("createJob: ENTER ticketId:" + ticketId);
            _stateMachine.jobInfoModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_JOB);
            console.log("createJob: _stateMachine.jobInfoModel = ", _stateMachine.jobInfoModel);
            _stateMachine.jobInfoModel.data.ticketId = ticketId;
            _stateMachine.jobInfoModel.data.priorityModeSessionId = _stateMachine.priorityModeSessionId;
            if(_stateMachine.isOneTouchQuickSet){
                _stateMachine.jobInfoModel.data.autoStart = Glossary_1_FeatureEnabled.FeatureEnabled.true_;
            }

            let future = _resourceStore.create("/cdm/jobManagement/v1/jobs", _stateMachine.jobInfoModel);
            console.log("requested create job, waiting for response " + future);

            future.resolved.connect((future) => {
                                        if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
                                            if(_stateMachine.isOneTouchQuickSet){
                                                console.log("createJob: oneTouchCreateJobResolved:");
                                                _stateMachine.oneTouchCreateJobResolved(future);
                                            }
                                            else{
                                                _stateMachine.submitEvent("ev.copyJobCreated")
                                                console.log("createJob: createJobResolvedAndIntializeJob:")
                                                createJobResolvedAndIntializeJob(future)
                                            }
                                        }
                                    });
            future.rejected.connect((future) => {
                                        if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
                                            createJobResolveFailed(future)
                                        }
                                    })
        }
    }

    function createDefaultJob(ticketId, resolvedFunc, failedFunc) {
        console.log("createJob: ENTER id:" + ticketId );
        _stateMachine.jobInfoModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_JOB);
        console.log("createJob: _stateMachine.jobInfoModel = ", _stateMachine.jobInfoModel);
        _stateMachine.jobInfoModel.data.ticketId = ticketId;
        _stateMachine.jobInfoModel.data.priorityModeSessionId = _stateMachine.priorityModeSessionId;
        _stateMachine.jobInfoModel.data.autoStart = Glossary_1_FeatureEnabled.FeatureEnabled.false_;

        let ticketResponse = _resourceStore.create("/cdm/jobManagement/v1/jobs", _stateMachine.jobInfoModel);

        ticketResponse.resolved.connect((future) => {
                                    createJobResolved(future)
                                    if (typeof resolvedFunc !== "undefined")
                                    {
                                        resolvedFunc(future)
                                    }
                                    else
                                    {
                                        console.assert("createJob: resolvedFunc not exist!")
                                    }
                                });
        ticketResponse.rejected.connect((future) => {
                                    createJobResolveFailed(future)
                                    if(typeof failedFunc !== "undefined")
                                    {
                                        failedFunc(future)
                                    }
                                    else
                                    {
                                        console.assert("createJob: failedFunc not exist!")
                                    }
                                });
        console.log("requested create job, waiting for response " + ticketResponse);
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

    function updateCdmTicketModel(resolvedFunc, rejectedFunc)
    {
        if(_stateMachine.ticketModel)
        {
            _stateMachine.ticketId = _stateMachine.ticketModel.data.ticketId

            console.log("updating CDM ticketmodel based on _stateMachine.ticketModel:" + _stateMachine.ticketModel +
                        " in resource_: " + _resourceStore);

            let ticketResponse = _resourceStore.modify(_stateMachine.ticketModel)
            console.log("waiting for Modify result " + ticketResponse);
            ticketResponse.resolved.connect((future) => {
                                        if(_stateMachine.ticketModel){
                                            printTicketModel( _stateMachine.ticketModel );
                                            console.log("ticket Modify Resolved " + future + " status " + future.status);
                                            console.log("setting ticketId in state machine");
                                            resolvedFunc();
                                        }
                                    });
            ticketResponse.rejected.connect((future) => {
                                        console.log("ticket Modify Failed " + future + " error " + future.error);
                                        rejectedFunc();
                                    });
        }
        else
        {
            console.log("ERROR cannot be update because _stateMachine.ticketModel is not defined");
        }
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
        }
        else
        {
            console.log("jobInfoModel: NULL, NOT DEFINED!" );
        }
        console.log("------------------------------------------------------------");
    }

    function createJobResolved(future) {
        console.log("createJobResolved: " + future)
        if (future) {
            console.log("status " + future.status);
            console.log(" error code: " + future.error)
        }
        
        _stateMachine.jobInfoModel = future.get();
        printJobInfoModel( _stateMachine.jobInfoModel );
        console.log("showing the progress...")
    }
    function createJobResolvedAndIntializeJob(future) {
        if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
            console.log("createJobResolved: " + future)
            if (_stateMachine.jobInfoModel) {
                console.log("status " + future.status);
                console.log(" error code: " + future.error)
            }
            
            _stateMachine.jobInfoModel = future.get();
            printJobInfoModel( _stateMachine.jobInfoModel );
            console.log("showing the progress...")

            // Subscribe the job for the job State
            subscribeJob()
            console.log("subscribeJob done...")
        }
    }

    function createJobResolveFailed(future) {
        console.log("createJobResolveFailed: " + future);
        let error = future.error;
        console.log("createJobResolveFailed: job create rejected " + error);
        console.info("quitting app..")
        _stateMachine.submitEvent("quitRequested");
    }

    function intializeJob(future) {
        if (_stateMachine.jobInfoModel.data.state == JobManagement_1_State.State.created) {
            console.log("queryJobResolved: State created, initializing...");
            _stateMachine.jobInfoModel.data.state = JobManagement_1_State.State.initializeProcessing;
            let future = _resourceStore.modify(_stateMachine.jobInfoModel);
            future.resolved.connect((future) => {
                                        if(_stateMachine.jobInfoModel){
                                            queryJobResolved(future)
                                            printJobInfoModel(_stateMachine.jobInfoModel)
                                            _stateMachine.submitEvent("ev.currentAppJobInitialized");
                                        }
                                    });
            future.rejected.connect(_stateMachine.startJobResolvedFailed);
        }
        else {
            console.log("Job is not created state");
            // TODO see what we can do
        }
    }

    function subscribeJob(){
        console.log("copy subscribeJob..enter")
        if(_stateMachine.jobInfoModel && _stateMachine.jobInfoModel.data)
        {
            console.log("copy subscribeJob..url=" + _stateMachine.jobInfoModel.data.url)
            let jobResponse = _resourceStore.subscribe(_stateMachine.jobInfoModel.data.url);
            jobResponse.resolved.connect((future) => {
                                        if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
                                            _stateMachine.subscribeJobResolved(future);
                                        }
                                    });
            jobResponse.rejected.connect((future) => {
                                        if (typeof _stateMachine != "undefined" && _stateMachine.ticketModel) {
                                            _stateMachine.subscribeJobResolvedFailed(future);
                                        }
                                    });
        }
        console.log("copy subscribeJob..exit")
    }

    function subscribeToJob(jobInfoModel, subscribeSucess, subscribeFailed){
        if(jobInfoModel)
        {
            let jobResponse = _resourceStore.subscribe(jobInfoModel.data.url);
            jobResponse.resolved.connect(subscribeSucess);
            jobResponse.rejected.connect(subscribeFailed);
        }
        else
        {
            subscribeFailed();
        }
    }

     function unsubscribeToJob(jobInfoModel)
     {
        console.log("unsubscribeToJob : " + jobInfoModel);

        if(jobInfoModel)
        {
            _resourceStore.unsubscribeURL(jobInfoModel.data.url);
        }
    }

    function startJob(){
        if(_stateMachine.jobInfoModel && _stateMachine.jobState == "ready"){
            console.log("queryJobResolved: State ready, starting...");
            _stateMachine.jobInfoModel.data.state = JobManagement_1_State.State.startProcessing;
            _stateMachine.cancelJobController.lastJobId = _stateMachine.jobInfoModel.data.jobId
            let jobStartResponse = _resourceStore.modify(_stateMachine.jobInfoModel);
            jobStartResponse.resolved.connect(_stateMachine.startJobResolved);
            jobStartResponse.rejected.connect(_stateMachine.startJobResolvedFailed);
        }
        else {
            _stateMachine.jobNotReady()
        }
    }

    function previewJob(funcResolve, funcReject){
        if(_stateMachine.jobInfoModel && _stateMachine.jobState == "ready"){
            console.log("queryJobResolved: State ready, starting...");
            _stateMachine.jobInfoModel.data.state = JobManagement_1_State.State.prepareProcessing;
            _stateMachine.cancelJobController.lastJobId = _stateMachine.jobInfoModel.data.jobId
            _stateMachine.inPreviewState = true
            let jobStartResponse = _resourceStore.modify(_stateMachine.jobInfoModel);
            jobStartResponse.resolved.connect(funcResolve);
            jobStartResponse.rejected.connect(funcReject);
        }
        else {
            _stateMachine.jobNotReady()
        }
    }

    function clearJobInfo(){
        if(_stateMachine.jobInfoModel){

            console.log("Unsubscribe jobInfo")

            // job is not in ready state
            _stateMachine.isJobInReadyState = false
            if(_stateMachine.isJobSubscribed){
                _stateMachine.jobInfoModel.data.stateChanged.disconnect(_stateMachine.subscribeStateChanged);
                _resourceStore.unsubscribe(_stateMachine.jobInfoModel)
            }
            
            console.log("queryJobResolved: State created, cancelling...");
            if(_stateMachine.jobInfoModel.data.state != JobManagement_1_State.State._undefined_){
                _stateMachine.previewJobId = ""
                _stateMachine.jobInfoModel.data.state = JobManagement_1_State.State.cancelProcessing;
                let future = _resourceStore.modify(_stateMachine.jobInfoModel);
            }
            else
            {
                _stateMachine.jobInfoModel.destroy()
                _stateMachine.jobInfoModel = null
            }
        }
    }

    function queryJobResolved(future)
    {
        console.log("queryJobResolved->")
        console.log("queryJobResolved: " + future + " status " + future.status);
        console.log("queryJobResolved: obtained " + _stateMachine.jobInfoModel);
        console.log("queryJobResolved<--")
        
    }

    function queryJobResolvedFailed(future)
    {
        console.log("queryJobResolvedFailed-->")
        console.log("queryJobResolvedFailed: " + future);
        let error = future.error;
        console.log("queryJobResolvedFailed: job query rejected " + error);
        if (error == IResourceStore.OperationResult.ERROR_RESOURCE_NOT_FOUND)
        {
            //job not found - exit workflow!
            console.log("ERROR! jobId not found. Exit the workflow");
        }
        console.log("queryJobResolvedFailed<--")
        _stateMachine.submitEvent("ev.copy.failed")
    }
    function getMediaConfiguration() {
        let ticketResponse = _resourceStore.get("/cdm/media/v1/configuration")

        ticketResponse.resolved.connect((future) => {
                                    console.log("media configuration resolved " + future.get());
                                    _stateMachine.mediaConfiguration = future.get();
                                });

        ticketResponse.rejected.connect((future) => {
                                    console.log("media configuration rejected ERROR:" + future.error);
                                    console.info("quitting app..")
                                    _stateMachine.submitEvent("quitRequested");
                                });
    }


    function initializeQuickSetView(appName){

        QuickSetsUtils.initializeTheQuickSetView(appName, //AppName
                                                 root.appId, //ShortcutId
                                                 root.href,  // href link
                                                 _stateMachine, // Handle QuickSet related property
                                                 ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET, // ResourceStore Identifier
                                                 Glossary_1_FeatureEnabled.FeatureEnabled.false_,// Information for copyAllowed key in QuickSet (to be false)
                                                 Shortcut_1_Type.Type.singleJob); // its only for single Job

    }


    function subscribeScannerStatus(){
        let future = _resourceStore.subscribe("/cdm/scan/v1/status")

        future.resolved.connect((future) => {
                                    console.log("scanner status resolved " + future.get());
                                    _stateMachine.scannerStatus = future.get();
                                    _stateMachine.scannerState = _stateMachine.scannerStatus.data.scannerState
                                    console.log("scanner status: version " + _stateMachine.scannerStatus.data.version);
                                    console.log("scanner flatbed state " + _stateMachine.scannerStatus.data.scannerState);
                                    console.log("scanner flatbed error " + _stateMachine.scannerStatus.data.scannerError);
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
            _stateMachine.scannerStatus.data.flatbed.data.stateChanged.disconnect(updateScannerMediaSource);
            _stateMachine.scannerStatus.data.adf.data.stateChanged.disconnect(updateScannerMediaSource); 
            _resourceStore.unsubscribe(_stateMachine.scannerStatus)               
        }

    }

    function updateScannerStatus(){
        if(_stateMachine.scannerStatus){

            console.log("Scanner state changed" + Number(_stateMachine.scannerStatus.data.scannerState))
            _stateMachine.scannerState = _stateMachine.scannerStatus.data.scannerState
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
            inputMediaSource = "adf";
            _stateMachine.isFlatbedLoaded = false
        }
        else if (flatbedAvailable && _stateMachine.scannerStatus.data.adf.data.state == Scan_1_ScanAdfStateType.ScanAdfStateType.ScannerAdfEmpty)
        {
            inputMediaSource = "flatbed";
            _stateMachine.isFlatbedLoaded = true
        }
        if(!_stateMachine.isFlatbedLoaded && !_stateMachine.isDuplexSupported){
            updatePlexMoode()
        }

        console.log("scanner source selected:" + inputMediaSource);

        if (_stateMachine.ticketModel && _qmlUtils.getEnumValueAsString(_stateMachine.ticketModel.data.src.data.scan.data,"mediaSource") != inputMediaSource){
            _stateMachine.ticketModel.data.src.data.scan.data.mediaSource = inputMediaSource
            console.log("Updating scannerStatus and inputMediaSource")
            updateJobTicket()
        }
    }

    function updatePlexMoode(){
        if(_stateMachine.ticketModel && _stateMachine.ticketModel.data.src.scan.plexMode == Glossary_1_PlexMode.PlexMode.duplex){
            console.log("Setting PlexMode to simplex")
            _stateMachine.ticketModel.data.src.scan.plexMode = Glossary_1_PlexMode.PlexMode.simplex
            updateJobTicket()
        }
    }

    function updateJobTicket(){
        if(_stateMachine.ticketModel){
            console.log("Updating JobTicket")
            let future = _resourceStore.modify(_stateMachine.ticketModel)
            console.log("waiting for Modify result " + future);
            future.resolved.connect((future) => {
                                        console.log("ticket Modify Resolved " + future + " status " + future.status);
                                         _stateMachine.submitEvent("ev.ticketupdated");
                                    });
            future.rejected.connect((future) => {
                                        console.log("ticket Modify Failed " + future + " error " + future.error);
                                        _stateMachine.submitEvent("quitRequested");
                                    });

        }
        else
        {
            console.log("updateJobTicket Updating JobTicket cannot be done");
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


     function subscribeConstraintWithCallbacks( ticketId, successSlot, failSlot)
     {
         let url = subscribe_constraints_url.arg(ticketId);

         console.log("subscribeConstraintWithCallbacks url:" + url);

         let subcribeRespose = _resourceStore.subscribe( url );

         subcribeRespose.resolved.connect(successSlot);
         subcribeRespose.rejected.connect(failSlot);
     }

     function createInstanceOfJobTicket()
     {
         console.log("createInstanceOfJobTicket");

         return _resourceStore.createInstance(ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET);
     }

     function createInstanceOfJobInfoModel()
     {
         console.log("createInstanceOfJobInfoModel");

         return _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_JOB);
     }

     function subscribeScannerStatusWithCallbacks( successSlot, failSlot)
     {
         console.log("subscribeScannerStatusWithCallbacks");

         let subcribeRespose = _resourceStore.subscribe( scan_status_url )

         subcribeRespose.resolved.connect(successSlot);
         subcribeRespose.rejected.connect(failSlot);
     }

     function createCopyTicketWithSlots(successSlot, failSlot)
     {
         console.log("createCopyTicketWithSlots");

         let ticketModel = createInstanceOfJobTicket();
         ticketModel.data.ticketReference = copy_ticket_reference;

         createTicketWithSlots(ticketModel, successSlot, failSlot);
     }

    // This function does the same than createCopyTicketWithSlots in this component
    // but it makes easier to understand what is expected
    // when you call it from the state machine.
    function createCopyTicketAndSubscribeWithSlots(successSlot, failSlot)
    {
        console.log("createCopyTicketAndSubscribeWithSlots");

        _stateMachine.tmpTicketModel = createInstanceOfJobTicket();

        _stateMachine.tmpTicketModel.data.ticketReference = copy_ticket_reference;
        
        createTicketWithSlots(_stateMachine.tmpTicketModel, successSlot, failSlot);
    }

     function createTicketWithSlots( ticketModel, successSlot, failSlot )
     {
         console.log("createTicketWithSlots");

         let creationResponse = _resourceStore.create( job_ticket_url, ticketModel)

         creationResponse.resolved.connect(successSlot);
         creationResponse.rejected.connect(failSlot);
     }

     function buildCloneTicketReference( ticketId )
     {
         return clone_ticket_reference + ticketId;
     }

     //maybe ticketClone is not needed and we obtained from future
     function cloneTicket( ticketToBeCloned, ticketClone, successSlot, failSlot )
     {
         console.assert( ticketToBeCloned !== undefined );
         console.assert( ticketClone !== undefined );

         console.log("cloneTicket original: " + ticketToBeCloned.data.ticketId +
                                   " clone: " + ticketClone.data.ticketId);

         console.log("buildCloneTicketReference:" + buildCloneTicketReference( ticketToBeCloned.data.ticketId) );
         //let ticketModel = _resourceStore.createInstance(ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET);

         ticketClone.data.ticketReference = buildCloneTicketReference( ticketToBeCloned.data.ticketId);

         let cloneResponse = _resourceStore.create(job_ticket_url, ticketClone)

         cloneResponse.resolved.connect(successSlot);
         cloneResponse.rejected.connect(failSlot);
     }


     function createJobWithSlots(jobInfoModel, successSlot, failSlot)
     {
        console.log("createJobWithSlots jobInfoModel:" + jobInfoModel);

         //Prerequisites: For create jobInfoModel it must be relatd to a concrete jobTicketId
         console.assert( jobInfoModel !== null );
         console.assert( jobInfoModel.data.ticketId !== "" );

         console.log("createJobInfoModelWithSlots jobInfoModel:" + jobInfoModel + " with jobticket reference:" + jobInfoModel.data.ticketId);


         let creationResponse = _resourceStore.create(job_management_url, jobInfoModel);
         creationResponse.resolved.connect(successSlot);
         creationResponse.rejected.connect(failSlot);

     }

     function executeJobPathing( jobInfoModel )
     {
         console.assert( jobInfoModel.data !== undefined );

         //ToDo, for some reason "===" comparison doesn't work for this type
         if (jobInfoModel.data.state == JobManagement_1_State.State.ready)
         {
             //Print before execute patching for print current values of jobInfoModel
             printPatching(jobInfoModel, JobManagement_1_State.State.startProcessing)

             jobInfoModel.data.state = JobManagement_1_State.State.startProcessing;
             let jobStartResponse = _resourceStore.modify(jobInfoModel);
             //jobStartResponse.resolved.connect(startJobResolved);
             //jobStartResponse.rejected.connect(startJobResolvedFailed);//If any problem in future enabled them
         }
         else if (jobInfoModel.data.state == JobManagement_1_State.State.created)
         {
             //Print before execute patching for print current values of jobInfoModel
             printPatching(jobInfoModel, JobManagement_1_State.State.initializeProcessing)

             jobInfoModel.data.state = JobManagement_1_State.State.initializeProcessing;
             let jobInitializeResponse = _resourceStore.modify(jobInfoModel);
             jobInitializeResponse.resolved.connect(executeJobPathing);//recursive asynch
             //jobInitializeResponse.rejected.connect(queryJobResolvedFailed); //If any problem in future enabled it
         }
         else
         {
             //This state has not patching state related
         }
     }

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

    function executeJobPatchingMultipage( jobInfoModel )
    {
        console.assert( jobInfoModel.data !== undefined );

        //ToDo, for some reason "===" comparison doesn't work for this type

        if (jobInfoModel.data.state == JobManagement_1_State.State.processing)
        {
            //Print before execute patching for print current values of jobInfoModel
            printPatching(jobInfoModel, JobManagement_1_State.State.prepareProcessing)

            jobInfoModel.data.state = JobManagement_1_State.State.prepareProcessing;
            let jobStartResponse = _resourceStore.modify(jobInfoModel);
            
            jobStartResponse.resolved.connect(_stateMachine.prepareProcessingResolved);
            // jobStartResponse.rejected.connect(startJobResolvedFailed);//If any problem in future enabled them
        }
        else if (jobInfoModel.data.state == JobManagement_1_State.State.ready)
        {
            //Print before execute patching for print current values of jobInfoModel
            printPatching(jobInfoModel, JobManagement_1_State.State.prepareProcessing)

            jobInfoModel.data.state = JobManagement_1_State.State.prepareProcessing;
            let jobStartResponse = _resourceStore.modify(jobInfoModel);
            
            jobStartResponse.resolved.connect(_stateMachine.prepareProcessingResolved);
            //jobStartResponse.rejected.connect(startJobResolvedFailed);//If any problem in future enabled them
        }
        else if (jobInfoModel.data.state == JobManagement_1_State.State.created)
        {
            //Print before execute patching for print current values of jobInfoModel
            printPatching(jobInfoModel, JobManagement_1_State.State.initializeProcessing)

            jobInfoModel.data.state = JobManagement_1_State.State.initializeProcessing;
            let jobInitializeResponse = _resourceStore.modify(jobInfoModel);
        }
        else
        {
            //This state has not patching state related
            console.log("executeJobPatchingMultipage -- Unhandled state: " + Number(jobInfoModel.data.state));
        }
    }

    function patchStartProcessing( jobInfoModel )
    {
        //Print before execute patching for print current values of jobInfoModel
        printPatching(jobInfoModel, JobManagement_1_State.State.startProcessing)

        jobInfoModel.data.state = JobManagement_1_State.State.startProcessing;
        let jobInitializeResponse = _resourceStore.modify(jobInfoModel);
    }

     function printPatching( jobInfoModel, patchToState)
     {
         console.log("=======EXECUTIN PATCHING=============================================")
         console.log("== jobInfoModel:"  + jobInfoModel);
         console.log("== jobId: " + jobInfoModel.data.jobId);
         console.log("== PATCHING from: " + jobStateToString(jobInfoModel.data.state) +
                                  " to: " + jobStateToString(patchToState));
     }

    function getJobTicketCapabilities(){
        let future = _resourceStore.get("/cdm/jobTicket/v1/capabilities")

        future.resolved.connect(resolvedJobTicketCapabilities);
        future.rejected.connect(rejectedJobTicketCapabilities);
    }

    function resolvedJobTicketCapabilities(future){
        console.log("Getting the jobTicket capabilities model")
        let jobTicketCapabilities = future.get()

        //Check whether multipage preview is supported or not
        // TODO: this logic will be updated, once we have the jobTicket Capabilities available for preview
        if(jobTicketCapabilities.data.print.collateSupported == Glossary_1_FeatureEnabled.FeatureEnabled.true_ && _stateMachine.isMdfCapabilities()){
            console.log("Set the multipagePreview supported true")
            _stateMachine.isMultiPagePreviewSupported = true
        }
        else{
            _stateMachine.isMultiPagePreviewSupported = false
        }

        if (jobTicketCapabilities.data.print.colorModeSupported == Glossary_1_FeatureEnabled.FeatureEnabled.true_){
            console.log("Set the isColorPrintSupported() : supported");
            _stateMachine.isColorPrintSupported = true
        }
        else{
            console.log("Set the isColorPrintSupported() : not supported");
            _stateMachine.isColorPrintSupported = false
        }
    }

    function rejectedJobTicketCapabilities(future){
        console.log("jobticket capabilities endpoint not available")
    }
    
     function jobStateToStringId(state)
     {
         let stateString;

         switch ( Number( state ) )
         {
         case JobManagement_1_State.State.created:
             stateString =  "StringIds.cJobStateTypeCreated";
             break;
         case JobManagement_1_State.State.ready:
             stateString =  "StringIds.cReady";
             break;
         case JobManagement_1_State.State.processing:
             stateString =  "StringIds.cJobStateTypeProcessing";
             break;
        case JobManagement_1_State.State.prepareProcessing:
             stateString =  "StringIds.cJobStateTypeProcessing";
             break;
         case JobManagement_1_State.State.startProcessing:
             stateString =  "StringIds.cJobStateTypeProcessing";
             break;
         case JobManagement_1_State.State.initializeProcessing:
             stateString =  "StringIds.cJobStateTypeInitializing";
             break;
         case JobManagement_1_State.State.cancelProcessing:
             stateString =  "StringIds.cJobStateTypeCanceling";
             break;
         case JobManagement_1_State.State.resumeProcessing:
             stateString =  "StringIds.cJobStateTypeResuming";
             break;
         case JobManagement_1_State.State.pauseProcessing:
             stateString =  "StringIds.cJobStateTypePausing";
             break;
         case JobManagement_1_State.State.waiting:
             stateString =  "StringIds.cJobStateTypePending";
             break;
         case JobManagement_1_State.State.paused:
             stateString =  "StringIds.cJobStateTypePaused";
             break;
         case JobManagement_1_State.State.completed:
             stateString =  "StringIds.cJobStateTypeCompleted";
             break;
         default:
             stateString =  "StringIds.cUnknown";
             break;
         }

         return stateString;
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
         ejectResponse.rejected.connect((future) => { console.error("ejectResponse: status request Resolved REJECTED " + future.error);});
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

     function logFromState( message )
     {
         console.log("logFromState: "+ message );
     }

    function setScannerCapabilities()
    {
        if (_stateMachine.scannerStatus)
        {
            if (_stateMachine.scannerStatus.data.adf && _stateMachine.scannerStatus.data.adf.data)
            {
                _stateMachine.setScannerCapabilities(_stateMachine.capabilityAdf);
            }
            else if(_stateMachine.scannerStatus.data.mdf && _stateMachine.scannerStatus.data.mdf.data)
            {
                _stateMachine.setScannerCapabilities( _stateMachine.capabilityMdf);
            }
        }
        else{
            console.assert("ERROR: ScannerStatus not found");
        }
        getJobTicketCapabilities()
    }

    function getInsertPageImage()
    {
        return  _qmlUtils.getWorkflowResourceUrl("InsertPageScanner", "images");
    }

    function getPrePreviewAnimation( )
    {
        if( !root.smallVersion  && _stateMachine.isMdfCapabilities())
        {
            return getInsertPageImage();
        }
        else
        {
            return "";
        }
    }
}
