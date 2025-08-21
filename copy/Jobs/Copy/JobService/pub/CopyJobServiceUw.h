/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_JOB_SERVICE_UW_H
#define DUNE_COPY_JOBS_COPY_JOB_SERVICE_UW_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobServiceUw.h
 * @date   Wed, 08 May 2019 11:36:41 -0700
 * @brief  JobService specific class to CopyJobs
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "string"

namespace dune { namespace copy { namespace Jobs { namespace Copy {
/**
 * @brief Interface exported to interpreters, also known as "underware
 * interface".
 */
class CopyJobServiceUw
{
public:

    /**
     * Destructor.
     */
    virtual ~CopyJobServiceUw() { }

    /**
     * Create a job with the default ticket
     *
     * @author Nadim Zubidat (10-May-19)
     *
     * @return const char* newly created job ID
     */
    virtual std::string PUB_createJob() = 0;

    /**
     * Create a job with a ticket
     *
     * @author Nadim Zubidat (10-May-19)
     *
     * @param ticketId of the ticket to create the job with
     *
     * @return const char* new created job ID
     */
    virtual std::string PUB_createJobWithTicket(const char *ticketId) = 0;

    /**
     * Create a job ticket
     *
     * @author Nadim Zubidat (10-May-19)
     *
     * @return const char* newly created job ticket ID
     */
    virtual std::string PUB_createJobTicket() = 0;

    /**
     * Create a job ticket
     *
     * @author Corey Norberg (01-30-20)
     * 
     * @param const char* source value for scan source and plex (adfsimplex, adfduplex, flatbed (assumes simplex))
     * 
     * @param const char* colorMode value for scan color mode (color, mono, auto)
     *
     */
    virtual void PUB_configureTicket(const char* ticketId, const char* source, const char* outputPlex, const char* colorMode, int64_t scale, const char* scanCaptureMode, int8_t nUp) = 0;

    /**
     * List created jobs
     *
     * @author Nadim Zubidat(10-May-19)
     *
     * @return const char* list of created jobs
     */
    virtual std::string PUB_listJobs() = 0;

    /**
     * List created job tickets
     *
     * @author Nadim Zubidat (10-May-19)
     *
     * @return const char* list of created job tickets
     */
    virtual std::string PUB_listJobTickets() = 0;

    /**
     * Initialize job
     *
     * @author Nadim Zubidat (14-May-19)
     *
     * @param jobId
     */
    virtual void PUB_initializeJob(const char* jobId) = 0;

    /**
     * Start job
     *
     * @author Nadim Zubidat (14-May-19)
     *
     * @param jobId
     */
    virtual void PUB_startJob(const char* jobId) = 0;

    /**
     * Cancel job
     *
     * @author Nadim Zubidat (14-May-19)
     *
     * @param jobId
     */
    virtual void PUB_cancelJob(const char* jobId) = 0;

    /**
     * Create and execute job with the default ticket
     * and wait for created, initializing, ready and completed events 
     *
     * @author om Singh (27-May-19)
     *
     * @return const char* newly created job ID
     */
    virtual std::string PUB_executeJob() = 0;

    /**
     * Create and execute job with the default ticket
     * and wait for created, initializing, ready and completed events 
     *
     * @author Corey Norberg (05-Feb-20)
     * 
     * @param const char* ticketId value returned from createJob
     *
     * @return const char* newly created job ID
     */
    virtual std::string PUB_executeJobWithTicket(const char* ticketId) = 0;

    /**
     * Create and execute job with the default ticket
     * and wait for created, initializing, ready and cancelled events 
     *
     * @author Corey Norberg (16-Jun-20)
     *
     * @return const char* newly created job ID
     */
    virtual std::string PUB_executeJobThenCancel(uint32_t secondsBeforeCancel) = 0;

    /**
     * This routine does the following sequence of commands:
     *  1. create a job ticket
     *  2. set some fields on it
     *  3. save it to the datastore via the JobService
     *  4. recover this very same ticket
     *  5. see if all fields match
     * 
     * @author Bruno Fontana Canella (10-Feb-20)
     * 
     * @return true when all fields match
     * @return false if something fails or if the fields mismatch
     */
    virtual bool PUB_persistJobTicketDemo() = 0;

    /**
     * Create and execute preview job with the default ticket
     * and wait for created, initializing, ready and completed events 
     *
     * @author Gwangeun Sim (19-Aug-21)
     *
     * @return const char* newly created job ID
     */
    virtual std::string PUB_executePreviewJob() = 0;

    /**
     * Create and execute preview job with the default ticket
     * and wait for created, initializing, ready and cancelled events
     *
     * @author Gwangeun Sim (23-Aug-21)
     *
     * @return const char* newly created job ID
     */
    virtual std::string PUB_executePreviewJobThenCancel(uint32_t secondsBeforeCancel) = 0;

    /**
     * Create and execute preview job with the default ticket
     * and wait for created, initializing, ready and continue copy job 
     *
     * @author Gwangeun Sim (23-Aug-21)
     *
     * @return const char* newly created job ID and ticket ID
     */
    virtual std::string PUB_executePreviewJobThenContinueCopy() = 0;

    /**
     * Create and execute preview job with the default ticket
     * and wait for created, initializing, ready and new preview job 
     *
     * @author Gwangeun Sim (23-Aug-21)
     *
     * @return const char* newly created job ID and ticket ID
     */
    virtual std::string PUB_executePreviewJobThenRedo() = 0;

    /**
     * Applicable to Devices with limited memory to store pages.
     * The 'Collate Problem' alert should appear once we scan the max collate pages.
     * @return the maxPagesToCollate value; 0 = no limit.
     */
    virtual int PUB_setMaxPagesToCollate(int val) = 0;

    // returns a helpful message
    virtual std::string PUB_getHelpMessage()
    {
        std::string retVal = 
        "CopyJobServiceUw Help:\n"
        "The various PUB_xxxJob functions operate only on jobs created with this service. The actual Job Queue is not Queried\n"
        "jobId    PUB_createJob()\n"
        "ticketId PUB_createJobWithTicket(string ticketId)\n"
        "ticketId PUB_createJobTicket()\n"
        "void   PUB_configureTicket(string ticketId, string source, string outputPlex, string colorMode, int64_t scale, string scanCaptureMode, int8_t nUp)\n"
        "string PUB_listJobs()\n"
        "string PUB_listJobTickets()\n"
        "void   PUB_initializeJob(string jobId)\n"
        "void   PUB_startJob(string jobId)\n"
        "void   PUB_cancelJob(string jobId)\n"
        "jobId  PUB_executeJob()\n"
        "jobId  PUB_executeJobWithTicket(string ticketId)\n"
        "jobId  PUB_executeJobThenCancel(uint32_t secondsBeforeCancel)\n"
        "bool   PUB_persistJobTicketDemo()  // true when all fields match; false if something fails or if the fields mismatch\n"
        "jobId  PUB_executePreviewJob() \n"
        "jobId  PUB_executePreviewJobThenCancel(uint32_t secondsBeforeCancel)\n"
        "jobId  PUB_executePreviewJobThenContinueCopy()\n"
        "jobId,ticketId PUB_executePreviewJobThenRedo()\n"
        "int    PUB_setMaxPagesToCollate(int val)   // sets the max pages that can be collated on this device.\n"
        "//               The 'Collate Problem' alert should appear once we scan the max collate pages.\n"
        ;
        return retVal;
    }
};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_JOB_SERVICE_UW_H

