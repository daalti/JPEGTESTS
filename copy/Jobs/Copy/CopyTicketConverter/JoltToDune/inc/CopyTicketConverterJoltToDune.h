/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPY_TICKET_CONVERTER_JOLT_TO_DUNE_H
#define DUNE_COPY_JOBS_COPY_COPY_TICKET_CONVERTER_JOLT_TO_DUNE_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyTicketConverterJoltToDune.h
 * @date   Fri, 02 May 2025 23:00:09 +0530
 * @brief
 *
 * (C) Copyright 2025 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponent.h"
#include "ICopyTicketConverter.h"
#include "IPipelineOptionsConvertionAdapter.h"
#include "IPrintIntentsConverter.h"
#include "IScanJoltToDuneConverter.h"
#include "SystemServices.h"
#include "dune_types.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_CopyTicketConverterJoltToDune);

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using IScanJoltToDuneConverter = dune::scan::IScanJoltToDuneConverter;
using IPipelineOptionsConvertionAdapter = dune::imaging::Jobs::IPipelineOptionsConvertionAdapter;

/**
 * Implementation of the Standard flavor of the CopyTicketConverter component.
 */
class CopyTicketConverterJoltToDune : public dune::framework::component::IComponent, public ICopyTicketConverter
{
  public:
    /**
     * @name ICopyTicketConverter methods.
     * @{
     */
    dune::framework::data::conversion::ConversionResult convert(
        const dune::framework::data::conversion::DataDescriptor& fileDescriptor,
        std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& jobTicketTable);

    
    /**
     * @brief CopyTicketConverterJoltToDune Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    CopyTicketConverterJoltToDune(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~CopyTicketConverterJoltToDune();

    /**
     * @name IComponent methods.
     * @{
     */

    dune::framework::component::ComponentFlavorUid getComponentFlavorUid() const override;
    const char                                    *getComponentInstanceName() const override;
    void  initialize(WorkingMode mode, const dune::framework::component::SystemServices *services) override;
    void *getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName) override;
    void  setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName,
                       void *interfacePtr) override;
    void  connected(dune::framework::component::IComponentManager *componentManager,
                    std::future<void>                             &asyncCompletion) override;
    void  shutdown(ShutdownCause cause, std::future<void> &asyncCompletion) override;

    /**
     * @}
     */

  protected:
    IPipelineOptionsConvertionAdapter *pipelineOptionsConverter_{nullptr};  ///< Pipeline options converter instance
    IPrintIntentsConverter *printJoltToDuneConverter_{nullptr};  ///< Print converter instance
  
  private:
    const char *instanceName_;  ///< The instance name.
    IScanJoltToDuneConverter *scanJoltToDuneConverter_{nullptr};  ///< Scan converter instance
};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_MODULE_UID(dune::copy::Jobs::Copy::CopyTicketConverterJoltToDune, 0x3da0ec);

DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::Jobs::Copy::CopyTicketConverterJoltToDune)
PROVIDES_INTERFACE(dune::copy::Jobs::Copy::ICopyTicketConverter)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::Jobs::Copy::CopyTicketConverterJoltToDune)

#endif  // DUNE_COPY_JOBS_COPY_COPY_TICKET_CONVERTER_JOLT_TO_DUNE_H
