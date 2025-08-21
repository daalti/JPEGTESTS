////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDetailsProviderGtest.cpp
 * @brief  CopyJobTicketHandler unit tests
 * @date   April 11, 2022
 *
 * (C) Sampleright 2021 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "IDateTime.h"
#include "CopyJobDetailsProvider.h"
#include "CopyTicketGtestUtilities.h"
#include "MockICopyJobService.h"
#include "MockICopyJobTicket.h"
#include "MockICopyPageTicket.h"
#include "MockIJobTicket.h"
#include "MockIJobTicketResourceManager.h"
#include "MockIScanPipeline.h"
#include "MockISettings.h"
#include "MockStatsHelper.h"
#include "typeMappers.h"
#include "TestSystemServices.h"
#include "MockIAccessControl.h"
#include "MockIAuthAgent.h"

using namespace dune::imaging::types;
using namespace dune::job;
using namespace dune::job::cdm;
using namespace dune::copy::Jobs::Copy;
using namespace dune::cdm::jobManagement_1;
using namespace dune::cdm::glossary_1;
using namespace dune::cdm::jobTicket_1;
using namespace dune::security::ac;

using ::testing::_;
using ::testing::Invoke;
using ::testing::Return;
using ::testing::ReturnRef;

using MockISettings = dune::print::engine::MockISettings;
using MockIScanPipeline = dune::scan::Jobs::Scan::MockIScanPipeline;
using MockStatsHelper = dune::print::JobAccounting::MockStatsHelper;
using TestSystemServices = dune::framework::component::TestingUtil::TestSystemServices;

constexpr double CONVERT_INCH_TO_MM = 25.4;

class TestableCopyJobDetailsProvider : public CopyJobDetailsProvider
{
  public:
    explicit TestableCopyJobDetailsProvider(ICopyJobService*                      jobService,
                                            dune::job::IJobTicketResourceManager* jobTicketResourceManager,
                                            ISettings* interfaceISettings, IScanPipeline* scanPipeline, IDateTime* dateTime)
        : CopyJobDetailsProvider(jobService, jobTicketResourceManager, interfaceISettings, scanPipeline, dateTime){};

    void testableStatsHelper(std::shared_ptr<dune::print::JobAccounting::StatsHelper> helper)
    {
        setStatsHelper(helper);
    }
};

class GivenACopyJobDetailsProvider : public ::testing::Test
{
  public:
    GivenACopyJobDetailsProvider();

  protected:
    void setPageDetailsExpectations(const CopyPageTicket& copyPageTicket);
    void comparePageDetails(const CopyPageTicket& copyPageTicket, const PageDetails& pageDetails);
    void comparePreview(const ImageDescriptorTable& imageDescriptor, const Uuid& pageId, bool highResPreview,
                        bool isLayer, const IPageTicket::Preview& expectedPreview);
    void comparePreviewLink(const links::ItemTable& link, const Uuid& pageId, bool highResPreview, bool isLayer,
                            const std::string& expectedPath);

    TestSystemServices             systemServices_;
    MockICopyJobService            mockICopyJobService_;
    MockIJobTicketResourceManager  mockIJobTicketResourceManager_;
    MockISettings                  mockISettings_;
    MockIScanPipeline              mockIScanPipeline_;
    TestableCopyJobDetailsProvider copyJobDetailsProvider_;

    std::shared_ptr<MockIJobTicket>      mockIJobTicket_;
    std::shared_ptr<MockICopyJobTicket>  mockICopyJobTicket_;
    std::shared_ptr<MockICopyPageTicket> mockICopyPageTicket_;
    std::shared_ptr<MockICopyJobIntent>  mockICopyJobIntent_;
    std::shared_ptr<MockICopyJobResult>  mockICopyJobResult_;
    std::shared_ptr<MockStatsHelper>     mockStatsHelper_ = std::make_shared<MockStatsHelper>();
    Uuid jobUuid_;
    std::shared_ptr<MockIAccessControl>  mockIAccessControl_;   
    std::shared_ptr<MockIAuthAgent>      mockIAuthAgentAdmin_;
};

GivenACopyJobDetailsProvider::GivenACopyJobDetailsProvider()
    : mockICopyJobService_{},
      mockIJobTicketResourceManager_{},
      mockISettings_{},
      mockIScanPipeline_{},
      copyJobDetailsProvider_{&mockICopyJobService_, &mockIJobTicketResourceManager_, &mockISettings_,
                              &mockIScanPipeline_, systemServices_.dateTime_},
      mockIJobTicket_{std::make_shared<MockIJobTicket>()},
      mockICopyJobTicket_{std::make_shared<MockICopyJobTicket>()},
      mockICopyPageTicket_{std::make_shared<MockICopyPageTicket>()},
      mockICopyJobIntent_{std::make_shared<MockICopyJobIntent>()},
      mockICopyJobResult_{std::make_shared<MockICopyJobResult>()},
      jobUuid_{Uuid::createUuid()},
      mockIAccessControl_{std::make_shared<MockIAccessControl>()},
      mockIAuthAgentAdmin_{std::make_shared<MockIAuthAgent>()}
{
    copyJobDetailsProvider_.testableStatsHelper(mockStatsHelper_);
}

