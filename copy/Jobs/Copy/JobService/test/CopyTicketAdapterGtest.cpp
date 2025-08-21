/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyTicketAdapterGtest.cpp
 * @date   May, 4th 2021 09:59:23 +0530
 * @author Corey Norberg (corey.b.norberg@hp.com)
 * @brief  This file contains unit test for CopyTicketAdapter
 *
 * (C) Copyright 2021 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include <iostream>
#include <memory>

#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "CopyTicketAdapterGtest_TraceAutogen.h"
#include "MockIJobServiceFactory.h"
#include "ICopyJobDynamicConstraintRules.h"
#include "CopyTicketAdapter.h"
#include "MockICopyJobTicket.h"
#include "MockICopyAdapter.h"
#include "MockICopyJobDynamicConstraintRules.h"
#include "MockIJobConstraints.h"
#include "MockILocaleProvider.h"
#include "StringIds.h"
#include "CopyTicketGtestUtilities.h"
#include "MockIMedia.h"
#include "IMedia.h"
#include "MockIFinisherCombination.h"
#include "typeMappers.h"

using namespace std;
using namespace testing;
using namespace dune::job;
using namespace dune::copy::Jobs::Copy;
using dune::cdm::jobTicket_1::jobTicket::SrcT;
using dune::cdm::jobTicket_1::jobTicket::DestT;
using dune::cdm::jobTicket_1::jobTicket::PipelineOptionsT;
using testing::Return;
using Permission = dune::security::ac::Permission;
using MockICopyAdapter = dune::copy::cdm::MockICopyAdapter;
using Product = dune::copy::Jobs::Copy::Product;
//using CopyJobDynamicConstraintRulesStandard = dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard;
using ICopyJobDynamicConstraintRules = dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules;
using IMedia                        = dune::print::engine::IMedia;
using MockIMedia = dune::print::engine::MockIMedia;
using MockIFinisherCombination = dune::print::engine::MockIFinisherCombination;
using MockIMediaIOutput = dune::print::engine::MockIMediaIOutput;

///////////////////////////////////////////////////////////////////////////////
//
// class GivenACopyTicketAdapter : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenANewCopyTicketAdapter : public ::testing::Test
{
  public:
    GivenANewCopyTicketAdapter() {}
    virtual void                                    SetUp() override;
    virtual void                                    TearDown() override;
    void createOutputBinWithPageBasedFinisherCombination();
    std::shared_ptr<ICopyJobTicket>                 copyJobTicket_;
    std::shared_ptr<ICopyJobIntent>                 copyJobIntent_;
    MockIJobServiceFactory<MockICopyJobTicket>*     mockIJobService_;
    CopyTicketAdapter*                              copyTicketAdapter_;
    std::shared_ptr<MockILocaleProvider>            mockLocaleProvider_;
  protected:
    MockIFinisherCombination finisherCombinationMock_;
    MockIMedia* mediaMock_ = new dune::print::engine::MockIMedia();
    MockIMediaIOutput* mockOutput1_ = new dune::print::engine::MockIMediaIOutput();
    MockIMediaIOutput* mockOutput2_ = new dune::print::engine::MockIMediaIOutput();
    MockIMediaIOutput* mockOutput3_ = new dune::print::engine::MockIMediaIOutput();
    MockIMediaIOutput* mockOutput4_ = new dune::print::engine::MockIMediaIOutput();
    MockIMediaIOutput* mockOutput5_ = new dune::print::engine::MockIMediaIOutput();
    MockIMediaIOutput* mockOutputAlternateBin_ = new dune::print::engine::MockIMediaIOutput();

    std::tuple<APIResult, bool>isStaplingSupported_{APIResult::NOT_AVAILABLE, false};
    std::tuple<APIResult, bool>isPunchingSupported_{APIResult::NOT_AVAILABLE, false};
    std::tuple<APIResult, bool>isFoldingSupported_{APIResult::NOT_AVAILABLE, false};
    std::tuple<APIResult, bool>isBookletMakerSupported_{APIResult::NOT_AVAILABLE, false};
};

