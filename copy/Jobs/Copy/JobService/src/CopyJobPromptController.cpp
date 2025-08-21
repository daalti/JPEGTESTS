////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobPromptController.cpp
 * @brief  Implements copy job PromptController
 * @date   February 17, 2021
 *
 * (C) Copyright 2021 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "CopyJobPromptController.h"
#include "CopyJobPromptController_TraceAutogen.h"
#include "common_debug.h"
#include "AlertProviderFBHelper.h"
#include "IScannerMedia.h"
#include "IJobTicketHandler.h"
#include "typeMappers.h"
#include "MediaCdmHelper.h"
#include "ICopyJobConstraints.h"
#include "ScanCommonPromptController.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using namespace dune::job::cdm;
using dune::cdm::jobManagement_1::JobManagementAlertsAction;
using AlertProviderFBHelper = dune::ws::cdm::AlertProviderFBHelper;
using Category = dune::cdm::alert_1::Category;

using IMedia                = dune::scan::scanningsystem::IMedia;
using IMediaPath            = dune::scan::scanningsystem::IMediaPath;
using MediaDetectionStatus  = dune::scan::scanningsystem::IMediaPath::MediaDetectionStatus;
using MediaPresenceStatus   = dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus;
using dune::copy::Jobs::Copy::Product;
using dune::job::cdm::mapFromCdm;

CopyJobPromptController::CopyJobPromptController(std::shared_ptr<ICopyJobTicket>    jobTicket,
                                                 IJobManagerAlertProvider*          jobManagerAlertProvider,
                                                 Product prePrintConfiguration,
                                                 bool multiPageSupportedFromFlatbed)
    : jobTicket_(jobTicket),
      jobManagerAlertProvider_(jobManagerAlertProvider),
      prePrintConfiguration_(prePrintConfiguration),
      multiPageSupportedFromFlatbed_(multiPageSupportedFromFlatbed)
{
    scanCommonPromptController_ = std::make_shared<dune::scan::Jobs::Scan::ScanCommonPromptController>();
}

/**
 * @brief Recalculates the prompting needs
 *
 * Use this method only at the beginning of a scanning segment.
 *
 * @param[in] sourceOrigin true if the method is triggered by the user, false if the method is triggered
 * when the pipeline is done
 *
 * @return true if the job will prompt the next time a segmnent is processed
 * false no prompting needed
 */
