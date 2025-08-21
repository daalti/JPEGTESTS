/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_I_COPY_PIPELINE_H
#define DUNE_COPY_JOBS_COPY_I_COPY_PIPELINE_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   ICopyPipeline.h
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
#include "ICopyPipelineBuilderAdapter.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {
/**
 * @brief  Configurable Copy Pipeline 
 *
 * @todo describe the main responsibilities and interactions of the
 * component(s) realizing this interface.
 */
class ICopyPipeline
{
public:

    /**
     * @brief Method to create copy pipe pipeline builder 
     * @param jobTicket copy job ticket 
     * @param prePrintConfiguration Pre print configuration of product
     * @param services service package for all the resources
     * @param scanPipeline scan pipeline interface
     * @param maxLengthConfig Max Lenght config
     * @param dateTime date time interface.
     */
    virtual std::shared_ptr<dune::job::IPipelineBuilder> createPipelineBuilder(
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket, dune::copy::Jobs::Copy::Product prePrintConfiguration,
                        dune::copy::Jobs::Copy::ServicesPackage& services, dune::scan::Jobs::Scan::IScanPipeline* scanPipeline, bool copyBasicPipeline, bool hasSharedPaperPath,
                        const dune::copy::Jobs::Copy::MaxLengthConfig& maxLengthConfig, dune::framework::core::time::IDateTime *dateTime, bool multiPageSupportedFromFlatbed) = 0;

    /**
     * @brief Set the Max Collate Pages value
     * 
     * @param max 
     * @return true when set successfully
     * @return false when not set successfully
     */
    virtual bool setMaxCollatePages(int max)
    {
        return false;
    }
    
    /**
     * Destructor.
     */
    virtual ~ICopyPipeline() { }

    // @todo add pure virtual methods of the interface here.
};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline, 0xcc9f8a);

#endif  // DUNE_COPY_JOBS_COPY_I_COPY_PIPELINE_H