void GivenANewCopyTicketAdapter::SetUp()
{
    copyJobTicket_ = std::make_shared<CopyJobTicket>();
    copyJobTicket_->getConstraints()->addCollate(dune::copy::SheetCollate::Collate);
    copyJobTicket_->getConstraints()->addCollate(dune::copy::SheetCollate::Uncollate);
    copyJobTicket_->getConstraints()->addPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket_->getConstraints()->addPlexMode(dune::imaging::types::Plex::DUPLEX);

    copyJobTicket_->getConstraints()->addPrintQuality(dune::imaging::types::PrintQuality::DRAFT);
    copyJobTicket_->getConstraints()->addPrintQuality(dune::imaging::types::PrintQuality::NORMAL);
    copyJobTicket_->getConstraints()->addPrintQuality(dune::imaging::types::PrintQuality::BEST);

    copyJobIntent_ = copyJobTicket_->getIntent();
    Uuid ticketID = Uuid::createUuid();
    // fill here any setInterface required
    mockIJobService_ = new MockIJobServiceFactory<MockICopyJobTicket>();
    copyTicketAdapter_ = new CopyTicketAdapter(copyJobTicket_, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);
    ASSERT_NE(copyTicketAdapter_, nullptr);

    // Set the default metric as units system
    mockLocaleProvider_ = std::make_shared<MockILocaleProvider>();
    ON_CALL(*mockLocaleProvider_, getMeasurmentUnit()).WillByDefault(Return(dune::localization::MeasurementUnit::METRIC));

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    dune::print::engine::IMedia::InputList inputs{mockIMediaIInput};

    ON_CALL(*mediaMock_, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    copyJobTicket_->setMediaInterface(mediaMock_);
    createOutputBinWithPageBasedFinisherCombination();
}

void GivenANewCopyTicketAdapter::createOutputBinWithPageBasedFinisherCombination()
{
    const std::vector<IMedia::FinisherCombinationPtr> finisherCombinations = { IMedia::FinisherCombinationPtr(&finisherCombinationMock_, [](IMedia::IFinisherCombination *) {} ) };
    ON_CALL(*mockOutput1_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));
    ON_CALL(*mockOutput2_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));
    ON_CALL(*mockOutput3_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));
    ON_CALL(*mockOutput4_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));
    ON_CALL(*mockOutput5_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));

    const IMedia::OutputList outputs = {
        IMedia::OutputPtr(mockOutput1_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(mockOutput2_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(mockOutput3_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(mockOutput4_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(mockOutput5_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(mockOutputAlternateBin_,[](IMedia::IOutput *) {})
    };

    ON_CALL(*mediaMock_, getOutputDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::OK, outputs)));

    isBookletMakerSupported_ = std::tuple<APIResult, bool>(APIResult::OK, true);
    ON_CALL(finisherCombinationMock_,isBookletMakerSupported()).WillByDefault(ReturnRef(isBookletMakerSupported_));

    isStaplingSupported_ = std::tuple<APIResult, bool>(APIResult::OK, true);
    ON_CALL(finisherCombinationMock_,isStaplingSupported()).WillByDefault(ReturnRef(isStaplingSupported_));

    isPunchingSupported_ = std::tuple<APIResult, bool>(APIResult::OK, true);
    ON_CALL(finisherCombinationMock_,isPunchingSupported()).WillByDefault(ReturnRef(isPunchingSupported_));

    isFoldingSupported_ = std::tuple<APIResult, bool>(APIResult::OK, true);
    ON_CALL(finisherCombinationMock_,isFoldingSupported()).WillByDefault(ReturnRef(isFoldingSupported_));
}

void GivenANewCopyTicketAdapter::TearDown()
{
    delete copyTicketAdapter_;
    delete mockIJobService_;
    delete mediaMock_;
    delete mockOutput1_;
    delete mockOutput2_;
    delete mockOutput3_;    
    delete mockOutput4_;
    delete mockOutput5_;
    delete mockOutputAlternateBin_;
}

TEST_F(GivenANewCopyTicketAdapter, BasicSerializeDeserializeTest)
{
    CHECKPOINTC(" BasicSerializeDeserializeTest Entry");
    //Uuid                                    uid = Uuid::createUuid();
    //string                                  testDestPath{""};
    //string                                  testFileName{"scan"};
    //dune::cdm::jobTicket_1::FileFormat      testFileFormat{dune::cdm::jobTicket_1::FileFormat::jpeg};
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->scaleToSize.getMutable()  = dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in;
    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->scaleToOutput.getMutable() = dune::cdm::glossary_1::MediaSourceId::tray_dash_1;
    jobTicket->pipelineOptions.getMutable()->generatePreview.getMutable()  = dune::cdm::glossary_1::FeatureEnabled::false_;
    jobTicket->pipelineOptions.getMutable()->promptForAdditionalPages.getMutable() = dune::cdm::glossary_1::FeatureEnabled::false_;
    jobTicket->src.getMutable()->scan.getMutable()->autoDeskew.getMutable()= dune::cdm::glossary_1::FeatureEnabled::false_;
    jobTicket->src.getMutable()->scan.getMutable()->edgeToEdgeScan.getMutable()= dune::cdm::glossary_1::FeatureEnabled::false_;

    EXPECT_EQ(jobTicket->src.get()->scan.get()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::color);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->mediaSource.get(), dune::cdm::glossary_1::ScanMediaSourceId::adf);
    EXPECT_EQ(dune::cdm::glossary_1::MediaSize::valueFromString(jobTicket->src.get()->scan.get()->mediaSize.get()), dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->plexMode.get(), dune::cdm::glossary_1::PlexMode::simplex);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e300Dpi);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->contentType.get(), dune::cdm::jobTicket_1::ContentType::mixed);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->mediaType.get(), dune::cdm::glossary_1::ScanMediaType::whitePaper);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->scanCaptureMode.get(), dune::cdm::jobTicket_1::ScanCaptureMode::standard);

    EXPECT_EQ(jobTicket->dest.get()->print.get()->collate.get(), dune::cdm::jobTicket_1::CollateModes::collated);
    EXPECT_EQ(jobTicket->dest.get()->print.get()->copies.get(), 1);
    EXPECT_EQ(dune::cdm::glossary_1::MediaSourceId::valueFromString(jobTicket->dest.get()->print.get()->mediaSource.get()), dune::cdm::glossary_1::MediaSourceId::tray_dash_1);
    EXPECT_EQ(dune::cdm::glossary_1::MediaSize::valueFromString(jobTicket->dest.get()->print.get()->mediaSize.get()), dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in);
    EXPECT_EQ(dune::cdm::glossary_1::MediaType::valueFromString(jobTicket->dest.get()->print.get()->mediaType.get()), dune::cdm::glossary_1::MediaType::stationery);
    EXPECT_EQ(jobTicket->dest.get()->print.get()->plexMode.get(), dune::cdm::glossary_1::PlexMode::simplex);
    EXPECT_EQ(jobTicket->dest.get()->print.get()->printQuality.get(), dune::cdm::glossary_1::PrintQuality::normal);

    EXPECT_EQ(jobTicket->pipelineOptions.get()->imageModifications.get()->exposure.get(), 5);

    EXPECT_EQ(jobTicket->pipelineOptions.get()->scaling.get()->xScalePercent.get(), 100);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->scaling.get()->yScalePercent.get(), 100);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->scaling.get()->scaleSelection.get(), dune::cdm::jobTicket_1::scaling::ScaleSelection::none);

    EXPECT_EQ(dune::cdm::glossary_1::MediaSize::valueFromString(jobTicket->pipelineOptions.get()->scaling.get()->scaleToSize.get()), dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in);
    EXPECT_EQ(dune::cdm::glossary_1::MediaSourceId::valueFromString(jobTicket->pipelineOptions.get()->scaling.get()->scaleToOutput.get()), dune::cdm::glossary_1::MediaSourceId::tray_dash_1);

    EXPECT_EQ(jobTicket->pipelineOptions.get()->generatePreview.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->promptForAdditionalPages.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->autoDeskew.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->edgeToEdgeScan.get(), dune::cdm::glossary_1::FeatureEnabled::false_);

    // gtest_copy_Jobs_Copy_JobService
    jobTicket->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::monochrome;
    jobTicket->src.getMutable()->scan.getMutable()->mediaSource = dune::cdm::glossary_1::ScanMediaSourceId::flatbed;
    jobTicket->src.getMutable()->scan.getMutable()->mediaSize = dune::cdm::glossary_1::MediaSize::valueToString(dune::cdm::glossary_1::MediaSize::na_legal_8_dot_5x14in);
    jobTicket->src.getMutable()->scan.getMutable()->plexMode = dune::cdm::glossary_1::PlexMode::duplex;
    jobTicket->src.getMutable()->scan.getMutable()->resolution = dune::cdm::jobTicket_1::Resolutions::e600Dpi;
    jobTicket->src.getMutable()->scan.getMutable()->contentType = dune::cdm::jobTicket_1::ContentType::mixed;
    jobTicket->src.getMutable()->scan.getMutable()->mediaType = dune::cdm::glossary_1::ScanMediaType::whitePaperEnhanced;
    jobTicket->src.getMutable()->scan.getMutable()->scanCaptureMode = dune::cdm::jobTicket_1::ScanCaptureMode::idCard;

    jobTicket->pipelineOptions.getMutable()->generatePreview = dune::cdm::glossary_1::FeatureEnabled::true_;
    jobTicket->pipelineOptions.getMutable()->promptForAdditionalPages = dune::cdm::glossary_1::FeatureEnabled::true_;
    jobTicket->src.getMutable()->scan.getMutable()->autoDeskew = dune::cdm::glossary_1::FeatureEnabled::true_;
    jobTicket->src.getMutable()->scan.getMutable()->edgeToEdgeScan = dune::cdm::glossary_1::FeatureEnabled::true_;

    jobTicket->dest.getMutable()->print.getMutable()->collate = dune::cdm::jobTicket_1::CollateModes::uncollated;
    jobTicket->dest.getMutable()->print.getMutable()->copies = 10;
    jobTicket->dest.getMutable()->print.getMutable()->mediaSource = dune::cdm::glossary_1::MediaSourceId::valueToString(dune::cdm::glossary_1::MediaSourceId::tray_dash_2);
    jobTicket->dest.getMutable()->print.getMutable()->mediaSize = dune::cdm::glossary_1::MediaSize::valueToString(dune::cdm::glossary_1::MediaSize::na_legal_8_dot_5x14in);
    jobTicket->dest.getMutable()->print.getMutable()->mediaType = dune::cdm::glossary_1::MediaType::valueToString(dune::cdm::glossary_1::MediaType::com_dot_hp_dot_recycled);
    jobTicket->dest.getMutable()->print.getMutable()->plexMode = dune::cdm::glossary_1::PlexMode::duplex;
    jobTicket->dest.getMutable()->print.getMutable()->printQuality = dune::cdm::glossary_1::PrintQuality::draft;

    jobTicket->pipelineOptions.getMutable()->imageModifications.getMutable()->exposure = 9;

    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->xScalePercent = 50;
    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->yScalePercent = 50;
    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->scaleSelection = dune::cdm::jobTicket_1::scaling::ScaleSelection::standardSizeScaling;
    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->scaleToSize = dune::cdm::glossary_1::MediaSize::valueToString(dune::cdm::glossary_1::MediaSize::na_govt_dash_letter_8x10in);
    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->scaleToOutput = dune::cdm::glossary_1::MediaSourceId::valueToString(dune::cdm::glossary_1::MediaSourceId::tray_dash_2);

    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    if (success)
    {
        jobTicket = copyTicketAdapter_->serializeIntoTable();
        EXPECT_EQ(jobTicket->src.get()->scan.get()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::monochrome);
        EXPECT_EQ(jobTicket->src.get()->scan.get()->mediaSource.get(), dune::cdm::glossary_1::ScanMediaSourceId::flatbed);
        EXPECT_EQ(jobTicket->src.get()->scan.get()->mediaSize.get(), dune::cdm::glossary_1::MediaSize::valueToString(dune::cdm::glossary_1::MediaSize::na_legal_8_dot_5x14in));
        EXPECT_EQ(jobTicket->src.get()->scan.get()->plexMode.get(), dune::cdm::glossary_1::PlexMode::duplex);
        EXPECT_EQ(jobTicket->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e600Dpi);
        EXPECT_EQ(jobTicket->src.get()->scan.get()->contentType.get(), dune::cdm::jobTicket_1::ContentType::mixed);
        EXPECT_EQ(jobTicket->src.get()->scan.get()->mediaType.get(), dune::cdm::glossary_1::ScanMediaType::whitePaperEnhanced);
        EXPECT_EQ(jobTicket->src.get()->scan.get()->scanCaptureMode.get(), dune::cdm::jobTicket_1::ScanCaptureMode::idCard);

        EXPECT_EQ(jobTicket->dest.get()->print.get()->collate.get(), dune::cdm::jobTicket_1::CollateModes::uncollated);
        EXPECT_EQ(jobTicket->dest.get()->print.get()->copies.get(), 10);
        EXPECT_EQ(jobTicket->dest.get()->print.get()->mediaSource.get(), dune::cdm::glossary_1::MediaSourceId::valueToString(dune::cdm::glossary_1::MediaSourceId::tray_dash_2));
        EXPECT_EQ(jobTicket->dest.get()->print.get()->mediaSize.get(), dune::cdm::glossary_1::MediaSize::valueToString(dune::cdm::glossary_1::MediaSize::na_legal_8_dot_5x14in));
        EXPECT_EQ(jobTicket->dest.get()->print.get()->mediaType.get(), dune::cdm::glossary_1::MediaType::valueToString(dune::cdm::glossary_1::MediaType::com_dot_hp_dot_recycled));
        EXPECT_EQ(jobTicket->dest.get()->print.get()->plexMode.get(), dune::cdm::glossary_1::PlexMode::duplex);
        EXPECT_EQ(jobTicket->dest.get()->print.get()->printQuality.get(), dune::cdm::glossary_1::PrintQuality::draft);

        EXPECT_EQ(jobTicket->pipelineOptions.get()->generatePreview.get(), dune::cdm::glossary_1::FeatureEnabled::true_);
        EXPECT_EQ(jobTicket->pipelineOptions.get()->promptForAdditionalPages.get(), dune::cdm::glossary_1::FeatureEnabled::true_);
        EXPECT_EQ(jobTicket->src.get()->scan.get()->autoDeskew.get(), dune::cdm::glossary_1::FeatureEnabled::true_);
        EXPECT_EQ(jobTicket->src.get()->scan.get()->edgeToEdgeScan.get(), dune::cdm::glossary_1::FeatureEnabled::true_);
        EXPECT_EQ(jobTicket->pipelineOptions.get()->imageModifications.get()->exposure.get(), 9);

        EXPECT_EQ(jobTicket->pipelineOptions.get()->scaling.get()->xScalePercent.get(), 50);
        EXPECT_EQ(jobTicket->pipelineOptions.get()->scaling.get()->yScalePercent.get(), 50);
        EXPECT_EQ(jobTicket->pipelineOptions.get()->scaling.get()->scaleSelection.get(), dune::cdm::jobTicket_1::scaling::ScaleSelection::standardSizeScaling);
        EXPECT_EQ(jobTicket->pipelineOptions.get()->scaling.get()->scaleToSize.get(), dune::cdm::glossary_1::MediaSize::na_govt_dash_letter_8x10in);
        EXPECT_EQ(jobTicket->pipelineOptions.get()->scaling.get()->scaleToOutput.get(), dune::cdm::glossary_1::MediaSourceId::tray_dash_2);
    }
    else
    {
        CHECKPOINTA(" copyTicketAdapter_ deserialize failed");
    }

}

TEST_F(GivenANewCopyTicketAdapter, BasicSerializeDeserializeTestForStamp)
{
    CHECKPOINTC(" BasicSerializeDeserializeTestForStamp Entry");
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    std::vector<dune::cdm::overlay_1::scanStampLocation::stampContent::ItemTable> emptyContent{};
    EXPECT_TRUE(std::equal(
        jobTicket->pipelineOptions.get()->stampTopLeft.get()->stampContent.get().begin(),
        jobTicket->pipelineOptions.get()->stampTopLeft.get()->stampContent.get().end(),
        emptyContent.begin(),
        [](const dune::cdm::overlay_1::scanStampLocation::stampContent::ItemTable& lhs, const dune::cdm::overlay_1::scanStampLocation::stampContent::ItemTable& rhs) { 
            return lhs.stampId.get() == rhs.stampId.get(); 
    }));
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->locationId.get(), dune::cdm::overlay_1::StampLocation::topLeft);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->policy.get(), dune::cdm::overlay_1::StampPolicy::none);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->textColor.get(), dune::cdm::overlay_1::StampWatermarkTextColor::black);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->textFont.get(), dune::cdm::overlay_1::StampWatermarkTextFont::letterGothic);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->textSize.get(), dune::cdm::overlay_1::StampWatermarkTextSize::twelvePoint);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->startingPage.get(), 1);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->startingNumber.get(), 1);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->numberOfDigits.get(), 1);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->pageNumberingStyle.get(), dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle::number);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->whiteBackground.get(), dune::cdm::glossary_1::FeatureEnabled::false_);

    EXPECT_TRUE(std::equal(
        jobTicket->pipelineOptions.get()->stampTopLeft.get()->stampContent.get().begin(),
        jobTicket->pipelineOptions.get()->stampTopLeft.get()->stampContent.get().end(),
        emptyContent.begin(),
        [](const dune::cdm::overlay_1::scanStampLocation::stampContent::ItemTable& lhs, const dune::cdm::overlay_1::scanStampLocation::stampContent::ItemTable& rhs) { 
            return lhs.stampId.get() == rhs.stampId.get(); 
    }));
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->locationId.get(), dune::cdm::overlay_1::StampLocation::topLeft);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->policy.get(), dune::cdm::overlay_1::StampPolicy::none);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->textColor.get(), dune::cdm::overlay_1::StampWatermarkTextColor::black);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->textFont.get(), dune::cdm::overlay_1::StampWatermarkTextFont::letterGothic);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->textSize.get(), dune::cdm::overlay_1::StampWatermarkTextSize::twelvePoint);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->startingPage.get(), 1);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->startingNumber.get(), 1);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->numberOfDigits.get(), 1);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->pageNumberingStyle.get(), dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle::number);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->whiteBackground.get(), dune::cdm::glossary_1::FeatureEnabled::false_);

    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->locationId.getMutable() = dune::cdm::overlay_1::StampLocation::topLeft;
    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->policy.getMutable() = dune::cdm::overlay_1::StampPolicy::none;
    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->textColor.getMutable() = dune::cdm::overlay_1::StampWatermarkTextColor::yellow;
    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->textFont.getMutable() = dune::cdm::overlay_1::StampWatermarkTextFont::garamond;
    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->textSize.getMutable() = dune::cdm::overlay_1::StampWatermarkTextSize::twentyPoint;
    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->startingPage.getMutable() = 5;
    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->startingNumber.getMutable() = 5;
    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->numberOfDigits.getMutable() = 5;
    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->pageNumberingStyle.getMutable() = dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle::number;
    jobTicket->pipelineOptions.getMutable()->stampTopLeft.getMutable()->whiteBackground.getMutable() = dune::cdm::glossary_1::FeatureEnabled::false_;
   
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->locationId.getMutable() = dune::cdm::overlay_1::StampLocation::bottomLeft;
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->policy.getMutable() = dune::cdm::overlay_1::StampPolicy::none;
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->textColor.getMutable() = dune::cdm::overlay_1::StampWatermarkTextColor::purple;
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->textFont.getMutable() = dune::cdm::overlay_1::StampWatermarkTextFont::centurySchoolbook;
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->textSize.getMutable() = dune::cdm::overlay_1::StampWatermarkTextSize::twelvePoint;
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->startingPage.getMutable() = 3;
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->startingNumber.getMutable() = 3;
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->numberOfDigits.getMutable() = 3;
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->pageNumberingStyle.getMutable() = dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle::pagePlusNumber;
    jobTicket->pipelineOptions.getMutable()->stampBottomLeft.getMutable()->whiteBackground.getMutable() = dune::cdm::glossary_1::FeatureEnabled::true_;

    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    
    ASSERT_TRUE(success);
    jobTicket = copyTicketAdapter_->serializeIntoTable();

    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->locationId.get(), dune::cdm::overlay_1::StampLocation::topLeft);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->policy.get(), dune::cdm::overlay_1::StampPolicy::none);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->textColor.get(), dune::cdm::overlay_1::StampWatermarkTextColor::yellow);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->textFont.get(), dune::cdm::overlay_1::StampWatermarkTextFont::garamond);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->textSize.get(), dune::cdm::overlay_1::StampWatermarkTextSize::twentyPoint);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->startingPage.get(), 5);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->startingNumber.get(), 5);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->numberOfDigits.get(), 5);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->pageNumberingStyle.get(), dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle::number);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampTopLeft.get()->whiteBackground.get(), dune::cdm::glossary_1::FeatureEnabled::false_);

    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->locationId.get(), dune::cdm::overlay_1::StampLocation::bottomLeft);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->policy.get(), dune::cdm::overlay_1::StampPolicy::none);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->textColor.get(), dune::cdm::overlay_1::StampWatermarkTextColor::purple);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->textFont.get(), dune::cdm::overlay_1::StampWatermarkTextFont::centurySchoolbook);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->textSize.get(), dune::cdm::overlay_1::StampWatermarkTextSize::twelvePoint);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->startingPage.get(), 3);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->startingNumber.get(), 3);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->numberOfDigits.get(), 3);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->pageNumberingStyle.get(), dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle::pagePlusNumber);
    EXPECT_EQ(jobTicket->pipelineOptions.get()->stampBottomLeft.get()->whiteBackground.get(), dune::cdm::glossary_1::FeatureEnabled::true_);
}

