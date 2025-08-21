/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   MockIPrintIntentsConverter.h
 * @date   Mon, 17 June 2025
 * @brief  Mock implementation of the PrintJoltToDuneConverter interface for testing
 *
 * (C) Copyright 2025 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#ifndef DUNE_COPY_JOBS_COPY_MOCK_PRINT_INTENTS_CONVERTER_H
#define DUNE_COPY_JOBS_COPY_MOCK_PRINT_INTENTS_CONVERTER_H

#include <gmock/gmock.h>
#include "IPrintIntentsConverter.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * @class MockIPrintIntentsConverter
 * @brief Mock class for PrintJoltToDuneConverter
 */
class MockIPrintIntentsConverter : public IPrintIntentsConverter
{
public:
    MockIPrintIntentsConverter() = default;
    virtual ~MockIPrintIntentsConverter() = default;

    MOCK_METHOD2(convert, 
                dune::framework::core::APIResult(
                    const dune::framework::data::conversion::DataDescriptor& fileDescriptor,
                    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable));
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif  // DUNE_COPY_JOBS_COPY_MOCK_PRINT_INTENTS_CONVERTER_H
