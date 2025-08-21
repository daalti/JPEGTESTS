////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobTicketHandlerGtest.cpp
 * @brief  CopyJobTicketHandler unit tests
 *
 * (C) Sampleright 2021 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "gmock/gmock.h"
#include "gtest/gtest.h"
#include "ConstraintsGroup.h"
#include "CopyJobTicketHandlerGtest_TraceAutogen.h"

#include "MockIPageTicket.h"
#include "MockIPageTicketHandler.h"
#include "MockICopyJobTicket.h"
#include "CopyJobTicketHandler.h"
#include "MockIMedia.h"

using namespace dune::imaging::types;
using namespace dune::copy::Jobs::Copy;
using namespace dune::job;
using namespace dune::framework::core;

using Margins = dune::imaging::types::Margins;
using Distance = dune::imaging::types::Distance;
using dune::print::engine::MockIMedia;

using ::testing::_;
using ::testing::InvokeWithoutArgs;
using ::testing::Invoke;
using ::testing::Return;
using ::testing::ReturnRef;

using PageTicketEventSource =
    dune::framework::core::event::EventSource<IPageTicket, std::shared_ptr<IPageTicket>>;  // Actual ticket, Original
                                                                                           // Ticket (not changed)

static const std::string         MAGIC_STRING{"Magic String"};
static constexpr uint8_t         MAGIC_NUMBER{7};
static constexpr PrintQuality    MAGIC_QUALITY{PrintQuality::BEST};
static constexpr ColorMode       MAGIC_COLOR_MODE{ColorMode::COLOR};
static constexpr uint32_t        MAGIC_DURATION{1000};

class TestableCopyJobTicketHandler : public CopyJobTicketHandler{
public:
    TestableCopyJobTicketHandler(ICopyJobTicket& ticket, const JobTicketEvents& jobTicketEvents,
                          dune::framework::core::ThreadPool* threadPool)
        : CopyJobTicketHandler(ticket, jobTicketEvents, threadPool)
    {
    }
    // Expose doSetResultDetails through a public method
    void testSetResultDetails(const IJobTicketHandler::ResultDetails& resultDetails,
                                     const std::vector<IJobTicketHandler::ResultDetailsProperties>& propertiesToBeUpdated) {
        this->doSetResultDetails(resultDetails, propertiesToBeUpdated);
    }
    // Expose doSetDocumentSettings through a public method
    void testSetDocumentSettings(const IJobTicketHandler::DocumentSettings& documentSettings,
                                     const std::vector<IJobTicketHandler::DocumentSettingsProperties>& propertiesToBeUpdated) {
        this->doSetDocumentSettings(documentSettings, propertiesToBeUpdated);
    }
    // Expose doSetInputDetails through a public method
    void testSetInputDetails(const IJobTicketHandler::InputDetails& inputDetails,
                                     const std::vector<IJobTicketHandler::InputDetailsProperties>& propertiesToBeUpdated) {
        this->doSetInputDetails(inputDetails, propertiesToBeUpdated);
    }
};

class GivenACopyJobTicketHandlerWithoutThreadPool : public ::testing::Test
{
  public:
    GivenACopyJobTicketHandlerWithoutThreadPool();

    virtual void SetUp() override;
    virtual void TearDown() override;

  protected:
    MockICopyJobTicket  mockICopyJobTicket_;
    std::shared_ptr<MockICopyJobIntent>    mockICopyJobIntent_;
    std::shared_ptr<MockICopyJobResult>    mockICopyJobResult_;
    JobTicketEventSource jobTicketEventSource_;
    JobTicketPageEventSource jobTicketPageEventSource_;

    std::unique_ptr<TestableCopyJobTicketHandler> copyJobTicketHandler_;
};

GivenACopyJobTicketHandlerWithoutThreadPool::GivenACopyJobTicketHandlerWithoutThreadPool()
    : mockICopyJobTicket_{},
      mockICopyJobIntent_{std::make_shared<MockICopyJobIntent>()},
      mockICopyJobResult_{std::make_shared<MockICopyJobResult>()},
      jobTicketEventSource_{&mockICopyJobTicket_},
      jobTicketPageEventSource_{&mockICopyJobTicket_},
      copyJobTicketHandler_{nullptr}
{
}