TEST_F(GivenANewCopyTicketAdapter, BasicSerializeDeserializeTestForEnterprise)
{
    CHECKPOINTC(" BasicSerializeDeserializeTestForEnterprise Entry");
    copyJobTicket_->setPrePrintConfiguration(Product::ENTERPRISE);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    EXPECT_EQ(jobTicket->dest.get()->print.get()->customMediaXFeedDimension.get(), 0.0);
    EXPECT_EQ(jobTicket->dest.get()->print.get()->customMediaYFeedDimension.get(), 0.0);

    jobTicket->dest.getMutable()->print.getMutable()->customMediaXFeedDimension = 40000;
    jobTicket->dest.getMutable()->print.getMutable()->customMediaYFeedDimension = 70000;

    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    if (success)
    {
        jobTicket = copyTicketAdapter_->serializeIntoTable();

        EXPECT_EQ(jobTicket->dest.get()->print.get()->customMediaXFeedDimension.get(), 40000);
        EXPECT_EQ(jobTicket->dest.get()->print.get()->customMediaYFeedDimension.get(), 70000);
    }
}

TEST_F(GivenANewCopyTicketAdapter, WhenMarginsAreConstrained_ValueUpdatesIfIntentValueIsDifferent)
{
    copyJobTicket_->getConstraints()->addCopyMargins(dune::imaging::types::CopyMargins::ADDTOCONTENT);
    copyJobTicket_->getConstraints()->addCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    copyJobIntent_->setCopyMargins(dune::imaging::types::CopyMargins::ADDTOCONTENT);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.get()->print.get()->printMargins.get(), dune::cdm::jobTicket_1::PrintMargins::addToContents);
    bool isTicketModified = false;
    copyJobIntent_->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    EXPECT_EQ(copyJobIntent_->getCopyMargins(), dune::imaging::types::CopyMargins::CLIPCONTENT);
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(isTicketModified, true);
    EXPECT_EQ(copyJobIntent_->getCopyMargins(), dune::imaging::types::CopyMargins::ADDTOCONTENT);
}

TEST_F(GivenANewCopyTicketAdapter, WhenMarginsAreConstrained_ValueDoesNotUpdateIfIntentValueIsSame)
{
    copyJobTicket_->getConstraints()->addCopyMargins(dune::imaging::types::CopyMargins::ADDTOCONTENT);
    copyJobTicket_->getConstraints()->addCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    copyJobIntent_->setCopyMargins(dune::imaging::types::CopyMargins::ADDTOCONTENT);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.get()->print.get()->printMargins.get(), dune::cdm::jobTicket_1::PrintMargins::addToContents);
    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(copyJobIntent_->getCopyMargins(), dune::imaging::types::CopyMargins::ADDTOCONTENT);
}

TEST_F(GivenANewCopyTicketAdapter, WhenMediaDestinationIsConstrainted_ValueUpdatesIfIntentValueIsDifferent)
{
    copyJobTicket_->getConstraints()->addMediaDestinations(dune::imaging::types::MediaDestinationId::AUTOSELECT);
    copyJobIntent_->setOutputDestination(dune::imaging::types::MediaDestinationId::AUTOSELECT);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->mediaDestination.get(), dune::cdm::glossary_1::MediaDestinationId::auto_);
    bool isTicketModified = false;
    copyJobIntent_->setOutputDestination(dune::imaging::types::MediaDestinationId::ALTERNATE);
    EXPECT_EQ(copyJobIntent_->getOutputDestination(), dune::imaging::types::MediaDestinationId::ALTERNATE);
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(isTicketModified, true);
    EXPECT_EQ(copyJobIntent_->getOutputDestination(), dune::imaging::types::MediaDestinationId::AUTOSELECT);
}
TEST_F(GivenANewCopyTicketAdapter, WhenMediaDestinationIsConstrainted_ValueDoesNotUpdateIfIntentValueIsSame)
{
    copyJobTicket_->getConstraints()->addMediaDestinations(dune::imaging::types::MediaDestinationId::AUTOSELECT);
    copyJobIntent_->setOutputDestination(dune::imaging::types::MediaDestinationId::AUTOSELECT);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->mediaDestination.get(), dune::cdm::glossary_1::MediaDestinationId::auto_);
    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(copyJobIntent_->getOutputDestination(), dune::imaging::types::MediaDestinationId::AUTOSELECT);
}

TEST_F(GivenANewCopyTicketAdapter, WhenPrintingOrderConstraints_ValueUpdatesIfIntentValueIsDifferent)
{
    copyJobTicket_->getConstraints()->addPrintingOrder(dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
    copyJobIntent_->setPrintingOrder(dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->printingOrder.get(), dune::cdm::jobTicket_1::PrintingOrder::firstPageOnTop);
    bool isTicketModified = false;
    copyJobIntent_->setPrintingOrder(dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
    EXPECT_EQ(copyJobIntent_->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(isTicketModified, true);
    EXPECT_EQ(copyJobIntent_->getPrintingOrder(), dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
}

TEST_F(GivenANewCopyTicketAdapter, WhenPrintingOrderConstraints_ValueDoesNotUpdateIfIntentValueIsSame)
{
    copyJobTicket_->getConstraints()->addPrintingOrder(dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
    copyJobIntent_->setPrintingOrder(dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->printingOrder.get(), dune::cdm::jobTicket_1::PrintingOrder::firstPageOnTop);
    bool isTicketModified = false;
    copyJobIntent_->setPrintingOrder(dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(copyJobIntent_->getPrintingOrder(), dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
}

TEST_F(GivenANewCopyTicketAdapter, WhenSetRotateAngleIsConstrained_WithAutoRotateFalse)
{
    copyJobTicket_->getConstraints()->addAutoRotate(false);
    copyJobIntent_->setAutoRotate(false);
    copyJobIntent_->setRotation(90);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->rotate.get(), dune::cdm::jobTicket_1::Rotate::rotate90);
    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    if (success)
    {
        jobTicket = copyTicketAdapter_->serializeIntoTable();
        EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->rotate.get(), dune::cdm::jobTicket_1::Rotate::rotate90);
    }
}

TEST_F(GivenANewCopyTicketAdapter, WhenSetRotateAngleIsConstrained_WithAutoRotateTrue)
{
    copyJobTicket_->getConstraints()->addAutoRotate(true);
    copyJobIntent_->setAutoRotate(true);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->rotate.get(), dune::cdm::jobTicket_1::Rotate::auto_);
    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    if (success)
    {
        jobTicket = copyTicketAdapter_->serializeIntoTable();
        EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->rotate.get(), dune::cdm::jobTicket_1::Rotate::auto_);
    }
}
TEST_F(GivenANewCopyTicketAdapter, WhenMediaFamilyConstraints_ValueUpdatesIfIntentValueIsDifferent)
{
    copyJobTicket_->getConstraints()->addMediaFamily(dune::imaging::types::MediaFamily::CANVAS);
    copyJobIntent_->setMediaFamily(dune::imaging::types::MediaFamily::CANVAS);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->mediaFamily.get(), dune::cdm::mediaProfile_1::MediaFamily::canvas);
    bool isTicketModified = false;
    copyJobIntent_->setMediaFamily(dune::imaging::types::MediaFamily::ADHESIVE);
    EXPECT_EQ(copyJobIntent_->getMediaFamily(), dune::imaging::types::MediaFamily::ADHESIVE);
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(isTicketModified, true);
    EXPECT_EQ(copyJobIntent_->getMediaFamily(), dune::imaging::types::MediaFamily::CANVAS);
}

TEST_F(GivenANewCopyTicketAdapter, WhenMediaFamilyConstraints_ValueDoesNotUpdateIfIntentValueIsSame)
{
    copyJobTicket_->getConstraints()->addMediaFamily(dune::imaging::types::MediaFamily::CANVAS);
    copyJobIntent_->setMediaFamily(dune::imaging::types::MediaFamily::CANVAS);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->mediaFamily.get(), dune::cdm::mediaProfile_1::MediaFamily::canvas);
    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(copyJobIntent_->getMediaFamily(), dune::imaging::types::MediaFamily::CANVAS);
}

TEST_F(GivenANewCopyTicketAdapter, WhenStapleOptionConstraints_ValueUpdatesIfIntentValueIsDifferent)
{
    copyJobTicket_->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::BOTTOM_LEFT_ONE_POINT_ANGLED);
    copyJobIntent_->setStapleOption(dune::imaging::types::StapleOptions::BOTTOM_LEFT_ONE_POINT_ANGLED);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->stapleOption.get(), dune::cdm::jobTicket_1::StapleOptions::bottomLeftOnePointAngled);
    bool isTicketModified = false;
    copyJobIntent_->setStapleOption(dune::imaging::types::StapleOptions::BOTTOM_LEFT_ONE_POINT_ANY);
    EXPECT_EQ(copyJobIntent_->getStapleOption(), dune::imaging::types::StapleOptions::BOTTOM_LEFT_ONE_POINT_ANY);
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(isTicketModified, true);
    EXPECT_EQ(copyJobIntent_->getStapleOption(), dune::imaging::types::StapleOptions::BOTTOM_LEFT_ONE_POINT_ANGLED);
}

