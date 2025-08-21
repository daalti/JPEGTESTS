/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_MOCKI_COPY_PIPELINE_H
#define DUNE_COPY_JOBS_COPY_MOCKI_COPY_PIPELINE_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   MockICopyPipeline.h
 * @date   Mon, 27 Feb 2023 13:43:04 +0530
 * @brief   Configurable Copy Pipeline 
 *
 * (C) Copyright 2023 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ComponentSystemTypes.h"
#include "IPipelineBuilder.h"
#include "ICopyJobTicket.h"
#include "IScanPipeline.h"
#include "ICopyPipeline.h"
#include "ICopyPipelineBuilderAdapter.h"

namespace dune {
namespace copy {
namespace Jobs {
namespace Copy {

class MockICopyPipeline : public ICopyPipeline {
 public:
 MockICopyPipeline() {};
 virtual ~MockICopyPipeline() {};

  MOCK_METHOD9(createPipelineBuilder,
      std::shared_ptr<dune::job::IPipelineBuilder>(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket, dune::copy::Jobs::Copy::Product prePrintConfiguration, dune::copy::Jobs::Copy::ServicesPackage& services, dune::scan::Jobs::Scan::IScanPipeline* scanPipeline, bool copyBasicPipeline, bool hasSharedPaperPath, const dune::copy::Jobs::Copy::MaxLengthConfig& maxLengthConfig, dune::framework::core::time::IDateTime *dateTime, bool multiPageSupportedFromFlatbed_));
};

}  // namespace Copy
}  // namespace Jobs
}  // namespace copy
}  // namespace dune

#endif  // DUNE_COPY_JOBS_COPY_I_COPY_PIPELINE_H