void GivenACopyJobTicketHandlerWithoutThreadPool::SetUp()
{
    ON_CALL(mockICopyJobTicket_, getIntent()).WillByDefault(Return(mockICopyJobIntent_));

    ON_CALL(mockICopyJobTicket_, getApplicationName()).WillByDefault(ReturnRef(MAGIC_STRING));
    ON_CALL(mockICopyJobTicket_, getUserName()).WillByDefault(Return(MAGIC_STRING));

    ON_CALL(*mockICopyJobIntent_, getCopies()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobIntent_, getCopyQuality()).WillByDefault(Return(MAGIC_QUALITY));
    ON_CALL(*mockICopyJobIntent_, getRequestedPages()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobIntent_, getColorMode()).WillByDefault(Return(MAGIC_COLOR_MODE));
    ON_CALL(*mockICopyJobIntent_, getCollate()).WillByDefault(Return(dune::copy::SheetCollate::Collate));
    ON_CALL(*mockICopyJobIntent_, getScanNumberPages()).WillByDefault(Return(MAGIC_NUMBER));

    // Results Details
    ON_CALL(mockICopyJobTicket_,  getResult()).WillByDefault(Return(mockICopyJobResult_));
    ON_CALL(*mockICopyJobResult_, getProgress()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getCompletedImpressions()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getCompletedCopies()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getCurrentPage()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getRemainingPrintingTime()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getCurrentCuringTemperature()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getTotalScanDuration()).WillByDefault(Return(MAGIC_DURATION));
    ON_CALL(*mockICopyJobResult_, getActiveScanDuration()).WillByDefault(Return(MAGIC_DURATION));

    copyJobTicketHandler_ = std::make_unique<TestableCopyJobTicketHandler>(
        mockICopyJobTicket_, CopyJobTicketHandler::JobTicketEvents{jobTicketEventSource_, jobTicketPageEventSource_},
        nullptr);
}

