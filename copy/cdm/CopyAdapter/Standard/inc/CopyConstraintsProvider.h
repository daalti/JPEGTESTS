#ifndef DUNE_COPY_CDM_COPYCONSTRAINTSPROVIDER_H
#define DUNE_COPY_CDM_COPYCONSTRAINTSPROVIDER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyConstraintsProvider.h
 * @date
 * @brief  Service provider classes for all Copy constraints
 *
 * (C) Copyright 2023 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "com.hp.cdm.service.copy.version.1.serviceDefinition_autogen.h"
#include "ConstraintsGroup.h"
#include "CopyAdapterStandardConfig_generated.h"

namespace dune { namespace localization {
class ILocaleProvider;
}}  // namespace dune::localization


namespace dune { namespace copy { namespace cdm {
// Forward declaration
class ICopyAdapter;
enum class CopyConfigurationEventType: uint8_t;

using namespace dune::ws::cdm;
using namespace dune::ws::cdm::framework;
using namespace dune::framework::data::constraints;

using ConfigurationConstraintsResourceData = dune::cdm::copy_1::configurationConstraints::ResourceData;

/**
 * Resource provider class for Copy constraints
 */
class CopyConfigurationConstraintsProvider : public dune::cdm::copy_1::configurationConstraints::ResourceProvider
{
public:
    explicit CopyConfigurationConstraintsProvider(ICopyAdapter * copyAdapter, dune::localization::ILocaleProvider * localeProvider, 
                                                  std::shared_ptr<dune::copy::cdm::ConstraintsStringIdValuesT> constraintsStringIds);

    std::unique_ptr<ConfigurationConstraintsResourceData> getImplementation(
        const RequestParameters &params, OperationResult &result, dune::ws::cdm::OperationResponseMetadataT &respMetadata) override;

    /**
     * @brief API for onDataChangeEventSubscription of SystemStatus
     * @param bool: If the parameter "active" is false, it would mean that there are no more receivers registered to
     * receive the data change events.
     */
    void onDataChangeEventSubscription(bool active) override;

    /**
     * @brief Method to handle updates of copy configuration from adapter
     * @param event type of configuration updated
     */
    bool handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType event);

private:
    ICopyAdapter *                         copyAdapter_{nullptr};
    dune::localization::ILocaleProvider *  localeProvider_{nullptr};
    std::shared_ptr<Constraints> getAllowInterruptConstraints(bool isCopyModePrintWhileScanning);
    bool 	isDataChangeSubscriptionActive_{false};
    uint32_t  copyEventSubscriptionId{0};
    std::shared_ptr<dune::copy::cdm::ConstraintsStringIdValuesT> constraintsStringIds_;

    /**
     * @brief It builds constraint message of interrupt setting
     * @return string constraint message
     */
    std::string getConstraintInterruptMessage();

    /**
     * @brief Get copy configuration constraints
     */
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> getCopyConfigurationConstraints();
};

}}}  // namespace dune::copy::cdm

#endif  // DUNE_COPY_CDM_COPYCONSTRAINTSPROVIDER_H
