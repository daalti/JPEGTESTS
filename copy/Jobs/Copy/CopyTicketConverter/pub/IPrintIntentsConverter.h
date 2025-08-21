/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   IPrintIntentsConverter.h
 * @date   Mon, 17 June 2025
 * @brief  Interface for Jolt to Dune print data converter
 *
 * (C) Copyright 2025 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#ifndef DUNE_COPY_JOBS_COPY_IPRINT_INTENTS_CONVERTER_H
#define DUNE_COPY_JOBS_COPY_IPRINT_INTENTS_CONVERTER_H

#include <memory>
#include "SystemConversionTypes.h"
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"
#include "dune_types.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * @class IPrintIntentsConverter
 * @brief Interface for converting print settings from Jolt XML format to Dune JobTicket format
 */
class IPrintIntentsConverter
{
public:
    /**
     * @brief Virtual destructor for interface class
     */
    virtual ~IPrintIntentsConverter() = default;

    /**
     * @brief Convert print settings from XML to JobTicket format
     * @param fileDescriptor The input data descriptor
     * @param updatedJobTicketTable The job ticket to populate
     * @return API result code
     */
    virtual dune::framework::core::APIResult convert(
        const dune::framework::data::conversion::DataDescriptor& fileDescriptor,
        std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable) = 0;
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif  // DUNE_COPY_JOBS_COPY_IPRINT_INTENTS_CONVERTER_H
