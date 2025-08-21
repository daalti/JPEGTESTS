import QtQml 2.15
import spiceGuiCore 1.0
QtObject{

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
            settingEnabled = (validator.disabled.value === _stateMachine.Glossary_1_FeatureEnabled.FeatureEnabled.false_);
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

    function isDuplexing() {
        if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null){
            return !(_stateMachine.ticketModel.data.dest.print.plexMode == Glossary_1_PlexMode.PlexMode.simplex)
        }
        return false
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
            let scalingEnabled = _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleSelection != JobTicket_1_Scaling_ScaleSelection.ScaleSelection.none &&
                _stateMachine.ticketModel.data.pipelineOptions.scaling.scaleSelection != JobTicket_1_Scaling_ScaleSelection.ScaleSelection.fitToPage
            let inputMediaSizeA3A4 = _stateMachine.ticketModel.data.src.scan.mediaSize == Glossary_1_MediaSize.MediaSize.com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_a4_dash_a3
            let inputMediaSizeLetterLegal = _stateMachine.ticketModel.data.src.scan.mediaSize == Glossary_1_MediaSize.MediaSize.com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_legal
            let inputMediaSizeLetterLedger = _stateMachine.ticketModel.data.src.scan.mediaSize == Glossary_1_MediaSize.MediaSize.com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_ledger            
            if(scalingEnabled || inputMediaSizeA3A4 || inputMediaSizeLetterLegal || inputMediaSizeLetterLedger){
                return false
            }
            else{
                return true
            }
        }
        
        return true
    }

    function isOutputScaleEnabled(){
        if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null){
            let pagesPerSheetEnabled = _stateMachine.ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet != JobTicket_1_PagesPerSheet.PagesPerSheet.oneUp
            let inputMediaSizeA3A4 = _stateMachine.ticketModel.data.src.scan.mediaSize == Glossary_1_MediaSize.MediaSize.com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_a4_dash_a3
            let inputMediaSizeLetterLegal = _stateMachine.ticketModel.data.src.scan.mediaSize == Glossary_1_MediaSize.MediaSize.com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_legal
            let inputMediaSizeLetterLedger = _stateMachine.ticketModel.data.src.scan.mediaSize == Glossary_1_MediaSize.MediaSize.com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_ledger            
            if(pagesPerSheetEnabled || inputMediaSizeA3A4 || inputMediaSizeLetterLegal || inputMediaSizeLetterLedger){
                return false
            }
            else{
                return true
            }
        }

        return true
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

    function isMdf()
    {
        return _stateMachine.scannerStatus && _stateMachine.scannerStatus.data.mdf !== null;
    }

    function isFlow20Supported()
    {
        let returnVal = false;
        if(_stateMachine.scannerStatus && _stateMachine.scannerStatus.data.adf)
        {
            console.debug("isFlow20Supported::Flavor: " + _stateMachine.scannerStatus.data.adf.data.flavor);
            if(_stateMachine.scannerStatus.data.adf.data.flavor == "valiant" ||
               _stateMachine.scannerStatus.data.adf.data.flavor == "growlerp" ||
               _stateMachine.scannerStatus.data.adf.data.flavor == "igrowler" ||
               _stateMachine.scannerStatus.data.adf.data.flavor == "iprowler")
            {
                returnVal = true;
            }
        }
        return returnVal
    }

    function isStapleMounted()
    {
        let retVal = false;
        if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null)
        {
             if(findValidatorForConstraint("dest/print/stapleOption")) 
            {
                retVal = true;
            }
        }
        return retVal;
    }

    function isPunchMounted()
    {
        let retVal = false;
        if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null)
        {
            if(findValidatorForConstraint("dest/print/punchOption"))
            {
                retVal = true;
            }
        }
        return retVal
    }

    function isFoldMounted()
    {
        let retVal = false;
        if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null)
        {
            if(findValidatorForConstraint("dest/print/foldOption"))
            {
                retVal = true;
            }
        }
        return retVal
    }

    function isStampEnabled()
    {
        let returnVal = false;
        let stampLocations = [
            "stampTopLeft",
            "stampTopCenter",
            "stampTopRight",
            "stampBottomLeft",
            "stampBottomCenter",
            "stampBottomRight"
        ];

        for (let i = 0; i < stampLocations.length; i++) {
            let stampLocation = stampLocations[i];
            let stampTicket = _stateMachine.ticketModel.data.pipelineOptions.data[stampLocation].data;

            if (stampTicket) {
                if (stampTicket.policy ===  Overlay_1_StampPolicy.StampPolicy.guided) {
                    returnVal = true;
                    break
                }
                for (let i = 0; i < stampTicket.stampContent.count; i++) {
                    let item = stampTicket.stampContent.get(i);
                    let value = _menuResource.enumStringFromValue("dune::spice::overlay_1::StampType::StampType", item.data.stampId);

                    if (value !== "none") {
                        returnVal = true;
                        break
                    }
                }
            }   
        }

        return returnVal
    }

    function isOutputDestinationEnabled()
    {
         if(typeof _stateMachine.ticketModel != "undefined" && _stateMachine.ticketModel != null)
         {
             let validator = findValidatorForConstraint("dest/print/mediaDestination");
             if(null != validator && 1 < validator.options.count)
             {
                return true
             }
             return false
         }
         return false
    }
}