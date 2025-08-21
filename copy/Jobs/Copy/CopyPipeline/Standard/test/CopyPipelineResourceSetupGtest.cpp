///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineResourceSetupGtest.cpp
 * @author Shubham Khandelwal
 * @date   25-04-2021
 * @brief  unit Test for the copy pipeline resource setup method
 *
 * (C) Copyright 2019 HP Inc.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ConstraintsGroup.h"
#include "CopyPipelineTestFixture.h"
#include "GTestConfigHelper.h"
#include "MockICopyJobTicket.h"
#include "MockILayoutFilterIntent.h"
#include "MockIMediaHandlingMgr.h"
// #include "MediaInputCapabilities.h"
#include "MockIScannerMedia.h"
#include "MockIDateTime.h"
#include "MockIPrint.h"
#include "MockICapabilitiesFactory.h"
#include "Capabilities.h"
#include "MockIJobQueue.h"
#include "MockIPrintIntentsFactory.h"
#include "MockIJob.h"

using namespace dune::copy::Jobs::Copy;

using ::testing::Matcher;

using MockIMediaHandlingMgr         = dune::print::mediaHandlingAssets::MockIMediaHandlingMgr;
using IInputList                    = dune::scan::scanningsystem::IMedia::IInputList;
using MockIMediaPath                = dune::scan::scanningsystem::MockIMediaPath;
using MockIPrintIntentsFactory      = dune::print::engine::MockIPrintIntentsFactory;

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class GivenCopyPipelineResourcesSetup : public GivenCopyPipelineResources
{
  public:
    GivenCopyPipelineResourcesSetup(){};

    virtual void SetUp() override;

    virtual void TearDown() override;

    std::shared_ptr<CopyPipelineResourceSetup> copyPipelineResourceSetup;
    std::shared_ptr<MockIScanDeviceIntent> scanDeviceIntent_ = std::make_shared<MockIScanDeviceIntent>();
    std::shared_ptr<MockIImagePersisterIntent> imagePersisterIntent_ = std::make_shared<MockIImagePersisterIntent>();
    std::shared_ptr<MockIImageRetrieverIntent> imageRetrieverIntent_ = std::make_shared<MockIImageRetrieverIntent>();
    std::shared_ptr<MockIPrintDeviceIntent> printDeviceIntent_ = std::make_shared<MockIPrintDeviceIntent>();
    std::shared_ptr<MockIPageAssemblerIntent> pageAssemblerIntent_ = std::make_shared<MockIPageAssemblerIntent>();
    std::shared_ptr<MockIMarkingFilterIntent> markingFilterIntent_ = std::make_shared<MockIMarkingFilterIntent>();
    std::shared_ptr<MockIMarkingFilterSettings> markingFilterSettings_ = std::make_shared<MockIMarkingFilterSettings>();
    std::shared_ptr<MockILayoutFilterIntent>    layoutFilterIntent_ = std::make_shared<MockILayoutFilterIntent>();
    std::shared_ptr<MockIImageProcessorIntent> imageProcessorIntent_ = std::make_shared<MockIImageProcessorIntent>();
    std::shared_ptr<MockIScannerCapabilities> scannerCapabilities_ = std::make_shared<MockIScannerCapabilities>();
    std::shared_ptr<MockIIntentsManager> mockIntentsManager_ = std::make_shared<MockIIntentsManager>();
    std::shared_ptr<dune::scan::Jobs::Scan::ScanPipelineConfigT> scanPipelineConfig_ = std::make_shared<dune::scan::Jobs::Scan::ScanPipelineConfigT>();
    std::shared_ptr<MockIIPADeviceIntents> ipaDeviceIntent_ = std::make_shared<MockIIPADeviceIntents>();
    std::shared_ptr<MockIMediaHandlingMgr> mockIMediaHandlingMgr_ = std::make_shared<MockIMediaHandlingMgr>();
    std::shared_ptr<dune::print::engine::MockIPrint> mockIPrint_ = std::make_shared<dune::print::engine::MockIPrint>();
    std::shared_ptr<dune::print::engine::MockICapabilitiesFactory> mockICapabilitiesFactory_ = std::make_shared<dune::print::engine::MockICapabilitiesFactory>();
    std::shared_ptr<MockIJobQueue> mockIJobQueue_ = std::make_shared<MockIJobQueue>();
    std::shared_ptr<MockIPrintIntentsFactory> mockIPrintIntentsFactory_ = std::make_shared<MockIPrintIntentsFactory>();
};

void GivenCopyPipelineResourcesSetup::SetUp()
{
    services_.imagePersister = static_cast<IImagePersister*>(imagePersister_.get());
    services_.imageProcessor = static_cast<IImageProcessor *>(imageProcessor_.get());
    services_.markingFilterService = static_cast<IMarkingFilter *>(markingFilter_.get());
    services_.layoutFilterService = static_cast<ILayoutFilter *>(layoutFilter_.get());
    services_.rtpFilterService = static_cast<IResourceService*>(rtpFilterService_.get());
    services_.printDevice = static_cast<IPrintDevice*>(printDevice_.get());
    services_.pageAssembler = static_cast<IPageAssembler*>(pageAssembler_.get());

    services_.resourceManager = managerClient_.get();
    services_.scanDeviceService = static_cast<IScanDevice *>(scanDeviceService_.get());
    services_.imageRetrieverService = imageRetrieverService_.get();
    services_.colorDirector = colorDirector_.get();
    services_.mediaAttributes = mediaAttributes_.get();
    services_.mediaInterface = mediaInterface_.get();
    services_.mediaInfo = mediaInfoInterface_.get();
    services_.mediaHandlingSettings = mediaSettingsInterface_.get();
    services_.intentsManager = mockIntentsManager_.get();
    services_.printEngine = mockIPrint_.get();
    services_.engineCapabilitiesFactory = mockICapabilitiesFactory_.get();
    services_.jobQueue = mockIJobQueue_.get();
    services_.printIntentsFactory = mockIPrintIntentsFactory_.get();

    maxLengthConfig_.scanMaxCm = 8000;

    ON_CALL(*mediaInterface_, getMargins(_))
        .WillByDefault(Return(std::tuple<APIResult, Margins>(APIResult::OK, desiredMargins_)));
    ON_CALL(*scanPipeline_, getScanPipelineConfiguration()).WillByDefault(Return(scanPipelineConfig_));
    ON_CALL(*mediaAttributes_, getColdResetMediaSize()).WillByDefault(Return(static_cast<uint32_t>(dune::imaging::types::MediaSizeId::LETTER)));

    dune::print::engine::IMedia::InputList inputs;
    auto mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();
    inputs.push_back(mockIMediaIInput);
    ON_CALL(*mediaInterface_, getInputDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));
}

void GivenCopyPipelineResourcesSetup::TearDown(){}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalled_ForHomePro)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = false;
    scanPipelineConfig_->imageQuality = false;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);

    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &addborderRequired](bool value) -> void {

                addborderRequired = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_)).Times(0);

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))

        .WillRepeatedly(

            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    dune::imaging::types::PrintScaleT printScaleTable;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_)).Times(0);

    bool clipOverSize{false};
    EXPECT_CALL(*imageProcessorIntent_, setClipOversize(_)).Times(0);

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_)).Times(0);
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(addborderRequired, false);
    EXPECT_EQ(useImageQuality, false);
    EXPECT_EQ(edgeRemoval, false);
    EXPECT_EQ(autoDeskew, intent->getAutoDeskew());
    EXPECT_EQ(threshold, false);
    EXPECT_EQ(clipOverSize, false);
    EXPECT_EQ(imageRotation, true);
    EXPECT_EQ(specificPadding.overridePadding, false);
    EXPECT_EQ(specificPadding.topPad, 0);
    EXPECT_EQ(specificPadding.bottomPad, 0);
    EXPECT_EQ(specificPadding.leftPad, 0);
    EXPECT_EQ(specificPadding.rightPad, 0);
    EXPECT_EQ(specificRotation.overrideRotation, false);
    EXPECT_EQ(specificRotation.rotation, 0);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(printScaleTable.xScalePercent, 0);
    EXPECT_EQ(printScaleTable.yScalePercent, 0);
    EXPECT_EQ(printScaleTable.scaleSelection, dune::imaging::types::PrintScaleSelection::NONE);
    EXPECT_EQ(printScaleTable.scaleToOutput, dune::imaging::types::MediaSource::AUTOSELECT);
    EXPECT_EQ(printScaleTable.scaleToSize, dune::imaging::types::MediaSizeId::ANY);
    EXPECT_EQ(printScaleTable.upScaleStrategy, dune::imaging::types::ScaleStrategy::UNKNOWN);
    EXPECT_EQ(printScaleTable.downScaleStrategy, dune::imaging::types::ScaleStrategy::UNKNOWN);


    if(scanPipelineConfig_->imageQuality)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_MANUAL);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->mediaIdType, dune::imaging::types::MediaIdType::CUSTOM);
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->backgroundDensity, intent->getBackgroundColorRemovalLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());

    }

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalled_ForHomeSmb)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = false;
    scanPipelineConfig_->imageQuality = false;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);

    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &addborderRequired](bool value) -> void {

                addborderRequired = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_)).Times(0);

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))

        .WillRepeatedly(

            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    dune::imaging::types::PrintScaleT printScaleTable;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_)).Times(0);

    bool clipOverSize{false};
    EXPECT_CALL(*imageProcessorIntent_, setClipOversize(_)).Times(0);

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_)).Times(0);
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(addborderRequired, false);
    EXPECT_EQ(useImageQuality, false);
    EXPECT_EQ(edgeRemoval, false);
    EXPECT_EQ(autoDeskew, intent->getAutoDeskew());
    EXPECT_EQ(threshold, false);
    EXPECT_EQ(clipOverSize, false);
    EXPECT_EQ(imageRotation, true);
    EXPECT_EQ(specificPadding.overridePadding, false);
    EXPECT_EQ(specificPadding.topPad, 0);
    EXPECT_EQ(specificPadding.bottomPad, 0);
    EXPECT_EQ(specificPadding.leftPad, 0);
    EXPECT_EQ(specificPadding.rightPad, 0);
    EXPECT_EQ(specificRotation.overrideRotation, false);
    EXPECT_EQ(specificRotation.rotation, 0);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(printScaleTable.xScalePercent, 0);
    EXPECT_EQ(printScaleTable.yScalePercent, 0);
    EXPECT_EQ(printScaleTable.scaleSelection, dune::imaging::types::PrintScaleSelection::NONE);
    EXPECT_EQ(printScaleTable.scaleToOutput, dune::imaging::types::MediaSource::AUTOSELECT);
    EXPECT_EQ(printScaleTable.scaleToSize, dune::imaging::types::MediaSizeId::ANY);

    if(scanPipelineConfig_->imageQuality)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_MANUAL);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->mediaIdType, dune::imaging::types::MediaIdType::CUSTOM);
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->backgroundDensity, intent->getBackgroundColorRemovalLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());

    }

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalled_ForHomeSmbWithPagerPerSheet2)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = false;
    scanPipelineConfig_->imageQuality = false;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &addborderRequired](bool value) -> void {

                addborderRequired = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &specificRotation](dune::imaging::Resources::SpecificRotation value) -> void {

                specificRotation = value;

            }));

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))

        .WillRepeatedly(

            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    dune::imaging::types::PrintScaleT printScaleTable;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_))

        .WillRepeatedly(

            testing::Invoke([this, &printScaleTable](dune::imaging::types::PrintScaleT value) -> void {

                printScaleTable = value;

            }));

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(addborderRequired, false);
    EXPECT_EQ(useImageQuality, false);
    EXPECT_EQ(edgeRemoval, false);
    EXPECT_EQ(autoDeskew, intent->getAutoDeskew());
    EXPECT_EQ(threshold, false);
    EXPECT_EQ(imageRotation, true);
    EXPECT_EQ(specificRotation.overrideRotation, true);
    EXPECT_EQ(specificRotation.rotation, 90);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(printScaleTable.xScalePercent, 0);
    EXPECT_EQ(printScaleTable.yScalePercent, 0);
    EXPECT_EQ(printScaleTable.scaleSelection, dune::imaging::types::PrintScaleSelection::NONE);
    EXPECT_EQ(printScaleTable.scaleToOutput, dune::imaging::types::MediaSource::AUTOSELECT);
    EXPECT_EQ(printScaleTable.scaleToSize, dune::imaging::types::MediaSizeId::ANY);

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalled_ForEnterprise)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = false;
    scanPipelineConfig_->imageQuality = false;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    intent->setXScalePercent(230);

    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &addborderRequired](bool value) -> void {

                addborderRequired = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_)).Times(0);

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))

        .WillRepeatedly(

            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    dune::imaging::types::PrintScaleT printScaleTable;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_)).Times(0);

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_)).Times(0);
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(addborderRequired, false);
    EXPECT_EQ(useImageQuality, false);
    EXPECT_EQ(edgeRemoval, false);
    EXPECT_EQ(autoDeskew, intent->getAutoDeskew());
    EXPECT_EQ(threshold, false);
    EXPECT_EQ(imageRotation, false);
    EXPECT_EQ(specificPadding.overridePadding, false);
    EXPECT_EQ(specificPadding.topPad, 0);
    EXPECT_EQ(specificPadding.bottomPad, 0);
    EXPECT_EQ(specificPadding.leftPad, 0);
    EXPECT_EQ(specificPadding.rightPad, 0);
    EXPECT_EQ(specificRotation.overrideRotation, false);
    EXPECT_EQ(specificRotation.rotation, 0);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(printScaleTable.xScalePercent, 0);
    EXPECT_EQ(printScaleTable.yScalePercent, 0);
    EXPECT_EQ(printScaleTable.scaleSelection, dune::imaging::types::PrintScaleSelection::NONE);
    EXPECT_EQ(printScaleTable.scaleToOutput, dune::imaging::types::MediaSource::AUTOSELECT);
    EXPECT_EQ(printScaleTable.scaleToSize, dune::imaging::types::MediaSizeId::ANY);

    if(scanPipelineConfig_->imageQuality)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_MANUAL);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->mediaIdType, dune::imaging::types::MediaIdType::CUSTOM);
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->backgroundDensity, intent->getBackgroundColorRemovalLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());

    }

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalled_ForLFP)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = true;
    scanPipelineConfig_->imageQuality = true;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::MDF);
    intent->setColorMode(ColorMode::BLACKANDWHITE);
    intent->setBackgroundColorRemoval(true);

    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &addborderRequired](bool value) -> void {

                addborderRequired = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_)).Times(0);

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))

        .WillRepeatedly(

            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    dune::imaging::types::PrintScaleT printScaleTable;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_))
        .WillRepeatedly(

            testing::Invoke([this, &printScaleTable](dune::imaging::types::PrintScaleT  value) -> void {

                printScaleTable = value;

            }));

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    bool detectOriginalScanSize{false};
    EXPECT_CALL(*imageProcessorIntent_, setDetectOriginalScanSize(_))
        .WillRepeatedly(
            testing::Invoke([this, &detectOriginalScanSize](bool value) -> void {
                detectOriginalScanSize = value;
            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))

        .WillRepeatedly(

            testing::Invoke([this, &iqTable](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> value) -> void {

                iqTable = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::LFP, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->upScaleStrategy =  dune::imaging::types::ScaleStrategy::QUADRATIC;
    resourceConfig->downScaleStrategy =  dune::imaging::types::ScaleStrategy::QUADRATIC;
    resourceConfig->detectOriginalScanSize = true;
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(addborderRequired, true);
    EXPECT_EQ(useImageQuality, true);
    EXPECT_EQ(edgeRemoval, true);
    EXPECT_EQ(autoDeskew, intent->getAutoDeskew());
    EXPECT_EQ(threshold, false);
    EXPECT_EQ(imageRotation, true);
    EXPECT_EQ(specificPadding.overridePadding, false);
    EXPECT_EQ(specificPadding.topPad, 0);
    EXPECT_EQ(specificPadding.bottomPad, 0);
    EXPECT_EQ(specificPadding.leftPad, 0);
    EXPECT_EQ(specificPadding.rightPad, 0);
    EXPECT_EQ(specificRotation.overrideRotation, false);
    EXPECT_EQ(specificRotation.rotation, 0);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(printScaleTable.xScalePercent, intent->getXScalePercent());
    EXPECT_EQ(printScaleTable.yScalePercent, intent->getYScalePercent());
    EXPECT_EQ(printScaleTable.scaleToOutput, intent->getScaleToOutput());
    EXPECT_EQ(printScaleTable.scaleToSize, intent->getScaleToSize());
    EXPECT_EQ(printScaleTable.upScaleStrategy, dune::imaging::types::ScaleStrategy::QUADRATIC);
    EXPECT_EQ(printScaleTable.downScaleStrategy, dune::imaging::types::ScaleStrategy::QUADRATIC);
    EXPECT_EQ(detectOriginalScanSize, true);

    if(scanPipelineConfig_->imageQuality)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_AUTOCTX);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->backgroundDensity, intent->getBackgroundColorRemovalLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());

    }

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalledWithAmmoniaForLFP_ThenBackgroundRemoval)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = true;
    scanPipelineConfig_->imageQuality = true;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::MDF);
    intent->setColorMode(ColorMode::BLACKANDWHITE);
    intent->setOriginalMediaType(dune::scan::types::OriginalMediaType::DARK_BLUEPRINTS);
    intent->setBackgroundColorRemoval(true);

    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &addborderRequired](bool value) -> void {

                addborderRequired = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_)).Times(0);

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))

        .WillRepeatedly(

            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    dune::imaging::types::PrintScaleT printScaleTable;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_))
        .WillRepeatedly(

            testing::Invoke([this, &printScaleTable](dune::imaging::types::PrintScaleT  value) -> void {

                printScaleTable = value;

            }));

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    bool detectOriginalScanSize{false};
    EXPECT_CALL(*imageProcessorIntent_, setDetectOriginalScanSize(_))
        .WillRepeatedly(
            testing::Invoke([this, &detectOriginalScanSize](bool value) -> void {
                detectOriginalScanSize = value;
            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))

        .WillRepeatedly(

            testing::Invoke([this, &iqTable](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> value) -> void {

                iqTable = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::LFP, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->upScaleStrategy =  dune::imaging::types::ScaleStrategy::QUADRATIC;
    resourceConfig->downScaleStrategy =  dune::imaging::types::ScaleStrategy::QUADRATIC;
    resourceConfig->detectOriginalScanSize = true;
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(addborderRequired, true);
    EXPECT_EQ(useImageQuality, true);
    EXPECT_EQ(edgeRemoval, true);
    EXPECT_EQ(autoDeskew, intent->getAutoDeskew());
    EXPECT_EQ(threshold, false);
    EXPECT_EQ(imageRotation, true);
    EXPECT_EQ(specificPadding.overridePadding, false);
    EXPECT_EQ(specificPadding.topPad, 0);
    EXPECT_EQ(specificPadding.bottomPad, 0);
    EXPECT_EQ(specificPadding.leftPad, 0);
    EXPECT_EQ(specificPadding.rightPad, 0);
    EXPECT_EQ(specificRotation.overrideRotation, false);
    EXPECT_EQ(specificRotation.rotation, 0);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(printScaleTable.xScalePercent, intent->getXScalePercent());
    EXPECT_EQ(printScaleTable.yScalePercent, intent->getYScalePercent());
    EXPECT_EQ(printScaleTable.scaleToOutput, intent->getScaleToOutput());
    EXPECT_EQ(printScaleTable.scaleToSize, intent->getScaleToSize());
    EXPECT_EQ(printScaleTable.upScaleStrategy, dune::imaging::types::ScaleStrategy::QUADRATIC);
    EXPECT_EQ(printScaleTable.downScaleStrategy, dune::imaging::types::ScaleStrategy::QUADRATIC);
    EXPECT_EQ(detectOriginalScanSize, true);

    if(scanPipelineConfig_->imageQuality)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_AUTOCTX);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->backgroundDensity, intent->getBackgroundColorRemovalLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());

    }
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalledWithAmmoniaAndBlackAndWhiteModeForLFP_ThenBackgroundRemovalContexIsSet)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = true;
    scanPipelineConfig_->imageQuality = true;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::MDF);
    intent->setColorMode(ColorMode::BLACKANDWHITE);
    intent->setOriginalMediaType(dune::scan::types::OriginalMediaType::DARK_BLUEPRINTS);
    intent->setBackgroundColorRemoval(true);

    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &addborderRequired](bool value) -> void {

                addborderRequired = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_)).Times(0);

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))

        .WillRepeatedly(

            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    dune::imaging::types::PrintScaleT printScaleTable;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_))
        .WillRepeatedly(

            testing::Invoke([this, &printScaleTable](dune::imaging::types::PrintScaleT  value) -> void {

                printScaleTable = value;

            }));

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    bool detectOriginalScanSize{false};
    EXPECT_CALL(*imageProcessorIntent_, setDetectOriginalScanSize(_))
        .WillRepeatedly(
            testing::Invoke([this, &detectOriginalScanSize](bool value) -> void {
                detectOriginalScanSize = value;
            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))

        .WillRepeatedly(

            testing::Invoke([this, &iqTable](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> value) -> void {

                iqTable = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::LFP, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->upScaleStrategy =  dune::imaging::types::ScaleStrategy::QUADRATIC;
    resourceConfig->downScaleStrategy =  dune::imaging::types::ScaleStrategy::QUADRATIC;
    resourceConfig->detectOriginalScanSize = true;
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(addborderRequired, true);
    EXPECT_EQ(useImageQuality, true);
    EXPECT_EQ(edgeRemoval, true);
    EXPECT_EQ(autoDeskew, intent->getAutoDeskew());
    EXPECT_EQ(threshold, false);
    EXPECT_EQ(imageRotation, true);
    EXPECT_EQ(specificPadding.overridePadding, false);
    EXPECT_EQ(specificPadding.topPad, 0);
    EXPECT_EQ(specificPadding.bottomPad, 0);
    EXPECT_EQ(specificPadding.leftPad, 0);
    EXPECT_EQ(specificPadding.rightPad, 0);
    EXPECT_EQ(specificRotation.overrideRotation, false);
    EXPECT_EQ(specificRotation.rotation, 0);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(printScaleTable.xScalePercent, intent->getXScalePercent());
    EXPECT_EQ(printScaleTable.yScalePercent, intent->getYScalePercent());
    EXPECT_EQ(printScaleTable.scaleToOutput, intent->getScaleToOutput());
    EXPECT_EQ(printScaleTable.scaleToSize, intent->getScaleToSize());
    EXPECT_EQ(printScaleTable.upScaleStrategy, dune::imaging::types::ScaleStrategy::QUADRATIC);
    EXPECT_EQ(printScaleTable.downScaleStrategy, dune::imaging::types::ScaleStrategy::QUADRATIC);
    EXPECT_EQ(detectOriginalScanSize, true);

    if(scanPipelineConfig_->imageQuality)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_AUTOCTX);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->backgroundDensity, intent->getBackgroundColorRemovalLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());

    }
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalledWithAmmoniaAndGrayscaleForLFP_ThenBackgroundRemovalHPIsSet)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = false;
    scanPipelineConfig_->imageQuality = true;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::MDF);
    intent->setColorMode(ColorMode::GRAYSCALE);
    intent->setOriginalMediaType(dune::scan::types::OriginalMediaType::DARK_BLUEPRINTS);
    intent->setBackgroundColorRemoval(true);

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_)).Times(0);

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))

        .WillRepeatedly(

            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    dune::imaging::types::PrintScaleT printScaleTable;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_))
        .WillRepeatedly(

            testing::Invoke([this, &printScaleTable](dune::imaging::types::PrintScaleT  value) -> void {

                printScaleTable = value;

            }));

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    bool detectOriginalScanSize{false};
    EXPECT_CALL(*imageProcessorIntent_, setDetectOriginalScanSize(_))
        .WillRepeatedly(
            testing::Invoke([this, &detectOriginalScanSize](bool value) -> void {
                detectOriginalScanSize = value;
            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))

        .WillRepeatedly(

            testing::Invoke([this, &iqTable](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> value) -> void {

                iqTable = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::LFP, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->upScaleStrategy =  dune::imaging::types::ScaleStrategy::QUADRATIC;
    resourceConfig->downScaleStrategy =  dune::imaging::types::ScaleStrategy::QUADRATIC;
    resourceConfig->detectOriginalScanSize = true;
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(useImageQuality, true);
    EXPECT_EQ(autoDeskew, intent->getAutoDeskew());
    EXPECT_EQ(threshold, false);
    EXPECT_EQ(imageRotation, true);
    EXPECT_EQ(specificPadding.overridePadding, false);
    EXPECT_EQ(specificPadding.topPad, 0);
    EXPECT_EQ(specificPadding.bottomPad, 0);
    EXPECT_EQ(specificPadding.leftPad, 0);
    EXPECT_EQ(specificPadding.rightPad, 0);
    EXPECT_EQ(specificRotation.overrideRotation, false);
    EXPECT_EQ(specificRotation.rotation, 0);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(printScaleTable.xScalePercent, intent->getXScalePercent());
    EXPECT_EQ(printScaleTable.yScalePercent, intent->getYScalePercent());
    EXPECT_EQ(printScaleTable.scaleToOutput, intent->getScaleToOutput());
    EXPECT_EQ(printScaleTable.scaleToSize, intent->getScaleToSize());
    EXPECT_EQ(printScaleTable.upScaleStrategy, dune::imaging::types::ScaleStrategy::QUADRATIC);
    EXPECT_EQ(printScaleTable.downScaleStrategy, dune::imaging::types::ScaleStrategy::QUADRATIC);
    EXPECT_EQ(detectOriginalScanSize, true);

    if(scanPipelineConfig_->imageQuality)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_AUTOHP);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->backgroundDensity, intent->getBackgroundColorRemovalLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());
    }
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalled_ForEnterprise_BackGroundColorRemovalSupportedTrue)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = true;
    scanPipelineConfig_->imageQuality = true;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::MDF);
    intent->setColorMode(ColorMode::BLACKANDWHITE);
    intent->setBackgroundColorRemoval(true);


    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &addborderRequired](bool value) -> void {

                addborderRequired = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_)).Times(0);

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))

        .WillRepeatedly(

            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    dune::imaging::types::PrintScaleT printScaleTable;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_))
        .WillRepeatedly(

            testing::Invoke([this, &printScaleTable](dune::imaging::types::PrintScaleT  value) -> void {

                printScaleTable = value;

            }));

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))

        .WillRepeatedly(

            testing::Invoke([this, &iqTable](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> value) -> void {

                iqTable = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(addborderRequired, true);
    EXPECT_EQ(useImageQuality, true);
    EXPECT_EQ(edgeRemoval, true);
    EXPECT_EQ(autoDeskew, intent->getAutoDeskew());
    EXPECT_EQ(threshold, false);
    EXPECT_EQ(imageRotation, false);
    EXPECT_EQ(specificPadding.overridePadding, false);
    EXPECT_EQ(specificPadding.topPad, 0);
    EXPECT_EQ(specificPadding.bottomPad, 0);
    EXPECT_EQ(specificPadding.leftPad, 0);
    EXPECT_EQ(specificPadding.rightPad, 0);
    EXPECT_EQ(specificRotation.overrideRotation, false);
    EXPECT_EQ(specificRotation.rotation, 0);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(printScaleTable.xScalePercent, intent->getXScalePercent());
    EXPECT_EQ(printScaleTable.yScalePercent, intent->getYScalePercent());
    EXPECT_EQ(printScaleTable.scaleToOutput, intent->getScaleToOutput());
    EXPECT_EQ(printScaleTable.scaleToSize, intent->getScaleToSize());

    if(scanPipelineConfig_->imageQuality)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_NONE);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());

    }
}

