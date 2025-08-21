////////////////////////////////////////////////////////////////////////////////
/**
 * @file  JobDetailsProvider.cpp
 * @brief Provider of details of a copy job
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "CopyJobDetailsProvider.h"

#include "common_debug.h"
#include "CopyJobDetailsProvider_TraceAutogen.h"

#include "ICopyJobTicket.h"
#include "ICopyPageTicket.h"
#include "IJobTicketHandler.h"
#include "IJobTicketResourceManager.h"
#include "JobDetailsHelper.h"
#include "typeMappers.h"

using IJobTicketResourceManager = dune::job::IJobTicketResourceManager;

using namespace dune::job;
using namespace dune::job::cdm;
using namespace dune::cdm::jobManagement_1;
using namespace dune::cdm::glossary_1;

constexpr double CONVERT_INCH_TO_MM = 25.4;
constexpr int    CONVERT_MS_TO_S    = 1000;

namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyJobDetailsProvider::CopyJobDetailsProvider(ICopyJobService*           jobService,
                                               IJobTicketResourceManager* jobTicketResourceManager,
                                               ISettings* interfaceISettings, IScanPipeline* scanPipeline,
                                               IDateTime* dateTime)
    : jobService_{jobService},
      jobTicketResourceManager_{jobTicketResourceManager},
      interfaceISettings_{interfaceISettings},
      scanPipeline_{scanPipeline},
      dateTime_{dateTime}
{
    CHECKPOINTC("CopyJobDetailsProvider::CopyJobDetailsProvider() jobService: %p, jobTicketResourceManager: %p",
                jobService_, jobTicketResourceManager_);
    assert(jobService != nullptr);
    assert(jobTicketResourceManager_ != nullptr);

    statsHelper_ = std::make_shared<dune::print::JobAccounting::StatsHelper>();
}

std::pair<bool, StatsInfoDetails> CopyJobDetailsProvider::populateJobDetails(const Uuid& jobTicketUuid, dune::security::ac::IAccessControl* accessControl)
{
    CHECKPOINTC("CopyJobDetailsProvider::populateJobDetails() uuid: %s", jobTicketUuid.toString().c_str());

    // Get Copy Job Ticket
    std::shared_ptr<ICopyJobTicket> copyJobTicket{getCopyJobTicket(jobTicketUuid)};
    if (!copyJobTicket)
    {
        CHECKPOINTB("CopyJobDetailsProvider::populateJobDetails() copy job ticket %s not found in cache",
                    jobTicketUuid.toString().c_str());
        return std::make_pair(false, generateEmptyJobDetails(jobTicketUuid));
    }

    return std::make_pair(true, generateJobDetails(*copyJobTicket, accessControl));
}

PagesDetails CopyJobDetailsProvider::populatePagesDetails(const Uuid& jobTicketUuid) const
{
    CHECKPOINTC("CopyJobDetailsProvider::populatePagesDetails() JobTicketId: %s", jobTicketUuid.toString().c_str());

    // Get Copy Job Ticket
    std::shared_ptr<ICopyJobTicket> copyJobTicket{getCopyJobTicket(jobTicketUuid)};
    if (!copyJobTicket)
    {
        CHECKPOINTB("CopyJobDetailsProvider::populateJobDetails() copy job ticket not found in cache");
        return generateEmptyPagesDetails();
    }
    return generatePagesDetails(*copyJobTicket);
}

PageDetails CopyJobDetailsProvider::populatePageDetails(const Uuid& jobTicketUuid, const Uuid& pageUuid) const
{
    CHECKPOINTC("CopyJobDetailsProvider::populatePageDetails() JobTicketId: %s, PageId: %s",
                jobTicketUuid.toString().c_str(), pageUuid.toString().c_str());

    // Get Copy Job Ticket
    std::shared_ptr<ICopyJobTicket> copyJobTicket{getCopyJobTicket(jobTicketUuid)};
    if (!copyJobTicket)
    {
        CHECKPOINTB("CopyJobDetailsProvider::populateJobDetails() copy job ticket not found in cache");
        return generateEmptyPageDetails(pageUuid);
    }

    // Get Page Ticket
    std::shared_ptr<ICopyPageTicket> pageTicket{copyJobTicket->getCopyPageTicket(pageUuid)};
    if (!pageTicket)
    {
        CHECKPOINTB("CopyJobDetailsProvider::populateJobDetails() page ticket not found");
        return generateEmptyPageDetails(pageUuid);
    }

    return generatePageDetails(*pageTicket, copyJobTicket->getJobId());
}

std::shared_ptr<ICopyJobTicket> CopyJobDetailsProvider::getCopyJobTicket(const Uuid jobTicketUuid) const
{
    CHECKPOINTC("CopyJobDetailsProvider::getCopyJobTicket() uuid: %s", jobTicketUuid.toString().c_str());

    // Load ticket to cache if needed
    bool persistentTicket;
    auto jobTicket = jobTicketResourceManager_->loadJobTicketIntoCacheIfNeeded(jobTicketUuid, persistentTicket);
    if (jobTicket == nullptr)
    {
        CHECKPOINTB("CopyJobDetailsProvider::getCopyJobTicket() job ticket %s not found in cache",
                    jobTicketUuid.toString().c_str());
        return nullptr;
    }

    // Get the copy job ticket from cache
    return jobService_->getTicketFromCache(jobTicketUuid);
}

StatsInfoDetails CopyJobDetailsProvider::generateEmptyJobDetails(const Uuid& jobTicketUuid)
{
    JobInfoDetails jobInfoTable{};
    jobInfoTable.jobUuid = jobTicketUuid.toString(false);
    jobInfoTable.jobType = dune::job::StatsDetails::StatsJobType::COPY;
    return StatsInfoDetails{jobInfoTable.jobUuid, jobInfoTable};
}

PagesDetails CopyJobDetailsProvider::generateEmptyPagesDetails()
{
    std::string version = dune::cdm::jobManagement_1::VERSION;
    return PagesDetails{version};
}

PageDetails CopyJobDetailsProvider::generateEmptyPageDetails(const Uuid& pageId)
{
    std::string version = dune::cdm::jobManagement_1::VERSION;
    PageDetails emptyPageDetails{};
    emptyPageDetails.version = version;
    emptyPageDetails.pageId = pageId.toString(false);
    dune::cdm::jobManagement_1::page::OutputSizeTable outputSize{};
    emptyPageDetails.outputSize = outputSize;

    return emptyPageDetails;
}

PrintSettingsDetails CopyJobDetailsProvider::generatePrintSettings(const std::shared_ptr<ICopyJobIntent> copyJobIntent)
{
    CHECKPOINTC("CopyJobDetailsProvider:generatePrintSettings - ENTER");
    PrintSettingsDetails printSettings{};

    // use scan colorMode because Copy UI app shows only printable color mode selections.
    printSettings.colorMode = copyJobIntent->getColorMode();

    // printSettings.econoMode
    printSettings.inQuietMode = statsHelper_->getQuietMode(interfaceISettings_);
    // printSettings.marginsType
    printSettings.mediaRequested = getMediaRequested(copyJobIntent);
    printSettings.plexMode = copyJobIntent->getOutputPlexMode();
    printSettings.printQuality = copyJobIntent->getCopyQuality();
    // printSettings.printResolution
    printSettings.requestedCopiesCount = copyJobIntent->getCopies();
    printSettings.requestedImpressionCount = copyJobIntent->getRequestedPages();
    printSettings.printResolution = copyJobIntent->getOutputXResolution();
    printSettings.mediaOutputId = copyJobIntent->getOutputDestination();

    printSettings.collate = dune::job::StatsDetails::SheetCollate::UNCOLLATE;
    if(copyJobIntent->getCollate() == dune::copy::SheetCollate::Collate)
    {
        printSettings.collate = dune::job::StatsDetails::SheetCollate::COLLATE;
    }

    CHECKPOINTC("CopyJobDetailsProvider:generatePrintSettings - EXIT");
    return printSettings;
}

PrintedSheetInfoDetails CopyJobDetailsProvider::generatePrintedSheetInfo(
    const std::shared_ptr<ICopyJobIntent> copyJobIntent)
{
    CHECKPOINTC("CopyJobDetailsProvider:generatePrintedSheetInfo - ENTER");
    PrintedSheetInfoDetails printedSheetInfo{};

    CHECKPOINTC("CopyJobDetailsProvider:generatePrintedSheetInfo - EXIT");
    return printedSheetInfo;
}

MediaRequestedDetails CopyJobDetailsProvider::getMediaRequested(const std::shared_ptr<ICopyJobIntent> copyJobIntent)
{
    std::string                       mediaId = "";
    dune::imaging::types::MediaIdType mediaType = copyJobIntent->getOutputMediaIdType();
    dune::imaging::types::MediaSizeId mediaSize = copyJobIntent->getOutputMediaSizeId();
    dune::imaging::types::MediaSource mediaSource = copyJobIntent->getOutputMediaSource();
    std::string                       mediaName = "";
    std::string                       donorMediaId = "";

    /*
        Fill MediaInputDetails

        Avoid setting the fields when the value is UNDEFINED, because it will
        erroneously report as isSet() == true.
    */

    MediaInputDetails mediaInput{};

    if (mediaType != dune::imaging::types::MediaIdType::UNDEFINED)
    {
        mediaInput.currentMediaType = mediaType;
    }

    if (mediaSize != dune::imaging::types::MediaSizeId::UNDEFINED)
    {
        mediaInput.currentMediaSize = mediaSize;
    }

    if (mediaSource != dune::imaging::types::MediaSource::UNDEFINED)
    {
        mediaInput.mediaSourceId = mediaSource;
    }
    /*
        Fill MediaRequestedDetails
    */

    MediaRequestedDetails mediaRequested{};
    
    mediaRequested.mediaId = mediaId;
    mediaRequested.mediaInput = mediaInput;

    return mediaRequested;
}

