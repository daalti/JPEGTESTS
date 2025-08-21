import QtQml 2.15
import spiceGuiCore 1.0

// This object is mainly used to request if a setting must to be displayed based on config files    
QtObject {
    id: checkCopyMoreOptionAvailability

    // Main function to check availablity of a Copy Setting
    function checkAvailability(settingName) {

        // Return true directly if there is not any list or items on list
        if(!_copySettingOptionListAvailability ||
            (!!_copySettingOptionListAvailability && _copySettingOptionListAvailability.length === 0))
        {
            return true
        }

        // Setting must to have the same name on CopyAppWorkflow.csf and origin used as consult
        let result = false
        for(var i = 0; i < _copySettingOptionListAvailability.length; ++i)
        {
            if(_copySettingOptionListAvailability[i] === settingName)
            {
                result = true
                break;
            }
        }

        // return result of search on list
        return result
    }  
}