void GivenACopyJobTicketHandlerWithoutThreadPool::TearDown()
{

}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenGettingDocumentSettings_ThenAttributesAreGet)
{
    // Fill document settings
    IJobTicketHandler::DocumentSettings expectedDocumentSettings;
    expectedDocumentSettings.jobName = "TestName";

    // Ticket is set with document settings values
    EXPECT_CALL(mockICopyJobTicket_, getJobName()).WillOnce(ReturnRef(expectedDocumentSettings.jobName));

    // Get document settings
    IJobTicketHandler::DocumentSettings documentSettings{copyJobTicketHandler_->getDocumentSettings()};

    // Compare data
    EXPECT_EQ(expectedDocumentSettings.jobName, documentSettings.jobName);
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenGettingInputDetails_ThenAttributesAreGet)
{
    // Get inputDetails
    IJobTicketHandler::InputDetails inputDetails{copyJobTicketHandler_->getInputDetails()};

    // Compare data
    EXPECT_EQ(MAGIC_STRING, inputDetails.applicationName);
    EXPECT_EQ(MAGIC_STRING, inputDetails.userName);
    EXPECT_EQ(MAGIC_NUMBER, inputDetails.requestedCopies);
    EXPECT_EQ(MAGIC_NUMBER, inputDetails.requestedPages);
    EXPECT_EQ(MAGIC_QUALITY,    inputDetails.printQuality);
    EXPECT_EQ(MAGIC_COLOR_MODE, inputDetails.colorMode);
    EXPECT_EQ(true,             inputDetails.isCollated);
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenSettingResultDetails_ThenAttributesAreset)
{
    IJobTicketHandler::ResultDetails        resultDetails;

    resultDetails.progress                 = 10;
    resultDetails.completedImpressions     = 3;
    resultDetails.completedCopies          = 3;
    resultDetails.currentPage              = 2;
    resultDetails.nonWhitePixelCount       = MAGIC_NUMBER;
    resultDetails.colorPixelCount          = MAGIC_NUMBER + 1;
    resultDetails.totalPixelCount          = MAGIC_NUMBER + 2;
    const PixelCounts pixelCounts{resultDetails.nonWhitePixelCount, resultDetails.colorPixelCount, resultDetails.totalPixelCount};
    EXPECT_CALL(*mockICopyJobResult_, setProgress(resultDetails.progress)).Times(1);
    EXPECT_CALL(*mockICopyJobResult_, setCompletedImpressions(resultDetails.completedImpressions)).Times(1);
    EXPECT_CALL(*mockICopyJobResult_, setCompletedCopies(resultDetails.completedCopies)).Times(1);
    EXPECT_CALL(*mockICopyJobResult_, setCurrentPage(resultDetails.currentPage)).Times(1);
    EXPECT_CALL(*mockICopyJobResult_, setPixelCounts(_)).Times(3);
    EXPECT_CALL(*mockICopyJobResult_, setTotalScanDuration(resultDetails.totalScanDuration)).Times(1);
    EXPECT_CALL(*mockICopyJobResult_, setActiveScanDuration(resultDetails.activeScanDuration)).Times(1);

    std::vector<IJobTicketHandler::ResultDetailsProperties> propertiesToBeUpdated = {IJobTicketHandler::ResultDetailsProperties::PROGRESS,
                                                                                     IJobTicketHandler::ResultDetailsProperties::COMPLETED_IMPRESSIONS,
                                                                                     IJobTicketHandler::ResultDetailsProperties::COMPLETED_COPIES,
                                                                                     IJobTicketHandler::ResultDetailsProperties::CURRENT_PAGE,
                                                                                     IJobTicketHandler::ResultDetailsProperties::NON_WHITE_PIXEL_COUNT,
                                                                                     IJobTicketHandler::ResultDetailsProperties::COLOR_PIXEL_COUNT,
                                                                                     IJobTicketHandler::ResultDetailsProperties::TOTAL_PIXEL_COUNT,
                                                                                     IJobTicketHandler::ResultDetailsProperties::SCAN_TOTAL_DURATION,
                                                                                     IJobTicketHandler::ResultDetailsProperties::SCAN_ACTIVE_DURATION};

    copyJobTicketHandler_->testSetResultDetails(resultDetails, propertiesToBeUpdated);

    EXPECT_CALL(*mockICopyJobResult_, getProgress()).WillOnce(Return(resultDetails.progress));
    EXPECT_CALL(*mockICopyJobResult_, getCompletedImpressions()).WillOnce(Return(resultDetails.completedImpressions));
    EXPECT_CALL(*mockICopyJobResult_, getCompletedCopies()).WillOnce(Return(resultDetails.completedCopies));
    EXPECT_CALL(*mockICopyJobResult_, getCurrentPage()).WillOnce(Return(resultDetails.currentPage));
    EXPECT_CALL(*mockICopyJobResult_, getPixelCounts()).Times(3).WillRepeatedly(Return(pixelCounts));
    EXPECT_CALL(*mockICopyJobResult_, getTotalScanDuration()).WillOnce(Return(resultDetails.totalScanDuration));
    EXPECT_CALL(*mockICopyJobResult_, getActiveScanDuration()).WillOnce(Return(resultDetails.activeScanDuration));

    auto actualResultDetail = copyJobTicketHandler_->getResultDetails();

    // Compare data
    EXPECT_EQ(resultDetails.progress, actualResultDetail.progress);
    EXPECT_EQ(resultDetails.completedImpressions, actualResultDetail.completedImpressions);
    EXPECT_EQ(resultDetails.completedCopies, actualResultDetail.completedCopies);
    EXPECT_EQ(resultDetails.currentPage, actualResultDetail.currentPage);
    EXPECT_EQ(resultDetails.nonWhitePixelCount, actualResultDetail.nonWhitePixelCount);
    EXPECT_EQ(resultDetails.colorPixelCount, actualResultDetail.colorPixelCount);
    EXPECT_EQ(resultDetails.totalPixelCount, actualResultDetail.totalPixelCount);
    EXPECT_EQ(resultDetails.totalScanDuration, actualResultDetail.totalScanDuration);
    EXPECT_EQ(resultDetails.activeScanDuration, actualResultDetail.activeScanDuration);
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenSettingDocumentSettings_ThenAttributesAreSet)
{
    // Fill document settings
    IJobTicketHandler::DocumentSettings documentSettings;
    documentSettings.jobName = "TestName";

    // Ticket is set with document settings values
    EXPECT_CALL(mockICopyJobTicket_, setJobName(documentSettings.jobName)).Times(1);

    // Set document settings
    copyJobTicketHandler_->testSetDocumentSettings(documentSettings, {IJobTicketHandler::DocumentSettingsProperties::JOB_NAME});
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenGetMarginIsCalLed_CorrectMarginIsRetrun)
{
    // Fill document settings
    IJobTicketHandler::DocumentSettings documentSettings;
    documentSettings.jobName = "TestName";
    std::shared_ptr<MockIMedia>           mediaInterface{std::make_shared<MockIMedia>()};
    EXPECT_CALL(mockICopyJobTicket_, getMediaInterface())
        .WillRepeatedly(Return(mediaInterface.get()));
    
    Margins desiredMargins_{Distance(236, 1200), Distance(236, 1200), Distance(236, 1200), Distance(236, 1200)};

    EXPECT_CALL(*mediaInterface, getMargins(_))
        .WillRepeatedly(Return(std::tuple<APIResult, Margins>(APIResult::OK, desiredMargins_)));
    // Set document settings
    std::shared_ptr<dune::imaging::types::Margins> margins = copyJobTicketHandler_->getMargins(dune::imaging::types::MediaSizeId::A4);
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenAddingPageTicket_ThenAttributesAreSetAndChangesAreNotified)
{
    Uuid pageId{Uuid::createUuid()};

    auto mockIPageTicket{std::make_shared<MockIPageTicket>()};
    PageTicketEventSource pageTicketEventSource{mockIPageTicket.get()};

    // Page ticket is added
    EXPECT_CALL(mockICopyJobTicket_, addPage(pageId)).WillOnce(Return(mockIPageTicket));

    // Subscribe to events
    EXPECT_CALL(*mockIPageTicket, getPageTicketChanged()).WillOnce(ReturnRef(pageTicketEventSource));

    // Get handler
    EXPECT_CALL(*mockIPageTicket, getHandler()).WillOnce(InvokeWithoutArgs([]() {
        return std::make_shared<MockIPageTicketHandler>();
    }));
    EXPECT_CALL(mockICopyJobTicket_, getPage(_)).Times(2).WillRepeatedly(Return(mockIPageTicket));

    EXPECT_NE(nullptr, copyJobTicketHandler_->addPage(pageId));
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenAddingAPageWithPageMetaInfo_ThenPageMetaInfoIsAddedToTheTicket)
{
    std::shared_ptr<dune::imaging::types::PageMetaInfoT> pageMetaInfo =
        std::make_shared<dune::imaging::types::PageMetaInfoT>();
    Uuid pageId{Uuid::createUuid()};

    auto                  mockIPageTicket{std::make_shared<MockIPageTicket>()};
    PageTicketEventSource pageTicketEventSource{mockIPageTicket.get()};

    // Page ticket is added
    EXPECT_CALL(mockICopyJobTicket_, addPage(pageId, pageMetaInfo)).WillOnce(Return(mockIPageTicket));
    EXPECT_CALL(*mockIPageTicket, getPageTicketChanged()).WillOnce(ReturnRef(pageTicketEventSource));

    // EXPECT Get Page is called when notify and to get the handler
    EXPECT_CALL(mockICopyJobTicket_, getPage(pageId))
        .WillOnce(Return(mockIPageTicket))
        .WillOnce(Return(mockIPageTicket));

    // Get handler
    EXPECT_CALL(*mockIPageTicket, getHandler()).WillOnce(InvokeWithoutArgs([]() {
        return std::make_shared<MockIPageTicketHandler>();
    }));
    EXPECT_NE(nullptr, copyJobTicketHandler_->addPage(pageId, pageMetaInfo));
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenSettingInputDetails_ThenAttributesAreSet)
{
    // Get inputDetails
    IJobTicketHandler::InputDetails inputDetails{copyJobTicketHandler_->getInputDetails()};

    inputDetails.requestedPages = 2;
    inputDetails.scannedPages = 1;
    inputDetails.printQuality = dune::imaging::types::PrintQuality::BEST;
    inputDetails.applicationName = "demo";

    // Ticket is set with inputDetails settings values
    EXPECT_CALL(mockICopyJobTicket_, setApplicationName(inputDetails.applicationName)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setCopyQuality(inputDetails.printQuality)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setRequestedPages(inputDetails.requestedPages)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setScanNumberPages(inputDetails.scannedPages)).Times(1);

    // Set inputDetails settings
    copyJobTicketHandler_->testSetInputDetails(inputDetails, {IJobTicketHandler::InputDetailsProperties::REQUESTED_PAGES,
                                                              IJobTicketHandler::InputDetailsProperties::REQUESTED_COPIES,
                                                              IJobTicketHandler::InputDetailsProperties::PRINT_QUALITY,
                                                              IJobTicketHandler::InputDetailsProperties::APPLICATION_NAME,
                                                              IJobTicketHandler::InputDetailsProperties::SCANNED_PAGES});
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenGettingMediaSettings_ThenAttributesAreGet)
{
    IJobTicketHandler::MediaSettings expectedMediaSettings;
    expectedMediaSettings.mediaSize = dune::imaging::types::MediaSizeId::A1;
    expectedMediaSettings.mediaType = dune::imaging::types::MediaIdType::BLUEPRINT;
    expectedMediaSettings.mediaSource = dune::imaging::types::MediaSource::ROLL2;

    // Return Expected Media Size
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillRepeatedly(Return(expectedMediaSettings.mediaSize));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaIdType()).WillRepeatedly(Return(expectedMediaSettings.mediaType));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSource()).WillRepeatedly(Return(expectedMediaSettings.mediaSource));

    // Get and compare data
    IJobTicketHandler::MediaSettings mediaSettings = copyJobTicketHandler_->getMediaSettings();
    EXPECT_EQ(expectedMediaSettings.mediaSize,   mediaSettings.mediaSize);
    EXPECT_EQ(expectedMediaSettings.mediaType,   mediaSettings.mediaType);
    EXPECT_EQ(expectedMediaSettings.mediaSource, mediaSettings.mediaSource);
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenSettingInputDetailsWithIDCard_ThenAttributesAreSet)
{
    EXPECT_CALL(*mockICopyJobIntent_, getScanCaptureMode()).WillRepeatedly(Return(dune::scan::types::ScanCaptureModeType::IDCARD));
    // Get inputDetails
    IJobTicketHandler::InputDetails inputDetails{copyJobTicketHandler_->getInputDetails()};

    inputDetails.requestedPages = 2;
    inputDetails.scannedPages = 1;
    inputDetails.colorMode = ColorMode::COLOR;
    inputDetails.isCollated = false;
    inputDetails.printQuality = dune::imaging::types::PrintQuality::BEST; 

    // Ticket is set with inputDetails settings values
    EXPECT_CALL(mockICopyJobTicket_, setApplicationName(inputDetails.applicationName)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setCopyQuality(inputDetails.printQuality)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setRequestedPages(inputDetails.requestedPages)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setRequestedPages(1 * MAGIC_NUMBER)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setScanNumberPages(inputDetails.scannedPages)).Times(1);

    // Set inputDetails settings
    copyJobTicketHandler_->setInputDetails(inputDetails, {IJobTicketHandler::InputDetailsProperties::APPLICATION_NAME,
                                                          IJobTicketHandler::InputDetailsProperties::PRINT_QUALITY,
                                                          IJobTicketHandler::InputDetailsProperties::REQUESTED_PAGES,
                                                          IJobTicketHandler::InputDetailsProperties::IS_COLLATED,
                                                          IJobTicketHandler::InputDetailsProperties::SCANNED_PAGES});
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenSettingInputDetailsWithTwoUp_ThenAttributesAreSet)
{
    EXPECT_CALL(*mockICopyJobIntent_, getPagesPerSheet()).WillRepeatedly(Return(dune::imaging::types::CopyOutputNumberUpCount::TwoUp));
    // Get inputDetails
    IJobTicketHandler::InputDetails inputDetails{copyJobTicketHandler_->getInputDetails()};

    inputDetails.requestedPages = 2;
    inputDetails.scannedPages = 1;
    inputDetails.colorMode = ColorMode::COLOR;
    inputDetails.isCollated = false;
    inputDetails.printQuality = dune::imaging::types::PrintQuality::BEST;

    // Ticket is set with inputDetails settings values
    EXPECT_CALL(mockICopyJobTicket_, setApplicationName(inputDetails.applicationName)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setCopyQuality(inputDetails.printQuality)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setRequestedPages(inputDetails.requestedPages)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setRequestedPages(1*MAGIC_NUMBER)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setScanNumberPages(inputDetails.scannedPages)).Times(1);

    // Set inputDetails settings
    copyJobTicketHandler_->setInputDetails(inputDetails, {IJobTicketHandler::InputDetailsProperties::APPLICATION_NAME,
                                                          IJobTicketHandler::InputDetailsProperties::SCANNED_PAGES,
                                                          IJobTicketHandler::InputDetailsProperties::REQUESTED_PAGES,
                                                          IJobTicketHandler::InputDetailsProperties::COLOR_MODE,
                                                          IJobTicketHandler::InputDetailsProperties::IS_COLLATED,
                                                          IJobTicketHandler::InputDetailsProperties::PRINT_QUALITY});
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenSettingInputDetailsWithFourUp_ThenAttributesAreSet)
{
    EXPECT_CALL(*mockICopyJobIntent_, getPagesPerSheet()).WillRepeatedly(Return(dune::imaging::types::CopyOutputNumberUpCount::FourUp));
    // Get inputDetails
    IJobTicketHandler::InputDetails inputDetails{copyJobTicketHandler_->getInputDetails()};

    inputDetails.requestedPages = 8;
    inputDetails.scannedPages = 8;
    inputDetails.colorMode = ColorMode::COLOR;
    inputDetails.isCollated = false;
    inputDetails.printQuality = dune::imaging::types::PrintQuality::BEST;

    // Ticket is set with inputDetails settings values
    EXPECT_CALL(mockICopyJobTicket_, setApplicationName(inputDetails.applicationName)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setCopyQuality(inputDetails.printQuality)).Times(1);
    uint32_t requestedPages;
    EXPECT_CALL(*mockICopyJobIntent_, setRequestedPages(_)).WillRepeatedly(
            ::testing::Invoke([this, &requestedPages](uint32_t value) -> void {
                requestedPages = value;
            }));
    EXPECT_CALL(*mockICopyJobIntent_, setScanNumberPages(inputDetails.scannedPages)).Times(1);

    // Set inputDetails settings
    copyJobTicketHandler_->setInputDetails(inputDetails, {IJobTicketHandler::InputDetailsProperties::APPLICATION_NAME,
                                                          IJobTicketHandler::InputDetailsProperties::SCANNED_PAGES,
                                                          IJobTicketHandler::InputDetailsProperties::REQUESTED_PAGES,
                                                          IJobTicketHandler::InputDetailsProperties::COLOR_MODE,
                                                          IJobTicketHandler::InputDetailsProperties::IS_COLLATED,
                                                          IJobTicketHandler::InputDetailsProperties::PRINT_QUALITY});
    EXPECT_EQ(14, requestedPages);
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenSettingInputDetailsWithFourUpScannedPageAs5_ThenAttributesAreSet)
{
    EXPECT_CALL(*mockICopyJobIntent_, getPagesPerSheet()).WillRepeatedly(Return(dune::imaging::types::CopyOutputNumberUpCount::FourUp));
    // Get inputDetails
    IJobTicketHandler::InputDetails inputDetails{copyJobTicketHandler_->getInputDetails()};

    inputDetails.requestedPages = 8;
    inputDetails.scannedPages = 5;
    inputDetails.colorMode = ColorMode::COLOR;
    inputDetails.isCollated = false;
    inputDetails.printQuality = dune::imaging::types::PrintQuality::BEST;

    // Ticket is set with inputDetails settings values
    EXPECT_CALL(mockICopyJobTicket_, setApplicationName(inputDetails.applicationName)).Times(1);
    EXPECT_CALL(*mockICopyJobIntent_, setCopyQuality(inputDetails.printQuality)).Times(1);
    uint32_t requestedPages;
    EXPECT_CALL(*mockICopyJobIntent_, setRequestedPages(_)).WillRepeatedly(
            ::testing::Invoke([this, &requestedPages](uint32_t value) -> void {
                requestedPages = value;
            }));
    EXPECT_CALL(*mockICopyJobIntent_, setScanNumberPages(inputDetails.scannedPages)).Times(1);

    // Set inputDetails settings
    copyJobTicketHandler_->setInputDetails(inputDetails, {IJobTicketHandler::InputDetailsProperties::APPLICATION_NAME,
                                                          IJobTicketHandler::InputDetailsProperties::SCANNED_PAGES,
                                                          IJobTicketHandler::InputDetailsProperties::REQUESTED_PAGES,
                                                          IJobTicketHandler::InputDetailsProperties::COLOR_MODE,
                                                          IJobTicketHandler::InputDetailsProperties::IS_COLLATED,
                                                          IJobTicketHandler::InputDetailsProperties::PRINT_QUALITY});
    EXPECT_EQ(14, requestedPages);
}

