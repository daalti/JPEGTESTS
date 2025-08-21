////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobPromptControllerGtest.cpp
 * @brief  CopyJobPromptControllerGtest unit tests
 *
 * (C) Sampleright 2021 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "CopyJobPromptControllerGtest_TraceAutogen.h"

#include "CopyJobPromptController.h"
#include "CopyJobTicket.h"
#include "ICopyJobTicket.h"
#include "MockIJobManagerAlertProvider.h"
#include "MockICopyJobTicket.h"
#include "MockIJobTicketHandler.h"
#include "MockIMedia.h"
#include "MockIScannerMedia.h"
#include "ConstraintsGroup.h"
using namespace dune::imaging::types;
using namespace dune::copy::Jobs::Copy;
using namespace dune::job::cdm;
using namespace dune::framework::core;

using ::testing::_;
using ::testing::InvokeWithoutArgs;
using ::testing::Return;
using ::testing::ReturnRef;

using IMediaPath            = dune::scan::scanningsystem::IMediaPath;
using MediaDetectionStatus  = IMediaPath::MediaDetectionStatus;
using MediaPresenceStatus   = dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus;

class GivenCopyJobPromptController : public ::testing::Test
{
  public:
    GivenCopyJobPromptController();

    virtual void SetUp() override;
    virtual void TearDown() override;

    void testFunction(dune::job::PromptType promptType, dune::job::PromptResponseType promptResponseType)
    {

    }

  protected:
    std::shared_ptr<CopyJobTicket>  copyJobTicket_;
    std::shared_ptr<MockIJobManagerAlertProvider>    mockIJobAlertProvider_;

    std::unique_ptr<CopyJobPromptController> copyJobPromptController_;
    //bool multi
};

GivenCopyJobPromptController::GivenCopyJobPromptController()
    : copyJobTicket_{std::make_shared<CopyJobTicket>()},
    mockIJobAlertProvider_{std::make_shared<MockIJobManagerAlertProvider>()}
{
}

void GivenCopyJobPromptController::SetUp()
{
    copyJobTicket_->setFirstScanStarted(true);
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::HOME_PRO, false);
}

void GivenCopyJobPromptController::TearDown()
{

}

TEST_F(GivenCopyJobPromptController, WhenCancelPromptIsCalled_ticketStateIsSetToCancel)
{
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::HOME_PRO, false);
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));

    copyJobPromptController_->getNewPromptToDisplay(true);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::IdCardSecondSide, std::bind(&GivenCopyJobPromptController::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    copyJobPromptController_->cancelPrompt();
    EXPECT_EQ(copyJobTicket_->getCompletionState(), dune::job::CompletionStateType::CANCELED);
}

TEST_F(GivenCopyJobPromptController, WhenCancelPromptIsCalledAfterPromptResponse_ticketStateIsNotSetToCancel)
{
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::HOME_PRO, false);
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobPromptController_->getNewPromptToDisplay(true);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::IdCardSecondSide, std::bind(&GivenCopyJobPromptController::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::scanManualDuplexSecondSide, nullptr);
    copyJobPromptController_->cancelPrompt();
    EXPECT_NE(copyJobTicket_->getCompletionState(), dune::job::CompletionStateType::CANCELED);
}

TEST_F(GivenCopyJobPromptController, WhenSimplexJobIsSentFromHomeproFlatbedNoPromptIsAdded)
{
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::HOME_PRO, false);
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, PromptType::None);
}

TEST_F(GivenCopyJobPromptController, WhenDuplexOutputTwoUpJobIsSentFromHomeproFlatbedDuplexPromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedSecondPage);
}

TEST_F(GivenCopyJobPromptController, WhenDuplexInputTwoUpJobIsSentFromHomeproFlatbedDuplexPromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedSecondPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedSecondPage, std::bind(&GivenCopyJobPromptController::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::scanManualDuplexSecondSide, nullptr);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::FlatbedSecondPage);
}

TEST_F(GivenCopyJobPromptController, WhenNUpJobSentForHomeproThenFlatbedSecondPagePromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedSecondPage);
}
TEST_F(GivenCopyJobPromptController, WhenIdcardwith2pagesPersheetIsSelectedPromptIsShown)
{
    copyJobTicket_->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobTicket_->setFirstScanStarted(true);
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    auto copyJobPromptController_ = std::make_shared<CopyJobPromptController>(copyJobTicket_, nullptr, Product::HOME_PRO, false);
    ASSERT_NE(nullptr, copyJobPromptController_);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardSecondSide);
}
class GivenCopyJobPromptControllerEnterprise : public ::testing::Test
{
  public:
    GivenCopyJobPromptControllerEnterprise();
    virtual void SetUp() override;
    virtual void TearDown() override;

    void testFunction(dune::job::PromptType promptType, dune::job::PromptResponseType promptResponseType)
    {

    }

  protected:
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket>     mockICopyJobTicket_{};
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobIntent>     mockICopyJobIntent_{};
    std::shared_ptr<MockIJobManagerAlertProvider>                   mockIJobAlertProvider_;
    std::unique_ptr<CopyJobPromptController>                        copyJobPromptController_;
    std::shared_ptr<dune::scan::scanningsystem::MockIMedia>         mockIScannerMedia_;
    std::shared_ptr<dune::scan::scanningsystem::MockIMediaPath>     mockIMediaPath_;
    std::shared_ptr<dune::job::MockIJobTicketHandler>               mockIJobTicketHandler_;
    std::shared_ptr<CopyJobTicket>  copyJobTicket_;
};