// when scan source is glass and scan capture mode is IDCard, specific padding should be applied
TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalled_ForHomeProGlass_ThenSpecificPaddingApplied)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = false;
    scanPipelineConfig_->imageQuality = false;

    // Scan Source - Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    // set Scan Source as Glass and Scan Capture Mode as IDCard
    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);

    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))
        .WillRepeatedly(
            testing::Invoke([this, &addborderRequired](bool value) -> void {

                addborderRequired = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))
        .WillRepeatedly(
            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_))
        .WillRepeatedly(
                testing::Invoke([this, &specificPadding](dune::imaging::Resources::SpecificPadding value) -> void {

                    specificPadding = value;

                }));


    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_))
        .WillRepeatedly(
                testing::Invoke([this, &specificRotation](dune::imaging::Resources::SpecificRotation value) -> void {

                    specificRotation = value;

                }));
    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))
        .WillRepeatedly(
            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))
        .WillRepeatedly(
            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))
        .WillRepeatedly(
            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool threshold{true};
    uint32_t thresholdValue{0};
    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_, _))
        .WillRepeatedly(
            testing::Invoke([this, &threshold, &thresholdValue](bool value1, uint32_t value) -> void {

                threshold = value1;
                thresholdValue = value;

            }));

    bool imageRotation{true};
    EXPECT_CALL(*imageProcessorIntent_, setCheckImageRotation(_))
        .WillRepeatedly(
            testing::Invoke([this, &imageRotation](bool value) -> void {

                imageRotation = value;

            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_)).Times(0);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::COPY);
    EXPECT_EQ(addborderRequired, false);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_ForIDCardCopy_WithMediaLetter)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;
            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value;
            }));
    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly(
            testing::Invoke([this, &xExtent]() -> uint32_t {
                return xExtent ;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly(
            testing::Invoke([this, &yExtent]() -> uint32_t {
                return yExtent ;
            }));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);

    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(intent->getScanCaptureMode(), dune::scan::types::ScanCaptureModeType::IDCARD);
    EXPECT_EQ(intent->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(scanDeviceIntent_->getXExtent(), xExtent);
    EXPECT_EQ(scanDeviceIntent_->getYExtent(), yExtent);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(intent->getScanCaptureMode(), dune::scan::types::ScanCaptureModeType::IDCARD);
    EXPECT_EQ(intent->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(scanDeviceIntent_->getXExtent(), 2550);
    EXPECT_EQ(scanDeviceIntent_->getYExtent(), 1650);

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupIPADeviceIntentCalled_ForIDCardCopy_WithMediaLetter)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);

    uint32_t xoutExtent;
    EXPECT_CALL(*ipaDeviceIntent_, setOutXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xoutExtent](uint32_t value) -> void {

                xoutExtent = value;

            }));

    uint32_t youtExtent;
    EXPECT_CALL(*ipaDeviceIntent_, setOutYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &youtExtent](uint32_t value) -> void {

                youtExtent = value;

            }));
    
    uint32_t brightness;
    EXPECT_CALL(*ipaDeviceIntent_, setBrightness(_))

        .WillRepeatedly(

            testing::Invoke([this, &brightness](uint32_t value) -> void {

                brightness = value;

            }));
    uint32_t autoToneLevel;
    EXPECT_CALL(*ipaDeviceIntent_, setAutoToneLevel(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoToneLevel](uint32_t value) -> void {

                autoToneLevel = value;

            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*ipaDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*ipaDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));

    uint32_t multipleLineRequired;
    EXPECT_CALL(*ipaDeviceIntent_, setMultipleNumberOfLinesRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &multipleLineRequired](uint32_t value) -> void {

                multipleLineRequired = value;

            }));

    uint32_t autoPaperColorRemoval;
    EXPECT_CALL(*ipaDeviceIntent_, setAutoPaperColorRemovalLevel(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoPaperColorRemoval](uint32_t value) -> void {

                autoPaperColorRemoval = value;

            }));

    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*ipaDeviceIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;

            }));

    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*ipaDeviceIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::ContentOrientation contentOrientation;
    EXPECT_CALL(*ipaDeviceIntent_, setOriginalContentOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &contentOrientation](dune::imaging::types::ContentOrientation  value) -> void {

                contentOrientation = value;

            }));
    dune::imaging::types::OriginalContentType originalContentType;
    EXPECT_CALL(*ipaDeviceIntent_, setOriginalContentType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalContentType](dune::imaging::types::OriginalContentType  value) -> void {

                originalContentType = value;

            }));

    dune::scan::types::ScanFeedOrientation scanFeedOrientation;
    EXPECT_CALL(*ipaDeviceIntent_, setScanFeedOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanFeedOrientation](dune::scan::types::ScanFeedOrientation  value) -> void {

                scanFeedOrientation = value;

            }));

    dune::scan::Resources::CompressionType compressionType;
    EXPECT_CALL(*ipaDeviceIntent_, setCompressionType(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionType](dune::scan::Resources::CompressionType value) -> void {

                compressionType = value;

            }));



    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, true, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setupIPADeviceIntent(ipaDeviceIntent_, resourceConfig);

    EXPECT_EQ(5100, xoutExtent);
    EXPECT_EQ(6600, youtExtent);
    EXPECT_EQ(100, xScalePercent);
    EXPECT_EQ(100, yScalePercent);

    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    copyPipelineResourceSetup->setupIPADeviceIntent(ipaDeviceIntent_, resourceConfig);

    EXPECT_EQ(0, xoutExtent);
    EXPECT_EQ(0, youtExtent);
}


TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_ForIDCardCopy_WithMediaA4)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;
            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value;
            }));
    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly(
            testing::Invoke([this, &xExtent]() -> uint32_t {
                return xExtent ;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly(
            testing::Invoke([this, &yExtent]() -> uint32_t {
                return yExtent ;
            }));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);

    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(intent->getScanCaptureMode(), dune::scan::types::ScanCaptureModeType::IDCARD);
    EXPECT_EQ(intent->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::A4);
    EXPECT_EQ(scanDeviceIntent_->getXExtent(), xExtent);
    EXPECT_EQ(scanDeviceIntent_->getYExtent(), yExtent);

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_ForIDCardCopy_WithMediaA3)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;
            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value;
            }));
    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly(
            testing::Invoke([this, &xExtent]() -> uint32_t {
                return xExtent ;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly(
            testing::Invoke([this, &yExtent]() -> uint32_t {
                return yExtent ;
            }));

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A3);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A3);

    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(intent->getScanCaptureMode(), dune::scan::types::ScanCaptureModeType::IDCARD);
    EXPECT_EQ(intent->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::A3);
    EXPECT_EQ(scanDeviceIntent_->getXExtent(), xExtent);
    EXPECT_EQ(scanDeviceIntent_->getYExtent(), yExtent);

}

// When edge to edge scan is enabled, autoCrop should be set to false
TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_WithEdgeToEdgeEnabled)
{
    // Look for edge to edge scan to cause the pipeline builder to set auto crop to false in the scan device intents
    EXPECT_CALL(*scanDeviceIntent_, setAutoCrop(false)).Times(1);
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    auto intent = jobTicket->getIntent();

    // ensure default value
    intent->setAutoCrop(true);
    // Set edgeToEdge to true to trigger auto crop to be set to false
    jobTicket->getIntent()->setEdgeToEdgeScan(true);

    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);
}