TEST_F(GivenANewCopyTicketAdapter, WhenStapleOptionConstraints_ValueDoesNotUpdateIfIntentValueIsSame)
{
    copyJobTicket_->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::BOTTOM_LEFT_ONE_POINT_ANGLED);
    copyJobIntent_->setStapleOption(dune::imaging::types::StapleOptions::BOTTOM_LEFT_ONE_POINT_ANGLED);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->stapleOption.get(), dune::cdm::jobTicket_1::StapleOptions::bottomLeftOnePointAngled);
    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(copyJobIntent_->getStapleOption(), dune::imaging::types::StapleOptions::BOTTOM_LEFT_ONE_POINT_ANGLED);
}

TEST_F(GivenANewCopyTicketAdapter, WhenPunchOptionConstraints_ValueUpdatesIfIntentValueIsDifferent)
{
    copyJobTicket_->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::BOTTOM_FOUR_POINT_DIN);
    copyJobIntent_->setPunchOption(dune::imaging::types::PunchingOptions::BOTTOM_FOUR_POINT_DIN);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->punchOption.get(), dune::cdm::jobTicket_1::PunchOptions::bottomFourPointDin);
    bool isTicketModified = false;
    copyJobIntent_->setPunchOption(dune::imaging::types::PunchingOptions::BOTTOM_TWO_POINT);
    EXPECT_EQ(copyJobIntent_->getPunchOption(), dune::imaging::types::PunchingOptions::BOTTOM_TWO_POINT);
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(isTicketModified, true);
    EXPECT_EQ(copyJobIntent_->getPunchOption(), dune::imaging::types::PunchingOptions::BOTTOM_FOUR_POINT_DIN);
}

TEST_F(GivenANewCopyTicketAdapter, WhenPunchOptionConstraints_ValueDoesNotUpdateIfIntentValueIsSame)
{
    copyJobTicket_->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::BOTTOM_FOUR_POINT_DIN);
    copyJobIntent_->setPunchOption(dune::imaging::types::PunchingOptions::BOTTOM_FOUR_POINT_DIN);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->punchOption.get(), dune::cdm::jobTicket_1::PunchOptions::bottomFourPointDin);
    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(copyJobIntent_->getPunchOption(), dune::imaging::types::PunchingOptions::BOTTOM_FOUR_POINT_DIN);
}

TEST_F(GivenANewCopyTicketAdapter, WhenDuplexBindingConstraintsWithDuplex_DuplexBindingSerializedWithIntent)
{
    copyJobTicket_->getConstraints()->addPlexBinding(dune::imaging::types::PlexBinding::LONG_EDGE);
    copyJobTicket_->getConstraints()->addPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobIntent_->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobIntent_->setOutputPlexBinding(dune::imaging::types::PlexBinding::LONG_EDGE);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->duplexBinding.get(), dune::cdm::glossary_1::DuplexBinding::twoSidedLongEdge);
}

TEST_F(GivenANewCopyTicketAdapter, WhenDuplexBindingConstraintsWithSimplex_DuplexBindingSerializedWithOneSided)
{
    copyJobTicket_->getConstraints()->addPlexBinding(dune::imaging::types::PlexBinding::SHORT_EDGE);
    copyJobTicket_->getConstraints()->addPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobIntent_->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    copyJobIntent_->setOutputPlexBinding(dune::imaging::types::PlexBinding::SHORT_EDGE);
    EXPECT_EQ(jobTicket->dest.getMutable()->print.get()->duplexBinding.get(), dune::cdm::glossary_1::DuplexBinding::oneSided);
    copyJobIntent_->setOutputPlexBinding(dune::imaging::types::PlexBinding::LONG_EDGE);
    EXPECT_EQ(copyJobIntent_->getOutputPlexBinding(), dune::imaging::types::PlexBinding::LONG_EDGE);
    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_EQ(success, true);
    EXPECT_EQ(isTicketModified, true);
    EXPECT_EQ(copyJobIntent_->getOutputPlexBinding(), dune::imaging::types::PlexBinding::ONE_SIDED);
}

TEST_F(GivenANewCopyTicketAdapter, UnitTest_getFallbackColorMode)
{
    // Set static constrains cache  to true
    copyTicketAdapter_->setLocaleProvider(mockLocaleProvider_.get());

    std::vector<dune::imaging::types::ColorMode> colorModes1 = {
        dune::imaging::types::ColorMode::COLOR,
        dune::imaging::types::ColorMode::MONOCHROME,
    };

    std::vector<dune::imaging::types::ColorMode> colorModes2 = {
        dune::imaging::types::ColorMode::COLOR,
        dune::imaging::types::ColorMode::MONOCHROME,
        dune::imaging::types::ColorMode::BLACKANDWHITE,
    };

    std::vector<dune::imaging::types::ColorMode> colorModes3 = {
        dune::imaging::types::ColorMode::COLOR,
        dune::imaging::types::ColorMode::BLACKANDWHITE,
        dune::imaging::types::ColorMode::MONOCHROME,
    };

    std::vector<dune::imaging::types::ColorMode> colorModes4 = {
        dune::imaging::types::ColorMode::COLOR,
        dune::imaging::types::ColorMode::GRAYSCALE,
        dune::imaging::types::ColorMode::MONOCHROME,
    };
    EXPECT_EQ(dune::imaging::types::ColorMode::MONOCHROME, copyTicketAdapter_->getFallbackColorMode(colorModes1));
    EXPECT_EQ(dune::imaging::types::ColorMode::MONOCHROME, copyTicketAdapter_->getFallbackColorMode(colorModes2));
    EXPECT_EQ(dune::imaging::types::ColorMode::BLACKANDWHITE, copyTicketAdapter_->getFallbackColorMode(colorModes3));
    EXPECT_EQ(dune::imaging::types::ColorMode::GRAYSCALE, copyTicketAdapter_->getFallbackColorMode(colorModes4));
}

TEST_F(GivenANewCopyTicketAdapter, WhenLocaleIsSetWithMetricUnits_OutputCanvasCustomAreInMm)
{
    // Set static constrains cache  to true
    copyTicketAdapter_->setLocaleProvider(mockLocaleProvider_.get());

    // Set values to outputCanvasCustomWidth and outputCanvasCustomLength
    dune::imaging::types::OutputCanvasT outputCanvas = dune::imaging::types::OutputCanvasT();
    outputCanvas.outputCanvasXExtent=2.6;
    outputCanvas.outputCanvasYExtent=2.6;
    copyJobIntent_->setOutputCanvas(outputCanvas);

    // Check the data stored in the ticketTable
    std::shared_ptr<JobTicketTable> jobTicketTable = copyTicketAdapter_->serializeIntoTable();
    ASSERT_DOUBLE_EQ(jobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get(), 66);
    ASSERT_DOUBLE_EQ(jobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomLength.get(), 66);
}

TEST_F(GivenANewCopyTicketAdapter, WhenLocaleIsSetWithImperialUnits_OutputCanvasCustomAreInMm)
{
    // Change to the imperial system of units
    EXPECT_CALL(*mockLocaleProvider_, getMeasurmentUnit()).WillRepeatedly(Return(dune::localization::MeasurementUnit::US));

    // Set static constrains cache  to true
    copyTicketAdapter_->setLocaleProvider(mockLocaleProvider_.get());

    // Set values to outputCanvasCustomWidth and outputCanvasCustomLength
    dune::imaging::types::OutputCanvasT outputCanvas = dune::imaging::types::OutputCanvasT();
    outputCanvas.outputCanvasXExtent=2.6;
    outputCanvas.outputCanvasYExtent=2.6;
    copyJobIntent_->setOutputCanvas(outputCanvas);

    // Check the data stored in the ticketTable
    std::shared_ptr<JobTicketTable> jobTicketTable = copyTicketAdapter_->serializeIntoTable();
    ASSERT_DOUBLE_EQ(jobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get(), 66.04);
    ASSERT_DOUBLE_EQ(jobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomLength.get(), 66.04);
}

TEST_F(GivenANewCopyTicketAdapter, WhenCopyTicketAdapterCreated_ThenCheckDataSource)
{
    EXPECT_EQ(copyJobTicket_->getDataSource(), dune::job::DataSource::SCANNER);
}

class GivenANewCopyTicketAdapterWithMockTicket : public ::testing::Test
{
public:
    GivenANewCopyTicketAdapterWithMockTicket() {}
    virtual void                                    SetUp() override;
    virtual void                                    TearDown() override;
    std::shared_ptr<MockICopyJobTicket>             mockICopyJobTicket_;
    std::shared_ptr<ICopyJobTicket>                 castICopyJobTicket_;
    MockIJobServiceFactory<MockICopyJobTicket>*     mockIJobService_;
    MockICopyAdapter*                               mockICopyAdapter_;
    CopyTicketAdapter*                              copyTicketAdapter_;
    std::shared_ptr<ICopyJobConstraints>            copyJobConstraints_{nullptr};
};

void GivenANewCopyTicketAdapterWithMockTicket::SetUp()
{
    CHECKPOINTA("GivenANewCopyTicketAdapterWithMockTicket::SetUp() Begin");
    mockICopyJobTicket_ = std::make_shared<MockICopyJobTicket>();
    mockICopyAdapter_ = new MockICopyAdapter();
    Uuid ticketID = Uuid::createUuid();
    // fill here any setInterface required
    mockIJobService_ = new MockIJobServiceFactory<MockICopyJobTicket>();

    // setup constraints expected on ticket
    copyJobConstraints_ = std::make_shared<CopyJobConstraint>();
    copyJobConstraints_->addCollate(dune::copy::SheetCollate::Collate);
    copyJobConstraints_->addCollate(dune::copy::SheetCollate::Uncollate);

    ON_CALL(*mockICopyJobTicket_,getConstraints()).WillByDefault(Return(copyJobConstraints_));

    castICopyJobTicket_ = dynamic_pointer_cast<ICopyJobTicket>(mockICopyJobTicket_);
    copyTicketAdapter_ = new CopyTicketAdapter(castICopyJobTicket_, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);
    ASSERT_NE(copyTicketAdapter_, nullptr);

    copyTicketAdapter_->setCopyConfigurationHelper(mockICopyAdapter_);
    CHECKPOINTA("GivenANewCopyTicketAdapterWithMockTicket::SetUp() End");
}

void GivenANewCopyTicketAdapterWithMockTicket::TearDown()
{
    delete copyTicketAdapter_;
    delete mockIJobService_;
    delete mockICopyAdapter_;
}

TEST_F(GivenANewCopyTicketAdapterWithMockTicket, WhenSerializeIntoTableIsCalledWithValidSecurityContextAndColorCopyEnabled_ThenColorModeDoesNotChange)
{
    auto intent = std::make_shared<CopyJobIntent>();
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    dune::security::ac::SecurityContextBuilder scb;
    scb.addPermission(Permission::CP_COPY_COLOR);
    std::shared_ptr<dune::security::ac::ISecurityContext> securityContext = std::move(scb.build());

    EXPECT_CALL(*mockICopyJobTicket_, getIntent()).WillRepeatedly(Return(intent));
    EXPECT_CALL(*mockICopyJobTicket_, getTicketId()).WillRepeatedly(Return(Uuid::createUuid()));
    EXPECT_CALL(*mockICopyJobTicket_, getSecurityContext()).WillRepeatedly(Return(securityContext));
    EXPECT_CALL(*mockICopyAdapter_, getColorCopyEnabled()).WillOnce(Return(true));

    auto jobTicketTable = copyTicketAdapter_->serializeIntoTable();
    ASSERT_EQ(intent->getColorMode(), dune::imaging::types::ColorMode::COLOR);
    EXPECT_EQ(jobTicketTable->src.getMutable()->scan.getMutable()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::color);
}