PromptType CopyJobPromptController::getNewPromptToDisplay(bool sourceOrigin, const std::string& pipelineSectionDoneName)
{
    CHECKPOINTA("CopyJobPromptController::getNewPromptToDisplay: sourceOrigin=%d", static_cast<int>(sourceOrigin));

    prompts_.clear();

    bool duplexInput = jobTicket_->getIntent()->getInputPlexMode() == dune::imaging::types::Plex::DUPLEX;
    bool duplexOutput = jobTicket_->getIntent()->getOutputPlexMode() == dune::imaging::types::Plex::DUPLEX;
    bool idCardJob = jobTicket_->getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD;
    bool nUpJob = jobTicket_->getIntent()->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp;
    bool flatbedSource = jobTicket_->getIntent()->getScanSource() == dune::scan::types::ScanSource::GLASS;
    bool mdfSource = jobTicket_->getIntent()->getScanSource() == dune::scan::types::ScanSource::MDF;
    bool firstScanStarted = jobTicket_->isFirstScanStarted();
    bool originalSizeAny = jobTicket_->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY;
    bool outputSizeAny = jobTicket_->getIntent()->getOutputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY;
    bool promptForMorePages = jobTicket_->getIntent()->getPromptForMorePages();
    bool previewIsRunning = jobTicket_->getPreviewMode();
    auto scanCaptureMode = jobTicket_->getIntent()->getScanCaptureMode();
    bool promptForIDCardBothSides = jobTicket_->getIntent()->getpromptForIdCardBothSide();

    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - previewIsRunning: %d", previewIsRunning);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - duplexInput: %d", duplexInput);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - duplexOutput: %d", duplexOutput);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - idCardJob: %d", idCardJob);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - nUpJob: %d", nUpJob);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - flatbedSource: %d", flatbedSource);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - firstScanStarted: %d", firstScanStarted);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - originalSizeAny: %d", originalSizeAny);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - ScanSource: %d",
                jobTicket_->getIntent()->getScanSource());
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - ScanCaptureMode: %d", scanCaptureMode);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - promptForMorePages: %d", promptForMorePages);
    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - promptForIDCardBothSides: %d",
                promptForIDCardBothSides);

    if(jobTicket_->getExecutionMode() != dune::job::ExecutionMode::NORMAL)
    {
        CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - ExecutionMode is not NORMAL, returning None");
        return PromptType::None;
    }

    if ( originalSizeAny &&
       prePrintConfiguration_ == Product::ENTERPRISE ) // Enterprise & Original Size : Any
    {
        CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - call Scan I/F !!!!!!!!!!!!!!!");
        IMedia *scanMedia = jobTicket_->getScanMediaInterface();
        dune::scan::types::ScanSource ticketScanSource = jobTicket_->getIntent()->getScanSource();
        std::pair<dune::imaging::types::MediaSizeId, dune::imaging::types::MediaOrientation> mediaDetected;

        auto scanSources = scanMedia->getInputs();
        if( (ticketScanSource == dune::scan::types::ScanSource::ADF_SIMPLEX) ||
            (ticketScanSource == dune::scan::types::ScanSource::ADF_DUPLEX) ||
            (ticketScanSource == dune::scan::types::ScanSource::MDF) )
        {
            CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Scan Source ADF!!!");
            for (const auto& scanSource : scanSources)
            {
                if ((scanSource->getType() == dune::scan::types::ScanSource::ADF_SIMPLEX) ||
                    (scanSource->getType() == dune::scan::types::ScanSource::ADF_DUPLEX) ||
                    (scanSource->getType() == dune::scan::types::ScanSource::MDF))
                {
                    mediaDetected = scanSource->getMediaDetectionStatus(); // get current media info
                    CHECKPOINTC(
                        "CopyJobPromptController::getNewPromptToDisplay - printScanMediaDetectionStatus [%s,%s]",
                        dune::imaging::types::EnumNameMediaSizeId(mediaDetected.first),
                        dune::imaging::types::EnumNameMediaOrientation(mediaDetected.second));
                    break;
                }
            }
        }
        else //Flatbed
        {
            CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Scan Source Flatbed!!!");
            for (const auto& scanSource : scanSources)
            {
                if (scanSource->getType() == dune::scan::types::ScanSource::GLASS)
                {
                    mediaDetected = scanSource->getMediaDetectionStatus();
                    CHECKPOINTC(
                        "CopyJobPromptController::getNewPromptToDisplay - printScanMediaDetectionStatusFb [%s,%s]",
                        dune::imaging::types::EnumNameMediaSizeId(mediaDetected.first),
                        dune::imaging::types::EnumNameMediaOrientation(mediaDetected.second));
                    break;
                }
            }
        }

        if(dune::imaging::types::MediaSizeId::UNDEFINED == mediaDetected.first) // detection fail!
        {
            CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Detection Fail! Adding Prompt");
            prompts_.emplace_back(PromptType::FlatbedAutoDetectFail);
        }
        else
        {
            CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Detecting Success! Update ticket as %d, %d",
                        (int)mediaDetected.first, (int)mediaDetected.second);
            if (jobTicket_->getIntent()->getInputMediaSizeId() != mediaDetected.first)
            {
                // Scan Media Size
                CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - setInputMediaSizeId = %d",
                            (int)mediaDetected.first);
                jobTicket_->getIntent()->setInputMediaSizeId(mediaDetected.first);
                if (outputSizeAny) // It means Match Original Size in Enterprise and OutputMediaSize should be the same with OrigianlSize.
                {
                    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - setOutputMediaSizeId = %d",
                                (int)mediaDetected.first);
                    jobTicket_->getIntent()->setMatchOriginalOutputMediaSizeId(mediaDetected.first);
                }

                // Scan Feed Orientation
                dune::scan::types::ScanFeedOrientation scanFeedOrientation;
                if (dune::imaging::types::MediaOrientation::LANDSCAPE == mediaDetected.second)
                {
                    scanFeedOrientation = dune::scan::types::ScanFeedOrientation::LONGEDGE;
                }
                else
                {
                    scanFeedOrientation = dune::scan::types::ScanFeedOrientation::SHORTEDGE;
                }

                if (jobTicket_->getIntent()->getScanFeedOrientation() != scanFeedOrientation)
                {
                    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - setScanFeedOrientation = %d",
                                (int)scanFeedOrientation);
                    jobTicket_->getIntent()->setScanFeedOrientation(scanFeedOrientation);
                }
            }
        }
    }

    CHECKPOINTA("CopyJobPromptController::getNewPromptToDisplay - getSegmentType: %d", jobTicket_->getSegmentType());

    if ((jobTicket_->getSegmentType() == dune::job::SegmentType::PrepareSegment) &&
        prePrintConfiguration_ == Product::ENTERPRISE && previewIsRunning)
    {
        if(scanCaptureMode == dune::scan::types::ScanCaptureModeType::IDCARD)
        {
           PromptType promptType = scanCommonPromptController_->scanEvalPrompts(jobTicket_->getIntent());
           if(promptType == PromptType::IdCardFirstSide)
           {
                idCardPromptSide_ = "front";
           }
           else if(promptType == PromptType::IdCardSecondSide)
           {
                idCardPromptSide_ = "back";
           }
           else if(promptType == PromptType::None && jobTicket_->getSegmentType() == dune::job::SegmentType::PrepareSegment && !promptForIDCardBothSides)
           {
                promptType = PromptType::None;
                idCardPromptSide_ = "front";
           }
           prompts_.emplace_back(promptType);        
        }
        else if(scanCaptureMode == dune::scan::types::ScanCaptureModeType::BOOKMODE)
        {
            CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Adding Book Mode Prompt");
            prompts_.emplace_back(PromptType::BookMode);
        }
        else if( previewIsRunning)
        {
            auto promptType = PromptType::FlatbedAddPage;
            prompts_.emplace_back(promptType);
            CHECKPOINTA("CopyJobPromptController::getNewPromptToDisplay - Adding  Add Another Page Prompt for Preview");
        }
    }
    else if (idCardJob && prePrintConfiguration_ == Product::ENTERPRISE && !previewIsRunning)
    {
        CHECKPOINTC("CopyJobPromptController::evalPrompts - Emplace ID Card promt");
        PromptType promptType = scanCommonPromptController_->scanEvalPrompts(jobTicket_->getIntent());
        if (promptType == PromptType::IdCardFirstSide)
        {
            CHECKPOINTC("CopyJobPromptController::evalPrompts - Emplace ID Card promt for first side");
            idCardPromptSide_ = "front";
        }
        else if(promptType == PromptType::IdCardSecondSide)
        {
            CHECKPOINTC("CopyJobPromptController::evalPrompts - Emplace ID Card promt for second side");
            idCardPromptSide_ = "back";
        }
        //For Preview Segment Even if prompt for both sides is disabled first prompt should be for IDCard First Side
        else if(promptType == PromptType::None && jobTicket_->getSegmentType() == dune::job::SegmentType::PrepareSegment && !promptForIDCardBothSides)
        {
            promptType = PromptType::None;
            idCardPromptSide_ = "front";
        }
        prompts_.emplace_back(promptType);
    }
    else if (promptForMorePages && firstScanStarted)
    {
        CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Adding promptForMore pages prompt");
        PromptType promptType = scanCommonPromptController_->scanEvalPrompts(jobTicket_->getIntent());
        prompts_.emplace_back(promptType);
    }
    else if(scanCaptureMode == dune::scan::types::ScanCaptureModeType::BOOKMODE && !previewIsRunning)
    {
        CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Adding Book Mode Prompt");
        prompts_.emplace_back(PromptType::BookMode);
    }
    else if (flatbedSource && firstScanStarted)
    {
        if (idCardJob)
        {
            CHECKPOINTC(
                "CopyJobPromptController::getNewPromptToDisplay - firstScanStarted : Checking ScanPromptController for "
                "ID Card Second Side Prompt");
            prompts_.emplace_back(PromptType::IdCardSecondSide);
            idCardPromptSide_ = "back";
        }
        else if (duplexInput)
        {
           if(multiPageSupportedFromFlatbed_)
            {
                CHECKPOINTC(
                    "CopyJobPromptController::getNewPromptToDisplay - firstScanStarted : Adding Flatbed next page "
                    "prompt");
                if(scanCommonPromptController_ != nullptr)
                {
                    PromptType promptType = scanCommonPromptController_->scanEvalPrompts(jobTicket_->getIntent());
                    prompts_.emplace_back(promptType);
                }
            }
            else 
            {
                CHECKPOINTC(
                    "CopyJobPromptController::getNewPromptToDisplay - firstScanStarted : Adding Flatbed Second Page "
                    "Prompt");
                prompts_.emplace_back(PromptType::FlatbedSecondPage);
            }
        }
        else if (!(idCardJob) && (duplexOutput || nUpJob)) //Flatbed 1-2 or nUp
        {
            CHECKPOINTC(
                "CopyJobPromptController::getNewPromptToDisplay - firstScanStarted : Adding Flatbed Add Another Page "
                "Prompt");
            if(multiPageSupportedFromFlatbed_) {
                prompts_.emplace_back(PromptType::FlatbedAddPage); 
            }
            else {
                prompts_.emplace_back(PromptType::FlatbedSecondPage);
            }
        }
        else //Flatbed 1-1
        {
            CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - firstScanStarted : Adding No Prompt");
        }
    }
    else if (mdfSource && firstScanStarted)
    {
        CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - firstScanStarted : Adding MDF eject page Prompt");
        prompts_.emplace_back(PromptType::MdfEjectPage);
    }
    else if(prePrintConfiguration_ == Product::ENTERPRISE && !firstScanStarted && sourceOrigin)
    {
        IMedia *scanMedia = jobTicket_->getScanMediaInterface();
        auto scanSources = scanMedia->getInputs();
        dune::scan::types::ScanSource ticketScanSource = jobTicket_->getIntent()->getScanSource();
        for (const auto& scanSource : scanSources)
        {
            if( ((scanSource->getType() == dune::scan::types::ScanSource::ADF_SIMPLEX) ||
                (scanSource->getType() == dune::scan::types::ScanSource::ADF_DUPLEX)) && (scanSource->getMediaPresenceStatus() == MediaPresenceStatus::NOT_LOADED))
            {
                CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Paper is not loaded in ADF");
                PromptType promptType = scanCommonPromptController_->scanEvalPrompts(jobTicket_->getIntent(), scanSource->getHwFlavor());
                if((promptType != PromptType::None) && (promptType == PromptType::AdfAddPage))
                {
                    CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Adding ADF add page prompt");
                    prompts_.emplace_back(promptType);
                }
                break;
            }
            else
            {
                CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Do not need ADF add page prompt");
            }
        }
    }
    else
    {
        CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay - Not firstScanStarted Case!");
    }

    //MorePagesDetectedForCollate prompt handling
    int maxCollatePageCount = jobTicket_->getMaxCollatePages();    
    if( jobTicket_->getIntent()->getCollate() == dune::copy::SheetCollate::Collate &&
        jobTicket_->getIntent()->getScanSource() != dune::scan::types::ScanSource::GLASS &&
        jobTicket_->getIntent()->getCopies() > 1 &&
        jobTicket_->getJobCompleting() == true &&
        maxCollatePageCount != 0)
    {
        CHECKPOINTC(
            "CopyJobPromptController::getNewPromptToDisplay - Total Scanned pages: %d, jobTicket::getScanNumberPages: "
            "%d",
            jobTicket_->getHandler()->getPagesIds(dune::job::PageOrder::CREATION).size(), maxCollatePageCount);
        if ((jobTicket_->getHandler()->getPagesIds(dune::job::PageOrder::CREATION).size() % maxCollatePageCount) == 0)
        {
            CHECKPOINTC(
                "CopyJobPromptController::getNewPromptToDisplay - MorePagesDetectedForCollate - Checking ADF still "
                "loaded");
            IMedia *scanMedia = jobTicket_->getScanMediaInterface();
            auto scanSources = scanMedia->getInputs();
            for (const auto& scanSource : scanSources)
            {
                if (scanSource->getType() == dune::scan::types::ScanSource::ADF_SIMPLEX || scanSource->getType() == dune::scan::types::ScanSource::ADF_DUPLEX)
                {
                    if (scanSource->getMediaPresenceStatus() == MediaPresenceStatus::LOADED)
                    {
                        CHECKPOINTA(
                            "CopyJobPromptController::getNewPromptToDisplay - Setting MorePagesDetectedForCollate");
                        prompts_.emplace_back(PromptType::MorePagesDetectedForCollate);
                        break;
                    }
                }
            }
        }
    }

    if (!prompts_.empty())
    {
        CHECKPOINTC("CopyJobPromptController::getNewPromptToDisplay: prompts_.front()=%d",
                    static_cast<int>(prompts_.front()));
        return prompts_.front();
    }
    return PromptType::None;
}

