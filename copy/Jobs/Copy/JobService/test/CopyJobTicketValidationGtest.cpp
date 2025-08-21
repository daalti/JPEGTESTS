// /* -*- c++ -*- */

// ///////////////////////////////////////////////////////////////////////////////
// /**
//  * @file   ScanJobIntentValidationGtest.cpp
//  * @date   Mon, 8 Mar 2023 13:10:21 CET
//  * @author Yago Cordero Carrera (yago.cordero.carrera@hp.com)
//  * @brief  Gtest for Validation of copy intent values 
//  *
//  * (C) Copyright 2023 HP Development Company, L.P.
//  * All rights reserved.
//  */
// ///////////////////////////////////////////////////////////////////////////////

#include "CopyJobTicket.h"
#include "gmock/gmock.h"
#include "gtest/gtest.h"
#include "GTestConfigHelper.h"
#include "IMedia.h"
#include "MockIMedia.h"
#include "MockIPageBasedFinisher.h"

using GTestConfigHelper         = dune::framework::core::gtest::GTestConfigHelper;
using ::testing::_;
using ::testing::Return;
using testing::ReturnRef;

using namespace dune::copy::Jobs::Copy;
using IMedia                        = dune::print::engine::IMedia;
using MockIMediaIOutputBin = dune::print::engine::MockIMediaIOutputBin;
using MediaProcessingTypes = dune::imaging::types::MediaProcessingTypes;

class GivenCopyJobTicketValidator : public ::testing::Test
{
public:
    GivenCopyJobTicketValidator(){};

    virtual void SetUp() override {};
    virtual void TearDown() override {};

    std::shared_ptr<ICopyJobTicket> generateTicket()
    { 
        auto ticket = std::make_shared<CopyJobTicket>(); 
        ticket->setConstraints(generateCopyConstraint());
        return ticket;
    };

    std::shared_ptr<CopyJobIntentFbT> generateFbIntent()
    {
        auto jobIntentFb = std::make_shared<CopyJobIntentFbT>();

        jobIntentFb->scanJobIntent = std::make_unique<dune::scan::Jobs::Scan::ScanJobIntentFbT>();
        jobIntentFb->scanJobIntent->scanXResolution = dune::imaging::types::Resolution::E300DPI;
        jobIntentFb->scanJobIntent->scanYResolution = dune::imaging::types::Resolution::E300DPI;
        jobIntentFb->scanJobIntent->scanHighlight = 1;
        jobIntentFb->outputMediaDestination = dune::imaging::types::MediaDestinationId::STACKER;

        return jobIntentFb;
    };

    std::shared_ptr<ICopyJobConstraints> generateCopyConstraint()
    { 
        auto constraints = std::make_shared<CopyJobConstraint>();

        // Scan constraints to avoid errors or problems
        dune::scan::Jobs::Scan::ScanJobMediaSupportedSize size;
        size.addId(dune::imaging::types::MediaSizeId::LETTER);
        constraints->addFlatbedOriginalSize(size);

        constraints->addMdfResolution(300);
        constraints->addInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
        constraints->addColorMode(dune::imaging::types::ColorMode::COLOR);
        constraints->addOriginalContentType(dune::imaging::types::OriginalContentType::MIXED);
        constraints->addScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
        constraints->setMinContrast(0);
        constraints->setMinSharpness(0);
        constraints->addOriginalType(dune::scan::types::OriginalMediaType::WHITE_PAPER);
        constraints->addScaleSelection(dune::scan::types::ScanScaleSelectionEnum::NONE);
        constraints->addScaleToSize(dune::imaging::types::MediaSizeId::LETTER);
        constraints->addScanCaptureMode(dune::scan::types::ScanCaptureModeType::STANDARD);
        constraints->addScanPagesFlipUpEnabled(false);
        constraints->addPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::OneUp);
        constraints->addOutputCanvasAnchors(dune::imaging::types::OutputCanvasAnchorType::TOPLEFT);
        constraints->addOutputCanvasMediaIds(dune::imaging::types::MediaSource::AUTOSELECT);
        constraints->addOutputStandardSizes(dune::imaging::types::MediaSizeId::ANY);
        constraints->addOutputCanvasOrientations(dune::imaging::types::ContentOrientation::PORTRAIT);

