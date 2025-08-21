/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobTicketGtest.cpp
 * @date   Wed, 08 May 2019 06:49:55 -0700
 * @brief  Copy Job Ticket Test
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "gmock/gmock.h"
#include "gtest/gtest.h"
#include "CopyJobTicketGtest_TraceAutogen.h"
#include "GTestConfigHelper.h"

#include <sstream>
#include <memory>

#include "MockIPrintIntentsFactory.h"
#include "MockICapabilities.h"
#include "CopyJobTicket.h"
#include "ScanJobIntent_generated.h"
#include "MockIMedia.h"
#include "CopyTicketGtestUtilities.h"
#include "IIntentsManager.h"
#include "IPrintUids.h"
#include "MockIIntentsManager.h"
#include "ImagingUtilities.h"
#include "MarginLayout_generated.h"
#include "MediaSizeId_generated.h"
#include "IMedia.h"
#include "MockICopyJobTicket.h"
#include "testResources/MediaSimulatorConfig_generated.h"
#include "MediaHelper.h"
#include "Media_generated.h"
#include "ContentType_generated.h"
#include "TestSystemServices.h"
#include "ContentAlignment_generated.h"
#include "ConvertToScanTypeHelper.h"
#include "MockIExportImport.h"
#include "ConstraintsGroup.h"
#include "MockIPageBasedFinisher.h"
#include "MockIFinisherCombination.h"
#include "MockILocale.h"
#include "MockILocaleProvider.h"
#include "StringId.h"
#include "StringIds.h"
#include "MockIColorAccessControl.h"
#include "IColorAccessControl.h"

using namespace dune::imaging::types;
using CopyJobTicket = dune::copy::Jobs::Copy::CopyJobTicket;
using CopyJobIntent = dune::copy::Jobs::Copy::CopyJobIntent;
using ICopyJobIntent = dune::copy::Jobs::Copy::ICopyJobIntent;
using ICopyJobResult = dune::copy::Jobs::Copy::ICopyJobResult;
using IMedia = dune::print::engine::IMedia;
using Margins = dune::imaging::types::Margins;
using Distance = dune::imaging::types::Distance;
using PrintIntents = dune::print::engine::PrintIntents;
using IIntent = dune::job::IIntent;
using MarginLayout = dune::imaging::types::MarginLayout;
using ScanScaleSelectionEnum = dune::scan::types::ScanScaleSelectionEnum;
using MediaSizeId = dune::imaging::types::MediaSizeId;
using MockIMediaIInput = dune::print::engine::MockIMediaIInput;
using MockICopyJobIntent = dune::copy::Jobs::Copy::MockICopyJobIntent;
using ConfigurationRawData = dune::framework::resources::IConfigurationService::ConfigurationRawData;
using MediaSimulatorConfigT = dune::print::engine::simulator::MediaSimulatorConfigT;
using MediaHelper = dune::print::engine::MediaHelper;
using TrayT = dune::print::engine::simulator::TrayT;
using DeviceOrder = dune::print::engine::DeviceOrder;
using OriginalContentType = dune::imaging::types::OriginalContentType;
using InputDeviceT = dune::print::engine::simulator::InputDeviceT;
using TestConfigurationService = dune::framework::component::TestingUtil::TestSystemServices::TestConfigurationService;
using MockIExportImport = dune::framework::data::backup::MockIExportImport;
using MockIMedia = dune::print::engine::MockIMedia;
using MockIFinisherCombination = dune::print::engine::MockIFinisherCombination;
using MockIMediaIOutput = dune::print::engine::MockIMediaIOutput;
using OrientedMediaSize = dune::imaging::types::OrientedMediaSize;
using MediaDestinationId = dune::imaging::types::MediaDestinationId;


//add for finisher media helper
using FinishingContentOrientation                   = dune::imaging::types::FinishingContentOrientation;
using ContentOrientation                            = dune::imaging::types::ContentOrientation;
using StaplingOptions                               = dune::imaging::types::StapleOptions;
using PunchingOptions                               = dune::imaging::types::PunchingOptions;
using FoldingOptions                                = dune::imaging::types::FoldingOptions;
using BookletMakingOptions                          = dune::imaging::types::BookletMakingOptions;
using StaplesOutAction                              = dune::imaging::types::StaplesOutAction;
using JobOffsetMode                                 = dune::imaging::types::JobOffsetMode;
using IPageBasedFinisher                            = IMedia::IPageBasedFinisher;
using IMediaProcessingType                          = IMedia::IPageBasedFinisher::IMediaProcessingType;
using StaplingAndPunchingMediaProcessingType        = IMedia::IPageBasedFinisher::StaplingAndPunchingMediaProcessingType;
using FoldingMediaProcessingType                    = IMedia::IPageBasedFinisher::FoldingMediaProcessingType;
using BookletMakingMediaProcessingType              = IMedia::IPageBasedFinisher::BookletMakingMediaProcessingType;
using JogMediaProcessingType                        = IMedia::IPageBasedFinisher::JogMediaProcessingType;
using MediaProcessingTypePtr                        = std::shared_ptr<IMediaProcessingType>;
using StaplingAndPunchingMediaProcessingTypePtr     = std::shared_ptr<StaplingAndPunchingMediaProcessingType>;
using FoldingMediaProcessingTypePtr                 = std::shared_ptr<FoldingMediaProcessingType>;
using BookletMakingMediaProcessingTypePtr           = std::shared_ptr<BookletMakingMediaProcessingType>;
using JogMediaProcessingTypePtr                     = std::shared_ptr<JogMediaProcessingType>;
using IMediaProcessingOption                        = IMedia::IPageBasedFinisher::IMediaProcessingOption;
using MediaProcessingOptionPtr                      = std::shared_ptr<IMediaProcessingOption>;
using StaplingAndPunchingMediaProcessingOption      = IMedia::IPageBasedFinisher::StaplingAndPunchingMediaProcessingOption;
using FoldingMediaProcessingOption                  = IMedia::IPageBasedFinisher::FoldingMediaProcessingOption;
using BookletMakingMediaProcessingOption            = IMedia::IPageBasedFinisher::BookletMakingMediaProcessingOption;
using JogMediaProcessingOption                      = IMedia::IPageBasedFinisher::JogMediaProcessingOption;
using StaplingAndPunchingMediaProcessingOptionPtr   = std::shared_ptr<StaplingAndPunchingMediaProcessingOption>;
using FoldingMediaProcessingOptionPtr               = std::shared_ptr<FoldingMediaProcessingOption>;
using BookletMakingMediaProcessingOptionPtr         = std::shared_ptr<BookletMakingMediaProcessingOption>;
using JogMediaProcessingOptionPtr                   = std::shared_ptr<JogMediaProcessingOption>;
using MediaSizeCharacteristicsOrientation           = IMedia::IPageBasedFinisher::MediaSizeCharacteristicsOrientation;
using IPPData                                       = IMedia::IPageBasedFinisher::IPPData;
using MediaSizeCharacteristicsOrientationPtr        = std::shared_ptr<MediaSizeCharacteristicsOrientation>;
using IPPDataPtr                                    = std::shared_ptr<IPPData>;
using MediaProcessingTypes                          = dune::imaging::types::MediaProcessingTypes;
using MediaProcessingTypeName                       = std::string;
using MediaProcessingOptionName                     = std::string;
using MediaProcessingBoundary                       = dune::imaging::types::MediaProcessingBoundary;
using MinAndMax                                     = IMedia::IDevice::MinAndMax;
using StaplingMenuItem                              = IMedia::IFinisherCombination::StaplingMenuItem;
using PunchingMenuItem                              = IMedia::IFinisherCombination::PunchingMenuItem;
using FoldingMenuItem                               = IMedia::IFinisherCombination::FoldingMenuItem;
using BookletMakingMenuItem                         = IMedia::IFinisherCombination::BookletMakingMenuItem;
using StaplingMenuItemPtr                           = std::shared_ptr<StaplingMenuItem>;
using PunchingMenuItemPtr                           = std::shared_ptr<PunchingMenuItem>;
using FoldingMenuItemPtr                            = std::shared_ptr<FoldingMenuItem>;
using BookletMakingMenuItemPtr                      = std::shared_ptr<BookletMakingMenuItem>;
using StaplingMenuItemList                          = std::vector<StaplingMenuItemPtr>;
using PunchingMenuItemList                          = std::vector<PunchingMenuItemPtr>;
using FoldingMenuItemList                           = std::vector<FoldingMenuItemPtr>;
using BookletMakingMenuItemList                     = std::vector<BookletMakingMenuItemPtr>;
using JobPageOrder                                  = dune::imaging::types::JobSequencePageOrder;
using DuplexPageOrder                               = dune::imaging::types::DuplexPageOrder;
using FormatterRotationPriority                     = dune::imaging::types::FormatterRotationPriority;
using ProcessingOptionDirection                     = dune::imaging::types::ProcessingOptionDirection;
using FoldingStyle                                  = IMedia::ILargeFormatFolder::Properties::FoldingStyle;
using Properties                                    = IMedia::ILargeFormatFolder::Properties;
using ProcessingOptionLocations                     = std::vector<std::vector<int32_t>>;
using ProcessingOptionOffsets                       = std::vector<int32_t>;
using FinisherType                              = dune::print::engine::FinisherType;
using DefaultMediaProcessingOption                  = dune::print::engine::IMedia::IPageBasedFinisher::DefaultMediaProcessingOption;

using ::testing::Return;
using ::testing::ReturnRef;
using ::testing::_;
using ::testing::Invoke;

static const uint32_t        RESOLUTION{600};



//CopyJobConstraintsFbT
/*
flatbuffer-y utility function filling out a CopyJobConstraintsFb
*/
bool loadCopyJobConstraintsFbT(
   std::shared_ptr<CopyJobConstraintsFbT>& tableT,
   const std::string& pathToResources,
   const std::string& loadedFbsSchema,
   const std::string& jsonDataString)
{
   bool resultOp = true;
   flatbuffers::Parser parser;
   //parser.opts.output_default_scalars_in_json = true;
   std::string path1 = ".";
   std::string path2 = pathToResources;
   const char* includePaths[] = {
       (const char*)path1.c_str(),
       (const char*)path2.c_str(),
       nullptr
   };
   //listFiles(path1.c_str());
   //listFiles(path2.c_str());
   //std::cerr << "Include paths: \n";
   //std::cerr << includePaths[0] << "\n";
   //std::cerr << includePaths[1] << "\n\n";

   std::string schemafile;
   std::string schemaPath = "testResources/" + loadedFbsSchema;
   resultOp = flatbuffers::LoadFile(schemaPath.c_str(), false, &schemafile)
       //&& flatbuffers::LoadFile(dataFileName, false, &jsonfile)
       ;

   // set the root type for parsing. (This is a special case that I haven't seen elsewhere. Normally the root_type is defined in a .fbs file
   // and this one is not usually the root_type, so we kinda 'hack' it to be by appending the root_type to the loaded string.)
   schemafile += "\n\n root_type CopyJobConstraintsFb;\n\n";

   if (!resultOp)
   {
       std::cerr << "parserLoadTest:: 'LoadFile()' failed for  '" << loadedFbsSchema << "' !\n";
   }
   if (!parser.Parse(schemafile.c_str(), includePaths))
   {
       resultOp = false;
       std::cerr << "loadCopyJobConstraintsFbT:: couldn't load loadedFbsSchema files!\n" << parser.error_.c_str() << "\n";
   }
   else if (!parser.Parse(jsonDataString.c_str(), includePaths))
   {
       resultOp = false;
       std::cerr << "loadCopyJobConstraintsFbT:: couldn't parse the JSON !\n" << parser.error_.c_str() << "\n";

   }
   else
   {
       uint8_t* bufferPointer = parser.builder_.GetBufferPointer();
       const uint32_t bufferSize = parser.builder_.GetSize();

       flatbuffers::Verifier verifier(bufferPointer, bufferSize);
       if (!verifier.VerifyBuffer<CopyJobConstraintsFb>(nullptr))
       {
           resultOp = false;
       }
       tableT = std::shared_ptr<CopyJobConstraintsFbT>((flatbuffers::GetRoot<CopyJobConstraintsFb>(bufferPointer)->UnPack()));
   }

   return resultOp;
}


TEST(GivenADefaultTicket, ThenValidateDefaultProperties)
{
    //Validating the default copy job ticket
    CopyJobTicket ticket;
    EXPECT_EQ(MediaSizeId::LETTER,                              ticket.getDefaultMediaSize());
    EXPECT_EQ(dune::copy::Jobs::Copy::Product::HOME_PRO,        ticket.getPrePrintConfiguration());
    EXPECT_EQ(dune::job::SegmentType::FinalSegment,             ticket.getSegmentType());
    EXPECT_EQ(0,                                                ticket.getPrescannedHeight());
    EXPECT_EQ(0,                                                ticket.getPrescannedWidth());
    EXPECT_EQ(false,                                            ticket.isPreScanJob());
    EXPECT_EQ(false,                                            ticket.getJobCompleting());
    EXPECT_EQ(PrintingOrder::LAST_PAGE_ON_TOP, ticket.getIntent()->getPrintingOrder());
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);

    // Copy job intents
    EXPECT_EQ(MediaSizeId::LETTER,                              intent->getOutputMediaSizeId());
    EXPECT_EQ(MediaOrientation::PORTRAIT,                       intent->getOutputMediaOrientation());
    EXPECT_EQ(MediaIdType::STATIONERY,                          intent->getOutputMediaIdType());
    EXPECT_EQ(MediaSource::TRAY1,                               intent->getOutputMediaSource());
    EXPECT_EQ(Plex::SIMPLEX,                                    intent->getOutputPlexMode());
    EXPECT_EQ(PlexBinding::LONG_EDGE,                           intent->getOutputPlexBinding());
    EXPECT_EQ(1,                                                intent->getCopies());
    EXPECT_EQ(dune::copy::SheetCollate::Collate,                intent->getCollate());
    EXPECT_EQ(PrintQuality::NORMAL,                             intent->getCopyQuality());
    EXPECT_EQ(false,                                            intent->getGeneratePreview());
    EXPECT_EQ(false,                                            intent->getAutoDeskew());
    EXPECT_EQ(CopyMargins::CLIPCONTENT,                         intent->getCopyMargins());
    EXPECT_EQ(PrintingOrder::LAST_PAGE_ON_TOP,                  intent->getPrintingOrder());
    EXPECT_EQ(0,                                                intent->getRotation());
    EXPECT_EQ(MediaFamily::ADHESIVE,                            intent->getMediaFamily());
    EXPECT_EQ(false,                                            intent->getAutoRotate());
    EXPECT_EQ(MediaDestinationId::STACKER,                      intent->getOutputDestination());
    EXPECT_EQ(0,                                                intent->getRequestedPages());

    // Scan job intents
    EXPECT_EQ(MediaSizeId::LETTER,                              intent->getInputMediaSizeId());
    EXPECT_EQ(Plex::SIMPLEX,                                    intent->getInputPlexMode());
    EXPECT_EQ(Resolution::E300DPI,                              intent->getOutputXResolution());
    EXPECT_EQ(Resolution::E300DPI,                              intent->getOutputYResolution());
    EXPECT_EQ(dune::scan::types::AttachmentSize::STANDARD,      intent->getQualityMode());
    EXPECT_EQ(ColorMode::COLOR,                                 intent->getColorMode());
    EXPECT_EQ(ContentOrientation::PORTRAIT,                     intent->getContentOrientation());
    EXPECT_EQ(ContentOrientation::PORTRAIT,                     intent->getBackSideContentOrientation());
    EXPECT_EQ(dune::imaging::types::OriginalContentType::MIXED, intent->getOriginalContentType());
    EXPECT_EQ(dune::scan::types::ScanSource::ADF_SIMPLEX,       intent->getScanSource());
    EXPECT_EQ(100,                                              intent->getXScalePercent());
    EXPECT_EQ(100,                                              intent->getYScalePercent());
    EXPECT_EQ(dune::scan::types::ScanScaleSelectionEnum::NONE,  intent->getScaleSelection());
    EXPECT_EQ(MediaSizeId::LETTER,                              intent->getScaleToSize());
    EXPECT_EQ(MediaSource::TRAY1,                               intent->getScaleToOutput());
    EXPECT_EQ(dune::scan::types::ScanFeedOrientation::SHORTEDGE,intent->getScanFeedOrientation());
    EXPECT_EQ(Resolution::E300DPI,                              intent->getScanXResolution());
    EXPECT_EQ(Resolution::E300DPI,                              intent->getScanYResolution());
    EXPECT_EQ(0,                                                intent->getJobScanLimit());
    EXPECT_EQ(4,                                                intent->getBrightness());
    EXPECT_EQ(dune::scan::types::ScanCaptureModeType::STANDARD, intent->getScanCaptureMode());
    EXPECT_EQ(dune::scan::types::ScanImagingProfileType::COPY,  intent->getScanImagingProfile());
    EXPECT_EQ(dune::scan::types::ImagePreview::MakeOptional,         intent->getImagePreview());
    EXPECT_EQ(false,                                            intent->getEdgeToEdgeScan());
    EXPECT_EQ(false,                                            intent->getLongPlotScan());
    EXPECT_EQ(false,                                            intent->getInvertColors());
    EXPECT_EQ(false,                                            intent->getBackgroundNoiseRemoval());
    EXPECT_EQ(false,                                            intent->getBackgroundColorRemoval());
    EXPECT_EQ(0,                                                intent->getBackgroundColorRemovalLevel());
    EXPECT_EQ(60,                                               intent->getBlackEnhancementLevel());
    EXPECT_EQ(dune::scan::types::CompressionModeEnum::Uncompressed,intent->getCompressionType());
    EXPECT_EQ(dune::imaging::types::StapleOptions::NONE,        intent->getStapleOption());
    EXPECT_EQ(dune::imaging::types::PunchingOptions::NONE,      intent->getPunchOption());
    EXPECT_EQ(dune::imaging::types::FoldingOptions::NONE,       intent->getFoldOption());
    EXPECT_EQ(1,                                                intent->getSheetsPerSetForCFold());
    EXPECT_EQ(1,                                                intent->getSheetsPerSetForVFold());
    EXPECT_EQ(dune::imaging::types::BookletMakingOptions::NONE, intent->getBookletMakerOption());
    EXPECT_EQ(1,                                                intent->getSheetsPerSetForFoldAndStitch());

    std::shared_ptr<ICopyJobResult> result = ticket.getResult();
    ASSERT_NE(result, nullptr);
    // Copy job results
    EXPECT_EQ(0,                                                result->getCompletedCopies());
    EXPECT_EQ(0,                                                result->getCompletedImpressions());
    EXPECT_EQ(0,                                                result->getCurrentCuringTemperature());
    EXPECT_EQ(0,                                                result->getCurrentPage());
    EXPECT_EQ(0,                                                result->getProgress());
    EXPECT_EQ(0,                                                result->getRemainingPrintingTime());
    EXPECT_EQ(false,                                            result->areAllPagesDiscovered());
}

TEST(GivenADefaultTicket , ThenValidateWriteAndReadSettingsToAndFromFile)
{
    CopyJobTicket                       ticket;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);


    EXPECT_EQ(ticket.getType(), dune::job::JobType::COPY);
    //Some of the inital copy and scan job intents
    EXPECT_EQ(MediaSizeId::LETTER,         intent->getOutputMediaSizeId());
    EXPECT_EQ(MediaOrientation::PORTRAIT,  intent->getOutputMediaOrientation());
    EXPECT_EQ(1,                           intent->getCopies());
    EXPECT_EQ(Plex::SIMPLEX,               intent->getOutputPlexMode());
    EXPECT_EQ(MediaSizeId::LETTER,         intent->getInputMediaSizeId());

    //updating some of the initial intents
    intent->setCopies(100);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setInputMediaSizeId(MediaSizeId::A4);

    std::string filePath( "/tmp/copybackupSettings" );
    filePath += std::to_string( std::chrono::system_clock::now().time_since_epoch().count() );
    EXPECT_EQ( ticket.writeSettingsToFile( filePath ), dune::framework::data::backup::OperationResult::SUCCESS );

    CopyJobTicket newJobTicket;
    EXPECT_EQ( newJobTicket.readSettingsFromFile( filePath ), dune::framework::data::backup::OperationResult::SUCCESS );
    std::shared_ptr<ICopyJobIntent> newIntent = newJobTicket.getIntent();

    EXPECT_EQ(100,             intent->getCopies());
    EXPECT_EQ(Plex::DUPLEX,    intent->getOutputPlexMode());
    EXPECT_EQ(MediaSizeId::A4, intent->getInputMediaSizeId());

}


TEST(GivenADefaultTicket , WhenReadSettingsWithoutWrite_ThenReturnsFailure)
{
    CopyJobTicket                       ticket;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);


    EXPECT_EQ(ticket.getType(), dune::job::JobType::COPY);
    //Some of the inital copy and scan job intents
    EXPECT_EQ(MediaSizeId::LETTER,         intent->getOutputMediaSizeId());
    EXPECT_EQ(MediaOrientation::PORTRAIT,  intent->getOutputMediaOrientation());
    EXPECT_EQ(1,                           intent->getCopies());

    std::string filePath( "/tmp/copybackupSettings" );
    filePath += std::to_string( std::chrono::system_clock::now().time_since_epoch().count() );

    CopyJobTicket newJobTicket;

    EXPECT_EQ( newJobTicket.readSettingsFromFile( filePath ), dune::framework::data::backup::OperationResult::ERROR );

}


TEST(CloneACopyJobTicket,IfNotReprintOrRetrieveThenValidateClonedJobTicketIsTheSameEvenResults)
{
    //Validating the default copy job ticket
    dune::copy::Jobs::Copy::MaxLengthConfig maxLengthConfig;
    maxLengthConfig.scanMaxCm = 2000;
    CopyJobTicket ticket;
    ticket.setMaxLengthConfig(maxLengthConfig);
    ticket.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::LFP);
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);

    // this clone will not be a reprint
    ticket.setJobReprintable(false);

    // Base job ticket values
    EXPECT_EQ(ticket.getType(), dune::job::JobType::COPY);
    EXPECT_EQ(PrintingOrder::LAST_PAGE_ON_TOP, ticket.getIntent()->getPrintingOrder());

    // Copy job intents
    EXPECT_EQ(MediaSizeId::LETTER,                          intent->getOutputMediaSizeId());
    EXPECT_EQ(MediaOrientation::PORTRAIT,                   intent->getOutputMediaOrientation());
    EXPECT_EQ(MediaIdType::STATIONERY,                      intent->getOutputMediaIdType());
    EXPECT_EQ(MediaSource::TRAY1,                           intent->getOutputMediaSource());
    EXPECT_EQ(Plex::SIMPLEX,                                intent->getOutputPlexMode());
    EXPECT_EQ(PlexBinding::LONG_EDGE,                       intent->getOutputPlexBinding());
    EXPECT_EQ(1,                                            intent->getCopies());
    EXPECT_EQ(dune::copy::SheetCollate::Collate,            intent->getCollate());
    EXPECT_EQ(dune::imaging::types::StapleOptions::NONE,    intent->getStapleOption());
    EXPECT_EQ(dune::imaging::types::PunchingOptions::NONE,  intent->getPunchOption());
    EXPECT_EQ(dune::imaging::types::FoldingOptions::NONE,   intent->getFoldOption());
    EXPECT_EQ(1,                                            intent->getSheetsPerSetForCFold());
    EXPECT_EQ(1,                                            intent->getSheetsPerSetForVFold());
    EXPECT_EQ(dune::imaging::types::BookletMakingOptions::NONE, intent->getBookletMakerOption());
    EXPECT_EQ(1,                                               intent->getSheetsPerSetForFoldAndStitch());

    // Scan job intents
    EXPECT_EQ(MediaSizeId::LETTER,                          intent->getInputMediaSizeId());
    EXPECT_EQ(Resolution::E300DPI,                          intent->getScanXResolution());
    EXPECT_EQ(Resolution::E300DPI,                          intent->getScanYResolution());
    EXPECT_EQ(dune::scan::types::AttachmentSize::STANDARD,  intent->getQualityMode());
    EXPECT_EQ(Plex::SIMPLEX,                                intent->getInputPlexMode());
    EXPECT_EQ(ColorMode::COLOR,                             intent->getColorMode());
    EXPECT_EQ(ContentOrientation::PORTRAIT,                 intent->getContentOrientation());

    //Updating values
    std::string jobName = "SimpleCopyJob";
    ticket.setJobName(jobName);
    ticket.getIntent()->setPrintingOrder(PrintingOrder::LAST_PAGE_ON_TOP);
    intent->setCopies(100);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setInputMediaSizeId(MediaSizeId::A4);
    intent->setInputPlexMode(Plex::DUPLEX);
    intent->setScanXResolution(Resolution::E300DPI);
    intent->setScanYResolution(Resolution::E300DPI);
    intent->setGeneratePreview(true);
    intent->setAutoDeskew(true);
    intent->setEdgeToEdgeScan(true);
    intent->setLongPlotScan(true);
    intent->setInvertColors(true);
    intent->setCopyMargins(CopyMargins::OVERSIZE);
    intent->setPrintingOrder(PrintingOrder::LAST_PAGE_ON_TOP);
    intent->setRotation(270);
    intent->setAutoRotate(true);
    intent->setMediaFamily(MediaFamily::ADHESIVE);
    intent->setOutputDestination(MediaDestinationId::STACKER);
    intent->setBackgroundNoiseRemoval(true);
    intent->setBackgroundColorRemoval(true);
    intent->setBackgroundColorRemovalLevel(-1);
    intent->setBlackEnhancementLevel(200);
    intent->setRequestedPages(10);
    intent->setStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::TWO_POINT_ANY);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::V_INWARD_TOP);
    intent->setSheetsPerSetForCFold(2);
    intent->setSheetsPerSetForVFold(3);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);
    intent->setSheetsPerSetForFoldAndStitch(10);

    EXPECT_EQ(jobName,                                      ticket.getJobName());
    EXPECT_EQ(100,                                          intent->getCopies());
    EXPECT_EQ(Plex::DUPLEX,                                 intent->getOutputPlexMode());
    EXPECT_EQ(MediaSizeId::A4,                              intent->getInputMediaSizeId());
    EXPECT_EQ(Plex::DUPLEX,                                 intent->getInputPlexMode());
    EXPECT_EQ(Resolution::E300DPI,                          intent->getScanXResolution());
    EXPECT_EQ(Resolution::E300DPI,                          intent->getScanYResolution());
    EXPECT_EQ(true,                                         intent->getEdgeToEdgeScan());
    EXPECT_EQ(true,                                         intent->getLongPlotScan());
    EXPECT_EQ(true,                                         intent->getInvertColors());
    EXPECT_EQ(CopyMargins::OVERSIZE,                        intent->getCopyMargins());
    EXPECT_EQ(PrintingOrder::LAST_PAGE_ON_TOP,              intent->getPrintingOrder());
    EXPECT_EQ(270,                                          intent->getRotation());
    EXPECT_EQ(true,                                         intent->getAutoRotate());
    EXPECT_EQ(MediaFamily::ADHESIVE,                        intent->getMediaFamily());
    EXPECT_EQ(MediaDestinationId::STACKER,                  intent->getOutputDestination());
    EXPECT_EQ(10,                                           intent->getRequestedPages());
    EXPECT_EQ(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY,   intent->getStapleOption());
    EXPECT_EQ(dune::imaging::types::PunchingOptions::TWO_POINT_ANY,         intent->getPunchOption());
    EXPECT_EQ(dune::imaging::types::FoldingOptions::V_INWARD_TOP,           intent->getFoldOption());
    EXPECT_EQ(2,                                            intent->getSheetsPerSetForCFold());
    EXPECT_EQ(3,                                            intent->getSheetsPerSetForVFold());
    EXPECT_EQ(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH, intent->getBookletMakerOption());
    EXPECT_EQ(10,                                                        intent->getSheetsPerSetForFoldAndStitch());

    std::shared_ptr<ICopyJobResult> result = ticket.getResult();
    ASSERT_NE(result, nullptr);
    result->setCompletedCopies(2);
    result->setCompletedImpressions(10);
    result->setCurrentCuringTemperature(100);
    result->setCurrentPage(10);
    result->setProgress(100);
    result->setRemainingPrintingTime(100);
    result->setAllPagesDiscovered(true);

    CopyJobTicket cloneCopyJobTicket(ticket);

    EXPECT_EQ(dune::job::JobType::COPY,                     cloneCopyJobTicket.getType());
    EXPECT_EQ(jobName,                                      cloneCopyJobTicket.getJobName());
    EXPECT_EQ(PrintingOrder::LAST_PAGE_ON_TOP, cloneCopyJobTicket.getIntent()->getPrintingOrder());
    EXPECT_EQ(100,                                          cloneCopyJobTicket.getIntent()->getCopies());
    EXPECT_EQ(Plex::DUPLEX,                                 cloneCopyJobTicket.getIntent()->getOutputPlexMode());
    EXPECT_EQ(MediaSizeId::A4,                              cloneCopyJobTicket.getIntent()->getInputMediaSizeId());
    EXPECT_EQ(Plex::DUPLEX,                                 cloneCopyJobTicket.getIntent()->getInputPlexMode());
    EXPECT_EQ(true,                                         cloneCopyJobTicket.getIntent()->getGeneratePreview());
    EXPECT_EQ(true,                                         cloneCopyJobTicket.getIntent()->getAutoDeskew());
    EXPECT_EQ(true,                                         cloneCopyJobTicket.getIntent()->getEdgeToEdgeScan());
    EXPECT_EQ(true,                                         cloneCopyJobTicket.getIntent()->getLongPlotScan());
    EXPECT_EQ(true,                                         cloneCopyJobTicket.getIntent()->getInvertColors());
    EXPECT_EQ(CopyMargins::OVERSIZE,                        cloneCopyJobTicket.getIntent()->getCopyMargins());
    EXPECT_EQ(PrintingOrder::LAST_PAGE_ON_TOP,              cloneCopyJobTicket.getIntent()->getPrintingOrder());
    EXPECT_EQ(270,                                          cloneCopyJobTicket.getIntent()->getRotation());
    EXPECT_EQ(true,                                         cloneCopyJobTicket.getIntent()->getAutoRotate());
    EXPECT_EQ(MediaFamily::ADHESIVE,                        cloneCopyJobTicket.getIntent()->getMediaFamily());
    EXPECT_EQ(MediaDestinationId::STACKER,                  cloneCopyJobTicket.getIntent()->getOutputDestination());
    EXPECT_EQ(true,                                         cloneCopyJobTicket.getIntent()->getBackgroundNoiseRemoval());
    EXPECT_EQ(true,                                         cloneCopyJobTicket.getIntent()->getBackgroundColorRemoval());
    EXPECT_EQ(-1,                                           cloneCopyJobTicket.getIntent()->getBackgroundColorRemovalLevel());
    EXPECT_EQ(200,                                          cloneCopyJobTicket.getIntent()->getBlackEnhancementLevel());
    EXPECT_EQ(10,                                           cloneCopyJobTicket.getIntent()->getRequestedPages());
    EXPECT_EQ(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY,  cloneCopyJobTicket.getIntent()->getStapleOption());
    EXPECT_EQ(dune::imaging::types::PunchingOptions::TWO_POINT_ANY,        cloneCopyJobTicket.getIntent()->getPunchOption());
    EXPECT_EQ(dune::imaging::types::FoldingOptions::V_INWARD_TOP,          cloneCopyJobTicket.getIntent()->getFoldOption());
    EXPECT_EQ(2,                                            intent->getSheetsPerSetForCFold());
    EXPECT_EQ(3,                                            intent->getSheetsPerSetForVFold());
    EXPECT_EQ(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH, intent->getBookletMakerOption());
    EXPECT_EQ(10,                                                        intent->getSheetsPerSetForFoldAndStitch());
    
    EXPECT_EQ(MediaSizeId::LETTER,                          cloneCopyJobTicket.getDefaultMediaSize());
    EXPECT_EQ(dune::copy::Jobs::Copy::Product::LFP,         cloneCopyJobTicket.getPrePrintConfiguration());
    EXPECT_EQ(dune::job::SegmentType::FinalSegment,         cloneCopyJobTicket.getSegmentType());
    EXPECT_EQ(0,                                            cloneCopyJobTicket.getPrescannedHeight());
    EXPECT_EQ(0,                                            cloneCopyJobTicket.getPrescannedWidth());
    EXPECT_EQ(false,                                        cloneCopyJobTicket.isPreScanJob());
    EXPECT_EQ(maxLengthConfig.scanMaxCm,                    cloneCopyJobTicket.getMaxLengthConfig().scanMaxCm);
    // REVISIT - With Resolution change, this step is not working
    // EXPECT_EQ(Resolution::E300DPI, cloneCopyJobTicket.getIntent()->getScanXResolution());
    // EXPECT_EQ(Resolution::E300DPI, cloneCopyJobTicket.getIntent()->getScanYResolution());

    EXPECT_EQ(2,                                            cloneCopyJobTicket.getResult()->getCompletedCopies());
    EXPECT_EQ(10,                                           cloneCopyJobTicket.getResult()->getCompletedImpressions());
    EXPECT_EQ(100,                                          cloneCopyJobTicket.getResult()->getCurrentCuringTemperature());
    EXPECT_EQ(10,                                           cloneCopyJobTicket.getResult()->getCurrentPage());
    EXPECT_EQ(100,                                          cloneCopyJobTicket.getResult()->getProgress());
    EXPECT_EQ(100,                                          cloneCopyJobTicket.getResult()->getRemainingPrintingTime());
    EXPECT_EQ(true,                                         cloneCopyJobTicket.getResult()->areAllPagesDiscovered());
}

