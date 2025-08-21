#include "CopyJobTicketHandler.h"

#include "common_debug.h"

#include "CopyJobTicketHandler_TraceAutogen.h"

#include "IJobTicketHandler.h"
#include "ICopyJobTicket.h"
#include "IMedia.h"

using DocumentSettings = dune::job::IJobTicketHandler::DocumentSettings;
using Uuid = dune::framework::core::Uuid;
using MediaSettings = dune::job::IJobTicketHandler::MediaSettings;
using InputDetails = dune::job::IJobTicketHandler::InputDetails;
using ResultDetails = dune::job::IJobTicketHandler::ResultDetails;
using TimingDetails = dune::job::IJobTicketHandler::TimingDetails;

using namespace dune::job;


namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyJobTicketHandler::CopyJobTicketHandler(ICopyJobTicket&                              copyTicket,
                                           const CopyJobTicketHandler::JobTicketEvents& jobTicketEvents,
                                           dune::framework::core::ThreadPool*           threadPool)
    : JobTicketHandlerBase(copyTicket, jobTicketEvents, threadPool),
      copyTicket_(copyTicket)
{}

DocumentSettings CopyJobTicketHandler::getDocumentSettings()
{
    DocumentSettings documentSettings;
    documentSettings.jobName = copyTicket_.getJobName();
    CHECKPOINTC("CopyJobTicketHandler::getDocumentSettings() %s", documentSettings.toString().c_str());
    return documentSettings;
}

void CopyJobTicketHandler::doSetDocumentSettings(const dune::job::IJobTicketHandler::DocumentSettings& documentSettings,
                                                 const std::vector<DocumentSettingsProperties> propertiesToBeUpdated)
{
    if (propertiesToBeUpdated.size() == 0)
    {
        CHECKPOINTB("CopyJobTicketHandler::doSetDocumentSettings: propertiesToBeUpdated is empty");
        return;
    }
    CHECKPOINTC("CopyJobTicketHandler::doSetDocumentSettings() %s", documentSettings.toString().c_str());
    
    if (documentSettings.jobName.empty())
    {
        CHECKPOINTB("CopyJobTicketHandler::doSetDocumentSettings Error setting empty jobName");
        return;
    }

    CHECKPOINTC("CopyJobTicketHandler::doSetDocumentSettings setting jobName %s", documentSettings.jobName.c_str());
    copyTicket_.setJobName(documentSettings.jobName);
}

MediaSettings CopyJobTicketHandler::getMediaSettings()
{
    MediaSettings mediaSettings;

    auto copyIntent = copyTicket_.getIntent();
    mediaSettings.mediaId         = "";
    mediaSettings.mediaSize       = copyIntent->getOutputMediaSizeId();
    mediaSettings.mediaSource     = copyIntent->getOutputMediaSource();
    mediaSettings.mediaType       = copyIntent->getOutputMediaIdType();
    mediaSettings.mediaCustomName = "";

    CHECKPOINTC_STR("CopyJobTicketHandler::getMediaSettings() %s", mediaSettings.toString().c_str());
    return mediaSettings;
}

void CopyJobTicketHandler::doSetMediaSettings(const MediaSettings& mediaSettings, const std::vector<MediaSettingsProperties> propertiesToBeUpdated)
{
    CHECKPOINTC_STR("CopyJobTicketHandler::CopyJobTicketHandler() %s", mediaSettings.toString().c_str());

    // TODO: set the media settings in the copyjob ticket
}

InputDetails CopyJobTicketHandler::getInputDetails()
{
    InputDetails inputDetails;

    inputDetails.applicationName = copyTicket_.getApplicationName();
    inputDetails.userName        = copyTicket_.getUserName();
    inputDetails.requestedCopies = copyTicket_.getIntent()->getCopies();
    inputDetails.requestedPages  = copyTicket_.getIntent()->getRequestedPages();
    inputDetails.printQuality    = copyTicket_.getIntent()->getCopyQuality();
    inputDetails.colorMode       = copyTicket_.getIntent()->getColorMode();
    inputDetails.isCollated      = copyTicket_.getIntent()->getCollate() == dune::copy::SheetCollate::Collate;
    inputDetails.scannedPages    = copyTicket_.getIntent()->getScanNumberPages();

    CHECKPOINTC_STR("CopyJobTicketHandler::getInputDetails() %s", inputDetails.toString().c_str());
    return inputDetails;
}

