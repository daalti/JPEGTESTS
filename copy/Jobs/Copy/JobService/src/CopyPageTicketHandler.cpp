////////////////////////////////////////////////////////////////////////////////
/**
 * @file  CopyPageTicketHandler.cpp
 * @brief Dune Job Pipeline - PageTicket Handler
 *
 * (c) Copyright HP Inc. 2022. All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "CopyPageTicketHandler.h"

#include "common_debug.h"

#include "CopyPageTicketHandler_TraceAutogen.h"

using namespace dune::job;


namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyPageTicketHandler::CopyPageTicketHandler(ICopyPageTicket& ticket, PageTicketEventSource& pageTicketEventSource)
    : PageTicketHandlerBase{ticket, pageTicketEventSource},
      ticket_{ticket},
      inputDetails_{getInputDetailsFromTicket()},
      resultDetails_{getResultDetailsFromTicket()}
{
    CHECKPOINTC("CopyPageTicketHandler::CopyPageTicketHandler");
}

IPageTicketHandler::MediaSettings CopyPageTicketHandler::getMediaSettings() const
{
    IPageTicketHandler::MediaSettings mediaSettings{};
    mediaSettings.size = ticket_.getMediaSize();
    return mediaSettings;
}

IPageTicketHandler::InputDetails& CopyPageTicketHandler::getInputDetails()
{
    CHECKPOINTC("CopyPageTicketHandler::getInputDetails() %s", inputDetails_.toString().c_str());
    return inputDetails_;
}

IPageTicketHandler::ResultDetails& CopyPageTicketHandler::getResultDetails()
{
    CHECKPOINTC("CopyPageTicketHandler::getResultDetails() %s", resultDetails_.toString().c_str());
    return resultDetails_;
}

IPageTicketHandler::TimingDetails& CopyPageTicketHandler::getTimingDetails()
{
    CHECKPOINTC("CopyPageTicketHandler::getTimingDetails() %s", timingDetails_.toString().c_str());
    return timingDetails_;
}

std::shared_ptr<dune::job::IIntent> CopyPageTicketHandler::getIntent(dune::job::IntentType intentType) const
{
    return ticket_.getIntent(intentType);
}

void CopyPageTicketHandler::doSetMediaSettings(const IPageTicketHandler::MediaSettings& mediaSettings)
{
    ticket_.setMediaSize(mediaSettings.size);
}

void CopyPageTicketHandler::doSetInputDetails(const IPageTicketHandler::InputDetails& inputDetails)
{
    CHECKPOINTC("CopyPageTicketHandler::doSetInputDetails() %s", inputDetails.toString().c_str());
    setInputDetailsToTicket(inputDetails);
    inputDetails_ = inputDetails;
}

void CopyPageTicketHandler::doSetResultDetails(const IPageTicketHandler::ResultDetails& resultDetails)
{
    CHECKPOINTC("CopyPageTicketHandler::doSetResultDetails() %s", resultDetails.toString().c_str());
    setResultDetailsToTicket(resultDetails);
    resultDetails_ = resultDetails;
}

void CopyPageTicketHandler::doSetTimingDetails(const IPageTicketHandler::TimingDetails& timingDetails)
{
    timingDetails_ = timingDetails;
}

void CopyPageTicketHandler::setPageStorePath(std::string pageStorePath)
{
    CHECKPOINTC("CopyPageTicketHandler::setStorePath");
    ticket_.setPageStorePath(pageStorePath);
}

std::string CopyPageTicketHandler::getPageStorePath() const
{
    CHECKPOINTC("CopyPageTicketHandler::getStorePath");
    return ticket_.getPageStorePath();
}
void CopyPageTicketHandler::setMemoryFileHandle(uint32_t fileHandle)
{
    CHECKPOINTC("CopyPageTicketHandler::setMemoryFileHandle");
    ticket_.setMemoryFileHandle(fileHandle);
}

uint32_t CopyPageTicketHandler::getMemoryFileHandle() const
{
    CHECKPOINTC("CopyPageTicketHandler::getMemoryFileHandle");
    return ticket_.getMemoryFileHandle();
}

IPageTicketHandler::InputDetails CopyPageTicketHandler::getInputDetailsFromTicket()
{
    IPageTicketHandler::InputDetails inputDetails{};
    // Intent Data
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = 
        std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(ticket_.getIntent(dune::job::IntentType::SCAN));
    if (scanIntent)
    {
        inputDetails.resolution = scanIntent->getXImageQuality();
    }
    return inputDetails;
}

void CopyPageTicketHandler::setInputDetailsToTicket(const IPageTicketHandler::InputDetails& inputDetails)
{
    CHECKPOINTC_STR("CopyPageTicketHandler::setInputDetailsToTicket() %s", inputDetails.toString().c_str());
    auto pageIntent = ticket_.getPageIntent();
    if (pageIntent)
    {
        auto printPageIntent = pageIntent->getPrintPageIntent();
        if (printPageIntent)
        {
            printPageIntent->setResolution(inputDetails.resolution);
            printPageIntent->setColorMode(inputDetails.colorMode);
            printPageIntent->setMediaDestination(inputDetails.mediaOutputId);
            printPageIntent->setMargins(inputDetails.margins);
            printPageIntent->setRequestedCopies(inputDetails.requestedCopies);
        }
    }
}

IPageTicketHandler::ResultDetails CopyPageTicketHandler::getResultDetailsFromTicket()
{
    IPageTicketHandler::ResultDetails resultDetails{};
    // Result Data
    auto pageResult = ticket_.getPageResult();
    if (pageResult)
    {
        auto scanPageResult = pageResult->getScanPageResult();
        auto printPageResult = pageResult->getPrintPageResult();
        if (scanPageResult)
        {
            resultDetails.scannedWidth = scanPageResult->getScannedWidth();     
            resultDetails.scannedHeight = scanPageResult->getScannedHeight();
        }
        if (printPageResult)
        {
            resultDetails.outputSize = printPageResult->getOutputSize();
            resultDetails.impressionWidth = printPageResult->getImpressionWidth();
            resultDetails.impressionHeight = printPageResult->getImpressionHeight();
            resultDetails.estimatedPrintTime = printPageResult->getEstimatedPrintTime();
            resultDetails.completedCopies = printPageResult->getCompletedCopies();
            resultDetails.printed = printPageResult->isPrinted();
            resultDetails.rendered = printPageResult->isRendered();
        }
    }

    CHECKPOINTC_STR("PrintPageTicketHandler::getResultDetailsFromTicket() %s", resultDetails.toString().c_str());
    return resultDetails;
}

void CopyPageTicketHandler::setResultDetailsToTicket(const IPageTicketHandler::ResultDetails& resultDetails)
{
    CHECKPOINTC_STR("CopyPageTicketHandler::setResultDetailsToTicket() %s", resultDetails.toString().c_str());
    auto pageResult = ticket_.getPageResult();
    if (pageResult)
    {
        auto scanPageResult = pageResult->getScanPageResult();
        auto printPageResult = pageResult->getPrintPageResult();
        if (scanPageResult)
        {
            scanPageResult->setScannedWidth(resultDetails.scannedWidth);
            scanPageResult->setScannedHeight(resultDetails.scannedHeight);
        }
        if (printPageResult)
        {
            printPageResult->setOutputSize(resultDetails.outputSize);
            printPageResult->setImpressionWidth(resultDetails.impressionWidth);
            printPageResult->setImpressionHeight(resultDetails.impressionHeight);
            printPageResult->setCompletedCopies(resultDetails.completedCopies);
            printPageResult->setEstimatedPrintTime(resultDetails.estimatedPrintTime);
            printPageResult->setPrinted(resultDetails.printed);
            printPageResult->setRendered(resultDetails.rendered);
        }
    }
}

}}}}  // namespace dune::copy::Jobs
