/* -*- c++ -*- */

#ifndef DUNE_COPY_CDM_MOCK_I_COPY_ADAPTER_H
#define DUNE_COPY_CDM_MOCK_I_COPY_ADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   MockICopyAdapter.h
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component(MOCK) defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////
#include <gmock/gmock.h>
#include "ICopyAdapter.h"

namespace dune { namespace copy { namespace cdm {

class MockICopyAdapter : public ICopyAdapter
{
  public:
    MockICopyAdapter();
    virtual ~MockICopyAdapter();

    MOCK_METHOD0(getCopyEnabled, bool());
    MOCK_METHOD1(setCopyEnabled, void(dune::cdm::glossary_1::FeatureEnabled value));

    MOCK_METHOD0(getColorCopyEnabled, bool());
    MOCK_METHOD1(setColorCopyEnabled, void(dune::cdm::glossary_1::FeatureEnabled value));

    MOCK_METHOD0(getCopyMode, dune::cdm::copy_1::configuration::CopyMode());
    MOCK_METHOD1(setCopyMode, void(dune::cdm::copy_1::configuration::CopyMode value));

    MOCK_METHOD0(getInterruptMode, dune::cdm::glossary_1::FeatureEnabled());
    MOCK_METHOD1(setInterruptMode, void(dune::cdm::glossary_1::FeatureEnabled value));

    MOCK_METHOD0(getCopyAdapterDataChangeEvent, ICopyAdapterDataChangeEvent&());
};

}}}  // namespace dune::copy::cdm

#endif  // DUNE_COPY_CDM_MOCK_I_COPY_ADAPTER_H