GivenCopyJobPromptControllerEnterprise::GivenCopyJobPromptControllerEnterprise()
    : mockIJobAlertProvider_{std::make_shared<MockIJobManagerAlertProvider>()},
    copyJobTicket_{std::make_shared<CopyJobTicket>()}
{
}

void GivenCopyJobPromptControllerEnterprise::SetUp()
{
    mockICopyJobTicket_      = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();
    mockICopyJobIntent_      = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    mockIJobAlertProvider_   = std::make_shared<MockIJobManagerAlertProvider>();
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(mockICopyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    mockIScannerMedia_       = std::make_shared<dune::scan::scanningsystem::MockIMedia>();
    mockIMediaPath_          = std::make_shared<dune::scan::scanningsystem::MockIMediaPath>();
    mockIJobTicketHandler_   = std::make_shared<dune::job::MockIJobTicketHandler>();

    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(mockICopyJobIntent_));
    ON_CALL(*mockICopyJobTicket_, getHandler()).WillByDefault(Return(mockIJobTicketHandler_));
    ON_CALL(*mockICopyJobTicket_, getScanMediaInterface()).WillByDefault(Return(mockIScannerMedia_.get()));
    ON_CALL(*mockICopyJobTicket_, getSegmentType()).WillByDefault(Return(dune::job::SegmentType::FinalSegment));
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    ON_CALL(*mockICopyJobIntent_, getScanCaptureMode()).WillByDefault(Return(dune::scan::types::ScanCaptureModeType::STANDARD));

    //Acutal copyJobTicket is used instead of Mock to test the prompts are actually added based on the ticket
    copyJobTicket_->setFirstScanStarted(true);
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
}