class GivenACopyJobTicket : public ::testing::Test
{
  public:
    GivenACopyJobTicket();

    virtual void SetUp() override;
    virtual void TearDown() override;
    void createOutputBinWithPageBasedFinisherCombination();
    void createPageBasedFinisher();

  protected:

    std::shared_ptr<dune::print::engine::PrintIntents> createDefaultPrintIntent();

    dune::imaging::types::MarginLayout convertToMarginLayout(dune::imaging::types::CopyMargins copyMargins);

    CopyJobTicket ticket_;

    //Mocks
    dune::print::engine::MockIPrintIntentsFactory* mockIPrintIntentsFactory_;
    dune::scan::scanningsystem::MockIScannerCapabilities* mockIScannerCapabilities_;
    dune::print::engine::MockIMedia* mockIMedia_;
    dune::job::MockIIntentsManager* intentsManager_;
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent_;
    MockIExportImport*                   mockIExportImport_{};

    dune::localization::MockILocaleProvider* mockLocaleProvider_;
    std::shared_ptr<dune::localization::MockILocale> mockLocale_;
    dune::imaging::MockIColorAccessControl* mockColorAccessControl_;

    MockIFinisherCombination finisherCombinationMock_;
    MockIMediaIOutput mockOutput1_, mockOutput2_, mockOutput3_, mockOutput4_, mockOutput5_, mockOutputAlternateBin_;
    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock1_, pageBasedFinisherMock2_, pageBasedFinisherMock3_, pageBasedFinisherMock4_, pageBasedFinisherMock5_;

    IMedia::FinisherList finishers1_ = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher *) {} ) // stapling
    };
    IMedia::FinisherList finishers2_ = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock2_, [](IMedia::IPageBasedFinisher *) {} ) // stapling  & Punching
    };
    IMedia::FinisherList finishers3_ = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock3_, [](IMedia::IPageBasedFinisher *) {} ) // punching
    };
    IMedia::FinisherList finishers4_ = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock4_, [](IMedia::IPageBasedFinisher *) {} ) // folding
    };
    IMedia::FinisherList finishers5_ = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock5_, [](IMedia::IPageBasedFinisher *) {} )  // bookletmaking
    };

    const std::vector<StaplingOptions> staplingMenuItems_ =
    {
        StaplingOptions::NONE,
        StaplingOptions::TOP_LEFT_ONE_POINT_ANY,
        StaplingOptions::TOP_RIGHT_ONE_POINT_ANY,
        StaplingOptions::LEFT_SIX_POINTS //added for ANY testing.
    };
    const std::vector<PunchingOptions>punchingMenuItems_ =
    {
        PunchingOptions::NONE,
        PunchingOptions::RIGHT_TWO_POINT_DIN,
        PunchingOptions::LEFT_TWO_POINT_DIN,
        PunchingOptions::TOP_TWO_POINT_DIN,
        PunchingOptions::BOTTOM_TWO_POINT_DIN,
        PunchingOptions::LEFT_FOUR_POINT_DIN,
        PunchingOptions::TOP_FOUR_POINT_DIN,
        PunchingOptions::RIGHT_TWO_POINT_US
    };
    const std::vector<StaplingOptions> allPossibleStaplingOptionList_ =
    {
        StaplingOptions::NONE,
        StaplingOptions::TOP_LEFT_ONE_POINT_ANY,
        StaplingOptions::TOP_RIGHT_ONE_POINT_ANY,
        StaplingOptions::LEFT_SIX_POINTS //added for ANY testing.
    };

    /*
        supportedStaplingOptionsInStaplingPunch_/supportedPunchingOptionsInStaplingPunch_ represents StaplingPunch of IFinisherCombination.
        So they should be synchronized with the optionsInStaplingAndPunchingMediaProcessingOption.
    */
    const std::map<PunchingOptions, std::vector<StaplingOptions>> supportedStaplingOptionsInStaplingPunch_ =
    {
        { PunchingOptions::NONE, { StaplingOptions::NONE, StaplingOptions::TOP_LEFT_ONE_POINT_ANY, StaplingOptions::TOP_RIGHT_ONE_POINT_ANY, StaplingOptions::LEFT_SIX_POINTS } },
        { PunchingOptions::RIGHT_TWO_POINT_DIN, { StaplingOptions::TOP_LEFT_ONE_POINT_ANY } },
        { PunchingOptions::LEFT_TWO_POINT_DIN, { StaplingOptions::TOP_LEFT_ONE_POINT_ANY } },
        { PunchingOptions::TOP_TWO_POINT_DIN, { StaplingOptions::TOP_LEFT_ONE_POINT_ANY } },
        { PunchingOptions::BOTTOM_TWO_POINT_DIN, { StaplingOptions::TOP_LEFT_ONE_POINT_ANY, StaplingOptions::TOP_RIGHT_ONE_POINT_ANY } },
        { PunchingOptions::LEFT_FOUR_POINT_DIN, { StaplingOptions::TOP_LEFT_ONE_POINT_ANY, StaplingOptions::TOP_RIGHT_ONE_POINT_ANY } },
        { PunchingOptions::TOP_FOUR_POINT_DIN, { StaplingOptions::TOP_LEFT_ONE_POINT_ANY, StaplingOptions::TOP_RIGHT_ONE_POINT_ANY } },
        { PunchingOptions::RIGHT_TWO_POINT_US, { StaplingOptions::TOP_RIGHT_ONE_POINT_ANY } }
    };
    std::map<StaplingOptions, std::vector<PunchingOptions>> supportedPunchingOptionsInStaplingPunch_ =
    {
        { StaplingOptions::NONE, {
                                    PunchingOptions::NONE,
                                    PunchingOptions::RIGHT_TWO_POINT_DIN,
                                    PunchingOptions::LEFT_TWO_POINT_DIN,
                                    PunchingOptions::TOP_TWO_POINT_DIN,
                                    PunchingOptions::BOTTOM_TWO_POINT_DIN,
                                    PunchingOptions::LEFT_FOUR_POINT_DIN,
                                    PunchingOptions::TOP_FOUR_POINT_DIN,
                                    PunchingOptions::RIGHT_TWO_POINT_US
                                    }
        },
        { StaplingOptions::TOP_LEFT_ONE_POINT_ANY, {
                                    PunchingOptions::NONE,
                                    PunchingOptions::RIGHT_TWO_POINT_DIN,
                                    PunchingOptions::LEFT_TWO_POINT_DIN,
                                    PunchingOptions::TOP_TWO_POINT_DIN,
                                    PunchingOptions::BOTTOM_TWO_POINT_DIN,
                                    PunchingOptions::LEFT_FOUR_POINT_DIN,
                                    PunchingOptions::TOP_FOUR_POINT_DIN
                                    }
        },
        { StaplingOptions::TOP_RIGHT_ONE_POINT_ANY, {
                                    PunchingOptions::TOP_TWO_POINT_DIN,
                                    PunchingOptions::BOTTOM_TWO_POINT_DIN,
                                    PunchingOptions::LEFT_FOUR_POINT_DIN,
                                    PunchingOptions::TOP_FOUR_POINT_DIN,
                                    PunchingOptions::RIGHT_TWO_POINT_US
                                    }
        },
        { StaplingOptions::LEFT_SIX_POINTS, { PunchingOptions::FOUR_POINT_ANY }
        }
    };
    const std::vector<StaplingOptions> paperPathStaplingOptions_ =
    {
        StaplingOptions::NONE,
        StaplingOptions::TOP_LEFT_ONE_POINT_ANY,
        StaplingOptions::TOP_RIGHT_ONE_POINT_ANY
    };
    const std::vector<PunchingOptions> allPossiblePunchingOptionList_ =
    {
        PunchingOptions::NONE,
        PunchingOptions::RIGHT_TWO_POINT_DIN,
        PunchingOptions::LEFT_TWO_POINT_DIN,
        PunchingOptions::TOP_TWO_POINT_DIN,
        PunchingOptions::BOTTOM_TWO_POINT_DIN,
        PunchingOptions::LEFT_FOUR_POINT_DIN,
        PunchingOptions::TOP_FOUR_POINT_DIN,
        PunchingOptions::RIGHT_TWO_POINT_US
    };
    const std::vector<PunchingOptions> paperPathPunchingOptions_ =
    {
        PunchingOptions::NONE,
        PunchingOptions::RIGHT_TWO_POINT_DIN,
        PunchingOptions::LEFT_TWO_POINT_DIN
    };
    const std::vector<FoldingOptions> allPossibleFoldingOptionList_ =
    {
        FoldingOptions::NONE,
        FoldingOptions::C_INWARD_TOP,
        FoldingOptions::C_INWARD_BOTTOM,
        FoldingOptions::C_OUTWARD_TOP,
        FoldingOptions::C_OUTWARD_BOTTOM,
        FoldingOptions::V_INWARD_TOP,
        FoldingOptions::V_OUTWARD_TOP,
        FoldingOptions::V_INWARD_BOTTOM //added for ANY testing.
    };
    const std::vector<FoldingOptions> paperPathFoldingOptions_ =
    {
        FoldingOptions::NONE,
        FoldingOptions::C_INWARD_TOP,
        FoldingOptions::V_OUTWARD_TOP
    };
    const std::vector<BookletMakingOptions> allPossibleBookletMakingOptionList_ =
    {
        BookletMakingOptions::NONE,
        BookletMakingOptions::SADDLE_STITCH
    };
    const std::vector<BookletMakingOptions> paperPathBookletMakingOptions_ =
    {
        BookletMakingOptions::NONE,
        BookletMakingOptions::SADDLE_STITCH
    };
    const std::vector<OrientedMediaSize> allPossibleMediaSizeList_ =
    {
        OrientedMediaSize(MediaSize(MediaSizeId::A4),               { MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE } ),
        OrientedMediaSize(MediaSize(MediaSizeId::LETTER),           { MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE } ),
        OrientedMediaSize(MediaSize(MediaSizeId::LEGAL),            { MediaOrientation::PORTRAIT } ),
        OrientedMediaSize(MediaSize(MediaSizeId::A3),               { MediaOrientation::PORTRAIT } ),
        OrientedMediaSize(MediaSize(MediaSizeId::JIS_B5),           { MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE } ),
        OrientedMediaSize(MediaSize(MediaSizeId::A5),               { MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE } ),
        OrientedMediaSize(MediaSize(MediaSizeId::OFICIO_216X340),   { MediaOrientation::PORTRAIT } ),
        OrientedMediaSize(MediaSize(MediaSizeId::ARCH_E3),          { MediaOrientation::PORTRAIT } ), //mismatch
        OrientedMediaSize(MediaSize(MediaSizeId::US_EXECUTIVE),     { MediaOrientation::PORTRAIT } ), //Not included at allPossibleMediaSizeListBookletAndFold_ for testing
        OrientedMediaSize(MediaSize(MediaSizeId::MEDIA8K_270X390),  { MediaOrientation::PORTRAIT } ), //added for requiredPairedContentOrientationProcess testing.
        OrientedMediaSize(MediaSize(MediaSizeId::COM10ENVELOPE),    { MediaOrientation::PORTRAIT } )  //added for ANY testing.
    };
    const std::vector<OrientedMediaSize> allPossibleMediaSizeListBookletAndFold_ =
    {
        OrientedMediaSize(MediaSize(MediaSizeId::A4),               { MediaOrientation::PORTRAIT } ),
        OrientedMediaSize(MediaSize(MediaSizeId::LETTER),           { MediaOrientation::PORTRAIT } ),
        OrientedMediaSize(MediaSize(MediaSizeId::LEGAL),            { MediaOrientation::PORTRAIT } ),
        OrientedMediaSize(MediaSize(MediaSizeId::A3),               { MediaOrientation::PORTRAIT } ),
        OrientedMediaSize(MediaSize(MediaSizeId::JIS_B5),           { MediaOrientation::PORTRAIT } ),
        OrientedMediaSize(MediaSize(MediaSizeId::OFICIO_216X340),   { MediaOrientation::PORTRAIT } ),
        OrientedMediaSize(MediaSize(MediaSizeId::ARCH_E3),          { MediaOrientation::PORTRAIT } ), //mismatch
        OrientedMediaSize(MediaSize(MediaSizeId::MEDIA8K_270X390),  { MediaOrientation::PORTRAIT } )  //added for requiredPairedContentOrientationProcess testing.
    };
    const std::vector<OrientedMediaSize> allPossibleMediaSizeListAlternateBin_ =
    {
        OrientedMediaSize(MediaSize(MediaSizeId::CHOU3_ENVELOPE),   { MediaOrientation::PORTRAIT } )
    };
    const std::vector<MediaId> allPossibleMediaIdList_ =
    {
        MediaId(MediaIdType::STATIONERY),
        MediaId(MediaIdType::HPECOFFICIENT),
        MediaId(MediaIdType::LIGHT),
        MediaId(MediaIdType::BOND),
        MediaId(MediaIdType::RECYCLED),
        MediaId(MediaIdType::PLAIN_PAPER_GRAPHICS),//mismatch
        MediaId(MediaIdType::PREPUNCHED), ////Not included at allPossibleMediaIdListBookletAndFold_ for testing
        MediaId(MediaIdType::PHOTOGRAPHICGLOSSY)    //added for ANY testing.
    };
    const std::vector<MediaId> allPossibleMediaIdListBookletAndFold_ =
    {
        MediaId(MediaIdType::STATIONERY),
        MediaId(MediaIdType::HPECOFFICIENT),
        MediaId(MediaIdType::LIGHT),
        MediaId(MediaIdType::BOND),
        MediaId(MediaIdType::RECYCLED),
        MediaId(MediaIdType::PLAIN_PAPER_GRAPHICS) //mismatch
    };
    const std::vector<MediaId> allPossibleMediaIdListAlternateBin_ =
    {
        MediaId(MediaIdType::CARDSTOCK)
    };
    const std::vector<ContentOrientation> allPossibleContentOrientationList_ = {
                                                                                ContentOrientation::PORTRAIT,
                                                                                ContentOrientation::REVERSEPORTRAIT,
                                                                                ContentOrientation::LANDSCAPE,
                                                                                ContentOrientation::REVERSELANDSCAPE
                                                                                };

    const std::vector<MediaDestinationId> allPossibleDestinationsList_ = {
        MediaDestinationId::UNDEFINED,
        MediaDestinationId::OUTPUTBIN1,
        MediaDestinationId::OUTPUTBIN2,
        MediaDestinationId::OUTPUTBIN3,
        MediaDestinationId::OUTPUTBIN4,
        MediaDestinationId::OUTPUTBIN5,
        MediaDestinationId::ALTERNATE
    };

    const std::vector<StaplesOutAction>  supportedStaplesOutAction_ =
    {
        StaplesOutAction::CONTINUE,
        StaplesOutAction::STOP
    };
    const std::vector<JobOffsetMode>  supportedJobOffsetModes_ =
    {
        JobOffsetMode::MODE_DISABLE,
        JobOffsetMode::MODE_ENABLE_NON_STAPLE_JOB
    };

    std::tuple<APIResult, StaplingMenuItemList> staplingMenuItemList_       {APIResult::NOT_AVAILABLE, {}};
    std::tuple<APIResult, std::vector<PunchingMenuItemPtr>> punchingMenuItemList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, std::vector<FoldingMenuItemPtr>> foldingMenuItemList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, std::vector<BookletMakingMenuItemPtr>> bookletMakingMenuItemList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, bool>isBookletMakerSupported_{APIResult::NOT_AVAILABLE, false};
    std::tuple<APIResult, std::vector<StaplesOutAction>> staplesOutActionList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, bool>isJobOffsetSupported_{APIResult::NOT_AVAILABLE, false};
    std::tuple<APIResult, std::vector<JobOffsetMode>> jobOffsetModeList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, std::vector<MediaProcessingTypePtr>> mediaProcessingTypeInstanceList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, StaplingAndPunchingMediaProcessingTypePtr> staplingMediaProcessingType_{APIResult::UNIMPLEMENTED, nullptr};
    std::tuple<APIResult, StaplingAndPunchingMediaProcessingTypePtr> punchingMediaProcessingType_{APIResult::UNIMPLEMENTED, nullptr};
    std::tuple<APIResult, StaplingAndPunchingMediaProcessingTypePtr> staplingAndPunchingMediaProcessingType_{APIResult::UNIMPLEMENTED, nullptr};
    std::tuple<APIResult, FoldingMediaProcessingTypePtr> foldingMediaProcessingType_{APIResult::UNIMPLEMENTED, nullptr};
    std::tuple<APIResult, BookletMakingMediaProcessingTypePtr> bookletMakingMediaProcessingType_{APIResult::UNIMPLEMENTED, nullptr};
    std::tuple<APIResult, StaplingAndPunchingMediaProcessingTypePtr> staplingAndPunchingMediaProcessingTypeNull_{APIResult::UNIMPLEMENTED, nullptr};
    std::tuple<APIResult, FoldingMediaProcessingTypePtr> foldingMediaProcessingTypeNull_{APIResult::UNIMPLEMENTED, nullptr};
    std::tuple<APIResult, BookletMakingMediaProcessingTypePtr> bookletMakingMediaProcessingTypeNull_{APIResult::UNIMPLEMENTED, nullptr};
    std::tuple<APIResult, MediaProcessingTypes> defaultMediaProcessingTypeNotAvailable_{APIResult::NOT_AVAILABLE, MediaProcessingTypes::BOOKLET_MAKING};
    std::tuple<APIResult, DefaultMediaProcessingOption> defaultMediaProcessingOptionNotAvailable_{APIResult::NOT_AVAILABLE, {}};
    std::tuple<APIResult, MediaProcessingTypes> defaultMediaProcessingType_{APIResult::OK, MediaProcessingTypes::BOOKLET_MAKING};
    std::tuple<APIResult, DefaultMediaProcessingOption> defaultMediaProcessingOption_{APIResult::OK, { StapleOptions::NONE, PunchingOptions::NONE, FoldingOptions::NONE, BookletMakingOptions::SADDLE_STITCH, JogOptions::NONE }};
    std::tuple<APIResult, bool>isStaplingSupported_{APIResult::NOT_AVAILABLE, false};
    std::tuple<APIResult, bool>isPunchingSupported_{APIResult::NOT_AVAILABLE, false};
    std::tuple<APIResult, bool>isFoldingSupported_{APIResult::NOT_AVAILABLE, false};
    std::tuple<APIResult, std::vector<StaplingOptions>> paperPathStaplingOptionList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, std::vector<PunchingOptions>> paperPathPunchingOptionList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, std::vector<FoldingOptions>> paperPathFoldingOptionList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, std::vector<BookletMakingOptions>> paperPathBookletMakingOptionList_{APIResult::UNIMPLEMENTED, {}};
    std::tuple<APIResult, std::vector<IPPDataPtr>> ippDataListStaple_{APIResult::NOT_AVAILABLE, {}};
    std::tuple<APIResult, std::vector<IPPDataPtr>> ippDataListPunch_{APIResult::NOT_AVAILABLE, {}};
    std::tuple<APIResult, std::vector<IPPDataPtr>> ippDataListStapleAndPunch_{APIResult::NOT_AVAILABLE, {}};
    std::tuple<APIResult, std::vector<IPPDataPtr>> ippDataListFold_{APIResult::NOT_AVAILABLE, {}};
    std::tuple<APIResult, std::vector<IPPDataPtr>> ippDataListBookletMaking_{APIResult::NOT_AVAILABLE, {}};
    std::tuple<APIResult, std::vector<IPPDataPtr>> ippDataListJog_{APIResult::NOT_AVAILABLE, {}};
    ProcessingOptionDirection processingOptionDirectionIPPDataTest_ = ProcessingOptionDirection::INWARD;
    ProcessingOptionReferenceEdge processingOptionReferenceEdgeIPPDataTest_ = ProcessingOptionReferenceEdge::TOP;
    ProcessingOptionLocations processingOptionLocationsIPPDataTest_ = { {4500, 16500} };
    ProcessingOptionOffsets processingOptionOffsetsIPPDataTest_= { 14850 };

    JobPageOrder appJobPageOrderForFolding_ = JobPageOrder::FRONT_TO_BACK;
    DuplexPageOrder appDuplexPageOrderForFolding_ = DuplexPageOrder::CORRECT_ORDER;
    JobPageOrder formatterJobPageOrderForFolding_ = JobPageOrder::BACK_TO_FRONT;;
    DuplexPageOrder formatterDuplexPageOrderForFolding_ = DuplexPageOrder::REVERSE_ORDER;
    FormatterRotationPriority formatterRotationPriorityForFolding_ = FormatterRotationPriority::RotationBasedOnBackSide;
    bool convertSimplexToDuplexForFolding_ = false;
    bool isImageRotationSupportedBySizeForFolding_ = true;
    MinAndMax setsLimitForCFold_{Distance(1, 1), Distance(3, 1)};
    MinAndMax setsLimitForVFold_{Distance(1, 1), Distance(5, 1)};

    JobPageOrder appJobPageOrderForBookletMaking_ = JobPageOrder::BACK_TO_FRONT;
    DuplexPageOrder appDuplexPageOrderForBookletMaking_ = DuplexPageOrder::REVERSE_ORDER;
    JobPageOrder formatterJobPageOrderForBookletMaking_ = JobPageOrder::FRONT_TO_BACK;;
    DuplexPageOrder formatterDuplexPageOrderForBookletMaking_ = DuplexPageOrder::CORRECT_ORDER;
    FormatterRotationPriority formatterRotationPriorityForBookletMaking_ = FormatterRotationPriority::RotationBasedOnFrontSide;
    bool convertSimplexToDuplexForBookletMaking_ = true;
    bool isImageRotationSupportedBySizeForBookletMaking_ = false;
    MinAndMax setsLimitForBookletMaking_{Distance(1, 1), Distance(25, 1)};

};

GivenACopyJobTicket::GivenACopyJobTicket()
{
}