void GivenACopyJobDetailsProvider::setPageDetailsExpectations(const CopyPageTicket& copyPageTicket)
{
    // Get page details from ticket
    EXPECT_CALL(*mockICopyPageTicket_, getPageId()).WillOnce(Return(copyPageTicket.getPageId())).RetiresOnSaturation();
    EXPECT_CALL(*mockICopyPageTicket_, getMediaSize())
        .WillOnce(Return(copyPageTicket.getMediaSize()))
        .RetiresOnSaturation();
    EXPECT_CALL(*mockICopyPageTicket_, getPreviewProgress())
        .WillOnce(Return(copyPageTicket.getPreviewProgress()))
        .RetiresOnSaturation();
    EXPECT_CALL(*mockICopyPageTicket_, getHighResPreview())
        .WillOnce(Return(copyPageTicket.getHighResPreview()))
        .RetiresOnSaturation();
    EXPECT_CALL(*mockICopyPageTicket_, getLowResPreview())
        .WillOnce(Return(copyPageTicket.getLowResPreview()))
        .RetiresOnSaturation();

    EXPECT_CALL(*mockICopyPageTicket_, getPageResult())
        .WillOnce(Return(copyPageTicket.getPageResult()))
        .RetiresOnSaturation();
    EXPECT_CALL(*mockICopyPageTicket_, getPageIntent())
        .WillOnce(Return(copyPageTicket.getPageIntent()))
        .RetiresOnSaturation();
}

void GivenACopyJobDetailsProvider::comparePageDetails(const CopyPageTicket& copyPageTicket,
                                                      const PageDetails&    pageDetails)
{
    Uuid pageId{copyPageTicket.getPageId()};

    EXPECT_TRUE(pageDetails.version.isSet());
    EXPECT_EQ(dune::cdm::jobManagement_1::VERSION, pageDetails.version.get());

    EXPECT_TRUE(pageDetails.pageId.isSet());
    EXPECT_EQ(copyPageTicket.getPageId(), pageDetails.pageId.get());

    EXPECT_TRUE(pageDetails.pageNumber.isSet());
    EXPECT_EQ(copyPageTicket.getPageNumber(), pageDetails.pageNumber.get());

    EXPECT_TRUE(pageDetails.outputSize.isSet());
    EXPECT_TRUE(pageDetails.outputSize.get()->mediaSize.isSet());
    EXPECT_EQ(copyPageTicket.getMediaSize(), mapFromCdm(pageDetails.outputSize.get()->mediaSize.get()));

    EXPECT_TRUE(pageDetails.previewProgress.isSet());
    EXPECT_EQ(copyPageTicket.getPreviewProgress(), pageDetails.previewProgress.get());

    EXPECT_TRUE(pageDetails.highResImage.isSet());
    comparePreview(*pageDetails.highResImage.get(), pageId, true, false, copyPageTicket.getHighResPreview());

    EXPECT_TRUE(pageDetails.lowResImage.isSet());
    comparePreview(*pageDetails.lowResImage.get(), pageId, false, false, copyPageTicket.getLowResPreview());
    auto pageResult = copyPageTicket.getPageResult();
    EXPECT_NE(nullptr, pageResult);
    auto pageIntent = copyPageTicket.getPageIntent();
    EXPECT_NE(nullptr, pageIntent);

    EXPECT_TRUE(pageDetails.originalSize.isSet());

    uint32_t resolution = pageIntent->getPrintPageIntent()->getResolution();
    double   unitConversionMmPerPixel = resolution == 0 ? 0 : CONVERT_INCH_TO_MM / resolution;

    int32_t scannedWidth = static_cast<int32_t>(std::lround(pageResult->getScanPageResult()->getScannedWidth() * unitConversionMmPerPixel));
    int32_t scannedHeight = static_cast<int32_t>(std::lround(pageResult->getScanPageResult()->getScannedHeight() * unitConversionMmPerPixel));
    EXPECT_EQ(scannedWidth, pageDetails.originalSize.get()->width);
    EXPECT_EQ(scannedHeight, pageDetails.originalSize.get()->length);
    
    int32_t topMargin =
        static_cast<int32_t>(std::lround(pageIntent->getPrintPageIntent()->getMargins().getTop().getOriginalValue() * unitConversionMmPerPixel));
    int32_t bottomMargin =
        static_cast<int32_t>(std::lround(pageIntent->getPrintPageIntent()->getMargins().getBottom().getOriginalValue() * unitConversionMmPerPixel));
    int32_t leftMargin =
        static_cast<int32_t>(std::lround(pageIntent->getPrintPageIntent()->getMargins().getLeft().getOriginalValue() * unitConversionMmPerPixel));
    int32_t rightMargin =
        static_cast<int32_t>(std::lround(pageIntent->getPrintPageIntent()->getMargins().getRight().getOriginalValue() * unitConversionMmPerPixel));

    EXPECT_EQ(topMargin, pageDetails.pageMargins.get()->topMargin);
    EXPECT_EQ(bottomMargin, pageDetails.pageMargins.get()->bottomMargin);
    EXPECT_EQ(leftMargin, pageDetails.pageMargins.get()->leftMargin);
    EXPECT_EQ(rightMargin, pageDetails.pageMargins.get()->rightMargin);
}