void GivenCopyJobPromptControllerEnterprise::TearDown()
{

}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithInputMediaSizeAnyAndOutputMediaSizeAny_DetectedMediaSizeShouldBeSetToOutputMediaSizeCorrectly)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setMatchOriginalOutputMediaSizeId(_)).WillOnce(Return());

    copyJobPromptController_->getNewPromptToDisplay(true);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithInputMediaSizeAnyAndOutputMediaSizeNotAny_DetectedMediaSizeShouldNotBeSetToOutputMediaSize)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);

    copyJobPromptController_->getNewPromptToDisplay(true);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithPromptForMorePagesTrueAndFirstScanStartedIsFalse_NoPromptIsAdded)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);

    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(false));

    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithPromptForMorePagesTrueAndFirstScanStartedIsTrue_NoPromptIsAdded)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);

    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(true));

    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAddPage);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithPromptForMorePagesTrueDuplexAndFirstScanStartedIsTrue_FlatbedSecondPromptIsAdded)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);
    EXPECT_CALL(*mockICopyJobIntent_, getInputPlexMode()).WillRepeatedly(Return(dune::imaging::types::Plex::DUPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(true));
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedDuplexAddPage);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithPromptForMorePagesTrueDuplexAndFirstScanStartedIsTrue_FlatbedAddPageIsAdded)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);
    EXPECT_CALL(*mockICopyJobIntent_, getInputPlexMode()).WillRepeatedly(Return(dune::imaging::types::Plex::DUPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobIntent_, isFlatbedDuplexCompleted()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(true));

    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAddPage);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithIDCardTruePromptForBothSidesEnabledAndEvalPromptCalledTwice_ThenIDCardFirstSideAndSecondSideIsPrompted)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);
    
    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(false));

    EXPECT_CALL(*mockICopyJobIntent_, getScanCaptureMode()).WillRepeatedly(Return(dune::scan::types::ScanCaptureModeType::IDCARD));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobTicket_, getSegmentType()).WillRepeatedly(Return(dune::job::SegmentType::FinalSegment));
    EXPECT_CALL(*mockICopyJobIntent_, getpromptForIdCardBothSide()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobIntent_, getScanSource()).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));
    
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardFirstSide);

    prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardSecondSide);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithIDCardTruePromptForBothSidesDisabledAndEvalPromptCalledTwice_ThenOnlySecondSideIsPrompted)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);
    
    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(false));

    EXPECT_CALL(*mockICopyJobIntent_, getScanCaptureMode()).WillRepeatedly(Return(dune::scan::types::ScanCaptureModeType::IDCARD));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobTicket_, getSegmentType()).WillRepeatedly(Return(dune::job::SegmentType::FinalSegment));
    EXPECT_CALL(*mockICopyJobIntent_, getpromptForIdCardBothSide()).WillRepeatedly(Return(false));
    EXPECT_CALL(*mockICopyJobIntent_, getScanSource()).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));

    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::None);

    prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardSecondSide);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithIDCardTrueAndPromptForBothSidesEnabled_IDCardFirstSideIsAdded)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);

    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(false));
    EXPECT_CALL(*mockICopyJobIntent_, getScanCaptureMode()).WillRepeatedly(Return(dune::scan::types::ScanCaptureModeType::IDCARD));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(false));
    EXPECT_CALL(*mockICopyJobIntent_, getScanSource()).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));
    EXPECT_CALL(*mockICopyJobTicket_, getSegmentType()).WillRepeatedly(Return(dune::job::SegmentType::FinalSegment));
    EXPECT_CALL(*mockICopyJobIntent_, getpromptForIdCardBothSide()).WillRepeatedly(Return(true));
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardFirstSide);
    
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithIDCardTruePromptForBothSidesEnabledAndDulpexPlexModeIsTrue_ThenIDCardFirstSideAndSecondSideIsPrompted)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_DUPLEX));
    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);
    
    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(false));

    EXPECT_CALL(*mockICopyJobIntent_, getScanCaptureMode()).WillRepeatedly(Return(dune::scan::types::ScanCaptureModeType::IDCARD));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobTicket_, getSegmentType()).WillRepeatedly(Return(dune::job::SegmentType::FinalSegment));
    EXPECT_CALL(*mockICopyJobIntent_, getpromptForIdCardBothSide()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobIntent_, getScanSource()).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));
    
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardFirstSide);

    prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardSecondSide);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPreviewCasePromptIsCalledWithIDCardTruePromptForBothSidesEnabledAndEvalPromptCalledTwice_ThenIDCardFirstSideAndSecondSideIsPrompted)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);
    
    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(false));

    EXPECT_CALL(*mockICopyJobIntent_, getScanCaptureMode()).WillRepeatedly(Return(dune::scan::types::ScanCaptureModeType::IDCARD));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobTicket_, getSegmentType()).WillRepeatedly(Return(dune::job::SegmentType::PrepareSegment));
    EXPECT_CALL(*mockICopyJobTicket_, getPreviewMode()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobIntent_, getpromptForIdCardBothSide()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobIntent_, getScanSource()).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));

    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardFirstSide);

    prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardSecondSide);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPreviewCasePromptIsCalledWithIDCardTruePromptForBothSidesDisabledAndEvalPromptCalledTwice_ThenOnlySecondSideIsPrompted)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);
    
    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(false));

    EXPECT_CALL(*mockICopyJobIntent_, getScanCaptureMode()).WillRepeatedly(Return(dune::scan::types::ScanCaptureModeType::IDCARD));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobTicket_, getSegmentType()).WillRepeatedly(Return(dune::job::SegmentType::PrepareSegment));
    EXPECT_CALL(*mockICopyJobTicket_, getPreviewMode()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobIntent_, getpromptForIdCardBothSide()).WillRepeatedly(Return(false));
    EXPECT_CALL(*mockICopyJobIntent_, getScanSource()).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));

    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, PromptType::None);

    prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardSecondSide);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPreviewCasePromptIsCalledWithIDCardTrueAndPromptForBothSidesEnabled_IDCardFirstSideIsAdded)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));

    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A4));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setOutputMediaSizeId(_)).Times(0);

    EXPECT_CALL(*mockICopyJobIntent_, getPromptForMorePages()).WillRepeatedly(Return(false));
    EXPECT_CALL(*mockICopyJobIntent_, getScanCaptureMode()).WillRepeatedly(Return(dune::scan::types::ScanCaptureModeType::IDCARD));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(false));
    EXPECT_CALL(*mockICopyJobIntent_, getScanSource()).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));
    EXPECT_CALL(*mockICopyJobTicket_, getSegmentType()).WillRepeatedly(Return(dune::job::SegmentType::PrepareSegment));
    EXPECT_CALL(*mockICopyJobTicket_, getPreviewMode()).WillRepeatedly(Return(true));
    EXPECT_CALL(*mockICopyJobIntent_, getpromptForIdCardBothSide()).WillRepeatedly(Return(true));
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardFirstSide);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithMediaOrientationLandScape_ScanFeedOrientationSetToLongEdge)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::LANDSCAPE) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    //Setting to ShortEdge for teting purpose so the check fails and we can expect call on the set
    ON_CALL(*mockICopyJobIntent_, getScanFeedOrientation()).WillByDefault(Return(dune::scan::types::ScanFeedOrientation::SHORTEDGE));
    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setMatchOriginalOutputMediaSizeId(_)).WillOnce(Return());
    //If this is called that means the ScanFeedorientation was set to LongEdge by the media Detection Logic
    EXPECT_CALL(*mockICopyJobIntent_,setScanFeedOrientation(_)).WillOnce(Return());
    copyJobPromptController_->getNewPromptToDisplay(true);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPromptIsCalledWithMediaOrientationPotrait_ScanFeedOrientationSetToShortEdge)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::LETTER, MediaOrientation::PORTRAIT) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    //Setting to ShortEdge for teting purpose so the check fails and we can expect call on the set
    ON_CALL(*mockICopyJobIntent_, getScanFeedOrientation()).WillByDefault(Return(dune::scan::types::ScanFeedOrientation::LONGEDGE));
    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, getOutputMediaSizeId()).WillOnce(Return(dune::imaging::types::MediaSizeId::ANY));
    EXPECT_CALL(*mockICopyJobIntent_, setMatchOriginalOutputMediaSizeId(_)).WillOnce(Return());
    //If this is called that means the ScanFeedorientation was set to SHortEdge by the media Detection Logic
    EXPECT_CALL(*mockICopyJobIntent_,setScanFeedOrientation(_)).WillOnce(Return());
    copyJobPromptController_->getNewPromptToDisplay(true);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPreviewJobIsSentFromEnterpriseFlatbedAddPromptIsAddedInPreviewIsRunning)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->setPreviewMode(true);
    copyJobTicket_->setSegmentType(dune::job::SegmentType::PrepareSegment);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAddPage);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenBookPreviewJobIsSentFromEnterprisBookModePromptIsAddedInPreviewIsRunning)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->setPreviewMode(true);
    copyJobTicket_->setSegmentType(dune::job::SegmentType::PrepareSegment);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::BookMode);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenIDcardPreviewJobIsSentFromEnterpriseIDCardPromptIsAddedInPreviewIsRunning)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->setPreviewMode(true);
    copyJobTicket_->setSegmentType(dune::job::SegmentType::PrepareSegment);
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardFirstSide);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenPreviewJobIsSentFromEnterpriseFirstSidePromptIsAddedInPreviewIsnotRunning)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    copyJobTicket_->setPreviewMode(false);
    copyJobTicket_->setSegmentType(dune::job::SegmentType::PrepareSegment);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardFirstSide);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenDuplexJobIsSentFromEnterpriseFlatbedDuplexPromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedDuplexAddPage);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenBookJobIsSentFromEnterpriseAfterEveryScan_BookModePromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobTicket_->setFirstScanStarted(true);
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::BookMode);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenBookJobIsSentFirstScanFalseFromEnterpriseAfterEveryScan_BookModePromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobTicket_->setFirstScanStarted(false);
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::BookMode);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenBookJobIsSentFirstScanTrueFromEnterpriseAfterDone_BookModePromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobTicket_->setFirstScanStarted(false);
    copyJobTicket_->setPreviewMode(false);
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::BookMode);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenBookJobIsSentFirstScanFalseFromEnterpriseAfterEveryScan_BookModePromptIsAddedAndAlertActionHandled)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobTicket_->setFirstScanStarted(false);
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::BookMode);

    copyJobPromptController_->displayPrompt(dune::job::PromptType::BookMode, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
    alertAction->param1 = "RightPageOnly";
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage, alertAction);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenBookJobWithLandscapeIsSentFirstScanFalseFromEnterpriseAfterEveryScan_BookModePromptIsAddedAndAlertActionHandled)
{
    dune::cdm::alert_1::AlertT* tempAlert;
    ON_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _))
    .WillByDefault(
        testing::DoAll(testing::Invoke([&](dune::cdm::alert_1::AlertT* alert, AlertActionCallback callback, uint32_t timeoutSeconds) {
                    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction =
                        std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
                    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
                    std::cout << "PromptResponseType::Add" << std::endl;
                    tempAlert = alert;
                    EXPECT_EQ(tempAlert->data[1]->value->sValue, "TopOnly");
                    callback(alert->category, alertAction);
                }),
                Return(true)));
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobTicket_->setFirstScanStarted(false);
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobTicket_->getIntent()->setContentOrientation(dune::imaging::types::ContentOrientation::LANDSCAPE);
    copyJobTicket_->getIntent()->setBookMode(dune::scan::types::BookModeEnum::RightPageOnly);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::BookMode);

    copyJobPromptController_->displayPrompt(dune::job::PromptType::BookMode, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
    alertAction->param1 = "TopOnly";
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage, alertAction);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenSimplexJobIsSentFromEnterprise_NoPromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenDuplexOutputTwoUpJobIsSentFromEnterpriseFlatbedAddPagePromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAddPage);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenDuplexInputTwoUpJobIsSentFromEnterpriseFlatbedAddPagePromptIsAdded)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedDuplexAddPage);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenIDCardJobIsStartedExpectIDCardPrompt)
{
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobTicket_->getIntent()->setpromptForIdCardBothSide(true);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardFirstSide);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenAddPageScanButtonIsPressed)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));

    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    mockIScannerMedia_ = std::make_shared<dune::scan::scanningsystem::MockIMedia>();
    copyJobTicket_->setScanMediaInterface(mockIScannerMedia_.get());

    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAddPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedAddPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage, alertAction);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenAddPageCancelButtonIsPressed)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAddPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedAddPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_03;
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage,alertAction );
    EXPECT_FALSE(copyJobTicket_->isFirstScanStarted());
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenAddPageDoneButtonIsPressed)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAddPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedAddPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_02;
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage,alertAction );
    EXPECT_FALSE(copyJobTicket_->isFirstScanStarted());
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenAddPageNoResponseIsGiven)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAddPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedAddPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::NoResponse;
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage,alertAction );
    EXPECT_FALSE(copyJobTicket_->isFirstScanStarted());
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenAddPageIsAdded_JobticketIdIsadded)
{
    dune::cdm::alert_1::AlertT* tempAlert;
    ON_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _))
    .WillByDefault(
        testing::DoAll(testing::Invoke([&](dune::cdm::alert_1::AlertT* alert, AlertActionCallback callback, uint32_t timeoutSeconds) {
                    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction =
                        std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
                    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
                    std::cout << "PromptResponseType::Cancel" << std::endl;
                    tempAlert = alert;
                    callback(alert->category, alertAction);
                }),
                Return(true)));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAddPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedAddPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    bool alertPresent = false;
    if(tempAlert->data.size() > 0)
    {
        alertPresent = true;
    }
    EXPECT_EQ(true, alertPresent);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenIDcardISAdded_DataIsAddedToAlert)
{
    dune::cdm::alert_1::AlertT* tempAlert;
    ON_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _))
    .WillByDefault(
        testing::DoAll(testing::Invoke([&](dune::cdm::alert_1::AlertT* alert, AlertActionCallback callback, uint32_t timeoutSeconds) {
                    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction =
                        std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
                    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
                    std::cout << "PromptResponseType::Add" << std::endl;
                    tempAlert = alert;
                    EXPECT_EQ(tempAlert->data[0]->value->sValue, "front");
                    callback(alert->category, alertAction);
                }),
                Return(true)));
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardFirstSide);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::IdCardFirstSide, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    bool alertPresent = false;
    if(tempAlert->data.size() > 0)
    {
        alertPresent = true;
    }
    EXPECT_EQ(true, alertPresent);

}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenIDcardSecondSideISAdded_DataIsAddedToAlert)
{
    dune::cdm::alert_1::AlertT* tempAlert;
    ON_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _))
    .WillByDefault(
        testing::DoAll(testing::Invoke([&](dune::cdm::alert_1::AlertT* alert, AlertActionCallback callback, uint32_t timeoutSeconds) {
                    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction =
                        std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
                    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
                    std::cout << "PromptResponseType::Add" << std::endl;
                    tempAlert = alert;
                    EXPECT_EQ(tempAlert->data[0]->value->sValue, "back");
                    callback(alert->category, alertAction);
                }),
                Return(true)));
    copyJobTicket_->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobTicket_->getIntent()->setpromptForIdCardBothSide(false);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::None);
    prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::IdCardSecondSide);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::IdCardSecondSide, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    bool alertPresent = false;
    if(tempAlert->data.size() > 0)
    {
        alertPresent = true;
    }
    EXPECT_EQ(true, alertPresent);

}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenFlatbedDuplexAddPageScanButtonIsPressed)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedDuplexAddPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedDuplexAddPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage, alertAction);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenFlatbedDuplexDoneButtonIsPressed)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedDuplexAddPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedDuplexAddPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_02;
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage, alertAction);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenFlatbedDuplexNoResponseIsGiven)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedDuplexAddPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedDuplexAddPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::NoResponse;
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage, alertAction);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}
TEST_F(GivenCopyJobPromptControllerEnterprise, WhenFlatbedDuplexCancelButtonIsPressed)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    copyJobTicket_->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->setCompletionState(CompletionStateType::SUCCESS);
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        copyJobTicket_, mockIJobAlertProvider_.get(), Product::ENTERPRISE, true);
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedDuplexAddPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::FlatbedDuplexAddPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_03;
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage, alertAction);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenMDFSourceIsSelectedMDFPromptIsEmplaced)
{
    copyJobTicket_->setFirstScanStarted(true);
    
    //setup mock interfaces
    mockIScannerMedia_ = std::make_shared<dune::scan::scanningsystem::MockIMedia>();
    mockIMediaPath_ = std::make_shared<dune::scan::scanningsystem::MockIMediaPath>();
    mockICopyJobTicket_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();
    mockICopyJobIntent_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    mockIJobAlertProvider_ = std::make_shared<MockIJobManagerAlertProvider>();
    mockIJobTicketHandler_ = std::make_shared<dune::job::MockIJobTicketHandler>();

    //setup tested component
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        mockICopyJobTicket_, mockIJobAlertProvider_.get(), Product::HOME_PRO,false);
    
    //setup common mock calls
    
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(mockICopyJobIntent_));
    ON_CALL(*mockICopyJobTicket_, getHandler()).WillByDefault(Return(mockIJobTicketHandler_));
    ON_CALL(*mockICopyJobTicket_, getScanMediaInterface()).WillByDefault(Return(mockIScannerMedia_.get()));
    ON_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillByDefault(Return(true));
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::MDF));
    ON_CALL(*mockICopyJobTicket_, getMaxCollatePages()).WillByDefault(Return(24));
    ON_CALL(*mockICopyJobIntent_, getCollate()).WillByDefault(Return(dune::copy::SheetCollate::Uncollate));
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    
    ON_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillByDefault(Return(2));
    ON_CALL(*mockICopyJobIntent_, getCopies()).WillByDefault(Return(2));
    ON_CALL(*mockICopyJobTicket_, getJobCompleting()).WillByDefault(Return(true));

    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    ON_CALL(*mockIMediaPath_, getId()).WillByDefault(Return("MDF"));
    ON_CALL(*mockIMediaPath_, getMediaReleaseStatus()).WillByDefault(Return(dune::scan::scanningsystem::IMediaPath::MediaReleaseStatus::RELEASABLE));
    
    copyJobTicket_->getIntent()->setScanSource(dune::scan::types::ScanSource::MDF);

    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::MdfEjectPage);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::MdfEjectPage, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::NoResponse;
    
    EXPECT_CALL(*mockIMediaPath_,unload()).Times(1);
    
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::mdfEjectPage, alertAction);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenCollateEnabled_MaxPagesForCollateIsDisplayed)
{
    std::vector<Uuid> pageIdList;
    for (int page = 0; page < 24; page++)
    {
        pageIdList.push_back(Uuid::createUuid());
    }
    ON_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillByDefault(Return(2));
    ON_CALL(*mockICopyJobTicket_, getMaxCollatePages()).WillByDefault(Return(24));
    ON_CALL(*mockICopyJobIntent_, getCollate()).WillByDefault(Return(dune::copy::SheetCollate::Collate));
    ON_CALL(*mockICopyJobIntent_, getCopies()).WillByDefault(Return(2));
    ON_CALL(*mockICopyJobTicket_, getJobCompleting()).WillByDefault(Return(true));
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    ON_CALL(*mockIJobTicketHandler_, getPagesIds(_)).WillByDefault(Return(pageIdList));

    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    ON_CALL(*mockIMediaPath_, getMediaPresenceStatus()).WillByDefault(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED));

    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::MorePagesDetectedForCollate);
    copyJobPromptController_->displayPrompt(dune::job::PromptType::MorePagesDetectedForCollate, std::bind(&GivenCopyJobPromptControllerEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction = std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::NoResponse;
    copyJobPromptController_->onPromptResponse(dune::cdm::alert_1::Category::morePagesDetectedForCollate, std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>());
    EXPECT_EQ(copyJobPromptController_->getPrompt(), dune::job::PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenNotFirstScanStartedAdfAddpageCalled_AddpagePrompt)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));

    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));  
    ON_CALL(*mockIMediaPath_, getMediaPresenceStatus()).WillByDefault(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::NOT_LOADED));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::UNDEFINED, MediaOrientation::UNDEFINED) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    
    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL));
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::MDF));
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(false));

    bool sourceOrigin = true;
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(sourceOrigin);
    EXPECT_EQ(prompt, dune::job::PromptType::AdfAddPage);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenNotSourceOriginAdfAddpageCalled_None)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));

    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));  
    ON_CALL(*mockIMediaPath_, getMediaPresenceStatus()).WillByDefault(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::NOT_LOADED));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::UNDEFINED, MediaOrientation::UNDEFINED) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    
    EXPECT_CALL(*mockICopyJobIntent_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL));
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::MDF));
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(false));

    bool sourceOrigin = false;
    auto prompt = copyJobPromptController_->getNewPromptToDisplay(sourceOrigin);
    EXPECT_EQ(prompt, PromptType::None);
}