// When edge to edge scan is not enabled, autoCrop should not be set to false
TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_WithEdgeToEdgeDisabled)
{
    // No edge to edge scan -> don't set auto crop to false in the scan device intents
    EXPECT_CALL(*scanDeviceIntent_, setAutoCrop(false)).Times(0);
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    auto intent = jobTicket->getIntent();

    // ensure default value
    intent->setAutoCrop(true);
    // Set edgeToEdge to false
    jobTicket->getIntent()->setEdgeToEdgeScan(false);

    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorPreviewIntentCalled_WithBasicMode)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = true;
    scanPipelineConfig_->imageQuality = true;
    scanPipelineConfig_->thumbnailResolution = 40;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    uint32_t thumbnailResolution;
    EXPECT_CALL(*imageProcessorIntent_, setThumbnailResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &thumbnailResolution](uint32_t value) -> void {

                thumbnailResolution = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));
    bool previewNeeded{true};
    EXPECT_CALL(*imageProcessorIntent_, setPreviewIsNeeded(_))

        .WillRepeatedly(

            testing::Invoke([this, &previewNeeded](bool value) -> void {

                previewNeeded = value;

            }));
    dune::imaging::Resources::ComputeScale computeScale;
    EXPECT_CALL(*imageProcessorIntent_, setComputeScale(_))

        .WillRepeatedly(

            testing::Invoke([this, &computeScale](dune::imaging::Resources::ComputeScale value) -> void {

                computeScale = value;

            }));

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool detectOriginalScanSize{false};
    EXPECT_CALL(*imageProcessorIntent_, setDetectOriginalScanSize(_))
        .WillRepeatedly(
            testing::Invoke([this, &detectOriginalScanSize](bool value) -> void {
                detectOriginalScanSize = value;
            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))

        .WillRepeatedly(

            testing::Invoke([this, &iqTable](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> value) -> void {

                iqTable = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->detectOriginalScanSize = true;
    copyPipelineResourceSetup->setupImageProcessorPreviewIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(useImageQuality, true);
    EXPECT_EQ(computeScale, dune::imaging::Resources::ComputeScale::RESOLUTION);
    EXPECT_EQ(previewNeeded, true);
    EXPECT_EQ(edgeRemoval, true);
    EXPECT_EQ(thumbnailResolution, 40);
    EXPECT_EQ(autoDeskew, false);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::PREVIEW);
    EXPECT_EQ(detectOriginalScanSize, true);

    if(iqTable.get() != nullptr)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_NONE);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());

    }

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorPreviewIntentCalled_WithBasicModeBackGroundColorRemovalOn)
{
    // Setup ScanPipelineConfig
    scanPipelineConfig_->edgeRemoval = true;
    scanPipelineConfig_->imageQuality = true;
    scanPipelineConfig_->thumbnailResolution = 40;

    // Scan Source - ADF/Flatbed
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    intent->setBackgroundColorRemoval(true);

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    uint32_t thumbnailResolution;
    EXPECT_CALL(*imageProcessorIntent_, setThumbnailResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &thumbnailResolution](uint32_t value) -> void {

                thumbnailResolution = value;

            }));

    bool useImageQuality{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseImageQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &useImageQuality](bool value) -> void {

                useImageQuality = value;

            }));
    bool previewNeeded{true};
    EXPECT_CALL(*imageProcessorIntent_, setPreviewIsNeeded(_))

        .WillRepeatedly(

            testing::Invoke([this, &previewNeeded](bool value) -> void {

                previewNeeded = value;

            }));
    dune::imaging::Resources::ComputeScale computeScale;
    EXPECT_CALL(*imageProcessorIntent_, setComputeScale(_))

        .WillRepeatedly(

            testing::Invoke([this, &computeScale](dune::imaging::Resources::ComputeScale value) -> void {

                computeScale = value;

            }));

    dune::imaging::Resources::FlowType flowType;
    EXPECT_CALL(*imageProcessorIntent_, setFlowType(_))

        .WillRepeatedly(

            testing::Invoke([this, &flowType](dune::imaging::Resources::FlowType value) -> void {

                flowType = value;

            }));

    bool edgeRemoval{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseEdgeRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &edgeRemoval](bool value) -> void {

                edgeRemoval = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));

    bool detectOriginalScanSize{false};
    EXPECT_CALL(*imageProcessorIntent_, setDetectOriginalScanSize(_))
        .WillRepeatedly(
            testing::Invoke([this, &detectOriginalScanSize](bool value) -> void {
                detectOriginalScanSize = value;
            }));

    std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable;

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))

        .WillRepeatedly(

            testing::Invoke([this, &iqTable](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> value) -> void {

                iqTable = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->detectOriginalScanSize = true;
    copyPipelineResourceSetup->setupImageProcessorPreviewIntent(imageProcessorIntent_, resourceConfig);

    EXPECT_EQ(useImageQuality, true);
    EXPECT_EQ(computeScale, dune::imaging::Resources::ComputeScale::RESOLUTION);
    EXPECT_EQ(previewNeeded, true);
    EXPECT_EQ(edgeRemoval, true);
    EXPECT_EQ(thumbnailResolution, 40);
    EXPECT_EQ(autoDeskew, false);
    EXPECT_EQ(flowType, dune::imaging::Resources::FlowType::PREVIEW);
    EXPECT_EQ(detectOriginalScanSize, true);

    if(iqTable.get() != nullptr)
    {
        EXPECT_EQ(iqTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_AUTOCTX);
        EXPECT_EQ(iqTable->originalContentType, intent->getOriginalContentType());
        EXPECT_EQ(iqTable->blackEnhancements, intent->getBlackEnhancementLevel());
        EXPECT_EQ(iqTable->backgroundDensity, intent->getBackgroundColorRemovalLevel());
        EXPECT_EQ(iqTable->negative, intent->getInvertColors());

    }

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_WithHomeProGlass)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .Times(2).WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .Times(2).WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .Times(2).WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .Times(2).WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .Times(2).WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .Times(2).WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .Times(2).WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    auto intent = jobTicket->getIntent();

    intent->setScanSource(ScanSource::GLASS);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LEGAL);

    uint32_t brightness;
    EXPECT_CALL(*scanDeviceIntent_, setBrightness(_))

        .WillRepeatedly(

            testing::Invoke([this, &brightness](uint32_t value) -> void {

                brightness = value;

            }));

    uint32_t alignmentRequired;
    EXPECT_CALL(*scanDeviceIntent_, setRequiredWidthAlignment(_))

        .WillRepeatedly(

            testing::Invoke([this, &alignmentRequired](uint32_t value) -> void {

                alignmentRequired = value;

            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yExtent](uint32_t value) -> void {

                yExtent = value;

            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));

    uint32_t multipleLineRequired;
    EXPECT_CALL(*scanDeviceIntent_, setMultipleNumberOfLinesRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &multipleLineRequired](uint32_t value) -> void {

                multipleLineRequired = value;

            }));

    bool interleavedObjectMap{true};
    EXPECT_CALL(*scanDeviceIntent_, setInterleavedObjectMap(_))

        .WillRepeatedly(

            testing::Invoke([this, &interleavedObjectMap](bool value) -> void {

                interleavedObjectMap = value;

            }));

    bool autoRelease{true};
    EXPECT_CALL(*scanDeviceIntent_, setAutoRelease(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoRelease](bool value) -> void {

                autoRelease = value;

            }));

    bool scanInYcc{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanInYcc(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanInYcc](bool value) -> void {

                scanInYcc = value;

            }));

    int32_t scanNoiseRemoval{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanNoiseRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanNoiseRemoval](int32_t value) -> void {

                scanNoiseRemoval = value;

            }));

    uint32_t backgroundColorRemoval;
    EXPECT_CALL(*scanDeviceIntent_, setBackgroundRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &backgroundColorRemoval](uint32_t value) -> void {

                backgroundColorRemoval = value;

            }));

    bool scanOutputInterleaved{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanOutputInterleaved(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanOutputInterleaved](bool value) -> void {

                scanOutputInterleaved = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*scanDeviceIntent_, setAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));
    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*scanDeviceIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;

            }));
    dune::scan::types::ScanSource scanSource;
    EXPECT_CALL(*scanDeviceIntent_, setScanSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanSource](dune::scan::types::ScanSource value) -> void {

                scanSource = value;

            }));

    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*scanDeviceIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::ContentOrientation contentOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &contentOrientation](dune::imaging::types::ContentOrientation  value) -> void {

                contentOrientation = value;

            }));
    dune::imaging::types::OriginalContentType originalContentType;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalContentType](dune::imaging::types::OriginalContentType  value) -> void {

                originalContentType = value;

            }));

    dune::scan::types::OriginalMediaType originalMediaType;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalMediaType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalMediaType](dune::scan::types::OriginalMediaType  value) -> void {

                originalMediaType = value;

            }));

    dune::scan::types::ScanFeedOrientation scanFeedOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setScanFeedOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanFeedOrientation](dune::scan::types::ScanFeedOrientation  value) -> void {

                scanFeedOrientation = value;

            }));

    dune::scan::types::ScanAcquisitionsSpeedEnum scanAcquistionSpeed;
    EXPECT_CALL(*scanDeviceIntent_, setScanAcquisitionsSpeed(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanAcquistionSpeed](dune::scan::types::ScanAcquisitionsSpeedEnum value) -> void {

                scanAcquistionSpeed = value;

            }));

    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {

                xResolution = value;

            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {

                yResolution = value;

            }));

    dune::scan::types::ScanCaptureModeType captureMode;
    EXPECT_CALL(*scanDeviceIntent_, setScanCaptureMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &captureMode](dune::scan::types::ScanCaptureModeType value) -> void {

                captureMode = value;

            }));

    dune::scan::Resources::CompressionType compressionType;
    EXPECT_CALL(*scanDeviceIntent_, setCompressionType(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionType](dune::scan::Resources::CompressionType value) -> void {

                compressionType = value;

            }));

    dune::scan::types::ScanMapQualityEnum scanMapQuality;
    EXPECT_CALL(*scanDeviceIntent_, setScanMapQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanMapQuality](dune::scan::types::ScanMapQualityEnum value) -> void {

                scanMapQuality = value;

            }));

    std::string fileName;
    EXPECT_CALL(*scanDeviceIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));
    std::string filePath;
    EXPECT_CALL(*scanDeviceIntent_, setFilePath(_))

        .WillRepeatedly(

            testing::Invoke([this, &filePath](std::string value) -> void {

                filePath = value;

            }));

    EXPECT_CALL(*scanDeviceIntent_, setBookMode(_)).Times(2);

    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*scanDeviceIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(scanImagingProfileType, dune::scan::types::ScanImagingProfileType::COPY);
    EXPECT_EQ(intent->getCollate(), dune::copy::SheetCollate::Uncollate);

    // jobTicket update to book mode
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    EXPECT_CALL(*scanPipeline_, setupScanDeviceForBookMode(_,_));
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);
    EXPECT_EQ(scanFeedOrientation, dune::scan::types::ScanFeedOrientation::LONGEDGE);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalledInputMatchesOutputAndBorderlessShouldSet_OutExtentsSetCorrectly)
{

    auto jobTicket = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();
    auto intent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();

    //Setup function call returns
    ON_CALL(*jobTicket, getScanCapabilitiesInterface())
        .WillByDefault(Return(scannerCapabilities_.get()));

    ON_CALL(*jobTicket, getIntent())
        .WillByDefault(Return(intent));

    ON_CALL(*jobTicket, shouldBeBorderless())
        .WillByDefault(Return(true));

    ON_CALL(*intent, getScanSource())
        .WillByDefault(Return(ScanSource::GLASS));

    ON_CALL(*intent, getInputMediaSizeId())
        .WillByDefault(Return(dune::imaging::types::MediaSizeId::PHOTO4X6));

    ON_CALL(*intent, getOutputMediaSizeId())
        .WillByDefault(Return(dune::imaging::types::MediaSizeId::PHOTO4X6));

    ON_CALL(*scanDeviceIntent_, getXScalePercent())
        .WillByDefault(Return(100));

    ON_CALL(*scanDeviceIntent_, getYScalePercent())
        .WillByDefault(Return(100));

    //Setup Feature values
    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    uint32_t xoutExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xoutExtent](uint32_t value) -> void {

                xoutExtent = value;

            }));

    uint32_t youtExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &youtExtent](uint32_t value) -> void {

                youtExtent = value;

            }));
    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xExtent](uint32_t value) -> void {

                xExtent = value;

            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yExtent](uint32_t value) -> void {

                yExtent = value;

            }));
    EXPECT_CALL(*scanDeviceIntent_, getXExtent())

        .WillRepeatedly(

            testing::Invoke([this, &xExtent]() -> uint32_t {

                return xExtent ;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())

        .WillRepeatedly(

            testing::Invoke([this, &yExtent]() -> uint32_t {

                return yExtent ;

            }));

    uint64_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint64_t value) -> void {

                xScalePercent = value;

            }));

    uint64_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint64_t value) -> void {

                yScalePercent = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);
    EXPECT_EQ(xoutExtent, 1200);
    EXPECT_EQ(youtExtent, 1800);
    EXPECT_EQ(xScalePercent, 110905);
    EXPECT_EQ(yScalePercent, 107015);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalledAndScanDeviceHasCapabilities_WithHomeProGlass)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    auto intent = jobTicket->getIntent();

    intent->setScanSource(ScanSource::GLASS);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    uint32_t brightness;
    EXPECT_CALL(*scanDeviceIntent_, setBrightness(_))

        .WillRepeatedly(

            testing::Invoke([this, &brightness](uint32_t value) -> void {

                brightness = value;

            }));

    uint32_t alignmentRequired;
    EXPECT_CALL(*scanDeviceIntent_, setRequiredWidthAlignment(_))

        .WillRepeatedly(

            testing::Invoke([this, &alignmentRequired](uint32_t value) -> void {

                alignmentRequired = value;

            }));

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xExtent](uint32_t value) -> void {

                xExtent = value;

            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yExtent](uint32_t value) -> void {

                yExtent = value;

            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));

    uint32_t multipleLineRequired;
    EXPECT_CALL(*scanDeviceIntent_, setMultipleNumberOfLinesRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &multipleLineRequired](uint32_t value) -> void {

                multipleLineRequired = value;

            }));

    bool interleavedObjectMap{true};
    EXPECT_CALL(*scanDeviceIntent_, setInterleavedObjectMap(_))

        .WillRepeatedly(

            testing::Invoke([this, &interleavedObjectMap](bool value) -> void {

                interleavedObjectMap = value;

            }));

    bool autoRelease{true};
    EXPECT_CALL(*scanDeviceIntent_, setAutoRelease(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoRelease](bool value) -> void {

                autoRelease = value;

            }));

    bool autoCrop{false};
    EXPECT_CALL(*scanDeviceIntent_, setAutoCrop(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoCrop](bool value) -> void {

                autoCrop = value;

            }));

    bool scanInYcc{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanInYcc(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanInYcc](bool value) -> void {

                scanInYcc = value;

            }));

    int32_t scanNoiseRemoval{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanNoiseRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanNoiseRemoval](int32_t value) -> void {

                scanNoiseRemoval = value;

            }));

    uint32_t backgroundColorRemoval;
    EXPECT_CALL(*scanDeviceIntent_, setBackgroundRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &backgroundColorRemoval](uint32_t value) -> void {

                backgroundColorRemoval = value;

            }));

    bool scanOutputInterleaved{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanOutputInterleaved(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanOutputInterleaved](bool value) -> void {

                scanOutputInterleaved = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*scanDeviceIntent_, setAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));
    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*scanDeviceIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;

            }));
    dune::scan::types::ScanSource scanSource;
    EXPECT_CALL(*scanDeviceIntent_, setScanSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanSource](dune::scan::types::ScanSource value) -> void {

                scanSource = value;

            }));

    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*scanDeviceIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::ContentOrientation contentOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &contentOrientation](dune::imaging::types::ContentOrientation  value) -> void {

                contentOrientation = value;

            }));
    dune::imaging::types::OriginalContentType originalContentType;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalContentType](dune::imaging::types::OriginalContentType  value) -> void {

                originalContentType = value;

            }));

    dune::scan::types::OriginalMediaType originalMediaType;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalMediaType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalMediaType](dune::scan::types::OriginalMediaType  value) -> void {

                originalMediaType = value;

            }));

    dune::scan::types::ScanFeedOrientation scanFeedOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setScanFeedOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanFeedOrientation](dune::scan::types::ScanFeedOrientation  value) -> void {

                scanFeedOrientation = value;

            }));

    dune::scan::types::ScanAcquisitionsSpeedEnum scanAcquistionSpeed;
    EXPECT_CALL(*scanDeviceIntent_, setScanAcquisitionsSpeed(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanAcquistionSpeed](dune::scan::types::ScanAcquisitionsSpeedEnum value) -> void {

                scanAcquistionSpeed = value;

            }));

    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {

                xResolution = value;

            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {

                yResolution = value;

            }));

    dune::scan::types::ScanCaptureModeType captureMode;
    EXPECT_CALL(*scanDeviceIntent_, setScanCaptureMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &captureMode](dune::scan::types::ScanCaptureModeType value) -> void {

                captureMode = value;

            }));

    dune::scan::Resources::CompressionType compressionType;
    EXPECT_CALL(*scanDeviceIntent_, setCompressionType(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionType](dune::scan::Resources::CompressionType value) -> void {

                compressionType = value;

            }));

    dune::scan::types::ScanMapQualityEnum scanMapQuality;
    EXPECT_CALL(*scanDeviceIntent_, setScanMapQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanMapQuality](dune::scan::types::ScanMapQualityEnum value) -> void {

                scanMapQuality = value;

            }));

    std::string fileName;
    EXPECT_CALL(*scanDeviceIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));
    std::string filePath;
    EXPECT_CALL(*scanDeviceIntent_, setFilePath(_))

        .WillRepeatedly(

            testing::Invoke([this, &filePath](std::string value) -> void {

                filePath = value;

            }));

    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*scanDeviceIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(scanImagingProfileType, dune::scan::types::ScanImagingProfileType::COPY);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    auto intent = jobTicket->getIntent();

    uint32_t brightness;
    EXPECT_CALL(*scanDeviceIntent_, setBrightness(_))

        .WillRepeatedly(

            testing::Invoke([this, &brightness](uint32_t value) -> void {

                brightness = value;

            }));

    uint32_t alignmentRequired;
    EXPECT_CALL(*scanDeviceIntent_, setRequiredWidthAlignment(_))

        .WillRepeatedly(

            testing::Invoke([this, &alignmentRequired](uint32_t value) -> void {

                alignmentRequired = value;

            }));

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xExtent](uint32_t value) -> void {

                xExtent = value;

            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yExtent](uint32_t value) -> void {

                yExtent = value;

            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));

    uint32_t multipleLineRequired;
    EXPECT_CALL(*scanDeviceIntent_, setMultipleNumberOfLinesRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &multipleLineRequired](uint32_t value) -> void {

                multipleLineRequired = value;

            }));

    bool interleavedObjectMap{true};
    EXPECT_CALL(*scanDeviceIntent_, setInterleavedObjectMap(_))

        .WillRepeatedly(

            testing::Invoke([this, &interleavedObjectMap](bool value) -> void {

                interleavedObjectMap = value;

            }));

    bool autoRelease{true};
    EXPECT_CALL(*scanDeviceIntent_, setAutoRelease(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoRelease](bool value) -> void {

                autoRelease = value;

            }));

    bool scanInYcc{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanInYcc(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanInYcc](bool value) -> void {

                scanInYcc = value;

            }));

    int32_t scanNoiseRemoval{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanNoiseRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanNoiseRemoval](int32_t value) -> void {

                scanNoiseRemoval = value;

            }));

    uint32_t backgroundColorRemoval;
    EXPECT_CALL(*scanDeviceIntent_, setBackgroundRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &backgroundColorRemoval](uint32_t value) -> void {

                backgroundColorRemoval = value;

            }));

    bool scanOutputInterleaved{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanOutputInterleaved(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanOutputInterleaved](bool value) -> void {

                scanOutputInterleaved = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*scanDeviceIntent_, setAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));
    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*scanDeviceIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;

            }));
    dune::scan::types::ScanSource scanSource;
    EXPECT_CALL(*scanDeviceIntent_, setScanSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanSource](dune::scan::types::ScanSource value) -> void {

                scanSource = value;

            }));

    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*scanDeviceIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::ContentOrientation contentOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &contentOrientation](dune::imaging::types::ContentOrientation  value) -> void {

                contentOrientation = value;

            }));
    dune::imaging::types::OriginalContentType originalContentType;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalContentType](dune::imaging::types::OriginalContentType  value) -> void {

                originalContentType = value;

            }));

    dune::scan::types::OriginalMediaType originalMediaType;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalMediaType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalMediaType](dune::scan::types::OriginalMediaType  value) -> void {

                originalMediaType = value;

            }));

    dune::scan::types::ScanFeedOrientation scanFeedOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setScanFeedOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanFeedOrientation](dune::scan::types::ScanFeedOrientation  value) -> void {

                scanFeedOrientation = value;

            }));

    dune::scan::types::ScanAcquisitionsSpeedEnum scanAcquistionSpeed;
    EXPECT_CALL(*scanDeviceIntent_, setScanAcquisitionsSpeed(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanAcquistionSpeed](dune::scan::types::ScanAcquisitionsSpeedEnum value) -> void {

                scanAcquistionSpeed = value;

            }));

    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {

                xResolution = value;

            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {

                yResolution = value;

            }));

    dune::scan::types::ScanCaptureModeType captureMode;
    EXPECT_CALL(*scanDeviceIntent_, setScanCaptureMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &captureMode](dune::scan::types::ScanCaptureModeType value) -> void {

                captureMode = value;

            }));

    dune::scan::Resources::CompressionType compressionType;
    EXPECT_CALL(*scanDeviceIntent_, setCompressionType(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionType](dune::scan::Resources::CompressionType value) -> void {

                compressionType = value;

            }));

    dune::scan::types::ScanMapQualityEnum scanMapQuality;
    EXPECT_CALL(*scanDeviceIntent_, setScanMapQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanMapQuality](dune::scan::types::ScanMapQualityEnum value) -> void {

                scanMapQuality = value;

            }));

    std::string fileName;
    EXPECT_CALL(*scanDeviceIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));
    std::string filePath;
    EXPECT_CALL(*scanDeviceIntent_, setFilePath(_))

        .WillRepeatedly(

            testing::Invoke([this, &filePath](std::string value) -> void {

                filePath = value;

            }));

    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*scanDeviceIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(scanImagingProfileType, dune::scan::types::ScanImagingProfileType::COPY);


}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalledForPreScan_ThenIntentHasPreviewScanTrue)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    auto intent = jobTicket->getIntent();

    uint32_t brightness;
    EXPECT_CALL(*scanDeviceIntent_, setBrightness(_))

        .WillRepeatedly(

            testing::Invoke([this, &brightness](uint32_t value) -> void {

                brightness = value;

            }));

    uint32_t alignmentRequired;
    EXPECT_CALL(*scanDeviceIntent_, setRequiredWidthAlignment(_))

        .WillRepeatedly(

            testing::Invoke([this, &alignmentRequired](uint32_t value) -> void {

                alignmentRequired = value;

            }));

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xExtent](uint32_t value) -> void {

                xExtent = value;

            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yExtent](uint32_t value) -> void {

                yExtent = value;

            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));

    uint32_t multipleLineRequired;
    EXPECT_CALL(*scanDeviceIntent_, setMultipleNumberOfLinesRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &multipleLineRequired](uint32_t value) -> void {

                multipleLineRequired = value;

            }));

    bool interleavedObjectMap{true};
    EXPECT_CALL(*scanDeviceIntent_, setInterleavedObjectMap(_))

        .WillRepeatedly(

            testing::Invoke([this, &interleavedObjectMap](bool value) -> void {

                interleavedObjectMap = value;

            }));

    bool autoRelease{true};
    EXPECT_CALL(*scanDeviceIntent_, setAutoRelease(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoRelease](bool value) -> void {

                autoRelease = value;

            }));

    bool scanInYcc{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanInYcc(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanInYcc](bool value) -> void {

                scanInYcc = value;

            }));

    int32_t scanNoiseRemoval{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanNoiseRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanNoiseRemoval](int32_t value) -> void {

                scanNoiseRemoval = value;

            }));

    uint32_t backgroundColorRemoval;
    EXPECT_CALL(*scanDeviceIntent_, setBackgroundRemoval(_))

        .WillRepeatedly(

            testing::Invoke([this, &backgroundColorRemoval](uint32_t value) -> void {

                backgroundColorRemoval = value;

            }));

    bool scanOutputInterleaved{true};
    EXPECT_CALL(*scanDeviceIntent_, setScanOutputInterleaved(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanOutputInterleaved](bool value) -> void {

                scanOutputInterleaved = value;

            }));

    bool autoDeskew{true};
    EXPECT_CALL(*scanDeviceIntent_, setAutoDeskew(_))

        .WillRepeatedly(

            testing::Invoke([this, &autoDeskew](bool value) -> void {

                autoDeskew = value;

            }));
    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*scanDeviceIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;

            }));
    dune::scan::types::ScanSource scanSource;
    EXPECT_CALL(*scanDeviceIntent_, setScanSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanSource](dune::scan::types::ScanSource value) -> void {

                scanSource = value;

            }));

    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*scanDeviceIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::ContentOrientation contentOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &contentOrientation](dune::imaging::types::ContentOrientation  value) -> void {

                contentOrientation = value;

            }));
    dune::imaging::types::OriginalContentType originalContentType;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalContentType](dune::imaging::types::OriginalContentType  value) -> void {

                originalContentType = value;

            }));

    dune::scan::types::OriginalMediaType originalMediaType;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalMediaType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalMediaType](dune::scan::types::OriginalMediaType  value) -> void {

                originalMediaType = value;

            }));

    dune::scan::types::ScanFeedOrientation scanFeedOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setScanFeedOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanFeedOrientation](dune::scan::types::ScanFeedOrientation  value) -> void {

                scanFeedOrientation = value;

            }));

    dune::scan::types::ScanAcquisitionsSpeedEnum scanAcquistionSpeed;
    EXPECT_CALL(*scanDeviceIntent_, setScanAcquisitionsSpeed(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanAcquistionSpeed](dune::scan::types::ScanAcquisitionsSpeedEnum value) -> void {

                scanAcquistionSpeed = value;

            }));

    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {

                xResolution = value;

            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {

                yResolution = value;

            }));

    dune::scan::types::ScanCaptureModeType captureMode;
    EXPECT_CALL(*scanDeviceIntent_, setScanCaptureMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &captureMode](dune::scan::types::ScanCaptureModeType value) -> void {

                captureMode = value;

            }));

    dune::scan::Resources::CompressionType compressionType;
    EXPECT_CALL(*scanDeviceIntent_, setCompressionType(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionType](dune::scan::Resources::CompressionType value) -> void {

                compressionType = value;

            }));

    dune::scan::types::ScanMapQualityEnum scanMapQuality;
    EXPECT_CALL(*scanDeviceIntent_, setScanMapQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanMapQuality](dune::scan::types::ScanMapQualityEnum value) -> void {

                scanMapQuality = value;

            }));

    std::string fileName;
    EXPECT_CALL(*scanDeviceIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));
    std::string filePath;
    EXPECT_CALL(*scanDeviceIntent_, setFilePath(_))

        .WillRepeatedly(

            testing::Invoke([this, &filePath](std::string value) -> void {

                filePath = value;

            }));

    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*scanDeviceIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));

    bool isPreviewScan = false;
    EXPECT_CALL(*scanDeviceIntent_, setIsPreviewScan(_)).WillRepeatedly(testing::SaveArg<0>(&isPreviewScan));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setSegmentType(SegmentType::PrepareSegment);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(isPreviewScan, true);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_ForBeam_ScanCalibration)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setScanCalibrationType(dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION);
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    auto intent = jobTicket->getIntent();

    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);
    intent->setScanCalibrationType(jobTicket->getScanCalibrationType());

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xExtent](uint32_t value) -> void {

                xExtent = value;

            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yExtent](uint32_t value) -> void {

                yExtent = value;

            }));

    uint32_t xoutExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xoutExtent](uint32_t value) -> void {

                xoutExtent = value;

            }));

    uint32_t youtExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &youtExtent](uint32_t value) -> void {

                youtExtent = value;

            }));

    dune::imaging::types::ScanCalibrationType scanCalibrationType;
    EXPECT_CALL(*scanDeviceIntent_, setScanCalibrationType(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanCalibrationType](dune::imaging::types::ScanCalibrationType value) -> void {

                scanCalibrationType = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(scanCalibrationType, dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_ForEnterprise_LongEdge)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    auto intent = jobTicket->getIntent();

    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;
            }));
    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly(
            testing::Invoke([this, &xExtent]() -> uint32_t {
                return xExtent ;
            }));


    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value;
            }));
    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly(
            testing::Invoke([this, &yExtent]() -> uint32_t {
                return yExtent ;
            }));

    uint32_t xOffset;
    EXPECT_CALL(*scanDeviceIntent_, setXOffset(_))
        .WillRepeatedly(
            testing::Invoke([this, &xOffset](uint32_t value) -> void {
                xOffset = value;
            }));

    uint32_t yOffset;
    EXPECT_CALL(*scanDeviceIntent_, setYOffset(_))
        .WillRepeatedly(
            testing::Invoke([this, &yOffset](uint32_t value) -> void {
                yOffset = value;
            }));

    bool flipUp;
    EXPECT_CALL(*scanDeviceIntent_, setScanPagesFlipUpEnabled(_))
        .WillRepeatedly(
            testing::Invoke([this, &flipUp](bool value) -> void {
                flipUp = value;
            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_TRUE(xExtent > yExtent);
    EXPECT_TRUE(xOffset > 0);
    EXPECT_TRUE(yOffset > 0);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_ForEnterprise_BackgroundCleanup)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setMediaInterface(mediaInterface_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    auto intent = jobTicket->getIntent();
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::SHORTEDGE);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);
    intent->setBackgroundRemoval(4);

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;
            }));
    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly(
            testing::Invoke([this, &xExtent]() -> uint32_t {
                return xExtent ;
            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value;
            }));
    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly(
            testing::Invoke([this, &yExtent]() -> uint32_t {
                return yExtent ;
            }));

    uint32_t xOffset;
    EXPECT_CALL(*scanDeviceIntent_, setXOffset(_))
        .WillRepeatedly(
            testing::Invoke([this, &xOffset](uint32_t value) -> void {
                xOffset = value;
            }));

    uint32_t yOffset;
    EXPECT_CALL(*scanDeviceIntent_, setYOffset(_))
        .WillRepeatedly(
            testing::Invoke([this, &yOffset](uint32_t value) -> void {
                yOffset = value;
            }));

    bool flipUp;
    EXPECT_CALL(*scanDeviceIntent_, setScanPagesFlipUpEnabled(_))
        .WillRepeatedly(
            testing::Invoke([this, &flipUp](bool value) -> void {
                flipUp = value;
            }));

    uint32_t backgroundCleanup;
    EXPECT_CALL(*scanDeviceIntent_, setBackgroundCleanup(_))
        .WillRepeatedly(
            testing::Invoke([this, &backgroundCleanup](uint32_t value) -> void {
                backgroundCleanup = value;
            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(backgroundCleanup, 4);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupMarkingFilterIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    auto markingFilterSettings = std::make_shared<MockIMarkingFilterSettings>();
    ON_CALL(*markingFilterIntent_, getFilterSettings())
        .WillByDefault(Return(markingFilterSettings));


    dune::imaging::types::Plex plex;
    EXPECT_CALL(*markingFilterSettings, setPlex(_))

        .WillRepeatedly(

            testing::Invoke([this, &plex](dune::imaging::types::Plex value) -> void {

                plex = value;

            }));

    dune::imaging::types::ContentOrientation contentOrientation;
    EXPECT_CALL(*markingFilterSettings, setContentOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &contentOrientation](dune::imaging::types::ContentOrientation value) -> void {

                contentOrientation = value;

            }));

    dune::imaging::types::NumberUpTilePlacementType placeMentType;
    EXPECT_CALL(*markingFilterSettings, setNumberUpTilePlacementType(_))

        .WillRepeatedly(

            testing::Invoke([this, &placeMentType](dune::imaging::types::NumberUpTilePlacementType value) -> void {

                placeMentType = value;

            }));

    dune::imaging::types::NumberUpPresentationDirection placeMentDirection;
    EXPECT_CALL(*markingFilterSettings, setNumberUpPresentationDirection(_))

        .WillRepeatedly(

            testing::Invoke([this, &placeMentDirection](dune::imaging::types::NumberUpPresentationDirection value) -> void {

                placeMentDirection = value;

            }));

    dune::imaging::types::CopyOutputNumberUpCount copyOutputCount;
    EXPECT_CALL(*markingFilterSettings, setCopyOutputNumberUpCount(_))

        .WillRepeatedly(

            testing::Invoke([this, &copyOutputCount](dune::imaging::types::CopyOutputNumberUpCount value) -> void {

                copyOutputCount = value;

            }));

    dune::imaging::types::ImageBorder imageBorder;
    EXPECT_CALL(*markingFilterSettings, setImageBorder(_))

        .WillRepeatedly(

            testing::Invoke([this, &imageBorder](dune::imaging::types::ImageBorder value) -> void {

                imageBorder = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupMarkingFilterIntent(markingFilterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupLayoutFilterIntentCalled_ThenIntentIsSet)
{
    // Expectations
    EXPECT_CALL(*layoutFilterIntent_, setSequencingParams(_))
        .WillOnce(Invoke([](const dune::imaging::Resources::LayoutSequencingParams &sequencingParams) -> void {
            EXPECT_EQ(1, sequencingParams.collationCopies);
            EXPECT_EQ(1, sequencingParams.uncollationCopies);
            EXPECT_EQ(0, sequencingParams.pagesNeededToSequence);
            EXPECT_EQ(false, sequencingParams.waitForSheet);
            EXPECT_EQ(false, sequencingParams.updateDetails);
            EXPECT_EQ(4, sequencingParams.imagesPerSheet);  // Duplex
        }));
    EXPECT_CALL(*layoutFilterIntent_, setNupLayout(_))
        .WillOnce(Invoke([](const dune::imaging::types::NUpParams nUpParams) -> void {
            EXPECT_EQ(dune::imaging::types::NumberUp::TWO_UP, nUpParams.getMode());
        }));
    EXPECT_CALL(*layoutFilterIntent_, setImageRotation(_))
        .WillRepeatedly(Invoke([](const dune::imaging::types::RotationCW &rotation) -> void {
            EXPECT_EQ(dune::imaging::types::RotationCW::ROTATE_0, rotation);
        }));

    // Setup Layout Filter Intent
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupLayoutFilterIntent(layoutFilterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupLayoutFilterIntentCalled_Enterprise_ThenIntentIsSet)
{
    // Expectations
    EXPECT_CALL(*layoutFilterIntent_, setSequencingParams(_))
        .WillOnce(Invoke([](const dune::imaging::Resources::LayoutSequencingParams &sequencingParams) -> void {
            EXPECT_EQ(1, sequencingParams.collationCopies);
            EXPECT_EQ(1, sequencingParams.uncollationCopies);
            EXPECT_EQ(0, sequencingParams.pagesNeededToSequence);
            EXPECT_EQ(false, sequencingParams.waitForSheet);
            EXPECT_EQ(false, sequencingParams.updateDetails);
            EXPECT_EQ(2, sequencingParams.imagesPerSheet);  // Duplex
        }));
    EXPECT_CALL(*layoutFilterIntent_, setNupLayout(_))
        .WillOnce(Invoke([](const dune::imaging::types::NUpParams nUpParams) -> void {
            EXPECT_EQ(dune::imaging::types::NumberUp::TWO_UP, nUpParams.getMode());
        }));
    EXPECT_CALL(*layoutFilterIntent_, setDecompressImage(_))
        .WillRepeatedly(Invoke([](bool decompressImage) -> void {
            EXPECT_EQ(true, decompressImage);
        }));
    EXPECT_CALL(*layoutFilterIntent_, setImageBorders(_))
        .WillOnce(Invoke([](const dune::imaging::types::ImageBorders imageBorders) -> void {
            EXPECT_EQ(dune::imaging::types::ImageBorders::PRINT_BORDERS, imageBorders);
        }));

    // Setup Layout Filter Intent
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setImageBorder(dune::imaging::types::ImageBorder::DefaultLineBorder);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupLayoutFilterIntent(layoutFilterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupLayoutFilterIntentCalledWithPortraitFourUp_Enterprise_ThenIntentIsSet)
{
    // Expectations
    EXPECT_CALL(*layoutFilterIntent_, setNupLayout(_))
        .WillOnce(Invoke([](const dune::imaging::types::NUpParams nUpParams) -> void {
            EXPECT_EQ(dune::imaging::types::NumberUp::FOUR_UP, nUpParams.getMode());
            EXPECT_EQ(dune::imaging::types::NumberUpPageOrder::DOWN_THEN_RIGHT, nUpParams.getOrder());
        }));
    // Setup Layout Filter Intent
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::FourUp);
    jobTicket->getIntent()->setContentOrientation(dune::imaging::types::ContentOrientation::PORTRAIT);
    jobTicket->getIntent()->setNumberUpPresentationDirection(dune::imaging::types::NumberUpPresentationDirection::ToBottomToRight);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupLayoutFilterIntent(layoutFilterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupLayoutFilterIntentCalledWithLandScapeFourUp_Enterprise_ThenIntentIsSet)
{
    // Expectations
    EXPECT_CALL(*layoutFilterIntent_, setNupLayout(_))
        .WillOnce(Invoke([](const dune::imaging::types::NUpParams nUpParams) -> void {
            EXPECT_EQ(dune::imaging::types::NumberUp::FOUR_UP, nUpParams.getMode());
            EXPECT_EQ(dune::imaging::types::NumberUpPageOrder::DOWN_THEN_LEFT, nUpParams.getOrder());
        }));
    // Setup Layout Filter Intent
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::FourUp);
    jobTicket->getIntent()->setContentOrientation(dune::imaging::types::ContentOrientation::LANDSCAPE);
    jobTicket->getIntent()->setNumberUpPresentationDirection(dune::imaging::types::NumberUpPresentationDirection::ToRightToBottom);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupLayoutFilterIntent(layoutFilterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupLayoutFilterIntentCalledWithWatermarkSettings_ThenWatermarkParamsAreSetCorrectly)
{
    // Arrange
    auto jobTicket = std::make_shared<CopyJobTicket>();

    // Configure the watermark settings in the job ticket
    dune::imaging::types::WatermarkSettingsT watermarkSettings;
    watermarkSettings.type = dune::imaging::types::WatermarkType::TEXT_WATERMARK;
    watermarkSettings.customText = "CONFIDENTIAL";
    watermarkSettings.textFont = dune::imaging::types::StampWatermarkTextFont::ANTIQUE_OLIVE;
    watermarkSettings.textColor = dune::imaging::types::StampWatermarkTextColor::RED;
    watermarkSettings.onlyFirstPage = false;
    watermarkSettings.textSize = dune::imaging::types::StampWatermarkTextSize::TWENTY_POINT;
    watermarkSettings.rotate45 = true;
    watermarkSettings.darkness = 5;
    watermarkSettings.backgroundPattern = dune::imaging::types::BackgroundPattern::FLAT;

    jobTicket->getIntent()->setWatermarkSettings(watermarkSettings);

    // Mock layout filter intent
    EXPECT_CALL(*layoutFilterIntent_, setWatermark(testing::_))
        .WillOnce(testing::Invoke([&watermarkSettings](const dune::imaging::types::WatermarkParams& actualParams) {
            // Assert that the actual parameters match the expected settings
            EXPECT_EQ(actualParams.text, watermarkSettings.customText);
            EXPECT_EQ(actualParams.typeface, watermarkSettings.textFont);
            EXPECT_EQ(actualParams.fontColor, watermarkSettings.textColor);
            EXPECT_EQ(actualParams.firstPageOnly, watermarkSettings.onlyFirstPage);
            EXPECT_EQ(actualParams.fontSize, 200); // Corresponds to TWENTY_POINT
            EXPECT_EQ(actualParams.rotation, 315); // Set to -45 degrees if rotate45 is true
            EXPECT_EQ(actualParams.darkness, 255); // 51 * darkness (5)
            EXPECT_EQ(actualParams.pattern, watermarkSettings.backgroundPattern);
        }));

    // Act
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupLayoutFilterIntent(layoutFilterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupLayoutFilterIntentCalledWithStampSettings_ThenStampParamsAreSetCorrectly)
{
    // Arrange
    auto jobTicket = std::make_shared<CopyJobTicket>();

    // Configure the stamp settings in the job ticket
    dune::imaging::types::ScanStampLocationFbT stampSettings;

    std::vector<std::unique_ptr<dune::imaging::types::StampContentT>> stampContents{};
    auto contentFBT = std::make_unique<dune::imaging::types::StampContentT>();
    contentFBT->stampId = dune::imaging::types::StampType::USER_DEFINED_1;
    contentFBT->customText = "userDefined1";
    stampContents.emplace_back(std::move(contentFBT));

    stampSettings.stampLocation = dune::imaging::types::StampLocation::TOP_LEFT;
    stampSettings.stampPolicy = dune::imaging::types::StampPolicy::NONE;
    stampSettings.stampContents = std::move(stampContents);
    stampSettings.stampTextColor = dune::imaging::types::StampWatermarkTextColor::YELLOW;
    stampSettings.stampTextFont = dune::imaging::types::StampWatermarkTextFont::ANTIQUE_OLIVE;
    stampSettings.stampTextSize = dune::imaging::types::StampWatermarkTextSize::EIGHT_POINT;
    stampSettings.stampStartingPage = 5;
    stampSettings.stampStartingNumber = 5;
    stampSettings.stampNumberOfDigits = 5;
    stampSettings.stampPageNumberingStyle = dune::imaging::types::PageNumberingStyle::NUMBER;
    stampSettings.stampWhiteBackground = false;
    std::shared_ptr<dune::framework::core::time::MockIDateTime> mockDateTime_ = std::make_shared<dune::framework::core::time::MockIDateTime>();
        
    jobTicket->getIntent()->setStampTopLeft(stampSettings);
    

    // Mock layout filter intent
    EXPECT_CALL(*layoutFilterIntent_, addStamp(testing::_))
        .WillOnce(testing::Invoke([&stampSettings](const dune::imaging::types::StampParams& actualParams) -> bool {
            // Assert that the actual parameters match the expected settings
            EXPECT_EQ(actualParams.stampContents[0].stampId, dune::imaging::types::StampType::USER_DEFINED_1);
            EXPECT_EQ(actualParams.stampContents[0].customText, "userDefined1");
            EXPECT_EQ(actualParams.typeface, stampSettings.stampTextFont);
            EXPECT_EQ(actualParams.fontColor, stampSettings.stampTextColor);
            EXPECT_EQ(actualParams.fontSize, 80); // Corresponds to EIGHT_POINT
            EXPECT_EQ(actualParams.position, dune::imaging::types::PagePosition::UPPER_LEFT);
            EXPECT_EQ(actualParams.whiteBackground, stampSettings.stampWhiteBackground);
            EXPECT_EQ(actualParams.startingPage, stampSettings.stampStartingPage);
            return true;
        }));

    // Act
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, mockDateTime_.get());
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupLayoutFilterIntent(layoutFilterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupLayoutFilterIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupLayoutFilterIntent(layoutFilterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalledWith300XOverwrite)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    auto intent = jobTicket->getIntent();
    intent->setScanXResolution(dune::imaging::types::Resolution::E150DPI);
    intent->setScanYResolution(dune::imaging::types::Resolution::E150DPI);
    intent->setScanSource(dune::scan::types::ScanSource::MDF);
    ON_CALL(*scanDeviceIntent_, getScanXResolution()).WillByDefault(Return(dune::imaging::types::Resolution::E150DPI));
    ON_CALL(*scanDeviceIntent_, getScanYResolution()).WillByDefault(Return(dune::imaging::types::Resolution::E300DPI));

    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(scanDeviceIntent_->getScanXResolution(), dune::imaging::types::Resolution::E150DPI);
    EXPECT_EQ(scanDeviceIntent_->getScanYResolution(), dune::imaging::types::Resolution::E300DPI);
}


TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalledWithFlatbedDuplexScanBackside)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);

    dune::scan::types::DuplexSideEnum duplexSide;
    EXPECT_CALL(*scanDeviceIntent_, setScanDuplexSide(_))
        .WillRepeatedly(
            testing::Invoke([this, &duplexSide](dune::scan::types::DuplexSideEnum value) -> void {
                duplexSide = value;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getScanDuplexSide())
        .WillRepeatedly(
            testing::Invoke([this, &duplexSide]() -> dune::scan::types::DuplexSideEnum {
                return duplexSide ;
            }));

    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->setFlatbedDuplexScanBackSide(true);
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(scanDeviceIntent_->getScanDuplexSide(), dune::scan::types::DuplexSideEnum::BackSide);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupPageAssemblerIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    dune::imaging::types::MediaSizeId mediaSize;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaSizeId(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaSize](dune::imaging::types::MediaSizeId value) -> void {

                mediaSize = value;

            }));

    dune::imaging::types::MediaSource mediaSource;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaSource](dune::imaging::types::MediaSource value) -> void {

                mediaSource = value;

            }));

    dune::imaging::types::MediaIdType mediaIdType;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaType(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaIdType](dune::imaging::types::MediaIdType value) -> void {

                mediaIdType = value;

            }));

    dune::job::JobType jobType;
    EXPECT_CALL(*pageAssemblerIntent_, setJobType(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobType](dune::job::JobType value) -> void {

                jobType = value;

            }));

    dune::imaging::types::PlexBinding plexBinding;
    EXPECT_CALL(*pageAssemblerIntent_, setPlexBindingType(_))

        .WillRepeatedly(

            testing::Invoke([this, &plexBinding](dune::imaging::types::PlexBinding value) -> void {

                plexBinding = value;

            }));

    dune::imaging::types::Plex inputPlex;
    EXPECT_CALL(*pageAssemblerIntent_, setInputDuplexMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &inputPlex](dune::imaging::types::Plex value) -> void {

                inputPlex = value;

            }));

    dune::imaging::types::Plex plex;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputDuplexMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &plex](dune::imaging::types::Plex value) -> void {

                plex = value;

            }));

    uint32_t collationCopies;
    EXPECT_CALL(*pageAssemblerIntent_, setCollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &collationCopies](uint32_t value) -> void {

                collationCopies = value;

            }));

    uint32_t uncollationCopies;
    EXPECT_CALL(*pageAssemblerIntent_, setUnCollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &uncollationCopies](uint32_t value) -> void {

                uncollationCopies = value;

            }));

    dune::imaging::types::Resolution resolution;
    EXPECT_CALL(*pageAssemblerIntent_, setResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &resolution](dune::imaging::types::Resolution value) -> void {

                resolution = value;

            }));
    dune::imaging::types::PrintQuality printQuality;
    EXPECT_CALL(*pageAssemblerIntent_, setPrintQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &printQuality](dune::imaging::types::PrintQuality value) -> void {

                printQuality = value;

            }));
    dune::imaging::types::PrintQuality copyQuality;
    EXPECT_CALL(*pageAssemblerIntent_, setCopyQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &copyQuality](dune::imaging::types::PrintQuality value) -> void {

                copyQuality = value;

            }));

    dune::imaging::types::OriginalContentType originalContentType;
    EXPECT_CALL(*pageAssemblerIntent_, setOriginalContentType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalContentType](dune::imaging::types::OriginalContentType  value) -> void {

                originalContentType = value;

            }));

    uint32_t topMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setTopMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &topMargin](uint32_t value) -> void {

                topMargin = value;

            }));

    uint32_t bottomMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setBottomMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &bottomMargin](uint32_t value) -> void {

                bottomMargin = value;

            }));

    uint32_t leftMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setLeftMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &leftMargin](uint32_t value) -> void {

                leftMargin = value;

            }));

    uint32_t rightMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setRightMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &rightMargin](uint32_t value) -> void {

                rightMargin = value;

            }));

    dune::imaging::types::ContentOrientation contentOrientation;
    EXPECT_CALL(*pageAssemblerIntent_, setContentOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &contentOrientation](dune::imaging::types::ContentOrientation  value) -> void {

                contentOrientation = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupPageAssemblerIntent(pageAssemblerIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupPageAssemblerIntentCalled_WithEnterprise)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);

    dune::imaging::types::MediaSizeId mediaSize;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaSizeId(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaSize](dune::imaging::types::MediaSizeId value) -> void {

                mediaSize = value;

            }));

    

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupPageAssemblerIntent(pageAssemblerIntent_, resourceConfig);
    EXPECT_EQ(mediaSize, dune::imaging::types::MediaSizeId::LETTER);

    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setMatchOriginalOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    
    copyPipelineResourceSetup->setupPageAssemblerIntent(pageAssemblerIntent_, resourceConfig);
    EXPECT_EQ(mediaSize, dune::imaging::types::MediaSizeId::A4);

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupPageAssemblerIntentCalled_WithCompressedMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    dune::imaging::types::MediaSizeId mediaSize;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaSizeId(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaSize](dune::imaging::types::MediaSizeId value) -> void {

                mediaSize = value;

            }));

    dune::imaging::types::MediaSource mediaSource;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaSource](dune::imaging::types::MediaSource value) -> void {

                mediaSource = value;

            }));

    dune::imaging::types::MediaIdType mediaIdType;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaType(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaIdType](dune::imaging::types::MediaIdType value) -> void {

                mediaIdType = value;

            }));

    dune::job::JobType jobType;
    EXPECT_CALL(*pageAssemblerIntent_, setJobType(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobType](dune::job::JobType value) -> void {

                jobType = value;

            }));

    dune::imaging::types::PlexBinding plexBinding;
    EXPECT_CALL(*pageAssemblerIntent_, setPlexBindingType(_))

        .WillRepeatedly(

            testing::Invoke([this, &plexBinding](dune::imaging::types::PlexBinding value) -> void {

                plexBinding = value;

            }));

    dune::imaging::types::Plex plex;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputDuplexMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &plex](dune::imaging::types::Plex value) -> void {

                plex = value;

            }));

    uint32_t collationCopies;
    EXPECT_CALL(*pageAssemblerIntent_, setCollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &collationCopies](uint32_t value) -> void {

                collationCopies = value;

            }));

    uint32_t uncollationCopies;
    EXPECT_CALL(*pageAssemblerIntent_, setUnCollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &uncollationCopies](uint32_t value) -> void {

                uncollationCopies = value;

            }));

    dune::imaging::types::Resolution resolution;
    EXPECT_CALL(*pageAssemblerIntent_, setResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &resolution](dune::imaging::types::Resolution value) -> void {

                resolution = value;

            }));
    dune::imaging::types::PrintQuality printQuality;
    EXPECT_CALL(*pageAssemblerIntent_, setPrintQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &printQuality](dune::imaging::types::PrintQuality value) -> void {

                printQuality = value;

            }));
    dune::imaging::types::PrintQuality copyQuality;
    EXPECT_CALL(*pageAssemblerIntent_, setCopyQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &copyQuality](dune::imaging::types::PrintQuality value) -> void {

                copyQuality = value;

            }));

    dune::imaging::types::OriginalContentType originalContentType;
    EXPECT_CALL(*pageAssemblerIntent_, setOriginalContentType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalContentType](dune::imaging::types::OriginalContentType  value) -> void {

                originalContentType = value;

            }));

    uint32_t topMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setTopMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &topMargin](uint32_t value) -> void {

                topMargin = value;

            }));

    uint32_t bottomMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setBottomMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &bottomMargin](uint32_t value) -> void {

                bottomMargin = value;

            }));

    uint32_t leftMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setLeftMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &leftMargin](uint32_t value) -> void {

                leftMargin = value;

            }));

    uint32_t rightMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setRightMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &rightMargin](uint32_t value) -> void {

                rightMargin = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupPageAssemblerIntent(pageAssemblerIntent_, resourceConfig);
    copyPipelineResourceSetup->setCollateMode(CollateMode::COMPRESSED);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupPageAssemblerIntentCalled_WithUnCompressedMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    dune::imaging::types::MediaSizeId mediaSize;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaSizeId(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaSize](dune::imaging::types::MediaSizeId value) -> void {

                mediaSize = value;

            }));

    dune::imaging::types::MediaSource mediaSource;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaSource](dune::imaging::types::MediaSource value) -> void {

                mediaSource = value;

            }));

    dune::imaging::types::MediaIdType mediaIdType;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaType(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaIdType](dune::imaging::types::MediaIdType value) -> void {

                mediaIdType = value;

            }));

    dune::job::JobType jobType;
    EXPECT_CALL(*pageAssemblerIntent_, setJobType(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobType](dune::job::JobType value) -> void {

                jobType = value;

            }));

    dune::imaging::types::PlexBinding plexBinding;
    EXPECT_CALL(*pageAssemblerIntent_, setPlexBindingType(_))

        .WillRepeatedly(

            testing::Invoke([this, &plexBinding](dune::imaging::types::PlexBinding value) -> void {

                plexBinding = value;

            }));

    dune::imaging::types::Plex plex;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputDuplexMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &plex](dune::imaging::types::Plex value) -> void {

                plex = value;

            }));

    uint32_t collationCopies;
    EXPECT_CALL(*pageAssemblerIntent_, setCollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &collationCopies](uint32_t value) -> void {

                collationCopies = value;

            }));

    uint32_t uncollationCopies;
    EXPECT_CALL(*pageAssemblerIntent_, setUnCollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &uncollationCopies](uint32_t value) -> void {

                uncollationCopies = value;

            }));

    dune::imaging::types::Resolution resolution;
    EXPECT_CALL(*pageAssemblerIntent_, setResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &resolution](dune::imaging::types::Resolution value) -> void {

                resolution = value;

            }));
    dune::imaging::types::PrintQuality printQuality;
    EXPECT_CALL(*pageAssemblerIntent_, setPrintQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &printQuality](dune::imaging::types::PrintQuality value) -> void {

                printQuality = value;

            }));
    dune::imaging::types::PrintQuality copyQuality;
    EXPECT_CALL(*pageAssemblerIntent_, setCopyQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &copyQuality](dune::imaging::types::PrintQuality value) -> void {

                copyQuality = value;

            }));

    dune::imaging::types::OriginalContentType originalContentType;
    EXPECT_CALL(*pageAssemblerIntent_, setOriginalContentType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalContentType](dune::imaging::types::OriginalContentType  value) -> void {

                originalContentType = value;

            }));

    uint32_t topMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setTopMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &topMargin](uint32_t value) -> void {

                topMargin = value;

            }));

    uint32_t bottomMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setBottomMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &bottomMargin](uint32_t value) -> void {

                bottomMargin = value;

            }));

    uint32_t leftMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setLeftMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &leftMargin](uint32_t value) -> void {

                leftMargin = value;

            }));

    uint32_t rightMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setRightMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &rightMargin](uint32_t value) -> void {

                rightMargin = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupPageAssemblerIntent(pageAssemblerIntent_, resourceConfig);
    copyPipelineResourceSetup->setCollateMode(CollateMode::UNCOMPRESSED);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImagePersisterIntentCalled_WithCollateOnProPipeline)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    std::string fileName;
    EXPECT_CALL(*imagePersisterIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));

    ON_CALL(*imagePersisterIntent_, getFileName()).WillByDefault(ReturnRef(fileName));

    uint32_t stripHeight;
    EXPECT_CALL(*imagePersisterIntent_, setStripHeight(_))

        .WillRepeatedly(

            testing::Invoke([this, &stripHeight](uint32_t value) -> void {

                stripHeight = value;

            }));

    dune::imaging::types::NotificationStrategy notificationStrategy;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrategy](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrategy = value;

            }));

    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*imagePersisterIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));
    uint32_t compressionFactor;
    EXPECT_CALL(*imagePersisterIntent_, setCompressionFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionFactor](uint32_t value) -> void {

                compressionFactor = value;

            }));

    bool jpegHwEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegHwEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegHwEnable](bool value) -> void {

                jpegHwEnable = value;

            }));
    bool jpegVqEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegVqEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegVqEnable](bool value) -> void {

                jpegVqEnable = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setCollateMode(CollateMode::COMPRESSED);
    copyPipelineResourceSetup->setupImagePersisterIntent(imagePersisterIntent_, resourceConfig);

}


TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupPageAssemblerIntentCalled_WithMixedMediaOutput)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER);

    dune::imaging::types::MediaSizeId mediaSize;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaSizeId(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaSize](dune::imaging::types::MediaSizeId value) -> void {

                mediaSize = value;

            }));

    dune::imaging::types::MediaSource mediaSource;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaSource](dune::imaging::types::MediaSource value) -> void {

                mediaSource = value;

            }));

    dune::imaging::types::MediaIdType mediaIdType;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputMediaType(_))

        .WillRepeatedly(

            testing::Invoke([this, &mediaIdType](dune::imaging::types::MediaIdType value) -> void {

                mediaIdType = value;

            }));

    dune::job::JobType jobType;
    EXPECT_CALL(*pageAssemblerIntent_, setJobType(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobType](dune::job::JobType value) -> void {

                jobType = value;

            }));

    dune::imaging::types::PlexBinding plexBinding;
    EXPECT_CALL(*pageAssemblerIntent_, setPlexBindingType(_))

        .WillRepeatedly(

            testing::Invoke([this, &plexBinding](dune::imaging::types::PlexBinding value) -> void {

                plexBinding = value;

            }));

    dune::imaging::types::Plex plex;
    EXPECT_CALL(*pageAssemblerIntent_, setOutputDuplexMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &plex](dune::imaging::types::Plex value) -> void {

                plex = value;

            }));

    uint32_t collationCopies;
    EXPECT_CALL(*pageAssemblerIntent_, setCollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &collationCopies](uint32_t value) -> void {

                collationCopies = value;

            }));

    uint32_t uncollationCopies;
    EXPECT_CALL(*pageAssemblerIntent_, setUnCollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &uncollationCopies](uint32_t value) -> void {

                uncollationCopies = value;

            }));

    dune::imaging::types::Resolution resolution;
    EXPECT_CALL(*pageAssemblerIntent_, setResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &resolution](dune::imaging::types::Resolution value) -> void {

                resolution = value;

            }));
    dune::imaging::types::PrintQuality printQuality;
    EXPECT_CALL(*pageAssemblerIntent_, setPrintQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &printQuality](dune::imaging::types::PrintQuality value) -> void {

                printQuality = value;

            }));
    dune::imaging::types::PrintQuality copyQuality;
    EXPECT_CALL(*pageAssemblerIntent_, setCopyQuality(_))

        .WillRepeatedly(

            testing::Invoke([this, &copyQuality](dune::imaging::types::PrintQuality value) -> void {

                copyQuality = value;

            }));

    dune::imaging::types::OriginalContentType originalContentType;
    EXPECT_CALL(*pageAssemblerIntent_, setOriginalContentType(_))

        .WillRepeatedly(

            testing::Invoke([this, &originalContentType](dune::imaging::types::OriginalContentType  value) -> void {

                originalContentType = value;

            }));

    bool mixedMediaOutput;
    EXPECT_CALL(*pageAssemblerIntent_, setMixedMediaOutput(_))

        .WillRepeatedly(

            testing::Invoke([this, &mixedMediaOutput](bool value) -> void {

                mixedMediaOutput = value;

            }));

    uint32_t topMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setTopMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &topMargin](uint32_t value) -> void {

                topMargin = value;

            }));

    uint32_t bottomMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setBottomMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &bottomMargin](uint32_t value) -> void {

                bottomMargin = value;

            }));

    uint32_t leftMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setLeftMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &leftMargin](uint32_t value) -> void {

                leftMargin = value;

            }));

    uint32_t rightMargin;
    EXPECT_CALL(*pageAssemblerIntent_, setRightMargin(_))

        .WillRepeatedly(

            testing::Invoke([this, &rightMargin](uint32_t value) -> void {

                rightMargin = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupPageAssemblerIntent(pageAssemblerIntent_, resourceConfig);

    EXPECT_EQ(mixedMediaOutput, true);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenDoPrintEarlyWarningCalledWithoutCapability_UltraFastCopyModeDisabled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaOrientation(dune::imaging::types::MediaOrientation::LANDSCAPE);
    intent->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);   
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY2);
    intent->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setCopies(1);

    std::map<dune::print::engine::EngineAttributeFieldType, dune::print::engine::Variant> engineAttributeFields_ =
        {{dune::print::engine::EngineAttributeFieldType::PRE_RUN_SUPPORTED, dune::print::engine::Variant(false)}};
    std::map<dune::print::engine::FinisherAttributeFieldType, dune::print::engine::Variant> finisherAttributeFields_ =
        {{dune::print::engine::FinisherAttributeFieldType::FINISHER_ATTRIBUTE_NONE, dune::print::engine::Variant(0)}};
    std::shared_ptr<dune::print::engine::Capabilities> testCapabilities_ =
        std::make_shared<dune::print::engine::Capabilities>(engineAttributeFields_, finisherAttributeFields_);    
    EXPECT_CALL(*mockICapabilitiesFactory_, getCapabilities()).WillRepeatedly(Return(testCapabilities_));
    
    EXPECT_CALL(*pageAssemblerIntent_, setUltraFastCopyMode(false));

    // Act
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->doPrintEarlyWarning(pageAssemblerIntent_, false);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenDoPrintEarlyWarningCalledWithBasicModeFalse_UltraFastCopyModeDisabled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaOrientation(dune::imaging::types::MediaOrientation::LANDSCAPE);
    intent->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);   
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY2);
    intent->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setCopies(1);

    std::map<dune::print::engine::EngineAttributeFieldType, dune::print::engine::Variant> engineAttributeFields_ =
        {{dune::print::engine::EngineAttributeFieldType::PRE_RUN_SUPPORTED, dune::print::engine::Variant(true)}};
    std::map<dune::print::engine::FinisherAttributeFieldType, dune::print::engine::Variant> finisherAttributeFields_ =
        {{dune::print::engine::FinisherAttributeFieldType::FINISHER_ATTRIBUTE_NONE, dune::print::engine::Variant(0)}};
    std::shared_ptr<dune::print::engine::Capabilities> testCapabilities_ =
        std::make_shared<dune::print::engine::Capabilities>(engineAttributeFields_, finisherAttributeFields_);    
    EXPECT_CALL(*mockICapabilitiesFactory_, getCapabilities()).WillRepeatedly(Return(testCapabilities_));

    std::map<dune::print::engine::PrintIntentFieldType, dune::print::engine::Variant> printIntentsJobFields = {
        {dune::print::engine::PrintIntentFieldType::PAGE_ID, dune::print::engine::INVALID_PAGE_UID},
        {dune::print::engine::PrintIntentFieldType::EARLY_INTENTS_ULTRA_FAST_COPY_METADATA_ADDRESS, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::EARLY_INTENTS_ULTRA_FAST_COPY_METADATA_ADDRESS_ALIGNED, dune::print::engine::Variant(0)}
    };
    std::shared_ptr<dune::print::engine::PrintIntents> printIntentsEarlyIntents = std::make_shared<dune::print::engine::PrintIntents>(printIntentsJobFields);
    EXPECT_CALL(*mockIPrintIntentsFactory_, createPrintIntentsEarlyIntents()).WillRepeatedly(Return(printIntentsEarlyIntents));

    EXPECT_CALL(*mockIPrint_, earlyWarning(testing::An<const std::shared_ptr<dune::print::engine::PrintIntents> &>())).Times(1);

    EXPECT_CALL(*pageAssemblerIntent_, getBasicCopyMode()).WillRepeatedly(Return(false));    
    EXPECT_CALL(*pageAssemblerIntent_, setUltraFastCopyMode(false));

    // Act
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->doPrintEarlyWarning(pageAssemblerIntent_, false);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenDoPrintEarlyWarningCalledWithActiveJob_UltraFastCopyModeDisabled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaOrientation(dune::imaging::types::MediaOrientation::LANDSCAPE);
    intent->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);   
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY2);
    intent->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setCopies(1);

    std::map<dune::print::engine::EngineAttributeFieldType, dune::print::engine::Variant> engineAttributeFields_ =
        {{dune::print::engine::EngineAttributeFieldType::PRE_RUN_SUPPORTED, dune::print::engine::Variant(true)}};
    std::map<dune::print::engine::FinisherAttributeFieldType, dune::print::engine::Variant> finisherAttributeFields_ =
        {{dune::print::engine::FinisherAttributeFieldType::FINISHER_ATTRIBUTE_NONE, dune::print::engine::Variant(0)}};
    std::shared_ptr<dune::print::engine::Capabilities> testCapabilities_ =
        std::make_shared<dune::print::engine::Capabilities>(engineAttributeFields_, finisherAttributeFields_);    
    EXPECT_CALL(*mockICapabilitiesFactory_, getCapabilities()).WillRepeatedly(Return(testCapabilities_));

    std::list<std::shared_ptr<dune::job::IJob>> jobs;
    auto activeJob = std::make_shared<dune::job::MockIJob>();
    EXPECT_CALL(*activeJob, getStateType())
                .WillRepeatedly(Return(dune::job::JobStateType::PROCESSING));  // Active job
    jobs.push_back(activeJob);
    EXPECT_CALL(*mockIJobQueue_, getJobs(Matcher<std::list<std::shared_ptr<dune::job::IJob>> &>(_)))
        .WillRepeatedly(SetArgReferee<0>(jobs));

    std::map<dune::print::engine::PrintIntentFieldType, dune::print::engine::Variant> printIntentsJobFields = {
        {dune::print::engine::PrintIntentFieldType::PAGE_ID, dune::print::engine::INVALID_PAGE_UID},
        {dune::print::engine::PrintIntentFieldType::EARLY_INTENTS_ULTRA_FAST_COPY_METADATA_ADDRESS, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::EARLY_INTENTS_ULTRA_FAST_COPY_METADATA_ADDRESS_ALIGNED, dune::print::engine::Variant(0)}
    };
    std::shared_ptr<dune::print::engine::PrintIntents> printIntentsEarlyIntents = std::make_shared<dune::print::engine::PrintIntents>(printIntentsJobFields);
    EXPECT_CALL(*mockIPrintIntentsFactory_, createPrintIntentsEarlyIntents()).WillRepeatedly(Return(printIntentsEarlyIntents));

    EXPECT_CALL(*mockIPrint_, earlyWarning(testing::An<const std::shared_ptr<dune::print::engine::PrintIntents> &>())).Times(1);

    EXPECT_CALL(*pageAssemblerIntent_, getBasicCopyMode()).WillRepeatedly(Return(true));    
    EXPECT_CALL(*pageAssemblerIntent_, setUltraFastCopyMode(false));

    // Act
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->doPrintEarlyWarning(pageAssemblerIntent_, false);
}