void GivenACopyJobTicket::SetUp()
{
    printIntent_ = createDefaultPrintIntent();
    mockIPrintIntentsFactory_ = new dune::print::engine::MockIPrintIntentsFactory();
    mockIScannerCapabilities_ = new dune::scan::scanningsystem::MockIScannerCapabilities();
    mockIMedia_ = new dune::print::engine::MockIMedia();
    intentsManager_ = new dune::job::MockIIntentsManager();
    mockIExportImport_ = new MockIExportImport();
    mockLocaleProvider_ = new dune::localization::MockILocaleProvider();
    mockLocale_ = std::make_shared<dune::localization::MockILocale>();
    mockColorAccessControl_ = new dune::imaging::MockIColorAccessControl();

    //Set interfaces
    ticket_.setScanCapabilitiesInterface(mockIScannerCapabilities_);
    ticket_.setPrintIntentsFactory(mockIPrintIntentsFactory_);
    ticket_.setMediaInterface(mockIMedia_);
    ticket_.setIntentsManager(intentsManager_);
    ticket_.setLocalizationInterface(mockLocaleProvider_);
    ticket_.setColorAccessControlInterface(mockColorAccessControl_);

    ON_CALL(*mockIPrintIntentsFactory_, createPrintIntentsPage()).WillByDefault(Return(printIntent_));

    Margins desiredMargins_{Distance(236, 1200), Distance(236, 1200), Distance(236, 1200), Distance(236, 1200)};
    ON_CALL(*mockIMedia_, getMargins(_)).WillByDefault(Return(std::tuple<APIResult, Margins>(APIResult::OK, desiredMargins_)));

    createOutputBinWithPageBasedFinisherCombination();
    createPageBasedFinisher();
}

void GivenACopyJobTicket::createOutputBinWithPageBasedFinisherCombination()
{
    const std::vector<IMedia::FinisherCombinationPtr> finisherCombinations = { IMedia::FinisherCombinationPtr(&finisherCombinationMock_, [](IMedia::IFinisherCombination *) {} ) };
    ON_CALL(mockOutput1_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));
    ON_CALL(mockOutput2_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));
    ON_CALL(mockOutput3_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));
    ON_CALL(mockOutput4_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));
    ON_CALL(mockOutput5_,getValidFinisherCombinations()).WillByDefault(Return(std::make_tuple(APIResult::OK, finisherCombinations)));

    ON_CALL(mockOutput1_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeList_)));
    ON_CALL(mockOutput1_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdList_)));
    ON_CALL(mockOutput1_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[0]));
    ON_CALL(mockOutput1_, getFinishers())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, finishers1_)));

    ON_CALL(mockOutput2_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeList_)));
    ON_CALL(mockOutput2_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdList_)));
    ON_CALL(mockOutput2_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[1]));
    ON_CALL(mockOutput2_, getFinishers())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, finishers2_)));

    ON_CALL(mockOutput3_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeList_)));
    ON_CALL(mockOutput3_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdList_)));
    ON_CALL(mockOutput3_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[2]));
    ON_CALL(mockOutput3_, getFinishers())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, finishers3_)));

    ON_CALL(mockOutput4_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeListBookletAndFold_)));
    ON_CALL(mockOutput4_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdListBookletAndFold_)));
    ON_CALL(mockOutput4_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[3]));
    ON_CALL(mockOutput4_, getFinishers())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, finishers4_)));

    ON_CALL(mockOutput5_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeListBookletAndFold_)));
    ON_CALL(mockOutput5_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdList_)));
    ON_CALL(mockOutput5_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[4]));
    ON_CALL(mockOutput5_, getFinishers())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, finishers5_)));

    ON_CALL(mockOutputAlternateBin_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeListAlternateBin_)));
    ON_CALL(mockOutputAlternateBin_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdListAlternateBin_)));
    ON_CALL(mockOutputAlternateBin_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[5]));

    const IMedia::OutputList outputs = {
        IMedia::OutputPtr(&mockOutput1_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(&mockOutput2_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(&mockOutput3_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(&mockOutput4_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(&mockOutput5_,[](IMedia::IOutput *) {}),
        IMedia::OutputPtr(&mockOutputAlternateBin_,[](IMedia::IOutput *) {})
    };
    ON_CALL(*mockIMedia_, getOutputDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::OK, outputs)));

    StaplingMenuItemList staplingMenuItemVec;
    MinAndMax pagesPerSetLimit{Distance(1, 1), Distance(100, 1)};
    auto staplingMenuItem = std::make_shared<StaplingMenuItem>(pagesPerSetLimit, staplingMenuItems_);
    staplingMenuItemVec.push_back(static_cast<StaplingMenuItemPtr>(staplingMenuItem));
    staplingMenuItemList_ = std::tuple<APIResult, StaplingMenuItemList>(APIResult::OK, staplingMenuItemVec);
    ON_CALL(finisherCombinationMock_,getStaplingMenuItems()).WillByDefault(ReturnRef(staplingMenuItemList_));
    ON_CALL(finisherCombinationMock_, getSupportedStaplingOptions(_))
        .WillByDefault(Invoke(
        [&](const PunchingOptions& punchingOption) -> std::tuple<APIResult, std::vector<StaplingOptions>> {
            auto it = supportedStaplingOptionsInStaplingPunch_.find(punchingOption);
            if (it != supportedStaplingOptionsInStaplingPunch_.end()) {
                // If the punchingOption is found in the map, return the corresponding StaplingOptions
                return {APIResult::OK, it->second};
            } else {
                // If the punchingOption is not found in the map, return an empty vector
                return {APIResult::NOT_AVAILABLE, {}};
            }
        }));
    ON_CALL(finisherCombinationMock_, getSupportedPunchingOptions(_))
        .WillByDefault(Invoke(
        [&](const StaplingOptions& staplingOption) -> std::tuple<APIResult, std::vector<PunchingOptions>> {
            auto it = supportedPunchingOptionsInStaplingPunch_.find(staplingOption);
            if (it != supportedPunchingOptionsInStaplingPunch_.end()) {
                // If the staplingOption is found in the map, return the corresponding PunchingOptions
                return {APIResult::OK, it->second};
            } else {
                // If the staplingOption is not found in the map, return an empty vector
                return {APIResult::NOT_AVAILABLE, {}};
            }
        }));

    PunchingMenuItemList punchingMenuItemVec;
    auto punchingMenuItem = std::make_shared<PunchingMenuItem>(pagesPerSetLimit, punchingMenuItems_);
    punchingMenuItemVec.push_back(static_cast<PunchingMenuItemPtr>(punchingMenuItem));
    punchingMenuItemList_ = std::tuple<APIResult, PunchingMenuItemList>(APIResult::OK, punchingMenuItemVec);
    ON_CALL(finisherCombinationMock_,getPunchingMenuItems()).WillByDefault(ReturnRef(punchingMenuItemList_));

    FoldingMenuItemList foldingMenuItemVec;
    auto foldingMenuItem = std::make_shared<FoldingMenuItem>(pagesPerSetLimit, allPossibleFoldingOptionList_);
    foldingMenuItemVec.push_back(static_cast<FoldingMenuItemPtr>(foldingMenuItem));
    foldingMenuItemList_ = std::tuple<APIResult, FoldingMenuItemList>(APIResult::OK, foldingMenuItemVec);
    ON_CALL(finisherCombinationMock_,getFoldingMenuItems()).WillByDefault(ReturnRef(foldingMenuItemList_));

    BookletMakingMenuItemList bookletMakingMenuItemVec;
    auto bookletMakingMenuItem = std::make_shared<BookletMakingMenuItem>(pagesPerSetLimit, allPossibleBookletMakingOptionList_);
    bookletMakingMenuItemVec.push_back(static_cast<BookletMakingMenuItemPtr>(bookletMakingMenuItem));
    bookletMakingMenuItemList_ = std::tuple<APIResult, BookletMakingMenuItemList>(APIResult::OK, bookletMakingMenuItemVec);
    ON_CALL(finisherCombinationMock_,getBookletMakingMenuItems()).WillByDefault(ReturnRef(bookletMakingMenuItemList_));

    isBookletMakerSupported_ = std::tuple<APIResult, bool>(APIResult::OK, true);
    ON_CALL(finisherCombinationMock_,isBookletMakerSupported()).WillByDefault(ReturnRef(isBookletMakerSupported_));

    staplesOutActionList_ = std::tuple<APIResult, std::vector<StaplesOutAction>>(APIResult::OK, supportedStaplesOutAction_);
    ON_CALL(finisherCombinationMock_,getStaplesOutActions()).WillByDefault(ReturnRef(staplesOutActionList_));

    isJobOffsetSupported_ = std::tuple<APIResult, bool>(APIResult::OK, true);
    ON_CALL(finisherCombinationMock_,isJobOffsetSupported()).WillByDefault(ReturnRef(isJobOffsetSupported_));

    jobOffsetModeList_ = std::tuple<APIResult, std::vector<JobOffsetMode>>(APIResult::OK, supportedJobOffsetModes_);
    ON_CALL(finisherCombinationMock_,getJobOffsetModes()).WillByDefault(ReturnRef(jobOffsetModeList_));

    isStaplingSupported_ = std::tuple<APIResult, bool>(APIResult::OK, true);
    ON_CALL(finisherCombinationMock_,isStaplingSupported()).WillByDefault(ReturnRef(isStaplingSupported_));

    isPunchingSupported_ = std::tuple<APIResult, bool>(APIResult::OK, true);
    ON_CALL(finisherCombinationMock_,isPunchingSupported()).WillByDefault(ReturnRef(isPunchingSupported_));

    isFoldingSupported_ = std::tuple<APIResult, bool>(APIResult::OK, true);
    ON_CALL(finisherCombinationMock_,isFoldingSupported()).WillByDefault(ReturnRef(isFoldingSupported_));

    paperPathStaplingOptionList_ = std::tuple<APIResult, std::vector<StaplingOptions>>(APIResult::OK, paperPathStaplingOptions_);
    paperPathPunchingOptionList_ = std::tuple<APIResult, std::vector<PunchingOptions>>(APIResult::OK, paperPathPunchingOptions_);
    paperPathFoldingOptionList_ = std::tuple<APIResult, std::vector<FoldingOptions>>(APIResult::OK, paperPathFoldingOptions_);
    paperPathBookletMakingOptionList_ = std::tuple<APIResult, std::vector<BookletMakingOptions>>(APIResult::OK, paperPathBookletMakingOptions_);

    ON_CALL(finisherCombinationMock_,getStaplingOptionsSupportedInPaperPath()).WillByDefault(Return(paperPathStaplingOptionList_));
    ON_CALL(finisherCombinationMock_,getPunchingOptionsSupportedInPaperPath()).WillByDefault(Return(paperPathPunchingOptionList_));
    ON_CALL(finisherCombinationMock_,getFoldingOptionsSupportedInPaperPath()).WillByDefault(Return(paperPathFoldingOptionList_));
    ON_CALL(finisherCombinationMock_,getBookletMakingOptionsSupportedInPaperPath()).WillByDefault(Return(paperPathBookletMakingOptionList_));
}

void GivenACopyJobTicket::createPageBasedFinisher()
{
    std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>> mediaSizeListInMediaSizeCharacteristicsData1 =
    {
        {
            OrientedMediaSize(MediaSize(MediaSizeId::A4),               { MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE } ),
            { FinishingContentOrientation::PORTRAIT, FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT, FinishingContentOrientation::REVERSE_LANDSCAPE }
        },
        {
            OrientedMediaSize(MediaSize(MediaSizeId::LETTER),           { MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE } ),
            { FinishingContentOrientation::PORTRAIT, FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT, FinishingContentOrientation::REVERSE_LANDSCAPE }
        },
        {
            OrientedMediaSize(MediaSize(MediaSizeId::LEGAL),            { MediaOrientation::PORTRAIT } ),
            { FinishingContentOrientation::PORTRAIT, FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT }
        },
        {
            OrientedMediaSize(MediaSize(MediaSizeId::MEDIA8K_270X390),            { MediaOrientation::PORTRAIT } ),
            { FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT }
        },
        {
            OrientedMediaSize(MediaSize(MediaSizeId::A5),            { MediaOrientation::PORTRAIT } ),
            { FinishingContentOrientation::PORTRAIT, FinishingContentOrientation::REVERSE_PORTRAIT }
        }
    };
    std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>> mediaSizeListInMediaSizeCharacteristicsData2 =
    {
        {
            OrientedMediaSize(MediaSize(MediaSizeId::JIS_B5),           { MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE } ),
            { FinishingContentOrientation::PORTRAIT, FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT, FinishingContentOrientation::REVERSE_LANDSCAPE }
        },
        {
            OrientedMediaSize(MediaSize(MediaSizeId::OFICIO_216X340),   { MediaOrientation::PORTRAIT } ),
            { FinishingContentOrientation::PORTRAIT, FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT, FinishingContentOrientation::REVERSE_LANDSCAPE }
        },
        {
            OrientedMediaSize(MediaSize(MediaSizeId::LEGAL),            { MediaOrientation::PORTRAIT } ),
            { FinishingContentOrientation::PORTRAIT, FinishingContentOrientation::REVERSE_PORTRAIT, FinishingContentOrientation::REVERSE_LANDSCAPE }
        },
        {
            OrientedMediaSize(MediaSize(MediaSizeId::A5),            { MediaOrientation::LANDSCAPE } ),
            { FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_LANDSCAPE }
        }
    };
    std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>> mediaSizeListInMediaSizeCharacteristicsData3 = //added for ANY testing.
    {
        {
            OrientedMediaSize(MediaSize(MediaSizeId::COM10ENVELOPE),           { MediaOrientation::PORTRAIT} ),
            { FinishingContentOrientation::PORTRAIT}
        }
    };
    std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>> mediaSizeCharacteristics_LEFT_1PT =
    {
        { OrientedMediaSize(MediaSize(MediaSizeId::A4), {MediaOrientation::LANDSCAPE}), {FinishingContentOrientation::REVERSE_PORTRAIT, FinishingContentOrientation::REVERSE_LANDSCAPE}},
        { OrientedMediaSize(MediaSize(MediaSizeId::A4), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LETTER), {MediaOrientation::LANDSCAPE}), {FinishingContentOrientation::REVERSE_PORTRAIT, FinishingContentOrientation::REVERSE_LANDSCAPE}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LETTER), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LEGAL), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT}}
    };
    std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>> mediaSizeCharacteristics_LEFT_1PT_LEFT_2PT_DIN =
    {
        { OrientedMediaSize(MediaSize(MediaSizeId::A4), {MediaOrientation::LANDSCAPE}), {FinishingContentOrientation::REVERSE_PORTRAIT}},
        { OrientedMediaSize(MediaSize(MediaSizeId::A4), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LETTER), {MediaOrientation::LANDSCAPE}), {FinishingContentOrientation::REVERSE_PORTRAIT}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LETTER), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LEGAL), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE}}
    };
    std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>> mediaSizeCharacteristics_LEFT_2PT_DIN =
    {
        { OrientedMediaSize(MediaSize(MediaSizeId::A4), {MediaOrientation::LANDSCAPE}), {FinishingContentOrientation::REVERSE_PORTRAIT}},
        { OrientedMediaSize(MediaSize(MediaSizeId::A4), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LETTER), {MediaOrientation::LANDSCAPE}), {FinishingContentOrientation::REVERSE_PORTRAIT}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LETTER), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LEGAL), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE}}
    };
    std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>> mediaSizeCharacteristics_C_IN_TOP =
    {
        { OrientedMediaSize(MediaSize(MediaSizeId::A4), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LETTER), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT}},
        { OrientedMediaSize(MediaSize(MediaSizeId::MEDIA8K_270X390), { MediaOrientation::PORTRAIT } ), { FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT}}
    };
    std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>> mediaSizeCharacteristics_BOOKLET_MAKER =
    {
        { OrientedMediaSize(MediaSize(MediaSizeId::A4), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::REVERSE_PORTRAIT, FinishingContentOrientation::REVERSE_LANDSCAPE}},
        { OrientedMediaSize(MediaSize(MediaSizeId::LETTER), {MediaOrientation::PORTRAIT}), {FinishingContentOrientation::REVERSE_PORTRAIT, FinishingContentOrientation::REVERSE_LANDSCAPE}},
        { OrientedMediaSize(MediaSize(MediaSizeId::MEDIA8K_270X390), { MediaOrientation::PORTRAIT } ), { FinishingContentOrientation::LANDSCAPE, FinishingContentOrientation::REVERSE_PORTRAIT}}
    };
    std::vector<MediaId> supportedOptionMediaTypesSupportedData1 =
    {
        MediaId(MediaIdType::STATIONERY),
        MediaId(MediaIdType::LIGHT),
        MediaId(MediaIdType::BOND)
    };
    std::vector<MediaId> supportedOptionMediaTypesSupportedData2 =
    {
        MediaId(MediaIdType::HPECOFFICIENT),
        MediaId(MediaIdType::LIGHT),
        MediaId(MediaIdType::BOND),
        MediaId(MediaIdType::RECYCLED)
    };
    std::vector<MediaId> supportedOptionMediaTypesSupportedData3 = //added for ANY testing.
    {
        MediaId(MediaIdType::PHOTOGRAPHICGLOSSY)
    };

    std::vector<std::tuple<std::tuple<StaplingOptions, PunchingOptions>, std::tuple<std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>>, std::vector<MediaId>>>> optionsInStaplingAndPunchingMediaProcessingOption = {
        {{ StaplingOptions::TOP_LEFT_ONE_POINT_ANY, PunchingOptions::NONE },                    {mediaSizeCharacteristics_LEFT_1PT, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_LEFT_ONE_POINT_ANY, PunchingOptions::RIGHT_TWO_POINT_DIN },     {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_LEFT_ONE_POINT_ANY, PunchingOptions::LEFT_TWO_POINT_DIN },      {mediaSizeCharacteristics_LEFT_1PT_LEFT_2PT_DIN, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_LEFT_ONE_POINT_ANY, PunchingOptions::TOP_TWO_POINT_DIN },       {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_LEFT_ONE_POINT_ANY, PunchingOptions::BOTTOM_TWO_POINT_DIN },    {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_LEFT_ONE_POINT_ANY, PunchingOptions::NONE },                    {mediaSizeCharacteristics_LEFT_1PT, supportedOptionMediaTypesSupportedData2}},
        {{ StaplingOptions::TOP_LEFT_ONE_POINT_ANY, PunchingOptions::LEFT_FOUR_POINT_DIN },     {mediaSizeListInMediaSizeCharacteristicsData2, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_LEFT_ONE_POINT_ANY, PunchingOptions::TOP_FOUR_POINT_DIN },      {mediaSizeListInMediaSizeCharacteristicsData2, supportedOptionMediaTypesSupportedData2}},
        {{ StaplingOptions::LEFT_SIX_POINTS, PunchingOptions::FOUR_POINT_ANY },                 {mediaSizeListInMediaSizeCharacteristicsData3, supportedOptionMediaTypesSupportedData3}},
        {{ StaplingOptions::TOP_RIGHT_ONE_POINT_ANY, PunchingOptions::TOP_TWO_POINT_DIN },      {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_RIGHT_ONE_POINT_ANY, PunchingOptions::BOTTOM_TWO_POINT_DIN },   {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_RIGHT_ONE_POINT_ANY, PunchingOptions::LEFT_FOUR_POINT_DIN },    {mediaSizeListInMediaSizeCharacteristicsData2, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_RIGHT_ONE_POINT_ANY, PunchingOptions::TOP_FOUR_POINT_DIN },     {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::TOP_RIGHT_ONE_POINT_ANY, PunchingOptions::RIGHT_TWO_POINT_US },     {mediaSizeListInMediaSizeCharacteristicsData2, supportedOptionMediaTypesSupportedData1}},
        {{ StaplingOptions::NONE, PunchingOptions::LEFT_TWO_POINT_DIN },                        {mediaSizeCharacteristics_LEFT_2PT_DIN, supportedOptionMediaTypesSupportedData1}},
        /* StaplingOptions::CENTER_POINT_POINT and PunchingOptions::BOTTOM_FOUR_POINT_SWD are not possible option. */
        {{ StaplingOptions::CENTER_POINT_POINT, PunchingOptions::BOTTOM_FOUR_POINT_SWD },       {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}}
    };

    std::vector<StaplingAndPunchingMediaProcessingOptionPtr> staplingAndPunchingMediaProcessingOptionPtrVec;
    for (const auto optionInStaplingAndPunchingMediaProcessingOption : optionsInStaplingAndPunchingMediaProcessingOption)
    {

        auto staplingOptionInMediaProcessingOption = std::get<0>(std::get<0>(optionInStaplingAndPunchingMediaProcessingOption));
        auto punchingOptionInMediaProcessingOption = std::get<1>(std::get<0>(optionInStaplingAndPunchingMediaProcessingOption));
        auto mediaSizeListMediaSizeCharacteristics = std::get<0>(std::get<1>(optionInStaplingAndPunchingMediaProcessingOption));
        auto supportedOptionMediaTypesSupported = std::get<1>(std::get<1>(optionInStaplingAndPunchingMediaProcessingOption));

        std::vector<MediaSizeCharacteristicsOrientationPtr> mediaSizeCharacteristicsOrientationPtrVec;
        for (const auto mediaSizeInMediaSizeCharacteristics : mediaSizeListMediaSizeCharacteristics)
        {
            std::vector<FinishingContentOrientation> finishingContentOrientationVec;
            for (const auto contentOrientation : std::get<1>(mediaSizeInMediaSizeCharacteristics))
            {
                finishingContentOrientationVec.push_back(contentOrientation);
            }

            std::vector<IPPDataPtr> iPPDataPtrVec;
            ProcessingOptionDirection processingOptionDirection = ProcessingOptionDirection::NONE;
            ProcessingOptionReferenceEdge processingOptionReferenceEdge = ProcessingOptionReferenceEdge::NONE;
            ProcessingOptionLocations processingOptionLocations;
            ProcessingOptionOffsets processingOptionOffsets;
            auto iPPDataPtr = std::make_shared<IPPData>(processingOptionDirection, processingOptionReferenceEdge, processingOptionLocations, processingOptionOffsets);
            iPPDataPtrVec.push_back(iPPDataPtr);

            auto orientedMediaSize = std::get<0>(mediaSizeInMediaSizeCharacteristics);
            auto mediaSizeCharacteristicsOrientationPtr = std::make_shared<MediaSizeCharacteristicsOrientation>(orientedMediaSize, finishingContentOrientationVec, iPPDataPtrVec, false, false);
            mediaSizeCharacteristicsOrientationPtrVec.push_back(mediaSizeCharacteristicsOrientationPtr);
        }

        MediaProcessingOptionName mediaProcessingOptionName;
        MediaProcessingOptionName mediaProcessingOptionOverrideNameLetterLedgerMixedMedia;
        uint32_t minBindingLimit = 2, maxBindingLimit = 65;
        std::vector<MediaProcessingBoundary> mediaProcessingBoundariesVec;
        MinAndMax bindingLimit(Distance(minBindingLimit, 1), Distance(maxBindingLimit, 1));
        MinAndMax tempMediaWidthLimit, tempMediaHeightLimit;
        bool isImageRotationSupportedBySize = true;
        auto staplingAndPunchingMediaProcessingOptionPtr = std::make_shared<StaplingAndPunchingMediaProcessingOption>(mediaProcessingOptionName,
                                                                                                                    mediaProcessingOptionOverrideNameLetterLedgerMixedMedia,
                                                                                                                    supportedOptionMediaTypesSupported,
                                                                                                                    tempMediaWidthLimit, tempMediaHeightLimit,
                                                                                                                    mediaProcessingBoundariesVec,
                                                                                                                    mediaSizeCharacteristicsOrientationPtrVec,
                                                                                                                    staplingOptionInMediaProcessingOption,
                                                                                                                    punchingOptionInMediaProcessingOption,
                                                                                                                    bindingLimit,
                                                                                                                    isImageRotationSupportedBySize);
        staplingAndPunchingMediaProcessingOptionPtrVec.push_back(staplingAndPunchingMediaProcessingOptionPtr);
    }

    MediaProcessingTypes mediaProcessingType = MediaProcessingTypes::MIN;
    std::string mediaProcessingTypeName;
    auto staplingAndPunchingMediaProcessingTypePtr = std::make_shared<StaplingAndPunchingMediaProcessingType>(mediaProcessingTypeName,
                                                                                                    mediaProcessingType,
                                                                                                    staplingAndPunchingMediaProcessingOptionPtrVec);

    std::vector <
                    std::tuple  <
                                    FoldingOptions,
                                    std::tuple<std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>>, std::vector<MediaId>>,
                                    MinAndMax
                                >
                > optionsInFoldingMediaProcessingOption = {
        {FoldingOptions::C_INWARD_TOP, {mediaSizeCharacteristics_C_IN_TOP, supportedOptionMediaTypesSupportedData1}, setsLimitForCFold_},
        {FoldingOptions::C_INWARD_BOTTOM, {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}, setsLimitForCFold_},
        {FoldingOptions::C_OUTWARD_BOTTOM, {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}, setsLimitForCFold_},
        {FoldingOptions::V_INWARD_TOP, {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData1}, setsLimitForVFold_},
        {FoldingOptions::C_OUTWARD_TOP, {mediaSizeListInMediaSizeCharacteristicsData1, supportedOptionMediaTypesSupportedData2}, setsLimitForCFold_},
        {FoldingOptions::V_OUTWARD_TOP, {mediaSizeListInMediaSizeCharacteristicsData2, supportedOptionMediaTypesSupportedData1}, setsLimitForVFold_}
    };

    std::vector<FoldingMediaProcessingOptionPtr> foldingMediaProcessingOptionPtrVec;
    for (const auto optionInFoldingMediaProcessingOption : optionsInFoldingMediaProcessingOption)
    {

        auto foldingOptionInMediaProcessingOption = std::get<0>(optionInFoldingMediaProcessingOption);
        auto mediaSizeListMediaSizeCharacteristics = std::get<0>(std::get<1>(optionInFoldingMediaProcessingOption));
        auto supportedOptionMediaTypesSupported = std::get<1>(std::get<1>(optionInFoldingMediaProcessingOption));
        auto setsLimit =  std::get<2>(optionInFoldingMediaProcessingOption);
        std::vector<MediaSizeCharacteristicsOrientationPtr> mediaSizeCharacteristicsOrientationPtrVec;
        for (const auto mediaSizeInMediaSizeCharacteristics : mediaSizeListMediaSizeCharacteristics)
        {
            std::vector<FinishingContentOrientation> finishingContentOrientationVec;
            for (const auto contentOrientation : std::get<1>(mediaSizeInMediaSizeCharacteristics))
            {
                finishingContentOrientationVec.push_back(contentOrientation);
            }

            std::vector<IPPDataPtr> iPPDataPtrVec;
            ProcessingOptionDirection processingOptionDirection = ProcessingOptionDirection::INWARD;
            ProcessingOptionReferenceEdge processingOptionReferenceEdge = ProcessingOptionReferenceEdge::NONE;
            ProcessingOptionLocations processingOptionLocations;
            ProcessingOptionOffsets processingOptionOffsets;
            auto iPPDataPtr = std::make_shared<IPPData>(processingOptionDirection, processingOptionReferenceEdge, processingOptionLocations, processingOptionOffsets);
            iPPDataPtrVec.push_back(iPPDataPtr);

            auto orientedMediaSize = std::get<0>(mediaSizeInMediaSizeCharacteristics);
            auto mediaSizeCharacteristicsOrientationPtr = std::make_shared<MediaSizeCharacteristicsOrientation>(orientedMediaSize, finishingContentOrientationVec, iPPDataPtrVec, false, false);
            mediaSizeCharacteristicsOrientationPtrVec.push_back(mediaSizeCharacteristicsOrientationPtr);
        }

        MediaProcessingOptionName mediaProcessingOptionName;
        MediaProcessingOptionName mediaProcessingOptionOverrideNameLetterLedgerMixedMedia;
        std::vector<MediaProcessingBoundary> mediaProcessingBoundariesVec;
        MinAndMax tempMediaWidthLimit, tempMediaHeightLimit;

        auto mediaProcessingOptionPtr = std::make_shared<FoldingMediaProcessingOption>(mediaProcessingOptionName,
                                                                                            mediaProcessingOptionOverrideNameLetterLedgerMixedMedia,
                                                                                            supportedOptionMediaTypesSupported,
                                                                                            tempMediaWidthLimit, tempMediaHeightLimit,
                                                                                            mediaProcessingBoundariesVec,
                                                                                            mediaSizeCharacteristicsOrientationPtrVec,
                                                                                            setsLimit,
                                                                                            appJobPageOrderForFolding_,
                                                                                            appDuplexPageOrderForFolding_,
                                                                                            formatterJobPageOrderForFolding_,
                                                                                            formatterDuplexPageOrderForFolding_,
                                                                                            formatterRotationPriorityForFolding_,
                                                                                            convertSimplexToDuplexForFolding_,
                                                                                            isImageRotationSupportedBySizeForFolding_,
                                                                                            foldingOptionInMediaProcessingOption);
        foldingMediaProcessingOptionPtrVec.push_back(mediaProcessingOptionPtr);
    }

    bool isSheetsPerSetSupported = false;
    auto foldingMediaProcessingTypePtr = std::make_shared<FoldingMediaProcessingType>(mediaProcessingTypeName,
                                                                                                    mediaProcessingType,
                                                                                                    foldingMediaProcessingOptionPtrVec,
                                                                                                    isSheetsPerSetSupported);

    std::vector<std::tuple<BookletMakingOptions, std::tuple<std::vector<std::tuple<OrientedMediaSize, std::vector<FinishingContentOrientation>>>, std::vector<MediaId>>>> optionsInbookletMakingMediaProcessingOption = {
        //expectedValidValues
        {BookletMakingOptions::SADDLE_STITCH, {mediaSizeCharacteristics_BOOKLET_MAKER, supportedOptionMediaTypesSupportedData1}}
    };

    std::vector<BookletMakingMediaProcessingOptionPtr> bookletMakingMediaProcessingOptionPtrVec;
    for (const auto optionInBookletMakingMediaProcessingOption : optionsInbookletMakingMediaProcessingOption)
    {
        auto bookletMakingOptionInMediaProcessingOption = std::get<0>(optionInBookletMakingMediaProcessingOption);
        auto mediaSizeListMediaSizeCharacteristics = std::get<0>(std::get<1>(optionInBookletMakingMediaProcessingOption));
        auto supportedOptionMediaTypesSupported = std::get<1>(std::get<1>(optionInBookletMakingMediaProcessingOption));

        std::vector<MediaSizeCharacteristicsOrientationPtr> mediaSizeCharacteristicsOrientationPtrVec;
        for (const auto mediaSizeInMediaSizeCharacteristics : mediaSizeListMediaSizeCharacteristics)
        {
            std::vector<FinishingContentOrientation> finishingContentOrientationVec;
            for (const auto contentOrientation : std::get<1>(mediaSizeInMediaSizeCharacteristics))
            {
                finishingContentOrientationVec.push_back(contentOrientation);
            }

            std::vector<IPPDataPtr> iPPDataPtrVec;
            ProcessingOptionDirection processingOptionDirection = ProcessingOptionDirection::OUTWARD;
            ProcessingOptionReferenceEdge processingOptionReferenceEdge = ProcessingOptionReferenceEdge::NONE;
            ProcessingOptionLocations processingOptionLocations;
            ProcessingOptionOffsets processingOptionOffsets;
            auto iPPDataPtr = std::make_shared<IPPData>(processingOptionDirection, processingOptionReferenceEdge, processingOptionLocations, processingOptionOffsets);
            iPPDataPtrVec.push_back(iPPDataPtr);

            auto orientedMediaSize = std::get<0>(mediaSizeInMediaSizeCharacteristics);
            auto mediaSizeCharacteristicsOrientationPtr = std::make_shared<MediaSizeCharacteristicsOrientation>(orientedMediaSize, finishingContentOrientationVec, iPPDataPtrVec, false, false);
            mediaSizeCharacteristicsOrientationPtrVec.push_back(mediaSizeCharacteristicsOrientationPtr);
        }

        MediaProcessingOptionName mediaProcessingOptionName;
        MediaProcessingOptionName mediaProcessingOptionOverrideNameLetterLedgerMixedMedia;
        std::vector<MediaProcessingBoundary> mediaProcessingBoundariesVec;
        MinAndMax tempMediaWidthLimit, tempMediaHeightLimit;

        auto mediaProcessingOptionPtr = std::make_shared<BookletMakingMediaProcessingOption>(mediaProcessingOptionName,
                                                                                            mediaProcessingOptionOverrideNameLetterLedgerMixedMedia,
                                                                                            supportedOptionMediaTypesSupported,
                                                                                            tempMediaWidthLimit, tempMediaHeightLimit,
                                                                                            mediaProcessingBoundariesVec,
                                                                                            mediaSizeCharacteristicsOrientationPtrVec,
                                                                                            setsLimitForBookletMaking_,
                                                                                            appJobPageOrderForBookletMaking_,
                                                                                            appDuplexPageOrderForBookletMaking_,
                                                                                            formatterJobPageOrderForBookletMaking_,
                                                                                            formatterDuplexPageOrderForBookletMaking_,
                                                                                            formatterRotationPriorityForBookletMaking_,
                                                                                            convertSimplexToDuplexForBookletMaking_,
                                                                                            isImageRotationSupportedBySizeForBookletMaking_,
                                                                                            bookletMakingOptionInMediaProcessingOption);
        bookletMakingMediaProcessingOptionPtrVec.push_back(mediaProcessingOptionPtr);
    }

    bool isSheetsPerSetSupportedBookletMaking = false;
    auto bookletMakingMediaProcessingTypePtr = std::make_shared<BookletMakingMediaProcessingType>(mediaProcessingTypeName,
                                                                                                    mediaProcessingType,
                                                                                                    bookletMakingMediaProcessingOptionPtrVec,
                                                                                                    isSheetsPerSetSupportedBookletMaking);


    staplingAndPunchingMediaProcessingType_ = std::tuple<APIResult, StaplingAndPunchingMediaProcessingTypePtr>(APIResult::OK, staplingAndPunchingMediaProcessingTypePtr);
    foldingMediaProcessingType_ = std::tuple<APIResult, FoldingMediaProcessingTypePtr>(APIResult::OK, foldingMediaProcessingTypePtr);
    bookletMakingMediaProcessingType_ = std::tuple<APIResult, BookletMakingMediaProcessingTypePtr>(APIResult::OK, bookletMakingMediaProcessingTypePtr);

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher *) {} ), // stapling
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock2_, [](IMedia::IPageBasedFinisher *) {} ), // stapling  & Punching
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock3_, [](IMedia::IPageBasedFinisher *) {} ), // punching
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock4_, [](IMedia::IPageBasedFinisher *) {} ), // folding
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock5_, [](IMedia::IPageBasedFinisher *) {} )  // bookletmaking
    };

    ON_CALL(*mockIMedia_, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, pageBasedFinishers)));

    auto iPPDataPtr = std::make_shared<IPPData>(processingOptionDirectionIPPDataTest_, processingOptionReferenceEdgeIPPDataTest_, processingOptionLocationsIPPDataTest_, processingOptionOffsetsIPPDataTest_);
    std::vector<IPPDataPtr> iPPDataCollection;
    iPPDataCollection.push_back(iPPDataPtr);
    ippDataListStaple_ = std::make_tuple(APIResult::OK, iPPDataCollection);
    ippDataListPunch_ = std::make_tuple(APIResult::OK, iPPDataCollection);
    ippDataListStapleAndPunch_ = std::make_tuple(APIResult::OK, iPPDataCollection);
    ippDataListFold_ = std::make_tuple(APIResult::OK, iPPDataCollection);
    ippDataListBookletMaking_ = std::make_tuple(APIResult::OK, iPPDataCollection);
    ippDataListJog_ =  std::make_tuple(APIResult::OK, iPPDataCollection);
    /** Stapling */
    ON_CALL(pageBasedFinisherMock1_, getType())
        .WillByDefault(Return(FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock1_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[0]));
    IMedia::PageBasedFinisherPtr pageBasedFinisherPtr1 = IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher * p){} );
    ON_CALL(pageBasedFinisherMock1_, getPageBasedFinisher())
        .WillByDefault(Return(pageBasedFinisherPtr1));
    ON_CALL(pageBasedFinisherMock1_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeList_)));
    ON_CALL(pageBasedFinisherMock1_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdList_)));
    ON_CALL(pageBasedFinisherMock1_, getStaplingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingType_));
    ON_CALL(pageBasedFinisherMock1_, getPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock1_, getStaplingAndPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock1_, getFoldingMediaProcessingType())
        .WillByDefault(ReturnRef(foldingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock1_, getBookletMakingMediaProcessingType())
        .WillByDefault(ReturnRef(bookletMakingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock1_, getDefaultMediaProcessingType())
        .WillByDefault(ReturnRef(defaultMediaProcessingTypeNotAvailable_));
    ON_CALL(pageBasedFinisherMock1_, getDefaultMediaProcessingOption())
        .WillByDefault(ReturnRef(defaultMediaProcessingOptionNotAvailable_));

    /** Stapling And Punching */
    ON_CALL(pageBasedFinisherMock2_, getType())
        .WillByDefault(Return(FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock2_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[1]));
    IMedia::PageBasedFinisherPtr pageBasedFinisherPtr2 = IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock2_, [](IMedia::IPageBasedFinisher * p){} );
    ON_CALL(pageBasedFinisherMock2_, getPageBasedFinisher())
        .WillByDefault(Return(pageBasedFinisherPtr2));
    ON_CALL(pageBasedFinisherMock2_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeList_)));
    ON_CALL(pageBasedFinisherMock2_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdList_)));
    ON_CALL(pageBasedFinisherMock2_, getStaplingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock2_, getPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock2_, getStaplingAndPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingType_));
    ON_CALL(pageBasedFinisherMock2_, getFoldingMediaProcessingType())
        .WillByDefault(ReturnRef(foldingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock2_, getBookletMakingMediaProcessingType())
        .WillByDefault(ReturnRef(bookletMakingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock2_, getDefaultMediaProcessingType())
        .WillByDefault(ReturnRef(defaultMediaProcessingTypeNotAvailable_));
    ON_CALL(pageBasedFinisherMock2_, getDefaultMediaProcessingOption())
        .WillByDefault(ReturnRef(defaultMediaProcessingOptionNotAvailable_));

    /** Punching */
    ON_CALL(pageBasedFinisherMock3_, getType())
        .WillByDefault(Return(FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock3_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[2]));
    IMedia::PageBasedFinisherPtr pageBasedFinisherPtr3 = IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock3_, [](IMedia::IPageBasedFinisher * p){} );
    ON_CALL(pageBasedFinisherMock3_, getPageBasedFinisher())
        .WillByDefault(Return(pageBasedFinisherPtr3));
    ON_CALL(pageBasedFinisherMock3_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeList_)));
    ON_CALL(pageBasedFinisherMock3_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdList_)));
    ON_CALL(pageBasedFinisherMock3_, getStaplingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock3_, getPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingType_));
    ON_CALL(pageBasedFinisherMock3_, getStaplingAndPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock3_, getFoldingMediaProcessingType())
        .WillByDefault(ReturnRef(foldingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock3_, getBookletMakingMediaProcessingType())
        .WillByDefault(ReturnRef(bookletMakingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock3_, getDefaultMediaProcessingType())
        .WillByDefault(ReturnRef(defaultMediaProcessingTypeNotAvailable_));
    ON_CALL(pageBasedFinisherMock3_, getDefaultMediaProcessingOption())
        .WillByDefault(ReturnRef(defaultMediaProcessingOptionNotAvailable_));

    /** folding*/
    ON_CALL(pageBasedFinisherMock4_, getType())
        .WillByDefault(Return(FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock4_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[3]));
    IMedia::PageBasedFinisherPtr pageBasedFinisherPtr4 = IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock4_, [](IMedia::IPageBasedFinisher * p){} );
    ON_CALL(pageBasedFinisherMock4_, getPageBasedFinisher())
        .WillByDefault(Return(pageBasedFinisherPtr4));
    ON_CALL(pageBasedFinisherMock4_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeListBookletAndFold_)));
    ON_CALL(pageBasedFinisherMock4_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdListBookletAndFold_)));
    ON_CALL(pageBasedFinisherMock4_, getStaplingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock4_, getPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock4_, getStaplingAndPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock4_, getFoldingMediaProcessingType())
        .WillByDefault(ReturnRef(foldingMediaProcessingType_));
    ON_CALL(pageBasedFinisherMock4_, getBookletMakingMediaProcessingType())
        .WillByDefault(ReturnRef(bookletMakingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock4_, getDefaultMediaProcessingType())
        .WillByDefault(ReturnRef(defaultMediaProcessingTypeNotAvailable_));
    ON_CALL(pageBasedFinisherMock4_, getDefaultMediaProcessingOption())
        .WillByDefault(ReturnRef(defaultMediaProcessingOptionNotAvailable_));

    /** bookletMaking */
    ON_CALL(pageBasedFinisherMock5_, getType())
        .WillByDefault(Return(FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock5_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[4]));
    IMedia::PageBasedFinisherPtr pageBasedFinisherPtr5 = IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock5_, [](IMedia::IPageBasedFinisher * p){} );
    ON_CALL(pageBasedFinisherMock5_, getPageBasedFinisher())
        .WillByDefault(Return(pageBasedFinisherPtr5));
    ON_CALL(pageBasedFinisherMock5_, getMediaSupportedSizes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeListBookletAndFold_)));
    ON_CALL(pageBasedFinisherMock5_, getMediaSupportedTypes())
        .WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdList_)));
    ON_CALL(pageBasedFinisherMock5_, getStaplingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock5_, getPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock5_, getStaplingAndPunchingMediaProcessingType())
        .WillByDefault(ReturnRef(staplingAndPunchingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock5_, getFoldingMediaProcessingType())
        .WillByDefault(ReturnRef(foldingMediaProcessingTypeNull_));
    ON_CALL(pageBasedFinisherMock5_, getBookletMakingMediaProcessingType())
        .WillByDefault(ReturnRef(bookletMakingMediaProcessingType_));
    ON_CALL(pageBasedFinisherMock5_, getDefaultMediaProcessingType())
        .WillByDefault(ReturnRef(defaultMediaProcessingType_));
    ON_CALL(pageBasedFinisherMock5_, getDefaultMediaProcessingOption())
        .WillByDefault(ReturnRef(defaultMediaProcessingOption_));
}