/**
 * @brief Get the Prompt object
 *
 * @return PromptType required prompt to post
 */
PromptType CopyJobPromptController::getPrompt()
{
    if (prompts_.empty())
    {
        CHECKPOINTB("CopyJobPromptController::getPrompt: Empty prompts");
        return PromptType::None;
    }

    PromptType promptType = prompts_.front();

    CHECKPOINTC("CopyJobPromptController::getPrompt: PromptType=%d", static_cast<int>(promptType));
    
    return promptType;
}

void CopyJobPromptController::onPromptResponse(dune::cdm::alert_1::Category category,
                                               std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction)
{
    PromptType          promptType = static_cast<PromptType>(category);
    PromptResponseType  promptResponseType = PromptResponseType::NoResponse;
    CHECKPOINTA("CopyJobPromptController::onPromptResponse: category=%d", static_cast<int>(category));
    switch(category)
    {
        case(Category::scanManualDuplexSecondSide):
            if(idCardPromptSide_ == "front")
            {
                promptType = PromptType::IdCardFirstSide;
            }
            else
            {
                promptType = PromptType::IdCardSecondSide;
            }
            break;
        case(Category::scanManualDuplexSecondPage):
            promptType = PromptType::FlatbedSecondPage;
            break;
        case (Category::flatbedAddPage):
            if(prompts_.front() == PromptType::FlatbedAddPage)
            {
                CHECKPOINTA("CopyJobPromptController::onPromptResponse: PromptType flatbedAddPage ");
                promptType = PromptType::FlatbedAddPage;
            }
            else if (prompts_.front() == PromptType::FlatbedDuplexAddPage)
            {
                CHECKPOINTA("CopyJobPromptController::onPromptResponse:  PromptType FlatbedDuplexAddPage ");
                promptType = PromptType::FlatbedDuplexAddPage;
            }
            //Book Mode
            else if (prompts_.front() == PromptType::BookMode)
            {
                promptType = PromptType::BookMode;
            }
           break;
        case(Category::mdfEjectPage):
            promptType = PromptType::MdfEjectPage;
            break;
        case(Category::morePagesDetectedForCollate):
            promptType = PromptType::MorePagesDetectedForCollate;
            break;
        case(Category::flatbedAutoDetectFail):
            promptType = PromptType::FlatbedAutoDetectFail;
            break;
        case(Category::adfAddPage):
            promptType = PromptType::AdfAddPage;
            break;
        default:
            break;
    }
    CHECKPOINTA("CopyJobPromptController::onPromptResponse: PromptType=%d", static_cast<int>(promptType));

    if (promptType == prompts_.front())
    {
        userRespondedToPrompt_ = true;
        if (alertAction)
        {
            prompts_.erase(prompts_.begin());
            if(promptType == PromptType::FlatbedDuplexAddPage || promptType == PromptType::IdCardSecondSide || promptType == PromptType::IdCardFirstSide || promptType == PromptType::FlatbedAutoDetectFail)
            {
                promptResponseType = scanCommonPromptController_->scanOnPromptResponse(promptType, alertAction, jobTicket_->getIntent());
                if(promptResponseType == PromptResponseType::NoResponse)
                {
                    CHECKPOINTC("CopyJobPromptController::onPromptResponse: FlatbedDuplexAddPage NoResponse.");
                    // jobFramework has already removed the alert from the alert provider
                    alertID_ = 0;
                }
                else if (promptResponseType == PromptResponseType::CancelJob)
                {
                    jobTicket_->setCompletionState(dune::job::CompletionStateType::CANCELED);
                }
            }
            else
            {
                if(alertAction->jobAction == JobManagementAlertsAction::Response_01) /// Ok
                {
                    promptResponseType  = PromptResponseType::Response_01;
                    //check if we are a 4 sheet flatbed duplex and 2pagespersheet job
                    CHECKPOINTC("CopyJobPromptController::onPromptResponse: Continue button pressed.");

                    if(promptType == PromptType::AdfAddPage)
                    {
                        CHECKPOINTC("CopyJobPromptController::onPromptResponse: promptType is AdfAddPage.");

                        IMedia *scanMedia = jobTicket_->getScanMediaInterface();
                        auto scanSources = scanMedia->getInputs();
                        
                        for (const auto& scanSource : scanSources)
                        {
                            if( (scanSource->getType() == dune::scan::types::ScanSource::ADF_SIMPLEX || scanSource->getType() == dune::scan::types::ScanSource::ADF_DUPLEX) )
                            {
                                if(scanSource->getMediaPresenceStatus() == MediaPresenceStatus::NOT_LOADED)
                                {
                                    CHECKPOINTC("CopyJobPromptController::onPromptResponse: MediaPresenceStatus::NOT_LOADED.");
                                    promptResponseType = PromptResponseType::DisplayNewPrompts;
                                }
                                jobTicket_->getIntent()->setScanSource(scanSource->getType());
                                break;
                            }
                        }
                        jobTicket_->setFirstScanStarted(false);
                    }
                    else if(promptType == PromptType::BookMode)
                    {
                        if(alertAction->param1 == "RightPageOnly" || alertAction->param1 == "TopOnly")
                            jobTicket_->getIntent()->setBookMode(dune::scan::types::BookModeEnum::RightPageOnly);
                        else if(alertAction->param1 == "LeftPageOnly" || alertAction->param1 == "BottomOnly")
                            jobTicket_->getIntent()->setBookMode(dune::scan::types::BookModeEnum::LeftPageOnly);
                        else if(alertAction->param1 == "BothPageTopBottom" || alertAction->param1 == "BothPageLeftRight")
                            jobTicket_->getIntent()->setBookMode(dune::scan::types::BookModeEnum::BothPages);
                        
                        if (scanCommonPromptController_ != nullptr)
                        {
                            promptResponseType = scanCommonPromptController_->scanOnPromptResponse(promptType, alertAction, jobTicket_->getIntent());
                        }
                    }
                }
                else if(alertAction->jobAction == JobManagementAlertsAction::Response_02) /// Done
                {
                    CHECKPOINTC("CopyJobPromptController::onPromptResponse: Response_02");
                    {
                        promptResponseType  = PromptResponseType::Response_02;
                        // Reset this flag to avoid prompting again in next stage of pipeline
                        jobTicket_->setFirstScanStarted(false);
                        CHECKPOINTC("CopyJobPromptController::onPromptResponse: Done button pressed.");
                    }
                }
                else if(alertAction->jobAction == JobManagementAlertsAction::Response_03) /// Cancel
                {
                    CHECKPOINTC("CopyJobPromptController::onPromptResponse: Response_03");
                    if(jobTicket_->getSegmentType() == SegmentType::PrepareSegment)
                    {
                        promptResponseType = PromptResponseType::CancelJob;
                        jobTicket_->setCompletionState(dune::job::CompletionStateType::CANCELED);
                    }
                    else
                    {
                        promptResponseType = PromptResponseType::Response_03;
                    }
                    jobTicket_->setFirstScanStarted(false);
                    CHECKPOINTC("CopyJobPromptController::onPromptResponse: Cancel button pressed.");
                }
                else if(alertAction->jobAction == JobManagementAlertsAction::NoResponse) /// Timeout
                {
                    promptResponseType  = PromptResponseType::NoResponse;
                    // Reset this flag to avoid prompting again in next stage of pipeline
                    jobTicket_->setFirstScanStarted(false);
                    if (promptType == PromptType::MdfEjectPage)
                    {
                        for (auto inputdev : jobTicket_->getScanMediaInterface()->getInputs())
                        {
                            if (inputdev && inputdev->getId() == "MDF" && inputdev->getMediaReleaseStatus() == dune::scan::scanningsystem::IMediaPath::MediaReleaseStatus::RELEASABLE)
                            {
                                CHECKPOINTC("CopyJobPromptController::onPromptResponse: NoResponse, ejecting MDF...");
                                inputdev->unload();
                            }
                            else if (inputdev && inputdev->getId() == "MDF")
                            {
                                CHECKPOINTC("CopyJobPromptController::onPromptResponse: NoResponse, MDF not in releasable state");
                            }
                        }
                    }
                    else
                    {
                        // jobFramework has already removed the alert from the alert provider
                        alertID_ = 0;
                    }
                    
                    CHECKPOINTC("CopyJobPromptController::onPromptResponse: No button pressed.");
                }
                else
                {
                    CHECKPOINTC("CopyJobPromptController::onPromptResponse: Invalid alert action.");
                }
            }
        }
    }
    else
    {
        CHECKPOINTC("CopyJobPromptController::onPromptResponse: Invalid promptType: %d", static_cast<int>(promptType));
        
        promptType = PromptType::None;
    }

    jobCallback_(promptType, promptResponseType);

    CHECKPOINTC("CopyJobPromptController::onPromptResponse: EXIT");
}

