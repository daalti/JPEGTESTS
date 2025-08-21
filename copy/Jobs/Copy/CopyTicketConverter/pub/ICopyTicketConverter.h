/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_I_COPY_TICKET_CONVERTER_H
#define DUNE_COPY_JOBS_COPY_I_COPY_TICKET_CONVERTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   ICopyTicketConverter.h
 * @date   Fri, 02 May 2025 23:00:08 +0530
 * @brief  
 *
 * (C) Copyright 2025 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ComponentSystemTypes.h"
#include <memory>
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"
#include "SystemConversionTypes.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {
/**
 * @brief 
 *
 * @todo describe the main responsibilities and interactions of the
 * component(s) realizing this interface.
 */
class ICopyTicketConverter
{
public:

    /**
     * Destructor.
     */
    virtual ~ICopyTicketConverter() { }

    virtual dune::framework::data::conversion::ConversionResult convert(
        const dune::framework::data::conversion::DataDescriptor& , std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& ) = 0;
};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyTicketConverter, 0xb8abb6);

#endif  // DUNE_COPY_JOBS_COPY_I_COPY_TICKET_CONVERTER_H