void GivenACopyJobTicket::TearDown()
{
    delete mockIPrintIntentsFactory_;
    delete mockIScannerCapabilities_;
    delete mockIMedia_;
    delete intentsManager_;
    delete mockIExportImport_;
    delete mockLocaleProvider_;
    delete mockColorAccessControl_;
}

std::shared_ptr<dune::print::engine::PrintIntents> GivenACopyJobTicket::createDefaultPrintIntent()
{
     //Create default print intent
    //ADD HERE ALL FIELDS YOU ARE GOING TO CHECK
    const std::map<dune::print::engine::PrintIntentFieldType, dune::print::engine::Variant> printIntentFields = {
        {dune::print::engine::PrintIntentFieldType::COLOR_MODE, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::TRAY_TYPE, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::BIN_TYPE, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::PLEX_BINDING, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::PLEX_MODE, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::PLEX_SIDE, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::PRINTING_ORDER, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::PAGE_NUMBER, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::PAGE_ID, dune::print::engine::INVALID_PAGE_UID},
        {dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::JOB_TYPE, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::PAGE_WIDTH, dune::print::engine::Variant(1)},
        {dune::print::engine::PrintIntentFieldType::PAGE_HEIGHT, dune::print::engine::Variant(1)},
        {dune::print::engine::PrintIntentFieldType::STAPLE_OPTION, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::PUNCH_OPTION, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::FOLD_OPTION, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::SHEETS_PER_SET, dune::print::engine::Variant(1)},
        {dune::print::engine::PrintIntentFieldType::BOOKLET_MAKER_OPTION, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::ROTATE_180, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::CONTENT_ORIENTATION, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::INTENDED_FEED_ORIENTATION, dune::print::engine::Variant(0)},
        {dune::print::engine::PrintIntentFieldType::FORCE_FEED_ORIENTATION, dune::print::engine::Variant(0)}
    };

    return std::make_shared<dune::print::engine::PrintIntents>(printIntentFields);
}

dune::imaging::types::MarginLayout GivenACopyJobTicket::convertToMarginLayout(dune::imaging::types::CopyMargins copyMargins)
{
    switch(copyMargins)
    {
        case dune::imaging::types::CopyMargins::OVERSIZE:
            return dune::imaging::types::MarginLayout::OVERSIZE;

        case dune::imaging::types::CopyMargins::CLIPCONTENT:
            return dune::imaging::types::MarginLayout::CLIPINSIDE;

        default:
            return dune::imaging::types::MarginLayout::STANDARD;
    }
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpage_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    ticket_.setPreviewMode(true);
    intent->setPrintingOrder(PrintingOrder::LAST_PAGE_ON_TOP);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::MAINROLL);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::MDF);

    intent->setAutoRotate(true);
    intent->setMediaFamily(dune::imaging::types::MediaFamily::WALLCOVERING);
    intent->setRotation(270);
    intent->setStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::TWO_POINT_ANY);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::V_INWARD_TOP);
    intent->setSheetsPerSetForVFold(3);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);

    EXPECT_EQ(intent->getBookletMakerOption(), dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);

    dune::job::IIntentsManager::IntentsMap intentsMap;
    dune::job::IIntentsManager::PageIntent pageIntent;

    EXPECT_CALL(*intentsManager_,updatePageIntents(_,_)).WillOnce(::testing::DoAll(
                ::testing::SaveArg<0>(&pageIntent),
                ::testing::SaveArg<1>(&intentsMap)
                ));
    std::shared_ptr<dune::imaging::types::PageMetaInfoT>  pageMetaInfo = std::make_shared<dune::imaging::types::PageMetaInfoT>();
    pageMetaInfo->mediaSize = dune::imaging::types::MediaSizeId::LETTER;
    pageMetaInfo->mediaOrientation = dune::imaging::types::MediaOrientation::LANDSCAPE;

    EXPECT_EQ(intent->getMatchOriginalOutputMediaSizeId(), dune::imaging::types::MediaSizeId::ANY);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId, pageMetaInfo);

    EXPECT_EQ(intent->getMatchOriginalOutputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(intent->getScanFeedOrientation(), dune::scan::types::ScanFeedOrientation::LONGEDGE);

    // check call intentsManager updatePageIntents
    EXPECT_EQ(pageIntent.autoRotate, intent->getAutoRotate());
    EXPECT_EQ(pageIntent.mediaFamily, intent->getMediaFamily());
    EXPECT_EQ(pageIntent.rotationCW, dune::imaging::ImagingUtilities::convertAnglesToRotationCW(intent->getRotation()));

    EXPECT_EQ(intentsMap.getIntents(dune::job::IntentType::PRINT).get(), pageTicket->getIntent(dune::job::IntentType::PRINT).get());
    EXPECT_EQ(intentsMap.getIntents(dune::job::IntentType::IMAGING).get(), pageTicket->getIntent(dune::job::IntentType::IMAGING).get());

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_EQ(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(MediaSizeId::CUSTOM, mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    PrintingOrder printingOrder;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINTING_ORDER, printingOrder);
    EXPECT_EQ(intent->getPrintingOrder(), printingOrder);

    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    EXPECT_EQ(ticket_.getPageCount()-1, pageCount);

    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    Uuid id;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_ID , id);
    EXPECT_EQ(pageId, id);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_EQ(dune::job::JobType::COPY, jobType);

    dune::imaging::types::StapleOptions stapleOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::STAPLE_OPTION, stapleOption);
    EXPECT_EQ(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY, stapleOption);

    dune::imaging::types::PunchingOptions punchOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PUNCH_OPTION, punchOption);
    EXPECT_EQ(dune::imaging::types::PunchingOptions::TWO_POINT_ANY, punchOption);

    dune::imaging::types::FoldingOptions foldOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::FOLD_OPTION, foldOption);
    EXPECT_EQ(dune::imaging::types::FoldingOptions::V_INWARD_TOP, foldOption);

    uint32_t sheetsPerSet;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::SHEETS_PER_SET, sheetsPerSet);
    EXPECT_EQ(3, sheetsPerSet);

    dune::imaging::types::BookletMakingOptions bookletOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BOOKLET_MAKER_OPTION, bookletOption);
    EXPECT_EQ(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH, bookletOption);

    dune::imaging::types::ContentOrientation contentOrientation;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::CONTENT_ORIENTATION, contentOrientation);
    EXPECT_EQ(dune::imaging::types::ContentOrientation::PORTRAIT, contentOrientation);

    dune::imaging::types::ForceFeedOrientationType forceFeedOrientation;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::FORCE_FEED_ORIENTATION, forceFeedOrientation);
    EXPECT_EQ(dune::imaging::types::ForceFeedOrientationType::OKTOOVERRIDE, forceFeedOrientation);

}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInEnterprise_ThenPrintIntentHasTheCorrectValues)
{
    // Add page with Letter as any output media size
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::ENTERPRISE);

    //Set intent settings values
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setMatchOriginalOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E300DPI);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);


    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(MediaSizeId::LETTER, mediaSize);

    // Add page with ANY as any output media size
    pageId = Uuid::createUuid();
    //Get intent
    intent = ticket_.getIntent();

    //Set intent settings values
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setMatchOriginalOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setOutputXResolution(Resolution::E300DPI);

    //Add new page
    pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(MediaSizeId::CUSTOM, mediaSize);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpage_ThenMixedMediaPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    ticket_.setPreviewMode(true);
    intent->setPrintingOrder(PrintingOrder::LAST_PAGE_ON_TOP);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::MAINROLL);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER);

    intent->setAutoRotate(true);
    intent->setMediaFamily(dune::imaging::types::MediaFamily::WALLCOVERING);
    intent->setRotation(270);
    intent->setStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::TWO_POINT_ANY);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::V_INWARD_TOP);
    intent->setSheetsPerSetForVFold(3);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);

    EXPECT_EQ(intent->getBookletMakerOption(), dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);

    dune::job::IIntentsManager::IntentsMap intentsMap;
    dune::job::IIntentsManager::PageIntent pageIntent;

    EXPECT_CALL(*intentsManager_,updatePageIntents(_,_)).WillOnce(::testing::DoAll(
                ::testing::SaveArg<0>(&pageIntent),
                ::testing::SaveArg<1>(&intentsMap)
                ));

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    // check call intentsManager updatePageIntents
    EXPECT_EQ(pageIntent.autoRotate, intent->getAutoRotate());
    EXPECT_EQ(pageIntent.mediaFamily, intent->getMediaFamily());
    EXPECT_EQ(pageIntent.rotationCW, dune::imaging::ImagingUtilities::convertAnglesToRotationCW(intent->getRotation()));

    EXPECT_EQ(intentsMap.getIntents(dune::job::IntentType::PRINT).get(), pageTicket->getIntent(dune::job::IntentType::PRINT).get());
    EXPECT_EQ(intentsMap.getIntents(dune::job::IntentType::IMAGING).get(), pageTicket->getIntent(dune::job::IntentType::IMAGING).get());

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    dune::imaging::types::ForceFeedOrientationType forceFeedOrientation;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::FORCE_FEED_ORIENTATION, forceFeedOrientation);
    EXPECT_EQ(dune::imaging::types::ForceFeedOrientationType::NOTOKTOOVERRIDE, forceFeedOrientation);

}

TEST_F(GivenACopyJobTicket, WhenCloningAJobTicketForReprint_ValuesShouldBeIdenticalResultsReset)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    // marking the job as completed and reprintable means this cloning is for a reprint
    ticket_.setState(dune::job::JobStateType::COMPLETED);
    ticket_.setJobReprintable(true);

    //Set intent settings values
    ticket_.setPreviewMode(true);
    intent->setPrintingOrder(PrintingOrder::LAST_PAGE_ON_TOP);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::MAINROLL);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::MDF);

    intent->setAutoRotate(true);
    intent->setMediaFamily(dune::imaging::types::MediaFamily::WALLCOVERING);
    intent->setRotation(270);

    dune::job::IIntentsManager::IntentsMap intentsMap;
    dune::job::IIntentsManager::PageIntent pageIntent;

    EXPECT_CALL(*intentsManager_,updatePageIntents(_,_)).WillOnce(::testing::DoAll(
                ::testing::SaveArg<0>(&pageIntent),
                ::testing::SaveArg<1>(&intentsMap)
                ));

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket1 = ticket_.addPage(pageId);

    // check call intentsManager updatePageIntents
    EXPECT_EQ(pageIntent.autoRotate, intent->getAutoRotate());
    EXPECT_EQ(pageIntent.mediaFamily, intent->getMediaFamily());
    EXPECT_EQ(pageIntent.rotationCW, dune::imaging::ImagingUtilities::convertAnglesToRotationCW(intent->getRotation()));

    EXPECT_EQ(intentsMap.getIntents(dune::job::IntentType::PRINT).get(), pageTicket1->getIntent(dune::job::IntentType::PRINT).get());
    EXPECT_EQ(intentsMap.getIntents(dune::job::IntentType::IMAGING).get(), pageTicket1->getIntent(dune::job::IntentType::IMAGING).get());

    ticket_.setJobReprintable(true);
    CopyJobTicket copiedTicket{ticket_};
    std::vector<Uuid> pageIds = copiedTicket.getPagesIds(PageOrder::CREATION);
    ASSERT_EQ(pageIds.size(), 1);
    std::shared_ptr<dune::job::IPageTicket> pageTicket = copiedTicket.getPage(pageIds[0]);
    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_EQ(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(MediaSizeId::CUSTOM, mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    PrintingOrder printingOrder;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINTING_ORDER, printingOrder);
    EXPECT_EQ(intent->getPrintingOrder(), printingOrder);

    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    EXPECT_EQ(ticket_.getPageCount()-1, pageCount);

    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_EQ(dune::job::JobType::COPY, jobType);

    // results must be reset after cloning to reprint
    EXPECT_EQ(0,                                             copiedTicket.getResult()->getCompletedCopies());
    EXPECT_EQ(0,                                             copiedTicket.getResult()->getCompletedImpressions());
    EXPECT_EQ(0,                                             copiedTicket.getResult()->getCurrentCuringTemperature());
    EXPECT_EQ(0,                                             copiedTicket.getResult()->getCurrentPage());
    EXPECT_EQ(0,                                             copiedTicket.getResult()->getProgress());
    EXPECT_EQ(0,                                             copiedTicket.getResult()->getRemainingPrintingTime());
    EXPECT_EQ(false,                                         copiedTicket.getResult()->areAllPagesDiscovered());
}