TEST_F(GivenCopyJobPromptControllerEnterprise, WhenNotFirstScanStartedFlatbedAutoDetectFailCalled_FlatbedAutoDetectFailPrompt)
{
    EXPECT_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));

    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));  
    ON_CALL(*mockIMediaPath_, getMediaPresenceStatus()).WillByDefault(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::NOT_LOADED));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::UNDEFINED, MediaOrientation::UNDEFINED) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));
    
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::MDF));
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL(*mockICopyJobTicket_, isFirstScanStarted()).WillRepeatedly(Return(false));

    auto prompt = copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(prompt, dune::job::PromptType::FlatbedAutoDetectFail);
}

class GivenCopyJobPromptControllerForEnterprise : public ::testing::Test
{
  public:
    GivenCopyJobPromptControllerForEnterprise();

    virtual void SetUp() override;
    virtual void TearDown() override;

    void testFunction(dune::job::PromptType promptType, dune::job::PromptResponseType promptResponseType)
    {
        testPromptTypeByCallBack_ = promptType;
        testPromptResponseTypeByCallBack_ = promptResponseType;
        CHECKPOINTA("GivenCopyJobPromptControllerForEnterprise::testFunction promptType : %d", static_cast<int>(promptType));
        CHECKPOINTA("GivenCopyJobPromptControllerForEnterprise::testFunction promptResponseType : %d", static_cast<int>(promptResponseType));
    }