        // Copy constraints
        constraints->addPlexMode(dune::imaging::types::Plex::SIMPLEX);
        constraints->addPlexBinding(dune::imaging::types::PlexBinding::LONG_EDGE);
        constraints->addCollate(dune::copy::SheetCollate::Collate);
        constraints->addPrintQuality(dune::imaging::types::PrintQuality::NORMAL);
        constraints->addMediaPrintSupportedSource(dune::imaging::types::MediaSource::TRAY1);
        constraints->addMediaPrintSupportedSize(dune::imaging::types::MediaSizeId::LETTER);
        constraints->addMediaPrintSupportedType(dune::imaging::types::MediaIdType::STATIONERY);
        constraints->addCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
        constraints->addPrintingOrder(dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
        constraints->addMediaFamily(dune::imaging::types::MediaFamily::ADHESIVE);
        constraints->addAutoRotate(false);
        constraints->addMediaDestinations(dune::imaging::types::MediaDestinationId::STACKER);

        CopyJobMediaSupportedSize mediaSupportedSize;
        mediaSupportedSize.addId(dune::imaging::types::MediaSizeId::LETTER);
        CopyJobMediaSupportedType mediaSupportedType;
        mediaSupportedType.addId(dune::imaging::types::MediaIdType::STATIONERY);

        constraints->addMediaSupportedSize(mediaSupportedSize);
        constraints->addMediaSupportedType(mediaSupportedType);

        return constraints;
    };

    bool intentWasUpdated_ = false;
};

TEST_F(GivenCopyJobTicketValidator,WhenValidateIntentIsCalledAndAllIsOK_ThenValidateResultOk)
{
    auto ticket = generateTicket();  
    validateTicket(ticket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_FALSE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(ticket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndOutputMediaSizeIdIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A0);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndOutputMediaIdTypeIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::BOND);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndOutputMediaSourceIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::CENTER);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndOutputPlexModeIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndOutputPlexBindingIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setOutputPlexBinding(dune::imaging::types::PlexBinding::SHORT_EDGE);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndCollateIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndCopyQualityIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setCopyQuality(dune::imaging::types::PrintQuality::DRAFT);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndCopyMarginsIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setCopyMargins(dune::imaging::types::CopyMargins::ADDTOCONTENT);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndOutputDestinationIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndPrintingOrderIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setPrintingOrder(dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndAutoRotateIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setAutoRotate(true);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndMediaFamilyIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setMediaFamily(dune::imaging::types::MediaFamily::CANVAS);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndCopiesIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setCopies(3000);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateIntentIsCalledAndRotationIsNotOk_ThenValidateResultOnRequestUpdate)
{
    auto badTicket = generateTicket();
    badTicket->getIntent()->setRotation(3000);
    validateTicket(badTicket, generateFbIntent(), intentWasUpdated_);    
    EXPECT_TRUE(intentWasUpdated_);
    EXPECT_TRUE(compareIntents(badTicket->getIntent(),generateTicket()->getIntent()));
}

TEST_F(GivenCopyJobTicketValidator, WhenUpdateMediaOutputDestinationPageBasedFinisherInstalledIsCalled_ThenValidateResultOk)
{
    dune::print::engine::MockIMedia* mockIMedia_ = new dune::print::engine::MockIMedia();;
    MockIMediaIOutputBin                        outputBinMock1_;
    IMedia::OutputBinPtr                        mockOutputBinPtr_{&outputBinMock1_, [](IMedia::IOutputBin *) {}};

    dune::print::engine::IMedia::OutputBinPtr outputPtr1(&outputBinMock1_, [](dune::print::engine::IMedia::IOutput *) {} );
    ON_CALL(outputBinMock1_, getType())
        .WillByDefault(Return(dune::print::engine::OutputType::BIN));
    
    ON_CALL(outputBinMock1_, getBin())
        .WillByDefault(Return(mockOutputBinPtr_));
     
    ON_CALL(outputBinMock1_, getMediaDestinationId())
        .WillByDefault(Return(dune::imaging::types::MediaDestinationId::OUTPUTBIN1));

    const dune::print::engine::IMedia::OutputList outputs = { outputPtr1 };
    ON_CALL(*mockIMedia_, getOutputDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::OK, outputs)));


    CopyJobTicket ticket;
    ticket.setMediaInterface(mockIMedia_);

    bool retVal = ticket.UpdateMediaOutputDestinationPageBasedFinisherInstalled();
    EXPECT_TRUE(retVal);

    delete mockIMedia_;
}

