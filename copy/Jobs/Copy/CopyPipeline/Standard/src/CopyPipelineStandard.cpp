/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineStandard.cpp
 * @date   Mon, 27 Feb 2023 13:43:04 +0530
 * @brief   Configurable Copy Pipeline 
 *
 * (C) Copyright 2023 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyPipelineStandard.h"

#include "common_debug.h"

#include "CopyPipelineStandard_TraceAutogen.h"

#include "CopyPipelineUwAdapter.h"
#include "ErrorManager.h"
#include "IConfigurationService.h"

// Factory method

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_CopyPipelineStandard)
{
    dune::copy::Jobs::Copy::CopyPipelineStandard *instance = new dune::copy::Jobs::Copy::CopyPipelineStandard(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}


namespace dune { namespace copy { namespace Jobs { namespace Copy {

// Constructor and destructor

CopyPipelineStandard::CopyPipelineStandard(const char *instanceName) :
    instanceName_(instanceName)
{
    CHECKPOINTC("%s/CopyPipelineStandard: constructed", instanceName_);
}

CopyPipelineStandard::~CopyPipelineStandard()
{
}

// IComponent methods.

dune::framework::component::ComponentFlavorUid CopyPipelineStandard::getComponentFlavorUid() const
{
    return GET_MODULE_UID(CopyPipelineStandard);
}

const char *CopyPipelineStandard::getComponentInstanceName() const
{
    return instanceName_;
}

void CopyPipelineStandard::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);
    services_ = services;
    if ( services_->configurationService_ != nullptr )
    {
        configuration_ = getConfiguration(services_->configurationService_);
    }

    CHECKPOINTC("%s/CopyPipelineStandard: initialized", instanceName_);
}

void * CopyPipelineStandard::getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName)
{
    DUNE_UNUSED(portName);
    void *interfacePtr = nullptr;
    if (interfaceUid == GET_INTERFACE_UID(ICopyPipeline))
    {
        interfacePtr = static_cast<ICopyPipeline *>(this);
    }
    CHECKPOINTC("%s/CopyPipelineStandard: getInterface %" PRIu32 " from port %s with addr %p", instanceName_, interfaceUid, portName, interfacePtr);
    return interfacePtr;
}

void CopyPipelineStandard::setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName, void *interfacePtr)
{
    if (interfacePtr != nullptr)
    {
        if (interfaceUid == GET_INTERFACE_UID(dune::job::IResourceManagerClient))
        {
            auto *resourceManagerClient = static_cast<dune::job::IResourceManagerClient *>(interfacePtr);
            servicePackage_.resourceManager = resourceManagerClient;
            CHECKPOINTC("%s/CopyPipelineStandard: setInterface IResourceManagerClient to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory))
        {
            auto *printIntentsFactoryPtr = static_cast<dune::print::engine::IPrintIntentsFactory *>(interfacePtr);
            servicePackage_.printIntentsFactory = printIntentsFactoryPtr;
            CHECKPOINTC("%s/CopyPipelineStandard: setInterface IPrintIntentsFactory to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::scan::Resources::IScanDevice))
        {
            assert(servicePackage_.scanDeviceService == nullptr);
            servicePackage_.scanDeviceService = static_cast<dune::scan::Resources::IScanDevice *>(interfacePtr);
                static_cast<dune::scan::Resources::IScanDevice *>(interfacePtr)->getResourceService();
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::imaging::color::IColorDirector))
        {
            servicePackage_.colorDirector = static_cast<dune::imaging::color::IColorDirector *>(interfacePtr);
            CHECKPOINTC("%s/CopyPipelineStandard: setInterface IColorDirector to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::IResourceService))
        {
            auto *resourceServicePtr = static_cast<dune::job::IResourceService *>(interfacePtr);

            if (strcmp(portName, "MarkingFilter") == 0)
            {
                assert(servicePackage_.markingFilterService == nullptr);
                servicePackage_.markingFilterService = 
                     dynamic_cast<dune::imaging::Resources::IMarkingFilter *>(resourceServicePtr);
                CHECKPOINTC(
                    "%s/CopyPipelineStandard: setInterface MarkingFilter IResourceService to port %s with addr %p",
                    instanceName_, portName, interfacePtr);
            }
            else if (strcmp(portName, "ImageRetriever") == 0)
            {
                assert(servicePackage_.imageRetrieverService == nullptr);
                servicePackage_.imageRetrieverService = resourceServicePtr;
                CHECKPOINTC(
                    "%s/CopyPipelineStandard: setInterface ImageRetriver IResourceService to port %s with addr %p",
                    instanceName_, portName, interfacePtr);
            }
            else if (strcmp(portName, "ImageProcessor") == 0)
            {
                assert(servicePackage_.imageProcessor == nullptr);
                servicePackage_.imageProcessor =
                    dynamic_cast<dune::imaging::Resources::IImageProcessor *>(resourceServicePtr);
                CHECKPOINTC("%s/CopyPipelineStandard: setInterface IImageProcessor to port %s with addr %p",
                            instanceName_, portName, interfacePtr);
            }
            else if (strcmp(portName, "RtpFilterService") == 0)
            {
                assert(servicePackage_.rtpFilterService == nullptr);
                servicePackage_.rtpFilterService = resourceServicePtr;
                CHECKPOINTC(
                    "%s/CopyPipelineStandard: setInterface RtpFilterService IResourceService to port %s with addr %p",
                    instanceName_, portName, interfacePtr);
            }
            else if (strcmp(portName, "IPADeviceService") == 0)
            {
                assert(ipaDeviceService == nullptr);
                ipaDeviceService = dynamic_cast<dune::scan::Resources::IIPADevice *>(resourceServicePtr);
                CHECKPOINTC(
                    "%s/CopyPipelineStandard: setInterface IIPADeviceService IResourceService to port %s with addr %p",
                    instanceName_, portName, interfacePtr);
            }
            else if (strcmp(portName, "ImageImporter") == 0)
            {
                assert(imageImporter_ == nullptr);
                imageImporter_ = dynamic_cast<dune::imaging::Resources::IImageImporter *>(resourceServicePtr);
                CHECKPOINTC(
                    "%s/CopyPipelineStandard: setInterface IImageImporter IResourceService to port %s with addr %p",
                    instanceName_, portName, interfacePtr);
            }
            else
            {
                CHECKPOINTC(
                    "%s/CopyPipelineStandard: setInterface portName is not implemented, port %s with addr %p",
                    instanceName_, portName, interfacePtr);
            }
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister))
        {
            assert(servicePackage_.imagePersister == nullptr);
            servicePackage_.imagePersister = static_cast<dune::imaging::Resources::IImagePersister *>(interfacePtr);
            CHECKPOINTC("%s/CopyPipelineStandard: setInterface IImagePersister to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler))
        {
            assert(servicePackage_.pageAssembler == nullptr);
            servicePackage_.pageAssembler = static_cast<dune::imaging::Resources::IPageAssembler *>(interfacePtr);
            CHECKPOINTC("%s/CopyPipelineStandard: setInterface IPageAssembler to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::Resources::IPrintDevice))
        {
            assert(servicePackage_.printDevice == nullptr);
            servicePackage_.printDevice = static_cast<dune::print::Resources::IPrintDevice *>(interfacePtr);
            CHECKPOINTA("%s/CopyPipelineStandard: Copy pipeline using print device memory client",
                        getComponentInstanceName());
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::IMedia))
        {
            CHECKPOINTA("%s/CopyPipelineStandard: setInterface IMedia interfaceUid %" PRIu32 " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
            servicePackage_.mediaInterface = static_cast<dune::print::engine::IMedia *>(interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements))
        {
            servicePackage_.renderingRequirements =
                static_cast<dune::print::engine::helpers::IRenderingRequirements *>(interfacePtr);
            CHECKPOINTB("%s/CopyPipelineStandard: setInterface IRenderingRequirements to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes))
        {
            servicePackage_.mediaAttributes = static_cast<dune::imaging::asset::IMediaAttributes *>(interfacePtr);
            CHECKPOINTB("%s/CopyPipelineStandard: setInterface IMediaAttributes to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline))
        {
            auto scanPipeline = static_cast<dune::scan::Jobs::Scan::IScanPipeline *>(interfacePtr);
            scanPipeline_ = scanPipeline;
            CHECKPOINTC("%s/CopyPipelineStandard: setInterface IScanPipeline to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::IIntentsManager))
        {
            intentsManager_ = static_cast<dune::job::IIntentsManager *>(interfacePtr);
            CHECKPOINTB("%s/CopyPipelineStandard: setInterface IIntentsManager to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter))
        {
            copyAdapter_ = static_cast<dune::copy::cdm::ICopyAdapter *>(interfacePtr);
            CHECKPOINTB("%s/CopyPipelineStandard: setInterface ICopyAdapter to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else
        {
            CHECKPOINTA("%s/CopyPipelineStandard: setInterface not handled for interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
        }

    }
    else
    {
        CHECKPOINTA("%s/CopyPipelineStandard: setInterface 0x%" PRIx32 " to port %s with addr %p",
                    getComponentInstanceName(), interfaceUid, portName, interfacePtr);
    }
}

void CopyPipelineStandard::connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(componentManager);
    DUNE_UNUSED(asyncCompletion);
    
    CHECKPOINTC("%s/CopyPipelineStandard: connected", instanceName_);

    // Create UW Adapter
    uwAdapter_ = std::make_unique<CopyPipelineUwAdapter>(services_->interpreterEnvironment_, "CopyPipeline", this);
}

void CopyPipelineStandard::shutdown(ShutdownCause cause, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(cause);
    DUNE_UNUSED(asyncCompletion);
    CHECKPOINTC("%s/CopyPipelineStandard: shutdown", instanceName_);
}

std::unique_ptr<CopyPipelineStandardConfigT> CopyPipelineStandard::getConfiguration(dune::framework::resources::IConfigurationService *configurationService) const
{
    assert(configurationService);
    dune::framework::resources::IConfigurationService::ConfigurationRawData rawConfiguration =
        configurationService->getConfiguration(GET_MODULE_UID(CopyPipelineStandard), instanceName_);
    if (rawConfiguration.data && (rawConfiguration.size > 0))
    {
        flatbuffers::Verifier verifier(rawConfiguration.data.get(), rawConfiguration.size);
        assert(VerifyCopyPipelineStandardConfigBuffer(verifier));
        return UnPackCopyPipelineStandardConfig(rawConfiguration.data.get());
    }
    else
    {
        return std::unique_ptr<CopyPipelineStandardConfigT>();
    }
}

std::shared_ptr<dune::job::IPipelineBuilder> CopyPipelineStandard::createPipelineBuilder(
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket, Product prePrintConfiguration,
                        ServicesPackage& services, dune::scan::Jobs::Scan::IScanPipeline* scanPipeline, bool copyBasicPipeline, bool hasSharedPaperPath,
                        const MaxLengthConfig& maxLengthConfig, dune::framework::core::time::IDateTime *dateTime, bool multiPageSupportedFromFlatbed)
{
    
    CHECKPOINTA("%s/CopyPipelineStandard: createPipelineBuilder", getComponentInstanceName());
    if(ipaDeviceService && services.ipaDeviceService == nullptr)
    {
        services.ipaDeviceService = ipaDeviceService;
        CHECKPOINTD("%s/CopyPipelineStandard: setInterface IIPADevice to port %s with addr %p", instanceName_, "IIPADevice", ipaDeviceService);
    }
    if(imageImporter_ && services.imageImporter == nullptr)
    {
        services.imageImporter = imageImporter_;
        CHECKPOINTD("%s/CopyPipelineStandard: setInterface IImageImporter to port %s with addr %p", instanceName_, "IImageImporter", imageImporter_);
    }
    auto pipelineBuilder = std::make_shared<CopyConfigurablePipelineBuilder>(
        jobTicket, services, hasSharedPaperPath, scanPipeline, (Product)prePrintConfiguration, copyBasicPipeline,
        maxLengthConfig, intentsManager_, dateTime, multiPageSupportedFromFlatbed, copyAdapter_,
        configuration_->layoutFilterEnabled);
    assert_msg(configuration_->pipelineBuilderConfig != nullptr,
                   "CopyPipelinebuilder::onBuildPipeline()- scanPipeline_ pipline config is null");
    pipelineBuilder->setPipelineConfig(configuration_->pipelineBuilderConfig.get());
    pipelineBuilder->setThresholdOverride(configuration_->thresholdOverride);
    pipelineBuilder->setTopSpecificPadding(configuration_->topSpecificPadding);
    pipelineBuilder->setBottomSpecificPadding(configuration_->bottomSpecificPadding);
    pipelineBuilder->setLeftSpecificPadding(configuration_->leftSpecificPadding);
    pipelineBuilder->setRightSpecificPadding(configuration_->rightSpecificPadding);
    pipelineBuilder->setPrintingOrder(configuration_->printingOrder);
    pipelineBuilder->setPageCountBeforeSequencing(configuration_->pageCountBeforeSequencing);
    pipelineBuilder->setMaxPagesToCollate(configuration_->maxPagesToCollate);
    pipelineBuilder->setMaxFlatbedDuplexPages(configuration_->maxFlatbedDuplexPages);

    return pipelineBuilder;
}

bool CopyPipelineStandard::setMaxCollatePages(int max)
{
    bool retVal = false;
    if(configuration_ != nullptr)
    {
        CHECKPOINTA("CopyPipelineStandard::setMaxCollatePages: prevVal:%d newValue:%d", configuration_->maxPagesToCollate, max);
        configuration_->maxPagesToCollate = max;
        retVal = true;
    }
    else
    {
        CHECKPOINTA("CopyPipelineStandard::setMaxCollatePages: error setting maxPagesToCollate; configuration is null");
    }
    return retVal;
}

void CopyPipelineStandard::enableLayoutFilter(bool enable)
{
    CHECKPOINTC("CopyPipelineStandard: enableLayoutFilter(%u)", enable);
    configuration_->layoutFilterEnabled = enable;
}

}}}}  // namespace dune::copy::Jobs::Copy

