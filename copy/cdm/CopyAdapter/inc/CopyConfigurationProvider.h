/* -*- c++ -*- */

#ifndef DUNE_COPY_CDM_COPYCONFIGURATIONPROVIDER_H
#define DUNE_COPY_CDM_COPYCONFIGURATIONPROVIDER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyConfigurationProvider.h
 * @date   May 18, 2022
 * @brief  This is a CDM provider for Copy configurations (/cdm/copy/v1/configuration)
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////
//#include "CopyAdapterStandardConfig_generated.h"
#include "com.hp.cdm.service.copy.version.1.serviceDefinition_autogen.h"
#include "ICopyAdapter.h"

namespace dune { namespace copy { namespace cdm {

using OperationResult = dune::ws::cdm::OperationResult;
using namespace dune::ws::cdm;
using namespace dune::ws::cdm::framework;

class CopyConfigurationProvider : public dune::cdm::copy_1::configuration::ResourceProvider
{
public:
    /**
     * constructor
     */
    explicit CopyConfigurationProvider(ICopyAdapter* copyAdapter);
    /**
     * destructor
     */
    ~CopyConfigurationProvider() = default;

    std::unique_ptr<dune::cdm::copy_1::configuration::ResourceData> getImplementation(
        const RequestParameters &params, OperationResult &result,
        dune::ws::cdm::OperationResponseMetadataT &respMetadata) override;

    OperationResult setImplementation(const RequestParameters &params,
                                      std::unique_ptr<dune::cdm::copy_1::configuration::ResourceData>,
                                      dune::ws::cdm::OperationResponseMetadataT &respMetadata) override;

    OperationResult modifyImplementation(const RequestParameters &params,
                                         std::unique_ptr<dune::cdm::copy_1::configuration::ResourceData>,
                                         dune::ws::cdm::OperationResponseMetadataT &respMetadata) override;

	/**
 	 * @brief API for onDataChangeEventSubscription of SystemStatus 	 
 	 * @param bool: If the parameter "active" is false, it would mean that there are no more receivers registered to receive
 	 * the data change events.
 	*/
    void onDataChangeEventSubscription(bool active) override;

	/**
	 * @brief Method to handle updates of copy configuration from adapter	 
	 * @param event type of configuration updated
	 */
	void handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType event);

private:

	/**
	 * @brief Check if modify method is allowed in current state with current data	 
	 * @param params received 
	 * @param data received 
	 * @return true if yes 
	 * @return false if no
	 */
    bool isModifyAllowed( const RequestParameters &params, std::unique_ptr<dune::cdm::copy_1::configuration::ResourceData> &data );

    dune::cdm::copy_1::types::Configuration::FBT 	configurations_;
    dune::cdm::glossary_1::FeatureEnabled 			copyEnabled_ = dune::cdm::glossary_1::FeatureEnabled::true_;
    dune::cdm::glossary_1::FeatureEnabled 			colorCopyEnabled_ = dune::cdm::glossary_1::FeatureEnabled::true_;
    dune::copy::cdm::ICopyAdapter* 					copyAdapter_{nullptr};
	bool                   							isDataChangeSubscriptionActive_{false};
	uint32_t                                    	copyEventSubscriptionId{0};
};

}}}  // namespace dune::copy::cdm

#endif  // DUNE_COPY_CDM_COPYCONFIGURATIONPROVIDER_H