void GivenACopyJobDetailsProvider::comparePreview(const ImageDescriptorTable& imageDescriptor, const Uuid& pageId,
                                                  bool highResPreview, bool isLayer,
                                                  const IPageTicket::Preview& expectedPreview)
{
    EXPECT_EQ(expectedPreview.widthPx, imageDescriptor.width);
    EXPECT_EQ(expectedPreview.heightPx, imageDescriptor.height);
    EXPECT_TRUE(imageDescriptor.links.isSet());
    EXPECT_EQ(1, imageDescriptor.links.get().size());
    comparePreviewLink(imageDescriptor.links.get().front(), pageId, highResPreview, isLayer, expectedPreview.path);
}

void GivenACopyJobDetailsProvider::comparePreviewLink(const links::ItemTable& link, const Uuid& pageId,
                                                      bool highResPreview, bool isLayer,
                                                      const std::string& expectedPath)
{
    EXPECT_EQ(expectedPath, link.href.get());
    EXPECT_TRUE(link.hrefTemplate.get().find(jobUuid_.toString(false)) != std::string::npos);
    EXPECT_TRUE(link.hrefTemplate.get().find(pageId.toString(false)) != std::string::npos);

    if (highResPreview)
    {
        EXPECT_TRUE(link.rel.get().find("High") != std::string::npos);
        EXPECT_TRUE(link.hrefTemplate.get().find("High") != std::string::npos);
        EXPECT_TRUE(link.rel.get().find("Low") == std::string::npos);
        EXPECT_TRUE(link.hrefTemplate.get().find("Low") == std::string::npos);
    }
    else
    {
        EXPECT_TRUE(link.rel.get().find("High") == std::string::npos);
        EXPECT_TRUE(link.hrefTemplate.get().find("High") == std::string::npos);
        EXPECT_TRUE(link.rel.get().find("Low") != std::string::npos);
        EXPECT_TRUE(link.hrefTemplate.get().find("Low") != std::string::npos);
    }
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingJobDetailsAndFailsLoadingCopyTicketeIntoCache_ThenDetailsAreNotSet)
{
    // Fail loading copy job ticket into cache
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _)).WillOnce(Return(nullptr));

    // // Fail populating details
    std::pair<bool, StatsInfoDetails> jobDetails(copyJobDetailsProvider_.populateJobDetails(jobUuid_, &(*mockIAccessControl_)));
    auto jobDetail = jobDetails.second;
    EXPECT_EQ(jobDetails.first, false);
    EXPECT_FALSE(jobDetail.scanInfo.isSet());
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingJobDetailsAndFailsGettingCopyTicket_ThenDetailsAreNotSet)
{
    // Fail getting copy job ticket from cache
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _))
        .WillOnce(Return(mockIJobTicket_));
    EXPECT_CALL(mockICopyJobService_, getTicketFromCache(jobUuid_)).WillOnce(Return(nullptr));

    // // Fail populating details
    std::pair<bool, StatsInfoDetails> jobDetails(copyJobDetailsProvider_.populateJobDetails(jobUuid_, &(*mockIAccessControl_)));
    auto jobDetail = jobDetails.second;
    EXPECT_EQ(jobDetails.first, false);
    EXPECT_FALSE(jobDetail.scanInfo.isSet());
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingJobDetails_ThenDetailsArePopulated)
{
    bool                                  expectedInQuietMode = false;
    dune::imaging::types::Plex            expectedOutputPlexMode = dune::imaging::types::Plex::DUPLEX;
    dune::imaging::types::PrintQuality    expectedCopyQuality = dune::imaging::types::PrintQuality::BEST;
    dune::imaging::types::MediaIdType     expectedOutputMediaIdType = dune::imaging::types::MediaIdType::STATIONERY;
    dune::imaging::types::MediaSource     expectedOutputMediaSource = dune::imaging::types::MediaSource::TRAY1;
    dune::imaging::types::MediaSizeId     expectedOutputMediaSize = dune::imaging::types::MediaSizeId::LETTER;
    dune::imaging::types::ColorMode       expectedColorMode = dune::imaging::types::ColorMode::COLOR;
    dune::imaging::types::PrintingOrder   expectedPrintingOrder = dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP;
    int                                   expectedRotation = 180;
    dune::imaging::types::MediaFamily     expectedMediaFamily = dune::imaging::types::MediaFamily::CANVAS;
    bool                                  expectedAutoRotate = false;
    int                                   expectedCopies = 2;
    int                                   expectedImpressionCount = 6;
    int                                   expectedProgress = 50;
    dune::copy::SheetCollate              expectedCollateValue = dune::copy::SheetCollate::Collate;
    dune::imaging::types::ScanCalibrationType   expectedScanCalibrationType = dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION;


    dune::job::JobType             expectedJobType = dune::job::JobType::COPY;
    std::time_t                    expectedStartTime = std::time_t(24000);
    dune::job::DataSource          expectedDataSource = dune::job::DataSource::NETWORKIO;
    std::string                    expectedJobName = "jobName";
    dune::job::JobStateType        expectedJobStateType = dune::job::JobStateType::COMPLETED;
    dune::job::CompletionStateType expectedCompletionStateType = dune::job::CompletionStateType::SUCCESS;
    std::time_t                    expectedCompletionTime = std::time_t(44000);
    std::string                    expectedUserName = "userName";
    dune::imaging::types::Resolution expectedOutputXResolution = dune::imaging::types::Resolution::E200DPI;
    dune::imaging::types::MediaDestinationId expectedOutputDestination = dune::imaging::types::MediaDestinationId::STANDARDBIN;
    std::string                    expectedApplicationName = "CopyApp";

    // Permissions
    dune::security::ac::SecurityContextBuilder scb;
    dune::security::ac::UserIdentity userIdentity;
    userIdentity.fullyQualifiedUserName = "fullyQualifiedUserName";
    userIdentity.authAgentId = "06458e72-d3f1-4582-a90a-70f63ee7d0cb";
    userIdentity.authenticationType = dune::security::ac::AuthType::AUTH_TYPE_LDAP;
    scb.setIdentity(userIdentity);
    scb.setAttribute(dune::security::ac::UserAttributeNames::SIMPLE_NAME(), "simpleName");
    scb.setAttribute(dune::security::ac::UserAttributeNames::DISPLAY_NAME(), "displayName");
    scb.setAttribute(dune::security::ac::UserAttributeNames::HOME_DIRECTORY(), "homeDirectory");
    scb.setAttribute(dune::security::ac::UserAttributeNames::EMAIL_ADDRESS(), "email");
    scb.setAttribute(dune::security::ac::UserAttributeNames::EXCHANGE_MAILBOX_URI(), "exchangeMailBoxUri");
    std::shared_ptr<dune::security::ac::ISecurityContext> securityContext = std::move(scb.build());

    ON_CALL(*mockIAccessControl_, findAgent(userIdentity.authAgentId)).WillByDefault(Return(&(*mockIAuthAgentAdmin_)));
    EXPECT_CALL(*mockICopyJobTicket_, getSecurityContext()).WillRepeatedly(Return(securityContext));

    // Get Print Job Ticket
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _))
        .WillOnce(Return(mockIJobTicket_));
    EXPECT_CALL(mockICopyJobService_, getTicketFromCache(jobUuid_)).WillOnce(Return(mockICopyJobTicket_));

    // Setting job info
    EXPECT_CALL(*mockICopyJobTicket_, getType()).WillRepeatedly(Return(expectedJobType));
    EXPECT_CALL(*mockICopyJobTicket_, getJobId()).WillRepeatedly(Return(jobUuid_));
    EXPECT_CALL(*mockICopyJobTicket_, getStartTime()).WillRepeatedly(Return(expectedStartTime));
    EXPECT_CALL(*mockICopyJobTicket_, getDataSource()).WillRepeatedly(Return(expectedDataSource));
    EXPECT_CALL(*mockICopyJobTicket_, getJobName()).WillRepeatedly(ReturnRef(expectedJobName));
    EXPECT_CALL(*mockICopyJobTicket_, getState()).WillRepeatedly(Return(expectedJobStateType));
    EXPECT_CALL(*mockICopyJobTicket_, getCompletionState()).WillRepeatedly(Return(expectedCompletionStateType));
    EXPECT_CALL(*mockICopyJobTicket_, getCompletionTime()).WillRepeatedly(Return(expectedCompletionTime));
    EXPECT_CALL(*mockICopyJobTicket_, getUserName()).WillRepeatedly(Return(expectedUserName));
    EXPECT_CALL(*mockICopyJobTicket_, getApplicationName()).WillRepeatedly(ReturnRef(expectedApplicationName));

    // Setting print info
    EXPECT_CALL(*mockICopyJobTicket_, getJobId()).WillRepeatedly(Return(jobUuid_));
    EXPECT_CALL(*mockICopyJobTicket_, getIntent()).WillRepeatedly(Return(mockICopyJobIntent_));
    EXPECT_CALL(*mockICopyJobTicket_, getResult()).WillOnce(Return(mockICopyJobResult_));
    EXPECT_CALL(*mockStatsHelper_, getQuietMode(_)).WillOnce(Return(expectedInQuietMode));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaIdType()).WillRepeatedly(Return(expectedOutputMediaIdType));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSource()).WillRepeatedly(Return(expectedOutputMediaSource));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillRepeatedly(Return(expectedOutputMediaSize));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputPlexMode()).WillRepeatedly(Return(expectedOutputPlexMode));
    EXPECT_CALL(*mockICopyJobIntent_, getColorMode()).WillRepeatedly(Return(expectedColorMode));
    EXPECT_CALL(*mockICopyJobIntent_, getCopyQuality()).WillRepeatedly(Return(expectedCopyQuality));
    EXPECT_CALL(*mockICopyJobIntent_, getCopies()).WillRepeatedly(Return(expectedCopies));
    EXPECT_CALL(*mockICopyJobIntent_, getRequestedPages()).WillRepeatedly(Return(expectedImpressionCount));
    EXPECT_CALL(*mockICopyJobIntent_, getPrintingOrder()).WillRepeatedly(Return(expectedPrintingOrder));
    EXPECT_CALL(*mockICopyJobIntent_, getCollate()).WillOnce(Return(expectedCollateValue));
    EXPECT_CALL(*mockICopyJobIntent_, getRotation()).WillRepeatedly(Return(expectedRotation));
    EXPECT_CALL(*mockICopyJobIntent_, getMediaFamily()).WillRepeatedly(Return(expectedMediaFamily));
    EXPECT_CALL(*mockICopyJobIntent_, getAutoRotate()).WillRepeatedly(Return(expectedAutoRotate));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputXResolution()).WillOnce(Return(expectedOutputXResolution));
    EXPECT_CALL(*mockICopyJobIntent_, getScanCalibrationType()).WillRepeatedly(Return(expectedScanCalibrationType));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputDestination()).WillOnce(Return(expectedOutputDestination));
    EXPECT_CALL(*mockICopyJobIntent_, getScanNumberPages()).WillRepeatedly(Return(10));

    EXPECT_CALL(*mockICopyJobResult_, getCompletedImpressions()).WillOnce(Return(expectedImpressionCount));
    EXPECT_CALL(*mockICopyJobResult_, getCompletedCopies()).WillOnce(Return(expectedCopies));
    EXPECT_CALL(*mockICopyJobResult_, getProgress()).WillOnce(Return(expectedProgress));

    // Setting scan info
    std::shared_ptr<dune::job::StatsDetails::ScanInfoDetails> scanInfoDetails = std::make_shared<dune::job::StatsDetails::ScanInfoDetails>();
    scanInfoDetails->scannedPageCount = 10;
    EXPECT_CALL(mockIScanPipeline_, populateScanInfo(_,_)).WillOnce(Return(scanInfoDetails));

    // Populate job details
    std::pair<bool, StatsInfoDetails> jobDetails(copyJobDetailsProvider_.populateJobDetails(jobUuid_, &(*mockIAccessControl_)));
    auto jobDetail = jobDetails.second;
    EXPECT_EQ(jobDetails.first, true);
    EXPECT_TRUE(jobDetail.scanInfo.isSet());
    EXPECT_TRUE(jobDetail.printInfo.isSet());
    EXPECT_TRUE(jobDetail.jobInfo.isSet());
    EXPECT_TRUE(jobDetail.userInfo.isSet());

    // Compare Print Info
    PrintInfoDetails printInfo{*jobDetail.printInfo.get()};
    EXPECT_TRUE(printInfo.printSettings.isSet());
    PrintSettingsDetails printSettings{*printInfo.printSettings.get()};

    EXPECT_EQ(expectedInQuietMode, printSettings.inQuietMode.get());
    EXPECT_EQ(expectedOutputPlexMode, printSettings.plexMode.get());
    EXPECT_EQ(expectedColorMode, printSettings.colorMode.get());
    EXPECT_EQ(expectedCopyQuality, printSettings.printQuality.get());
    EXPECT_EQ(expectedCopies, printSettings.requestedCopiesCount.get());
    EXPECT_EQ(expectedImpressionCount, printSettings.requestedImpressionCount.get());
    EXPECT_EQ(expectedOutputXResolution, printSettings.printResolution.get());
    EXPECT_EQ(dune::job::StatsDetails::SheetCollate::COLLATE, printSettings.collate.get());
    EXPECT_EQ(expectedOutputDestination, printSettings.mediaOutputId.get());
    EXPECT_EQ(10, jobDetail.scanInfo.get()->scannedPageCount.get());

    // Compare Media Requested
    EXPECT_TRUE(printSettings.mediaRequested.isSet());
    MediaRequestedDetails mediaRequested{*printSettings.mediaRequested.get()};
    EXPECT_EQ("", mediaRequested.mediaId.get());


    // Compare Media Input
    EXPECT_TRUE(printSettings.mediaRequested.get()->mediaInput.isSet());
    MediaInputDetails mediaInput{*printSettings.mediaRequested.get()->mediaInput.get()};
    EXPECT_EQ(dune::imaging::types::MediaSource::TRAY1, mediaInput.mediaSourceId.get());
    EXPECT_EQ(expectedOutputMediaSize, mediaInput.currentMediaSize.get());
    EXPECT_EQ(expectedOutputMediaIdType, mediaInput.currentMediaType.get());

    // Compare Job Info
    std::vector<dune::job::StatsDetails::JobDestinationType> expectedJobDestinationTypes =
        std::vector<dune::job::StatsDetails::JobDestinationType>{dune::job::StatsDetails::JobDestinationType::PRINT_ENGINE};
    EXPECT_TRUE(jobDetail.jobInfo.isSet());
    JobInfoDetails jobInfo{*jobDetail.jobInfo.get()};
    EXPECT_EQ(dune::job::StatsDetails::StatsJobType::COPY, jobInfo.jobType.get());
    EXPECT_EQ(jobUuid_.toString(false), jobInfo.jobUuid.get());
    EXPECT_EQ(systemServices_.dateTime_->getTimeInZuluFormat(expectedStartTime), jobInfo.creationTime.get());
    EXPECT_EQ(systemServices_.dateTime_->getTimeInZuluFormat(expectedStartTime), jobInfo.startTime.get());
    EXPECT_EQ(dune::job::DataSource::NETWORKIO, jobInfo.jobDataSource.get());
    EXPECT_EQ(expectedJobName, jobInfo.jobName.get());
    EXPECT_EQ(expectedJobDestinationTypes, jobInfo.jobDestinations.get());
    EXPECT_EQ(dune::job::CompletionStateType::SUCCESS, jobInfo.jobCompletionState.get());
    EXPECT_EQ(systemServices_.dateTime_->getTimeInZuluFormat(expectedCompletionTime), jobInfo.endTime.get());
    EXPECT_EQ(dune::job::JobStateType::COMPLETED, jobInfo.state.get());
    EXPECT_EQ(expectedUserName, jobInfo.userName.get());
    EXPECT_EQ(jobInfo.applicationName.get(), expectedApplicationName);

    // Compare User Info
    dune::security::ac::UserIdentity userIdentityDetails = jobDetail.userInfo.get()->userIdentity.get();
    EXPECT_EQ(userIdentityDetails.fullyQualifiedUserName, userIdentity.fullyQualifiedUserName);
    EXPECT_EQ(userIdentityDetails.authAgentId, userIdentity.authAgentId);
    EXPECT_EQ(userIdentityDetails.authenticationType, userIdentity.authenticationType);
   
    std::string expectedAgentName = mockIAuthAgentAdmin_->getAgentInfo().agentName;
    EXPECT_EQ(jobDetail.userInfo.get()->authenticationAgentName.get(), expectedAgentName);
    
    dune::security::ac::UserAttributeMap userAttributes = jobDetail.userInfo.get()->userAttributes.get();
    EXPECT_EQ(userAttributes.size(), 5);
    EXPECT_EQ(userAttributes[dune::security::ac::UserAttributeNames::SIMPLE_NAME()], "simpleName");
    EXPECT_EQ(userAttributes[dune::security::ac::UserAttributeNames::DISPLAY_NAME()], "displayName");
    EXPECT_EQ(userAttributes[dune::security::ac::UserAttributeNames::HOME_DIRECTORY()], "homeDirectory");
    EXPECT_EQ(userAttributes[dune::security::ac::UserAttributeNames::EMAIL_ADDRESS()], "email");
    EXPECT_EQ(userAttributes[dune::security::ac::UserAttributeNames::EXCHANGE_MAILBOX_URI()], "exchangeMailBoxUri");
}

