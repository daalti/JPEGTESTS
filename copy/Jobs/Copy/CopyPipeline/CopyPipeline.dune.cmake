DUNE_ADD_COMPONENT()
DUNE_LINK_LIBRARIES(
    framework/component
    framework/core/uuid
    job/Job
    job/JobService
    job/PipeObject
    job/PipeQueue
    job/ResourceService
    job/types
    job/JobTicketHandler
    imaging/types
    imaging/color/types
    imaging/PipeObjects/ImageContainer
    imaging/Resources/MarkingFilter
    imaging/Resources/LayoutFilter
    imaging/Resources/PageAssembler
    imaging/Resources/ImagePersister
    imaging/Resources/ImageRetriever
    imaging/Resources/ImageProcessor
    imaging/PipelineMemoryClientFactory
    imaging/RasterFormatSelectorFactory
    imaging/color/ColorDirector
    scan/Resources/ScanDevice
    scan/Resources/IPADevice
    print/Resources/PrintDevice
    copy/Jobs/Copy
    scan/Jobs/Scan
    print/Resources/RtpFilter)

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