TEST_F(GivenACopyJobTicket, WhenCloningAFailJobTicketForReprint_ValuesShouldNotBeIdentical)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    ticket_.setPreviewMode(true);
    intent->setPrintingOrder(PrintingOrder::LAST_PAGE_ON_TOP);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::MAINROLL);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::MDF);

    intent->setAutoRotate(true);
    intent->setMediaFamily(dune::imaging::types::MediaFamily::WALLCOVERING);
    intent->setRotation(270);

    dune::job::IIntentsManager::IntentsMap intentsMap;
    dune::job::IIntentsManager::PageIntent pageIntent;

    EXPECT_CALL(*intentsManager_,updatePageIntents(_,_)).WillOnce(::testing::DoAll(
                ::testing::SaveArg<0>(&pageIntent),
                ::testing::SaveArg<1>(&intentsMap)
                ));

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket1 = ticket_.addPage(pageId);

    // check call intentsManager updatePageIntents
    EXPECT_EQ(pageIntent.autoRotate, intent->getAutoRotate());
    EXPECT_EQ(pageIntent.mediaFamily, intent->getMediaFamily());
    EXPECT_EQ(pageIntent.rotationCW, dune::imaging::ImagingUtilities::convertAnglesToRotationCW(intent->getRotation()));

    EXPECT_EQ(intentsMap.getIntents(dune::job::IntentType::PRINT).get(), pageTicket1->getIntent(dune::job::IntentType::PRINT).get());
    EXPECT_EQ(intentsMap.getIntents(dune::job::IntentType::IMAGING).get(), pageTicket1->getIntent(dune::job::IntentType::IMAGING).get());

    ticket_.setJobReprintable(true);
    CopyJobTicket copiedTicket{ticket_};
    std::vector<Uuid> pageIds = copiedTicket.getPagesIds(PageOrder::CREATION);
    ASSERT_EQ(pageIds.size(), 0);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfOrGlass_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_EQ(dune::imaging::types::MarginLayout::STANDARD, marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    uint32_t jobPageCount;
    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenPagesSerializedAndDeserialized_PagesAreValid)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicketInit = ticket_.addPage(pageId);

    auto SerializedPages = ticket_.serialize();

    auto pageTicket = ticket_.getCopyPageTicket(pageId);

    //Once page has been serialized and deserialized, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_EQ(dune::imaging::types::MarginLayout::STANDARD, marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInGlassWithStapleFinisher_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN2);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E600DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANGLED);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    dune::imaging::types::StapleOptions stapleOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::STAPLE_OPTION, stapleOption);
    EXPECT_EQ(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANGLED, stapleOption);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfWithStapleFinisher_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    dune::imaging::types::StapleOptions stapleOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::STAPLE_OPTION, stapleOption);
    EXPECT_EQ(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANY, stapleOption);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfWithPunchFinisher_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::TWO_POINT_ANY);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    dune::imaging::types::PunchingOptions punchOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PUNCH_OPTION, punchOption);
    EXPECT_EQ(dune::imaging::types::PunchingOptions::TWO_POINT_ANY, punchOption);

    uint32_t jobPageCount;
    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInGlassWithPunchFinisher_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN2);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputXResolution(Resolution::E600DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::MIXED);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::RIGHT_THREE_POINT_US);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    dune::imaging::types::PunchingOptions punchOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PUNCH_OPTION, punchOption);
    EXPECT_EQ(dune::imaging::types::PunchingOptions::RIGHT_THREE_POINT_US, punchOption);

    uint32_t jobPageCount;
    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInGlassWithStaplePunchFinisher_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::GRAYSCALE);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN2);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputXResolution(Resolution::E600DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::MIXED);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::SIMPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANGLED);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::RIGHT_THREE_POINT_US);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    dune::imaging::types::StapleOptions stapleOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::STAPLE_OPTION, stapleOption);
    EXPECT_EQ(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANGLED, stapleOption);

    dune::imaging::types::PunchingOptions punchOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PUNCH_OPTION, punchOption);
    EXPECT_EQ(dune::imaging::types::PunchingOptions::RIGHT_THREE_POINT_US, punchOption);

    uint32_t jobPageCount;
    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}


TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfWithStaplePunchFinisher_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::GRAYSCALE);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN2);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E600DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::MIXED);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::SIMPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    intent->setStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANGLED);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::RIGHT_THREE_POINT_US);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    dune::imaging::types::StapleOptions stapleOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::STAPLE_OPTION, stapleOption);
    EXPECT_EQ(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANGLED, stapleOption);

    dune::imaging::types::PunchingOptions punchOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PUNCH_OPTION, punchOption);
    EXPECT_EQ(dune::imaging::types::PunchingOptions::RIGHT_THREE_POINT_US, punchOption);

    uint32_t jobPageCount;
    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfWithFoldFinisher_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::GRAYSCALE);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN2);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E600DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::MIXED);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::SIMPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::V_INWARD_TOP);
    intent->setSheetsPerSetForVFold(2);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    dune::imaging::types::FoldingOptions foldOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::FOLD_OPTION, foldOption);
    EXPECT_EQ(dune::imaging::types::FoldingOptions::V_INWARD_TOP, foldOption);

    uint32_t sheetsPerSet;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::SHEETS_PER_SET, sheetsPerSet);
    EXPECT_EQ(2, sheetsPerSet);

    uint32_t jobPageCount;
    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfWithBookletFinisher_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::GRAYSCALE);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN2);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E600DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::MIXED);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::SIMPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);
    intent->setSheetsPerSetForFoldAndStitch(10);

    EXPECT_EQ(intent->getBookletMakerOption(), dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);
    EXPECT_EQ(intent->getSheetsPerSetForFoldAndStitch(), 10);      

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    dune::imaging::types::BookletMakingOptions bookletMakerOption;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BOOKLET_MAKER_OPTION, bookletMakerOption);
    EXPECT_EQ(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH, bookletMakerOption);

    uint32_t sheetsPerSet;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::SHEETS_PER_SET, sheetsPerSet);
    EXPECT_EQ(10, sheetsPerSet);

    uint32_t jobPageCount;
    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageWithoutPageSizeInformation_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<MockICopyJobIntent> intent = std::make_shared<MockICopyJobIntent>();

    //Set intent settings values
    ON_CALL(*intent, getInputMediaSizeId())
        .WillByDefault(Return(dune::imaging::types::MediaSizeId::LETTER));
    ON_CALL(*intent, getOutputMediaSizeId())
        .WillByDefault(Return(dune::imaging::types::MediaSizeId::LETTER));
    ON_CALL(*intent, getScanFeedOrientation())
        .WillByDefault(Return(dune::scan::types::ScanFeedOrientation::LONGEDGE));
    ON_CALL(*intent, getOutputXResolution())
        .WillByDefault(Return(Resolution::E300DPI));
    ON_CALL(*intent, getOriginalContentType())
        .WillByDefault(Return(dune::imaging::types::OriginalContentType::PHOTO));
    ON_CALL(*intent, getOutputDestination())
            .WillByDefault(Return(dune::imaging::types::MediaDestinationId::BIN));

    ticket_.setIntent(std::static_pointer_cast<ICopyJobIntent>(intent));

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_EQ(dune::imaging::types::MarginLayout::STANDARD, marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    // Check page width and height
    auto widthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(
        mediaSize, dune::imaging::types::MediaOrientation::PORTRAIT);
    uint32_t resolution = dune::scan::types::ConvertToScanTypeHelper::getResolutionIntFromEnum(intent->getOutputXResolution());

    int32_t pageHeight;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_HEIGHT, pageHeight);
    EXPECT_EQ(widthAndHeight.height.get(resolution), pageHeight);

    int32_t pageWidth;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_WIDTH, pageWidth);
    EXPECT_EQ(widthAndHeight.width.get(resolution), pageWidth);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    dune::imaging::types::MediaOrientation mediaOrientation;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::INTENDED_FEED_ORIENTATION, mediaOrientation);
    EXPECT_EQ(dune::imaging::types::MediaOrientation::LANDSCAPE, mediaOrientation);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    uint32_t jobPageCount;
    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageWithLetterAndPortraitOrientation_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<MockICopyJobIntent> intent = std::make_shared<MockICopyJobIntent>();

    //Set intent settings values
    ON_CALL(*intent, getInputMediaSizeId())
        .WillByDefault(Return(dune::imaging::types::MediaSizeId::LETTER));
    ON_CALL(*intent, getOutputMediaSizeId())
        .WillByDefault(Return(dune::imaging::types::MediaSizeId::LETTER));
    ON_CALL(*intent, getScanFeedOrientation())
        .WillByDefault(Return(dune::scan::types::ScanFeedOrientation::SHORTEDGE));
    ON_CALL(*intent, getOutputXResolution())
        .WillByDefault(Return(Resolution::E300DPI));
    ON_CALL(*intent, getOutputMediaOrientation())
        .WillByDefault(Return(dune::imaging::types::MediaOrientation::LANDSCAPE));

    ticket_.setIntent(std::static_pointer_cast<ICopyJobIntent>(intent));

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    // Check page width and height
    auto widthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(
        mediaSize, dune::imaging::types::MediaOrientation::LANDSCAPE);
    uint32_t resolution = dune::scan::types::ConvertToScanTypeHelper::getResolutionIntFromEnum(intent->getOutputXResolution());

    int32_t pageHeight;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_HEIGHT, pageHeight);
    EXPECT_EQ(widthAndHeight.height.get(resolution), pageHeight);

    int32_t pageWidth;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_WIDTH, pageWidth);
    EXPECT_EQ(widthAndHeight.width.get(resolution), pageWidth);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageWithCustomPageSizeAndEnterprise_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<MockICopyJobIntent> intent = std::make_shared<MockICopyJobIntent>();

    //Set intent settings values
    ON_CALL(*intent, getOutputMediaSizeId())
        .WillByDefault(Return(dune::imaging::types::MediaSizeId::CUSTOM));
    ON_CALL(*intent, getOutputXResolution())
        .WillByDefault(Return(Resolution::E300DPI));
    double customMediaXDimension{85000.0};
    double customMediaYDimension{110000.0};
    EXPECT_CALL(*intent, getCustomMediaXDimension()).WillOnce(Return(customMediaXDimension));
    EXPECT_CALL(*intent, getCustomMediaYDimension()).WillOnce(Return(customMediaYDimension));

    ticket_.setIntent(std::static_pointer_cast<ICopyJobIntent>(intent));
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::ENTERPRISE);

    // addPage() - createIntetnts() - updateIntents()
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    // Check page width and height
    auto widthAndHeight = dune::imaging::types::convertCustomMediaSizeIdToWidthAndHeight(customMediaXDimension, customMediaYDimension);
    uint32_t resolution = dune::scan::types::ConvertToScanTypeHelper::getResolutionIntFromEnum(intent->getOutputXResolution());

    int32_t pageHeight;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_HEIGHT, pageHeight);
    EXPECT_EQ(widthAndHeight.height.get(resolution), pageHeight);

    int32_t pageWidth;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_WIDTH, pageWidth);
    EXPECT_EQ(widthAndHeight.width.get(resolution), pageWidth);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageWithIDCardAndEnterprise_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);

    ticket_.setIntent(std::static_pointer_cast<ICopyJobIntent>(intent));
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::ENTERPRISE);

    // addPage() - createIntetnts() - updateIntents()
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    // Check page width and height, OutPage should be portrait in case of IDCard job.
    auto widthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(intent->getOutputMediaSizeId(), dune::imaging::types::MediaOrientation::PORTRAIT);
    uint32_t resolution = dune::scan::types::ConvertToScanTypeHelper::getResolutionIntFromEnum(intent->getOutputXResolution());

    int32_t pageHeight;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_HEIGHT, pageHeight);
    EXPECT_EQ(widthAndHeight.height.get(resolution), pageHeight);

    int32_t pageWidth;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_WIDTH, pageWidth);
    EXPECT_EQ(widthAndHeight.width.get(resolution), pageWidth);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageFor2Up_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check Alignment is set correctly
    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    uint32_t pageCount;
    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(((pageCount+1)+1)/2), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageFor2UpPortraitDuplexInEnterprise_ThenPrintIntentHasTheCorrectValues)
{
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::ENTERPRISE);
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    intent->setContentOrientation(ContentOrientation::PORTRAIT);
    intent->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    ContentOrientation contentOrientation;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::CONTENT_ORIENTATION , contentOrientation);
    EXPECT_EQ(ContentOrientation::LANDSCAPE, contentOrientation);

    dune::imaging::types::PlexBinding plexBinding;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING , plexBinding);
    EXPECT_EQ(dune::imaging::types::PlexBinding::SHORT_EDGE, plexBinding);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageFor2UpLandScapeDuplexInEnterprise_ThenPrintIntentHasTheCorrectValues)
{
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::ENTERPRISE);
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    intent->setContentOrientation(ContentOrientation::LANDSCAPE);
    intent->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    ContentOrientation contentOrientation;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::CONTENT_ORIENTATION , contentOrientation);
    EXPECT_EQ(ContentOrientation::PORTRAIT, contentOrientation);

    dune::imaging::types::PlexBinding plexBinding;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING , plexBinding);
    EXPECT_EQ(dune::imaging::types::PlexBinding::LONG_EDGE, plexBinding);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageFor2UpDuplexSecondPage_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrintAlignmentChangeRequired(true);
    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    intent->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    intent->setPlexSide(dune::imaging::types::PlexSide::SECOND);
    intent->setCollate(dune::copy::SheetCollate::Uncollate);
    intent->setOutputPlexBinding(dune::imaging::types::PlexBinding::LONG_EDGE);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check Alignment is set correctly
    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    uint32_t pageCount;
    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(((pageCount+1)+1)/2), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageFor2UpDuplexSecondPageShortEdge_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrintAlignmentChangeRequired(true);
    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    intent->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    intent->setPlexSide(dune::imaging::types::PlexSide::SECOND);
    intent->setCollate(dune::copy::SheetCollate::Uncollate);
    intent->setOutputPlexBinding(dune::imaging::types::PlexBinding::SHORT_EDGE);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check Alignment is set correctly
    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    uint32_t pageCount;
    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(((pageCount+1)+1)/2), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageForDuplexCollateSecondPageShortEdge_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrintAlignmentChangeRequired(true);
    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);

    intent->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    intent->setPlexSide(dune::imaging::types::PlexSide::SECOND);
    intent->setCollate(dune::copy::SheetCollate::Collate);
    intent->setOutputPlexBinding(dune::imaging::types::PlexBinding::SHORT_EDGE);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check Alignment is set correctly
    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::TOP, verticalAlignment);

    uint32_t pageCount;
    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(((pageCount+1)+1)/2), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageForDuplexSecondPage_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrintAlignmentChangeRequired(true);
    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);

    intent->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    intent->setPlexSide(dune::imaging::types::PlexSide::SECOND);
    intent->setOutputPlexBinding(dune::imaging::types::PlexBinding::LONG_EDGE);
    intent->setCollate(dune::copy::SheetCollate::Collate);
    intent->setScaleSelection(dune::scan::types::ScanScaleSelectionEnum::CUSTOM);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check Alignment is set correctly
    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::TOP, verticalAlignment);

    uint32_t pageCount;
    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(((pageCount+1)+1)/2), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfOrGlass_ThenPrintIntentHasTheCorrectValuesForDifferentMediaSize)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    intent->setColorMode(ColorMode::COLOR);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::ROLL1);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LEGAL);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::TOP, verticalAlignment);

    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    EXPECT_EQ(ticket_.getPageCount()-1, pageCount);

    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfOrGlassWithCustomScaleValue_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    intent->setColorMode(ColorMode::COLOR);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::ROLL1);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setScaleSelection(dune::scan::types::ScanScaleSelectionEnum::CUSTOM);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::TOP, verticalAlignment);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfOrGlassWithFullPageScaleValue_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    intent->setColorMode(ColorMode::COLOR);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::ROLL1);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setScaleSelection(dune::scan::types::ScanScaleSelectionEnum::FULLPAGE);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::TOP, verticalAlignment);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}


TEST_F(GivenACopyJobTicket, WhenAddingANewpageInAdfOrGlass_ThenPrintIntentHasTheCorrectValuesForScaleToFitEnabled)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::ROLL1);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LEGAL);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setScaleToFitEnabled(true);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    uint32_t jobPageCount;
    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}
TEST_F(GivenACopyJobTicket, WhenAddingDuplexPrintPageInAdfOrGlass_ThenPrintIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::ROLL1);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));
    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);


    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::CENTER, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::CENTER, verticalAlignment);

    PlexSide plexSide;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_SIDE, plexSide);
    EXPECT_EQ(PlexSide::FIRST, plexSide);

    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    EXPECT_EQ(ticket_.getPageCount()-1, pageCount);

    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    // Add a second page
    pageId = Uuid::createUuid();
    std::shared_ptr<dune::job::IPageTicket> pageTicket2 = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent2 = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket2->getIntent(dune::job::IntentType::PRINT));
    printIntent2->getValue(dune::print::engine::PrintIntentFieldType::PLEX_SIDE, plexSide);
    EXPECT_EQ(PlexSide::SECOND, plexSide);

    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    EXPECT_EQ(ticket_.getPageCount()-1, pageCount);

    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingDuplexPrintPageInAdfOrGlass_ThenPrintIntentHasTheCorrectValuesForDifferentMediaSize)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrintAlignmentChangeRequired(true);

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::ROLL1);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    intent->setCollate(dune::copy::SheetCollate::Uncollate);
    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));
    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);


    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::TOP, verticalAlignment);

    PlexSide plexSide;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_SIDE, plexSide);
    EXPECT_EQ(PlexSide::FIRST, plexSide);

    PrintingOrder printingOrder;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINTING_ORDER, printingOrder);
    EXPECT_EQ(intent->getPrintingOrder(), printingOrder);

    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    EXPECT_EQ(ticket_.getPageCount()-1, pageCount);

    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    // Add a second page
    pageId = Uuid::createUuid();
    std::shared_ptr<dune::job::IPageTicket> pageTicket2 = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent2 = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket2->getIntent(dune::job::IntentType::PRINT));
    printIntent2->getValue(dune::print::engine::PrintIntentFieldType::PLEX_SIDE, plexSide);
    EXPECT_EQ(PlexSide::SECOND, plexSide);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment1;
    printIntent2->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment1);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::KEEP_RIGHT, horizontalAlignment1);

    dune::imaging::types::VerticalContentAlignment verticalAlignment1;
    printIntent2->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment1);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::BOTTOM, verticalAlignment1);

    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    EXPECT_EQ(ticket_.getPageCount()-1, pageCount);

    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    dune::job::JobType jobType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE , jobType);
    EXPECT_NE(dune::job::JobType::COPY, jobType);
}

TEST_F(GivenACopyJobTicket, WhenAddingDuplexPrintPageInAdfOrGlassForHomePro_ThenPrintIntentHasTheCorrectValuesForDifferentMediaSize)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrintAlignmentChangeRequired(false);

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);
    intent->setCopyMargins(dune::imaging::types::CopyMargins::CLIPCONTENT);
    intent->setOutputMediaSource(dune::imaging::types::MediaSource::ROLL1);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputXResolution(Resolution::E300DPI);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setOutputPlexBinding(PlexBinding::LONG_EDGE);
    intent->setOutputPlexMode(Plex::DUPLEX);
    intent->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));
    //Check color mode
    ColorMode colorMode;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, colorMode);
    EXPECT_EQ(intent->getColorMode(), colorMode);

    //Check quality
    PrintQuality quality;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, quality);
    EXPECT_EQ(intent->getCopyQuality(), quality);

    //Check Copy Margins
    MarginLayout marginLayout;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, marginLayout);
    EXPECT_NE(convertToMarginLayout(intent->getCopyMargins()), marginLayout);

    //Check output media source
    MediaSource outputMediaSource;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, outputMediaSource);
    EXPECT_EQ( intent->getOutputMediaSource(), outputMediaSource );

    MediaDestinationId mediaDestination;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE,mediaDestination);
    EXPECT_EQ(intent->getOutputDestination(), mediaDestination);

    MediaSizeId mediaSize;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSize);
    EXPECT_EQ(intent->getOutputMediaSizeId(), mediaSize);

    Plex plexType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, plexType);
    EXPECT_EQ(intent->getOutputPlexMode(), plexType);

    OriginalContentType originalContentType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, originalContentType);
    EXPECT_EQ(intent->getOriginalContentType(), originalContentType);

    PlexBinding plexBindingType;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, plexBindingType);
    EXPECT_EQ(intent->getOutputPlexBinding(), plexBindingType);


    dune::imaging::types::HorizontalContentAlignment horizontalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT, horizontalAlignment);

    dune::imaging::types::VerticalContentAlignment verticalAlignment;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::TOP, verticalAlignment);

    PlexSide plexSide;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PLEX_SIDE, plexSide);
    EXPECT_EQ(PlexSide::FIRST, plexSide);

    PrintingOrder printingOrder;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PRINTING_ORDER, printingOrder);
    EXPECT_EQ(intent->getPrintingOrder(), printingOrder);

    uint32_t pageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    EXPECT_EQ(ticket_.getPageCount()-1, pageCount);

    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);

    // Add a second page
    pageId = Uuid::createUuid();
    std::shared_ptr<dune::job::IPageTicket> pageTicket2 = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent2 = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket2->getIntent(dune::job::IntentType::PRINT));
    printIntent2->getValue(dune::print::engine::PrintIntentFieldType::PLEX_SIDE, plexSide);
    EXPECT_EQ(PlexSide::SECOND, plexSide);

    dune::imaging::types::HorizontalContentAlignment horizontalAlignment1;
    printIntent2->getValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, horizontalAlignment1);
    EXPECT_EQ(dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT, horizontalAlignment1);

    dune::imaging::types::VerticalContentAlignment verticalAlignment1;
    printIntent2->getValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, verticalAlignment1);
    EXPECT_EQ(dune::imaging::types::VerticalContentAlignment::TOP, verticalAlignment1);

    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    EXPECT_EQ(ticket_.getPageCount()-1, pageCount);

    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(intent->getCopies()*(pageCount+1), jobPageCount);
}

TEST_F(GivenACopyJobTicket, WhenTotalPageExceedTheCollateMaxPageCount_ThenJobPageCountIsReseted)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrintAlignmentChangeRequired(false);
    ticket_.setMaxCollatePages(1);
    ticket_.getIntent()->setCollate(dune::copy::SheetCollate::Collate);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    uint32_t jobPageCount;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(1, jobPageCount);

    // Add a second page
    pageId = Uuid::createUuid();
    std::shared_ptr<dune::job::IPageTicket> pageTicket2 = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent2 = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket2->getIntent(dune::job::IntentType::PRINT));

    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_EQ(1, jobPageCount);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndPreScanJobWithError_ThenScanIntentHasTheCorrectValues)
{
    ticket_.setPreScanJob(true);
    ticket_.setPrescannedWidth(0);
    ticket_.setPrescannedHeight(0);
    ticket_.setDefaultMediaSize(dune::imaging::types::MediaSizeId::ANY);
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(false,                                                scanIntent->getAutoCrop());
    EXPECT_EQ(dune::imaging::types::MediaSizeId::ANY,               intent->getInputMediaSizeId());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewPageAndProductNotHomepro_ThenIntentsAreNotTouched)
{
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::LFP);
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(false, scanIntent->getInterleaved());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndPreScanJobNoError_ThenScanIntentHasTheCorrectValues)
{
    ticket_.setPreScanJob(true);
    ticket_.setPrescannedWidth(50);
    ticket_.setPrescannedHeight(50);
    ticket_.setDefaultMediaSize(dune::imaging::types::MediaSizeId::ANY);
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(false,                                                scanIntent->getAutoCrop());
    EXPECT_EQ(dune::imaging::types::MediaSizeId::LEGAL,             intent->getInputMediaSizeId());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndIntentSourceMDF_ThenScanIntentHasTheCorrectValues)
{
    ticket_.setPreScanJob(false);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::MDF);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(true,                                             scanIntent->getInterleaved());
    EXPECT_EQ(dune::scan::types::ScanSourceEnum::MDF,           scanIntent->getScanSource());
}
TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndIntentSourceADFDuplex_ThenScanIntentHasTheCorrectValues)
{
    ticket_.setPreScanJob(false);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    intent->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(true,                                         scanIntent->getInterleaved());
    EXPECT_EQ(dune::scan::types::ScanSourceEnum::ADF,       scanIntent->getScanSource());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewPageAndHomeProAndScanSourceMdf_ThenScanDeviceIntentOffsetsAreSetCorrectly)
{
    ticket_.setPreScanJob(true);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::HOME_PRO);
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::MDF);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get scan intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(0, scanIntent->getXScanOriginSide());
    EXPECT_EQ(0, scanIntent->getYScanOriginSide());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndHomeProAndOutputMediaIdIsAny_ThenAssertIsRaised)
{
    ticket_.setPreScanJob(false);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::HOME_PRO);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);

    EXPECT_DEATH(ticket_.addPage(pageId), "");
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndScaleToFitEnabledAndGlassScansource_ThenScanIntentHasTheCorrectValues)
{
    ticket_.setPreScanJob(false);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::HOME_PRO);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setScaleToFitEnabled(true);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(true,     scanIntent->getAutoCrop());
    EXPECT_EQ(2362,     scanIntent->getOutXExtent());
    EXPECT_EQ(2362,     scanIntent->getOutXExtent());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndHomeProAndCopyQualityBest_ThenResolution600dpi)
{
    ticket_.setPreScanJob(false);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::HOME_PRO);
    ticket_.setSegmentType(dune::job::SegmentType::FinalSegment);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setCopyQuality(dune::imaging::types::PrintQuality::BEST);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(dune::scan::types::ImageQualityEnum::DPI600,     scanIntent->getOutputXImageQuality());
    EXPECT_EQ(dune::scan::types::ImageQualityEnum::DPI600,     scanIntent->getOutputYImageQuality());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndHomeProAndPrepareSegment_ThenResolution100dpi)
{
    ticket_.setPreScanJob(false);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::HOME_PRO);
    ticket_.setSegmentType(dune::job::SegmentType::PrepareSegment);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(dune::scan::types::ImageQualityEnum::DPI100,     scanIntent->getOutputXImageQuality());
    EXPECT_EQ(dune::scan::types::ImageQualityEnum::DPI100,     scanIntent->getOutputYImageQuality());
}

TEST_F(GivenACopyJobTicket, WhenAddingNewPagesInGlassPrepareSegment_ThenPrintIntentJobPageCountHasTheCorrectValue)
{
    ticket_.setSegmentType(dune::job::SegmentType::PrepareSegment);

    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Set intent settings values
    intent->setColorMode(ColorMode::COLOR);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::BIN);
    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOriginalContentType(dune::imaging::types::OriginalContentType::PHOTO);
    intent->setScanSource(dune::scan::types::ScanSource::GLASS);

    uint32_t jobPageCount;
    uint32_t pageCount;

    //Add new page (First preview page)
    Uuid pageId{Uuid::createUuid()};
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_NE(jobPageCount, pageCount + 1);

    // Add a second page (Refresh preview page)
    pageId = Uuid::createUuid();
    std::shared_ptr<dune::job::IPageTicket> pageTicket2 = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_NE(jobPageCount, pageCount + 1);

    // Add a third page (Refresh preview page)
    pageId = Uuid::createUuid();
    std::shared_ptr<dune::job::IPageTicket> pageTicket3 = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_NE(jobPageCount, pageCount + 1);

    //Final copy page (Non-preview page)
    ticket_.setSegmentType(dune::job::SegmentType::FinalSegment);
    pageId = Uuid::createUuid();
    std::shared_ptr<dune::job::IPageTicket> pageTicket4 = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount);
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT , jobPageCount);
    EXPECT_NE(jobPageCount, pageCount + 1);
    EXPECT_EQ(jobPageCount, 1);
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndNotHomePro_ThenResolutionSameAsCopyIntent)
{
    ticket_.setPreScanJob(false);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::LFP);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setOutputXResolution(dune::imaging::types::Resolution::E600DPI);
    intent->setOutputYResolution(dune::imaging::types::Resolution::E600DPI);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(dune::scan::types::ImageQualityEnum::DPI600,     scanIntent->getOutputXImageQuality());
    EXPECT_EQ(dune::scan::types::ImageQualityEnum::DPI600,     scanIntent->getOutputYImageQuality());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndEdgeToEdgeEnabled_ThenScanRegionHasTheCorrectValues)
{
    ticket_.setPreScanJob(false);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::LFP);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setEdgeToEdgeScan(true);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(0,     scanIntent->getXScanSizeSide());
    EXPECT_EQ(0,     scanIntent->getXMediaSize());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndEdgeToEdgeNotEnabledWithHighMaxLength_ThenScanRegionHasTheCorrectValues)
{
    dune::copy::Jobs::Copy::MaxLengthConfig maxLengthConfig;
    maxLengthConfig.scanMaxCm = 2000;

    ticket_.setPreScanJob(false);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::LFP);
    ticket_.setMaxLengthConfig(maxLengthConfig);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setEdgeToEdgeScan(false);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(2480,     scanIntent->getXScanSizeSide());
    EXPECT_EQ(2480,     scanIntent->getXMediaSize());
    EXPECT_EQ(3507,     scanIntent->getYScanSizeSide());
    EXPECT_EQ(3507,     scanIntent->getYMediaSize());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndEdgeToEdgeNotEnabledWithSmallMaxLength_ThenScanRegionHasTheCorrectValues)
{
    dune::copy::Jobs::Copy::MaxLengthConfig maxLengthConfig;
    maxLengthConfig.scanMaxCm = 5; //5cm

    ticket_.setPreScanJob(false);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::LFP);
    ticket_.setMaxLengthConfig(maxLengthConfig);

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setEdgeToEdgeScan(false);
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(2480,     scanIntent->getXScanSizeSide());
    EXPECT_EQ(2480,     scanIntent->getXMediaSize());
    EXPECT_EQ(590,      scanIntent->getYScanSizeSide());
    EXPECT_EQ(590,      scanIntent->getYMediaSize());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndScaleNotSupported_ThenScanIntentHasTheCorrectValues)
{
    ticket_.setPreScanJob(false);
    ON_CALL(*mockIScannerCapabilities_, isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale, _)).WillByDefault(Return(APIResult::ERROR));

    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(100000,     scanIntent->getScaleXFactor());
    EXPECT_EQ(100000,     scanIntent->getScaleYFactor());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageAndCompressionFactorIsSet_ThenCompressionFactorInScanIntentHasTheCorrectValues)
{
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::LFP);
    intent->setCompressionFactor(80);

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);

    EXPECT_EQ(80,     scanIntent->getCompressionFactor());
    EXPECT_EQ(dune::copy::SheetCollate::Collate, ticket_.getIntent()->getCollate());

}