/**
* @brief Display prompt on UI
*
* @return void
*/
void CopyJobPromptController::displayPrompt(PromptType promptType, PromptCallback callback)
{
    CHECKPOINTC("CopyJobPromptController::displayPrompt: PromptType=%d", static_cast<int>(promptType));

    if(promptType != prompts_.front())
    {
        assert(false);
    }

    jobCallback_ = callback;
    dune::cdm::alert_1::AlertT  alert;
    uint32_t timeoutSeconds = 240;
    std::string dataType;
    switch(promptType)
    {
        case (PromptType::IdCardSecondSide):
        {
            CHECKPOINTA("CopyJobPromptController::displayPrompt: PromptType::IdCardSecondSide");
            scanCommonPromptController_->scanDisplayPrompt(alert, promptType, idCardPromptSide_);
            break;
        }
        case (PromptType::IdCardFirstSide):
        {
            CHECKPOINTA("CopyJobPromptController::displayPrompt: PromptType::IdCardFirstSide");
            scanCommonPromptController_->scanDisplayPrompt(alert, promptType, idCardPromptSide_);
            break;
        }
        case (PromptType::FlatbedSecondPage):
        {
            CHECKPOINTC("CopyJobPromptController::displayPrompt: PromptType::FlatbedSecondPage");
            DUNE_CDM_ALERT_SCANMANUALDUPLEXSECONDPAGE(alert);
            std::vector<std::string> alActions;
            alActions.push_back(EnumNameJobManagementAlertsAction(JobManagementAlertsAction::Response_01));
            alActions.push_back(EnumNameJobManagementAlertsAction(JobManagementAlertsAction::NoResponse));
            alActions.push_back(EnumNameJobManagementAlertsAction(JobManagementAlertsAction::Response_02));

            AlertProviderFBHelper::addAlertActions(&alert,
                    std::string("com.hp.cdm.service.jobManagement.version.1.resource.jobAction"),
                    std::string("/cdm/jobManagement/v1/jobAction"),
                    std::string("/jobAction"), alActions);
            timeoutSeconds = 120;
            break;
        }
        case (PromptType::FlatbedDuplexAddPage): {
            CHECKPOINTA("CopyJobPromptController::displayPrompt: PromptType::FlatbedDuplexAddPage");
            dataType = "Duplex";
            scanCommonPromptController_->scanDisplayPrompt(alert, promptType, dataType);
            break;
        }
        case (PromptType::MdfEjectPage):
        {
            CHECKPOINTC("CopyJobPromptController::displayPrompt: PromptType::MdfEjectPage");
            DUNE_CDM_ALERT_MDFEJECTPAGE(alert);
            std::vector<std::string> alActions;
            alActions.push_back(EnumNameJobManagementAlertsAction(JobManagementAlertsAction::NoResponse));

            AlertProviderFBHelper::addAlertActions(&alert,
                    std::string("com.hp.cdm.service.jobManagement.version.1.resource.jobAction"),
                    std::string("/cdm/jobManagement/v1/jobAction"),
                    std::string("/jobAction"), alActions);
            break;
        }
        case (PromptType::MorePagesDetectedForCollate):
        {
            CHECKPOINTC("CopyJobPromptController::displayPrompt: PromptType::MorePagesDetectedForCollate");
            DUNE_CDM_ALERT_MOREPAGESDETECTEDFORCOLLATE(alert);
            std::vector<std::string> alActions;
            alActions.push_back(EnumNameJobManagementAlertsAction(JobManagementAlertsAction::Response_01));
            alActions.push_back(EnumNameJobManagementAlertsAction(JobManagementAlertsAction::NoResponse));
            alActions.push_back(EnumNameJobManagementAlertsAction(JobManagementAlertsAction::Response_02));

            AlertProviderFBHelper::addAlertActions(&alert,
                    std::string("com.hp.cdm.service.jobManagement.version.1.resource.jobAction"),
                    std::string("/cdm/jobManagement/v1/jobAction"),
                    std::string("/jobAction"), alActions);
            break;
        }
        case (PromptType::FlatbedAddPage):
        {
            DUNE_CDM_ALERT_FLATBEDADDPAGE(alert);
            std::vector<std::string> alertActions;
            alertActions.push_back(
                EnumNameJobManagementAlertsAction(JobManagementAlertsAction::Response_01));  // Add Page button press
            alertActions.push_back(
                EnumNameJobManagementAlertsAction(JobManagementAlertsAction::NoResponse));  // Timeout
            // for some of the action add the response data ..
            alertActions.push_back(
                EnumNameJobManagementAlertsAction(JobManagementAlertsAction::Response_02));  // Finish button press
            alertActions.push_back(
                EnumNameJobManagementAlertsAction(JobManagementAlertsAction::Response_03));  // Finish button press
            AlertProviderFBHelper::addAlertActions(
                &alert, std::string("com.hp.cdm.service.jobManagement.version.1.resource.jobAction"),
                std::string("/cdm/jobManagement/v1/jobAction"), std::string("/jobAction"), alertActions, true);
            AlertProviderFBHelper::addAlertData(&alert,
                            std::string("com.hp.cdm.service.jobManagement.version.1.resource.jobAction"),
                            std::string("/cdm/jobManagement/v1/jobAction"),
                            std::string("/jobAction"),
                            std::string("Addpage"),
                            false);

            auto id = jobTicket_->getTicketId().toString();
            for (int i = id.size() - 1; i > -1; i--)
            {
                if (id[i] == '{' || id[i] == '}')
                {
                    id.erase(i, 1);
                }
            }

            AlertProviderFBHelper::addAlertData(&alert,
                            std::string("com.hp.cdm.service.jobManagement.version.1.resource.jobAction"),
                            std::string("/cdm/jobManagement/v1/jobAction"),
                            std::string("/jobAction"),
                            std::string(id),
                            false);
            break;
   
        }
        case (PromptType::FlatbedAutoDetectFail):
        {
            CHECKPOINTC("CopyJobPromptController::displayPrompt: PromptType::FlatbedAutoDetectFail");
            scanCommonPromptController_->scanDisplayPrompt(alert, promptType, dataType);
            break;
        }
        case (PromptType::AdfAddPage):
        {
            CHECKPOINTC("CopyJobPromptController::displayPrompt: PromptType::AdfAddPage");
            dataType = "AdfAddPage";
            scanCommonPromptController_->scanDisplayPrompt(alert, promptType, dataType, jobTicket_->getTicketId().toString());
            break;
        }
        case (PromptType::BookMode):
        {
            CHECKPOINTC("CopyJobPromptController::displayPrompt: PromptType::BookMode");
            dataType = "BookMode";
            auto bookModeOption = jobTicket_->getIntent()->getBookMode();
            auto contentOrientation = jobTicket_->getIntent()->getContentOrientation();
            std::string value = "";
            switch (bookModeOption)
                {
                    case dune::scan::types::BookModeEnum::BothPages:
                        if(contentOrientation == dune::imaging::types::ContentOrientation::LANDSCAPE)
                        {
                            value = "BothPageTopBottom";
                        }
                        else
                        {
                            value = "BothPageLeftRight";
                        }
                        break;
                    case dune::scan::types::BookModeEnum::RightPageOnly:
                        if(contentOrientation == dune::imaging::types::ContentOrientation::LANDSCAPE)
                        {
                            value = "TopOnly";
                        }
                        else
                        {
                            value = "RightPageOnly";
                        }
                        break;
                    case dune::scan::types::BookModeEnum::LeftPageOnly:
                        if(contentOrientation == dune::imaging::types::ContentOrientation::LANDSCAPE)
                        {
                            value = "BottomOnly";
                        }
                        else
                        {
                            value = "LeftPageOnly";
                        }
                        break;
                    default:
                        if(contentOrientation == dune::imaging::types::ContentOrientation::LANDSCAPE)
                        {
                            value = "BothPageTopBottom";
                        }
                        else
                        {
                            value = "BothPageLeftRight";
                        }
                        break;
                }
            if (scanCommonPromptController_ != nullptr)
            {
                scanCommonPromptController_->scanDisplayPrompt(alert, promptType, dataType, value);
            }
            break;
        }
        case (PromptType::None):
            assert(false);

        default:
            assert(false);
    }
    
    alertID_ = jobManagerAlertProvider_->notifyAlert(&alert, std::bind(&CopyJobPromptController::onPromptResponse, this, std::placeholders::_1, std::placeholders::_2), timeoutSeconds);

    if(alertID_ == 0)
    {
        CHECKPOINTC("CopyJobPromptController::displayPrompt: notifyAlert(PromptType=%d) failed!!", static_cast<int>(promptType));

        jobCallback_(promptType, PromptResponseType::NoResponse);
    }

    CHECKPOINTC("CopyJobPromptController::displayPrompt: EXIT");
}

/**
 * @brief Cancel prompt ignoring job callback.
 *
 * @return void
 */
void CopyJobPromptController::cancelPrompt()
{
    CHECKPOINTC("CopyJobPromptController::cancelPrompt: BEGIN");
    if (alertID_ > 0)
    {
        jobManagerAlertProvider_->removeAlert(alertID_);

        if(!userRespondedToPrompt_)
        {
            CHECKPOINTC("CopyJobPromptController::cancelPrompt: user doesn't responded to prompt");
            jobTicket_->setCompletionState(dune::job::CompletionStateType::CANCELED);
        }
        
    }
}

}}}}  // namespace dune::copy::Jobs::Copy