TEST_F(GivenACopyJobDetailsProvider, WhenSomePopulatingJobDetailsAreUndefined_ThenDetailsArePopulated)
{
    dune::imaging::types::MediaIdType     expectedOutputMediaIdType = dune::imaging::types::MediaIdType::UNDEFINED;
    dune::imaging::types::MediaSource     expectedOutputMediaSource = dune::imaging::types::MediaSource::UNDEFINED;
    dune::imaging::types::MediaSizeId     expectedOutputMediaSize = dune::imaging::types::MediaSizeId::UNDEFINED;
    std::string                           expectedJobName = "jobName";
    std::string                           expectedApplicationName = "CopyApp";

    // Get Print Job Ticket
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _))
        .WillOnce(Return(mockIJobTicket_));
    EXPECT_CALL(mockICopyJobService_, getTicketFromCache(jobUuid_)).WillOnce(Return(mockICopyJobTicket_));

    // Setting job info
    EXPECT_CALL(*mockICopyJobTicket_, getJobId()).WillRepeatedly(Return(jobUuid_));
    EXPECT_CALL(*mockICopyJobTicket_, getJobName()).WillRepeatedly(ReturnRef(expectedJobName));
    EXPECT_CALL(*mockICopyJobTicket_, getApplicationName()).WillRepeatedly(ReturnRef(expectedApplicationName));

    // Setting print info
    EXPECT_CALL(*mockICopyJobTicket_, getJobId()).WillRepeatedly(Return(jobUuid_));
    EXPECT_CALL(*mockICopyJobTicket_, getIntent()).WillRepeatedly(Return(mockICopyJobIntent_));
    EXPECT_CALL(*mockICopyJobTicket_, getResult()).WillOnce(Return(mockICopyJobResult_));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaIdType()).WillRepeatedly(Return(expectedOutputMediaIdType));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSource()).WillRepeatedly(Return(expectedOutputMediaSource));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillRepeatedly(Return(expectedOutputMediaSize));
    EXPECT_CALL(*mockICopyJobIntent_, getScanNumberPages()).WillRepeatedly(Return(10));

    // Setting scan info
    std::shared_ptr<dune::job::StatsDetails::ScanInfoDetails> scanInfoDetails = std::make_shared<dune::job::StatsDetails::ScanInfoDetails>();
    scanInfoDetails->scannedPageCount = 12;
    EXPECT_CALL(mockIScanPipeline_, populateScanInfo(_,_)).WillOnce(Return(scanInfoDetails));

    // Populate job details
    std::pair<bool, StatsInfoDetails> jobDetails(copyJobDetailsProvider_.populateJobDetails(jobUuid_, &(*mockIAccessControl_)));
    auto jobDetail = jobDetails.second;
    EXPECT_EQ(jobDetails.first, true);
    EXPECT_TRUE(jobDetail.scanInfo.isSet());
    EXPECT_TRUE(jobDetail.printInfo.isSet());
    EXPECT_TRUE(jobDetail.jobInfo.isSet());
    EXPECT_TRUE(jobDetail.userInfo.isSet());

    // Compare Print Info
    PrintInfoDetails printInfo{*jobDetail.printInfo.get()};
    EXPECT_TRUE(printInfo.printSettings.isSet());
    PrintSettingsDetails printSettings{*printInfo.printSettings.get()};
    EXPECT_EQ(10, jobDetail.scanInfo.get()->scannedPageCount.get());

    // Compare Media Requested
    EXPECT_TRUE(printSettings.mediaRequested.isSet());
    MediaRequestedDetails mediaRequested{*printSettings.mediaRequested.get()};
    EXPECT_EQ("", mediaRequested.mediaId.get());

    // Compare Media Input
    EXPECT_TRUE(printSettings.mediaRequested.get()->mediaInput.isSet());
    MediaInputDetails mediaInput{*printSettings.mediaRequested.get()->mediaInput.get()};
    EXPECT_EQ(dune::imaging::types::MediaSource::AUTOSELECT, mediaInput.mediaSourceId.get());
    EXPECT_EQ(dune::imaging::types::MediaSizeId::ANY, mediaInput.currentMediaSize.get());
    EXPECT_EQ(dune::imaging::types::MediaIdType::CUSTOM, mediaInput.currentMediaType.get());
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingPagesDetailsAndFailsLoadingCopyTicketeIntoCache_ThenDetailsAreNotSet)
{
    // Fail loading copy job ticket into cache
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _)).WillOnce(Return(nullptr));

    // Fail populating details
    PagesDetails pagesDetails{copyJobDetailsProvider_.populatePagesDetails(jobUuid_)};
    EXPECT_TRUE(pagesDetails.pages.get().empty());
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingPagesDetailsAndFailsGettingCopyTicket_ThenDetailsAreNotSet)
{
    // Fail getting copy job ticket from cache
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _))
        .WillOnce(Return(mockIJobTicket_));
    EXPECT_CALL(mockICopyJobService_, getTicketFromCache(jobUuid_)).WillOnce(Return(nullptr));

    // Fail populating details
    PagesDetails pagesDetails{copyJobDetailsProvider_.populatePagesDetails(jobUuid_)};
    EXPECT_TRUE(pagesDetails.pages.get().empty());
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingPagesDetails_ThenDetailsArePopulated)
{
    // Populate Pages Details
    std::shared_ptr<CopyPageTicket> firstCopyPageTicket = CopyTicketsUtilities::createDefaultPageTicket();
    std::shared_ptr<CopyPageTicket> secondCopyPageTicket = CopyTicketsUtilities::createDefaultPageTicket();
    secondCopyPageTicket->setPageId(Uuid::createUuid());

    // Get copy Page Ticket
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _))
        .WillOnce(Return(mockIJobTicket_));
    EXPECT_CALL(mockICopyJobService_, getTicketFromCache(jobUuid_)).WillOnce(Return(mockICopyJobTicket_));

    EXPECT_CALL(*mockICopyJobTicket_, getPagesIds(PageOrder::CREATION))
        .WillOnce(Return(std::vector<Uuid>{firstCopyPageTicket->getPageId(), secondCopyPageTicket->getPageId()}));
    EXPECT_CALL(*mockICopyJobTicket_, getCopyPageTicket(_)).Times(2).WillRepeatedly(Return(mockICopyPageTicket_));
    EXPECT_CALL(*mockICopyJobTicket_, getJobId()).Times(2).WillRepeatedly(Return(jobUuid_));

    // Get Details from ticket
    setPageDetailsExpectations(*secondCopyPageTicket);
    setPageDetailsExpectations(*firstCopyPageTicket);

    // Compare Page details
    PagesDetails pagesDetails{copyJobDetailsProvider_.populatePagesDetails(jobUuid_)};
    EXPECT_TRUE(pagesDetails.version.isSet());
    EXPECT_EQ(dune::cdm::jobManagement_1::VERSION, pagesDetails.version.get());
    EXPECT_EQ(2, pagesDetails.pages.get().size());
    comparePageDetails(*firstCopyPageTicket, pagesDetails.pages.get()[0]);
    comparePageDetails(*secondCopyPageTicket, pagesDetails.pages.get()[1]);
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingPagesDetailsWithDifferentOriginalSizes_ThenSeveralOriginalSizeIsTrue)
{
    // Every ticket has different dimensions to set SeveralOriginalSizes to True
    uint32_t expectedScannedWidthA = 50;
    uint32_t expectedScannedHeightA = 50;
    uint32_t expectedScannedWidthB = 100;
    uint32_t expectedScannedHeightB = 100;

    // Populate Pages Details
    std::shared_ptr<CopyPageTicket> firstCopyPageTicket = CopyTicketsUtilities::createDefaultPageTicket();
    std::shared_ptr<CopyPageTicket> secondCopyPageTicket = CopyTicketsUtilities::createDefaultPageTicket();

    firstCopyPageTicket->getPageIntent()->getPrintPageIntent()->setResolution(200);
    secondCopyPageTicket->getPageIntent()->getPrintPageIntent()->setResolution(200);
    firstCopyPageTicket->getPageResult()->getScanPageResult()->setScannedWidth(expectedScannedWidthA);
    firstCopyPageTicket->getPageResult()->getScanPageResult()->setScannedHeight(expectedScannedHeightA);
    secondCopyPageTicket->getPageResult()->getScanPageResult()->setScannedWidth(expectedScannedWidthB);
    secondCopyPageTicket->getPageResult()->getScanPageResult()->setScannedHeight(expectedScannedHeightB);

    // Get Print Page Ticket
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _))
        .WillOnce(Return(mockIJobTicket_));
    EXPECT_CALL(mockICopyJobService_, getTicketFromCache(jobUuid_)).WillOnce(Return(mockICopyJobTicket_));

    EXPECT_CALL(*mockICopyJobTicket_, getJobId()).Times(2).WillRepeatedly(Return(jobUuid_));
    EXPECT_CALL(*mockICopyJobTicket_, getPagesIds(PageOrder::CREATION))
        .WillOnce(Return(std::vector<Uuid>{firstCopyPageTicket->getPageId(), secondCopyPageTicket->getPageId()}));

    EXPECT_CALL(*mockICopyJobTicket_, getCopyPageTicket(_)).WillOnce(Return(firstCopyPageTicket))
                                                           .WillOnce(Return(secondCopyPageTicket));

    // Compare Page details
    PagesDetails pagesDetails{copyJobDetailsProvider_.populatePagesDetails(jobUuid_)};
    EXPECT_TRUE(mapFromCdm(pagesDetails.severalOriginalSizes.get()));
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingPageDetailsAndFailsLoadingCopyTicketeIntoCache_ThenDetailsAreNotSet)
{
    // Page Ticket Uuid
    Uuid pageUuid{Uuid::createUuid()};

    // Fail loading copy job ticket into cache
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _)).WillOnce(Return(nullptr));

    // Fail populating details
    PageDetails pageDetails{copyJobDetailsProvider_.populatePageDetails(jobUuid_, pageUuid)};
    EXPECT_TRUE(pageDetails.outputSize.isSet());
    EXPECT_FALSE(pageDetails.outputSize.get()->mediaSize.isSet());
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingPageDetailsAndFailsGettingCopyTicket_ThenDetailsAreNotSet)
{
    // Page Ticket Uuid
    Uuid pageUuid{Uuid::createUuid()};

    // Fail getting copy job ticket from cache
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _))
        .WillOnce(Return(mockIJobTicket_));
    EXPECT_CALL(mockICopyJobService_, getTicketFromCache(jobUuid_)).WillOnce(Return(nullptr));

    // Fail populating details
    PageDetails pageDetails{copyJobDetailsProvider_.populatePageDetails(jobUuid_, pageUuid)};
    EXPECT_TRUE(pageDetails.outputSize.isSet());
    EXPECT_FALSE(pageDetails.outputSize.get()->mediaSize.isSet());
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingPageDetailsAndPageTicketIsNull_ThenDetailsAreNotSet)
{
    // Page Ticket Uuid
    Uuid pageUuid{Uuid::createUuid()};

    // Get JobTicket handler
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _))
        .WillOnce(Return(mockIJobTicket_));
    EXPECT_CALL(mockICopyJobService_, getTicketFromCache(jobUuid_)).WillOnce(Return(mockICopyJobTicket_));

    // Ticket is set with media settings values
    EXPECT_CALL(*mockICopyJobTicket_, getCopyPageTicket(_)).Times(1).WillRepeatedly(Return(nullptr));

    // Fail populating details
    PageDetails pageDetails{copyJobDetailsProvider_.populatePageDetails(jobUuid_, pageUuid)};
    EXPECT_TRUE(pageDetails.outputSize.isSet());
    EXPECT_FALSE(pageDetails.outputSize.get()->mediaSize.isSet());
}