TEST_F(GivenANewCopyTicketAdapterWithMockTicket, WhenSerializeIntoTableIsCalledWithValidSecurityContextAndColorCopyDisabled_ThenColorModeIsGrayscale)
{
    auto intent = std::make_shared<CopyJobIntent>();
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    dune::security::ac::SecurityContextBuilder scb;
    scb.addPermission(Permission::CP_COPY_COLOR);
    std::shared_ptr<dune::security::ac::ISecurityContext> securityContext = std::move(scb.build());

    EXPECT_CALL(*mockICopyJobTicket_, getIntent()).WillRepeatedly(Return(intent));
    EXPECT_CALL(*mockICopyJobTicket_, getTicketId()).WillRepeatedly(Return(Uuid::createUuid()));
    EXPECT_CALL(*mockICopyJobTicket_, getSecurityContext()).WillRepeatedly(Return(securityContext));
    EXPECT_CALL(*mockICopyAdapter_, getColorCopyEnabled()).WillOnce(Return(false));

    auto jobTicketTable = copyTicketAdapter_->serializeIntoTable();
    ASSERT_EQ(intent->getColorMode(), dune::imaging::types::ColorMode::GRAYSCALE);
    EXPECT_EQ(jobTicketTable->src.getMutable()->scan.getMutable()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::grayscale);
}

TEST_F(GivenANewCopyTicketAdapterWithMockTicket, WhenSerializeIntoTableIsCalledWithSecurityContextWithoutCorrectPermissions_ThenColorModeIsGrayscale)
{
    auto intent = std::make_shared<CopyJobIntent>();
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    dune::security::ac::SecurityContextBuilder scb;
    std::shared_ptr<dune::security::ac::ISecurityContext> securityContext = std::move(scb.build());

    // setup constraints expected on ticket
    copyJobConstraints_ = std::make_shared<CopyJobConstraint>();
    copyJobConstraints_->addCollate(dune::copy::SheetCollate::Collate);
    copyJobConstraints_->addCollate(dune::copy::SheetCollate::Uncollate);
    ON_CALL(*mockICopyJobTicket_,getConstraints()).WillByDefault(Return(copyJobConstraints_));

    EXPECT_CALL(*mockICopyJobTicket_, getIntent()).WillRepeatedly(Return(intent));
    EXPECT_CALL(*mockICopyJobTicket_, getTicketId()).WillRepeatedly(Return(Uuid::createUuid()));
    EXPECT_CALL(*mockICopyJobTicket_, getSecurityContext()).WillRepeatedly(Return(securityContext));

    auto jobTicketTable = copyTicketAdapter_->serializeIntoTable();
    ASSERT_EQ(intent->getColorMode(), dune::imaging::types::ColorMode::GRAYSCALE);
    EXPECT_EQ(jobTicketTable->src.getMutable()->scan.getMutable()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::grayscale);
}

TEST_F(GivenANewCopyTicketAdapterWithMockTicket, WhenSerializeIntoTableIsCalledWithSecurityContextWithCorrectOutplutPlexPermissions_ThenOuputPLexIsSet)
{
    auto intent = std::make_shared<CopyJobIntent>();
    intent->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setOutputPlexBinding(dune::imaging::types::PlexBinding::LONG_EDGE);
    dune::security::ac::SecurityContextBuilder scb;
    scb.addPermission(Permission::CP_COPY_ONE_SIDED);
    std::shared_ptr<dune::security::ac::ISecurityContext> securityContext = std::move(scb.build());

    copyJobConstraints_ = std::make_shared<CopyJobConstraint>();
    copyJobConstraints_->addPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobConstraints_->addPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ON_CALL(*mockICopyJobTicket_,getConstraints()).WillByDefault(Return(copyJobConstraints_));

    EXPECT_CALL(*mockICopyJobTicket_, getIntent()).WillRepeatedly(Return(intent));
    EXPECT_CALL(*mockICopyJobTicket_, getSecurityContext()).WillRepeatedly(Return(securityContext));
    
    auto jobTicketTable = copyTicketAdapter_->serializeIntoTable();

    // Check if duplexBinding is set correctly when permissions are present
    EXPECT_EQ(jobTicketTable->dest.get()->print.get()->plexMode.get(), dune::cdm::glossary_1::PlexMode::simplex);
}

TEST_F(GivenANewCopyTicketAdapterWithMockTicket, WhenSerializeIntoTableIsCalledWithSecurityContextWithoutCorrectOutplutPlexPermissions_ThenOuputPlexIsNotSet)
{
    auto intent = std::make_shared<CopyJobIntent>();
    intent->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setOutputPlexBinding(dune::imaging::types::PlexBinding::LONG_EDGE);
    dune::security::ac::SecurityContextBuilder scb;
    std::shared_ptr<dune::security::ac::ISecurityContext> securityContext = std::move(scb.build());

    copyJobConstraints_ = std::make_shared<CopyJobConstraint>();
    copyJobConstraints_->addPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobConstraints_->addPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ON_CALL(*mockICopyJobTicket_,getConstraints()).WillByDefault(Return(copyJobConstraints_));
    
    EXPECT_CALL(*mockICopyJobTicket_, getIntent()).WillRepeatedly(Return(intent));
    EXPECT_CALL(*mockICopyJobTicket_, getSecurityContext()).WillRepeatedly(Return(securityContext));
    
    auto jobTicketTable = copyTicketAdapter_->serializeIntoTable();
    // Check if duplexBinding falls back to one-sided
    EXPECT_EQ(jobTicketTable->dest.get()->print.get()->plexMode.get(), dune::cdm::glossary_1::PlexMode::duplex);
}

TEST_F(GivenANewCopyTicketAdapterWithMockTicket, WhenSerializeIntoTableIsCalledWithRestrictPrintValidSecurityAndCopyColorEnabled_ThenColorModeIsGrayscale)
{
    auto intent = std::make_shared<CopyJobIntent>();
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    dune::security::ac::SecurityContextBuilder scb;
    scb.addPermission(Permission::CP_COPY_COLOR);
    std::shared_ptr<dune::security::ac::ISecurityContext> securityContext = std::move(scb.build());

    EXPECT_CALL(*mockICopyJobTicket_, getIntent()).WillRepeatedly(Return(intent));
    EXPECT_CALL(*mockICopyJobTicket_, getTicketId()).WillRepeatedly(Return(Uuid::createUuid()));
    EXPECT_CALL(*mockICopyJobTicket_, getSecurityContext()).WillRepeatedly(Return(securityContext));
    EXPECT_CALL(*mockICopyJobTicket_, isRestrictColorPrint()).WillRepeatedly(Return(true));
    

    auto jobTicketTable = copyTicketAdapter_->serializeIntoTable();
    ASSERT_EQ(intent->getColorMode(), dune::imaging::types::ColorMode::GRAYSCALE);
    EXPECT_EQ(jobTicketTable->src.getMutable()->scan.getMutable()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::grayscale);
}

TEST_F(GivenANewCopyTicketAdapterWithMockTicket, WhenSerializeIntoTableIsCalledWithoutRestrictingPrintValidSecurityAndCopyColorEnabled_ThenColorModeIsColor)
{
    auto intent = std::make_shared<CopyJobIntent>();
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    dune::security::ac::SecurityContextBuilder scb;
    scb.addPermission(Permission::CP_COPY_COLOR);
    std::shared_ptr<dune::security::ac::ISecurityContext> securityContext = std::move(scb.build());

    EXPECT_CALL(*mockICopyJobTicket_, getIntent()).WillRepeatedly(Return(intent));
    EXPECT_CALL(*mockICopyJobTicket_, getTicketId()).WillRepeatedly(Return(Uuid::createUuid()));
    EXPECT_CALL(*mockICopyJobTicket_, getSecurityContext()).WillRepeatedly(Return(securityContext));
    EXPECT_CALL(*mockICopyJobTicket_, isRestrictColorPrint()).WillRepeatedly(Return(false));
    EXPECT_CALL(*mockICopyAdapter_, getColorCopyEnabled()).WillOnce(Return(true));


    auto jobTicketTable = copyTicketAdapter_->serializeIntoTable();
    ASSERT_EQ(intent->getColorMode(), dune::imaging::types::ColorMode::COLOR);
    EXPECT_EQ(jobTicketTable->src.getMutable()->scan.getMutable()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::color);
}

class GivenANewCopyTicketAdapterWithConstraintsMocked : public ::testing::Test
{
public:
    GivenANewCopyTicketAdapterWithConstraintsMocked() {}
    virtual void                                    SetUp() override;
    virtual void                                    TearDown() override;

    /**
     * @brief Get the Color Mode Constraints object
     * @return std::shared_ptr<Constraints> constraint result
     */
    std::shared_ptr<Constraints> getColorModeConstraints();

    /**
     * @brief Get the Color Mode Constraints object
     * @param supportedColorModes expected supported color modes
     * @return std::shared_ptr<Constraints> constraint result
     */
    std::shared_ptr<Constraints> getColorModeConstraints(std::vector<dune::cdm::jobTicket_1::ColorModes> supportedColorModes);

    /**
     * @brief Get the Prompt For Additional Pages Constraints object
     * @return std::shared_ptr<Constraints> constraint result
     */
    std::shared_ptr<Constraints> getPromptForAdditionalPagesConstraints();

    std::shared_ptr<ICopyJobTicket>                 copyJobTicket_;
    std::shared_ptr<ICopyJobIntent>                 copyJobIntent_;
    MockIJobServiceFactory<MockICopyJobTicket>*     mockIJobService_;
    CopyTicketAdapter*                              copyTicketAdapter_;
    std::shared_ptr<ConstraintsGroup> staticConstraints_{nullptr};
    std::shared_ptr<MockIJobConstraints>            copyJobConstraints_{nullptr};
    std::shared_ptr<MockICopyJobDynamicConstraintRules>  copyJobDynamicConstraints_{nullptr};

};

void GivenANewCopyTicketAdapterWithConstraintsMocked::SetUp()
{
    copyJobTicket_ = std::make_shared<CopyJobTicket>();
    copyJobIntent_ = copyJobTicket_->getIntent();
    Uuid ticketID = Uuid::createUuid();
    // fill here any setInterface required
    mockIJobService_ = new MockIJobServiceFactory<MockICopyJobTicket>();
    copyTicketAdapter_ = new CopyTicketAdapter(copyJobTicket_, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);
    ASSERT_NE(copyTicketAdapter_, nullptr);

    // constructor of constraint mocks
    copyJobConstraints_ = std::make_shared<MockIJobConstraints>();
    copyJobDynamicConstraints_ = std::make_shared<MockICopyJobDynamicConstraintRules>();

    // Create constraints return
    staticConstraints_ = std::make_shared<ConstraintsGroup>();
    auto constraints = getColorModeConstraints();
    staticConstraints_->set("src/scan/colorMode", constraints);

    // return default of get constraints
    ON_CALL(*copyJobConstraints_,getConstraints(_,_)).WillByDefault(Return(staticConstraints_));
    ON_CALL(*copyJobDynamicConstraints_,getDynamicConstraints(_,_,_)).WillByDefault(Return(staticConstraints_));

    copyTicketAdapter_->setCopyJobConstraintsHelper(copyJobConstraints_.get());
    copyTicketAdapter_->setCopyDynamicConstraintsHelper(copyJobDynamicConstraints_.get());
}