TEST_F(GivenACopyJobTicket, WhenAddingANewpage_ThenScanIntentByDefaultHasTheCorrectValues)
{
    Margins desiredMargins_{Distance(236, 1200), Distance(236, 1200), Distance(236, 1200), Distance(236, 1200)};
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::HOME_PRO);

    dune::print::engine::MockIMedia mockIMedia;
    ticket_.setMediaInterface(&mockIMedia);
    ON_CALL(mockIMedia, getMargins(_)).WillByDefault(Return(std::tuple<APIResult, Margins>(APIResult::OK, desiredMargins_)));

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);
    //Check scan intent values
    EXPECT_EQ(dune::scan::types::ScanTypeEnum::Copy,                    scanIntent->getScanType());
    EXPECT_EQ(dune::scan::types::ScanOrientationEnum::ShortEdgeFeed,    scanIntent->getScanOrientation());
    EXPECT_EQ(dune::scan::types::DuplexSideEnum::FrontSide,             scanIntent->getInputDuplexMode());
    EXPECT_EQ(dune::scan::types::OriginalMediaType::WHITE_PAPER,        scanIntent->getInputMediaType());
    EXPECT_EQ(0,                                                        scanIntent->getXScanScaledSize());
    EXPECT_EQ(0,                                                        scanIntent->getYScanScaledSize());
    EXPECT_EQ(4,                                                        scanIntent->getBrightness());
    EXPECT_EQ(dune::scan::types::OriginalTypeEnum::Mixed,               scanIntent->getOriginalType());
    EXPECT_EQ(dune::scan::types::OriginalSubTypeEnum::Printed,          scanIntent->getOriginalSubType());
    EXPECT_EQ(dune::scan::types::ColorSpaceEnum::RGB,                   scanIntent->getColorSpace());
    EXPECT_EQ(600,                                                      scanIntent->getXImageQuality());
    EXPECT_EQ(600,                                                      scanIntent->getYImageQuality());
    EXPECT_EQ(0,                                                        scanIntent->getSharpness());
    EXPECT_EQ(2,                                                        scanIntent->getTextGraphicsPriority());
    EXPECT_EQ(2,                                                        scanIntent->getBackgroundRemoval());
    EXPECT_EQ(2,                                                        scanIntent->getBackgroundCleanup());
    EXPECT_EQ(dune::scan::types::PhotoModeEnum::Glossy,                 scanIntent->getPhotoModeType());
    EXPECT_EQ(0,                                                        scanIntent->getJobScanLimit());
    EXPECT_EQ(0,                                                        scanIntent->getContrast());
    EXPECT_EQ(false,                                                    scanIntent->getTransferObjectTypeMap());
    EXPECT_EQ(dune::scan::types::ScanBitDepthEnum::Depth8Bits,          scanIntent->getDigitalSendOutputBitDepth());
    EXPECT_EQ(false,                                                    scanIntent->getMixedMediaInput());
    EXPECT_EQ(dune::scan::types::ScanMediaEnum::Normal,                 scanIntent->getScannerMedia());
    EXPECT_EQ(dune::scan::types::ContentOrientationEnum::Portrait,      scanIntent->getContentOrientation());
    EXPECT_EQ(dune::scan::types::BookModeEnum::Disable,                 scanIntent->getBookMode());
    EXPECT_EQ(dune::scan::types::PageBindingModeEnum::HorizontalBinding,scanIntent->getPageBindingMode());
    EXPECT_EQ(0,                                                        scanIntent->getStripHeight());
    EXPECT_EQ(0,                                                        scanIntent->getStripWidth());
    EXPECT_EQ(1,                                                        scanIntent->getDigitalSendFileSize());
    EXPECT_EQ(0,                                                        scanIntent->getCounterfeitDetection());
    EXPECT_EQ(dune::scan::types::ScanBitDepthEnum::Depth8Bits,          scanIntent->getBitDepth());
    EXPECT_EQ(dune::scan::types::CompressionModeEnum::Uncompressed,     scanIntent->getCompressionMode());
    EXPECT_EQ(256,                                                      scanIntent->getMultipleNumberOfLinesRequired());
    EXPECT_EQ(false,                                                    scanIntent->getAutoToneScale());
    EXPECT_EQ(2,                                                        scanIntent->getAutoToneScaleRange());
    EXPECT_EQ(false,                                                    scanIntent->getAutoWhiteColorRemoval());
    EXPECT_EQ(1,                                                        scanIntent->getAutoWhiteColorRemovalRange());
    EXPECT_EQ(false,                                                    scanIntent->getNoImagePadding());
    EXPECT_EQ(true,                                                     scanIntent->getDisableMultiPickSensing());
    EXPECT_EQ(false,                                                    scanIntent->getMultiPickSensingAction());
    EXPECT_EQ(true,                                                     scanIntent->getDeskew());
    EXPECT_EQ(false,                                                    scanIntent->getDustDetection());
    EXPECT_EQ(dune::scan::types::BlankDetectEnum::Disable,              scanIntent->getDetectBlankPage());
    EXPECT_EQ(4,                                                        scanIntent->getSaturation());
    EXPECT_EQ(false,                                                    scanIntent->getPageCrop());
    EXPECT_EQ(false,                                                    scanIntent->getContentCrop());
    EXPECT_EQ(false,                                                    scanIntent->getNegative());
    EXPECT_EQ(true,                                                     scanIntent->getInterleaved());
    EXPECT_EQ(dune::scan::types::CcdChannelEnum::GrayCcdEmulated,       scanIntent->getCcdChannel());
    EXPECT_EQ(dune::scan::types::BinaryRenderingEnum::Halftone,         scanIntent->getBinaryRendering());
    EXPECT_EQ(false,                                                    scanIntent->getDescreen());
    EXPECT_EQ(false,                                                    scanIntent->getFeederPickStop());
    EXPECT_EQ(0,                                                        scanIntent->getShadow());
    EXPECT_EQ(20,                                                       scanIntent->getCompressionFactor());
    EXPECT_EQ(0,                                                        scanIntent->getThreshold());
    EXPECT_EQ(dune::scan::types::AutoColorDetectEnum::DetectOnly,       scanIntent->getScanAutoColorDetect());
    EXPECT_EQ(false,                                                    scanIntent->getScanBlackBackground());
    EXPECT_EQ(0,                                                        scanIntent->getScanNumberPages());
    EXPECT_EQ(false,                                                    scanIntent->getScanAutoExposure());
    EXPECT_EQ(100,                                                      scanIntent->getScanGamma());
    EXPECT_EQ(0,                                                        scanIntent->getScanHighlight());
    EXPECT_EQ(0,                                                        scanIntent->getScanColorSensitivity());
    EXPECT_EQ(0,                                                        scanIntent->getScanColorRange());
    EXPECT_EQ(false,                                                    scanIntent->getScanPagesFlipUpEnabled());
    EXPECT_EQ(dune::scan::types::ImagePreview::Disable,                 scanIntent->getImagePreview());
    EXPECT_EQ(dune::scan::types::OverScanType::TOPANDBOTTOM,            scanIntent->getOverScan());
    EXPECT_EQ(false,                                                    scanIntent->getAutoCrop());
    EXPECT_EQ(0,                                                        scanIntent->getScanNoiseRemoval());
    EXPECT_EQ(0,                                                        scanIntent->getScanBlankPageSensitivity());
    EXPECT_EQ(false,                                                    scanIntent->getAutoRelease());
    EXPECT_EQ(dune::scan::types::ScanCaptureModeType::STANDARD,         scanIntent->getScanCaptureMode());
    EXPECT_EQ(dune::scan::types::ScanAcquisitionsSpeedEnum::AUTO,       scanIntent->getScanAcquisitionsSpeed());
    EXPECT_EQ(false,                                                    scanIntent->getIsCalibrationJob());
    EXPECT_EQ(0,                                                        scanIntent->getTopOffsetOversize());
    EXPECT_EQ(0,                                                        scanIntent->getBottomOffsetOversize());
    EXPECT_EQ(0,                                                        scanIntent->getAdfMaxPagesToScan());
    EXPECT_EQ(dune::copy::SheetCollate::Collate, ticket_.getIntent()->getCollate());
}

TEST_F(GivenACopyJobTicket, WhenAddingANewpageInScan_ThenResolutionByDefaultHasTheCorrectValues)
{
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::LFP);

    Margins desiredMargins_{Distance(236, 1200), Distance(236, 1200), Distance(236, 1200), Distance(236, 1200)};
    //Create uuid
    Uuid pageId{Uuid::createUuid()};
    //Get intent
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    dune::print::engine::MockIMedia mockIMedia;
    ticket_.setMediaInterface(&mockIMedia);
    ON_CALL(mockIMedia, getMargins(_)).WillByDefault(Return(std::tuple<APIResult, Margins>(APIResult::OK, desiredMargins_)));

    //Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    //Once page has been added, get print intent and check values
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent = std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(pageTicket->getIntent(dune::job::IntentType::SCAN));

    EXPECT_TRUE(scanIntent != nullptr);
    EXPECT_EQ(RESOLUTION, scanIntent->getXImageQuality());
}

TEST_F(GivenACopyJobTicket, WhenCallingGetMediaSizeFromMediaSource_MediaSizeIsReturned)
{
    CopyJobTicket ticket;
    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();

    dune::print::engine::MockIMedia mockIMedia;
    std::shared_ptr<dune::print::engine::MockIMediaIInputTray> mockIMediaIInputTray;
    mockIMediaIInputTray = std::make_shared<dune::print::engine::MockIMediaIInputTray>();
    std::shared_ptr<const dune::print::engine::MockIMediaIInputTray> cMockIMediaIInputTray;
    cMockIMediaIInputTray = std::make_shared<const dune::print::engine::MockIMediaIInputTray>();
    auto traySnapshot = std::make_shared<IMedia::InputTraySnapshot>(cMockIMediaIInputTray);

    traySnapshot->setMediaSize(std::make_tuple(true, MediaSize(dune::imaging::types::MediaSizeId::A4)));
    //ensure mediaInterface not null
    ticket.setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket.getMediaInterface() != NULL);

    IMedia::InputList inputs;
    inputs.push_back(mockIMediaIInput);

    EXPECT_CALL(*mockIMediaIInput, getMediaSource()).WillRepeatedly(Return(dune::print::engine::MediaSource::AUTOSELECT));
    EXPECT_CALL(*mockIMediaIInput, getType()).WillRepeatedly(Return(dune::print::engine::InputType::TRAY));
    EXPECT_CALL(*mockIMediaIInput, getTray()).WillRepeatedly(Return(mockIMediaIInputTray));
    EXPECT_CALL(*mockIMediaIInputTray, getSnapShot()).WillRepeatedly(Return(std::make_tuple(APIResult::OK, traySnapshot)));
    EXPECT_CALL(*mockIMediaIInputTray, getMediaSource()).WillRepeatedly(Return(dune::imaging::types::MediaSource::AUTOSELECT));
    EXPECT_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillOnce(Return(std::make_tuple(APIResult::OK, inputs)));

    auto mediaSizeFromMediaSource = ticket.getMediaSizeFromMediaSource(mockIMediaIInput->getMediaSource());

    EXPECT_EQ(mediaSizeFromMediaSource , dune::imaging::types::MediaSizeId::A4);
}

TEST_F(GivenACopyJobTicket, WhenCallingGetSupportedMediaSizesWithSourceSetToRoll_CustomMediaSizeIsReturned)
{
    CopyJobTicket ticket;

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();

    std::shared_ptr<dune::print::engine::MockIMediaIInputRoll> mockIMediaIInputRoll;
    mockIMediaIInputRoll = std::make_shared<dune::print::engine::MockIMediaIInputRoll>();
    dune::print::engine::MockIMediaIInputRoll inputRollMock;

    ON_CALL(inputRollMock, getMediaSource())
        .WillByDefault(Return(MediaSource::MAINROLL));
    ON_CALL(inputRollMock, getType())
        .WillByDefault(Return(dune::print::engine::InputType::ROLL));
    IMedia::InputRollPtr mockInputRollPtr{&inputRollMock, [](IMedia::IInput *) {}};
    ON_CALL(inputRollMock, getRoll())
        .WillByDefault(Return(mockInputRollPtr));
    std::tuple<APIResult, bool> customSizeSupported{APIResult::OK, true};
    ON_CALL(inputRollMock, isCustomSizeSupported())
        .WillByDefault(ReturnRef(customSizeSupported));

    auto rollSnapshot = std::make_shared<IMedia::InputRollSnapshot>(mockInputRollPtr);
    ON_CALL(inputRollMock, getSnapShot())
        .WillByDefault(Return(std::make_tuple<APIResult>(APIResult::OK, rollSnapshot)));

    IMedia::InputList inputs{mockInputRollPtr};
    dune::print::engine::MockIMedia mockIMedia;
    ON_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    ticket.setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket.getMediaInterface() != NULL);

    auto results = ticket.getSupportedMediaSizes(MediaSource::MAINROLL);
    EXPECT_EQ(std::get<0>(results), APIResult::OK);
    EXPECT_EQ(std::get<1>(results).size(), 1);
    EXPECT_EQ(std::get<1>(results).at(0), dune::cdm::glossary_1::MediaSize::custom);
}

TEST_F(GivenACopyJobTicket, WhenCallingGetMediaSizeFromMediaSourceSetToRoll_CustomMediaSizeIsReturned)
{
    CopyJobTicket ticket;

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();

    std::shared_ptr<dune::print::engine::MockIMediaIInputRoll> mockIMediaIInputRoll;
    mockIMediaIInputRoll = std::make_shared<dune::print::engine::MockIMediaIInputRoll>();
    dune::print::engine::MockIMediaIInputRoll inputRollMock;

    ON_CALL(inputRollMock, getMediaSource())
        .WillByDefault(Return(MediaSource::MAINROLL));
    ON_CALL(inputRollMock, getType())
        .WillByDefault(Return(dune::print::engine::InputType::ROLL));
    IMedia::InputRollPtr mockInputRollPtr{&inputRollMock, [](IMedia::IInput *) {}};
    ON_CALL(inputRollMock, getRoll())
        .WillByDefault(Return(mockInputRollPtr));
    std::tuple<APIResult, bool> customSizeSupported{APIResult::OK, true};
    ON_CALL(inputRollMock, isCustomSizeSupported())
        .WillByDefault(ReturnRef(customSizeSupported));

    auto rollSnapshot = std::make_shared<IMedia::InputRollSnapshot>(mockInputRollPtr);
    ON_CALL(inputRollMock, getSnapShot())
        .WillByDefault(Return(std::make_tuple<APIResult>(APIResult::OK, rollSnapshot)));

    IMedia::InputList inputs{mockInputRollPtr};
    dune::print::engine::MockIMedia mockIMedia;
    ON_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    ticket.setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket.getMediaInterface() != NULL);

    auto mediaSize = ticket.getMediaSizeFromMediaSource(dune::imaging::types::MediaSource::MAINROLL);
    EXPECT_EQ(mediaSize, dune::imaging::types::MediaSizeId::CUSTOM);
}

TEST_F(GivenACopyJobTicket, WhenCallingGetAllSupportedMediaSizesInEnterprise_ThenMediaSizeHasTheCorrectValues)
{
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::ENTERPRISE);

    std::vector<dune::imaging::types::OrientedMediaSize> supportedMediaSizes;
    std::vector<dune::imaging::types::MediaOrientation> mediaOrientationMostOfAll;
    mediaOrientationMostOfAll.push_back(dune::imaging::types::MediaOrientation::PORTRAIT);
    supportedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::ANY), mediaOrientationMostOfAll));
    supportedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::A4), mediaOrientationMostOfAll));

    dune::print::engine::MockIMedia mockIMedia;
    ticket_.setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket_.getMediaInterface() != NULL);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();
    IMedia::InputList inputs{mockIMediaIInput};
    ON_CALL(*mockIMediaIInput, getMediaSource()).WillByDefault(Return(dune::print::engine::MediaSource::AUTOSELECT));
    ON_CALL(*mockIMediaIInput, getType()).WillByDefault(Return(dune::print::engine::InputType::TRAY));
    ON_CALL(*mockIMediaIInput, getMediaSupportedSizes()).WillByDefault(Return(std::make_tuple(APIResult::OK, supportedMediaSizes)));
    ON_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    auto result = ticket_.getAllSupportedMediaSizes();

    auto supportedMediaSize = std::get<1>(result);
    bool foundAny{false};
    for (auto mediaSize : supportedMediaSize)
    {
        if (mediaSize == dune::cdm::glossary_1::MediaSize::any)
        {
            foundAny = true;
            break;
        }
    }

    EXPECT_TRUE(foundAny == true);
}

TEST_F(GivenACopyJobTicket, WhenCallingGetAllSupportedMediaSizesInNotEnterprise_ThenMediaSizeHasTheCorrectValues)
{
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::HOME_PRO);

    std::vector<dune::imaging::types::OrientedMediaSize> supportedMediaSizes;
    std::vector<dune::imaging::types::MediaOrientation> mediaOrientationMostOfAll;
    mediaOrientationMostOfAll.push_back(dune::imaging::types::MediaOrientation::PORTRAIT);
    supportedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::ANY), mediaOrientationMostOfAll));
    supportedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::A4), mediaOrientationMostOfAll));

    dune::print::engine::MockIMedia mockIMedia;
    ticket_.setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket_.getMediaInterface() != NULL);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();
    IMedia::InputList inputs{mockIMediaIInput};
    ON_CALL(*mockIMediaIInput, getMediaSource()).WillByDefault(Return(dune::print::engine::MediaSource::AUTOSELECT));
    ON_CALL(*mockIMediaIInput, getType()).WillByDefault(Return(dune::print::engine::InputType::TRAY));
    ON_CALL(*mockIMediaIInput, getMediaSupportedSizes()).WillByDefault(Return(std::make_tuple(APIResult::OK, supportedMediaSizes)));
    ON_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    auto result = ticket_.getAllSupportedMediaSizes();

    auto supportedMediaSize = std::get<1>(result);
    bool foundAny{false};
    for (auto mediaSize : supportedMediaSize)
    {
        if (mediaSize == dune::cdm::glossary_1::MediaSize::any)
        {
            foundAny = true;
            break;
        }
    }

    EXPECT_TRUE(foundAny == false);
}

TEST_F(GivenACopyJobTicket, WhenCallingGetSupportedMediaSizesInEnterprise_ThenMediaSizeHasTheCorrectValues)
{
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::ENTERPRISE);

    std::vector<dune::imaging::types::OrientedMediaSize> supportedMediaSizes;
    std::vector<dune::imaging::types::MediaOrientation> mediaOrientationMostOfAll;
    mediaOrientationMostOfAll.push_back(dune::imaging::types::MediaOrientation::PORTRAIT);
    supportedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::ANY), mediaOrientationMostOfAll));
    supportedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::A4), mediaOrientationMostOfAll));

    dune::print::engine::MockIMedia mockIMedia;
    ticket_.setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket_.getMediaInterface() != NULL);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();
    IMedia::InputList inputs{mockIMediaIInput};
    std::tuple<APIResult, bool> customSizeSupported{APIResult::OK, true};
    ON_CALL(*mockIMediaIInput, isCustomSizeSupported()).WillByDefault(ReturnRef(customSizeSupported));
    ON_CALL(*mockIMediaIInput, getMediaSource()).WillByDefault(Return(dune::print::engine::MediaSource::TRAY1));
    ON_CALL(*mockIMediaIInput, getType()).WillByDefault(Return(dune::print::engine::InputType::TRAY));
    ON_CALL(*mockIMediaIInput, getMediaSupportedSizes()).WillByDefault(Return(std::make_tuple(APIResult::OK, supportedMediaSizes)));
    ON_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    auto result = ticket_.getSupportedMediaSizes(dune::imaging::types::MediaSource::TRAY1);

    auto supportedMediaSize = std::get<1>(result);
    bool foundAny{false};
    for (auto mediaSize : supportedMediaSize)
    {
        if (mediaSize == dune::cdm::glossary_1::MediaSize::any)
        {
            foundAny = true;
            break;
        }
    }

    EXPECT_TRUE(foundAny == true);
}

TEST_F(GivenACopyJobTicket, WhenCallingGetSupportedMediaSizesInNotEnterprise_ThenMediaSizeHasTheCorrectValues)
{
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::HOME_PRO);

    std::vector<dune::imaging::types::OrientedMediaSize> supportedMediaSizes;
    std::vector<dune::imaging::types::MediaOrientation> mediaOrientationMostOfAll;
    mediaOrientationMostOfAll.push_back(dune::imaging::types::MediaOrientation::PORTRAIT);
    supportedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::ANY), mediaOrientationMostOfAll));
    supportedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::A4), mediaOrientationMostOfAll));

    dune::print::engine::MockIMedia mockIMedia;
    ticket_.setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket_.getMediaInterface() != NULL);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();
    IMedia::InputList inputs{mockIMediaIInput};
    std::tuple<APIResult, bool> customSizeSupported{APIResult::OK, true};
    ON_CALL(*mockIMediaIInput, isCustomSizeSupported()).WillByDefault(ReturnRef(customSizeSupported));
    ON_CALL(*mockIMediaIInput, getMediaSource()).WillByDefault(Return(dune::print::engine::MediaSource::TRAY1));
    ON_CALL(*mockIMediaIInput, getType()).WillByDefault(Return(dune::print::engine::InputType::TRAY));
    ON_CALL(*mockIMediaIInput, getMediaSupportedSizes()).WillByDefault(Return(std::make_tuple(APIResult::OK, supportedMediaSizes)));
    ON_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    auto result = ticket_.getSupportedMediaSizes(dune::imaging::types::MediaSource::TRAY1);

    auto supportedMediaSize = std::get<1>(result);
    bool foundAny{false};
    for (auto mediaSize : supportedMediaSize)
    {
        if (mediaSize == dune::cdm::glossary_1::MediaSize::any)
        {
            foundAny = true;
            break;
        }
    }

    EXPECT_TRUE(foundAny == false);
}

TEST_F(GivenACopyJobTicket, WhenCallingGetAllSupportedMediaSourcesInEnterprise_ThenMediaSourceHasTheCorrectValues)
{
    CopyJobTicket ticket;
    ticket.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::ENTERPRISE);

    std::shared_ptr<dune::print::engine::MockIMediaIInputTray> mockIMediaIInputTray;
    mockIMediaIInputTray = std::make_shared<dune::print::engine::MockIMediaIInputTray>();
    std::shared_ptr<const dune::print::engine::MockIMediaIInputTray> cMockIMediaIInputTray;
    cMockIMediaIInputTray = std::make_shared<const dune::print::engine::MockIMediaIInputTray>();
    auto traySnapshot = std::make_shared<IMedia::InputTraySnapshot>(cMockIMediaIInputTray);

    dune::print::engine::MockIMedia* mockIMedia;
    mockIMedia = new dune::print::engine::MockIMedia();
    ticket.setMediaInterface(mockIMedia);
    EXPECT_TRUE(ticket.getMediaInterface() != NULL);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();
    IMedia::InputList inputs{mockIMediaIInput};
    ON_CALL(*mockIMediaIInput, getType()).WillByDefault(Return(dune::print::engine::InputType::TRAY));
    ON_CALL(*mockIMediaIInput, getTray()).WillByDefault(Return(mockIMediaIInputTray));
    ON_CALL(*mockIMediaIInputTray, getSnapShot()).WillByDefault(Return(std::make_tuple(APIResult::OK, traySnapshot)));
    ON_CALL(*mockIMediaIInputTray, getMediaSource()).WillByDefault(Return(dune::print::engine::MediaSource::TRAY1));
    ON_CALL(*mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    auto result = ticket.getAllSupportedMediaSources();

    auto supportedMediaSource = std::get<1>(result);
    bool foundAny{false};
    for (auto mediaSource : supportedMediaSource)
    {
        if (mediaSource == dune::cdm::glossary_1::MediaSourceId::manual)
        {
            foundAny = true;
            break;
        }
    }

    delete(mockIMedia);
    EXPECT_TRUE(foundAny == true);
}

TEST_F(GivenACopyJobTicket, WhenCallingGetAllSupportedMediaSourcesInNotEnterprise_ThenMediaSourceHasTheCorrectValues)
{
    CopyJobTicket ticket;
    ticket.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::HOME_PRO);

    std::shared_ptr<dune::print::engine::MockIMediaIInputTray> mockIMediaIInputTray;
    mockIMediaIInputTray = std::make_shared<dune::print::engine::MockIMediaIInputTray>();
    std::shared_ptr<const dune::print::engine::MockIMediaIInputTray> cMockIMediaIInputTray;
    cMockIMediaIInputTray = std::make_shared<const dune::print::engine::MockIMediaIInputTray>();
    auto traySnapshot = std::make_shared<IMedia::InputTraySnapshot>(cMockIMediaIInputTray);

    dune::print::engine::MockIMedia* mockIMedia;
    mockIMedia = new dune::print::engine::MockIMedia();
    ticket.setMediaInterface(mockIMedia);
    EXPECT_TRUE(ticket.getMediaInterface() != NULL);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();
    IMedia::InputList inputs{mockIMediaIInput};
    ON_CALL(*mockIMediaIInput, getType()).WillByDefault(Return(dune::print::engine::InputType::TRAY));
    ON_CALL(*mockIMediaIInput, getTray()).WillByDefault(Return(mockIMediaIInputTray));
    ON_CALL(*mockIMediaIInputTray, getSnapShot()).WillByDefault(Return(std::make_tuple(APIResult::OK, traySnapshot)));
    ON_CALL(*mockIMediaIInputTray, getMediaSource()).WillByDefault(Return(dune::print::engine::MediaSource::TRAY1));
    ON_CALL(*mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    auto result = ticket.getAllSupportedMediaSources();

    auto supportedMediaSource = std::get<1>(result);
    bool foundAny{false};
    for (auto mediaSource : supportedMediaSource)
    {
        if (mediaSource == dune::cdm::glossary_1::MediaSourceId::manual)
        {
            foundAny = true;
            break;
        }
    }

    delete(mockIMedia);
    EXPECT_TRUE(foundAny == false);
}

TEST_F(GivenACopyJobTicket, WhenSetTheColorModeToAutoDetect_ThenColorModeIsAutoDetect)
{
    //Validating the default copy job ticket
    CopyJobTicket ticket;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);

    // Base job ticket values
    EXPECT_EQ(ticket.getType(), dune::job::JobType::COPY);

    intent->setColorMode(ColorMode::AUTODETECT);

    EXPECT_EQ(ColorMode::AUTODETECT, intent->getColorMode());
}

TEST_F(GivenACopyJobTicket, WhenSerializingAndDeserializingResult_ThenResultIsTheSame)
{
    CopyJobTicket ticket;
    std::shared_ptr<ICopyJobResult> result = ticket.getResult();


    ticket.getResult()->setCompletedCopies(2);
    ticket.getResult()->setCompletedImpressions(10);

    CopyJobResult                   copyJobResult;
    copyJobResult.deserialize(*ticket.getResult()->serialize());

    CopyTicketsUtilities::compareCopyJobResult(*ticket.getResult(), copyJobResult);
}