TEST_F(GivenCopyPipelineResourcesSetup, WhenDoPrintEarlyWarningCalled_UltraFastCopyModeEnabled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaOrientation(dune::imaging::types::MediaOrientation::LANDSCAPE);
    intent->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);   
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY2);
    intent->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    intent->setCopies(1);

    std::map<dune::print::engine::EngineAttributeFieldType, dune::print::engine::Variant> engineAttributeFields_ =
        {{dune::print::engine::EngineAttributeFieldType::PRE_RUN_SUPPORTED, dune::print::engine::Variant(true)}};
    std::map<dune::print::engine::FinisherAttributeFieldType, dune::print::engine::Variant> finisherAttributeFields_ =
        {{dune::print::engine::FinisherAttributeFieldType::FINISHER_ATTRIBUTE_NONE, dune::print::engine::Variant(0)}};
    std::shared_ptr<dune::print::engine::Capabilities> testCapabilities_ =
        std::make_shared<dune::print::engine::Capabilities>(engineAttributeFields_, finisherAttributeFields_);    
    EXPECT_CALL(*mockICapabilitiesFactory_, getCapabilities()).WillRepeatedly(Return(testCapabilities_));

    std::list<std::shared_ptr<dune::job::IJob>> jobs;
    EXPECT_CALL(*mockIJobQueue_, getJobs(Matcher<std::list<std::shared_ptr<dune::job::IJob>> &>(_)))
        .WillRepeatedly(SetArgReferee<0>(jobs));

    std::map<dune::print::engine::PrintIntentFieldType, dune::print::engine::Variant> printIntentsJobFields = {
        {dune::print::engine::PrintIntentFieldType::PAGE_ID, dune::print::engine::INVALID_PAGE_UID},
        {dune::print::engine::PrintIntentFieldType::EARLY_INTENTS_ULTRA_FAST_COPY_METADATA_ADDRESS, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::EARLY_INTENTS_ULTRA_FAST_COPY_METADATA_ADDRESS_ALIGNED, dune::print::engine::Variant(0)}
    };
    std::shared_ptr<dune::print::engine::PrintIntents> printIntentsEarlyIntents = std::make_shared<dune::print::engine::PrintIntents>(printIntentsJobFields);
    EXPECT_CALL(*mockIPrintIntentsFactory_, createPrintIntentsEarlyIntents()).WillRepeatedly(Return(printIntentsEarlyIntents));

    EXPECT_CALL(*mockIPrint_, earlyWarning(testing::An<const std::shared_ptr<dune::print::engine::PrintIntents> &>())).Times(1);

    EXPECT_CALL(*pageAssemblerIntent_, getBasicCopyMode()).WillRepeatedly(Return(true));    
    EXPECT_CALL(*pageAssemblerIntent_, setUltraFastCopyMode(true));

    // Act
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    copyPipelineResourceSetup->doPrintEarlyWarning(pageAssemblerIntent_, false);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupPrintDeviceIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    dune::job::JobType jobType;
    EXPECT_CALL(*printDeviceIntent_, setJobType(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobType](dune::job::JobType value) -> void {

                jobType = value;

            }));

    uint32_t collationCopies;
    EXPECT_CALL(*printDeviceIntent_, setCollationCopies(_,_))

        .WillRepeatedly(

            testing::Invoke([this, &collationCopies](uint32_t value, bool mustHonour) -> void {

                collationCopies = value;

            }));

    uint32_t uncollationCopies;
    EXPECT_CALL(*printDeviceIntent_, setUncollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &uncollationCopies](uint32_t value) -> void {

                uncollationCopies = value;

            }));

    uint32_t jobPageCount;
    EXPECT_CALL(*printDeviceIntent_, setJobPageCount(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobPageCount](uint32_t value) -> void {

                jobPageCount = value;

            }));

    bool isCollationJob{false};
    EXPECT_CALL(*printDeviceIntent_, setIsCollationJob(_))

        .WillRepeatedly(

            testing::Invoke([this, &isCollationJob](bool value) -> void {

                isCollationJob = value;

            }));

   dune::imaging::types::JobOffsetMode JobOffsetMode{dune::imaging::types::JobOffsetMode::MODE_DISABLE};
    EXPECT_CALL(*printDeviceIntent_, setJobOffsetMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &JobOffsetMode](dune::imaging::types::JobOffsetMode value) -> void {

                JobOffsetMode = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupPrintDeviceIntent(printDeviceIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupPrintDeviceIntentCalled_WithCompressedMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    dune::job::JobType jobType;
    EXPECT_CALL(*printDeviceIntent_, setJobType(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobType](dune::job::JobType value) -> void {

                jobType = value;

            }));

    uint32_t collationCopies;
    EXPECT_CALL(*printDeviceIntent_, setCollationCopies(_,_))

        .WillRepeatedly(

            testing::Invoke([this, &collationCopies](uint32_t value, bool mustHonour) -> void {

                collationCopies = value;

            }));

    uint32_t uncollationCopies;
    EXPECT_CALL(*printDeviceIntent_, setUncollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &uncollationCopies](uint32_t value) -> void {

                uncollationCopies = value;

            }));

    uint32_t jobPageCount;
    EXPECT_CALL(*printDeviceIntent_, setJobPageCount(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobPageCount](uint32_t value) -> void {

                jobPageCount = value;

            }));

    bool isCollationJob{false};
    EXPECT_CALL(*printDeviceIntent_, setIsCollationJob(_))

        .WillRepeatedly(

            testing::Invoke([this, &isCollationJob](bool value) -> void {

                isCollationJob = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupPrintDeviceIntent(printDeviceIntent_, resourceConfig);
    copyPipelineResourceSetup->setCollateMode(CollateMode::COMPRESSED);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupPrintDeviceIntentCalled_WithUncompressedMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    dune::job::JobType jobType;
    EXPECT_CALL(*printDeviceIntent_, setJobType(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobType](dune::job::JobType value) -> void {

                jobType = value;

            }));

    uint32_t collationCopies;
    EXPECT_CALL(*printDeviceIntent_, setCollationCopies(_,_))

        .WillRepeatedly(

            testing::Invoke([this, &collationCopies](uint32_t value, bool mustHonour) -> void {

                collationCopies = value;

            }));

    uint32_t uncollationCopies;
    EXPECT_CALL(*printDeviceIntent_, setUncollatedCopies(_))

        .WillRepeatedly(

            testing::Invoke([this, &uncollationCopies](uint32_t value) -> void {

                uncollationCopies = value;

            }));

    uint32_t jobPageCount;
    EXPECT_CALL(*printDeviceIntent_, setJobPageCount(_))

        .WillRepeatedly(

            testing::Invoke([this, &jobPageCount](uint32_t value) -> void {

                jobPageCount = value;

            }));

    bool isCollationJob{false};
    EXPECT_CALL(*printDeviceIntent_, setIsCollationJob(_))

        .WillRepeatedly(

            testing::Invoke([this, &isCollationJob](bool value) -> void {

                isCollationJob = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupPrintDeviceIntent(printDeviceIntent_, resourceConfig);
    copyPipelineResourceSetup->setCollateMode(CollateMode::UNCOMPRESSED);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupRtpFilterIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupRtpFilterTicketIntent(nullptr, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImagePersisterIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool encodeJpegInRgb;
    EXPECT_CALL(*imagePersisterIntent_, setEncodeJpegInRGB(_))

        .WillRepeatedly(

            testing::Invoke([this, &encodeJpegInRgb](bool value) -> void {

                encodeJpegInRgb = value;

            }));

    bool jpegHwEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegHwEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegHwEnable](bool value) -> void {

                jpegHwEnable = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, getJpegHwEnable())

        .WillRepeatedly(

            testing::Invoke([this, &jpegHwEnable]() -> bool {

                return jpegHwEnable ;

            }));

    bool jpegVqEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegVqEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegVqEnable](bool value) -> void {

                jpegVqEnable = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, getJpegVqEnable())

        .WillRepeatedly(

            testing::Invoke([this, &jpegVqEnable]() -> bool {

                return jpegVqEnable;

            }));

    uint32_t stripHeigth;
    EXPECT_CALL(*imagePersisterIntent_, setStripHeight(_))

        .WillRepeatedly(

            testing::Invoke([this, &stripHeigth](uint32_t value) -> void {

                stripHeigth = value;

            }));

    uint32_t compressionFactor;
    EXPECT_CALL(*imagePersisterIntent_, setCompressionFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionFactor](uint32_t value) -> void {

                compressionFactor = value;

            }));

    dune::imaging::types::NotificationStrategy notificationStrategy;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrategy](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrategy = value;

            }));
    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*imagePersisterIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::Resolution resolution;
    EXPECT_CALL(*imagePersisterIntent_, setResolutionMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &resolution](dune::imaging::types::Resolution value) -> void {

                resolution = value;

            }));

    std::string fileName;
    EXPECT_CALL(*imagePersisterIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));

    ON_CALL(*imagePersisterIntent_, getFileName()).WillByDefault(ReturnRef(fileName));

    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*imagePersisterIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImagePersisterIntent(imagePersisterIntent_, resourceConfig);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    jobTicket->getIntent()->setContentOrientation(dune::imaging::types::ContentOrientation::PORTRAIT);
    EXPECT_CALL(*imagePersisterIntent_, setReorderType(_)).Times(1);
    copyPipelineResourceSetup->setupImagePersisterIntent(imagePersisterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImagePersisterIntentCalled_WithLfpMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setColorMode(dune::imaging::types::ColorMode::COLOR);


    bool encodeJpegInRgb;
    EXPECT_CALL(*imagePersisterIntent_, setEncodeJpegInRGB(_))

        .WillRepeatedly(

            testing::Invoke([this, &encodeJpegInRgb](bool value) -> void {

                encodeJpegInRgb = value;

            }));

    bool jpegHwEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegHwEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegHwEnable](bool value) -> void {

                jpegHwEnable = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, getJpegHwEnable())

        .WillRepeatedly(

            testing::Invoke([this, &jpegHwEnable]() -> bool {

                return jpegHwEnable ;

            }));

    bool jpegVqEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegVqEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegVqEnable](bool value) -> void {

                jpegVqEnable = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, getJpegVqEnable())

        .WillRepeatedly(

            testing::Invoke([this, &jpegVqEnable]() -> bool {

                return jpegVqEnable;

            }));

    uint32_t stripHeigth;
    EXPECT_CALL(*imagePersisterIntent_, setStripHeight(_))

        .WillRepeatedly(

            testing::Invoke([this, &stripHeigth](uint32_t value) -> void {

                stripHeigth = value;

            }));

    uint32_t compressionFactor;
    EXPECT_CALL(*imagePersisterIntent_, setCompressionFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionFactor](uint32_t value) -> void {

                compressionFactor = value;

            }));

    dune::imaging::types::NotificationStrategy notificationStrategy;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrategy](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrategy = value;

            }));
    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*imagePersisterIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::Resolution resolution;
    EXPECT_CALL(*imagePersisterIntent_, setResolutionMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &resolution](dune::imaging::types::Resolution value) -> void {

                resolution = value;

            }));

    std::string fileName;
    EXPECT_CALL(*imagePersisterIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));

    ON_CALL(*imagePersisterIntent_, getFileName()).WillByDefault(ReturnRef(fileName));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::LFP, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->notificationStrategy = dune::imaging::types::NotificationStrategy::OPTIMIZED;
    copyPipelineResourceSetup->setupImagePersisterIntent(imagePersisterIntent_, resourceConfig);

    // Expectations
    EXPECT_EQ(stripHeigth,256);
    EXPECT_EQ(colorMode,dune::imaging::types::ColorMode::COLOR);
    EXPECT_EQ(resolution, dune::imaging::types::Resolution::E600DPI);
    EXPECT_EQ(notificationStrategy, dune::imaging::types::NotificationStrategy::OPTIMIZED);
}