TEST_F(GivenACopyJobTicketHandlerWithoutThreadPool, WhenRemovePageIsCalled_ThenScannedPagesAndRequestedPagesIsUpdated)
{
    PageNotification::Action action = PageNotification::Action::ADDED;

    // Page removed notification
    auto subscription = jobTicketPageEventSource_.addSubscriptionEx(
        [&](IJobTicket* jobTicket, std::shared_ptr<PageNotification> pageNotification) {
            action = pageNotification->action;
        });

    int requestedPages = 1;
    int requestCopies = 1;
    uint scannedPages = 2;

    EXPECT_CALL(*mockICopyJobIntent_, getRequestedPages()).WillRepeatedly(Return(requestedPages));
    EXPECT_CALL(*mockICopyJobIntent_, getScanNumberPages()).WillRepeatedly(Return(scannedPages));
    EXPECT_CALL(*mockICopyJobIntent_, getCopies()).WillRepeatedly(Return(requestCopies));

    EXPECT_CALL(*mockICopyJobIntent_, setRequestedPages(_)).WillOnce(testing::Invoke(
        [&] (int value)
        {
            requestedPages = value;
        }
    ));
    EXPECT_CALL(*mockICopyJobIntent_, setScanNumberPages(_)).WillOnce(testing::Invoke(
        [&] (uint value)
        {
            scannedPages = value;
        }
    ));

    copyJobTicketHandler_->removePage(Uuid::createUuid());

    EXPECT_EQ(PageNotification::Action::REMOVED, action);

    EXPECT_EQ(0, requestedPages);
    EXPECT_EQ(1, scannedPages);
    EXPECT_EQ(1, requestCopies);
}