void GivenANewCopyTicketAdapterWithConstraintsMocked::TearDown()
{
    delete copyTicketAdapter_;
    delete mockIJobService_;
}

std::shared_ptr<Constraints> GivenANewCopyTicketAdapterWithConstraintsMocked::getColorModeConstraints()
{
    return getColorModeConstraints({dune::cdm::jobTicket_1::ColorModes::color, dune::cdm::jobTicket_1::ColorModes::grayscale});
}

std::shared_ptr<Constraints> GivenANewCopyTicketAdapterWithConstraintsMocked::getColorModeConstraints(std::vector<dune::cdm::jobTicket_1::ColorModes> supportedColorModes)
{
    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::ColorModes>>(supportedColorModes,
                                        &dune::cdm::jobTicket_1::ColorModes::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>>(supportedColorModes, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> GivenANewCopyTicketAdapterWithConstraintsMocked::getPromptForAdditionalPagesConstraints()
{
    auto constraints = std::make_shared<Constraints>();

    std::vector<dune::cdm::glossary_1::FeatureEnabledEnum> possibleValuesPromptForAdditionalPages;
    auto enumPossibleValueConstraint =
            std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::FeatureEnabledEnum>>(possibleValuesPromptForAdditionalPages, &dune::cdm::glossary_1::FeatureEnabledEnum::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    constraints->add(std::make_unique<dune::framework::data::constraints::Lock>(string_id::cUnavailable));

    return constraints;
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenCallToDeserializeAndCopyJobDynamicIsCalledToForceApplyAValue_ThenCopyJobTicketWillChange)
{
    // Ticket table with unsupported value
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    jobTicket->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::monochrome;

    // test action of first check and apply force work, second return false to deserialize only one time
    EXPECT_CALL(*copyJobDynamicConstraints_,checkAndApplyForceSets(_,_,_,_))
        // First color iteration return color
        .WillOnce(testing::WithArg<0>(testing::Invoke(
        [&] (const std::shared_ptr<JobTicketTable>& updatedJobTicketTable)
        {
            updatedJobTicketTable->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::color;
            return true;
        })));

    bool isTicketModified = false;
    // Check that current value is monochrome
    EXPECT_EQ(jobTicket->src.getMutable()->scan.getMutable()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::monochrome);
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));

    // Check that deserialize actions goes well, and new value is as Force Sets copyJobDynamicConstraints_ is as expected
    EXPECT_TRUE(success);
    EXPECT_TRUE(isTicketModified);
    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::COLOR);
    EXPECT_EQ(jobTicket->src.getMutable()->scan.getMutable()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::color);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked,
    WhenCallToDeserializeAndCustomScallingAnd2Up_ThenDeserilizeShouldSuccess)
{
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->xScalePercent = 50;
    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->yScalePercent = 50;
    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->scaleSelection =
        dune::cdm::jobTicket_1::scaling::ScaleSelection::custom;
    jobTicket->pipelineOptions.getMutable()->imageModifications.getMutable()->pagesPerSheet =
        dune::cdm::jobTicket_1::PagesPerSheet::oneUp;

    jobTicket = copyTicketAdapter_->serializeIntoTable();
    jobTicket->pipelineOptions.getMutable()->scaling.getMutable()->scaleSelection =
        dune::cdm::jobTicket_1::scaling::ScaleSelection::none;
    jobTicket->pipelineOptions.getMutable()->imageModifications.getMutable()->pagesPerSheet =
        dune::cdm::jobTicket_1::PagesPerSheet::twoUp;

    bool isTicketModified = false;
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));
    EXPECT_TRUE(success);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenCallToDeserializeAndPromptForAdditionalPagesIsContrainedForBookMode_ThenDeserializeShouldFail)
{
    auto promptForAdditionalPagesConstraints = getPromptForAdditionalPagesConstraints();
    staticConstraints_->set("pipelineOptions/promptForAdditionalPages", promptForAdditionalPagesConstraints);

    copyJobIntent_->setPromptForMorePages(true);
    copyJobIntent_->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    bool isTicketModified = false;

    std::tuple<bool, dune::ws::cdm::ErrorItemT> response = copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified);
    bool deserializeResponse = std::get<0>(response);
    dune::ws::cdm::ErrorItemT errorDetails = std::get<1>(response);

    ASSERT_FALSE(deserializeResponse);
    ASSERT_EQ(errorDetails.code, "setValueError");
    ASSERT_EQ(errorDetails.message, "promptForAdditionalPages value cannot be set if it is constrained");
    ASSERT_EQ(copyJobIntent_->getScanCaptureMode(), dune::scan::types::ScanCaptureModeType::BOOKMODE);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenCallToDeserializeAndPromptForAdditionalPagesIsNotConstrainedAndSettingValueIsFalseForBookMode_ThenDeserializeShouldSuccess)
{
    copyJobIntent_->setPromptForMorePages(false);
    copyJobIntent_->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    bool isTicketModified = false;

    std::tuple<bool, dune::ws::cdm::ErrorItemT> response = copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified);
    bool deserializeResponse = std::get<0>(response);

    ASSERT_TRUE(deserializeResponse);
    ASSERT_EQ(copyJobIntent_->getScanCaptureMode(), dune::scan::types::ScanCaptureModeType::BOOKMODE);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenCallToDeserializeAndPromptForAdditionalPagesIsContrainedForIDCardMode_ThenDeserializeShouldFail)
{
    auto promptForAdditionalPagesConstraints = getPromptForAdditionalPagesConstraints();
    staticConstraints_->set("pipelineOptions/promptForAdditionalPages", promptForAdditionalPagesConstraints);

    copyJobIntent_->setPromptForMorePages(true);
    copyJobIntent_->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    bool isTicketModified = false;

    std::tuple<bool, dune::ws::cdm::ErrorItemT> response = copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified);
    bool deserializeResponse = std::get<0>(response);
    dune::ws::cdm::ErrorItemT errorDetails = std::get<1>(response);

    ASSERT_FALSE(deserializeResponse);
    ASSERT_EQ(errorDetails.code, "setValueError");
    ASSERT_EQ(errorDetails.message, "promptForAdditionalPages value cannot be set if it is constrained");
    ASSERT_EQ(copyJobIntent_->getScanCaptureMode(), dune::scan::types::ScanCaptureModeType::IDCARD);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenCallToDeserializeAndPromptForAdditionalPagesIsNotConstrainedAndSettingValueIsFalseForIDCardMode_ThenDeserializeShouldSuccess)
{
    copyJobIntent_->setPromptForMorePages(false);
    copyJobIntent_->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    bool isTicketModified = false;

    std::tuple<bool, dune::ws::cdm::ErrorItemT> response = copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified);
    bool deserializeResponse = std::get<0>(response);

    ASSERT_TRUE(deserializeResponse);
    ASSERT_EQ(copyJobIntent_->getScanCaptureMode(), dune::scan::types::ScanCaptureModeType::IDCARD);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenCallToDeserializeAndPromptForAdditionalPagesIsNotContrainedForStandardMode_ThenDeserializeShouldSuccess)
{
    copyJobIntent_->setPromptForMorePages(true);
    copyJobIntent_->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::STANDARD);
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    bool isTicketModified = false;

    std::tuple<bool, dune::ws::cdm::ErrorItemT> response = copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified);
    bool deserializeResponse = std::get<0>(response);

    ASSERT_TRUE(deserializeResponse);
    ASSERT_EQ(copyJobIntent_->getScanCaptureMode(), dune::scan::types::ScanCaptureModeType::STANDARD);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenDeserializingPlex_ThenConstraintsGetRecalculated)
{
    // Ticket table with unsupported value
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicket = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    jobTicket->dest = dune::cdm::jobTicket_1::jobTicket::DestTable();
    jobTicket->dest.getMutable()->print = dune::cdm::jobTicket_1::PrintTable();
    jobTicket->dest.getMutable()->print.getMutable()->plexMode = dune::cdm::glossary_1::PlexMode::duplex;
    copyJobTicket_->getConstraints()->addPlexMode(dune::imaging::types::Plex::DUPLEX);
    copyJobTicket_->getConstraints()->addPlexMode(dune::imaging::types::Plex::SIMPLEX);

    ON_CALL(*copyJobDynamicConstraints_, getDynamicConstraints(_,_,_)).WillByDefault(Return(staticConstraints_));

    // currently called 2x inside 'deserializeFromTable()', should be called 1x more when plexMode is set
    EXPECT_CALL(*copyJobDynamicConstraints_, getDynamicConstraints(_,_,_)).Times(3);

    bool isTicketModified = false;
    // Check that current value is monochrome
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));

    // Check that deserialize actions goes well, and new value is as Force Sets copyJobDynamicConstraints_ is as
    // expected
    EXPECT_TRUE(success);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked,WhenDeserializeIsCalledAndStaticFlagIsSupportedTrue_ThenDeserializationGoesWellAndGetDynamicConstraintIsCalledTwoTimes)
{
    // Ticket table with unsupported value
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    // Set static constrains as cached and force to get a set of constraints saved on ConstraintGroup
    copyTicketAdapter_->setStaticConstrainsAreCached(true);
    copyTicketAdapter_->getConstraints();
    EXPECT_CALL(*copyJobDynamicConstraints_,checkAndApplyForceSets(_,_,_,_)).WillOnce(Return(false));

    // Check that on exercise from deserialize table, only dynamic constraint is called one time, when
    EXPECT_CALL(*copyJobConstraints_,getConstraints(_,_)).Times(0);
    EXPECT_CALL(*copyJobDynamicConstraints_,getDynamicConstraints(_,_,_)).WillOnce(Return(staticConstraints_));

    bool isTicketModified = false;
    // Check that current value is monochrome
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));

    // Check that deserialize actions goes well
    EXPECT_TRUE(success);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked,WhenDeserializeIsCalledAndStaticFlagIsSupportedTrueAndCheckAndApplyForceIsRequestedOneTime_ThenDeserializationGoesWellAndGetDynamicConstraintIsCalledOnlyOneTime)
{
    // Ticket table with unsupported value
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    // Set static constrains as cached and force to get a set of constraints saved on ConstraintGroup
    copyTicketAdapter_->setStaticConstrainsAreCached(true);
    copyTicketAdapter_->getConstraints();
    EXPECT_CALL(*copyJobDynamicConstraints_,checkAndApplyForceSets(_,_,_,_)).WillOnce(Return(true));

    // Check that on exercise from deserialize table, only dynamic constraint is called one time, when
    EXPECT_CALL(*copyJobConstraints_,getConstraints(_,_)).Times(0);
    EXPECT_CALL(*copyJobDynamicConstraints_,getDynamicConstraints(_,_,_)).Times(2).WillRepeatedly(Return(staticConstraints_));

    bool isTicketModified = false;
    // Check that current value is monochrome
    bool success = std::get<0>(copyTicketAdapter_->deserializeFromTable(jobTicket, isTicketModified));

    // Check that deserialize actions goes well
    EXPECT_TRUE(success);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenGetConstraintIsCalledWithStaticConstraintCached_ThenConstraintAreReceivedButComponentsAreNotCalled)
{
    // Ticket table with unsupported value
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    // Set static constrains as cached and force to get a set of constraints saved on ConstraintGroup
    copyTicketAdapter_->setStaticConstrainsAreCached(true);
    copyTicketAdapter_->getConstraints();

    // Check that on exercise from deserialize table, no components are called
    EXPECT_CALL(*copyJobConstraints_,getConstraints(_,_)).Times(0);
    EXPECT_CALL(*copyJobDynamicConstraints_,getDynamicConstraints(_,_,_)).Times(0);

    // Call to Getter
    auto constraints = copyTicketAdapter_->getConstraints();
    EXPECT_NE(constraints, nullptr);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenGetConstraintIsCalledWithStaticConstraintNotCached_ThenConstraintAreReceivedButComponentsAreNotCalled)
{
    // Ticket table with unsupported value
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    // Check that on exercise from deserialize table, only dynamic constraint is called one time
    EXPECT_CALL(*copyJobConstraints_,getConstraints(_,_)).WillOnce(Return(staticConstraints_));
    EXPECT_CALL(*copyJobDynamicConstraints_,getDynamicConstraints(_,_,_)).WillOnce(Return(staticConstraints_));

    // Call to Getter
    auto constraints = copyTicketAdapter_->getConstraints();
    EXPECT_NE(constraints, nullptr);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenGetConstraintIsCalledWithoutDynamicConstraint_ThenConstraintAreReceivedButComponentsAreNotCalled)
{
    // Ticket table with unsupported value
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();

    // Check that on exercise from deserialize table, only dynamic constraint is called one time
    EXPECT_CALL(*copyJobConstraints_,getConstraints(_,_)).WillOnce(Return(staticConstraints_));
    ON_CALL(*copyJobDynamicConstraints_,getDynamicConstraints(_,_,_)).WillByDefault(Return(nullptr));

    // Call to Getter
    auto constraints = copyTicketAdapter_->getConstraints();
    EXPECT_NE(constraints, nullptr);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, 
    WhenSerializeIsCalledAndValidateTicketOnSerializationIsTrue_ThenAFirstDeserializationIsCalledForAdjustTicket)
{
    // Check that on exercise from deserialize table, only dynamic constraint is called one time
    copyTicketAdapter_->setValidateTicketOnSerialization(true);
    EXPECT_CALL(*copyJobConstraints_,getConstraints(_,_)).WillRepeatedly(Return(staticConstraints_));
    auto dynamicConstraints = std::make_shared<ConstraintsGroup>();
    auto constraints = getColorModeConstraints({dune::cdm::jobTicket_1::ColorModes::grayscale});
    dynamicConstraints->set("src/scan/colorMode", constraints);
    EXPECT_CALL(*copyJobDynamicConstraints_,getDynamicConstraints(_,_,_)).WillRepeatedly(Return(dynamicConstraints));
    EXPECT_CALL(*copyJobDynamicConstraints_,checkAndApplyForceSets(_,_,_,_))
        // First color iteration return color
        .WillOnce(testing::WithArg<0>(testing::Invoke(
        [&] (const std::shared_ptr<JobTicketTable>& updatedJobTicketTable)
        {
            updatedJobTicketTable->src = dune::cdm::jobTicket_1::jobTicket::SrcTable();
            updatedJobTicketTable->src.getMutable()->scan = dune::cdm::jobTicket_1::ScanTable();
            updatedJobTicketTable->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::grayscale;
            return true;
        })));

    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::COLOR);

    // Ticket table with supported value as dynamic constraint expected
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_NE(jobTicket, nullptr);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::grayscale);
    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::GRAYSCALE);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenSerializeIsCalledAndValidateTicketOnSerializationIsFalse_ThenTicketIsNotAdjustedBeforeDeserialize)
{
    // Check that on exercise from deserialize table, only dynamic constraint is called one time
    EXPECT_CALL(*copyJobConstraints_,getConstraints(_,_)).Times(0);
    auto dynamicConstraints = std::make_shared<ConstraintsGroup>();
    auto constraints = getColorModeConstraints({dune::cdm::jobTicket_1::ColorModes::grayscale});
    dynamicConstraints->set("src/scan/colorMode", constraints);
    EXPECT_CALL(*copyJobDynamicConstraints_,getDynamicConstraints(_,_,_)).Times(0);
    EXPECT_CALL(*copyJobDynamicConstraints_,checkAndApplyForceSets(_,_,_,_)).Times(0);

    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::COLOR);

    // Ticket table with supported value as dynamic constraint expected
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_NE(jobTicket, nullptr);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::color);
    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::COLOR);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, 
    WhenSerializeIsCalledWithStaticConstraintsCachedAndValidateTicketOnSerializationIsTrue_ThenAFirstDeserializationIsCalledForAdjustTicket)
{
    // Check that on exercise from deserialize table, only dynamic constraint is called one time
    copyTicketAdapter_->setValidateTicketOnSerialization(true);
    copyTicketAdapter_->setStaticConstrainsAreCached(true);
    EXPECT_CALL(*copyJobConstraints_,getConstraints(_,_)).WillOnce(Return(staticConstraints_));
    auto dynamicConstraints = std::make_shared<ConstraintsGroup>();
    auto constraints = getColorModeConstraints({dune::cdm::jobTicket_1::ColorModes::grayscale});
    dynamicConstraints->set("src/scan/colorMode", constraints);
    EXPECT_CALL(*copyJobDynamicConstraints_,getDynamicConstraints(_,_,_)).Times(2).WillRepeatedly(Return(dynamicConstraints));
    EXPECT_CALL(*copyJobDynamicConstraints_,checkAndApplyForceSets(_,_,_,_))
        // First color iteration return color
        .WillOnce(testing::WithArg<0>(testing::Invoke(
        [&] (const std::shared_ptr<JobTicketTable>& updatedJobTicketTable)
        {
            updatedJobTicketTable->src = dune::cdm::jobTicket_1::jobTicket::SrcTable();
            updatedJobTicketTable->src.getMutable()->scan = dune::cdm::jobTicket_1::ScanTable();
            updatedJobTicketTable->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::grayscale;
            return true;
        })));

    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::COLOR);

    // Ticket table with supported value as dynamic constraint expected
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    EXPECT_NE(jobTicket, nullptr);
    EXPECT_EQ(jobTicket->src.get()->scan.get()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::grayscale);
    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::GRAYSCALE);
}