  protected:
    std::shared_ptr<CopyJobTicket>  copyJobTicketForEnterprise_;
    std::unique_ptr<CopyJobPromptController> copyJobPromptControllerForEnterprise_;

    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket>     mockICopyJobTicketForEnterprise_{};
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobIntent>     mockICopyJobIntentForEnterprise_{};
    std::shared_ptr<MockIJobManagerAlertProvider>                   mockIJobAlertProviderForEnterprise_;
    std::shared_ptr<dune::job::MockIJobTicketHandler>               mockIJobTicketHandlerForEnterprise_;
    std::shared_ptr<dune::scan::scanningsystem::MockIMedia>         mockIScannerMediaForEnterprise_;
    std::shared_ptr<dune::scan::scanningsystem::MockIMediaPath>     mockIMediaPath_;

    PromptType testPromptTypeByCallBack_;
    PromptResponseType testPromptResponseTypeByCallBack_;

};

GivenCopyJobPromptControllerForEnterprise::GivenCopyJobPromptControllerForEnterprise()
    : copyJobTicketForEnterprise_{std::make_shared<CopyJobTicket>()},
    mockIJobAlertProviderForEnterprise_{std::make_shared<MockIJobManagerAlertProvider>()}
{
}

void GivenCopyJobPromptControllerForEnterprise::SetUp()
{
    //setup mock interfaces
    mockIScannerMediaForEnterprise_ = std::make_shared<dune::scan::scanningsystem::MockIMedia>();
    mockICopyJobTicketForEnterprise_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();
    mockICopyJobIntentForEnterprise_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    mockIJobAlertProviderForEnterprise_ = std::make_shared<MockIJobManagerAlertProvider>();
    mockIMediaPath_          = std::make_shared<dune::scan::scanningsystem::MockIMediaPath>();

    copyJobTicketForEnterprise_->setFirstScanStarted(false);
    copyJobTicketForEnterprise_->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    copyJobTicketForEnterprise_->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    copyJobPromptControllerForEnterprise_ = std::make_unique<CopyJobPromptController>(
        mockICopyJobTicketForEnterprise_, mockIJobAlertProviderForEnterprise_.get(), Product::ENTERPRISE, true);
    
    ON_CALL(*mockICopyJobTicketForEnterprise_, isFirstScanStarted()).WillByDefault(Return(false));

    ON_CALL(*mockICopyJobTicketForEnterprise_, getIntent()).WillByDefault(Return(mockICopyJobIntentForEnterprise_));
    ON_CALL(*mockICopyJobTicketForEnterprise_, getHandler()).WillByDefault(Return(mockIJobTicketHandlerForEnterprise_));
    ON_CALL(*mockICopyJobTicketForEnterprise_, getScanMediaInterface()).WillByDefault(Return(mockIScannerMediaForEnterprise_.get()));
    ON_CALL(*mockICopyJobTicketForEnterprise_, getSegmentType()).WillByDefault(Return(dune::job::SegmentType::FinalSegment));
}

