/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobTicketResourceHelper.cpp
 * @date   Tue, 06 Aug 2019 12:14:22 +0530
 * @brief
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "JobTicketResourceHelper.h"

#include "common_debug.h"

#include "JobTicketResourceHelper_TraceAutogen.h"

#include "IConfigurationService.h"
#include "CopyTicketAdapter.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using dune::job::JobSourceDestinationType;
using dune::job::JobType;

// Constructor and destructor

JobTicketResourceHelper::JobTicketResourceHelper(JobServiceFactory<ICopyJobTicket>* jobService)
    : copyJobService_(jobService)
{
    CHECKPOINTC("Copy/JobTicketResourceHelper: constructed");
    configurations_ = {{JobSourceDestinationType::SCAN, JobSourceDestinationType::PRINT, JobType::COPY, "copy", this}};
}

JobTicketResourceHelper::~JobTicketResourceHelper()
{
    CHECKPOINTA("dune::copy::Jobs::Copy::JobTicketResourceHelper::~JobTicketResourceHelper -- ENTER");
    
    if(configurations_.size() > 0)
    {
        CHECKPOINTA("dune::copy::Jobs::Copy::JobTicketResourceHelper::~JobTicketResourceHelper -- configurations_.size() ");
        configurations_.clear();
        configurations_.shrink_to_fit();
    }
    CHECKPOINTC("Copy/JobTicketResourceHelper: destroyed");
}

void JobTicketResourceHelper::registerHelper(IJobTicketResourceManager* jobTicketResourceManager)
{
    CHECKPOINTA("dune::copy::Jobs::Copy::JobTicketResourceHelper::registerHelper -- ENTER");
    int count = 0;
    for (auto& config : configurations_)
    {
        CHECKPOINTA(
            "dune::copy::Jobs::Copy::JobTicketResourceHelper::registerHelper -- configuration[%d] src:%s,dest:%s.",
            count++, EnumNameJobSourceDestinationType(config.src_), EnumNameJobSourceDestinationType(config.dest_));
    }
    jobTicketResourceManager->registerResourceHelper(configurations_);
    CHECKPOINTA("dune::copy::Jobs::Copy::JobTicketResourceHelper::registerHelper -- EXIT");
}

std::shared_ptr<ITicketAdapter> JobTicketResourceHelper::createTicketAdapter(const Configuration& configuration,
                                                                             JobTicketType        jobTicketType)
{
    std::shared_ptr<CopyTicketAdapter> copyTicketAdapter;
    // If there are multiple configuration supported, check configuration to provide the particular jobTicket i.e.
    // TicketAdapter
    if (configuration.src_ == JobSourceDestinationType::SCAN && configuration.dest_ == JobSourceDestinationType::PRINT)
    {
        if (jobTicketType == JobTicketType::DEFAULT)
        {
            std::shared_ptr<ICopyJobTicket> defaultCopyJobTicket = copyJobService_->getDefaultJobTicket();
            copyTicketAdapter = std::make_shared<CopyTicketAdapter>(defaultCopyJobTicket, copyJobService_);
            assert(copyJobConstraintsHelper_ != nullptr);
            copyTicketAdapter->setCopyJobConstraintsHelper(copyJobConstraintsHelper_);
            copyTicketAdapter->setCopyDynamicConstraintsHelper(copyDynamicConstraintsHelper_);
            copyTicketAdapter->setStaticConstrainsAreCached(staticConstrainsAreCached_);
            copyTicketAdapter->setValidateTicketOnSerialization(validateTicketOnSerialization_);
            copyTicketAdapter->setCopyConfigurationHelper(copyConfigurationHelper_);
            copyTicketAdapter->setLocaleProvider(localeProvider_);
        }
        else
        {
            // TODO - Implement for other JobTicketType
            copyTicketAdapter = nullptr;
        }
    }
    else
    {
        // TODO - throw an exception later.
        copyTicketAdapter = nullptr;
    }

    return copyTicketAdapter;
}

std::shared_ptr<ITicketAdapter> JobTicketResourceHelper::createTicketAdapter(
    const SerializedDataBufferPtr& serializedDataBuffer)
{
    // If there are multiple configuration supported, check configuration to provide the particular jobTicket i.e.
    // TicketAdapter
    std::shared_ptr<ICopyJobTicket> copyJobTicket = copyJobService_->deserializeJobTicket(serializedDataBuffer);
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, copyJobService_);
    assert(copyJobConstraintsHelper_ != nullptr);
    copyTicketAdapter->setCopyJobConstraintsHelper(copyJobConstraintsHelper_);
    copyTicketAdapter->setCopyDynamicConstraintsHelper(copyDynamicConstraintsHelper_);
    copyTicketAdapter->setStaticConstrainsAreCached(staticConstrainsAreCached_);
    copyTicketAdapter->setValidateTicketOnSerialization(validateTicketOnSerialization_);
    copyTicketAdapter->setCopyConfigurationHelper(copyConfigurationHelper_);
    copyTicketAdapter->setLocaleProvider(localeProvider_);
    
    return copyTicketAdapter;
};

std::shared_ptr<ITicketAdapter> JobTicketResourceHelper::createTicketAdapter(const Uuid& ticketID)
{
    std::shared_ptr<ICopyJobTicket> copyJobTicket = copyJobService_->getTicketFromCache(ticketID);
    if (copyJobTicket == nullptr)
    {
        return nullptr;
    }

    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, copyJobService_);
    assert(copyJobConstraintsHelper_ != nullptr);
    copyTicketAdapter->setCopyJobConstraintsHelper(copyJobConstraintsHelper_);
    copyTicketAdapter->setCopyDynamicConstraintsHelper(copyDynamicConstraintsHelper_);
    copyTicketAdapter->setStaticConstrainsAreCached(staticConstrainsAreCached_);
    copyTicketAdapter->setValidateTicketOnSerialization(validateTicketOnSerialization_);
    copyTicketAdapter->setCopyConfigurationHelper(copyConfigurationHelper_);
    copyTicketAdapter->setLocaleProvider(localeProvider_);
    
    return copyTicketAdapter;
};

}}}}  // namespace dune::copy::Jobs::Copy