StatsInfoDetails CopyJobDetailsProvider::generateJobDetails(ICopyJobTicket& copyJobTicket, dune::security::ac::IAccessControl* accessControl)
{
    CHECKPOINTC("CopyJobDetailsProvider::generateJobDetails()");
    StatsInfoDetails jobDetails{generateEmptyJobDetails(copyJobTicket.getJobId())};

    auto           copyJobIntent = copyJobTicket.getIntent();
    auto           result        = copyJobTicket.getResult();
    PrintInfoDetails printInfo{};

    // Result Data
    auto completedPages  = result->getCompletedImpressions();
    auto completedCopies = result->getCompletedCopies();
    auto progress        = result->getProgress();

    CHECKPOINTC("CopyJobDetailsProvider::generateJobDetails() completed impressions %" PRIu32 ", completed copies %" PRIu32 "", 
        completedPages, completedCopies);

    printInfo.impressionCount = completedPages;
    printInfo.copiesCount     = completedCopies;
    printInfo.progress        = progress;

    uint32_t remainingPrintingTime = result->getRemainingPrintingTime() / CONVERT_MS_TO_S;
    printInfo.remainingPrintingTime = remainingPrintingTime;

    printInfo.printSettings = generatePrintSettings(copyJobIntent);
    printInfo.printedSheetInfo = generatePrintedSheetInfo(copyJobIntent);

    jobDetails.printInfo = printInfo;
    jobDetails.jobInfo = dune::job::generateJobInfo(copyJobTicket, dateTime_);
    jobDetails.userInfo = dune::job::generateUserInfo(copyJobTicket, accessControl);

    // Scan Info
    if (scanPipeline_ != nullptr)
    {
        jobDetails.scanInfo = *scanPipeline_->populateScanInfo(copyJobTicket.getHandler(), copyJobIntent);
    }
    else
    {
        CHECKPOINTA("CopyJobDetailsProvider:generateJobDetails - scanPipeline is null");
    }

    // In the case when Image Retriever is creating a blank page
    // Page Ticket count and scan page will not match
    // so use the scan page count from the Job ticket
    if(copyJobTicket.getIntent()->getScanNumberPages()> 0 && static_cast<uint>(jobDetails.scanInfo.get()->scannedPageCount.get()) != copyJobTicket.getIntent()->getScanNumberPages())
    {
        CHECKPOINTB("CopyJobDetailsProvider:generateJobDetails - scanPageCount %d does not match intent scanNumberPages %d",
                    jobDetails.scanInfo.get()->scannedPageCount, copyJobTicket.getIntent()->getScanNumberPages());
        jobDetails.scanInfo.getMutable()->scannedPageCount.set(copyJobTicket.getIntent()->getScanNumberPages());
    }

    return jobDetails;
}

