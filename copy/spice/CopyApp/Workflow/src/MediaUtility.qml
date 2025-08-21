import QtQml 2.15
import spiceGuiCore 1.0
import spiceuxToastSystem 1.0

QtObject {
    id : root
    property ISpiceModel userdefinedConfigurationModel: null
    property string userDefinedConfigurationurl : "/cdm/mediaProperty/v2/mediaConfigs"

    function subscribeToUserDefinedMediaConfigurationModel(userDefinedmediaConfigurationModelSuccess, UserDefinedConfigurationModelFailed = onMediaInfoFailed)
    {
        function onUserDefinedConfigurationSuccess(future)
        {
            root.userdefinedConfigurationModel = future.get()
            userDefinedmediaConfigurationModelSuccess()
        }
        subscribeToMediaInfo(root.userDefinedConfigurationurl, onUserDefinedConfigurationSuccess, UserDefinedConfigurationModelFailed)
    }

    function subscribeToMediaInfo(url, mediaInfoSuccess, mediaInfoFailed)
    {
        let future = _resourceStore.subscribe(url)
        future.resolved.connect(mediaInfoSuccess)
        future.rejected.connect(mediaInfoFailed)
    }

    function onMediaInfoFailed(future)
    {
        let error = future.error
        console.log("MediaUtility: media info retrieve failed with error:", error)
    }

    function isUserDefinedMediaType(mediaTypeIdCDMenum)
    {
         console.log("check isUserDefinedMediaType ",mediaTypeIdCDMenum )
         switch(mediaTypeIdCDMenum)
         {
            case "com_dot_hp_dot_usertype_dash_1":
            case "com_dot_hp_dot_usertype_dash_2":
            case "com_dot_hp_dot_usertype_dash_3":
            case "com_dot_hp_dot_usertype_dash_4":
            case "com_dot_hp_dot_usertype_dash_5":
            case "com_dot_hp_dot_usertype_dash_6":
            case "com_dot_hp_dot_usertype_dash_7":
            case "com_dot_hp_dot_usertype_dash_8":
            case "com_dot_hp_dot_usertype_dash_9":
            case "com_dot_hp_dot_usertype_dash_10":
                return true
            default:
                return false
         }
    }

    function convertToCDMString(mediaTypeIdCDMenum)
    {
        //let mediaTypeIdCDMenum = _menuResource.enumStringFromValue("dune::spice::glossary_1::MediaType::MediaType", mediaTypeId)
        switch(mediaTypeIdCDMenum)
        {
        case "com_dot_hp_dot_usertype_dash_1":
            return "com.hp.usertype-1"
        case "com_dot_hp_dot_usertype_dash_2":
            return "com.hp.usertype-2"
        case "com_dot_hp_dot_usertype_dash_3":
            return "com.hp.usertype-3"
        case "com_dot_hp_dot_usertype_dash_4":
            return "com.hp.usertype-4"
        case "com_dot_hp_dot_usertype_dash_5":
            return "com.hp.usertype-5"
        case "com_dot_hp_dot_usertype_dash_6":
            return "com.hp.usertype-6"
        case "com_dot_hp_dot_usertype_dash_7":
            return "com.hp.usertype-7"
        case "com_dot_hp_dot_usertype_dash_8":
            return "com.hp.usertype-8"
        case "com_dot_hp_dot_usertype_dash_9":
            return "com.hp.usertype-9"
        case "com_dot_hp_dot_usertype_dash_10":
            return "com.hp.usertype-10"
        default:
            return mediaTypeIdCDMenum
        }
    }

}