TEST_F(GivenANewCopyTicketAdapter, WhenPrintPropertiesAreConstrained_SupportsPropertyReturnsTrue)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    copyJobTicket->getConstraints()->setMaxRotation(0);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/printMargins"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/mediaType"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/duplexBinding"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/mediaDestination"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/printingOrder"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/rotate"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/mediaFamily"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/colorMode"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/plexMode"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/collate"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/printQuality"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/stapleOption"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/punchOption"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/foldOption"));
    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/bookletMakerOption"));

    copyJobTicket->getConstraints()->addCopyMargins(dune::imaging::types::CopyMargins::ADDTOCONTENT);
    copyJobTicket->getConstraints()->addCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/printMargins"));

    CopyJobMediaSupportedType mediaSupportedType;
    mediaSupportedType.addId(dune::imaging::types::MediaIdType::STATIONERY);
    vector<dune::imaging::types::MediaSource> mediaSources = {dune::imaging::types::MediaSource::TRAY1, dune::imaging::types::MediaSource::TRAY2 };
    mediaSupportedType.addSupportedMediaSource(mediaSources);
    std::vector<dune::imaging::types::Plex> plexes = {dune::imaging::types::Plex::SIMPLEX, dune::imaging::types::Plex::DUPLEX };
    mediaSupportedType.addDuplex(plexes);
    copyJobTicket->getConstraints()->addMediaSupportedType(mediaSupportedType);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/mediaType"));


    copyJobTicket->getConstraints()->addPlexBinding(dune::imaging::types::PlexBinding::LONG_EDGE);
    copyJobTicket->getConstraints()->addPlexBinding(dune::imaging::types::PlexBinding::SHORT_EDGE);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/duplexBinding"));

    copyJobTicket->getConstraints()->addMediaDestinations(dune::imaging::types::MediaDestinationId::BIN);
    copyJobTicket->getConstraints()->addMediaDestinations(dune::imaging::types::MediaDestinationId::AUTOSELECT);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/mediaDestination"));

    copyJobTicket->getConstraints()->addPrintingOrder(dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
    copyJobTicket->getConstraints()->addPrintingOrder(dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/printingOrder"));

    copyJobTicket->getConstraints()->setMaxRotation(270);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/rotate"));

    copyJobTicket->getConstraints()->addMediaFamily(dune::imaging::types::MediaFamily::CANVAS );
    copyJobTicket->getConstraints()->addMediaFamily(dune::imaging::types::MediaFamily::FILM );
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/mediaFamily"));

    copyJobTicket->getConstraints()->addAutoRotate(true);
    copyJobTicket->getConstraints()->addAutoRotate(false);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/autoRotate"));

    copyJobTicket->getConstraints()->addPlexMode(dune::imaging::types::Plex::SIMPLEX);
    copyJobTicket->getConstraints()->addPlexMode(dune::imaging::types::Plex::DUPLEX);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/plexMode"));

    copyJobTicket->getConstraints()->addCollate(dune::copy::SheetCollate::Collate);
    copyJobTicket->getConstraints()->addCollate(dune::copy::SheetCollate::Uncollate);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/collate"));

    copyJobTicket->getConstraints()->addPrintQuality(dune::imaging::types::PrintQuality::DRAFT);
    copyJobTicket->getConstraints()->addPrintQuality(dune::imaging::types::PrintQuality::NORMAL);
    copyJobTicket->getConstraints()->addPrintQuality(dune::imaging::types::PrintQuality::BEST);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/printQuality"));

    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY);
    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::TOP_LEFT_ONE_POINT_ANGLED);
    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::RIGHT_TWO_POINTS);
    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::TOP_TWO_POINTS);
    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::BOTTOM_TWO_POINTS);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/stapleOption"));

    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::LEFT_TWO_POINT_DIN);
    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::BOTTOM_TWO_POINT_DIN);
    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::LEFT_FOUR_POINT_DIN);
    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::LEFT_TWO_POINT_US);
    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::TOP_FOUR_POINT_SWD);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/punchOption"));

    copyJobTicket->getConstraints()->addFoldOption(dune::imaging::types::FoldingOptions::C_INWARD_TOP);
    copyJobTicket->getConstraints()->addFoldOption(dune::imaging::types::FoldingOptions::V_INWARD_TOP);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/foldOption"));
    
    copyJobTicket->getConstraints()->addBookletMakerOption(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/bookletMakerOption"));
}



TEST_F(GivenANewCopyTicketAdapter, WhenPrintPrintMediaSourceIsConfigured_SupportsPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/mediaSource"));

    copyJobTicket->getConstraints()->addMediaPrintSupportedSource(dune::imaging::types::MediaSource::ROLL1);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/mediaSource"));
}

TEST_F(GivenANewCopyTicketAdapter, WhenMediaSupportedStuffIsConfigured_SupportsPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/mediaSource"));

    copyJobTicket->getConstraints()->addMediaSupportedSize(dune::copy::Jobs::Copy::CopyJobMediaSupportedSize());
    copyJobTicket->getConstraints()->addMediaSupportedType(dune::copy::Jobs::Copy::CopyJobMediaSupportedType());
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/mediaSource"));
}

TEST_F(GivenANewCopyTicketAdapter, WhenStapleOptionIsConfigured_SupportsPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/stapleOption"));

    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY);
    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::TOP_LEFT_ONE_POINT_ANGLED);
    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::RIGHT_TWO_POINTS);
    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::TOP_TWO_POINTS);
    copyJobTicket->getConstraints()->addStapleOption(dune::imaging::types::StapleOptions::BOTTOM_TWO_POINTS);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/stapleOption"));
}