TEST_F(GivenACopyJobTicket, WhenCloningCopyResult_ThenClonedResultAreCorrect)
{
    CopyJobResult                   copyJobResult{*ticket_.getResult()};
    std::unique_ptr<ICopyJobResult> clonedCopyJotbResult{copyJobResult.clone()};

    CopyTicketsUtilities::compareCopyJobResult(copyJobResult, *clonedCopyJotbResult);
}

TEST_F(GivenACopyJobTicket, WhenGettingHandler_ThenHandlerIsValid)
{
    EXPECT_NE(nullptr, ticket_.getHandler());
}

TEST_F(GivenACopyJobTicket, WhenDeserializeIsCalled_ThenHandlerIsSet)
{
    CopyJobTicket ticket;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);

    ticket.setJobName("Sample_Job");

    bool check = ticket.deserialize(ticket.serialize());
    std::shared_ptr<dune::job::IJobTicketHandler> copyJobTicketHandler = ticket.getHandler();
    dune::job::IJobTicketHandler::DocumentSettings docSettings = copyJobTicketHandler->getDocumentSettings();

    // Validate jobTicket handler
    EXPECT_EQ(true, check);
    EXPECT_NE(nullptr, copyJobTicketHandler);
    EXPECT_EQ(docSettings.jobName, "Sample_Job");
}

TEST_F(GivenACopyJobTicket, WhenRemovePage_ThenPageIsRemoved)
{
    // Create uuid
    Uuid pageId{Uuid::createUuid()};

    dune::job::IIntentsManager::IntentsMap intentsMap;
    dune::job::IIntentsManager::PageIntent pageIntent;

    EXPECT_CALL(*intentsManager_, updatePageIntents(_, _)).Times(1);

    // Add new page
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);

    // Remove the page
    ticket_.removePage(pageId);

    // try to get the page
    EXPECT_EQ(ticket_.getPage(pageId), nullptr);
}

TEST_F(GivenACopyJobTicket, WhenRemoveNotExistingPage_ThenPageNotExist)
{
    // Create uuid
    Uuid pageId{Uuid::createUuid()};

    // Remove the page
    ticket_.removePage(pageId);

    // try to get the page
    EXPECT_EQ(ticket_.getPage(pageId), nullptr);
}

TEST_F(GivenACopyJobTicket, WhengetEnabledMediaTypesIsCalled_ThenEnabledMediaTypesAreReturned)
{
    CopyJobTicket ticket;

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();

    IMedia::InputList inputs{mockIMediaIInput};
    dune::print::engine::MockIMedia mockIMedia;
    ON_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    ticket.setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket.getMediaInterface() != NULL);

    std::vector<dune::imaging::types::MediaIdType> mediaIdTypes;
    mediaIdTypes.push_back(dune::imaging::types::MediaIdType::STATIONERY);
    mediaIdTypes.push_back(dune::imaging::types::MediaIdType::HPECOFFICIENT);
    mediaIdTypes.push_back(dune::imaging::types::MediaIdType::TRANSPARENCY);
    mediaIdTypes.push_back(dune::imaging::types::MediaIdType::USER_DEFINED_1);
    std::vector<dune::print::engine::MediaId> mediaIds;
    for(auto mediaType: mediaIdTypes)
    {
        dune::imaging::types::MediaId med(mediaType);
        mediaIds.push_back(med);
    }

    EXPECT_CALL(*mockIMediaIInput, getMediaSupportedTypes()).WillOnce(Return(std::make_tuple(APIResult::OK, mediaIds)));

    auto results = ticket.getEnabledMediaTypes();
    EXPECT_EQ(std::get<0>(results), APIResult::OK);
    EXPECT_EQ(std::get<1>(results).size(), 4);
    EXPECT_EQ(std::get<1>(results).at(0), dune::cdm::glossary_1::MediaType::stationery);
    EXPECT_EQ(std::get<1>(results).at(1), dune::cdm::glossary_1::MediaType::com_dot_hp_dot_EcoSMARTLite);
    EXPECT_EQ(std::get<1>(results).at(2), dune::cdm::glossary_1::MediaType::transparency);
    EXPECT_EQ(std::get<1>(results).at(3), dune::cdm::glossary_1::MediaType::com_dot_hp_dot_usertype_dash_1);
}

TEST_F(GivenACopyJobTicket, WhensetisMediaTypeVisibilityTogglingSupportedIsCalled_ThenMediaTypeVisibilityTogglingSupportedIsSet)
{
    CopyJobTicket ticket;
    ticket.setisMediaTypeVisibilityTogglingSupported(true);
    EXPECT_EQ(ticket.isMediaTypeVisibilityTogglingSupported(), true);
}

TEST_F(GivenACopyJobTicket, WhenIsInstalledSpecificPageBasedFinisherDeviceIsCalled_ThenStapleFinisherAreReturned)
{
    EXPECT_TRUE(ticket_.IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::STAPLE));
}

TEST_F(GivenACopyJobTicket, WhenIsInstalledSpecificPageBasedFinisherDeviceIsCalled_ThenPunchFinisherAreReturned)
{
    EXPECT_TRUE(ticket_.IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::PUNCH));
}

TEST_F(GivenACopyJobTicket, WhenIsInstalledSpecificPageBasedFinisherDeviceIsCalled_ThenFoldFinisherAreReturned)
{
    EXPECT_TRUE(ticket_.IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::FOLD));
}

TEST_F(GivenACopyJobTicket, WhenIsInstalledSpecificPageBasedFinisherDeviceIsCalled_ThenBookletFinisherAreReturned)
{
    EXPECT_TRUE(ticket_.IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::BOOKLET_MAKING));
}

TEST_F(GivenACopyJobTicket, WhensetConstraintsFromFb_TestConstraintsLoadSuccess)
{
    CopyJobTicket ticket;

     std::string jsonConstraints =
    "    { "
    "        \"plexMode\": [ "
    "            \"SIMPLEX\", "
    "            \"DUPLEX\" "
    "    	 ], "
    "        \"plexBinding\": [ "
    "            \"LONG_EDGE\", "
    "            \"SHORT_EDGE\" "
    "        ], "
    "        \"collate\": [ "
    "            \"Collate\", "
    "            \"Uncollate\" "
    "        ], "
    "        \"minCopies\": 1, "
    "        \"maxCopies\": 999, "
    "        \"stepCopies\": 1.0, "
    "        \"printQuality\": [ "
    "            \"DRAFT\", "
    "            \"BEST\" "
    "        ], "
    "        \"stapleOptionStr\": [ "
	"            {\"nameValue\":\"none\",\"stringId\":\"StringIds.cNone\"}, "
	"            {\"nameValue\":\"topAnyOnePointAny\",\"stringId\":\"StringIds.cStapleTopLeftOrRight\"}, "
	"            {\"nameValue\":\"topAnyOnePointAngled\",\"stringId\":\"StringIds.cStapleTopLeftOnePointAngled\"}, "
	"            {\"nameValue\":\"topLeftOnePointAny\",\"stringId\":\"StringIds.cStapleTopLeftOnePointAngled\"}, "
	"            {\"nameValue\":\"topLeftOnePointAngled\",\"stringId\":\"StringIds.cStapleTopLeftOnePointAngled\"}, "
	"            {\"nameValue\":\"topRightOnePointAny\",\"stringId\":\"StringIds.cStapleTopRightOnePointAngled\"}, "
	"            {\"nameValue\":\"topRightOnePointAngled\",\"stringId\":\"StringIds.cStapleTopRightOnePointAngled\"}, "
	"            {\"nameValue\":\"leftTwoPoints\",\"stringId\":\"StringIds.cStapleLeftTwoPoints\"}, "
	"            {\"nameValue\":\"leftTwoPointsAny\",\"stringId\":\"StringIds.cStapleTopLeftOrRight\"}, "
	"            {\"nameValue\":\"rightTwoPoints\",\"stringId\":\"StringIds.cStapleRightTwoPoints\"}, "
	"            {\"nameValue\":\"topTwoPoints\",\"stringId\":\"StringIds.cStapleTopTwoPoints\"}, "
	"            {\"nameValue\":\"leftThreePointsAny\",\"stringId\":\"StringIds.cStapleLeftThreePointsAny\"}, "
	"            {\"nameValue\":\"topThreePoints\",\"stringId\":\"StringIds.cStapleTopThreePoints\"}, "
	"        ], "
    "        \"punchOptionStr\": [ "
    "            {\"nameValue\":\"none\",\"stringId\":\"StringIds.cNone\"}, "
    "            {\"nameValue\":\"leftTwoPointDin\",\"stringId\":\"StringIds.cStapleLeftTwoPoints\"}, "
    "            {\"nameValue\":\"rightTwoPointUs\",\"stringId\":\"StringIds.cStapleRightTwoPoints\"}, "
    "            {\"nameValue\":\"bottomThreePointUs\",\"stringId\":\"StringIds.cPunchingOptionsBottomThreePointUs\"}, "
    "            {\"nameValue\":\"topFourPointDin\",\"stringId\":\"StringIds.cPunchingOptionsTopFourPointDin\"}, "
    "            {\"nameValue\":\"bottomFourPointDin\",\"stringId\":\"StringIds.cPunchingOptionsBottomFourPointDin\"}, "
    "            {\"nameValue\":\"leftFourPointSwd\",\"stringId\":\"StringIds.cPunchingOptionsLeftFourPointDin\"}, "
    "            {\"nameValue\":\"bottomFourPointSwd\",\"stringId\":\"StringIds.cPunchingOptionsBottomFourPointDin\"}, "
    "            {\"nameValue\":\"bottomTwoPoint\",\"stringId\":\"StringIds.cPunchingOptionsBottomTwoPointDin\"} "
	"        ], "
    "        \"finisherConstraintString\": [ "
    "            {\"nameValue\":\"cHolePunchConstraint\",\"stringId\":\"StringIds.cHolePunchConstraint\"}, "
    "            {\"nameValue\":\"cStapleHolePunchConstraint\",\"stringId\":\"StringIds.cStapleHolePunchConstraint\" },"
    "            {\"nameValue\":\"cStapleConstraint\",\"stringId\":\"StringIds.cStapleConstraint\" },"
    "            {\"nameValue\":\"cHolePunchStapleConstraint\",\"stringId\":\"StringIds.cHolePunchStapleConstraint\"} "
    "        ], "
    "        \"finisherOptionStrings\": [ "
    "		     {\"nameValue\":\"STAPLE\",\"stringId\":\"StringIds.cStapleConstraint\"}, "
    "            {\"nameValue\":\"PUNCH\",\"stringId\":\"StringIds.cHolePunchConstraint\"}, "
    "            {\"nameValue\":\"PUNCH_STAPLE\",\"stringId\":\"StringIds.cHolePunchStapleConstraint\"}, "
    "            {\"nameValue\":\"STAPLE_PUNCH\",\"stringId\":\"StringIds.cStapleHolePunchConstraint\"}, "
    "            {\"nameValue\":\"BOOKLET_STAPLE\",\"stringId\":\"StringIds.cStapleBookletTurnedOff\"}, "
    "            {\"nameValue\":\"FOLD_STAPLE\",\"stringId\":\"StringIds.cStapleNoneFoldSelected\"}, "
    "            {\"nameValue\":\"BOOKLET_PUNCH\",\"stringId\":\"StringIds.cHolePunchTurnedOff\"}, "
    "            {\"nameValue\":\"FOLD_PUNCH\",\"stringId\":\"StringIds.cHolePunchFoldSelected\"}, "
    "            {\"nameValue\":\"STAPLE_BOOKLET\",\"stringId\":\"StringIds.cBookletNoneOptionSelected\"}, "
    "            {\"nameValue\":\"PUNCH_BOOKLET\",\"stringId\":\"StringIds.cBookletNoneHoleSelected\"}, "
    "            {\"nameValue\":\"FOLD_BOOKLET\",\"stringId\":\"StringIds.cBookletFoldOptionSelected\"}, "
    "            {\"nameValue\":\"STAPLE_PUNCH_BOOKLET\",\"stringId\":\"StringIds.cBookletHolePunchSelected\"}, "
    "            {\"nameValue\":\"BOOKLET_FOLD\",\"stringId\":\"StringIds.cFoldStitchTurnedOff\"}, "
    "            {\"nameValue\":\"STAPLE_FOLD\",\"stringId\":\"StringIds.cFoldOptionStapleSelected\"}, "
    "            {\"nameValue\":\"PUNCH_FOLD\",\"stringId\":\"StringIds.cFoldNoneHoleSelected\"}, "
    "            {\"nameValue\":\"STAPLE_PUNCH_FOLD\",\"stringId\":\"StringIds.cFoldNoneOptionSelected\"} "
    "      ], " 
    "       \"scanJobConstraint\": {  "
    "            \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
    "            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
    "            \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
    "            \"scanPagesFlipUpEnabled\": [ false, true ], "
    "            \"minScanExposure\": 1, "
    "            \"maxScanExposure\": 9, "
    "            \"stepScanExposure\": 1.0, "
    "            \"minScalePercent\": 25, "
    "            \"maxScalePercent\": 400, "
    "            \"step\":1.0, "
    "         }"
    "     } "
    ;

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket.clearConstraintsFromFb();
    ticket.setConstraintsFromFb(tableT);
}

TEST_F(GivenACopyJobTicket, WhengetStapleString_ConstraintsStaringIReturned)
{
    CopyJobTicket ticket;
    std::string constraintString1 = ticket.getStapleString(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANGLED);
    EXPECT_EQ(constraintString1 , "StringIds.cStapleTopLeftOnePointAngled");
    std::string constraintString2 = ticket.getStapleString(dune::imaging::types::StapleOptions::LEFT_TWO_POINTS);
    EXPECT_EQ(constraintString2 , "StringIds.cStapleLeftTwoPoints");
}

TEST_F(GivenACopyJobTicket, WhengetHolePunchString_ConstraintsStaringIReturned)
{
    CopyJobTicket ticket;
    std::string constraintString1 = ticket.getHolePunchString(dune::imaging::types::PunchingOptions::LEFT_TWO_POINT_DIN);
    EXPECT_EQ(constraintString1, "StringIds.cStapleLeftTwoPoints");
    std::string constraintString2 = ticket.getHolePunchString(dune::imaging::types::PunchingOptions::TOP_FOUR_POINT_DIN);
    EXPECT_EQ(constraintString2, "StringIds.cPunchingOptionsTopFourPointDin");
}

TEST_F(GivenACopyJobTicket, WhengetFinisherConstraintString_ConstraintsStaringIReturned)
{
    CopyJobTicket ticket;
    std::string constraintString1 = ticket.getFinisherConstraintString("cHolePunchConstraint");
    EXPECT_EQ(constraintString1, "StringIds.cHolePunchConstraint");
    std::string constraintString2 = ticket.getFinisherConstraintString("cStapleHolePunchConstraint");
    EXPECT_EQ(constraintString2, "StringIds.cStapleHolePunchConstraint");
}

TEST_F(GivenACopyJobTicket, WhengetConstraintsMsgBetweenFinisherOption_ConstraintsStaringIReturned)
{    
    CopyJobTicket ticket;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();

    ticket.setLocalizationInterface(mockLocaleProvider_);

    StringId_Type stringIdTypeBookletStaple = (string_id::cStapleBookletTurnedOff).value();
    StringId_Type stringIdTypeBookletFold = (string_id::cFoldStitchTurnedOff).value();

    ON_CALL(*mockLocale_, get(testing::Matcher<StringId_Type>(_))).WillByDefault(Return("The Staple feature can only be used when ""Booklet Fold and Stitch"" is turned off."));
    ON_CALL(*mockLocaleProvider_, deviceLocale()).WillByDefault(Return(mockLocale_));
    
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);
    auto constraintString1 = ticket.getConstraintsMsgBetweenFinisherOption(dune::imaging::types::MediaProcessingTypes::STAPLE);
    EXPECT_EQ(constraintString1, "The Staple feature can only be used when Booklet Fold and Stitch is turned off.");
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::NONE);

    ON_CALL(*mockLocale_, get(testing::Matcher<StringId_Type>(_))).WillByDefault(Return("The Booklet Fold and Stitch feature can only be used if the ""None"" option in ""Fold"" is selected."));
    intent->setFoldOption(dune::imaging::types::FoldingOptions::C_INWARD_TOP);
    auto constraintString2 = ticket.getConstraintsMsgBetweenFinisherOption(dune::imaging::types::MediaProcessingTypes::BOOKLET_MAKING);
    EXPECT_EQ(constraintString2, "The Booklet Fold and Stitch feature can only be used if the None option in Fold is selected.");
}

TEST_F(GivenACopyJobTicket, WhenclearConstraintsFromFb_TestConstraintsClearSuccess)
{
    CopyJobTicket ticket;
    ticket.clearConstraintsFromFb();
}

TEST_F(GivenACopyJobTicket, WhengetPageBasedFinisherValidMediaSizesIsCalledNoFinisher_ThenSupportMediaSizeOptionsAreReturned)
{
  //  CopyJobTicket ticket;
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setMediaInterface(mockIMedia_);

    std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaSize>> result;

    intent->setStapleOption(dune::imaging::types::StapleOptions::NONE);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::NONE);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::NONE);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::NONE);

    intent->setOutputMediaIdType(dune::imaging::types::MediaIdType::ANY);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::UNDEFINED);

    result = ticket_.getPageBasedFinisherValidMediaSizes();
    ASSERT_EQ(std::get<0>(result), false);
}

TEST_F(GivenACopyJobTicket, WhengetPageBasedFinisherValidMediaSizesIsCalledNoOption_ThenSupportMediaSizeOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaSize>> result;

    intent->setStapleOption(dune::imaging::types::StapleOptions::NONE);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::NONE);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::NONE);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::NONE);

    intent->setOutputMediaIdType(dune::imaging::types::MediaIdType::ANY);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::UNDEFINED);
/*
    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock1_;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher *) {} ) // stapling
    };

    const std::vector<dune::imaging::types::MediaDestinationId> allPossibleDestinationsList_ = {
        dune::imaging::types::MediaDestinationId::OUTPUTBIN1,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN2,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN3
    };

    ON_CALL(*mockIMedia_, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, pageBasedFinishers)));
    //ON_CALL(*mockIMedia_, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));
    IMedia::PageBasedFinisherPtr pageBasedFinisherPtr = IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher * p){} );

    ON_CALL(pageBasedFinisherMock1_, getType()).WillByDefault(Return(dune::print::engine::FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock1_, getMediaSupportedSizes()).WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaSizeList_)));
    ON_CALL(pageBasedFinisherMock1_, getMediaSupportedTypes()).WillByDefault(Return(std::make_tuple(APIResult::OK, allPossibleMediaIdList_)));
    ON_CALL(pageBasedFinisherMock1_, getMediaDestinationId()).WillByDefault(Return(allPossibleDestinationsList_[0]));
    ON_CALL(pageBasedFinisherMock1_, getPageBasedFinisher()).WillByDefault(Return(pageBasedFinisherPtr));*/

    result = ticket_.getPageBasedFinisherValidMediaSizes();
    ASSERT_EQ(std::get<0>(result), false);
}

TEST_F(GivenACopyJobTicket, WhengetPageBasedFinisherValidMediaSizesIsCalled_ThenSupportMediaSizeOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaSize>> result;

    intent->setStapleOption(dune::imaging::types::StapleOptions::LEFT_TWO_POINTS);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::NONE);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::NONE);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::NONE);

    intent->setOutputMediaIdType(dune::imaging::types::MediaIdType::ANY);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::UNDEFINED);

    result = ticket_.getPageBasedFinisherValidMediaSizes();
    ASSERT_EQ(std::get<0>(result), true);
    ASSERT_NE((std::get<1>(result)).size(), 0);
}

TEST_F(GivenACopyJobTicket, WhengetPageBasedFinisherValidMediaTypesIsCalledNoOption_ThenSupportMediaTypeOptionsAreFalseReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaType>> result;

    intent->setStapleOption(dune::imaging::types::StapleOptions::NONE);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::NONE);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::NONE);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::NONE);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::AUTOSELECT);

    result = ticket_.getPageBasedFinisherValidMediaTypes();
    ASSERT_EQ(std::get<0>(result), false);
}

TEST_F(GivenACopyJobTicket, WhengetPageBasedFinisherValidMediaTypesIsCalled_ThenSupportMediaTypeOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    ticket_.setMediaInterface(mockIMedia_);
    std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaType>> result;

    intent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    intent->setOutputMediaOrientation(MediaOrientation::PORTRAIT);
    intent->setStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANGLED);

    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN2);

    result = ticket_.getPageBasedFinisherValidMediaTypes();
    ASSERT_EQ(std::get<0>(result), true);
}

TEST_F(GivenACopyJobTicket, WhengetPageBasedFinisherValidContentOrientationIsCalledNoFinisher_ThenSupportOrientationOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    std::tuple<bool, std::vector<dune::cdm::glossary_1::ContentOrientation>> result;

    intent->setStapleOption(dune::imaging::types::StapleOptions::NONE);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::NONE);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::NONE);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::NONE);

    result = ticket_.getPageBasedFinisherValidContentOrientation();
    ASSERT_EQ(std::get<0>(result), false);    
}

TEST_F(GivenACopyJobTicket, WhengetPageBasedFinisherValidContentOrientationIsCalledNoOption_ThenSupportOrientationOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    std::tuple<bool, std::vector<dune::cdm::glossary_1::ContentOrientation>> result;

    intent->setStapleOption(dune::imaging::types::StapleOptions::NONE);
    intent->setPunchOption(dune::imaging::types::PunchingOptions::NONE);
    intent->setFoldOption(dune::imaging::types::FoldingOptions::NONE);
    intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::NONE);

    result = ticket_.getPageBasedFinisherValidContentOrientation();
    ASSERT_EQ(std::get<0>(result), false);
}

TEST_F(GivenACopyJobTicket, WhengetPageBasedFinisherValidContentOrientationIsCalled_ThenSupportOrientationOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    std::tuple<bool, std::vector<dune::cdm::glossary_1::ContentOrientation>> result;

    intent->setStapleOption(dune::imaging::types::StapleOptions::TOP_ANY_ONE_POINT_ANGLED);
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN2);

    result = ticket_.getPageBasedFinisherValidContentOrientation();
    ASSERT_EQ(std::get<0>(result), true);
}

TEST_F(GivenACopyJobTicket, WhengetOutputMediaSizeIdTypeforFinisher_OutputSizeLetterAndOrientationAreReturned)
{
    CopyJobTicket ticket;
    bool isPossibleBothOrientation = false;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);

    // Base job ticket values
    EXPECT_EQ(ticket.getType(), dune::job::JobType::COPY);
    MediaSizeId OutputMediaSizeId{dune::imaging::types::MediaSizeId::ANY};
    MediaOrientation OutputMediaOrientation{dune::imaging::types::MediaOrientation::LANDSCAPE};

    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);

    ticket.getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);

    EXPECT_EQ(OutputMediaSizeId, dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(OutputMediaOrientation, dune::imaging::types::MediaOrientation::LANDSCAPE);
    EXPECT_EQ(isPossibleBothOrientation, true);
}

TEST_F(GivenACopyJobTicket, WhengetOutputMediaSizeIdTypeforFinisher_OutputSizeA5AndOrientationAreReturned)
{
    CopyJobTicket ticket;
    bool isPossibleBothOrientation = false;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);

    // Base job ticket values
    EXPECT_EQ(ticket.getType(), dune::job::JobType::COPY);
    MediaSizeId OutputMediaSizeId{dune::imaging::types::MediaSizeId::ANY};
    MediaOrientation OutputMediaOrientation{dune::imaging::types::MediaOrientation::LANDSCAPE};
 
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A5);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);

    ticket.getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);

    EXPECT_EQ(OutputMediaSizeId, dune::imaging::types::MediaSizeId::A5);
    EXPECT_EQ(OutputMediaOrientation, dune::imaging::types::MediaOrientation::LANDSCAPE);
    EXPECT_EQ(isPossibleBothOrientation, true);
}

TEST_F(GivenACopyJobTicket, WhengetOutputMediaSizeIdTypeforFinisher_OutputSizeMixedAndOrientationAreReturned)
{
    CopyJobTicket ticket;
    bool isPossibleBothOrientation = false;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);

    // Base job ticket values
    EXPECT_EQ(ticket.getType(), dune::job::JobType::COPY);
    // TEST 1
    MediaSizeId OutputMediaSizeId{dune::imaging::types::MediaSizeId::ANY};
    MediaOrientation OutputMediaOrientation{dune::imaging::types::MediaOrientation::LANDSCAPE};

    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::SHORTEDGE);

    ticket.getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);

    EXPECT_EQ(OutputMediaSizeId, dune::imaging::types::MediaSizeId::LEDGER);
    EXPECT_EQ(OutputMediaOrientation, dune::imaging::types::MediaOrientation::PORTRAIT);
    EXPECT_EQ(isPossibleBothOrientation, false);
}

TEST_F(GivenACopyJobTicket, WhengetOutputMediaSizeIdTypeforFinisher_OutputSizeA4AndOrientationAreReturned)
{
    CopyJobTicket ticket;
    bool isPossibleBothOrientation = false;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);

    // Base job ticket values
    EXPECT_EQ(ticket.getType(), dune::job::JobType::COPY);

    MediaSizeId OutputMediaSizeId{dune::imaging::types::MediaSizeId::A4};
    MediaOrientation OutputMediaOrientation{dune::imaging::types::MediaOrientation::PORTRAIT};

    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::SHORTEDGE);

    ticket.getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);

    EXPECT_EQ(OutputMediaSizeId, dune::imaging::types::MediaSizeId::A4);
    EXPECT_EQ(OutputMediaOrientation, dune::imaging::types::MediaOrientation::PORTRAIT);
    EXPECT_EQ(isPossibleBothOrientation, true);
}

TEST_F(GivenACopyJobTicket, WhengetOutputMediaSizeIdTypeforFinisher_OutputSizeB5AndOrientationAreReturned)
{
    CopyJobTicket ticket;
    bool isPossibleBothOrientation = false;
    std::shared_ptr<ICopyJobIntent> intent = ticket.getIntent();
    ASSERT_NE(intent, nullptr);

    // Base job ticket values
    EXPECT_EQ(ticket.getType(), dune::job::JobType::COPY);

    MediaSizeId OutputMediaSizeId{dune::imaging::types::MediaSizeId::JIS_B5};
    MediaOrientation OutputMediaOrientation{dune::imaging::types::MediaOrientation::PORTRAIT};

    isPossibleBothOrientation = false;  
    intent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::SHORTEDGE);

    ticket.getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);

    EXPECT_EQ(OutputMediaSizeId, dune::imaging::types::MediaSizeId::JIS_B5);
    EXPECT_EQ(OutputMediaOrientation, dune::imaging::types::MediaOrientation::PORTRAIT);
    EXPECT_EQ(isPossibleBothOrientation, true);
}

TEST_F(GivenACopyJobTicket, WhenisValidStaplingOptionForCopyIsCalled_ThenSupportStaplingOptionsAreReturned)
{
    CopyJobTicket ticket;

    bool fResult = ticket.isValidStaplingOptionForCopy(dune::cdm::jobTicket_1::StapleOptions::topLeftOnePointAny);
    EXPECT_EQ(fResult,true);

    fResult = ticket.isValidStaplingOptionForCopy(dune::cdm::jobTicket_1::StapleOptions::leftTwoPointsAny);
    EXPECT_EQ(fResult,false);
}

TEST_F(GivenACopyJobTicket, WhengetValidStaplingOptionsIsCalled_ThenSupportStaplingOptionsAreReturned)
{
    dune::localization::StringId_Type localizationId{0};

    ON_CALL(*mockLocale_, get(testing::Matcher<StringId_Type>(_))).WillByDefault(Return("TEST String"));
    ON_CALL(*mockLocale_, getStringIdForCsfOnly(_)).WillByDefault(Return(localizationId));
    ON_CALL(*mockLocaleProvider_,deviceLocale()).WillByDefault(Return(mockLocale_));

    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::AUTOSELECT);

    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>> result;
    std::string constraintsmsg{};

    result = ticket_.getValidStaplingOptions(constraintsmsg);

    EXPECT_EQ(std::get<0>(result),APIResult::OK);
}

