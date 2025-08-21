DUNE_ADD_FLAVOR()
DUNE_LINK_LIBRARIES(
    framework/component
    framework/resources/configuration
    framework/underware/Interpreter
    job/JobManager
    job/JobServiceManager
    job/ResourceManager
    print/engine
    scan/Jobs/Scan/ScanPipeline
    copy/Jobs/Copy/JobService
    scan/scanningsystem
    imaging/asset/ImagingAttributeManager
    print/IntentsManager
    localization/LocaleProvider)
    DUNE_INCLUDE_DIRECTORIES(PRIVATE ${DUNE_BASE_PATH}/copy/Jobs/Copy/JobService/inc)

    if(DUNE_JPEG_HARDWARE_AVAILABLE)
        message("[CopyPipelineService] Jpeg hardware is available")
        DUNE_SET_CFLAGS(-DJPEG_HARDWARE_AVAILABLE)
    endif()
    if(DUNE_JPEG_DECODER_YCC_RGB_CONVERSION)
        message("[CopyPipelineService] Jpeg decoder YCC_RGB conversion is available")
        DUNE_SET_CFLAGS(-DJPEG_DECODER_YCC_RGB_CONVERSION)
    else()
        message("[CopyPipelineService] Jpeg decoder YCC_RGB conversion is NOT available")
    endif()
    if(${DUNE_INCLUDE_EFIVAR})
        DUNE_SET_CFLAGS(-DEFIVAR_EXIST)
    endif()

    DUNE_ADD_GTEST(framework/component/TestingUtil
                    print/Jobs/Print)