void GivenCopyJobPromptControllerForEnterprise::TearDown()
{

}

TEST_F(GivenCopyJobPromptControllerForEnterprise, WhenEnterprisePromptOrignalSizeSetToAnyWithGlass_PromptSetToCancel)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIJobAlertProviderForEnterprise_, notifyAlert(_, _, _))
    .WillByDefault(
        testing::DoAll(testing::Invoke([](dune::cdm::alert_1::AlertT* alert, AlertActionCallback callback, uint32_t timeoutSeconds) {
                    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction =
                        std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
                    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_02;
                    std::cout << "PromptResponseType::Cancel" << std::endl;
                    callback(alert->category, alertAction);
                }),
                Return(true)));

    ON_CALL(*mockIScannerMediaForEnterprise_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::UNDEFINED, MediaOrientation::UNDEFINED) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));

    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::GLASS));
    EXPECT_CALL(*mockICopyJobIntentForEnterprise_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    copyJobPromptControllerForEnterprise_->getNewPromptToDisplay(true);
    copyJobPromptControllerForEnterprise_->displayPrompt(dune::job::PromptType::FlatbedAutoDetectFail, std::bind(&GivenCopyJobPromptControllerForEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));

    // Check Callback result
    EXPECT_EQ(testPromptTypeByCallBack_, PromptType::FlatbedAutoDetectFail);
    EXPECT_EQ(testPromptResponseTypeByCallBack_, PromptResponseType::CancelJob);
}