TEST_F(GivenCopyPipelineResourcesSetup, WhenBlankPageSuppressionEnabled_ImaePersisterStrategy)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool encodeJpegInRgb;
    EXPECT_CALL(*imagePersisterIntent_, setEncodeJpegInRGB(_))

        .WillRepeatedly(

            testing::Invoke([this, &encodeJpegInRgb](bool value) -> void {

                encodeJpegInRgb = value;

            }));

    bool jpegHwEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegHwEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegHwEnable](bool value) -> void {

                jpegHwEnable = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, getJpegHwEnable())

        .WillRepeatedly(

            testing::Invoke([this, &jpegHwEnable]() -> bool {

                return jpegHwEnable ;

            }));

    bool jpegVqEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegVqEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegVqEnable](bool value) -> void {

                jpegVqEnable = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, getJpegVqEnable())

        .WillRepeatedly(

            testing::Invoke([this, &jpegVqEnable]() -> bool {

                return jpegVqEnable;

            }));

    uint32_t stripHeigth;
    EXPECT_CALL(*imagePersisterIntent_, setStripHeight(_))

        .WillRepeatedly(

            testing::Invoke([this, &stripHeigth](uint32_t value) -> void {

                stripHeigth = value;

            }));

    uint32_t compressionFactor;
    EXPECT_CALL(*imagePersisterIntent_, setCompressionFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionFactor](uint32_t value) -> void {

                compressionFactor = value;

            }));

    dune::imaging::types::NotificationStrategy notificationStrategy;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrategy](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrategy = value;

            }));
    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*imagePersisterIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::Resolution resolution;
    EXPECT_CALL(*imagePersisterIntent_, setResolutionMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &resolution](dune::imaging::types::Resolution value) -> void {

                resolution = value;

            }));

    std::string fileName;
    EXPECT_CALL(*imagePersisterIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));

    ON_CALL(*imagePersisterIntent_, getFileName()).WillByDefault(ReturnRef(fileName));

    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*imagePersisterIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, setUsableImageDetection(true));

    EXPECT_EQ(intent->getBlankPageDetection(), dune::scan::types::BlankDetectEnum::Disable);

    intent->setBlankPageDetection(dune::scan::types::BlankDetectEnum::DetectAndSupress);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImagePersisterIntent(imagePersisterIntent_, resourceConfig);

    EXPECT_EQ(notificationStrategy, dune::imaging::types::NotificationStrategy::ON_COMPLETED);
    EXPECT_EQ(intent->getBlankPageDetection(), dune::scan::types::BlankDetectEnum::DetectAndSupress);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupBufferImagePersisterIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    uint32_t stripHeigth;
    EXPECT_CALL(*imagePersisterIntent_, setStripHeight(_))

        .WillRepeatedly(

            testing::Invoke([this, &stripHeigth](uint32_t value) -> void {

                stripHeigth = value;

            }));

    dune::imaging::types::NotificationStrategy notificationStrategy;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrategy](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrategy = value;

            }));
    std::string fileName;
    EXPECT_CALL(*imagePersisterIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));

    ON_CALL(*imagePersisterIntent_, getFileName()).WillByDefault(ReturnRef(fileName));
    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*imagePersisterIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupBufferingImagePersisterIntent(imagePersisterIntent_, resourceConfig);

    EXPECT_EQ(stripHeigth, 64);
    EXPECT_EQ(fileFormat, dune::imaging::types::FileFormat::RAW);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupBufferingImagePersisterIntent(imagePersisterIntent_, resourceConfig);
    EXPECT_EQ(stripHeigth, 128);
    EXPECT_NE(fileFormat, dune::imaging::types::FileFormat::RAW);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    jobTicket->getIntent()->setContentOrientation(dune::imaging::types::ContentOrientation::PORTRAIT);
    EXPECT_CALL(*imagePersisterIntent_, setReorderType(_)).Times(1);
    copyPipelineResourceSetup->setupBufferingImagePersisterIntent(imagePersisterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageRetrieverIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool generateStripImage;
    EXPECT_CALL(*imageRetrieverIntent_, setGenerateStripImage(_))

        .WillRepeatedly(

            testing::Invoke([this, &generateStripImage](bool value) -> void {

                generateStripImage = value;

            }));

    bool removeImageWhenFinish;
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(_))

        .WillRepeatedly(

            testing::Invoke([this, &removeImageWhenFinish](bool value) -> void {

                removeImageWhenFinish = value;

            }));

    bool performSequenceOperation;
    uint32_t collationCopies;
    uint32_t uncollationCopies;
    uint32_t pagesToSequence;
    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_))

        .WillRepeatedly(

            testing::Invoke([this, &performSequenceOperation, &collationCopies, &uncollationCopies, &pagesToSequence](
                                std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams) -> void {
                performSequenceOperation = (sequencingParams != nullptr);
                collationCopies = sequencingParams ? sequencingParams->collationCopies : 0;
                uncollationCopies = sequencingParams ? sequencingParams->uncollationCopies : 0;
                pagesToSequence = sequencingParams ? sequencingParams->pagesNeededToSequence : 0;
            }));

    bool checkDuplexRotation;
    EXPECT_CALL(*imageRetrieverIntent_, setCheckDuplexRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &checkDuplexRotation](bool value) -> void {

                checkDuplexRotation = value;

            }));

    bool duplexJob;
    EXPECT_CALL(*imageRetrieverIntent_, setDuplexJob(_))

        .WillRepeatedly(

            testing::Invoke([this, &duplexJob](bool value) -> void {

                duplexJob = value;

            }));

    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*imageRetrieverIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;
            }));

    uint32_t rotationAngle;
    EXPECT_CALL(*imageRetrieverIntent_, setRotationAngle(_))

        .WillRepeatedly(

            testing::Invoke([this, &rotationAngle](uint32_t value) -> void {

                rotationAngle = value;

            }));

    uint32_t scaleDownFactor;
    EXPECT_CALL(*imageRetrieverIntent_, setScaleDownFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &scaleDownFactor](uint32_t value) -> void {

                scaleDownFactor = value;

            }));

    uint32_t workingStrips;
    EXPECT_CALL(*imageRetrieverIntent_, setWorkingStrips(_))

        .WillRepeatedly(

            testing::Invoke([this, &workingStrips](uint32_t value) -> void {

                workingStrips = value;

            }));

    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,nullptr)).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageRetrieverIntentCalledWithMediaHandlingTrueAndMockIsNullptr_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool generateStripImage;
    EXPECT_CALL(*imageRetrieverIntent_, setGenerateStripImage(_))

        .WillRepeatedly(

            testing::Invoke([this, &generateStripImage](bool value) -> void {

                generateStripImage = value;

            }));

    bool removeImageWhenFinish;
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(_))

        .WillRepeatedly(

            testing::Invoke([this, &removeImageWhenFinish](bool value) -> void {

                removeImageWhenFinish = value;

            }));

    bool performSequenceOperation;
    uint32_t collationCopies;
    uint32_t uncollationCopies;
    uint32_t pagesToSequence;
    bool     performMediaHandlingCheck;
    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_))

        .WillRepeatedly(

            testing::Invoke([this, &performSequenceOperation, &collationCopies, &uncollationCopies, &pagesToSequence, &performMediaHandlingCheck](
                                std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams) -> void {
                performSequenceOperation = (sequencingParams != nullptr);
                collationCopies = sequencingParams ? sequencingParams->collationCopies : 0;
                uncollationCopies = sequencingParams ? sequencingParams->uncollationCopies : 0;
                pagesToSequence = sequencingParams ? sequencingParams->pagesNeededToSequence : 0;
                performMediaHandlingCheck = sequencingParams ? sequencingParams->performMediaHandling : false;
            }));

    bool checkDuplexRotation;
    EXPECT_CALL(*imageRetrieverIntent_, setCheckDuplexRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &checkDuplexRotation](bool value) -> void {

                checkDuplexRotation = value;

            }));

    bool duplexJob;
    EXPECT_CALL(*imageRetrieverIntent_, setDuplexJob(_))

        .WillRepeatedly(

            testing::Invoke([this, &duplexJob](bool value) -> void {

                duplexJob = value;

            }));

    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*imageRetrieverIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;
            }));

    uint32_t rotationAngle;
    EXPECT_CALL(*imageRetrieverIntent_, setRotationAngle(_))

        .WillRepeatedly(

            testing::Invoke([this, &rotationAngle](uint32_t value) -> void {

                rotationAngle = value;

            }));

    uint32_t scaleDownFactor;
    EXPECT_CALL(*imageRetrieverIntent_, setScaleDownFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &scaleDownFactor](uint32_t value) -> void {

                scaleDownFactor = value;

            }));

    uint32_t workingStrips;
    EXPECT_CALL(*imageRetrieverIntent_, setWorkingStrips(_))

        .WillRepeatedly(

            testing::Invoke([this, &workingStrips](uint32_t value) -> void {

                workingStrips = value;

            }));

    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,nullptr)).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->doMediaHandlingCheck = true;
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);
    EXPECT_TRUE(performMediaHandlingCheck);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageRetrieverIntentCalledWithMediaHandlingTrueAndMockIsOk_WithBasicMode)
{
    services_.mediaHandlingMgr = mockIMediaHandlingMgr_.get();

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool generateStripImage;
    EXPECT_CALL(*imageRetrieverIntent_, setGenerateStripImage(_))

        .WillRepeatedly(

            testing::Invoke([this, &generateStripImage](bool value) -> void {

                generateStripImage = value;

            }));

    bool removeImageWhenFinish;
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(_))

        .WillRepeatedly(

            testing::Invoke([this, &removeImageWhenFinish](bool value) -> void {

                removeImageWhenFinish = value;

            }));

    bool performSequenceOperation;
    uint32_t collationCopies;
    uint32_t uncollationCopies;
    uint32_t pagesToSequence;
    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_))

        .WillRepeatedly(

            testing::Invoke([this, &performSequenceOperation, &collationCopies, &uncollationCopies, &pagesToSequence](
                                std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams) -> void {
                performSequenceOperation = (sequencingParams != nullptr);
                collationCopies = sequencingParams ? sequencingParams->collationCopies : 0;
                uncollationCopies = sequencingParams ? sequencingParams->uncollationCopies : 0;
                pagesToSequence = sequencingParams ? sequencingParams->pagesNeededToSequence : 0;
            }));

    bool checkDuplexRotation;
    EXPECT_CALL(*imageRetrieverIntent_, setCheckDuplexRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &checkDuplexRotation](bool value) -> void {

                checkDuplexRotation = value;

            }));

    bool duplexJob;
    EXPECT_CALL(*imageRetrieverIntent_, setDuplexJob(_))

        .WillRepeatedly(

            testing::Invoke([this, &duplexJob](bool value) -> void {

                duplexJob = value;

            }));

    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*imageRetrieverIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;
            }));

    uint32_t rotationAngle;
    EXPECT_CALL(*imageRetrieverIntent_, setRotationAngle(_))

        .WillRepeatedly(

            testing::Invoke([this, &rotationAngle](uint32_t value) -> void {

                rotationAngle = value;

            }));

    uint32_t scaleDownFactor;
    EXPECT_CALL(*imageRetrieverIntent_, setScaleDownFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &scaleDownFactor](uint32_t value) -> void {

                scaleDownFactor = value;

            }));

    uint32_t workingStrips;
    EXPECT_CALL(*imageRetrieverIntent_, setWorkingStrips(_))

        .WillRepeatedly(

            testing::Invoke([this, &workingStrips](uint32_t value) -> void {

                workingStrips = value;

            }));

    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,mockIMediaHandlingMgr_.get())).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->doMediaHandlingCheck = true;
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageRetrieverIntentCalled_ForEnterprise)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    // 2up, duplex, 3 collate copies
    intent->setCopies(3);
    intent->setCollate(dune::copy::SheetCollate::Collate);
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    intent->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);

    uint32_t rotationAngle;
    EXPECT_CALL(*imageRetrieverIntent_, setRotationAngle(_))

        .WillRepeatedly(

            testing::Invoke([this, &rotationAngle](uint32_t value) -> void {

                rotationAngle = value;

            }));

    bool removeImageWhenFinish;
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(_))

        .WillRepeatedly(

            testing::Invoke([this, &removeImageWhenFinish](bool value) -> void {

                removeImageWhenFinish = value;

            }));

    bool perfromSequenceOperation;
    uint32_t collationCopies;
    uint32_t uncollationCopies;
    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_))

        .WillRepeatedly(

            testing::Invoke([this, &perfromSequenceOperation, &collationCopies, &uncollationCopies](
                                std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams) -> void {
                perfromSequenceOperation = (sequencingParams != nullptr);
                collationCopies = sequencingParams ? sequencingParams->collationCopies : 0;
                uncollationCopies = sequencingParams ? sequencingParams->uncollationCopies : 0;
            }));

    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,nullptr)).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setCollateMode(CollateMode::UNCOMPRESSED);
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);

    EXPECT_EQ(0, rotationAngle);
    EXPECT_EQ(true, removeImageWhenFinish);
    EXPECT_EQ(1, collationCopies);
    EXPECT_EQ(1, uncollationCopies);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageRetrieverIntentCalledWithMediaHandlingTrueAndMockIsOk_WithLfpMode)
{
    services_.mediaHandlingMgr = mockIMediaHandlingMgr_.get();

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool generateStripImage;
    EXPECT_CALL(*imageRetrieverIntent_, setGenerateStripImage(_))
        .WillRepeatedly(
            testing::Invoke([this, &generateStripImage](bool value) -> void {
                generateStripImage = value;
            }));

    bool removeImageWhenFinish;
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(_))
        .WillRepeatedly(
            testing::Invoke([this, &removeImageWhenFinish](bool value) -> void {
                removeImageWhenFinish = value;
            }));

    bool performSequenceOperation;
    uint32_t collationCopies;
    uint32_t uncollationCopies;
    uint32_t pagesToSequence;
    bool     performMediaHandling;
    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_))
        .WillRepeatedly(
            testing::Invoke([this, &performSequenceOperation, &collationCopies, &uncollationCopies, &pagesToSequence, &performMediaHandling](
                                std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams) -> void {
                performSequenceOperation = (sequencingParams != nullptr);
                collationCopies = sequencingParams ? sequencingParams->collationCopies : 0;
                uncollationCopies = sequencingParams ? sequencingParams->uncollationCopies : 0;
                performMediaHandling = sequencingParams ? sequencingParams->performMediaHandling : false;
            }));

    bool checkDuplexRotation;
    EXPECT_CALL(*imageRetrieverIntent_, setCheckDuplexRotation(_))
        .WillRepeatedly(
            testing::Invoke([this, &checkDuplexRotation](bool value) -> void {
                checkDuplexRotation = value;
            }));

    bool duplexJob = false;
    EXPECT_CALL(*imageRetrieverIntent_, setDuplexJob(_))
        .WillRepeatedly(
            testing::Invoke([this, &duplexJob](bool value) -> void {
                duplexJob = value;
            }));

    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*imageRetrieverIntent_, setScanImagingProfile(_))
        .WillRepeatedly(
            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {
                scanImagingProfileType = value;
            }));

    uint32_t rotationAngle;
    EXPECT_CALL(*imageRetrieverIntent_, setRotationAngle(_))
        .WillRepeatedly(
            testing::Invoke([this, &rotationAngle](uint32_t value) -> void {
                rotationAngle = value;
            }));

    uint32_t scaleDownFactor;
    EXPECT_CALL(*imageRetrieverIntent_, setScaleDownFactor(_))
        .WillRepeatedly(
            testing::Invoke([this, &scaleDownFactor](uint32_t value) -> void {
                scaleDownFactor = value;
            }));

    uint32_t workingStrips;
    EXPECT_CALL(*imageRetrieverIntent_, setWorkingStrips(_))
        .WillRepeatedly(
            testing::Invoke([this, &workingStrips](uint32_t value) -> void {
                workingStrips = value;
            }));

    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,mockIMediaHandlingMgr_.get())).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::LFP, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->doMediaHandlingCheck = true;
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);

    EXPECT_TRUE(generateStripImage);
    EXPECT_FALSE(removeImageWhenFinish);
    EXPECT_TRUE(performSequenceOperation);
    EXPECT_EQ(1, collationCopies);
    EXPECT_EQ(1, uncollationCopies);
    EXPECT_TRUE(performMediaHandling);
    EXPECT_FALSE(checkDuplexRotation);
    EXPECT_FALSE(duplexJob);
    EXPECT_EQ(dune::scan::types::ScanImagingProfileType::COPY, scanImagingProfileType);
    EXPECT_EQ(0, rotationAngle);
    EXPECT_EQ(1, scaleDownFactor);
    EXPECT_EQ(3, workingStrips);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenOneUpUncollateCopy_ThenImageDoesNotPersist)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    intent->setCopies(1);
    intent->setCollate(dune::copy::SheetCollate::Uncollate);

    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(true))
        .Times(2);
    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,nullptr)).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenCollatedOrMultipleCopies_ThenImagePersists)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    intent->setCopies(2);
    intent->setCollate(dune::copy::SheetCollate::Collate);

    // First expect call is due to function always being called regardless of settings.
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(true));
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(false));
    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,nullptr)).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);
}