TEST_F(GivenACopyJobTicket, WhenisValidPunchingOptionForCopyIsCalled_ThenSupportPunchingOptionsAreReturned)
{
    CopyJobTicket ticket;

    bool fResult = ticket.isValidPunchingOptionForCopy(dune::cdm::jobTicket_1::PunchOptions::leftFourPointDin);
    EXPECT_EQ(fResult,true);

    fResult = ticket.isValidPunchingOptionForCopy(dune::cdm::jobTicket_1::PunchOptions::twoPointDin);
    EXPECT_EQ(fResult,false);

    fResult = ticket.isValidPunchingOptionForCopy(dune::cdm::jobTicket_1::PunchOptions::topThreePointUs);
    EXPECT_EQ(fResult,true);

    fResult = ticket.isValidPunchingOptionForCopy(dune::cdm::jobTicket_1::PunchOptions::fourPointSwd);
    EXPECT_EQ(fResult,false);
}

TEST_F(GivenACopyJobTicket, WhengetValidPunchingOptionsIsCalled_ThenSupportPunchingOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    dune::localization::StringId_Type localizationId{0};


    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::AUTOSELECT);

    ON_CALL(*mockLocale_, get(testing::Matcher<StringId_Type>(_))).WillByDefault(Return("TEST String"));
    ON_CALL(*mockLocale_, getStringIdForCsfOnly(_)).WillByDefault(Return(localizationId));
    ON_CALL(*mockLocaleProvider_,deviceLocale()).WillByDefault(Return(mockLocale_));

    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>> result;
    std::string constraintsmsg{};

    result = ticket_.getValidPunchingOptions(constraintsmsg);

    EXPECT_EQ(std::get<0>(result),APIResult::OK);
}

TEST_F(GivenACopyJobTicket, WhengetValidFoldingOptionsIsCalled_ThenSupportPunchingOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::AUTOSELECT);

    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>> result;
    std::string constraintsmsg{};

    result = ticket_.getValidFoldingOptions(constraintsmsg);

    EXPECT_EQ(std::get<0>(result),APIResult::OK);
}

TEST_F(GivenACopyJobTicket, WhengetPagesPerSetLimitForFinishingOptionIsCalled_ThenSheetsPerSetIsReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    std::tuple<int, int> result;

    result = ticket_.getPagesPerSetLimitForFinishingOption(dune::imaging::types::FoldingOptions::V_INWARD_TOP, dune::imaging::types::BookletMakingOptions::NONE);
    EXPECT_NE(std::get<1>(result),1);

    result = ticket_.getPagesPerSetLimitForFinishingOption(dune::imaging::types::FoldingOptions::C_INWARD_TOP, dune::imaging::types::BookletMakingOptions::NONE);
    EXPECT_NE(std::get<1>(result),1);
}

TEST_F(GivenACopyJobTicket, WhengetPagesPerSetLimitForBookletFinishingOptionIsCalled_ThenSheetsPerSetIsReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();

    std::tuple<int, int> result;

    result = ticket_.getPagesPerSetLimitForFinishingOption(dune::imaging::types::FoldingOptions::NONE, dune::imaging::types::BookletMakingOptions::SADDLE_STITCH);
    EXPECT_NE(std::get<1>(result),1);
}


TEST_F(GivenACopyJobTicket, WhengetPossibleBookletMakingOptionsIsCalled_ThenSupportBookletMakingOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::AUTOSELECT);

    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>> result;

    result = ticket_.getPossibleBookletMakingOptions();

    EXPECT_NE(std::get<0>(result),APIResult::NOT_AVAILABLE);
}

TEST_F(GivenACopyJobTicket, WhengetValidBookletMakingOptionsIsCalled_ThenSupportBookletMakingOptionsAreReturned)
{
    std::shared_ptr<ICopyJobIntent> intent = ticket_.getIntent();
    intent->setOutputDestination(dune::imaging::types::MediaDestinationId::AUTOSELECT);

    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>> result;
    std::string constraintsmsg{};

    result = ticket_.getValidBookletMakingOptions(constraintsmsg);

    EXPECT_EQ(std::get<0>(result),APIResult::OK);
}


TEST_F(GivenACopyJobTicket, WhengetValidgetValidOutputBinsIsCalled_ThenSupportgetValidOutputBinsAreReturned)
{
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>> result;

    result = ticket_.getValidOutputBins();

    EXPECT_EQ(std::get<0>(result),APIResult::OK);
}

TEST_F(GivenACopyJobTicket, WhenupdateSupportedPageBasedFinisherValidMediaSizes_WithBothA4AndLetter_ThenAddsBothRotatedVersions)
{
    CopyJobTicket ticket;
    std::vector<dune::cdm::glossary_1::MediaSize> validMediaSizesList;
    
    // Add both A4 and Letter to the list
    validMediaSizesList.push_back(dune::cdm::glossary_1::MediaSize::iso_a4_210x297mm);
    validMediaSizesList.push_back(dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in);
    
    // Call the function under test
    ticket.updateSupportedPageBasedFinisherValidMediaSizes(validMediaSizesList);
    
    // Verify that both rotated versions were added
    EXPECT_EQ(validMediaSizesList.size(), 4);
    EXPECT_TRUE(std::find(validMediaSizesList.begin(), validMediaSizesList.end(), 
                         dune::cdm::glossary_1::MediaSize::iso_a4_210x297mm) != validMediaSizesList.end());
    EXPECT_TRUE(std::find(validMediaSizesList.begin(), validMediaSizesList.end(), 
                         dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_iso_a4_210x297mm_dot_rotated) != validMediaSizesList.end());
    EXPECT_TRUE(std::find(validMediaSizesList.begin(), validMediaSizesList.end(), 
                         dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in) != validMediaSizesList.end());
    EXPECT_TRUE(std::find(validMediaSizesList.begin(), validMediaSizesList.end(), 
                         dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_na_letter_8_dot_5x11in_dot_rotated) != validMediaSizesList.end());
}

TEST_F(GivenACopyJobTicket, WhenupdateSupportedPageBasedFinisherValidMediaSizes_WithExistingRotatedVersions_ThenDoesNotAddDuplicates)
{
    CopyJobTicket ticket;
    std::vector<dune::cdm::glossary_1::MediaSize> validMediaSizesList;
    
    // Add both normal and rotated versions already
    validMediaSizesList.push_back(dune::cdm::glossary_1::MediaSize::iso_a4_210x297mm);
    validMediaSizesList.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_iso_a4_210x297mm_dot_rotated);
    
    // Call the function under test
    ticket.updateSupportedPageBasedFinisherValidMediaSizes(validMediaSizesList);
    
    // Verify no duplicates were added
    EXPECT_EQ(validMediaSizesList.size(), 2);
    EXPECT_TRUE(std::find(validMediaSizesList.begin(), validMediaSizesList.end(), 
                         dune::cdm::glossary_1::MediaSize::iso_a4_210x297mm) != validMediaSizesList.end());
    EXPECT_TRUE(std::find(validMediaSizesList.begin(), validMediaSizesList.end(), 
                         dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_iso_a4_210x297mm_dot_rotated) != validMediaSizesList.end());
}

TEST_F(GivenACopyJobTicket, WhenupdateSupportedPageBasedFinisherValidMediaSizes_WithOtherMediaSizes_ThenRemainsUnchanged)
{
    CopyJobTicket ticket;
    std::vector<dune::cdm::glossary_1::MediaSize> validMediaSizesList;
    
    // Add some other media sizes that shouldn't trigger any additions
    validMediaSizesList.push_back(dune::cdm::glossary_1::MediaSize::iso_a3_297x420mm);
    validMediaSizesList.push_back(dune::cdm::glossary_1::MediaSize::na_legal_8_dot_5x14in);
    
    // Call the function under test
    ticket.updateSupportedPageBasedFinisherValidMediaSizes(validMediaSizesList);
    
    // Verify list remains unchanged
    EXPECT_EQ(validMediaSizesList.size(), 2);
    EXPECT_TRUE(std::find(validMediaSizesList.begin(), validMediaSizesList.end(), 
                         dune::cdm::glossary_1::MediaSize::iso_a3_297x420mm) != validMediaSizesList.end());
    EXPECT_TRUE(std::find(validMediaSizesList.begin(), validMediaSizesList.end(), 
                         dune::cdm::glossary_1::MediaSize::na_legal_8_dot_5x14in) != validMediaSizesList.end());
}

struct CopyJobIntentMarginLayoutParameterizedTestStruct
{
    public:
        ScanScaleSelectionEnum scaleSelection_      ;
        MediaSizeId            inputMediaSizeId_    ;
        MediaSizeId            outputMediaSizeId_   ;
        int64_t                xScalePercent_       ;
        int64_t                yScalePercent_       ;
        MarginLayout           defaultMarginLayout_ ;
        MarginLayout           expectedMarginLayout_;
};



class GivenACopyJobIntentParameterizedForMarginLayout : public ::testing::TestWithParam<CopyJobIntentMarginLayoutParameterizedTestStruct>
{
    public:
        GivenACopyJobIntentParameterizedForMarginLayout();

    protected:
        CopyJobIntent intent_;
        MarginLayout defaultMarginLayout_;
        MarginLayout expectedMarginLayout_;
};



GivenACopyJobIntentParameterizedForMarginLayout::GivenACopyJobIntentParameterizedForMarginLayout()
{
    auto param = GetParam();

    intent_.setScaleSelection(param.scaleSelection_);
    intent_.setInputMediaSizeId(param.inputMediaSizeId_);
    intent_.setOutputMediaSizeId(param.outputMediaSizeId_);
    intent_.setXScalePercent(param.xScalePercent_);
    intent_.setYScalePercent(param.yScalePercent_);

    defaultMarginLayout_ = param.defaultMarginLayout_;
    expectedMarginLayout_ = param.expectedMarginLayout_;
};



TEST_P(GivenACopyJobIntentParameterizedForMarginLayout, WhenDeterminingMarginLayoutOrDefault)
{
    MarginLayout resultantMarginLayout = intent_.determineMarginLayoutOrDefault(defaultMarginLayout_);
    EXPECT_EQ(resultantMarginLayout, expectedMarginLayout_) << "Expected " << EnumNameMarginLayout(expectedMarginLayout_) << " but got " << EnumNameMarginLayout(resultantMarginLayout) << "\n";
};



INSTANTIATE_TEST_CASE_P
(
    ,
    GivenACopyJobIntentParameterizedForMarginLayout,
    ::testing::Values
    (
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::NONE, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::STANDARD, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::NONE, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::OVERSIZE, MarginLayout::OVERSIZE},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::NONE, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::CLIPINSIDE},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::NONE, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::ADDTOCONTENTS, MarginLayout::ADDTOCONTENTS},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::FITTOPAGE, MediaSizeId::A4, MediaSizeId::LETTER, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::FITTOPAGE, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::CLIPINSIDE},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::FITTOPAGE, MediaSizeId::LETTER, MediaSizeId::LETTER, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::CLIPINSIDE},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::FULLPAGE, MediaSizeId::A4, MediaSizeId::LETTER, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::FULLPAGE, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::CLIPINSIDE},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::FULLPAGE, MediaSizeId::LETTER, MediaSizeId::LETTER, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::CLIPINSIDE},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::CUSTOM, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::CLIPINSIDE},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::CUSTOM, MediaSizeId::A4, MediaSizeId::A4, 50, 100, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::CUSTOM, MediaSizeId::A4, MediaSizeId::A4, 100, 50, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::CUSTOM, MediaSizeId::A4, MediaSizeId::A4, 50, 50, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::CUSTOM, MediaSizeId::A4, MediaSizeId::A4, 200, 200, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::SCALE_TO_OUTPUT, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::LEGALTOLETTER, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::A4TOLETTER, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD},
        CopyJobIntentMarginLayoutParameterizedTestStruct{ScanScaleSelectionEnum::LETTERTOA4, MediaSizeId::A4, MediaSizeId::A4, 100, 100, MarginLayout::CLIPINSIDE, MarginLayout::STANDARD}
    ),
    [] (const ::testing::TestParamInfo<CopyJobIntentMarginLayoutParameterizedTestStruct>& info) -> std::string
    {
        std::stringstream name;
        name << info.index;
        name << "_WithMarginLayout";
        name << EnumNameMarginLayout(info.param.defaultMarginLayout_);
        name << "AndScaleSelection";
        name << EnumNameScanScaleSelectionEnum(info.param.scaleSelection_);
        name << EnumNameMediaSizeId(info.param.inputMediaSizeId_);
        name << "To";
        name << EnumNameMediaSizeId(info.param.outputMediaSizeId_);
        name << ((info.param.xScalePercent_ == 100 && info.param.yScalePercent_ == 100) ? "" : "AndCustomScalePercent");
        name << "_ThenTheResultIs";
        name << EnumNameMarginLayout(info.param.expectedMarginLayout_);
        return name.str();
    }
);


struct CopyJobIntentBorderlessParameterizedTestStruct
{
    public:
        MediaSizeId         inputMediaSizeId_   ;
        MediaSizeId         outputMediaSizeId_  ;
        int64_t             xScalePercent_      ;
        int64_t             yScalePercent_      ;
        MediaIdType         outputMediaIdType_  ;
        bool                is2up_;
        bool                expectedBorderless_ ;
};



class GivenACopyJobTicketWithCopyJobIntentParameterizedForBorderless : public GivenACopyJobTicket,
                                                                       public ::testing::WithParamInterface<CopyJobIntentBorderlessParameterizedTestStruct>
{
    public:
        void SetUp();

    protected:
        bool expectedBorderless_;
};



void GivenACopyJobTicketWithCopyJobIntentParameterizedForBorderless::SetUp()
{
    GivenACopyJobTicket::SetUp();
    auto param = GetParam();

    std::shared_ptr<MockICopyJobIntent> intent = std::make_shared<MockICopyJobIntent>();

    ON_CALL(*intent, getInputMediaSizeId())
        .WillByDefault(Return(param.inputMediaSizeId_));
    ON_CALL(*intent, getXScalePercent())
        .WillByDefault(Return(param.xScalePercent_));
    ON_CALL(*intent, getYScalePercent())
        .WillByDefault(Return(param.yScalePercent_));
    ON_CALL(*intent, getOutputMediaSizeId())
        .WillByDefault(Return(param.outputMediaSizeId_));
    ON_CALL(*intent, getOutputMediaIdType())
        .WillByDefault(Return(param.outputMediaIdType_));

    if (param.is2up_)
    {
        ON_CALL(*intent, getPagesPerSheet())
                .WillByDefault(Return(dune::imaging::types::CopyOutputNumberUpCount::TwoUp));
    }

    ticket_.setIntent(std::static_pointer_cast<ICopyJobIntent>(intent));

    TestConfigurationService configService;
    configService.setBehaviour("./testResources/MediaSimulatorConfig.fbs", "./testResources/MediaSimulator.json", "testResources", 0);
    ConfigurationRawData rawConfig = configService.getConfiguration(0, "EngineSimulatorMedia");

    ASSERT_NE(nullptr, rawConfig.data.get()) << "Unable to load test resources for configuration";
    std::unique_ptr<MediaSimulatorConfigT> config = dune::print::engine::simulator::UnPackMediaSimulatorConfig(rawConfig.data.get());

    ASSERT_TRUE(config->inputDevicesPresent) << "Unable to load input devices from given config";
    ASSERT_TRUE(config->inputDevices.size() > 0) << "No input devices found in the given config";

    IMedia::InputList mockIInputList;
    for (auto it = config->inputDevices.cbegin(); it != config->inputDevices.cend(); it++)
    {
        const InputDeviceT * inputDevice = it->get();
        ASSERT_NE(nullptr, inputDevice) << "Device with nullptr loaded";
        const TrayT * tray = inputDevice->subType.AsTray();
        ASSERT_NE(nullptr, tray) << "Could not get an input device as a tray";

        IMedia::FullBleedConstraints fullBleedConstraints;
        bool hasFullBleedSupportConstraints = tray->hasFullBleedSupportConstraints;
        if (hasFullBleedSupportConstraints)
        {
            fullBleedConstraints = MediaHelper::deSerializeFullBleedConstraintsFbs(*(tray->fullBleedSupportConstraints));
        }
        std::shared_ptr<MockIMediaIInput> mockIInput = std::make_shared<MockIMediaIInput>();
        ON_CALL(*mockIInput, getFullBleedSupport())
            .WillByDefault(Return(std::make_tuple<bool, const IMedia::FullBleedConstraints&>(std::move(hasFullBleedSupportConstraints), fullBleedConstraints)));
        mockIInputList.push_back(mockIInput);
    }

    std::tuple<APIResult, IMedia::InputList> getInputDevicesResult(std::make_tuple(APIResult::OK, mockIInputList));
    ON_CALL(*mockIMedia_, getInputDevices(_))
        .WillByDefault(Return(getInputDevicesResult));

    expectedBorderless_ = param.expectedBorderless_;
};



TEST_P(GivenACopyJobTicketWithCopyJobIntentParameterizedForBorderless, WhenDeterminingBorderless)
{
    bool isBorderless = ticket_.shouldBeBorderless();
    EXPECT_EQ(isBorderless, expectedBorderless_);
};



INSTANTIATE_TEST_CASE_P
(
    ,
    GivenACopyJobTicketWithCopyJobIntentParameterizedForBorderless,
    ::testing::Values
    (
        //                                             inputMediaSizeId       outputMediaSizeId      x%   y%   outputMediaIdType        is2up  expectedBorderless
        CopyJobIntentBorderlessParameterizedTestStruct{MediaSizeId::LETTER,   MediaSizeId::LETTER,   100, 100, MediaIdType::STATIONERY, false, false},
        CopyJobIntentBorderlessParameterizedTestStruct{MediaSizeId::LETTER,   MediaSizeId::LETTER,   100, 100, MediaIdType::OTHERPHOTO, false, true},
        CopyJobIntentBorderlessParameterizedTestStruct{MediaSizeId::LETTER,   MediaSizeId::LETTER,   100, 100, MediaIdType::OTHERPHOTO, false, true},
        CopyJobIntentBorderlessParameterizedTestStruct{MediaSizeId::PHOTO4X6, MediaSizeId::LETTER,   400, 400, MediaIdType::OTHERPHOTO, false, true},
        CopyJobIntentBorderlessParameterizedTestStruct{MediaSizeId::PHOTO4X6, MediaSizeId::LETTER,   100, 100, MediaIdType::OTHERPHOTO, false, false},
        CopyJobIntentBorderlessParameterizedTestStruct{MediaSizeId::LETTER,   MediaSizeId::PHOTO4X6, 100, 100, MediaIdType::OTHERPHOTO, false, true},
        CopyJobIntentBorderlessParameterizedTestStruct{MediaSizeId::LETTER,   MediaSizeId::PHOTO4X6,  25,  25, MediaIdType::OTHERPHOTO, false, false},
        CopyJobIntentBorderlessParameterizedTestStruct{MediaSizeId::LETTER,   MediaSizeId::PHOTO4X6, 100, 100, MediaIdType::OTHERPHOTO, true, false},
        CopyJobIntentBorderlessParameterizedTestStruct{MediaSizeId::LETTER,   MediaSizeId::LETTER,   100, 100, MediaIdType::OTHERPHOTO, true, false}
    ),
    [] (const ::testing::TestParamInfo<CopyJobIntentBorderlessParameterizedTestStruct>& info) -> std::string
    {
        std::stringstream name;
        name << info.index;
        name << "_With";
        name << EnumNameMediaSizeId(info.param.inputMediaSizeId_);
        name << "To";
        name << EnumNameMediaSizeId(info.param.outputMediaSizeId_);
        name << "ScaledAt";
        name << info.param.xScalePercent_;
        name << "PercentOn";
        name << EnumNameMediaIdType(info.param.outputMediaIdType_);
        name << (info.param.is2up_ ? "2up" : "");
        name << "Paper_ThenTheResultShould";
        name << (info.param.expectedBorderless_ ? "" : "Not");
        name << "BeBorderless";
        return name.str();
    }
);

struct CopyJobIntentRotate180ParameterizedTestStruct
{
    public:
        dune::scan::types::ScanSource           scanSource_;
        ContentOrientation                      contentOrientation_;
        dune::scan::types::ScanFeedOrientation  scanFeedOrientation_;
        CopyOutputNumberUpCount                 nupSettings_;
        bool                                    expectedRotate180_;

};

class GivenACopyJobTicketWithCopyJobIntentParameterizedForRotate180 : public GivenACopyJobTicket,
                                                                       public ::testing::WithParamInterface<CopyJobIntentRotate180ParameterizedTestStruct>
{
    public:
        void SetUp();

    protected:
        bool expectedRotate180_;
};

void GivenACopyJobTicketWithCopyJobIntentParameterizedForRotate180::SetUp()
{
    GivenACopyJobTicket::SetUp();
    auto param = GetParam();

    ticket_.setEarlyCopyJob(true);
    ticket_.getIntent()->setPagesPerSheet(param.nupSettings_);
    ticket_.getIntent()->setScanSource(param.scanSource_);
    ticket_.getIntent()->setContentOrientation(param.contentOrientation_);
    ticket_.getIntent()->setScanFeedOrientation(param.scanFeedOrientation_);
    ticket_.setPrePrintConfiguration(dune::copy::Jobs::Copy::Product::ENTERPRISE);

    expectedRotate180_ = param.expectedRotate180_;
}

TEST_P(GivenACopyJobTicketWithCopyJobIntentParameterizedForRotate180, WhenDeterminingRotate180)
{
    Uuid pageId{Uuid::createUuid()};
    std::shared_ptr<dune::job::IPageTicket> pageTicket = ticket_.addPage(pageId);
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent = std::static_pointer_cast<dune::print::engine::PrintIntents>(pageTicket->getIntent(dune::job::IntentType::PRINT));

    bool rotate180;
    printIntent->getValue(dune::print::engine::PrintIntentFieldType::ROTATE_180 , rotate180);
    EXPECT_EQ(rotate180, expectedRotate180_);
};

INSTANTIATE_TEST_CASE_P(InstantiationName
    , GivenACopyJobTicketWithCopyJobIntentParameterizedForRotate180,
    ::testing::Values(
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::ADF_SIMPLEX, ContentOrientation::PORTRAIT, dune::scan::types::ScanFeedOrientation::SHORTEDGE , dune::imaging::types::CopyOutputNumberUpCount::OneUp, false},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::ADF_SIMPLEX, ContentOrientation::PORTRAIT, dune::scan::types::ScanFeedOrientation::SHORTEDGE, dune::imaging::types::CopyOutputNumberUpCount::TwoUp, true},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::ADF_SIMPLEX, ContentOrientation::PORTRAIT, dune::scan::types::ScanFeedOrientation::LONGEDGE, dune::imaging::types::CopyOutputNumberUpCount::OneUp, false},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::ADF_SIMPLEX, ContentOrientation::PORTRAIT, dune::scan::types::ScanFeedOrientation::LONGEDGE, dune::imaging::types::CopyOutputNumberUpCount::TwoUp, true},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::ADF_SIMPLEX, ContentOrientation::LANDSCAPE, dune::scan::types::ScanFeedOrientation::SHORTEDGE, dune::imaging::types::CopyOutputNumberUpCount::OneUp, true}, // actual case
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::ADF_SIMPLEX, ContentOrientation::LANDSCAPE, dune::scan::types::ScanFeedOrientation::SHORTEDGE, dune::imaging::types::CopyOutputNumberUpCount::TwoUp, false},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::ADF_DUPLEX, ContentOrientation::LANDSCAPE, dune::scan::types::ScanFeedOrientation::SHORTEDGE, dune::imaging::types::CopyOutputNumberUpCount::OneUp, true}, //actual case
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::GLASS, ContentOrientation::LANDSCAPE, dune::scan::types::ScanFeedOrientation::SHORTEDGE, dune::imaging::types::CopyOutputNumberUpCount::TwoUp, true},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::GLASS, ContentOrientation::PORTRAIT, dune::scan::types::ScanFeedOrientation::LONGEDGE , dune::imaging::types::CopyOutputNumberUpCount::OneUp, true},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::GLASS, ContentOrientation::PORTRAIT, dune::scan::types::ScanFeedOrientation::LONGEDGE , dune::imaging::types::CopyOutputNumberUpCount::TwoUp, false}, //actual case
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::GLASS, ContentOrientation::PORTRAIT, dune::scan::types::ScanFeedOrientation::SHORTEDGE, dune::imaging::types::CopyOutputNumberUpCount::OneUp, false},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::GLASS, ContentOrientation::PORTRAIT, dune::scan::types::ScanFeedOrientation::SHORTEDGE, dune::imaging::types::CopyOutputNumberUpCount::TwoUp, true},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::GLASS, ContentOrientation::LANDSCAPE, dune::scan::types::ScanFeedOrientation::LONGEDGE , dune::imaging::types::CopyOutputNumberUpCount::OneUp, false},
        CopyJobIntentRotate180ParameterizedTestStruct{dune::scan::types::ScanSource::GLASS, ContentOrientation::LANDSCAPE, dune::scan::types::ScanFeedOrientation::LONGEDGE , dune::imaging::types::CopyOutputNumberUpCount::TwoUp, true}

    )
);

// Tests for isRestrictColorPrint method
TEST_F(GivenACopyJobTicket, WhenColorAccessControlIsNull_ThenColorPrintingIsNotRestricted)
{
    // Arrange
    ticket_.setColorAccessControlInterface(nullptr);
    
    // Act
    bool isRestricted = ticket_.isRestrictColorPrint();
    
    // Assert
    EXPECT_FALSE(isRestricted) << "Color printing should not be restricted when color access control interface is null";
}

TEST_F(GivenACopyJobTicket, WhenColorAccessIsEnabled_ThenColorPrintingIsNotRestricted)
{
    // Arrange
    EXPECT_CALL(*mockColorAccessControl_, getColorAccess())
        .WillOnce(::testing::Return(dune::imaging::ColorAccess::ENABLED));
    
    // Act
    bool isRestricted = ticket_.isRestrictColorPrint();
    
    // Assert
    EXPECT_FALSE(isRestricted) << "Color printing should not be restricted when color access is enabled";
}

TEST_F(GivenACopyJobTicket, WhenColorAccessIsDisabled_ThenColorPrintingIsRestricted)
{
    // Arrange
    EXPECT_CALL(*mockColorAccessControl_, getColorAccess())
        .WillOnce(::testing::Return(dune::imaging::ColorAccess::DISABLED));
    
    // Act
    bool isRestricted = ticket_.isRestrictColorPrint();
    
    // Assert
    EXPECT_TRUE(isRestricted) << "Color printing should be restricted when color access is disabled";
}

TEST_F(GivenACopyJobTicket, WhenColorAccessIsUnknown_ThenColorPrintingIsNotRestricted)
{
    // Arrange - Test with an unknown/undefined color access value
    EXPECT_CALL(*mockColorAccessControl_, getColorAccess())
        .WillOnce(::testing::Return(static_cast<dune::imaging::ColorAccess>(999))); // Unknown value
    
    // Act
    bool isRestricted = ticket_.isRestrictColorPrint();
    
    // Assert
    EXPECT_FALSE(isRestricted) << "Color printing should not be restricted when color access is unknown";
}

TEST_F(GivenACopyJobTicket, WhenMultipleCallsAreMadeToIsRestrictColorPrint_ThenEachCallQueriesColorAccessControl)
{
    // Arrange
    EXPECT_CALL(*mockColorAccessControl_, getColorAccess())
        .Times(3)
        .WillOnce(::testing::Return(dune::imaging::ColorAccess::ENABLED))
        .WillOnce(::testing::Return(dune::imaging::ColorAccess::DISABLED))
        .WillOnce(::testing::Return(dune::imaging::ColorAccess::ENABLED));
    
    // Act & Assert
    EXPECT_FALSE(ticket_.isRestrictColorPrint()) << "First call: should not be restricted when enabled";
    EXPECT_TRUE(ticket_.isRestrictColorPrint()) << "Second call: should be restricted when disabled";
    EXPECT_FALSE(ticket_.isRestrictColorPrint()) << "Third call: should not be restricted when enabled";
}