class GivenACopyJobTicketHandlerWithThreadPool : public ::testing::Test
{
  public:
    GivenACopyJobTicketHandlerWithThreadPool();

    virtual void SetUp() override;
    virtual void TearDown() override;

  protected:
    MockICopyJobTicket  mockICopyJobTicket_;
    std::shared_ptr<MockICopyJobIntent>    mockICopyJobIntent_;
    std::shared_ptr<MockICopyJobResult>    mockICopyJobResult_;

    JobTicketEventSource jobTicketEventSource_;
    JobTicketPageEventSource jobTicketPageEventSource_;
    ThreadPool            threadPool_;

    std::unique_ptr<CopyJobTicketHandler> copyJobTicketHandler_;
};

GivenACopyJobTicketHandlerWithThreadPool::GivenACopyJobTicketHandlerWithThreadPool()
    : mockICopyJobTicket_{},
      mockICopyJobIntent_{std::make_shared<MockICopyJobIntent>()},
      mockICopyJobResult_{std::make_shared<MockICopyJobResult>()},
      jobTicketEventSource_{&mockICopyJobTicket_},
      jobTicketPageEventSource_{&mockICopyJobTicket_},
      threadPool_{ThreadPool::ThreadAttributes{DUNE_THREAD_TEST}, "TestPoolName", 1},
      copyJobTicketHandler_{nullptr}
{
}