// This tests has not much sense right now, we need to configure the sequencing operation in ImageRetriever and then
// check the configured copies in its configuration
TEST_F(GivenCopyPipelineResourcesSetup, DISABLED_WhenUncollateOrMultipleCopies_ThenImagePersists)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    intent->setCopies(2);
    intent->setCollate(dune::copy::SheetCollate::Uncollate);

    // auto numCopies = intent->getCopies();

    // First expect call is due to function always being called regardless of settings.
    // EXPECT_CALL(*imageRetrieverIntent_, setUncollationCopies(1));
    // EXPECT_CALL(*imageRetrieverIntent_, setUncollationCopies(numCopies));
    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,nullptr)).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupBufferImageRetrieverIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool generateStripImage;
    EXPECT_CALL(*imageRetrieverIntent_, setGenerateStripImage(_))

        .WillRepeatedly(

            testing::Invoke([this, &generateStripImage](bool value) -> void {

                generateStripImage = value;

            }));

    bool removeImageWhenFinish;
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(_))

        .WillRepeatedly(

            testing::Invoke([this, &removeImageWhenFinish](bool value) -> void {

                removeImageWhenFinish = value;

            }));

    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*imageRetrieverIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;

            }));
    uint32_t rotationAngle;
    EXPECT_CALL(*imageRetrieverIntent_, setRotationAngle(_))

        .WillRepeatedly(

            testing::Invoke([this, &rotationAngle](uint32_t value) -> void {

                rotationAngle = value;

            }));
    
    bool performRotation;
    EXPECT_CALL(*imageRetrieverIntent_, setPerformRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &performRotation](bool value) -> void {

                performRotation = value;

            }));

    uint32_t scaleDownFactor;
    EXPECT_CALL(*imageRetrieverIntent_, setScaleDownFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &scaleDownFactor](uint32_t value) -> void {

                scaleDownFactor = value;

            }));

    uint32_t workingStrips;
    EXPECT_CALL(*imageRetrieverIntent_, setWorkingStrips(_))

        .WillRepeatedly(

            testing::Invoke([this, &workingStrips](uint32_t value) -> void {

                workingStrips = value;

            }));

    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,nullptr)).Times(2);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupBufferingImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);

    EXPECT_CALL(*imageRetrieverIntent_, setDecompressImage(true));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupBufferingImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupBufferImageRetrieverIntentCalledWithMediaHandlingTrueButMockIsNullptr_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool generateStripImage;
    EXPECT_CALL(*imageRetrieverIntent_, setGenerateStripImage(_))

        .WillRepeatedly(

            testing::Invoke([this, &generateStripImage](bool value) -> void {

                generateStripImage = value;

            }));

    bool removeImageWhenFinish;
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(_))

        .WillRepeatedly(

            testing::Invoke([this, &removeImageWhenFinish](bool value) -> void {

                removeImageWhenFinish = value;

            }));

    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*imageRetrieverIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;

            }));
    uint32_t rotationAngle;
    EXPECT_CALL(*imageRetrieverIntent_, setRotationAngle(_))

        .WillRepeatedly(

            testing::Invoke([this, &rotationAngle](uint32_t value) -> void {

                rotationAngle = value;

            }));
    
    bool performRotation;
    EXPECT_CALL(*imageRetrieverIntent_, setPerformRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &performRotation](bool value) -> void {

                performRotation = value;

            }));

    uint32_t scaleDownFactor;
    EXPECT_CALL(*imageRetrieverIntent_, setScaleDownFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &scaleDownFactor](uint32_t value) -> void {

                scaleDownFactor = value;

            }));

    uint32_t workingStrips;
    EXPECT_CALL(*imageRetrieverIntent_, setWorkingStrips(_))

        .WillRepeatedly(

            testing::Invoke([this, &workingStrips](uint32_t value) -> void {

                workingStrips = value;

            }));

    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,nullptr)).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->doMediaHandlingCheck = true;
    copyPipelineResourceSetup->setupBufferingImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupBufferImageRetrieverIntentCalledWithMediaHandlingTrueAndMockIsok_WithBasicMode)
{
    services_.mediaHandlingMgr = mockIMediaHandlingMgr_.get();

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    bool generateStripImage;
    EXPECT_CALL(*imageRetrieverIntent_, setGenerateStripImage(_))

        .WillRepeatedly(

            testing::Invoke([this, &generateStripImage](bool value) -> void {

                generateStripImage = value;

            }));

    bool removeImageWhenFinish;
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(_))

        .WillRepeatedly(

            testing::Invoke([this, &removeImageWhenFinish](bool value) -> void {

                removeImageWhenFinish = value;

            }));

    dune::scan::types::ScanImagingProfileType scanImagingProfileType;
    EXPECT_CALL(*imageRetrieverIntent_, setScanImagingProfile(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanImagingProfileType](dune::scan::types::ScanImagingProfileType value) -> void {

                scanImagingProfileType = value;

            }));

    uint32_t rotationAngle;
    EXPECT_CALL(*imageRetrieverIntent_, setRotationAngle(_))

        .WillRepeatedly(

            testing::Invoke([this, &rotationAngle](uint32_t value) -> void {

                rotationAngle = value;

            }));

    bool performRotation;
    EXPECT_CALL(*imageRetrieverIntent_, setPerformRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &performRotation](bool value) -> void {

                performRotation = value;

            }));

    uint32_t scaleDownFactor;
    EXPECT_CALL(*imageRetrieverIntent_, setScaleDownFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &scaleDownFactor](uint32_t value) -> void {

                scaleDownFactor = value;

            }));

    uint32_t workingStrips;
    EXPECT_CALL(*imageRetrieverIntent_, setWorkingStrips(_))

        .WillRepeatedly(

            testing::Invoke([this, &workingStrips](uint32_t value) -> void {

                workingStrips = value;

            }));

    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,mockIMediaHandlingMgr_.get())).Times(1);
    EXPECT_CALL(*imageRetrieverIntent_, setPerformMediaHandlingChecks(true));
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    resourceConfig->doMediaHandlingCheck = true;
    copyPipelineResourceSetup->setupBufferingImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImagePersisterPreviewIntentCalled_WithBasicMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    uint32_t stripHeigth;
    EXPECT_CALL(*imagePersisterIntent_, setStripHeight(_))

        .WillRepeatedly(

            testing::Invoke([this, &stripHeigth](uint32_t value) -> void {

                stripHeigth = value;

            }));

    dune::imaging::types::NotificationStrategy notificationStrategy;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrategy](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrategy = value;

            }));
    std::string fileName;
    EXPECT_CALL(*imagePersisterIntent_, setFileName(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileName](std::string value) -> void {

                fileName = value;

            }));

    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*imagePersisterIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));

    bool savePreviewMode;
    EXPECT_CALL(*imagePersisterIntent_, setSavePreviewMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &savePreviewMode](bool value) -> void {

                savePreviewMode = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupBufferingImagePersisterIntent(imagePersisterIntent_, resourceConfig);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_WithHomeProADFForScaling2upSetsOutExtents)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();

    intent->setScanSource(ScanSource::ADF_SIMPLEX);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LEGAL);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E300DPI);


    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xExtent](uint32_t value) -> void {

                xExtent = value;

            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yExtent](uint32_t value) -> void {

                yExtent = value;

            }));
    EXPECT_CALL(*scanDeviceIntent_, getXExtent())

        .WillRepeatedly(

            testing::Invoke([this, &xExtent]() -> uint32_t {

                return xExtent ;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())

        .WillRepeatedly(

            testing::Invoke([this, &yExtent]() -> uint32_t {

                return yExtent ;

            }));

    uint32_t xOutExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xOutExtent](uint32_t value) -> void {

                xOutExtent = value;

            }));

    uint32_t yOutExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yOutExtent](uint32_t value) -> void {

                yOutExtent = value;

            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));

    dune::scan::types::ScanSource scanSource;
    EXPECT_CALL(*scanDeviceIntent_, setScanSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanSource](dune::scan::types::ScanSource value) -> void {

                scanSource = value;

            }));

    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*scanDeviceIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::ContentOrientation contentOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &contentOrientation](dune::imaging::types::ContentOrientation  value) -> void {

                contentOrientation = value;

            }));
    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {

                xResolution = value;

            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {

                yResolution = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    uint32_t expectedWidth = (3300 - (desiredMargins_.getTop().get(300) + desiredMargins_.getBottom().get(300)))/2;
    uint32_t expectedHeight = 2550 - (desiredMargins_.getLeft().get(300) + desiredMargins_.getRight().get(300));
    uint32_t newExpectedWidth = (xExtent * xScalePercent )/100;
    uint32_t newExpectedHeight = (yExtent * yScalePercent )/100;

    GTEST_CHECKPOINTA("CopyPipelineResourceSetup: xScalePercent calculated  : %d\n", xScalePercent);
    GTEST_CHECKPOINTA("CopyPipelineResourceSetup: yScalePercent calculated  : %d\n", yScalePercent);
    GTEST_CHECKPOINTA("CopyPipelineResourceSetup: newExpectedWidth calculated  : %d\n", newExpectedWidth);
    GTEST_CHECKPOINTA("CopyPipelineResourceSetup: newExpectedHeight calculated  : %d\n", newExpectedHeight);

    EXPECT_NE(xOutExtent, expectedWidth);
    EXPECT_NE(yOutExtent, expectedHeight);
    EXPECT_EQ(xOutExtent, newExpectedWidth);
    EXPECT_EQ(yOutExtent, newExpectedHeight);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_WithHomeProADFForScalePercentSetsOutExtentInExtents)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    auto intent = jobTicket->getIntent();

    intent->setCollate(dune::copy::SheetCollate::Collate);
    intent->setScanSource(ScanSource::ADF_SIMPLEX);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setXScalePercent(250);
    intent->setYScalePercent(250);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E300DPI);
    jobTicket->setIntent(intent);

    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .Times(3)

        .WillRepeatedly(

            testing::Invoke([this, &xExtent](uint32_t value) -> void {

                xExtent = value;

            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .Times(3)

        .WillRepeatedly(

            testing::Invoke([this, &yExtent](uint32_t value) -> void {

                yExtent = value;

            }));

    uint32_t xOutExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xOutExtent](uint32_t value) -> void {

                xOutExtent = value;

            }));

    uint32_t yOutExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yOutExtent](uint32_t value) -> void {

                yOutExtent = value;

            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));

    dune::scan::types::ScanSource scanSource;
    EXPECT_CALL(*scanDeviceIntent_, setScanSource(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanSource](dune::scan::types::ScanSource value) -> void {

                scanSource = value;

            }));

    dune::imaging::types::ColorMode colorMode;
    EXPECT_CALL(*scanDeviceIntent_, setColorMode(_))

        .WillRepeatedly(

            testing::Invoke([this, &colorMode](dune::imaging::types::ColorMode  value) -> void {

                colorMode = value;

            }));

    dune::imaging::types::ContentOrientation contentOrientation;
    EXPECT_CALL(*scanDeviceIntent_, setOriginalContentOrientation(_))

        .WillRepeatedly(

            testing::Invoke([this, &contentOrientation](dune::imaging::types::ContentOrientation  value) -> void {

                contentOrientation = value;

            }));
    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {

                xResolution = value;

            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {

                yResolution = value;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent()).Times(7);


    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);

    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);
    EXPECT_EQ(jobTicket->getIntent()->getCollate(), dune::copy::SheetCollate::Collate);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_WithHomeProGlassthenCollateIsSetToUncollate)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto intent = jobTicket->getIntent();

    intent->setScanSource(ScanSource::GLASS);
    intent->setCollate(dune::copy::SheetCollate::Collate);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setXScalePercent(250);
    intent->setYScalePercent(250);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E300DPI);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);

    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);
    EXPECT_EQ(jobTicket->getIntent()->getCollate(), dune::copy::SheetCollate::Uncollate);

}

