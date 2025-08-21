////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobServiceTemplateTypes.cpp
 * @brief  Template types exposed by CopyJobService
 * @author sateesh.nalamothu@hp.com
 * @date   2024-05-08
 *
 * (C) Copyright 2019 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "JobServiceFactory.hpp"
#include "ICopyJobTicket.h"

namespace dune { namespace job {
    template class JobServiceFactory<dune::copy::Jobs::Copy::ICopyJobTicket>; 
}}