TEST_F(GivenCopyJobTicketValidator, WhenUpdateMediaOutputDestinationPageBasedFinisherInstalledIsCalled_ThenValidateResultFalse)
{
    dune::print::engine::MockIMedia* mockIMedia_ = new dune::print::engine::MockIMedia();;
    MockIMediaIOutputBin                        outputBinMock1_;
    IMedia::OutputBinPtr                        mockOutputBinPtr_{&outputBinMock1_, [](IMedia::IOutputBin *) {}};

    dune::print::engine::IMedia::OutputBinPtr outputPtr1(&outputBinMock1_, [](dune::print::engine::IMedia::IOutput *) {} );
    ON_CALL(outputBinMock1_, getType())
        .WillByDefault(Return(dune::print::engine::OutputType::BIN));
    
    ON_CALL(outputBinMock1_, getBin())
        .WillByDefault(Return(mockOutputBinPtr_));
     
    const dune::print::engine::IMedia::OutputList outputs = { outputPtr1 };
    ON_CALL(*mockIMedia_, getOutputDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::ERROR, outputs)));

    CopyJobTicket ticket;
    ticket.setMediaInterface(mockIMedia_);

    bool retVal = ticket.UpdateMediaOutputDestinationPageBasedFinisherInstalled();
    EXPECT_TRUE(retVal);

    delete mockIMedia_;
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateTicketForPageBasedFinisherIsCalledWithInstalledFinisher_ThenValidateResultOk)
{
    dune::print::engine::MockIMedia* mockIMedia = new dune::print::engine::MockIMedia();;
    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock, [](IMedia::IPageBasedFinisher *) {} )
    };

    ON_CALL(*mockIMedia, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, pageBasedFinishers)));

    IMedia::PageBasedFinisherPtr pageBasedFinisherPtr = IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock, [](IMedia::IPageBasedFinisher * p){} );
    ON_CALL(pageBasedFinisherMock, getPageBasedFinisher())
        .WillByDefault(Return(pageBasedFinisherPtr));

    ON_CALL(pageBasedFinisherMock, getType())
        .WillByDefault(Return(dune::print::engine::FinisherType::PAGEBASED_FINISHER));

    std::tuple<APIResult, std::vector<MediaProcessingTypes>> mediaProcessingTypes{APIResult::OK, {MediaProcessingTypes::STAPLE}};
    ON_CALL(pageBasedFinisherMock, getMediaProcessingTypes())
        .WillByDefault(ReturnRef(mediaProcessingTypes));

    bool intentWasUpdated_ = false;
    auto ticket = generateTicket();
    ticket->setMediaInterface(mockIMedia);
    validateTicketForPageBasedFinisher(ticket, generateFbIntent(), intentWasUpdated_);
    EXPECT_TRUE(intentWasUpdated_);

    delete mockIMedia;
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateTicketForPageBasedFinisherIsCalledWithOutFinisherStaple_ThenValidateResultOk)
{
    dune::print::engine::MockIMedia* mockIMedia = new dune::print::engine::MockIMedia();;
    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock, [](IMedia::IPageBasedFinisher *) {} )
    };

    ON_CALL(*mockIMedia, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::ERROR, pageBasedFinishers)));

    bool intentWasUpdated_ = false;
    auto ticket = generateTicket();
    ticket->setMediaInterface(mockIMedia);
    ticket->getIntent()->setStapleOption(dune::imaging::types::StapleOptions::LEFT_TWO_POINTS);
    validateTicketForPageBasedFinisher(ticket, generateFbIntent(), intentWasUpdated_);
    EXPECT_TRUE(intentWasUpdated_);

    delete mockIMedia;
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateTicketForPageBasedFinisherIsCalledWithOutFinisherPunch_ThenValidateResultOk)
{
    dune::print::engine::MockIMedia* mockIMedia = new dune::print::engine::MockIMedia();;
    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock, [](IMedia::IPageBasedFinisher *) {} )
    };

    ON_CALL(*mockIMedia, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::ERROR, pageBasedFinishers)));

    bool intentWasUpdated_ = false;
    auto ticket = generateTicket();
    ticket->setMediaInterface(mockIMedia);
    ticket->getIntent()->setPunchOption(dune::imaging::types::PunchingOptions::LEFT_TWO_POINT_DIN);
    validateTicketForPageBasedFinisher(ticket, generateFbIntent(), intentWasUpdated_);
    EXPECT_TRUE(intentWasUpdated_);

    delete mockIMedia;
}

TEST_F(GivenCopyJobTicketValidator, WhenValidateTicketForPageBasedFinisherIsCalledWithOutFinisherDestination_ThenValidateResultOk)
{
    dune::print::engine::MockIMedia* mockIMedia = new dune::print::engine::MockIMedia();;
    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock, [](IMedia::IPageBasedFinisher *) {} )
    };

    ON_CALL(*mockIMedia, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::ERROR, pageBasedFinishers)));

    bool intentWasUpdated_ = false;
    auto ticket = generateTicket();
    ticket->setMediaInterface(mockIMedia);
    ticket->getIntent()->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN1);

    auto defaultIntentFromConfig = generateFbIntent();
    defaultIntentFromConfig->outputMediaDestination = dune::imaging::types::MediaDestinationId::STANDARDBIN;

    validateTicketForPageBasedFinisher(ticket, defaultIntentFromConfig, intentWasUpdated_);
    EXPECT_TRUE(intentWasUpdated_);

    delete mockIMedia;
}


/**
 * @brief Values on Intent currently not covered.
 * If on future is needed to cover any of them, add a test related.
 * 
 * intent->setResize ( ... )
 * intent->setLighterDarker( ... )
 * intent->setPlexSide( ... )
 * intent->setOutputMediaOrientation( ... )
 * 
 * And rest of intents not covered on scan part are defined on src/fw/scan/Jobs/Scan/test/ScanJobIntentValidationGtest.cpp
 */