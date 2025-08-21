/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPY_PIPELINE_STANDARD_H
#define DUNE_COPY_JOBS_COPY_COPY_PIPELINE_STANDARD_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineStandard.h
 * @date   Mon, 27 Feb 2023 13:43:04 +0530
 * @brief   Configurable Copy Pipeline 
 *
 * (C) Copyright 2023 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponent.h"
#include "ICopyPipeline.h"
#include "CopyPipelineStandardConfig_generated.h"

#include "IColorDirector.h"
#include "IColorEngine.h"
#include "IImageColorEngine.h"
#include "IImagePersisterTicket.h"
#include "IImageProcessorTicket.h"
#include "IImageRetrieverTicket.h"
#include "IRtpFilterTicket.h"
#include "IScanPipeline.h"
#include "IIntentsManager.h"
#include "ResourceInstanceProxy.h"
#include "CopyConfigurablePipelineBuilder.h"
#include "IDateTime.h"
#include "ICopyAdapter.h"

using namespace std;
using dune::job::IPipelineBuilder;
using dune::job::IResourceInstanceProxy;
using dune::job::IResourceService;
using dune::job::ResourceInstanceProxy;
using dune::job::ResourceInstanceProxyAgent;
using IScanPipeline = dune::scan::Jobs::Scan::IScanPipeline;
using IIntentsManager = dune::job::IIntentsManager;
using IDateTime = dune::framework::core::time::IDateTime;

namespace dune { namespace imaging {
  class IPipelineMemoryClientCreator;
}}

namespace dune { namespace print { namespace engine {
class IPrintIntentsFactory;
class ISettings;
}}}

namespace dune { namespace job {
class IIntentsManager;
}}

namespace dune { namespace print { namespace engine { namespace helpers {
class IPrintIntentsFactory;
}}}}

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_CopyPipelineStandard);

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class CopyPipelineUwAdapter;

/**
 * Implementation of the Standard flavor of the CopyPipeline component.
 */
class CopyPipelineStandard:
    public dune::framework::component::IComponent,
    public ICopyPipeline
{
public:

    /**
     * @name ICopyPipeline methods.
     * @{
     */
    std::shared_ptr<dune::job::IPipelineBuilder> createPipelineBuilder(
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket, Product prePrintConfiguration,
                        ServicesPackage& services, dune::scan::Jobs::Scan::IScanPipeline* scanPipeline, bool copyBasicPipeline, bool hasSharedPaperPath,
                        const MaxLengthConfig& maxLengthConfig, dune::framework::core::time::IDateTime *dateTime, bool multiPageSupportedFromFlatbed) override;
    // exposed for udw
    bool setMaxCollatePages(int max) override;

    /**
     * @brief Enable and use LayoutFilter instead of MarkingFilter
     *
     * @param enable true to enable LayoutFilter, false to disable it
     * @note this method is only exposed to the underware
     */
    void enableLayoutFilter(bool enable);

    /**
     * @brief CopyPipelineStandard Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit CopyPipelineStandard(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~CopyPipelineStandard();

    /**
     * @name IComponent methods.
     * @{
     */

    dune::framework::component::ComponentFlavorUid getComponentFlavorUid() const override;
    const char * getComponentInstanceName() const override;
    void initialize(WorkingMode mode, const dune::framework::component::SystemServices *services) override;
    void * getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName) override;
    void setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName, void *interfacePtr) override;
    void connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion) override;
    void shutdown(ShutdownCause cause, std::future<void> &asyncCompletion) override;

    /**
     * @}
     */

protected:

    /**
     * @brief Loads the configuration for this component instance
     *
     * @param configurationService the pointer to the system's configuration service
     * @return the configuration values to be used by this instance, according to the system's product and proto
     *         versions or nullptr if the configuration is not available for this instance.
     */
    std::unique_ptr<CopyPipelineStandardConfigT> getConfiguration(dune::framework::resources::IConfigurationService *configurationService) const;

private:

    const char                                              *instanceName_; ///< The instance name.
    const dune::framework::component::SystemServices        *services_{nullptr};
    std::unique_ptr<CopyPipelineStandardConfigT>            configuration_; ///< The instance's constants configuration
    std::unique_ptr<CopyPipelineUwAdapter>                   uwAdapter_{nullptr};  ///< Uw Adapter

    dune::scan::Jobs::Scan::IScanPipeline                   *scanPipeline_{nullptr};
    ServicesPackage                                         servicePackage_{};  
    dune::print::engine::ISettings                          *interfaceISettings_ { nullptr }; ///< interface to the ISettings subsystem
    dune::job::IIntentsManager                              *intentsManager_{nullptr}; ///< IIntentsManager interface
    IDateTime*                                              dateTime_{nullptr};
    dune::copy::cdm::ICopyAdapter                           *copyAdapter_{nullptr};
    dune::scan::Resources::IIPADevice                       *ipaDeviceService{nullptr};
    dune::imaging::Resources::IImageImporter                *imageImporter_{nullptr}; ///< Image Importer interface
};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_MODULE_UID(dune::copy::Jobs::Copy::CopyPipelineStandard, 0x5c2e52);

DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::Jobs::Copy::CopyPipelineStandard)
    PROVIDES_INTERFACE(dune::copy::Jobs::Copy::ICopyPipeline)
    REQUIRES_INTERFACE(dune::copy::cdm::ICopyAdapter)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::Jobs::Copy::CopyPipelineStandard)


#endif  // DUNE_COPY_JOBS_COPY_COPY_PIPELINE_STANDARD_H

