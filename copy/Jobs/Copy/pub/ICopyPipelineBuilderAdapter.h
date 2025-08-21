#ifndef DUNE_COPY_JOBS_COPY_ICOPY_PIPELINE_BUILDER_ADAPTER_H
#define DUNE_COPY_JOBS_COPY_ICOPY_PIPELINE_BUILDER_ADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   ICopyPipelineBuilderAdapter.h
 * @date   28 Sept 2022 
 * @brief  Copy pipelines builder adapter interface
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IColorDirector.h"
#include "IImagePersister.h"
#include "IImageProcessor.h"
#include "IIntentsManager.h"
#include "ILayoutFilter.h"
#include "IMarkingFilter.h"
#include "IMedia.h"
#include "IMediaAttributes.h"
#include "IPageAssembler.h"
#include "IPrintDevice.h"
#include "IPrintIntentsFactory.h"
#include "IRenderingRequirements.h"
#include "IResourceManagerClient.h"
#include "IResourceService.h"
#include "IRtpFilter.h"
#include "IScanDevice.h"
#include "IIPADevice.h"
#include "JobFrameworkBaseTypes.h"
#include "MediaSizeId_generated.h"
#include "IDeviceInfo.h"
#include "INetworkManager.h"
#include "IImageImporter.h"


namespace dune { namespace job {
    class IJobQueue;
}}
namespace dune { namespace print { 
namespace engine {
    class IPrint;
    class IMediaInfo;
    class ICapabilitiesFactory;
}
namespace mediaHandlingAssets {
    class IMediaHandlingSettings;
    class IMediaHandlingMgr;
}}}

namespace dune { namespace copy { namespace Jobs { namespace Copy {

struct ServicesPackage
{
    dune::job::IResourceManagerClient*              resourceManager{nullptr};
    dune::scan::Resources::IScanDevice*             scanDeviceService{nullptr};
    dune::imaging::Resources::IImagePersister*      imagePersister{nullptr};
    dune::job::IResourceService*                    imageRetrieverService{nullptr};
    dune::imaging::Resources::IMarkingFilter*       markingFilterService{nullptr};
    dune::imaging::Resources::ILayoutFilter*        layoutFilterService{nullptr};
    dune::imaging::Resources::IPageAssembler*       pageAssembler{nullptr};
    dune::print::Resources::IPrintDevice *          printDevice{nullptr};
    dune::print::engine::IPrint*                    printEngine{nullptr};
    dune::print::engine::IPrintIntentsFactory*      printIntentsFactory{nullptr};
    dune::print::engine::ICapabilitiesFactory*      engineCapabilitiesFactory{nullptr};
    dune::imaging::color::IColorDirector*           colorDirector{nullptr};
    dune::imaging::Resources::IImageProcessor*      imageProcessor{nullptr};
    dune::print::engine::helpers::IRenderingRequirements* renderingRequirements{nullptr};
    dune::imaging::asset::IMediaAttributes*         mediaAttributes{nullptr};
    dune::job::IResourceService*                    rtpFilterService{nullptr};
    dune::print::engine::IMedia*                    mediaInterface{nullptr};
    dune::job::IIntentsManager*                   intentsManager{nullptr};
    dune::print::mediaHandlingAssets::IMediaHandlingSettings *mediaHandlingSettings{nullptr};
    dune::print::engine::IMediaInfo                 *mediaInfo{nullptr};
    dune::print::mediaHandlingAssets::IMediaHandlingMgr *mediaHandlingMgr{nullptr};
    dune::scan::Resources::IIPADevice*              ipaDeviceService{nullptr};
    dune::job::IJobQueue                            *jobQueue{nullptr};
    dune::admin::deviceinfo::IDeviceInfo*            deviceInfo{nullptr};
    dune::io::net::core::INetworkManager*            networkManager{nullptr};
    dune::imaging::Resources::IImageImporter*        imageImporter{nullptr};
};

/**
 * @class ICopyPipelineBuilderAdapater
 * @brief Copy pipeline builder adapter Interface
 * 
 */
class ICopyPipelineBuilderAdapter
{
public:

    struct MaxLengthConfig
    {
    u_int32_t                                         scanMaxCm;
    u_int32_t                                         jpegMaxLines;
    u_int32_t                                         tiffMaxMb;
    u_int32_t                                         pdfMaxCm;
    u_int32_t                                         pdfaMaxCm;
    u_int32_t                                         longPlotMaxCm;
    };

    enum class Product
    {
    HOME_PRO,
    LFP,
    ENTERPRISE
    };

    // Get if we are in a preScan job or not
    virtual bool isPreScanJob() = 0;

    // Get default media size
    virtual dune::imaging::types::MediaSizeId getDefaultMediaSize() = 0;
    
    //Get  prescanned width and heigth
    virtual uint32_t getPrescannedWidth() = 0;
    virtual uint32_t getPrescannedHeight() = 0;

    //Get preprint configuration
    virtual ICopyPipelineBuilderAdapter::Product getPrePrintConfiguration() = 0;

    //Get segment type
    virtual dune::job::SegmentType getSegmentType() = 0;

    //Get max length configuration
    virtual ICopyPipelineBuilderAdapter::MaxLengthConfig getMaxLengthConfig() = 0;
};

}}}} // DUNE_COPY_JOBS_COPY_ICOPY_PIPELINE_BUILDER_ADAPTER_H

#endif