void GivenACopyJobTicketHandlerWithThreadPool::SetUp()
{
    ON_CALL(mockICopyJobTicket_, getIntent()).WillByDefault(Return(mockICopyJobIntent_));

    ON_CALL(mockICopyJobTicket_, getApplicationName()).WillByDefault(ReturnRef(MAGIC_STRING));
    ON_CALL(mockICopyJobTicket_, getUserName()).WillByDefault(Return(MAGIC_STRING));

    ON_CALL(*mockICopyJobIntent_, getCopies()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobIntent_, getCopyQuality()).WillByDefault(Return(dune::imaging::types::PrintQuality::BEST));

    // Results Details
    ON_CALL(mockICopyJobTicket_, getResult()).WillByDefault(Return(mockICopyJobResult_));
    ON_CALL(*mockICopyJobResult_, getProgress()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getCompletedImpressions()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getCompletedCopies()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getCurrentPage()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getRemainingPrintingTime()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getCurrentCuringTemperature()).WillByDefault(Return(MAGIC_NUMBER));
    ON_CALL(*mockICopyJobResult_, getTotalScanDuration()).WillByDefault(Return(MAGIC_DURATION));
    ON_CALL(*mockICopyJobResult_, getActiveScanDuration()).WillByDefault(Return(MAGIC_DURATION));

    copyJobTicketHandler_ = std::make_unique<CopyJobTicketHandler>(
        mockICopyJobTicket_, CopyJobTicketHandler::JobTicketEvents{jobTicketEventSource_, jobTicketPageEventSource_},
        nullptr);
}

