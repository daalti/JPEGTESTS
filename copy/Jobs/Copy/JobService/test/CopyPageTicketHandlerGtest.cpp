////////////////////////////////////////////////////////////////////////////////
/**
 * @file   PageTicketHandlerGtest.cpp
 * @brief  CopyPageTicketHandler unit tests
 *
 * (C) Sampleright 2021 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "MockICopyPageTicket.h"

#include "CopyPageTicketHandler.h"
#include "CopyPageTicket.h"
#include "CopyTicketGtestUtilities.h"

using namespace dune::job;
using namespace dune::copy::Jobs::Copy;
using namespace dune::framework::core;
using namespace dune::imaging::types;


using ::testing::_;
using ::testing::Return;
using ::testing::Invoke;

static const uint8_t            REQUESTED_AND_COMPLETED_COPIES{5};
static const uint8_t            IMPRESSION_WIDTH{10};
static const uint8_t            IMPRESSION_HEIGHT{10};
static const uint8_t            ESTIMATED_PRINT_TIME{7};
static const uint8_t            RESOLUTION{200};
static const uint8_t            SCANNED_WIDTH{10};
static const uint8_t            SCANNED_HEIGHT{10};
static const ColorMode          COLOR_MODE{ColorMode::COLOR};
static const Margins            MARGINS{Distance{1, 2}, Distance{3, 4}, Distance{5, 6}, Distance{7, 8}};
static const MediaDestinationId MEDIA_DESTINATION{MediaDestinationId::DEFAULT};
static const MediaSource        MEDIA_SOURCE{MediaSource::MAIN};
static const MediaIdType        MEDIA_TYPE{MediaIdType::STATIONERY};
static const MediaSizeId        MEDIA_SIZE{MediaSizeId::CUSTOM};

class TestIntent : public IIntent
{
};

class GivenACopyPageTicketHandler : public ::testing::Test
{
  public:
    GivenACopyPageTicketHandler();

  protected:
    MockICopyPageTicket     mockICopyPageTicket_;
    PageTicketEventSource   pageTicketEventSource_;

    CopyPageTicketHandler pageTicketHandler_;
    std::string storePath = "/tmp/print";
};

GivenACopyPageTicketHandler::GivenACopyPageTicketHandler()
    : mockICopyPageTicket_{},
      pageTicketEventSource_{&mockICopyPageTicket_},
      pageTicketHandler_{mockICopyPageTicket_, pageTicketEventSource_}
{
}

TEST_F(GivenACopyPageTicketHandler, WhenGettingMediaSettings_ThenAttributesAreGet)
{
    IPageTicketHandler::MediaSettings expectedMediaSettings;
    expectedMediaSettings.size = MEDIA_SIZE;
    expectedMediaSettings.type = MEDIA_TYPE;
    expectedMediaSettings.source = MEDIA_SOURCE;

    // Return Expected Media Size
    EXPECT_CALL(mockICopyPageTicket_, getMediaSize()).WillOnce(Return(expectedMediaSettings.size));

    // Get and compare data
    IPageTicketHandler::MediaSettings mediaSettings = pageTicketHandler_.getMediaSettings();
    EXPECT_EQ(expectedMediaSettings.size, mediaSettings.size);

    // Not Used
    EXPECT_NE(expectedMediaSettings.type, mediaSettings.type);
    EXPECT_NE(expectedMediaSettings.source, mediaSettings.source);
}

TEST_F(GivenACopyPageTicketHandler, WhenSettingMediaSettings_ThenAttributesAreSetAndChangesNotified)
{
    IPageTicketHandler::MediaSettings expectedMediaSettings;
    expectedMediaSettings.size = MEDIA_SIZE;
    expectedMediaSettings.type = MEDIA_TYPE;
    expectedMediaSettings.source = MEDIA_SOURCE;

    // Ticket is set with media settings values
    EXPECT_CALL(mockICopyPageTicket_, setMediaSize(expectedMediaSettings.size)).Times(1);
    pageTicketHandler_.setMediaSettings(expectedMediaSettings);
}

TEST_F(GivenACopyPageTicketHandler, WhenGettingAndSettingInputDetails_ThenAttributesAreCorrect)
{
    // Expectations
    IPageTicketHandler::InputDetails expectedInputDetails;
    expectedInputDetails.colorMode = COLOR_MODE;
    expectedInputDetails.margins = MARGINS;
    expectedInputDetails.requestedCopies = REQUESTED_AND_COMPLETED_COPIES;

    // Set the Input Details
    pageTicketHandler_.setInputDetails(expectedInputDetails);

    // Get the Input Details
    const IPageTicketHandler::InputDetails& inputDetails = pageTicketHandler_.getInputDetails();

    // Compare data
    EXPECT_EQ(expectedInputDetails.resolution, inputDetails.resolution);
    EXPECT_EQ(expectedInputDetails.colorMode, inputDetails.colorMode);
    EXPECT_EQ(expectedInputDetails.margins, inputDetails.margins);
    EXPECT_EQ(expectedInputDetails.requestedCopies, inputDetails.requestedCopies);
}

TEST_F(GivenACopyPageTicketHandler, WhenGettingResultDetails_ThenAttributesAreGet)
{
    // Set Result details
    IPageTicketHandler::ResultDetails expectedResultDetails;
    expectedResultDetails.outputSize = MEDIA_SIZE;
    expectedResultDetails.impressionWidth = IMPRESSION_WIDTH;
    expectedResultDetails.impressionHeight = IMPRESSION_HEIGHT;
    expectedResultDetails.estimatedPrintTime = ESTIMATED_PRINT_TIME;
    expectedResultDetails.completedCopies = REQUESTED_AND_COMPLETED_COPIES;

    // Set the Result Details
    pageTicketHandler_.setResultDetails(expectedResultDetails);

    // Get the Result Details
    const IPageTicketHandler::ResultDetails& resultDetails{pageTicketHandler_.getResultDetails()};
    EXPECT_EQ(expectedResultDetails.outputSize, resultDetails.outputSize);
    EXPECT_EQ(expectedResultDetails.impressionWidth, resultDetails.impressionWidth);
    EXPECT_EQ(expectedResultDetails.impressionHeight, resultDetails.impressionHeight);
    EXPECT_EQ(expectedResultDetails.estimatedPrintTime, resultDetails.estimatedPrintTime);
    EXPECT_EQ(expectedResultDetails.completedCopies, resultDetails.completedCopies);
}

TEST_F(GivenACopyPageTicketHandler, WhenGettingIntent_ThenJobTicketReturnIt)
{
    // Nullptr intent
    IntentType expectedIntent{IntentType::PRINT};
    EXPECT_CALL(mockICopyPageTicket_, getIntent(expectedIntent)).WillOnce(Return(nullptr));
    EXPECT_EQ(nullptr, pageTicketHandler_.getIntent(expectedIntent));

    // Valid Intent
    std::shared_ptr<TestIntent> testIntent{std::make_shared<TestIntent>()};
    EXPECT_CALL(mockICopyPageTicket_, getIntent(expectedIntent)).WillOnce(Return(testIntent));
    EXPECT_EQ(testIntent.get(), pageTicketHandler_.getIntent(expectedIntent).get());
}

TEST_F(GivenACopyPageTicketHandler, WhenSettingInputDetailsToTicket_ThenAttributesAreGet)
{
    // Set Expected Result details
    IPageTicketHandler::InputDetails expectedInputDetails;
    expectedInputDetails.resolution = RESOLUTION;
    expectedInputDetails.colorMode = COLOR_MODE;
    expectedInputDetails.mediaOutputId = MEDIA_DESTINATION;
    expectedInputDetails.margins = MARGINS;
    expectedInputDetails.requestedCopies = REQUESTED_AND_COMPLETED_COPIES;

    std::shared_ptr<CopyPageTicket> copyPageTicket{CopyTicketsUtilities::createDefaultPageTicket()};
    EXPECT_CALL(mockICopyPageTicket_, getPageIntent()).WillOnce(Return(copyPageTicket->getPageIntent()));
    
    auto pageIntent = copyPageTicket->getPageIntent();
    EXPECT_NE(nullptr, pageIntent);

    // Set the Input Details
    pageTicketHandler_.setInputDetails(expectedInputDetails);

    // Get the Input Details
    const IPageTicketHandler::InputDetails& inputDetails = pageTicketHandler_.getInputDetails();

    // Compare the Input Details
    EXPECT_EQ(expectedInputDetails.resolution,          inputDetails.resolution);
    EXPECT_EQ(expectedInputDetails.colorMode,           inputDetails.colorMode);
    EXPECT_EQ(expectedInputDetails.mediaOutputId,       inputDetails.mediaOutputId);
    EXPECT_EQ(expectedInputDetails.margins,             inputDetails.margins);
    EXPECT_EQ(expectedInputDetails.requestedCopies,     inputDetails.requestedCopies);
}

TEST_F(GivenACopyPageTicketHandler, WhenSettingInputDetailsToTicketWithoutPageIntent_ThenAttributesAreNotGet)
{
    // Set Expected Result details
    IPageTicketHandler::InputDetails expectedInputDetails;
    expectedInputDetails.resolution = RESOLUTION;
    expectedInputDetails.colorMode = COLOR_MODE;
    expectedInputDetails.mediaOutputId = MEDIA_DESTINATION;
    expectedInputDetails.margins = MARGINS;
    expectedInputDetails.requestedCopies = REQUESTED_AND_COMPLETED_COPIES;

    std::shared_ptr<CopyPageTicket> copyPageTicket{CopyTicketsUtilities::createDefaultPageTicket()};
    ON_CALL(mockICopyPageTicket_, getPageIntent()).WillByDefault(Return(nullptr));

    // Get print page intent
    auto printPageIntent = copyPageTicket->getPageIntent()->getPrintPageIntent();

    // Set the Input Details
    pageTicketHandler_.setInputDetails(expectedInputDetails);

    // Compare the Input Details
    EXPECT_NE(expectedInputDetails.resolution,          printPageIntent->getResolution());
    EXPECT_NE(expectedInputDetails.colorMode,           printPageIntent->getColorMode());
    EXPECT_NE(expectedInputDetails.mediaOutputId,       printPageIntent->getMediaDestination());
    EXPECT_NE(expectedInputDetails.margins,             printPageIntent->getMargins());
    EXPECT_NE(expectedInputDetails.requestedCopies,     printPageIntent->getRequestedCopies());
}

TEST_F(GivenACopyPageTicketHandler, WhenSettingInputDetailsToTicketWithPrintPageIntent_ThenAttributesAreGet)
{
    // Set Expected Result details
    IPageTicketHandler::InputDetails expectedInputDetails;
    expectedInputDetails.resolution = RESOLUTION;
    expectedInputDetails.colorMode = COLOR_MODE;
    expectedInputDetails.mediaOutputId = MEDIA_DESTINATION;
    expectedInputDetails.margins = MARGINS;
    expectedInputDetails.requestedCopies = REQUESTED_AND_COMPLETED_COPIES;

    std::shared_ptr<CopyPageTicket> copyPageTicket{CopyTicketsUtilities::createDefaultPageTicket()};
    ON_CALL(mockICopyPageTicket_, getPageIntent()).WillByDefault(Return(copyPageTicket->getPageIntent()));

    // Get print page intent
    auto printPageIntent = copyPageTicket->getPageIntent()->getPrintPageIntent();

    // Set the Input Details
    pageTicketHandler_.setInputDetails(expectedInputDetails);

    // Compare the Input Details
    EXPECT_EQ(expectedInputDetails.resolution,          printPageIntent->getResolution());
    EXPECT_EQ(expectedInputDetails.colorMode,           printPageIntent->getColorMode());
    EXPECT_EQ(expectedInputDetails.mediaOutputId,       printPageIntent->getMediaDestination());
    EXPECT_EQ(expectedInputDetails.margins,             printPageIntent->getMargins());
    EXPECT_EQ(expectedInputDetails.requestedCopies,     printPageIntent->getRequestedCopies());
}

TEST_F(GivenACopyPageTicketHandler, WhenSettingResultDetailsToTicket_ThenAttributesAreGet)
{
    // Set Expected Result details
    IPageTicketHandler::ResultDetails expectedResultDetails;
    expectedResultDetails.scannedWidth = SCANNED_WIDTH;
    expectedResultDetails.scannedHeight = SCANNED_HEIGHT;
    expectedResultDetails.outputSize = MEDIA_SIZE;
    expectedResultDetails.impressionWidth = IMPRESSION_WIDTH;
    expectedResultDetails.impressionHeight = IMPRESSION_HEIGHT;
    expectedResultDetails.estimatedPrintTime = ESTIMATED_PRINT_TIME;
    expectedResultDetails.completedCopies = REQUESTED_AND_COMPLETED_COPIES;
    expectedResultDetails.printed = true;
    expectedResultDetails.rendered = true;

    std::shared_ptr<CopyPageTicket> copyPageTicket{CopyTicketsUtilities::createDefaultPageTicket()};
    EXPECT_CALL(mockICopyPageTicket_, getPageResult()).WillOnce(Return(copyPageTicket->getPageResult()));
    
    auto pageResult = copyPageTicket->getPageResult();
    EXPECT_NE(nullptr, pageResult);

    // Set the Result Details
    pageTicketHandler_.setResultDetails(expectedResultDetails);

    // Get the Result Details
    const IPageTicketHandler::ResultDetails& resultDetails{pageTicketHandler_.getResultDetails()};
    
    // Compare the result Details
    EXPECT_EQ(expectedResultDetails.scannedWidth,        resultDetails.scannedWidth);
    EXPECT_EQ(expectedResultDetails.scannedHeight,       resultDetails.scannedHeight);
    EXPECT_EQ(expectedResultDetails.outputSize,          resultDetails.outputSize);
    EXPECT_EQ(expectedResultDetails.impressionWidth,     resultDetails.impressionWidth);
    EXPECT_EQ(expectedResultDetails.impressionHeight,    resultDetails.impressionHeight);
    EXPECT_EQ(expectedResultDetails.estimatedPrintTime,  resultDetails.estimatedPrintTime);
    EXPECT_EQ(expectedResultDetails.completedCopies,     resultDetails.completedCopies);
    EXPECT_EQ(expectedResultDetails.printed,             resultDetails.printed);
    EXPECT_EQ(expectedResultDetails.rendered,            resultDetails.rendered);
}

TEST_F(GivenACopyPageTicketHandler, WhenSettingResultDetailsToTicketWithoutPageResult_ThenAttributesAreNotGet)
{
    // Set Expected Result details
    IPageTicketHandler::ResultDetails expectedResultDetails;
    expectedResultDetails.scannedWidth = SCANNED_WIDTH;
    expectedResultDetails.scannedHeight = SCANNED_HEIGHT;
    expectedResultDetails.outputSize = MEDIA_SIZE;
    expectedResultDetails.impressionWidth = IMPRESSION_WIDTH;
    expectedResultDetails.impressionHeight = IMPRESSION_HEIGHT;
    expectedResultDetails.estimatedPrintTime = ESTIMATED_PRINT_TIME;
    expectedResultDetails.completedCopies = REQUESTED_AND_COMPLETED_COPIES;
    expectedResultDetails.printed = true;
    expectedResultDetails.rendered = true;

    std::shared_ptr<CopyPageTicket> copyPageTicket{CopyTicketsUtilities::createDefaultPageTicket()};
    ON_CALL(mockICopyPageTicket_, getPageResult()).WillByDefault(Return(nullptr));
    
    // Get print page result and scan page result
    auto printPageResult = copyPageTicket->getPageResult()->getPrintPageResult();
    auto scanPageResult = copyPageTicket->getPageResult()->getScanPageResult();

    // Set the Result Details
    pageTicketHandler_.setResultDetails(expectedResultDetails);
    
    // Compare the result Details
    EXPECT_NE(expectedResultDetails.scannedWidth,        scanPageResult->getScannedWidth());
    EXPECT_NE(expectedResultDetails.scannedHeight,       scanPageResult->getScannedHeight());
    EXPECT_NE(expectedResultDetails.outputSize,          printPageResult->getOutputSize());
    EXPECT_NE(expectedResultDetails.impressionWidth,     printPageResult->getImpressionWidth());
    EXPECT_NE(expectedResultDetails.impressionHeight,    printPageResult->getImpressionHeight());
    EXPECT_NE(expectedResultDetails.estimatedPrintTime,  printPageResult->getEstimatedPrintTime());
    EXPECT_NE(expectedResultDetails.completedCopies,     printPageResult->getCompletedCopies());
    EXPECT_NE(expectedResultDetails.printed,             printPageResult->isPrinted());
    EXPECT_NE(expectedResultDetails.rendered,            printPageResult->isRendered());
}

TEST_F(GivenACopyPageTicketHandler, WhenSettingResultDetailsToTicketWithPrinPageResultAndScanPageResult_ThenAttributesAreGet)
{
    // Set Expected Result details
    IPageTicketHandler::ResultDetails expectedResultDetails;
    expectedResultDetails.scannedWidth = SCANNED_WIDTH;
    expectedResultDetails.scannedHeight = SCANNED_HEIGHT;
    expectedResultDetails.outputSize = MEDIA_SIZE;
    expectedResultDetails.impressionWidth = IMPRESSION_WIDTH;
    expectedResultDetails.impressionHeight = IMPRESSION_HEIGHT;
    expectedResultDetails.estimatedPrintTime = ESTIMATED_PRINT_TIME;
    expectedResultDetails.completedCopies = REQUESTED_AND_COMPLETED_COPIES;
    expectedResultDetails.printed = true;
    expectedResultDetails.rendered = true;

    std::shared_ptr<CopyPageTicket> copyPageTicket{CopyTicketsUtilities::createDefaultPageTicket()};
    ON_CALL(mockICopyPageTicket_, getPageResult()).WillByDefault(Return(copyPageTicket->getPageResult()));
    
    // Get print page result and scan page result
    auto printPageResult = copyPageTicket->getPageResult()->getPrintPageResult();
    auto scanPageResult = copyPageTicket->getPageResult()->getScanPageResult();

    // Set the Result Details
    pageTicketHandler_.setResultDetails(expectedResultDetails);
    
    // Compare the result Details
    EXPECT_EQ(expectedResultDetails.scannedWidth,        scanPageResult->getScannedWidth());
    EXPECT_EQ(expectedResultDetails.scannedHeight,       scanPageResult->getScannedHeight());
    EXPECT_EQ(expectedResultDetails.outputSize,          printPageResult->getOutputSize());
    EXPECT_EQ(expectedResultDetails.impressionWidth,     printPageResult->getImpressionWidth());
    EXPECT_EQ(expectedResultDetails.impressionHeight,    printPageResult->getImpressionHeight());
    EXPECT_EQ(expectedResultDetails.estimatedPrintTime,  printPageResult->getEstimatedPrintTime());
    EXPECT_EQ(expectedResultDetails.completedCopies,     printPageResult->getCompletedCopies());
    EXPECT_EQ(expectedResultDetails.printed,             printPageResult->isPrinted());
    EXPECT_EQ(expectedResultDetails.rendered,            printPageResult->isRendered());
}