TEST_F(GivenACopyJobDetailsProvider, WhenPopulatingPageDetails_ThenDetailsArePopulated)
{
    // Populate Page details
    std::shared_ptr<CopyPageTicket> copyPageTicket = CopyTicketsUtilities::createDefaultPageTicket();

    copyPageTicket->getPageResult()->getScanPageResult()->setScannedWidth(50);
    copyPageTicket->getPageResult()->getScanPageResult()->setScannedHeight(50);

    // Get copy Page Ticket
    EXPECT_CALL(mockIJobTicketResourceManager_, loadJobTicketIntoCacheIfNeeded(jobUuid_, _))
        .WillOnce(Return(mockIJobTicket_));
    EXPECT_CALL(mockICopyJobService_, getTicketFromCache(jobUuid_)).WillOnce(Return(mockICopyJobTicket_));
    EXPECT_CALL(*mockICopyJobTicket_, getCopyPageTicket(_)).WillOnce(Return(mockICopyPageTicket_));
    EXPECT_CALL(*mockICopyJobTicket_, getJobId()).WillOnce(Return(jobUuid_));

    // Get Details from ticket
    setPageDetailsExpectations(*copyPageTicket);

    // Compare Page details
    PageDetails pageDetails{copyJobDetailsProvider_.populatePageDetails(jobUuid_, copyPageTicket->getPageId())};
    comparePageDetails(*copyPageTicket, pageDetails);
}