void GivenACopyJobTicketHandlerWithThreadPool::TearDown()
{

}

TEST_F(GivenACopyJobTicketHandlerWithThreadPool, WhenGettingJobPath_ThenAttributesAreG)
{
    std::string jobPath{"JobPath"};

    // Get Job Path Value
    EXPECT_CALL(mockICopyJobTicket_, getStorePath()).WillOnce(ReturnRef(jobPath));
    EXPECT_EQ(jobPath, copyJobTicketHandler_->getJobPath());
}

TEST_F(GivenACopyJobTicketHandlerWithThreadPool,
       WhenAddingIncorrectPageTicket_ThenAttributesAreNotSetAndChangesAreNotNotified)
{
    Uuid pageId{Uuid::createUuid()};

    // Page ticket is not added
    EXPECT_CALL(mockICopyJobTicket_, addPage(_)).WillOnce(InvokeWithoutArgs([]() { return nullptr; }));
    EXPECT_EQ(nullptr, copyJobTicketHandler_->addPage(pageId));
}

TEST_F(GivenACopyJobTicketHandlerWithThreadPool, WhenAddingPageTicket_ThenAttributesAreSetAndChangesAreNotified)
{
    Uuid pageId{Uuid::createUuid()};

    auto mockIPageTicket{std::make_shared<MockIPageTicket>()};
    PageTicketEventSource pageTicketEventSource{mockIPageTicket.get()};

    // Page ticket is added
    EXPECT_CALL(mockICopyJobTicket_, addPage(pageId)).WillOnce(Return(mockIPageTicket));
    EXPECT_CALL(*mockIPageTicket, getPageTicketChanged()).WillOnce(ReturnRef(pageTicketEventSource));

    // EXPECT Get Page is called when notify and to get the handler
    EXPECT_CALL(mockICopyJobTicket_, getPage(pageId)).WillOnce(Return(mockIPageTicket))
                                                      .WillOnce(Return(mockIPageTicket));

    // Get handler
    EXPECT_CALL(*mockIPageTicket, getHandler()).WillOnce(InvokeWithoutArgs([]() {
        return std::make_shared<MockIPageTicketHandler>();
    }));
    EXPECT_NE(nullptr, copyJobTicketHandler_->addPage(pageId));
}

