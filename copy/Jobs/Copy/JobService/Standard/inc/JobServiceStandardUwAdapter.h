/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_JOB_SERVICE_STANDARD_UW_ADAPTER_H
#define DUNE_COPY_JOBS_COPY_JOB_SERVICE_STANDARD_UW_ADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobServiceStandardUwAdapter.h
 * @date   Wed, 08 May 2019 11:36:41 -0700
 * @brief  JobService specific class to CopyJobs
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "Job.h"
#include "IJob.h"
#include "CopyJobServiceUw.h"
#include "JobServiceStandard.h"

#include "InterpreterEnvironment.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * Underware object adapter between CopyJobServiceUw and JobServiceStandard.
 */
class JobServiceStandardUwAdapter: public CopyJobServiceUw
{
public:

    /**
     * Constructor.
     *
     * @param instanceName name of the instance exported to the interpreter.
     * @param adaptee pointer to the JobServiceStandard instance.
     */
    JobServiceStandardUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment, const std::string & instanceName, JobServiceStandard * adaptee );

    /**
     * Destructor.
     */
    virtual ~JobServiceStandardUwAdapter();

    /**
     * @name CopyJobServiceUw methods.
     * @{
     */

    std::string PUB_createJob() override final;

    std::string PUB_createJobWithTicket(const char* ticketId) override final;

    std::string PUB_createJobTicket() override final;

    void PUB_configureTicket(const char* ticketId, const char* source, const char* outputPlex, const char* colorMode, int64_t scale, const char* scanCaptureMode, int8_t nUp) override final;

    std::string PUB_listJobs() override final;

    std::string PUB_listJobTickets() override final;

    void PUB_initializeJob(const char* jobId) override final;

    void PUB_startJob(const char* jobId) override final;

    void PUB_cancelJob(const char* jobId) override final;

    std::string PUB_executeJob() override final;

    std::string PUB_executeJobWithTicket(const char* ticketId) override final;

    std::string PUB_executeJobThenCancel(uint32_t secondsBeforeCancel) override final;
    
    bool PUB_persistJobTicketDemo() override final;

    std::string PUB_executePreviewJob() override final;

    std::string PUB_executePreviewJobThenCancel(uint32_t secondsBeforeCancel) override final;

    std::string PUB_executePreviewJobThenContinueCopy() override final;

    std::string PUB_executePreviewJobThenRedo() override final;

    int PUB_setMaxPagesToCollate(int val) override final;

    /**
     * @}
     */

private:
    std::string registerName_;
    dune::framework::underware::InterpreterEnvironment * interpreterEnvironment_;
    JobServiceStandard * adaptee_{nullptr}; ///< Pointer to the underlying JobServiceStandard object.

    // map of Job ID's to job tickets
    std::map<std::string, std::shared_ptr<ICopyJobTicket>> jobTickets_;

    // map of Job ID's to jobs
    std::map<std::string, std::shared_ptr<dune::job::IJob>> jobs_;

    std::condition_variable condVar{};
    std::mutex              condVarMutex{};

    void handleJobEvent(const std::shared_ptr<dune::job::IJob> j);

    bool waitForJobEvent(std::shared_ptr<dune::job::IJob> job, dune::job::JobStateType state);

};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_JOB_SERVICE_STANDARD_UW_ADAPTER_H