TEST_F(GivenCopyPipelineResourcesSetup, WhenScaleToFitEnable_WithEnterprise_ThenScalingAppliedCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto intent = jobTicket->getIntent();
    intent->setScanSource(ScanSource::GLASS);
    intent->setCollate(dune::copy::SheetCollate::Collate);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A5);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E300DPI);
    intent->setScaleToFitEnabled(true);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, true, maxLengthConfig_, nullptr);

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));
    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);
    int dpi = ConvertToScanTypeHelper::getResolutionIntFromEnum(intent->getOutputXResolution());
    auto inWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(intent->getInputMediaSizeId(), dune::imaging::types::MediaOrientation::PORTRAIT);
    auto outWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(intent->getOutputMediaSizeId(), dune::imaging::types::MediaOrientation::PORTRAIT);
    uint32_t fitToPagePercent = ConvertToScanTypeHelper::getScalingForScaleToFit(inWidthAndHeight.width.get(dpi), inWidthAndHeight.height.get(dpi), outWidthAndHeight.width.get(dpi), outWidthAndHeight.height.get(dpi));

    int expectedScale = fitToPagePercent / 1000;

    EXPECT_EQ(xScalePercent, expectedScale);
    EXPECT_EQ(yScalePercent, expectedScale);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenScaleToFitEnable_WithEnterpriseOutPutMediaAsAny_ThenScalingAppliedCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    ASSERT_NE(nullptr, jobTicket);

    auto intent = jobTicket->getIntent();
    intent->setScanSource(ScanSource::GLASS);
    intent->setCollate(dune::copy::SheetCollate::Collate);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E300DPI);
    intent->setScaleToFitEnabled(true);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, true, maxLengthConfig_, nullptr);

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));
    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);
    int dpi = ConvertToScanTypeHelper::getResolutionIntFromEnum(intent->getOutputXResolution());
    auto inWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(intent->getInputMediaSizeId(), dune::imaging::types::MediaOrientation::PORTRAIT);
    auto outWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(intent->getOutputMediaSizeId(), dune::imaging::types::MediaOrientation::PORTRAIT);

    EXPECT_EQ(xScalePercent, 100);
    EXPECT_EQ(yScalePercent, 100);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenScaleToFitEnableIncludeMargin_WithEnterprise_ThenScalingAppliedCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto intent = jobTicket->getIntent();
    intent->setScanSource(ScanSource::GLASS);
    intent->setCollate(dune::copy::SheetCollate::Collate);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A5);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E300DPI);
    intent->setScaleToFitEnabled(true);
    intent->setFitToPageIncludeMargin(true);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, true, maxLengthConfig_, nullptr);

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));
    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);
    int dpi = ConvertToScanTypeHelper::getResolutionIntFromEnum(intent->getOutputXResolution());
    auto inWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(intent->getInputMediaSizeId(), dune::imaging::types::MediaOrientation::PORTRAIT);
    auto outWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(intent->getOutputMediaSizeId(), dune::imaging::types::MediaOrientation::PORTRAIT);
    uint32_t fitToPagePercent = ConvertToScanTypeHelper::getScalingForScaleToFit(inWidthAndHeight.width.get(dpi), inWidthAndHeight.height.get(dpi), outWidthAndHeight.width.get(dpi), outWidthAndHeight.height.get(dpi));

    int expectedScale = fitToPagePercent / 1000 * 97 / 100;

    EXPECT_EQ(xScalePercent, expectedScale);
    EXPECT_EQ(yScalePercent, expectedScale);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceCalledWith2up_scalingAppliedCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);
    jobTicket->getIntent()->setOutputYResolution(dune::imaging::types::Resolution::E300DPI);
    jobTicket->getIntent()->setScanSource(ScanSource::GLASS);

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));


    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xExtent](uint32_t value) -> void {

                xExtent = value;

            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yExtent](uint32_t value) -> void {

                yExtent = value;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent())

        .WillRepeatedly(

            testing::Invoke([this, &xExtent]() -> uint32_t {

                return xExtent ;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())

        .WillRepeatedly(

            testing::Invoke([this, &yExtent]() -> uint32_t {

                return yExtent ;

            }));

    uint32_t outXExtent = 0;
    EXPECT_CALL(*scanDeviceIntent_, setOutXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &outXExtent](uint32_t value) -> void {

                outXExtent = value;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getOutXExtent())
        .WillRepeatedly( testing::Invoke([this, &outXExtent]() -> uint32_t {
                return outXExtent; }));

    uint32_t outYExtent = 0;
    EXPECT_CALL(*scanDeviceIntent_, setOutYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &outYExtent](uint32_t value) -> void {

                outYExtent = value;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getOutYExtent())
        .WillRepeatedly( testing::Invoke([this, &outYExtent]() -> uint32_t {
              return outYExtent; }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {

                xScalePercent = value;

            }));
    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {

                yScalePercent = value;

            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    //set some specific padding value for testing purposes
    copyPipelineResourceSetup->setTopSpecificPadding(10);
    copyPipelineResourceSetup->setBottomSpecificPadding(10);
    copyPipelineResourceSetup->setLeftSpecificPadding(10);
    copyPipelineResourceSetup->setRightSpecificPadding(10);

    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    //The desired width output of the scaled image is equal to the output media size height divided by 2 because of the rotation.
    //The desired height output of the scaled image is equal to the width of the output media size.
    uint32_t rotatedY = 2550 - (desiredMargins_.getLeft().get(300) + desiredMargins_.getRight().get(300)) - (118 + 118);
    uint32_t rotatedX = (3300 - (desiredMargins_.getTop().get(300) + desiredMargins_.getBottom().get(300)))/2 - (118 + 118);

    int shouldBeScale = ConvertToScanTypeHelper::getScalingForScaleToFit(xExtent, yExtent, rotatedX,  rotatedY)/1000;
    int shouldBeOutXExtent = xExtent * shouldBeScale /100;
    int shouldBeOutYExtent = yExtent * shouldBeScale /100;

    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: xScalePercent calculated  : %d\n", xScalePercent);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: yScalePercent calculated  : %d\n", yScalePercent);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: rotatedX calculated  : %d\n", rotatedX);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: rotatedY calculated  : %d\n", rotatedY);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: shouldBeScale %d\n", shouldBeScale);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: shouldBeOutExtent %d\n", shouldBeOutXExtent);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: shouldBeOutYExtent %d\n", shouldBeOutYExtent);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: XExtent %d\n", xExtent);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: YExtent %d\n", yExtent);



    EXPECT_NE(xExtent, outXExtent);
    EXPECT_NE(yExtent, outYExtent);
    EXPECT_EQ(xScalePercent, yScalePercent);
    EXPECT_NE(outXExtent, 0);
    EXPECT_NE(outYExtent, 0);
    EXPECT_NE(xScalePercent, 0);
    EXPECT_EQ(xScalePercent, shouldBeScale);
    EXPECT_EQ(outXExtent, shouldBeOutXExtent);
    EXPECT_EQ(outYExtent, shouldBeOutYExtent);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceCalledWith2up_Enterprise_SHORTEDGE_scalingAppliedCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setScanSource(ScanSource::GLASS);
    jobTicket->getIntent()->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::SHORTEDGE);

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));


    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;
            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly(
            testing::Invoke([this, &xExtent]() -> uint32_t {
                return xExtent ;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly(
            testing::Invoke([this, &yExtent]() -> uint32_t {
                return yExtent ;
            }));

    uint32_t outXExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &outXExtent](uint32_t value) -> void {
                outXExtent = value;
            }));

    uint32_t outYExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &outYExtent](uint32_t value) -> void {
                outYExtent = value;
            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {
                xScalePercent = value;
            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {
                yScalePercent = value;
            }));

    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))
        .WillRepeatedly(
            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {
                xResolution = value;
            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))
        .WillRepeatedly(
            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {
                yResolution = value;
            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();

    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: xScalePercent calculated  : %d\n", xScalePercent);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: yScalePercent calculated  : %d\n", yScalePercent);

    EXPECT_EQ(xScalePercent, yScalePercent);
    EXPECT_NE(xScalePercent, 0);
    EXPECT_EQ(xScalePercent, 62);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceCalledWith2up_Enterprise_LONGEDGE_scalingAppliedCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setScanSource(ScanSource::GLASS);
    jobTicket->getIntent()->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));


    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;
            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly(
            testing::Invoke([this, &xExtent]() -> uint32_t {
                return xExtent ;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly(
            testing::Invoke([this, &yExtent]() -> uint32_t {
                return yExtent ;
            }));

    uint32_t outXExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &outXExtent](uint32_t value) -> void {
                outXExtent = value;
            }));

    uint32_t outYExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &outYExtent](uint32_t value) -> void {
                outYExtent = value;
            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {
                xScalePercent = value;
            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {
                yScalePercent = value;
            }));

    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))
        .WillRepeatedly(
            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {
                xResolution = value;
            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))
        .WillRepeatedly(
            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {
                yResolution = value;
            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();

    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: xScalePercent calculated  : %d\n", xScalePercent);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: yScalePercent calculated  : %d\n", yScalePercent);

    EXPECT_EQ(xScalePercent, yScalePercent);
    EXPECT_NE(xScalePercent, 0);
    EXPECT_EQ(xScalePercent, 62);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceCalledWith4up_Enterprise_SHORTEDGE_scalingAppliedCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::FourUp);
    jobTicket->getIntent()->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setScanSource(ScanSource::GLASS);
    jobTicket->getIntent()->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::SHORTEDGE);

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));


    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;
            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly(
            testing::Invoke([this, &xExtent]() -> uint32_t {
                return xExtent ;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly(
            testing::Invoke([this, &yExtent]() -> uint32_t {
                return yExtent ;
            }));

    uint32_t outXExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &outXExtent](uint32_t value) -> void {
                outXExtent = value;
            }));

    uint32_t outYExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &outYExtent](uint32_t value) -> void {
                outYExtent = value;
            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {
                xScalePercent = value;
            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {
                yScalePercent = value;
            }));

    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))
        .WillRepeatedly(
            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {
                xResolution = value;
            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))
        .WillRepeatedly(
            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {
                yResolution = value;
            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();

    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: xScalePercent calculated  : %d\n", xScalePercent);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: yScalePercent calculated  : %d\n", yScalePercent);

    EXPECT_EQ(xScalePercent, yScalePercent);
    EXPECT_NE(xScalePercent, 0);
    EXPECT_EQ(xScalePercent, 47);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceCalledWith4up_Enterprise_LONGEDGE_scalingAppliedCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::FourUp);
    jobTicket->getIntent()->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setScanSource(ScanSource::GLASS);
    jobTicket->getIntent()->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);

    bool featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));


    uint32_t xExtent;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;
            }));

    uint32_t yExtent;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly(
            testing::Invoke([this, &xExtent]() -> uint32_t {
                return xExtent ;
            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly(
            testing::Invoke([this, &yExtent]() -> uint32_t {
                return yExtent ;
            }));

    uint32_t outXExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutXExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &outXExtent](uint32_t value) -> void {
                outXExtent = value;
            }));

    uint32_t outYExtent;
    EXPECT_CALL(*scanDeviceIntent_, setOutYExtent(_))
        .WillRepeatedly(
            testing::Invoke([this, &outYExtent](uint32_t value) -> void {
                outYExtent = value;
            }));

    uint32_t xScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_))
        .WillRepeatedly(
            testing::Invoke([this, &xScalePercent](uint32_t value) -> void {
                xScalePercent = value;
            }));

    uint32_t yScalePercent;
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_))
        .WillRepeatedly(
            testing::Invoke([this, &yScalePercent](uint32_t value) -> void {
                yScalePercent = value;
            }));

    dune::imaging::types::Resolution xResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))
        .WillRepeatedly(
            testing::Invoke([this, &xResolution](dune::imaging::types::Resolution value) -> void {
                xResolution = value;
            }));

    dune::imaging::types::Resolution yResolution;
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))
        .WillRepeatedly(
            testing::Invoke([this, &yResolution](dune::imaging::types::Resolution value) -> void {
                yResolution = value;
            }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();

    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: xScalePercent calculated  : %d\n", xScalePercent);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: yScalePercent calculated  : %d\n", yScalePercent);

    EXPECT_EQ(xScalePercent, yScalePercent);
    EXPECT_NE(xScalePercent, 0);
    EXPECT_EQ(xScalePercent, 47);
}


TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageRetrieverIntentCalled_WithIdcard2UP)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();

    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    intent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);

    EXPECT_EQ(0, imageRetrieverIntent_->getRotationAngle());
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageProcessorIntentCalled_IDcardWithPerSheet2)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    auto intent = jobTicket->getIntent();
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    dune::imaging::Resources::SpecificRotation specificRotation;
    dune::imaging::types::PrintScaleT          printScaleTable;
    printScaleTable.scaleSelection = dune::imaging::types::PrintScaleSelection::CUSTOM;

    EXPECT_CALL(*imageProcessorIntent_, setPrintScale(_))
        .WillRepeatedly(
            testing::Invoke([this, &printScaleTable](dune::imaging::types::PrintScaleT value) -> void {
                printScaleTable = value;
            }));

    intent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    intent->setScaleSelection(dune::scan::types::ScanScaleSelectionEnum::CUSTOM);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupImageProcessorIntent(imageProcessorIntent_, resourceConfig);
    EXPECT_EQ(printScaleTable.scaleSelection, dune::imaging::types::PrintScaleSelection::NONE);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_withScallingForIDcard)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    uint32_t xScale_ = 0;
    uint32_t yScale_ = 0;

    bool featureVal = true;
    ON_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillByDefault(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    ON_CALL(*scanDeviceIntent_, setXScalePercent(_)).WillByDefault(testing::Invoke([&](uint32_t value) {
        xScale_ = value;
    }));

    ON_CALL(*scanDeviceIntent_, setYScalePercent(_)).WillByDefault(testing::Invoke([&](uint32_t value) {
        yScale_ = value;
    }));

    ON_CALL(*scanDeviceIntent_, getXScalePercent()).WillByDefault(Return(100));
    ON_CALL(*scanDeviceIntent_, getYScalePercent()).WillByDefault(Return(100));

    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    jobTicket->getIntent()->setScaleSelection(dune::scan::types::ScanScaleSelectionEnum::CUSTOM);
    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(xScale_, 100);
    EXPECT_EQ(yScale_, 100);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_BookModeAnd2UP_CorrectScalePercentForEnterprise)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());

    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);

    bool featureVal = true;
    ON_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillByDefault(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    
    uint32_t xExtent = 6400;
    uint32_t yExtent = 4900 * 2;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_)).WillRepeatedly(testing::Invoke([this, &xExtent](uint32_t value) -> void {
        xExtent = value;
    }));
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_)).WillRepeatedly(testing::Invoke([this, &yExtent](uint32_t value) -> void {
        yExtent = value;
    }));
    EXPECT_CALL(*scanDeviceIntent_, getXExtent()).WillRepeatedly(testing::Invoke([this, &xExtent]() -> uint32_t {
        return xExtent ;
    }));
    EXPECT_CALL(*scanDeviceIntent_, getYExtent()).WillRepeatedly(testing::Invoke([this, &yExtent]() -> uint32_t {
        return yExtent ;
    }));

    uint32_t xScale = 0;
    uint32_t yScale = 0;
    EXPECT_CALL(*scanDeviceIntent_, setXScalePercent(_)).WillRepeatedly(testing::Invoke([this, &xScale](uint32_t value) -> void {
        xScale = value;
    }));
    EXPECT_CALL(*scanDeviceIntent_, setYScalePercent(_)).WillRepeatedly(testing::Invoke([this, &yScale](uint32_t value) -> void {
        yScale = value;
    }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: xScalePercent calculated  : %d\n", xScale);
    GTEST_CHECKPOINTC("CopyPipelineResourceSetup: yScalePercent calculated  : %d\n", yScale);

    EXPECT_EQ(xScale, 62);
    EXPECT_EQ(yScale, 62);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupScanDeviceIntentCalled_InputAnySize_detectMediaFromSensorsEnterprise)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<MockIMediaPath>     pMockIMediaPath_;
    pMockIMediaPath_ = std::make_shared<MockIMediaPath>();
    ASSERT_TRUE(pMockIMediaPath_ != nullptr);
    auto intent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);

    EXPECT_CALL((*pMockIMediaPath_), getType).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));
    EXPECT_CALL((*pMockIMediaPath_), getMediaDetectionStatus).WillOnce(Return(std::make_pair(MediaSizeId::LETTER, dune::imaging::types::MediaOrientation::PORTRAIT)));

    dune::scan::scanningsystem::IMedia::IInputList scanSourceList{pMockIMediaPath_};
    scanSourceList.push_back(pMockIMediaPath_);
    auto mockIScannerMediaForEnterprise_ = std::make_shared<dune::scan::scanningsystem::MockIMedia>();
    ON_CALL(*mockIScannerMediaForEnterprise_, getInputs()).WillByDefault(Return(scanSourceList));

    jobTicket->setScanMediaInterface(mockIScannerMediaForEnterprise_.get());
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::STANDARD);
    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(
        jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(jobTicket->getIntent()->getInputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(jobTicket->getIntent()->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
}

TEST_F(GivenCopyPipelineResourcesSetup, WhenSetupImageRetrieverIntentForEnterpriseRetrieveJob)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRIEVE);

    auto intent = jobTicket->getIntent();

    uint32_t rotationAngle;
    EXPECT_CALL(*imageRetrieverIntent_, setRotationAngle(_))

        .WillRepeatedly(

            testing::Invoke([this, &rotationAngle](uint32_t value) -> void {

                rotationAngle = value;

            }));

    bool removeImageWhenFinish;
    
    EXPECT_CALL(*imageRetrieverIntent_, setRemoveImageWhenFinish(_))

        .WillRepeatedly(

            testing::Invoke([this, &removeImageWhenFinish](bool value) -> void {

                removeImageWhenFinish = value;

            }));

    bool perfromSequenceOperation;
    uint32_t collationCopies;
    uint32_t uncollationCopies;
    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_))

        .WillRepeatedly(

            testing::Invoke([this, &perfromSequenceOperation, &collationCopies, &uncollationCopies](
                                std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams) -> void {
                perfromSequenceOperation = (sequencingParams != nullptr);
                collationCopies = sequencingParams ? sequencingParams->collationCopies : 0;
                uncollationCopies = sequencingParams ? sequencingParams->uncollationCopies : 0;
            }));

    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(_,_,_,nullptr)).Times(1);

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setCollateMode(CollateMode::UNCOMPRESSED);
    copyPipelineResourceSetup->setupImageRetrieverIntent(imageRetrieverIntent_, resourceConfig);

    EXPECT_EQ(false, removeImageWhenFinish);   
}

class GivenCopyPipelineScanCalibrationSetup : public GivenCopyPipelineResourcesSetup
{
  public:
    GivenCopyPipelineScanCalibrationSetup(){};

    virtual void SetUp() override;
    virtual void TearDown() override;

    uint32_t xExtent;
    uint32_t yExtent;

};

void GivenCopyPipelineScanCalibrationSetup::SetUp()
{
    GivenCopyPipelineResourcesSetup::SetUp();

    bool featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop,_))
        .WillRepeatedly(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = true;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));
    featureVal = false;
    EXPECT_CALL(*scannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors,_))
        .WillOnce(DoAll(SetArgReferee<1>(featureVal),
                    Return(dune::framework::core::APIResult::OK)));

    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this](uint32_t value) -> void {

                this->xExtent = value;

            }));
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this](uint32_t value) -> void {

                this->yExtent = value;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent())

        .WillRepeatedly(

            testing::Invoke([this]() -> uint32_t {

                return this->xExtent ;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())

        .WillRepeatedly(

            testing::Invoke([this]() -> uint32_t {

                return this->yExtent ;

            }));
}

void GivenCopyPipelineScanCalibrationSetup::TearDown()
{
    GivenCopyPipelineResourcesSetup::TearDown();
}

TEST_F(GivenCopyPipelineScanCalibrationSetup, WhenSetupScanDeviceIntentCalled_ForDesignjet_ScanCalibration)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setScanCalibrationType(dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION);

    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobTicket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobTicket->getIntent()->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    jobTicket->getIntent()->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setScanCalibrationType(jobTicket->getScanCalibrationType());

    dune::imaging::types::ScanCalibrationType scanCalibrationType = dune::imaging::types::ScanCalibrationType::UNKNOWN;
    EXPECT_CALL(*scanDeviceIntent_, setScanCalibrationType(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanCalibrationType](dune::imaging::types::ScanCalibrationType value) -> void {

                scanCalibrationType = value;

            }));

    uint32_t xExtent = 0;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly( testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;  }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly( testing::Invoke([this, &xExtent]() -> uint32_t {
              return xExtent; }));

    uint32_t yExtent = 0;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly( testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value; }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly( testing::Invoke([this, &yExtent]() -> uint32_t {
              return yExtent; }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::LFP, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(scanCalibrationType, dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION);
}

TEST_F(GivenCopyPipelineScanCalibrationSetup, WhenSetupScanDeviceIntentCalled_ForHomepro_ScanCalibration)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setScanCapabilitiesInterface(scannerCapabilities_.get());
    jobTicket->setScanCalibrationType(dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION);

    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobTicket->getIntent()->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    jobTicket->getIntent()->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);
    jobTicket->getIntent()->setScanCalibrationType(jobTicket->getScanCalibrationType());

    dune::imaging::types::ScanCalibrationType scanCalibrationType = dune::imaging::types::ScanCalibrationType::UNKNOWN;
    EXPECT_CALL(*scanDeviceIntent_, setScanCalibrationType(_))

        .WillRepeatedly(

            testing::Invoke([this, &scanCalibrationType](dune::imaging::types::ScanCalibrationType value) -> void {

                scanCalibrationType = value;

            }));

    uint32_t xExtent = 0;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))
        .WillRepeatedly( testing::Invoke([this, &xExtent](uint32_t value) -> void {
                xExtent = value;  }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent())
        .WillRepeatedly( testing::Invoke([this, &xExtent]() -> uint32_t {
              return xExtent; }));

    uint32_t yExtent = 0;
    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))
        .WillRepeatedly( testing::Invoke([this, &yExtent](uint32_t value) -> void {
                yExtent = value; }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())
        .WillRepeatedly( testing::Invoke([this, &yExtent]() -> uint32_t {
              return yExtent; }));

    copyPipelineResourceSetup = std::make_shared<CopyPipelineResourceSetup>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, nullptr);
    auto resourceConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    copyPipelineResourceSetup->setupScanDeviceIntent(scanDeviceIntent_, resourceConfig);

    EXPECT_EQ(scanCalibrationType, dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION);

}

}}}} //namespace dune::copy::Jobs::Copy