TEST_F(GivenACopyJobTicketHandlerWithThreadPool, WhenGettingIncorrectPageTicketHander_ThenPageTicketHandlerIsNotGet)
{
    Uuid pageId{Uuid::createUuid()};

    // Page ticket is not get
    EXPECT_CALL(mockICopyJobTicket_, getPage(pageId)).WillOnce(Return(nullptr));

    EXPECT_EQ(nullptr, copyJobTicketHandler_->getPageTicketHandler(pageId));
}

TEST_F(GivenACopyJobTicketHandlerWithThreadPool, WhenGettingPageTicketHandler_ThenPageTicketHandlerIsGet)
{
    Uuid pageId{Uuid::createUuid()};

    // Get handler
    EXPECT_CALL(mockICopyJobTicket_, getPage(pageId)).WillOnce(InvokeWithoutArgs([]() {
        std::shared_ptr<MockIPageTicket> mockICopyPageTicket{std::make_shared<MockIPageTicket>()};
        EXPECT_CALL(*mockICopyPageTicket, getHandler()).WillOnce(InvokeWithoutArgs([]() {
            return std::make_shared<MockIPageTicketHandler>();
        }));
        return mockICopyPageTicket;
    }));

    EXPECT_NE(nullptr, copyJobTicketHandler_->getPageTicketHandler(pageId));
}