bool compareOriginalSizes(dune::cdm::jobManagement_1::page::OriginalSizeTable originalSizeA, dune::cdm::jobManagement_1::page::OriginalSizeTable originalSizeB, 
                          dune::cdm::jobManagement_1::page::PageMarginsTable marginsA, dune::cdm::jobManagement_1::page::PageMarginsTable marginsB)
{
    return (
            originalSizeA.width     == originalSizeB.width &&
            originalSizeA.length    == originalSizeB.length &&
            marginsA.topMargin      == marginsB.topMargin &&
            marginsA.bottomMargin   == marginsB.bottomMargin &&
            marginsA.leftMargin     == marginsB.leftMargin &&
            marginsA.rightMargin    == marginsB.rightMargin);
}

PagesDetails CopyJobDetailsProvider::generatePagesDetails(ICopyJobTicket& copyJobTicket)
{
    PagesDetails pagesDetails{generateEmptyPagesDetails()};

    dune::cdm::jobManagement_1::page::OriginalSizeTable originalSizeFromFirstPage{};
    dune::cdm::jobManagement_1::page::PageMarginsTable  originalPageMarginsFromFirstPage{};
    bool                                                setOriginalSizeFirstPage = true;
    bool                                                severalOriginalSizes = false;

    // Get Pages Ids
    for (const auto& pageId : copyJobTicket.getPagesIds(PageOrder::CREATION))
    {
        PageDetails pageDetails =
            generatePageDetails(*copyJobTicket.getCopyPageTicket(pageId), copyJobTicket.getJobId());
        pagesDetails.pages.insertItem(pageDetails);

        if (setOriginalSizeFirstPage)
        {
            CHECKPOINTC("PrintJobDetailsProvider::generatePagesDetails setting firstOriginal Size");
            originalSizeFromFirstPage = pageDetails.originalSize;
            originalPageMarginsFromFirstPage = pageDetails.pageMargins;
            setOriginalSizeFirstPage = false;
        }
        else if (!severalOriginalSizes)
        {
            CHECKPOINTC("PrintJobDetailsProvider::generatePagesDetails comparing...");
            if (!compareOriginalSizes(originalSizeFromFirstPage, *pageDetails.originalSize.get(), originalPageMarginsFromFirstPage, *pageDetails.pageMargins.get()))
            {
                CHECKPOINTC("PrintJobDetailsProvider::generatePagesDetails seting severalSizes to true");
                severalOriginalSizes = true;
                pagesDetails.severalOriginalSizes = mapToCdmFeatureEnabled(true);
            }
        }
    }
    return pagesDetails;
}

