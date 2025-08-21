/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_ICOPYJOBSERVICE_H
#define DUNE_COPY_JOBS_COPY_ICOPYJOBSERVICE_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   ICopyJobService.h
 * @date   Wed, 08 May 2019 06:49:54 -0700
 * @brief  JobService specific class to CopyJobs
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ComponentSystemTypes.h"
#include "IJobServiceFactory.h"
#include "ICopyJobTicket.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {
    /**
     * @brief Concrete interface to be used by CopyApp
     * 
     */
    using ICopyJobService = dune::job::IJobServiceFactory<ICopyJobTicket>;

}}}} // namespace dune::copy::Jobs::Copy

DEFINE_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService, 0x2a82f1);

#endif // DUNE_COPY_JOBS_COPY_ICOPYJOBSERVICE_H