void CopyJobTicketHandler::doSetInputDetails(const InputDetails& inputDetails, const std::vector<InputDetailsProperties> propertiesToBeUpdated)
{
    InputDetails detailsToBeUpdated = inputDetails;
    CHECKPOINTC_STR("CopyJobTicketHandler::setInputDetails() %s", inputDetails.toString().c_str());

    setInputDetailsToTicket(detailsToBeUpdated, propertiesToBeUpdated);

    if(copyTicket_.getIntent()->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp ||
        copyTicket_.getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
    {

        if(inputDetails.scannedPages  %2 == 0)
        {
            detailsToBeUpdated.requestedPages = (inputDetails.scannedPages/2) * copyTicket_.getIntent()->getCopies();
        }
        else
        {
            detailsToBeUpdated.requestedPages = ((inputDetails.scannedPages +1)/2) * copyTicket_.getIntent()->getCopies();
        }
        copyTicket_.getIntent()->setRequestedPages(detailsToBeUpdated.requestedPages);
    }
    else if(copyTicket_.getIntent()->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::FourUp)
    {
        if(inputDetails.scannedPages %4 == 0)
        {
            detailsToBeUpdated.requestedPages = (inputDetails.scannedPages/4) * copyTicket_.getIntent()->getCopies();
        }
        else
        {
            auto remainder = inputDetails.scannedPages % 4;
            detailsToBeUpdated.requestedPages = ((inputDetails.scannedPages + (4-remainder))/4) * copyTicket_.getIntent()->getCopies();
        }
        copyTicket_.getIntent()->setRequestedPages(detailsToBeUpdated.requestedPages);
    }
}

ResultDetails CopyJobTicketHandler::getResultDetails()
{
    // TODO fectch the result details from job ticket
    ResultDetails resultDetails = getResultDetailsFromTicket();
    CHECKPOINTC_STR("CopyJobTicketHandler::getResultDetails() %s", resultDetails.toString().c_str());
    return resultDetails;
}

TimingDetails& CopyJobTicketHandler::getTimingDetails()
{
    // TODO fectch the timing details from job ticket

    CHECKPOINTC_STR("CopyJobTicketHandler::getTimingDetails() %s", timingDetails_.toString().c_str());
    return timingDetails_;
}

void CopyJobTicketHandler::removePage(const Uuid& pageId)
{
    CHECKPOINTC_STR("CopyJobTicketHandler::removePage() %s", pageId.toString().c_str());

    auto currentInputDetails = getInputDetails();
    currentInputDetails.scannedPages -= 1;
    setInputDetails(currentInputDetails,{IJobTicketHandler::InputDetailsProperties::SCANNED_PAGES});
    JobTicketHandlerBase::removePage(pageId);
}

void CopyJobTicketHandler::doSetResultDetails(const ResultDetails& resultDetails, const std::vector<ResultDetailsProperties> propertiesToBeUpdated)
{
    CHECKPOINTC_STR("CopyJobTicketHandler::doSetResultDetails() %s", resultDetails.toString().c_str());
    setResultDetailsToTicket(resultDetails, propertiesToBeUpdated);
}

void CopyJobTicketHandler::doSetTimingDetails(const TimingDetails& timingDetails)
{
    CHECKPOINTC_STR("CopyJobTicketHandler::doSetTimingDetails() %s", timingDetails.toString().c_str());
    timingDetails_ = timingDetails;
}

InputDetails CopyJobTicketHandler::getInputDetailsFromTicket()
{
    InputDetails inputDetails;

    inputDetails.applicationName = copyTicket_.getApplicationName();
    inputDetails.userName        = copyTicket_.getUserName();
    inputDetails.requestedCopies = copyTicket_.getIntent()->getCopies();
    inputDetails.printQuality    = copyTicket_.getIntent()->getCopyQuality();
    inputDetails.requestedPages  = copyTicket_.getIntent()->getRequestedPages();
    inputDetails.colorMode       = copyTicket_.getIntent()->getColorMode();
    inputDetails.isCollated      = copyTicket_.getIntent()->getCollate() == dune::copy::SheetCollate::Collate;
    inputDetails.scannedPages    = copyTicket_.getIntent()->getScanNumberPages();

    // copyTicket does not have the below properties.
    // inputDetails.printModeName 
    // inputDetails.printModeDescription 
    // inputDetails.curingTemperature
    // inputDetails.interPassDelayOffset
    // inputDetails.vacuum
    // inputDetails.mediaAdvanceFactor
    // inputDetails.overcoatLevel
    // inputDetails.printZoneTemperature
    // inputDetails.printZoneAirflow
    // inputDetails.whiteMode
    // inputDetails.colorModeSelector
    // inputDetails.inkDensity
    // inputDetails.inkDensitySideB
    // inputDetails.whiteDensity

    CHECKPOINTC("CopyJobTicketHandler::getInputDetailsFromTicket() %s", inputDetails.toString().c_str());
    return inputDetails;
}

void CopyJobTicketHandler::setInputDetailsToTicket(const InputDetails& inputDetails, const std::vector<IJobTicketHandler::InputDetailsProperties> propertiesToBeUpdated)
{
    CHECKPOINTC("CopyJobTicketHandler::setInputDetailsToTicket() %s", inputDetails.toString().c_str());
    for (auto property : propertiesToBeUpdated)
    {
        switch (property)
        {
            case IJobTicketHandler::InputDetailsProperties::APPLICATION_NAME:
                copyTicket_.setApplicationName(inputDetails.applicationName);
                break;
            case IJobTicketHandler::InputDetailsProperties::SCANNED_PAGES:
                if (inputDetails.scannedPages > 0)
                {
                    copyTicket_.getIntent()->setScanNumberPages(inputDetails.scannedPages);
                }
                break;
            case IJobTicketHandler::InputDetailsProperties::PRINT_QUALITY:
                copyTicket_.getIntent()->setCopyQuality(inputDetails.printQuality);
                break;
            case IJobTicketHandler::InputDetailsProperties::REQUESTED_PAGES:
                copyTicket_.getIntent()->setRequestedPages(inputDetails.requestedPages);
                break;
            default:
                break;
        }
    }
   
}

ResultDetails CopyJobTicketHandler::getResultDetailsFromTicket()
{
    ResultDetails                   resultDetails;
    std::shared_ptr<ICopyJobResult> result{copyTicket_.getResult()};

    resultDetails.progress                 = result->getProgress();
    resultDetails.completedImpressions     = result->getCompletedImpressions();
    resultDetails.completedCopies          = result->getCompletedCopies();
    resultDetails.currentPage              = result->getCurrentPage();
    resultDetails.remainingPrintingTime    = result->getRemainingPrintingTime();
    resultDetails.currentCuringTemperature = result->getCurrentCuringTemperature();
    resultDetails.allPagesDiscovered       = result->areAllPagesDiscovered();
    resultDetails.nonWhitePixelCount       = result->getPixelCounts().nonWhitePixelCount;
    resultDetails.colorPixelCount          = result->getPixelCounts().colorPixelCount;
    resultDetails.totalPixelCount          = result->getPixelCounts().totalPixelCount;
    resultDetails.totalScanDuration        = result->getTotalScanDuration();
    resultDetails.activeScanDuration       = result->getActiveScanDuration();
    CHECKPOINTC("CopyJobTicketHandler::getResultDetailsFromTicket() %s", resultDetails.toString().c_str());
    return resultDetails;
}

void CopyJobTicketHandler::setResultDetailsToTicket(const ResultDetails& resultDetails, const std::vector<ResultDetailsProperties> propertiesToBeUpdated)
{
    CHECKPOINTC("CopyJobTicketHandler::setResultDetailsToTicket() %s", resultDetails.toString().c_str());
    std::shared_ptr<ICopyJobResult> result{copyTicket_.getResult()};

    for (auto property : propertiesToBeUpdated)
    {
        switch (property)
        {
            case IJobTicketHandler::ResultDetailsProperties::PROGRESS:
                result->setProgress(resultDetails.progress);
                break;
            case IJobTicketHandler::ResultDetailsProperties::COMPLETED_IMPRESSIONS:
                result->setCompletedImpressions(resultDetails.completedImpressions);
                break;
            case IJobTicketHandler::ResultDetailsProperties::COMPLETED_COPIES:
                result->setCompletedCopies(resultDetails.completedCopies);
                break;
            case IJobTicketHandler::ResultDetailsProperties::CURRENT_PAGE:
                result->setCurrentPage(resultDetails.currentPage);
                break;
            case IJobTicketHandler::ResultDetailsProperties::REMAINING_PRINTING_TIME:
                result->setRemainingPrintingTime(resultDetails.remainingPrintingTime);
                break;
            case IJobTicketHandler::ResultDetailsProperties::CURRENT_CURING_TEMPERATURE:
                result->setCurrentCuringTemperature(resultDetails.currentCuringTemperature);
                break;
            case IJobTicketHandler::ResultDetailsProperties::ALL_PAGES_DISCOVERED:
                result->setAllPagesDiscovered(resultDetails.allPagesDiscovered);
                break;
            case IJobTicketHandler::ResultDetailsProperties::NON_WHITE_PIXEL_COUNT:
            case IJobTicketHandler::ResultDetailsProperties::COLOR_PIXEL_COUNT:
            case IJobTicketHandler::ResultDetailsProperties::TOTAL_PIXEL_COUNT:
                result->setPixelCounts(PixelCounts{.nonWhitePixelCount = resultDetails.nonWhitePixelCount,
                                                   .colorPixelCount = resultDetails.colorPixelCount,
                                                   .totalPixelCount = resultDetails.totalPixelCount});
                break;
            case IJobTicketHandler::ResultDetailsProperties::SCAN_TOTAL_DURATION:
                result->setTotalScanDuration(resultDetails.totalScanDuration);
                break;
            case IJobTicketHandler::ResultDetailsProperties::SCAN_ACTIVE_DURATION:
                result->setActiveScanDuration(resultDetails.activeScanDuration);
                break;
            default:
                CHECKPOINTB("CopyJobTicketHandler::setResultDetailsToTicket: property %d not handled.", property);
                break;
        }
    }
}

std::shared_ptr<dune::imaging::types::Margins> CopyJobTicketHandler::getMargins(dune::imaging::types::MediaSizeId mediaSize)
{
    CHECKPOINTC("CopyJobTicketHandler::getMargins() for mediaSize %d", mediaSize);

    dune::print::engine::IMedia::MarginsParameters marginParams;
    marginParams.setMediaSource(copyTicket_.getIntent()->getOutputMediaSource());
    dune::imaging::types::Margins mediaMargins = std::get<1>(copyTicket_.getMediaInterface()->getMargins(marginParams));
    return std::make_shared<dune::imaging::types::Margins>(mediaMargins);
}

}}}}  // namespace dune::copy::Jobs