PageDetails CopyJobDetailsProvider::generatePageDetails(const ICopyPageTicket& pageTicket, const Uuid& jobId)
{
    const Uuid& pageId{pageTicket.getPageId()};
    CHECKPOINTC("CopyJobDetailsProvider::generatePageDetails() JobId: %s, PageId: %s", jobId.toString(false).c_str(),
                pageId.toString(false).c_str());

    PageDetails pageDetails{generateEmptyPageDetails(pageId)};
    pageDetails.pageNumber = pageTicket.getPageNumber();
    pageDetails.outputSize.getMutable()->mediaSize = job::cdm::mapToCdm(pageTicket.getMediaSize());
    pageDetails.previewProgress = pageTicket.getPreviewProgress();

    // High Resolution Preview
    const IPageTicket::Preview& highResPreview{pageTicket.getHighResPreview()};
    if (!highResPreview.path.empty())
    {
        pageDetails.highResImage = mapToCdm(highResPreview, jobId, pageId, true);
    }

    // Low Resolution Previw
    const IPageTicket::Preview& lowResPreview{pageTicket.getLowResPreview()};
    if (!lowResPreview.path.empty())
    {
        pageDetails.lowResImage = mapToCdm(lowResPreview, jobId, pageId, false);
    }

    dune::cdm::jobManagement_1::page::OriginalSizeTable originalSize{};
    dune::cdm::jobManagement_1::page::PageMarginsTable  originalPageMargins{};

    auto pageIntent = pageTicket.getPageIntent();
    auto pageResult = pageTicket.getPageResult();
    double   unitConversionMmPerPixel = 0;

    if (pageIntent != nullptr)
    {
        auto printPageIntent = pageIntent->getPrintPageIntent();
        uint32_t resolution = 0;
        if (printPageIntent != nullptr)
        {
            resolution = printPageIntent->getResolution();
            unitConversionMmPerPixel = resolution == 0 ? 0 : CONVERT_INCH_TO_MM / resolution;
            pageDetails.requestedCopiesCount = printPageIntent->getRequestedCopies();
        }
    }

    if (pageResult != nullptr)
    {
        auto scanPageResult  = pageResult->getScanPageResult();
        if (scanPageResult != nullptr)
        {
            originalSize.width = static_cast<int32_t>(std::lround(scanPageResult->getScannedWidth() * unitConversionMmPerPixel));
            CHECKPOINTC("CopyJobDetailsProvider::generatePageDetails() Result: original width mm[%d]",
                        static_cast<int32_t>(originalSize.width));
            originalSize.length = static_cast<int32_t>(std::lround(scanPageResult->getScannedHeight() * unitConversionMmPerPixel));
            CHECKPOINTC("CopyJobDetailsProvider::generatePageDetails() Result: original length mm[%d]",
                        static_cast<int32_t>(originalSize.length));
        }
        auto printPageResult = pageResult->getPrintPageResult();
        if (printPageResult != nullptr)
        {
            pageDetails.completedCopiesCount = printPageResult->getCompletedCopies();
        }
    }

    pageDetails.originalSize = originalSize;
    pageDetails.pageMargins  = originalPageMargins;
    return pageDetails;
}

