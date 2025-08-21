/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobServiceStandardUwAdapter.cpp
 * @date   Wed, 08 May 2019 11:36:41 -0700
 * @brief  JobService specific class to CopyJobs
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////


#include "JobServiceStandardUwAdapter.h"
#include "IJob.h"

#include <chrono>
#include <condition_variable>
#include <functional>
#include <iostream>
#include <sstream>
#include <thread>

#include "common_debug.h"

#include "JobServiceStandardUwAdapter_TraceAutogen.h"

#include "Interpreter.h"
#include "JobServiceExtension.h"
#include "JobFrameworkTypes.h"
#include "JobFrameworkBaseTypes.h"

using dune::job::JobEvent;
using dune::job::TicketUpdationMode;

namespace dune { namespace copy { namespace Jobs { namespace Copy {

JobServiceStandardUwAdapter::JobServiceStandardUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment, const std::string & instanceName, JobServiceStandard * adaptee )
: registerName_(instanceName), interpreterEnvironment_(interpreterEnvironment), adaptee_( adaptee )
{
    // Register the extension
    interpreterEnvironment_->addExtension( JobServiceExtension::instance() );

    // Register this instance
    interpreterEnvironment_->addInstance(
        dune::framework::underware::InterpreterInstance(
            static_cast<CopyJobServiceUw*>(this), registerName_,
            "dune__copy__Jobs__Copy__CopyJobServiceUw", "CopyJobServiceUw"
        ));
}

JobServiceStandardUwAdapter::~JobServiceStandardUwAdapter()
{
    interpreterEnvironment_->removeInstance(registerName_);
}

std::string JobServiceStandardUwAdapter::PUB_createJob()
{
    auto ticket = adaptee_->getDefaultJobTicket();
    //ticket->setStorePath("/tmp/");

    auto job = adaptee_->createJob(ticket);
    if (job)
    {
        // Save job and return its ID
        jobs_[job->getJobId().toString(false)] = job;
        // Subscribe to JobStateChanged events
        job->getJobStateChanged().addSubscription([this](std::shared_ptr<dune::job::IJob> job) { handleJobEvent(job); });

        waitForJobEvent(job, dune::job::JobStateType::CREATED);
        CHECKPOINTB("Job %s CREATED", job->getJobId().toString(false).c_str());

        job->initialize();

        waitForJobEvent(job, dune::job::JobStateType::INITIALIZING);
        CHECKPOINTB("Job %s INITIALIZING", job->getJobId().toString(false).c_str());

        waitForJobEvent(job, dune::job::JobStateType::READY);
        CHECKPOINTB("Job %s READY", job->getJobId().toString(false).c_str());

        return job->getJobId().toString(false).c_str();
    }
    else
    {
        // Job creation failed
        CHECKPOINTB("Failed creating Copy job");
        return "Failed creating Copy job";
    }
}

std::string JobServiceStandardUwAdapter::PUB_createJobWithTicket(const char* ticketId)
{
    auto search = jobTickets_.find(ticketId);
    if (search != jobTickets_.end())
    {
        auto job = adaptee_->createJob(search->second);
        if (job)
        {
            // Save job and return its ID
            jobs_[job->getJobId().toString(false)] = job;

            CHECKPOINTB("Job %s created", job->getJobId().toString(false).c_str());
            return job->getJobId().toString(false).c_str();
        }
        else
        {
            // Job creation failed
            CHECKPOINTB("Failed creating Copy job");
            return "Failed creating Copy job";
        }
    }

    // Job ticket not found
    CHECKPOINTB("Job ticket not found\n");
    return "Job ticket not found";
}

std::string JobServiceStandardUwAdapter::PUB_createJobTicket()
{
    auto jobTicket = adaptee_->getDefaultJobTicket();
    if (jobTicket)
    {
        // Save job ticket and return its ID
        jobTickets_[jobTicket->getTicketId().toString(false)] = jobTicket;

        CHECKPOINTB("Job ticket %s created", jobTicket->getJobId().toString(false).c_str());
        return jobTicket->getTicketId().toString(false).c_str();
    }
    else
    {
        // Job ticket creation failed
        CHECKPOINTB("Failed creating job ticket");
        return "Failed creating Copy job ticket";
    }
}

void JobServiceStandardUwAdapter::PUB_configureTicket(const char* ticketId,
                                                      const char* source,
                                                      const char* outputPlex,
                                                      const char* colorMode,
                                                      int64_t scale,
                                                      const char* scanCaptureMode,
                                                      int8_t nUp)
{
    CHECKPOINTB("configureTicket:Finding job ticket %s and setting the source to %s", ticketId, source);
    auto search = jobTickets_.find(ticketId);
    if (search != jobTickets_.end())
    {
        //Ticket found
        CHECKPOINTB("configureTicket::TicketFound");
        std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket = search->second;
        auto intent = jobTicket->getIntent();
        auto copyIntent = static_cast<std::shared_ptr<ICopyJobIntent>>(intent);

        // Setup the plex and source for the scan
        if (strcmp(source, "adfsimplex") == 0)
        {
            CHECKPOINTB("configureTicket::ADF Simplex job set");
            copyIntent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
            copyIntent->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
        }
        else if (strcmp(source, "adfduplex") == 0)
        {
            CHECKPOINTB("configureTicket::ADF Duplex job set");
            copyIntent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
            copyIntent->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
        }
        else if (strcmp(source, "glassduplex") == 0)
        {
            CHECKPOINTB("configureTicket::Flatbed Duplex job set");
            copyIntent->setScanSource(dune::scan::types::ScanSource::GLASS);
            copyIntent->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
        }
        else
        {
            CHECKPOINTB("configureTicket::Flatbed job set");
            copyIntent->setScanSource(dune::scan::types::ScanSource::GLASS);
            copyIntent->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
        }

        if (strcmp(outputPlex, "duplex") == 0)
        {
            copyIntent->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
        }
        else
        {
            copyIntent->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
        }

        // Setup the color mode for the scan
        if (strcmp(colorMode, "color") == 0)
        {
            CHECKPOINTB("configureTicket::setColorMode to Color");
            copyIntent->setColorMode(dune::imaging::types::ColorMode::COLOR);
        }
        else if (strcmp(colorMode, "grayscale") == 0)
        {
            CHECKPOINTB("configureTicket::setColorMode to Grayscale");
            copyIntent->setColorMode(dune::imaging::types::ColorMode::GRAYSCALE);
        }
        else if (strcmp(colorMode, "mono") == 0)
        {
            CHECKPOINTB("configureTicket::setColorMode to Mono");
            copyIntent->setColorMode(dune::imaging::types::ColorMode::MONOCHROME);
        }
        else 
        {
            CHECKPOINTB("configureTicket::setColorMode to Auto");
            copyIntent->setColorMode(dune::imaging::types::ColorMode::AUTODETECT);
        }

        // Setup scale factor
        CHECKPOINTB("configureTicket::setScalePercent : %llu \n ", (long long unsigned)scale);
        copyIntent->setXScalePercent(scale);
        copyIntent->setYScalePercent(scale);

        // Setup ScanCaptureModeType
        if (strcmp(scanCaptureMode, "idcard") == 0)
        {
            copyIntent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
        }
        else
        {
            copyIntent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::STANDARD);
        }
        //n-up mode
        if(nUp == 2)
        {
            copyIntent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
        }
        else
        {
            copyIntent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::OneUp);
        }
    }
    else
    {
        // Job ticket not found
        CHECKPOINTB("configureTicket:Job ticket not found\n");
    }
}

std::string JobServiceStandardUwAdapter::PUB_listJobs()
{
    std::stringstream jobList;

    for (const auto& job : jobs_)
    {
        jobList << job.second->getJobId().toString(false) << " : " << EnumNameJobStateType(job.second->getStateType());
        jobList << "\n";
    }

    CHECKPOINTB("%s", jobList.str().c_str());
    return jobList.str().c_str();
}

std::string JobServiceStandardUwAdapter::PUB_listJobTickets()
{
    std::stringstream jobTicketList;

    for (const auto& jobTicket : jobTickets_)
    {
        jobTicketList << jobTicket.second->getTicketId().toString(false) << " : "
                      << EnumNameJobStateType(jobTicket.second->getState());
        jobTicketList << "\n";
    }

    CHECKPOINTB("%s", jobTicketList.str().c_str());
    return jobTicketList.str().c_str();
}

void JobServiceStandardUwAdapter::PUB_initializeJob(const char* jobId)
{
    auto search = jobs_.find(jobId);
    if (search != jobs_.end())
    {
        auto job = search->second;

        CHECKPOINTB("Initializing job %s", job->getJobId().toString(false).c_str());
        job->initialize();

        return;
    }

    // Job not found
    CHECKPOINTB("Job not found");
}

void JobServiceStandardUwAdapter::PUB_startJob(const char* jobId)
{
    auto search = jobs_.find(jobId);
    if (search != jobs_.end())
    {
        auto job = search->second;

        CHECKPOINTB("Starting job %s", job->getJobId().toString(false).c_str());
        job->start();

        return;
    }

    // Job not found
    CHECKPOINTB("Job not found");
}

void JobServiceStandardUwAdapter::PUB_cancelJob(const char* jobId)
{
    auto search = jobs_.find(jobId);
    if (search != jobs_.end())
    {
        auto job = search->second;

        CHECKPOINTB("Canceling job %s", job->getJobId().toString(false).c_str());
        job->cancel();

        return;
    }

    // Job not found
    CHECKPOINTB("Job not found");
}

std::string JobServiceStandardUwAdapter::PUB_executeJob()
{    
    auto ticket = adaptee_->getDefaultJobTicket();
    auto job = adaptee_->createJob(ticket);
    bool completed{false};    

    if (job)
    {
        // Subscribe to JobStateChanged events
        JobEvent::SubscriptionId hasCompletedId =
            job->getJobStateChanged().addSubscription([this](std::shared_ptr<dune::job::IJob> job) { handleJobEvent(job); });

        if( waitForJobEvent(job, dune::job::JobStateType::CREATED) )
        {
            CHECKPOINTB("Job %s CREATED", job->getJobId().toString(false).c_str());

            job->initialize();

            //if( waitForJobEvent(job, dune::job::JobStateType::INITIALIZING) )
            //{
                //CHECKPOINTB("Job %s INITIALIZING", job->getJobId().toString(false).c_str());

                if( waitForJobEvent(job, dune::job::JobStateType::READY) )
                {
                    CHECKPOINTB("Job %s READY", job->getJobId().toString(false).c_str());
                    job->start();
                    CHECKPOINTB("Job %s started", job->getJobId().toString(false).c_str());

                    if( waitForJobEvent(job, dune::job::JobStateType::COMPLETED) )
                    {
                        CHECKPOINTB("Job %s COMPLETED", job->getJobId().toString(false).c_str());
                        completed=true;
                    }
                }
            //}

        }

        job->getJobStateChanged().removeSubscription(hasCompletedId);
        if( completed == true )
        {
            return job->getJobId().toString(false).c_str();
        }
        else
        {
            return std::string("FAILED");
        }


    }
    else
    {
        // Job creation failed
        CHECKPOINTB("Failed executed Copy job");
        return "Failed executed Copy job";
    }
}

std::string JobServiceStandardUwAdapter::PUB_executeJobWithTicket(const char* ticketId)
{
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket;
    auto search = jobTickets_.find(ticketId);
    if (search != jobTickets_.end())
    {
        ticket = search->second;
    }
    else 
    {
        // Job ticket not found
        CHECKPOINTB("executeJobWithTicket:Job ticket not found\n");
    }
    auto job = adaptee_->createJob(ticket);
    bool completed{false};

    if (job)
    {
        // Subscribe to JobStateChanged events
        JobEvent::SubscriptionId hasCompletedId =
            job->getJobStateChanged().addSubscription([this](std::shared_ptr<dune::job::IJob> job) { handleJobEvent(job); });

        if( waitForJobEvent(job, dune::job::JobStateType::CREATED) )
        {
            CHECKPOINTB("executeJobWithTicket:Job %s CREATED", job->getJobId().toString(false).c_str());

            job->initialize();
            if( waitForJobEvent(job, dune::job::JobStateType::READY) )
            {
                CHECKPOINTB("executeJobWithTicket:Job %s READY", job->getJobId().toString(false).c_str());

                job->start();
                CHECKPOINTB("executeJobWithTicket:Job %s started", job->getJobId().toString(false).c_str());

                if( waitForJobEvent(job, dune::job::JobStateType::COMPLETED) )
                {
                    CHECKPOINTB("executeJobWithTicket:Job %s COMPLETED", job->getJobId().toString(false).c_str());
                    completed=true;
                }
            }
        }

        job->getJobStateChanged().removeSubscription(hasCompletedId);
        if( completed == true )
        {
            return job->getJobId().toString(false).c_str();
        }
        else
        {
            return "executeJobWithTicket:Job failed to complete";
        }
    }
    else
    {
        // Job creation failed
        CHECKPOINTB("Failed to create Copy job");
        return "Failed to create Copy job";
    }
}

std::string JobServiceStandardUwAdapter::PUB_executeJobThenCancel(uint32_t secondsBeforeCancel)
{
    auto ticket = adaptee_->getDefaultJobTicket();
    auto job = adaptee_->createJob(ticket);
    bool completed{false};

    if (job)
    {
        // Subscribe to JobStateChanged events
        JobEvent::SubscriptionId hasCompletedId =
            job->getJobStateChanged().addSubscription([this](std::shared_ptr<dune::job::IJob> job) { handleJobEvent(job); });

        if( waitForJobEvent(job, dune::job::JobStateType::CREATED) )
        {
            CHECKPOINTB("Job %s CREATED", job->getJobId().toString(false).c_str());

            job->initialize();

            if( waitForJobEvent(job, dune::job::JobStateType::READY) )
            {
                CHECKPOINTB("Job %s READY", job->getJobId().toString(false).c_str());

                job->start();
                CHECKPOINTB("Job %s started", job->getJobId().toString(false).c_str());

                if( waitForJobEvent(job, dune::job::JobStateType::PROCESSING) )
                {
                    CHECKPOINTB("Job %s PROCESSING", job->getJobId().toString(false).c_str());
                }
                std::this_thread::sleep_for(std::chrono::seconds(secondsBeforeCancel));
                job->cancel();
                if( waitForJobEvent(job, dune::job::JobStateType::CANCELING) )
                {
                    CHECKPOINTB("Job %s CANCELING", job->getJobId().toString(false).c_str());
                }
                if( waitForJobEvent(job, dune::job::JobStateType::COMPLETED) )
                {
                    CHECKPOINTB("Job %s CANCELED", job->getJobId().toString(false).c_str());
                    completed = true;
                }
            }
        }

        job->getJobStateChanged().removeSubscription(hasCompletedId);
        if( completed == true )
        {
            return job->getJobId().toString(false).c_str();
        }
        else
        {
            return std::string("FAILED");
        }
    }
    else
    {
        // Job creation failed
        CHECKPOINTB("Failed executed Copy job");
        return "Failed executed Copy job";
    }
}

bool JobServiceStandardUwAdapter::PUB_persistJobTicketDemo()
{
    // (1). Creating a ticket
    auto ticketSave = adaptee_->getDefaultJobTicket();

    // (2). Setting data into the ticket
    // Ticket:
    const auto TICKET_JOB_ID = dune::framework::core::Uuid{"557c10b7-e752-45a3-80c0-7e604f7af170"};
    const auto TICKET_ORDINAL = 99;
    const auto TICKET_STATE = dune::job::JobStateType::PROCESSING;
    const auto TICKET_COMPLETION_STATE = dune::job::CompletionStateType::SUCCESS;
    const auto TICKET_PRIORITY = dune::job::JobPriorityType::HIGH;
    const auto TICKET_JOB_NAME = "this is a ticket name!";
    const auto TICKET_STORE_PATH = "/in/my/pocket";
    ticketSave->setJobId(TICKET_JOB_ID);
    ticketSave->setOrdinal(TICKET_ORDINAL);
    ticketSave->setState(TICKET_STATE);
    ticketSave->setCompletionState(TICKET_COMPLETION_STATE);
    ticketSave->setPriority(TICKET_PRIORITY);
    ticketSave->setJobName(TICKET_JOB_NAME);
    ticketSave->setStorePath(TICKET_STORE_PATH);
    // Intent:
    auto intentSave = ticketSave->getIntent();
    // Intent: Copy
    const auto OUTPUT_MEDIA_SIZE_ID = dune::imaging::types::MediaSizeId::A6;
    const auto OUTPUT_MEDIA_ID_TYPE = dune::imaging::types::MediaIdType::COLORED;
    const auto OUTPUT_MEDIA_SOURCE = dune::imaging::types::MediaSource::MANUALFEED;
    const auto OUTPUT_PLEX_MODE = dune::imaging::types::Plex::DUPLEX;
    const auto OUTPUT_PLEX_BINDING = dune::imaging::types::PlexBinding::LONG_EDGE;
    const auto COPIES = 3;
    const auto COLLATE = dune::copy::SheetCollate::Collate;
    intentSave->setOutputMediaSizeId(OUTPUT_MEDIA_SIZE_ID);
    intentSave->setOutputMediaIdType(OUTPUT_MEDIA_ID_TYPE);
    intentSave->setOutputMediaSource(OUTPUT_MEDIA_SOURCE);
    intentSave->setOutputPlexMode(OUTPUT_PLEX_MODE);
    intentSave->setOutputPlexBinding(OUTPUT_PLEX_BINDING);
    intentSave->setCopies(COPIES);
    intentSave->setCollate(COLLATE);
    // Intent: Scan
    const auto INPUT_MEDIA_SIZE_ID = dune::imaging::types::MediaSizeId::US_EXECUTIVE;
    const auto INPUT_PLEX_MODE = dune::imaging::types::Plex::SIMPLEX;
    const auto OUTPUT_X_RESOLUTION = dune::imaging::types::Resolution::E600DPI;
    const auto OUTPUT_Y_RESOLUTION = dune::imaging::types::Resolution::E600DPI;
    const auto QUALITY_MODE = dune::scan::types::AttachmentSize::SMALL;
    const auto COLOR_MODE = dune::imaging::types::ColorMode::BLACKANDWHITE;
    const auto CONTENT_ORIENTATION = dune::imaging::types::ContentOrientation::REVERSELANDSCAPE;
    const auto BACKSIDE_CONTENT_ORIENTATION = dune::imaging::types::ContentOrientation::PORTRAIT;
    const auto ORIGINAL_CONTENT_TYPE = dune::imaging::types::OriginalContentType::TEXT;
    const auto ORIGINAL_MEDIA_TYPE = dune::scan::types::OriginalMediaType::BLUEPRINTS;
    const auto SCAN_SOURCE = dune::scan::types::ScanSource::ADF_SIMPLEX;
    const auto SCAN_FEED_ORIENTATION = dune::scan::types::ScanFeedOrientation::LONGEDGE;
    const auto SCAN_X_RESOLUTION = dune::imaging::types::Resolution::E150DPI;
    const auto SCAN_Y_RESOLUTION = dune::imaging::types::Resolution::E100DPI;
    const auto MULTIPICK_DETECTION = true;
    const auto JOB_SCAN_LIMIT = 11;
    const auto AUTO_CROP = true;
    const auto AUTO_TONE = true;
    const auto BLANK_PAGE_DETECTION = dune::scan::types::BlankDetectEnum::DetectOnly;
    const auto BRIGHTNESS = 12;
    const auto CONTRAST = 13;
    const auto SHARPEN = 14;
    const auto OFFSET = 15;
    const auto BACKGROUND_REMOVAL = false;
    const auto OVER_SCAN = dune::scan::types::OverScanType::TOPANDBOTTOM;
    const auto SCAN_CAPTURE_MODE = dune::scan::types::ScanCaptureModeType::IDCARD;
    const auto SCAN_IMAGE_PROFILE = dune::scan::types::ScanImagingProfileType::COPY;
    intentSave->setInputMediaSizeId(INPUT_MEDIA_SIZE_ID);
    intentSave->setInputPlexMode(INPUT_PLEX_MODE);
    intentSave->setOutputXResolution(OUTPUT_X_RESOLUTION);
    intentSave->setOutputYResolution(OUTPUT_Y_RESOLUTION);
    intentSave->setQualityMode(QUALITY_MODE);
    intentSave->setColorMode(COLOR_MODE);
    intentSave->setContentOrientation(CONTENT_ORIENTATION);
    intentSave->setBackSideContentOrientation(BACKSIDE_CONTENT_ORIENTATION);
    intentSave->setOriginalContentType(ORIGINAL_CONTENT_TYPE);
    intentSave->setOriginalMediaType(ORIGINAL_MEDIA_TYPE);
    intentSave->setScanSource(SCAN_SOURCE);
    intentSave->setScanFeedOrientation(SCAN_FEED_ORIENTATION);
    intentSave->setScanXResolution(SCAN_X_RESOLUTION);
    intentSave->setScanYResolution(SCAN_Y_RESOLUTION);
    intentSave->setMultipickDetection(MULTIPICK_DETECTION);
    intentSave->setJobScanLimit(JOB_SCAN_LIMIT);
    intentSave->setAutoCrop(AUTO_CROP);
    intentSave->setAutoTone(AUTO_TONE);
    intentSave->setBlankPageDetection(BLANK_PAGE_DETECTION);
    intentSave->setBrightness(BRIGHTNESS);
    intentSave->setContrast(CONTRAST);
    intentSave->setSharpen(SHARPEN);    
    intentSave->setXOffset(OFFSET);
    intentSave->setYOffset(OFFSET);
    intentSave->setXExtend(OFFSET);
    intentSave->setYExtend(OFFSET);
    intentSave->setBackgroundRemoval(BACKGROUND_REMOVAL);
    intentSave->setOverScan(OVER_SCAN);
    intentSave->setScanCaptureMode(SCAN_CAPTURE_MODE);
    intentSave->setScanImagingProfile(SCAN_IMAGE_PROFILE);

    ticketSave->setIntent(intentSave);
    // (3). Saving
    if (adaptee_->saveDefaultJobTicket(ticketSave, TicketUpdationMode::internal))
    {
        // (4). Recovering it
        auto ticketLoad = adaptee_->getDefaultJobTicket();
        
        // (5). Checking if equal
        // Ticket:
        assert(ticketLoad->getJobId() == TICKET_JOB_ID);
        assert(ticketLoad->getOrdinal() == TICKET_ORDINAL);
        assert(ticketLoad->getState() == TICKET_STATE);
        assert(ticketLoad->getCompletionState() == TICKET_COMPLETION_STATE);
        assert(ticketLoad->getPriority() == TICKET_PRIORITY);
        assert(ticketLoad->getJobName() == TICKET_JOB_NAME);
        assert(ticketLoad->getStorePath() == TICKET_STORE_PATH);
        // Intent:
        auto intentLoad = ticketLoad->getIntent();
        // Intent: Copy
        assert(intentLoad->getOutputMediaSizeId() == OUTPUT_MEDIA_SIZE_ID);
        assert(intentLoad->getOutputMediaIdType() == OUTPUT_MEDIA_ID_TYPE);
        assert(intentLoad->getOutputMediaSource() == OUTPUT_MEDIA_SOURCE);
        assert(intentLoad->getOutputPlexMode() == OUTPUT_PLEX_MODE);
        assert(intentLoad->getOutputPlexBinding() == OUTPUT_PLEX_BINDING);
        assert(intentLoad->getCopies() == COPIES);
        assert(intentLoad->getCollate() == COLLATE);
        // Intent: Scan
        assert(intentLoad->getInputMediaSizeId() == INPUT_MEDIA_SIZE_ID);
        assert(intentLoad->getInputPlexMode() == INPUT_PLEX_MODE);
        assert(intentSave->getOutputXResolution() == OUTPUT_X_RESOLUTION);
        assert(intentSave->getOutputYResolution() == OUTPUT_Y_RESOLUTION);
        assert(intentLoad->getQualityMode() == QUALITY_MODE);
        assert(intentLoad->getColorMode() == COLOR_MODE);
        assert(intentLoad->getContentOrientation() == CONTENT_ORIENTATION);
        assert(intentLoad->getBackSideContentOrientation() == BACKSIDE_CONTENT_ORIENTATION);
        assert(intentLoad->getOriginalContentType() == ORIGINAL_CONTENT_TYPE);
        assert(intentLoad->getOriginalMediaType() == ORIGINAL_MEDIA_TYPE);
        assert(intentLoad->getScanSource() == SCAN_SOURCE);
        assert(intentLoad->getScanFeedOrientation() == SCAN_FEED_ORIENTATION);
        assert(intentLoad->getScanXResolution() == SCAN_X_RESOLUTION);
        assert(intentLoad->getScanYResolution() == SCAN_Y_RESOLUTION);
        assert(intentLoad->getMultipickDetection() == MULTIPICK_DETECTION);
        assert(intentLoad->getJobScanLimit() == JOB_SCAN_LIMIT);
        assert(intentLoad->getAutoCrop() == AUTO_CROP);
        assert(intentLoad->getAutoTone() == AUTO_TONE);
        assert(intentLoad->getBlankPageDetection() == BLANK_PAGE_DETECTION);
        assert(intentLoad->getBrightness() == BRIGHTNESS);
        assert(intentLoad->getContrast() == CONTRAST);
        assert(intentLoad->getSharpen() == SHARPEN);
        assert(intentLoad->getXOffset() == OFFSET);
        assert(intentLoad->getYOffset() == OFFSET);
        assert(intentLoad->getXExtend() == OFFSET);
        assert(intentLoad->getYExtend() == OFFSET);
        assert(intentLoad->getBackgroundRemoval() == BACKGROUND_REMOVAL);
        assert(intentLoad->getOverScan() == OVER_SCAN);
        assert(intentLoad->getScanCaptureMode() == SCAN_CAPTURE_MODE);
        assert(intentLoad->getScanImagingProfile() == SCAN_IMAGE_PROFILE);

        return true;
    }
    else
    {
        CHECKPOINTB("Save default ticket failed");
        return false;
    }

}

void JobServiceStandardUwAdapter::handleJobEvent(const std::shared_ptr<dune::job::IJob> j)
{
    CHECKPOINTA("ENTER - IJob state event\n");
    CHECKPOINTA("Job state event: %d", static_cast<int32_t>(j->getStateType()));
    condVar.notify_all();
    CHECKPOINTA("EXIT - IJob state event\n");
}

bool JobServiceStandardUwAdapter::waitForJobEvent(const std::shared_ptr<dune::job::IJob> job,
                                                  dune::job::JobStateType                state)
{
    using namespace std::chrono_literals;
    int  count{2};
    bool found{false};
    std::unique_lock<std::mutex> lock{condVarMutex};

    //condVar.wait_for(lock, 100ms, [job, &state, &count]() { return job->getStateType() == state || count < 1; });
    CHECKPOINTB("Copy UDW waitForJobEvent: Request Wait For - JobStateType.%d\n", static_cast<int>(state));
    if( job->getStateType() != state )
    {
        CHECKPOINTB("Copy UDW waitForJobEvent: Waiting for - JobStateType.%d\n", static_cast<int>(state));
        while( count-- > 0 && found == false)
        {
            if( condVar.wait_for(lock, 20000ms, [job, &state] { return job->getStateType() == state; }))
            {
                CHECKPOINTB("Copy UDW waitForJobEvent: Done Waiting - JobStateType.%d\n", static_cast<int>(job->getStateType()));
                found = true;
            }
            else
            {
                CHECKPOINTB("Copy UDW waitForJobEvent: Still Waiting - JobStateType.%d\n", static_cast<int>(job->getStateType()));
            }
        }
    }
    else
    {
        CHECKPOINTB("Copy UDW waitForJobEvent: Current - JobStateType.%d\n", static_cast<int>(job->getStateType()));
        found = true;
    }

    if( found == false )
    {
        CHECKPOINTB("Copy UDW waitForJobEvent: Never transitioned to desired state");
    }

    return found;
}

std::string JobServiceStandardUwAdapter::PUB_executePreviewJob()
{
    auto ticket = adaptee_->getDefaultJobTicket();
    auto job = adaptee_->createJob(ticket);
    bool completed{false};

    if (job)
    {
        // Subscribe to JobStateChanged events
        JobEvent::SubscriptionId hasCompletedId =
            job->getJobStateChanged().addSubscription([this](std::shared_ptr<dune::job::IJob> job) { handleJobEvent(job); });

        if( waitForJobEvent(job, dune::job::JobStateType::CREATED) )
        {
            CHECKPOINTB("PUB_executePreviewJob Job %s CREATED", job->getJobId().toString(false).c_str());

            job->initialize();

            if( waitForJobEvent(job, dune::job::JobStateType::READY) )
            {
                CHECKPOINTB("PUB_executePreviewJob Job %s READY", job->getJobId().toString(false).c_str());

                job->start(SegmentType::PrepareSegment);
                CHECKPOINTB("PUB_executePreviewJob Job %s started", job->getJobId().toString(false).c_str());

                if( waitForJobEvent(job, dune::job::JobStateType::PROCESSING) )
                {
                    CHECKPOINTB("PUB_executePreviewJob Job %s PROCESSING", job->getJobId().toString(false).c_str());
                    
                    if( waitForJobEvent(job, dune::job::JobStateType::READY) )
                    {
                        CHECKPOINTB("PUB_executePreviewJob Job %s READY again", job->getJobId().toString(false).c_str());
                        completed=true;
                    }
                }
            }

        }

        job->getJobStateChanged().removeSubscription(hasCompletedId);
        if( completed == true )
        {
            return job->getJobId().toString(false).c_str();
        }
        else
        {
            return std::string("FAILED");
        }


    }
    else
    {
        // Job creation failed
        CHECKPOINTB("PUB_executePreviewJob Failed executed Copy Preview job");
        return "Failed executed Copy Preview job";
    }
}

std::string JobServiceStandardUwAdapter::PUB_executePreviewJobThenCancel(uint32_t secondsBeforeCancel)
{
    auto ticket = adaptee_->getDefaultJobTicket();
    auto job = adaptee_->createJob(ticket);
    bool completed{false};

    if (job)
    {
        // Subscribe to JobStateChanged events
        JobEvent::SubscriptionId hasCompletedId =
            job->getJobStateChanged().addSubscription([this](std::shared_ptr<dune::job::IJob> job) { handleJobEvent(job); });

        if( waitForJobEvent(job, dune::job::JobStateType::CREATED) )
        {
            CHECKPOINTB("PUB_executePreviewJobThenCancel Job %s CREATED", job->getJobId().toString(false).c_str());

            job->initialize();

            if( waitForJobEvent(job, dune::job::JobStateType::READY) )
            {
                CHECKPOINTB("PUB_executePreviewJobThenCancel Job %s READY", job->getJobId().toString(false).c_str());

                job->start(SegmentType::PrepareSegment);
                CHECKPOINTB("PUB_executePreviewJobThenCancel Job %s started", job->getJobId().toString(false).c_str());

                if( waitForJobEvent(job, dune::job::JobStateType::PROCESSING) )
                {
                    CHECKPOINTB("PUB_executePreviewJobThenCancel Job %s PROCESSING", job->getJobId().toString(false).c_str());
                }
                std::this_thread::sleep_for(std::chrono::seconds(secondsBeforeCancel));
                job->cancel();
                if( waitForJobEvent(job, dune::job::JobStateType::CANCELING) )
                {
                    CHECKPOINTB("PUB_executePreviewJobThenCancel Job %s CANCELING", job->getJobId().toString(false).c_str());
                }
                if( waitForJobEvent(job, dune::job::JobStateType::COMPLETED) )
                {
                    CHECKPOINTB("PUB_executePreviewJobThenCancel Job %s CANCELED", job->getJobId().toString(false).c_str());
                    completed = true;
                }
            }
        }

        job->getJobStateChanged().removeSubscription(hasCompletedId);
        if( completed == true )
        {
            return job->getJobId().toString(false).c_str();
        }
        else
        {
            return std::string("FAILED");
        }
    }
    else
    {
        // Job creation failed
        CHECKPOINTB("PUB_executePreviewJobThenCancel Failed executed Copy Preview job");
        return "Failed executed Copy Preview job";
    }
}

std::string JobServiceStandardUwAdapter::PUB_executePreviewJobThenContinueCopy()
{
    auto ticket = adaptee_->getDefaultJobTicket();
    auto job= adaptee_->createJob(ticket);
    bool completed{false};
    std::string result = std::string();

    if (job)
    {
        // Subscribe to JobStateChanged events
        JobEvent::SubscriptionId hasCompletedId =
            job->getJobStateChanged().addSubscription([this](std::shared_ptr<dune::job::IJob> job) { handleJobEvent(job); });

        if( waitForJobEvent(job, dune::job::JobStateType::CREATED) )
        {
            CHECKPOINTB("PUB_executePreviewJobThenContinueCopy job %s CREATED", job->getJobId().toString(false).c_str());

            job->initialize();

            if( waitForJobEvent(job, dune::job::JobStateType::READY) )
            {
                CHECKPOINTB("PUB_executePreviewJobThenContinueCopy job %s READY", job->getJobId().toString(false).c_str());

                job->start(SegmentType::PrepareSegment);
                CHECKPOINTB("PUB_executePreviewJobThenContinueCopy job %s started", job->getJobId().toString(false).c_str());

                if( waitForJobEvent(job, dune::job::JobStateType::PROCESSING) )
                {
                    CHECKPOINTB("PUB_executePreviewJobThenContinueCopy job %s PROCESSING", job->getJobId().toString(false).c_str());

                    if( waitForJobEvent(job, dune::job::JobStateType::READY) )
                    {
                        CHECKPOINTB("PUB_executePreviewJobThenContinueCopy previewJob %s READY again", job->getJobId().toString(false).c_str());

                        //Continue copy job.
                        job->start(SegmentType::FinalSegment);
                        CHECKPOINTB("PUB_executePreviewJobThenContinueCopy copyJob %s started with FinalSegment", job->getJobId().toString(false).c_str());

                        if( waitForJobEvent(job, dune::job::JobStateType::COMPLETED) )
                        {
                            CHECKPOINTB("PUB_executePreviewJobThenContinueCopy copyJob %s COMPLETED", job->getJobId().toString(false).c_str());
                            completed=true;
                        }
                    }
                }
            }
        }
        
        job->getJobStateChanged().removeSubscription(hasCompletedId);
        if( completed == true )
        {
            result.append("Job\nJob ID : ");
            result.append(job->getJobId().toString(false));
            auto ticketId = job->getTicket()->getTicketId();
            result.append(" Ticket ID : ");
            result.append(ticketId.toString(false).c_str());
        }
        else
        {
            result = std::string("FAILED");
        }
    }
    else
    {
        // Job creation failed
        CHECKPOINTB("PUB_executePreviewJobThenContinueCopy Failed executed Copy Preview job");
        return "Failed executed Copy Preview job";
    }
    
    return result;
}

std::string JobServiceStandardUwAdapter::PUB_executePreviewJobThenRedo()
{
    auto ticket = adaptee_->getDefaultJobTicket();
    auto job= adaptee_->createJob(ticket);
    bool completed{false};
    std::string result = std::string();

    if(job)
    {
        // Subscribe to JobStateChanged events
        JobEvent::SubscriptionId hasCompletedId =
            job->getJobStateChanged().addSubscription([this](std::shared_ptr<dune::job::IJob> job) { handleJobEvent(job); });

        if( waitForJobEvent(job, dune::job::JobStateType::CREATED) )
        {
            CHECKPOINTB("PUB_executePreviewJobThenRedo job %s CREATED", job->getJobId().toString(false).c_str());

            job->initialize();

            if( waitForJobEvent(job, dune::job::JobStateType::READY) )
            {
                CHECKPOINTB("PUB_executePreviewJobThenRedo previewJob %s READY", job->getJobId().toString(false).c_str());

                job->start(SegmentType::PrepareSegment);
                CHECKPOINTB("PUB_executePreviewJobThenRedo previewJob %s started", job->getJobId().toString(false).c_str());

                if( waitForJobEvent(job, dune::job::JobStateType::PROCESSING) )
                {
                    CHECKPOINTB("PUB_executePreviewJobThenRedo previewJob %s PROCESSING", job->getJobId().toString(false).c_str());

                    if( waitForJobEvent(job, dune::job::JobStateType::READY) )
                    {    
                        CHECKPOINTB("PUB_executePreviewJobThenRedo previewJob %s READY again", job->getJobId().toString(false).c_str());
                            
                        //Redo Preview.
                        job->start(SegmentType::PrepareSegment);
                        CHECKPOINTB("PUB_executePreviewJobThenRedo redo previewJob %s start", job->getJobId().toString(false).c_str());

                        if( waitForJobEvent(job, dune::job::JobStateType::PROCESSING) )
                        {
                            CHECKPOINTB("PUB_executePreviewJobThenRedo redo previewJob %s PROCESSING again", job->getJobId().toString(false).c_str());
                            if( waitForJobEvent(job, dune::job::JobStateType::READY) )
                            {
                                CHECKPOINTB("PUB_executePreviewJobThenRedo redo previewJob %s READY again", job->getJobId().toString(false).c_str());
                                completed=true;
                            }
                        }

                    }
                }
            }
        }
        
        job->getJobStateChanged().removeSubscription(hasCompletedId);
        if( completed == true )
        {
            result.append("Job\nJob ID : ");
            result.append(job->getJobId().toString(false));
            auto ticketId = job->getTicket()->getTicketId();
            result.append(" Ticket ID : ");
            result.append(ticketId.toString(false).c_str());
        }
        else
        {
            result = std::string("FAILED");
        }
    }
    else
    {
        // Job creation failed
        CHECKPOINTB("PUB_executePreviewJobThenRedo Failed executed Copy Preview job");
        return "Failed executed Copy Preview job";
    }
    return result;
}

int JobServiceStandardUwAdapter::PUB_setMaxPagesToCollate(int val)
{
    adaptee_->copyPipeline_->setMaxCollatePages(val);
    CHECKPOINTB("PUB_setMaxPagesToCollate set max collate pages to: %d", val);
    return val;
}

}}}}  // namespace dune::copy::Jobs::Copy