TEST_F(GivenCopyJobPromptControllerForEnterprise, WhenEnterprisePromptOrignalSizeSetToAnyWithGlass_PromptSetToMediaSizeId)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIJobAlertProviderForEnterprise_, notifyAlert(_, _, _))
    .WillByDefault(
        testing::DoAll(testing::Invoke([](dune::cdm::alert_1::AlertT* alert, AlertActionCallback callback, uint32_t timeoutSeconds) {
                    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction =
                        std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
                    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
                    alertAction->param1 = "na_invoice_5.5x8.5in";
                    std::cout << "PromptResponseType::Continue" << std::endl;
                    callback(alert->category, alertAction);
                }),
                Return(true)));

    ON_CALL(*mockIScannerMediaForEnterprise_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::UNDEFINED, MediaOrientation::UNDEFINED) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));

    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::GLASS));
    EXPECT_CALL(*mockICopyJobIntentForEnterprise_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::ANY));
    copyJobPromptControllerForEnterprise_->getNewPromptToDisplay(true);
    copyJobPromptControllerForEnterprise_->displayPrompt(dune::job::PromptType::FlatbedAutoDetectFail, std::bind(&GivenCopyJobPromptControllerForEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));

    // Check Callback result
    EXPECT_EQ(testPromptTypeByCallBack_, PromptType::FlatbedAutoDetectFail);
    EXPECT_EQ(testPromptResponseTypeByCallBack_, PromptResponseType::Response_01);
}

TEST_F(GivenCopyJobPromptControllerForEnterprise, WhenEnterprisePromptOrignalSizeSetToMSOWithGlass_AdfAddPagePromptIsDisplayedAndSetToCancel)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIJobAlertProviderForEnterprise_, notifyAlert(_, _, _))
    .WillByDefault(
        testing::DoAll(testing::Invoke([&](dune::cdm::alert_1::AlertT* alert, AlertActionCallback callback, uint32_t timeoutSeconds) {
                    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction =
                        std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
                    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_02;
                    std::cout << "PromptResponseType::Cancel" << std::endl;
                    callback(alert->category, alertAction);
                }),
                Return(true)));

    ON_CALL(*mockIScannerMediaForEnterprise_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::UNDEFINED, MediaOrientation::UNDEFINED) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));

    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL(*mockICopyJobIntentForEnterprise_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL));
    ON_CALL(*mockICopyJobIntentForEnterprise_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    copyJobPromptControllerForEnterprise_->getNewPromptToDisplay(true);
    copyJobPromptControllerForEnterprise_->displayPrompt(dune::job::PromptType::AdfAddPage, std::bind(&GivenCopyJobPromptControllerForEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));

    // Check Callback result
    EXPECT_EQ(testPromptTypeByCallBack_, PromptType::AdfAddPage);
    EXPECT_EQ(testPromptResponseTypeByCallBack_, PromptResponseType::Response_02);
}

TEST_F(GivenCopyJobPromptControllerForEnterprise, WhenEnterprisePromptOrignalSizeSetToMSOWithGlass_AdfAddPagePromptIsDisplayedAndSetToMediaInADF)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    ON_CALL(*mockIJobAlertProviderForEnterprise_, notifyAlert(_, _, _))
    .WillByDefault(
        testing::DoAll(testing::Invoke([](dune::cdm::alert_1::AlertT* alert, AlertActionCallback callback, uint32_t timeoutSeconds) {
                    std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction =
                        std::make_shared<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT>();
                    alertAction->jobAction = dune::cdm::jobManagement_1::JobManagementAlertsAction::Response_01;
                    std::cout << "PromptResponseType::Cancel" << std::endl;
                    callback(alert->category, alertAction);
                }),
                Return(true)));

    ON_CALL(*mockIScannerMediaForEnterprise_, getInputs()).WillByDefault(Return(scanSourceList));
    MediaDetectionStatus mediaDetectionStatus_{ std::make_pair(MediaSizeId::UNDEFINED, MediaOrientation::UNDEFINED) };
    ON_CALL(*mockIMediaPath_, getMediaDetectionStatus()).WillByDefault(Return(mediaDetectionStatus_));

    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL(*mockICopyJobIntentForEnterprise_, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL));
    copyJobPromptControllerForEnterprise_->getNewPromptToDisplay(true);
    copyJobPromptControllerForEnterprise_->displayPrompt(dune::job::PromptType::AdfAddPage, std::bind(&GivenCopyJobPromptControllerForEnterprise::testFunction, this, std::placeholders::_1, std::placeholders::_2));

    // Check Callback result
    EXPECT_EQ(testPromptTypeByCallBack_, PromptType::AdfAddPage);
    EXPECT_EQ(testPromptResponseTypeByCallBack_, dune::job::PromptResponseType::DisplayNewPrompts);
}