ImageDescriptorTable CopyJobDetailsProvider::mapToCdm(const IPageTicket::Preview& preview, const Uuid& jobId,
                                                       const Uuid& pageId, bool highResPreview,
                                                       const std::string& layerName /*= ""*/)
{
    // Create CDM Image Descriptor
    ImageDescriptorTable image(preview.heightPx, preview.widthPx);

    // Generate Preview Link if preview is valid/completed
    if (preview.progress == 100)
    {
        std::string      previewRel{highResPreview ? "High Resolution Image" : "Low Resolution Image"};
        std::string      layerRel{layerName.empty() ? "" : " - Layer " + layerName};
        links::ItemTable previewLink{previewRel + layerRel};
        previewLink.href = preview.path;
        previewLink.hrefTemplate = generatePreviewId(jobId, pageId, highResPreview, layerName);
        image.links = std::vector<links::ItemTable>{previewLink};
    }
    return image;
}

std::string CopyJobDetailsProvider::generatePreviewId(const Uuid& jobId, const Uuid& pageId, bool highResPreview,
                                                       const std::string& layerName /*= ""*/)
{
    return std::string(jobId.toString(false) + "_" + pageId.toString(false) + "_" +
                       (highResPreview ? "HighResPreview" : "LowResPreview") +
                       (layerName.empty() ? "" : std::string("Layer_" + layerName)));
}

void CopyJobDetailsProvider::setStatsHelper(std::shared_ptr<dune::print::JobAccounting::StatsHelper> helper)
{
    statsHelper_.swap(helper);
}

}}}}  // namespace dune::copy::Jobs
