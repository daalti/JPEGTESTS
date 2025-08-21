/* -*- c++ -*- */

#ifndef DUNE_COPY_CDM_I_COPY_ADAPTER_H
#define DUNE_COPY_CDM_I_COPY_ADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   ICopyAdapter.h
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ComponentSystemTypes.h"
#include "Event.h"
#include "com.hp.cdm.domain.glossary.version.1_generated.h"
#include "com.hp.cdm.service.copy.version.1_generated.h"

namespace dune { namespace copy { namespace cdm {

enum class CopyConfigurationEventType : uint8_t
{
    COPY_ENABLE_STATE_CHANGE = 0,
    COLOR_COPY_ENABLE_STATE_CHANGE = 1,
    COPY_MODE = 2,
    COPY_INTERRUPT_MODE=3
};

using ICopyAdapterDataChangeEvent =
	dune::framework::core::event::Event<CopyConfigurationEventType>;

/**
 * @brief This is a CDM Adapter component defining the Copy Service
 *
 * @todo describe the main responsibilities and interactions of the
 * component(s) realizing this interface.
 */
class ICopyAdapter
{
public:
    /**
     * Destructor.
     */
    virtual ~ICopyAdapter() {}

    // @todo add pure virtual methods of the interface here.
    virtual bool getCopyEnabled() = 0;
    virtual void setCopyEnabled(dune::cdm::glossary_1::FeatureEnabled value) = 0;

    virtual bool getColorCopyEnabled() = 0;
    virtual void setColorCopyEnabled(dune::cdm::glossary_1::FeatureEnabled value) = 0;

    /**
     * @brief Get the Copy Mode
     * 
     * @return The current copy mode
     */
    virtual dune::cdm::copy_1::configuration::CopyMode getCopyMode() = 0;

    /**
     * @brief Set the Copy Mode
     * 
     * @param value Copy mode type
     */
    virtual void setCopyMode(dune::cdm::copy_1::configuration::CopyMode value) = 0;

    /**
     * @brief Get the Interrupt Mode object
     * @return featureEnabled current interrupt mode
     */
    virtual dune::cdm::glossary_1::FeatureEnabled getInterruptMode() = 0;

    /**
     * @brief Set the Interrupt Mode object     
     * @param value cdm boolean to change mode
     */    
    virtual void setInterruptMode(dune::cdm::glossary_1::FeatureEnabled value) = 0;

	/**
	 * @brief Get the Copy Adapter Data Change Event object
	 * @return ICopyAdapterDataChangeEvent& event to subscribe to changes in settings in adapter
	 */
    virtual ICopyAdapterDataChangeEvent& getCopyAdapterDataChangeEvent() = 0;
};

}}}  // namespace dune::copy::cdm

DEFINE_INTERFACE_UID(dune::copy::cdm::ICopyAdapter, 0xa619a7);

#endif  // DUNE_COPY_CDM_I_COPY_ADAPTER_H