struct CopyJobPromptControllerWithMockTicketParameterizedTestStruct
{
    public:
        int                 numPages_;
        PromptType          expectedPrompt_;
};

class GivenCopyJobPromptControllerWithMockTicketParameterizedForPageCount : public ::testing::TestWithParam<CopyJobPromptControllerWithMockTicketParameterizedTestStruct>
{
  public:
    GivenCopyJobPromptControllerWithMockTicketParameterizedForPageCount();

    virtual void SetUp() override;

protected:
    std::unique_ptr<CopyJobPromptController>                        copyJobPromptController_;
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket>     mockICopyJobTicket_{};
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobIntent>     mockICopyJobIntent_{};
    std::shared_ptr<MockIJobManagerAlertProvider>                   mockIJobAlertProvider_;
    std::shared_ptr<dune::job::MockIJobTicketHandler>               mockIJobTicketHandler_;
    std::shared_ptr<dune::scan::scanningsystem::MockIMedia>         mockIScannerMedia_;
    std::shared_ptr<dune::scan::scanningsystem::MockIMediaPath>     mockIMediaPath_;

    //param values
    int                                                             numPages_;
    PromptType                                                      expectedPrompt_;
};

GivenCopyJobPromptControllerWithMockTicketParameterizedForPageCount::GivenCopyJobPromptControllerWithMockTicketParameterizedForPageCount()
{
    //Parse parameters
    auto param = GetParam();
    numPages_ = param.numPages_;
    expectedPrompt_ = param.expectedPrompt_;
}

void GivenCopyJobPromptControllerWithMockTicketParameterizedForPageCount::SetUp()
{   
    //setup mock interfaces
    mockIScannerMedia_ = std::make_shared<dune::scan::scanningsystem::MockIMedia>();
    mockIMediaPath_ = std::make_shared<dune::scan::scanningsystem::MockIMediaPath>();
    mockICopyJobTicket_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();
    mockICopyJobIntent_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    mockIJobAlertProvider_ = std::make_shared<MockIJobManagerAlertProvider>();
    mockIJobTicketHandler_ = std::make_shared<dune::job::MockIJobTicketHandler>();

    //setup tested component
    copyJobPromptController_ = std::make_unique<CopyJobPromptController>(
        mockICopyJobTicket_, mockIJobAlertProvider_.get(), Product::HOME_PRO,false);
    
    //setup common mock calls
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(mockICopyJobIntent_));
    ON_CALL(*mockICopyJobTicket_, getHandler()).WillByDefault(Return(mockIJobTicketHandler_));
    ON_CALL(*mockICopyJobTicket_, getScanMediaInterface()).WillByDefault(Return(mockIScannerMedia_.get()));
    ON_CALL(*mockICopyJobTicket_, getMaxCollatePages()).WillByDefault(Return(24));
}

TEST_P(GivenCopyJobPromptControllerWithMockTicketParameterizedForPageCount, WhenPageLimitDetectedOrNot_PromptIsShownCorrectly)
{
    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{mockIMediaPath_};
    
    std::vector<Uuid> pageIdList;
    for (int page = 0; page < numPages_; page++)
    {
        pageIdList.push_back(Uuid::createUuid());
    }
    ON_CALL(*mockIJobAlertProvider_, notifyAlert(_, _, _)).WillByDefault(Return(2));
    ON_CALL(*mockICopyJobIntent_, getCollate()).WillByDefault(Return(dune::copy::SheetCollate::Collate));
    ON_CALL(*mockICopyJobIntent_, getCopies()).WillByDefault(Return(2));
    ON_CALL(*mockICopyJobTicket_, getJobCompleting()).WillByDefault(Return(true));
    ON_CALL(*mockICopyJobIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    ON_CALL(*mockIJobTicketHandler_, getPagesIds(_)).WillByDefault(Return(pageIdList));
    ON_CALL(*mockIScannerMedia_, getInputs()).WillByDefault(Return(scanSourceList));
    ON_CALL(*mockIMediaPath_, getType()).WillByDefault(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    ON_CALL(*mockIMediaPath_, getMediaPresenceStatus()).WillByDefault(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED));

    copyJobPromptController_->getNewPromptToDisplay(true);
    EXPECT_EQ(copyJobPromptController_->getPrompt(), expectedPrompt_);
}

INSTANTIATE_TEST_CASE_P
(
    ,
    GivenCopyJobPromptControllerWithMockTicketParameterizedForPageCount,
    ::testing::Values
    (
        CopyJobPromptControllerWithMockTicketParameterizedTestStruct{24, PromptType::MorePagesDetectedForCollate},
        CopyJobPromptControllerWithMockTicketParameterizedTestStruct{5, PromptType::None},
        CopyJobPromptControllerWithMockTicketParameterizedTestStruct{27, PromptType::None}
    )
);