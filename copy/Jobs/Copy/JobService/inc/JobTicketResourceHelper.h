/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_JOB_TICKET_RESOURCE_HELPER_H
#define DUNE_COPY_JOBS_COPY_JOB_TICKET_RESOURCE_HELPER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobTicketResourceHelper.h
 * @date   Tue, 06 Aug 2019 12:14:22 +0530
 * @brief
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IJobTicketResourceHelper.h"
#include "IJobTicketResourceManager.h"
#include "JobServiceFactory.h"
#include "IJobConstraints.h"
#include "ICopyJobDynamicConstraintRules.h"
#include "ICopyAdapter.h"
#include "ILocaleProvider.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using dune::framework::core::Uuid;
using dune::job::Configuration;
using dune::job::IJobTicketResourceManager;
using dune::job::ITicketAdapter;
using dune::job::JobServiceFactory;
using dune::job::JobTicketType;

/**
 * Implementation of the Standard flavor of the JobTicketResourceHelper component.
 */
class JobTicketResourceHelper : public dune::job::IJobTicketResourceHelper
{
  public:
    /**
     * @name IJobTicketResourceHelper methods.
     * @{
     */

    std::shared_ptr<ITicketAdapter> createTicketAdapter(const Configuration &configuration, JobTicketType jobTicketType) override;

    std::shared_ptr<ITicketAdapter> createTicketAdapter(const SerializedDataBufferPtr &serializedDataBuffer) override;

    std::shared_ptr<ITicketAdapter> createTicketAdapter(const Uuid &ticketID) override;
    /**
     * @}
     */

    /**
     * @brief JobTicketResourceHelper Constructor.
     *
     * @param instanceName the name of the` component instance.
     */
    explicit JobTicketResourceHelper(JobServiceFactory<ICopyJobTicket> *jobService);

    /**
     * Destructor.
     */
    virtual ~JobTicketResourceHelper();

    // /**
    //  * Destructor.
    //  */
    // virtual ~JobTicketResourceHelper() = default;

    void registerHelper(IJobTicketResourceManager *jobTicketResourceManager);

    inline void setCopyJobConstraintsHelper(dune::copy::Jobs::Copy::IJobConstraints *helper) 
    { copyJobConstraintsHelper_ = helper; }

    inline void setCopyDynamicConstraintsHelper(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules *helper) 
    { copyDynamicConstraintsHelper_ = helper; }

    inline void setCopyConfigurationHelper(dune::copy::cdm::ICopyAdapter *helper) 
    { copyConfigurationHelper_ = helper; }

    /**
    * @brief set the local provider
    * @param localeProvider value to be set.
    */
    inline void setLocaleProvider(dune::localization::ILocaleProvider* localeProvider) 
    { localeProvider_ = localeProvider; }

    /**
     * @brief Variable that will notify ticket adapter that static constraints will be cached
     */
    bool staticConstrainsAreCached_{false};

    /**
     * @brief Variable to notify that ticket will be checked in serialization method
     */
    bool validateTicketOnSerialization_{false};

  private:
    JobServiceFactory<ICopyJobTicket> *copyJobService_;
    dune::copy::Jobs::Copy::IJobConstraints *copyJobConstraintsHelper_{ nullptr };
    dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules *copyDynamicConstraintsHelper_{ nullptr};
    dune::copy::cdm::ICopyAdapter *copyConfigurationHelper_{ nullptr };
    dune::localization::ILocaleProvider *localeProvider_{ nullptr };
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif  // DUNE_COPY_JOBS_COPY_JOB_TICKET_RESOURCE_HELPER_H