TEST_F(GivenANewCopyTicketAdapter, WhenPunchOptionIsConfigured_SupportsPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/punchOption"));

    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::LEFT_TWO_POINT_DIN);
    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::BOTTOM_TWO_POINT_DIN);
    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::LEFT_FOUR_POINT_DIN);
    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::LEFT_TWO_POINT_US);
    copyJobTicket->getConstraints()->addPunchOption(dune::imaging::types::PunchingOptions::TOP_FOUR_POINT_SWD);
    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/punchOption"));
}

TEST_F(GivenANewCopyTicketAdapter, WhenBookletMakerOptionIsConfigured_SupportsPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/bookletMakerOption"));

    copyJobTicket->getConstraints()->addBookletMakerOption(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);

    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/bookletMakerOption"));
}

/* Enterprise */
TEST_F(GivenANewCopyTicketAdapter, WhenCustomMediaXDimensionIsConfiguredAndEnterprise_SupportPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaXFeedDimension"));
    copyJobTicket->setPrePrintConfiguration(Product::ENTERPRISE);

    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/customMediaXFeedDimension"));
}

TEST_F(GivenANewCopyTicketAdapter, WhenCustomMediaYDimensionIsConfiguredAndEnterprise_SupportPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaYFeedDimension"));
    copyJobTicket->setPrePrintConfiguration(Product::ENTERPRISE);

    EXPECT_EQ(true, copyTicketAdapter->supportsProperty("dest/print/customMediaYFeedDimension"));
}

/* Homepro */
TEST_F(GivenANewCopyTicketAdapter, WhenCustomMediaXDimensionIsConfiguredAndHomepro_SupportPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaXFeedDimension"));
    copyJobTicket->setPrePrintConfiguration(Product::HOME_PRO);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaXFeedDimension"));
}

TEST_F(GivenANewCopyTicketAdapter, WhenCustomMediaYDimensionIsConfiguredAndHomepro_SupportPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaYFeedDimension"));
    copyJobTicket->setPrePrintConfiguration(Product::HOME_PRO);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaYFeedDimension"));
}

/* LFP */
TEST_F(GivenANewCopyTicketAdapter, WhenCustomMediaXDimensionIsConfiguredAndDesignjet_SupportPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaXFeedDimension"));
    copyJobTicket->setPrePrintConfiguration(Product::LFP);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaXFeedDimension"));
}

TEST_F(GivenANewCopyTicketAdapter, WhenCustomMediaYDimensionIsConfiguredAndDesignjet_SupportPropertyReturnsCorrectly)
{
    std::shared_ptr<ICopyJobTicket>     copyJobTicket = std::make_shared<CopyJobTicket>();
    std::shared_ptr<CopyTicketAdapter>  copyTicketAdapter = std::make_shared<CopyTicketAdapter>(copyJobTicket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService_);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaYFeedDimension"));
    copyJobTicket->setPrePrintConfiguration(Product::LFP);

    EXPECT_EQ(false, copyTicketAdapter->supportsProperty("dest/print/customMediaYFeedDimension"));
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenDeserializeFromTableWithRulesIsCalledWithValidTable_ThenDeserializationSucceeds)
{
    // Setup the job ticket with valid values
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    jobTicket->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::color;
    
    // Set expectations for dynamic constraints - allow multiple calls with Times(AnyNumber())
    EXPECT_CALL(*copyJobDynamicConstraints_, checkAndApplyForceSets(_, _, _, _))
        .WillOnce(Return(false));
    
    EXPECT_CALL(*copyJobDynamicConstraints_, getDynamicConstraints(_, _, _))
        .WillRepeatedly(Return(staticConstraints_));
    
    // Call the method under test
    bool isTicketModified = false;
    auto result = copyTicketAdapter_->deserializeFromTableWithRules(jobTicket, isTicketModified);
    
    // Verify the results
    EXPECT_TRUE(std::get<0>(result));
    EXPECT_TRUE(isTicketModified);
    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::COLOR);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenDeserializeFromTableWithRulesIsCalledWithInvalidValue_ThenDeserializationFails)
{
    // Setup the job ticket with an invalid color mode value
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    jobTicket->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::monochrome;

    // set color mode constraints to only allow color and grayscale
    auto colorConstraints = getColorModeConstraints({dune::cdm::jobTicket_1::ColorModes::color, dune::cdm::jobTicket_1::ColorModes::grayscale});
    staticConstraints_->set("src/scan/colorMode", colorConstraints);
    
    // Also add prompt for additional pages constraints that fail validation
    auto promptConstraints = getPromptForAdditionalPagesConstraints();
    staticConstraints_->set("pipelineOptions/promptForAdditionalPages", promptConstraints);
    jobTicket->pipelineOptions.getMutable()->promptForAdditionalPages = dune::cdm::glossary_1::FeatureEnabled::true_;
    
    // Set expectations for dynamic constraints - allow multiple calls
    EXPECT_CALL(*copyJobDynamicConstraints_, checkAndApplyForceSets(_, _, _, _))
        .WillOnce(Return(false)); // No forced changes
    
    EXPECT_CALL(*copyJobDynamicConstraints_, getDynamicConstraints(_, _, _))
        .WillRepeatedly(Return(staticConstraints_));
    
    // Call the method under test
    bool isTicketModified = false;
    auto result = copyTicketAdapter_->deserializeFromTableWithRules(jobTicket, isTicketModified);
    
    // Verify the results - should fail on first constraint violation
    EXPECT_FALSE(std::get<0>(result));
    EXPECT_NE(std::get<1>(result).code, "");
    // The first error reported should be either colorMode or promptForAdditionalPages
    EXPECT_TRUE(std::get<1>(result).message.find("colorMode") != std::string::npos || 
               std::get<1>(result).message.find("promptForAdditionalPages") != std::string::npos);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenDeserializeFromTableWithRulesIsCalledWithSkipValidation_ThenUsesDefaultValues)
{
    // Setup the job ticket with an invalid value
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    jobTicket->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::monochrome;
    
    // Set up color mode constraints to only allow color and grayscale
    auto colorConstraints = getColorModeConstraints({dune::cdm::jobTicket_1::ColorModes::color, dune::cdm::jobTicket_1::ColorModes::grayscale});
    staticConstraints_->set("src/scan/colorMode", colorConstraints);
    
    // Create a default intent with grayscale color mode
    auto defaultIntent = std::make_shared<CopyJobIntent>();
    defaultIntent->setColorMode(dune::imaging::types::ColorMode::GRAYSCALE);
    
    // Set expectations for dynamic constraints - allow multiple calls
    EXPECT_CALL(*copyJobDynamicConstraints_, checkAndApplyForceSets(_, _, _, _))
        .WillOnce(Return(false)); // No forced changes
    
    EXPECT_CALL(*copyJobDynamicConstraints_, getDynamicConstraints(_, _, _))
        .WillRepeatedly(Return(staticConstraints_));
    
    // Call the method under test with skipValidationErrorReport = true and default intent
    bool isTicketModified = false;
    auto result = copyTicketAdapter_->deserializeFromTableWithRules(jobTicket, isTicketModified, true, defaultIntent);
    
    // Verify the results - should succeed and use default value
    EXPECT_TRUE(std::get<0>(result));
    EXPECT_TRUE(isTicketModified);
    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::GRAYSCALE);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenDeserializeFromTableWithRulesAppliesForcedChanges_ThenTicketIsModified)
{
    // Setup the job ticket
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    
    // Set original values to compare after the test
    jobTicket->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::color;
    jobTicket->src.getMutable()->scan.getMutable()->resolution = dune::cdm::jobTicket_1::Resolutions::e200Dpi;
    
    // Set expectations for dynamic constraints - force a change to just color mode
    EXPECT_CALL(*copyJobDynamicConstraints_, checkAndApplyForceSets(_, _, _, _))
        .WillOnce(testing::WithArg<0>(testing::Invoke(
            [&](const std::shared_ptr<JobTicketTable>& updatedTable) {
                // Force change only color mode to grayscale
                updatedTable->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::grayscale;
                return true; // Changes were made
            })));
    
    EXPECT_CALL(*copyJobDynamicConstraints_, getDynamicConstraints(_, _, _))
        .WillRepeatedly(Return(staticConstraints_));
    
    // Call the method under test
    bool isTicketModified = false;
    auto result = copyTicketAdapter_->deserializeFromTableWithRules(jobTicket, isTicketModified);
    
    // Verify the results
    EXPECT_TRUE(std::get<0>(result));
    EXPECT_TRUE(isTicketModified);
    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::GRAYSCALE);
    
    // Resolution should remain unchanged from what was in the jobTicket
    EXPECT_EQ(dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
              copyTicketAdapter_->serializeIntoTable()->src.get()->scan.get()->resolution.get());
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenDeserializeFromTableWithRulesIsCalledWithNullConstraints_ThenUsesExistingConstraints)
{
    // Setup the job ticket with valid values
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    jobTicket->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::color;
    
    // Set expectations for dynamic constraints
    EXPECT_CALL(*copyJobDynamicConstraints_, checkAndApplyForceSets(_, _, _, _))
        .WillOnce(Return(false)); // No forced changes needed
    
    // Return a null constraints pointer to simulate missing dynamic constraints
    EXPECT_CALL(*copyJobDynamicConstraints_, getDynamicConstraints(_, _, _))
        .WillRepeatedly(Return(nullptr));
    
    // Make sure static constraints are still used
    EXPECT_CALL(*copyJobConstraints_, getConstraints(_, _))
        .WillRepeatedly(Return(staticConstraints_));
    
    // Call the method under test
    bool isTicketModified = false;
    auto result = copyTicketAdapter_->deserializeFromTableWithRules(jobTicket, isTicketModified);
    
    // Verify the results - should still succeed using static constraints
    EXPECT_TRUE(std::get<0>(result));
    EXPECT_TRUE(isTicketModified);
    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::COLOR);
}

TEST_F(GivenANewCopyTicketAdapterWithConstraintsMocked, WhenDeserializeFromTableWithRulesIsCalledWithPartialForcedUpdates_ThenPartiallyUpdatesTicket)
{
    // Setup the job ticket
    auto jobTicket = copyTicketAdapter_->serializeIntoTable();
    
    // Set original values to compare after the test
    jobTicket->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::color;
    jobTicket->src.getMutable()->scan.getMutable()->resolution = dune::cdm::jobTicket_1::Resolutions::e200Dpi;
    
    // Set expectations for dynamic constraints - force a change to just color mode
    EXPECT_CALL(*copyJobDynamicConstraints_, checkAndApplyForceSets(_, _, _, _))
        .WillOnce(testing::WithArg<0>(testing::Invoke(
            [&](const std::shared_ptr<JobTicketTable>& updatedTable) {
                // Force change only color mode to grayscale
                updatedTable->src.getMutable()->scan.getMutable()->colorMode = dune::cdm::jobTicket_1::ColorModes::grayscale;
                return true; // Changes were made
            })));
    
    EXPECT_CALL(*copyJobDynamicConstraints_, getDynamicConstraints(_, _, _))
        .WillRepeatedly(Return(staticConstraints_));
    
    // Call the method under test
    bool isTicketModified = false;
    auto result = copyTicketAdapter_->deserializeFromTableWithRules(jobTicket, isTicketModified);
    
    // Verify the results
    EXPECT_TRUE(std::get<0>(result));
    EXPECT_TRUE(isTicketModified);
    EXPECT_EQ(copyJobIntent_->getColorMode(), dune::imaging::types::ColorMode::GRAYSCALE);
    
    // Resolution should remain unchanged from what was in the jobTicket
    EXPECT_EQ(dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
              copyTicketAdapter_->serializeIntoTable()->src.get()->scan.get()->resolution.get());
}
