/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobTicket.cpp
 * @date   Wed, 08 May 2019 11:36:41 -0700
 * @brief  Copy Job Ticket
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "common_debug.h"
#include "CopyJobTicket.h"
#include "CopyJobTicket_TraceAutogen.h"

#include "StringIds.h"
#include "MediaCdmHelper.h"
#include "ConvertToScanTypeHelper.h"
#include "IScanJobConstraint.h"
#include "IPageTicket.h"
#include "PrintArea_generated.h"
#include "Uuid.h"
#include "ImagingUtilities.h"
#include "MarginSettings_generated.h"
#include "Borderless_generated.h"
#include "IMedia.h"
#include "MediaSize.h"
#include "MediaType_generated.h"
#include "MediaId.h"
#include <fstream>
#include "FlatbufferHelper.h"
#include "typeMappers.h"
#include "FinishingOptions_generated.h"
#include "IPrintIntentsFactory.h"
#include "ICapabilities.h"
#include "ILocaleProvider.h"
#include "ILocale.h"

using Distance = dune::imaging::types::Distance;
using IPageTicket = dune::job::IPageTicket;
using ConvertToScanTypeHelper = dune::scan::types::ConvertToScanTypeHelper;
using IMedia = dune::print::engine::IMedia;
using MediaSize = dune::imaging::types::MediaSize;
using MediaIdType = dune::imaging::types::MediaIdType;
using MediaId = dune::imaging::types::MediaId;
using FinishingContentOrientation = dune::imaging::types::FinishingContentOrientation;
using MediaProcessingTypes = dune::imaging::types::MediaProcessingTypes;
using StapleOptions = dune::imaging::types::StapleOptions;
using PunchingOptions = dune::imaging::types::PunchingOptions;
using FoldingOptions = dune::imaging::types::FoldingOptions;
using BookletMakingOptions = dune::imaging::types::BookletMakingOptions;
using OrientedMediaSize = dune::imaging::types::OrientedMediaSize;
using MediaDestinationId = dune::imaging::types::MediaDestinationId;
using MediaOrientation = dune::imaging::types::MediaOrientation;
using ScanSource = dune::scan::types::ScanSource;
using ScanFeedOrientation = dune::scan::types::ScanFeedOrientation;
using ContentOrientation = dune::imaging::types::ContentOrientation;
using MediaSizeId =  dune::imaging::types::MediaSizeId;
using PlexBinding = dune::imaging::types::PlexBinding;

namespace dune { namespace copy { namespace Jobs { namespace Copy {

constexpr int32_t FOLDING_STYLE_FOLDER_DEFAULT = 2;
constexpr int32_t FOLDING_STYLE_MIN_ALLOWED_ID = 256;
constexpr int32_t FOLDING_STYLE_MAX_ALLOWED_ID = 65535;

/**
 * @brief Construct a new Copy Job Intent:: Copy Job Intent object
 *
 */
CopyJobIntent::CopyJobIntent()
{
}

void CopyJobIntent::dumpIntentToLog()
{
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() outputMediaSizeId_ %d", static_cast<int>(getOutputMediaSizeId()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() outputMediaOrientation_ %d", static_cast<int>(getOutputMediaOrientation()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() outputMediaIdType_ %d", static_cast<int>(getOutputMediaIdType()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() outputMediaSource_ %d", static_cast<int>(getOutputMediaSource()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() outputPlexMode_ %d", static_cast<int>(getOutputPlexMode()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() outputPlexBinding_ %d", static_cast<int>(getOutputPlexBinding()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() foldingStyle %d", static_cast<short>(getFoldingStyleId()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() copies_ %d", static_cast<int>(getCopies()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() collate_ %d", static_cast<int>(getCollate()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() copyQuality_ %d", static_cast<int>(getCopyQuality()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() resize_ %d", static_cast<int>(getResize()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() lighterDarker_ %d", static_cast<int>(getLighterDarker()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() copyMargins_ %d", static_cast<int>(getCopyMargins()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() outputDestination_ %d", static_cast<int>(getOutputDestination()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() plexSide_ %d", static_cast<int>(getPlexSide()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() requestedPages_ %d", static_cast<int>(getRequestedPages()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() printingOrder_ %d", static_cast<int>(getPrintingOrder()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() rotation_ %d", static_cast<int>(getRotation()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() autoRotate_ %d", static_cast<int>(getAutoRotate()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() mediaFamily_ %d", static_cast<int>(getMediaFamily()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() stapleOption_ %d", static_cast<int>(getStapleOption()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() punchOption_ %d", static_cast<int>(getPunchOption()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() jobOffsetMode_ %d", static_cast<int>(getJobOffsetMode()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() foldOption_ %d", static_cast<int>(getFoldOption()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() SheetsPerSetForCFold_ %d", static_cast<int>(getSheetsPerSetForCFold()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() SheetsPerSetForVFold_ %d", static_cast<int>(getSheetsPerSetForVFold()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() bookletMakerOption_ %d", static_cast<int>(getBookletMakerOption()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() SheetsPerSetForFoldAndStitch_ %d", static_cast<int>(getSheetsPerSetForFoldAndStitch()));
    CHECKPOINTC("CopyJobIntent::dumpIntentToLog() deviceSetsFoldAndStitchSheetsEnabled_ %d", static_cast<int>(getDeviceSetsFoldAndStitchSheetsEnabled()));
}

MarginLayout CopyJobIntent::determineMarginLayoutOrDefault(MarginLayout defaultMarginLayout) const
{
    CHECKPOINTD("CopyJobIntent::determineMarginLayoutOrDefault - Enter");
    MarginLayout returnValue = defaultMarginLayout;

    const auto intentScaleSelection = this->getScaleSelection();

    bool hasFittingOutputScale = (
                                     intentScaleSelection == dune::scan::types::ScanScaleSelectionEnum::FITTOPAGE ||
                                     intentScaleSelection == dune::scan::types::ScanScaleSelectionEnum::FULLPAGE
                                 ) &&
                                 this->getInputMediaSizeId() != this->getOutputMediaSizeId();

    bool hasCustomOutputScale  = intentScaleSelection == dune::scan::types::ScanScaleSelectionEnum::CUSTOM &&
                                 (this->getXScalePercent() != 100 || this->getYScalePercent() != 100);

    bool hasScaleToSize        = intentScaleSelection == dune::scan::types::ScanScaleSelectionEnum::SCALE_TO_OUTPUT ||
                                 intentScaleSelection == dune::scan::types::ScanScaleSelectionEnum::LEGALTOLETTER ||
                                 intentScaleSelection == dune::scan::types::ScanScaleSelectionEnum::A4TOLETTER ||
                                 intentScaleSelection == dune::scan::types::ScanScaleSelectionEnum::LETTERTOA4;

    bool twoupEnabled          = this->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp;


    if (hasFittingOutputScale || hasCustomOutputScale || hasScaleToSize || twoupEnabled)
    {
        returnValue = MarginLayout::STANDARD;
    }

    CHECKPOINTD("CopyJobIntent::determineMarginLayoutOrDefault - Exit with value %d", returnValue);
    return returnValue;
};



bool CopyJobTicket::shouldBeBorderless() const
{
    CHECKPOINTD("CopyJobTicket::shouldBeBorderless - Enter");


    auto orientation = dune::imaging::types::MediaOrientation::PORTRAIT;
    if (copyJobIntent_->getScanFeedOrientation() == dune::scan::types::ScanFeedOrientation::LONGEDGE)
    {
        orientation = dune::imaging::types::MediaOrientation::LANDSCAPE;
    }

    auto inputWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(copyJobIntent_->getInputMediaSizeId(), orientation);
    auto outputWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(copyJobIntent_->getOutputMediaSizeId(), orientation);

    float xScaleCoefficient = copyJobIntent_->getXScalePercent() / 100.0;
    float yScaleCoefficient = copyJobIntent_->getYScalePercent() / 100.0;

    bool isInputMediaBigEnough{true};
    if (inputWidthAndHeight.width  * xScaleCoefficient < outputWidthAndHeight.width ||
        inputWidthAndHeight.height * yScaleCoefficient < outputWidthAndHeight.height)
    {
        CHECKPOINTC("CopyJobTicket::shouldBeBorderless - Borderless disabled due to output media being larger than input image");
        isInputMediaBigEnough = false;
    }


    MediaId outputMediaId(copyJobIntent_->getOutputMediaIdType());
    MediaSize outputMediaSize(copyJobIntent_->getOutputMediaSizeId());

    bool outputMediaHasFullBleedSupport{false};
    std::tuple<APIResult, IMedia::InputList> inputDevicesResult = mediaInterface_->getInputDevices();
    if (std::get<0>(inputDevicesResult) == APIResult::OK)
    {
        IMedia::InputList inputDevices = std::get<1>(inputDevicesResult);
        for (IMedia::InputPtr inputDevicePtr : inputDevices)
        {
            std::tuple<bool, IMedia::FullBleedConstraints> fullBleedConstraintsResult = inputDevicePtr->getFullBleedSupport();
            if (std::get<0>(fullBleedConstraintsResult))
            {
                IMedia::FullBleedConstraints fullBleedConstraints = std::get<1>(fullBleedConstraintsResult);

                const std::vector<MediaId> supportedTypes = fullBleedConstraints.getSupportedIds();
                bool mediaTypeSupported = std::find(supportedTypes.cbegin(), supportedTypes.cend(), outputMediaId) != supportedTypes.cend();

                const std::vector<MediaSize> supportedSizes = fullBleedConstraints.getSupportedSizes();
                bool mediaSizeSupported = std::find(supportedSizes.cbegin(), supportedSizes.cend(), outputMediaSize) != supportedSizes.cend();

                if (mediaTypeSupported && mediaSizeSupported)
                {
                    CHECKPOINTC("CopyJobTicket::shouldBeBorderless - Borderless is supported for current media type and size");
                    outputMediaHasFullBleedSupport = true;
                    break;
                }
            }
        }
    }


    bool isBorderless = isInputMediaBigEnough &&
                        outputMediaHasFullBleedSupport &&
                        copyJobIntent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::TwoUp;
    CHECKPOINTD("CopyJobTicket::shouldBeBorderless - Exit with bool value: %d", isBorderless);
    return isBorderless;
};



/**
 * @brief Construct a new Copy Job Ticket:: Copy Job Ticket object
 *
 */
CopyJobTicket::CopyJobTicket(dune::framework::core::ThreadPool* threadPool)
    : JobTicket(),
      printIntentsFactory_{nullptr},
      threadPool_{threadPool},
      copyJobIntent_{std::make_shared<CopyJobIntent>()},
      copyJobResult_{std::make_shared<CopyJobResult>()},
      copyJobConstraints_{std::make_shared<CopyJobConstraint>()},
      handler_{nullptr},
      copyTicketMutex_{}
{
    CHECKPOINTD("CopyJobTicket::CopyJobTicket() threadPool: %p", threadPool_);
    setType(dune::job::JobType::COPY);

    handler_ = std::make_shared<CopyJobTicketHandler>(
        *this, CopyJobTicketHandler::JobTicketEvents{jobTicketChanged_, jobTicketPageChanged_}, threadPool_);
}
CopyJobTicket::CopyJobTicket(const CopyJobTicket& oldCopyJobTicket)
    : JobTicket(oldCopyJobTicket), threadPool_{oldCopyJobTicket.threadPool_}, handler_{nullptr}, copyTicketMutex_{}
{
    CHECKPOINTD("CopyJobTicket::CopyJobTicket clone() threadPool: %p", threadPool_);
    std::shared_ptr<CopyJobIntent> oldCopyJobIntent = std::static_pointer_cast<CopyJobIntent>(oldCopyJobTicket.getIntent());
    copyJobIntent_ = std::make_shared<CopyJobIntent>(*oldCopyJobIntent);
    std::shared_ptr<CopyJobResult> oldCopyJobResult = std::static_pointer_cast<CopyJobResult>(oldCopyJobTicket.getResult());
    copyJobResult_ = std::make_shared<CopyJobResult>(*oldCopyJobResult);
    intentsManager_ = oldCopyJobTicket.getIntentsManager();
    copyJobConstraints_ = std::make_shared<CopyJobConstraint>();
    mediaInterface_ = oldCopyJobTicket.getMediaInterface();
    mediaInfoPtr_ = oldCopyJobTicket.getMediaInfoInterface();
    scanMediaInterface_ = oldCopyJobTicket.getScanMediaInterface();
    scanCapabilitiesInterface_ = oldCopyJobTicket.getScanCapabilitiesInterface();
    nvramInterface_ = oldCopyJobTicket.getNvramInterface();
    localization_ = oldCopyJobTicket.getLocalizationInterface();
    prePrintConfiguration_ = oldCopyJobTicket.getPrePrintConfiguration();
    maxLengthConfig_ = oldCopyJobTicket.getMaxLengthConfig();
    version_ = oldCopyJobTicket.getVersion();
    colorAccessControl_ = oldCopyJobTicket.getColorAccessControlInterface();
    isMediaTypeVisibilityTogglingSupported_ = oldCopyJobTicket.isMediaTypeVisibilityTogglingSupported();

    if (cloneIsARerun(oldCopyJobTicket) || cloneIsARetrieve(oldCopyJobTicket))
    {
        for (const auto pageTicket : oldCopyJobTicket.copyPageTickets_)
        {
            CHECKPOINTA("CopyJobTicket:: Rerun clone page Ticket ");
            copyPageTickets_.emplace_back(pageTicket->clone(true)); // never copy results
        }

        // when cloning a ticket for reprint or retieve,... reset old results
        copyJobResult_ = std::make_shared<CopyJobResult>(); 
    }

    populateDefaultConstraints();

    handler_ = std::make_shared<CopyJobTicketHandler>(
        *this, CopyJobTicketHandler::JobTicketEvents{jobTicketChanged_, jobTicketPageChanged_}, threadPool_);
}



void CopyJobTicket::populateDefaultConstraints()
{
    if(dune::copy::Jobs::Copy::constraintsFb_  != nullptr)
    {
        setConstraintsFromFb(dune::copy::Jobs::Copy::constraintsFb_ );
    }
    else
    {
        CHECKPOINTA("CopyJobTicket::populateDefaultConstraints(): Error!!! Config is null. Did not set default constraints on CopyJobTicket.");
    }
}
std::unique_ptr<CopyJobIntentFbT> serializeCopyJobIntent(std::shared_ptr<ICopyJobIntent> intent)
{
    auto data = std::make_unique<CopyJobIntentFbT>();
    if (intent)
    {
        data->outputMediaSizeId = intent->getOutputMediaSizeId();
        data->outputMediaOrientation = intent->getOutputMediaOrientation();
        data->outputMediaIdType = intent->getOutputMediaIdType();
        data->outputMediaSource = intent->getOutputMediaSource();
        data->outputPlexMode = intent->getOutputPlexMode();
        data->foldingStyleId = intent->getFoldingStyleId();
        data->copyMargins = intent->getCopyMargins();
        data->outputPlexBinding = intent->getOutputPlexBinding();
        data->copies = intent->getCopies();
        data->collate = intent->getCollate();
        data->copyQuality = intent->getCopyQuality();
        data->outputMediaDestination = intent->getOutputDestination();
        data->scanJobIntent = std::move(dune::scan::Jobs::Scan::serializeScanJobIntent(intent));
        data->printingOrder = intent->getPrintingOrder();
        data->rotation = intent->getRotation();
        data->autoRotate = intent->getAutoRotate();
        data->mediaFamily = intent->getMediaFamily();
        data->customMediaXDimension = intent->getCustomMediaXDimension();
        data->customMediaYDimension = intent->getCustomMediaYDimension();
        using StaplingOption = decltype(data->stapleOption);
        data->stapleOption = static_cast<StaplingOption>(intent->getStapleOption());
        using PunchingOption = decltype(data->punchOption);
        data->punchOption = static_cast<PunchingOption>(intent->getPunchOption());
        data->jobOffset = intent->getJobOffsetMode();
        data->foldOption = intent->getFoldOption();
        data->cFoldSheets = intent->getSheetsPerSetForCFold();
        data->vFoldSheets = intent->getSheetsPerSetForVFold();
        data->bookletMakerOption = intent->getBookletMakerOption();
        data->foldAndStitchSheets = intent->getSheetsPerSetForFoldAndStitch();
        data->deviceSetsFoldAndStitchSheetsEnabled = intent->getDeviceSetsFoldAndStitchSheetsEnabled();
    }
    return data;
}
std::unique_ptr<dune::job::JobTicketFbT> serializeJobTicket(std::shared_ptr<dune::job::IJobTicket> ticket)
{
    auto jobFbT = std::make_unique<dune::job::JobTicketFbT>();
    if (ticket) {
        jobFbT->name = "";
        jobFbT->jobId.reset(new dune::framework::core::uuid::fbs::Uuid(ticket->getJobId()));
        jobFbT->ordinal = ticket->getOrdinal();
        jobFbT->state = ticket->getState();
        jobFbT->storePath = ticket->getStorePath().c_str();
        jobFbT->priority = ticket->getPriority();
        jobFbT->completionState = ticket->getCompletionState();
    }
    return jobFbT;
}
std::unique_ptr<CopyJobTicketFbT> serializeCopyJobTicket(std::shared_ptr<ICopyJobTicket> ticket)
{
    std::unique_ptr<CopyJobTicketFbT> CopyJobT = std::make_unique<CopyJobTicketFbT>();
    if(ticket)
    {
        CopyJobT->intent = std::move(serializeCopyJobIntent(ticket->getIntent()));
        CopyJobT->base = std::move(serializeJobTicket(ticket));
    }
    return CopyJobT;
}
bool deserializeCopyJobIntent(std::shared_ptr<CopyJobIntentFbT> data, std::shared_ptr<ICopyJobIntent>&& intent)
{
    bool retVal{false};
    if (intent && data)
    {
        intent->setOutputMediaSizeId(data->outputMediaSizeId);
        intent->setOutputMediaOrientation(data->outputMediaOrientation);
        intent->setOutputMediaIdType(data->outputMediaIdType);
        intent->setOutputMediaSource(data->outputMediaSource);
        intent->setOutputPlexMode(data->outputPlexMode);
        intent->setCopyMargins(data->copyMargins);
        intent->setOutputPlexBinding(data->outputPlexBinding);
        intent->setFoldingStyleId(data->foldingStyleId);
        intent->setCopies(data->copies);
        intent->setCollate(data->collate);
        intent->setCopyQuality(data->copyQuality);
        intent->setOutputDestination(data->outputMediaDestination);
        intent->setPrintingOrder(data->printingOrder);
        intent->setRotation(data->rotation);
        intent->setAutoRotate(data->autoRotate);
        intent->setMediaFamily(data->mediaFamily);
        intent->setCustomMediaXDimension(data->customMediaXDimension);
        intent->setCustomMediaYDimension(data->customMediaYDimension);
        intent->setStapleOption(static_cast<dune::imaging::types::StapleOptions>(data->stapleOption));
        intent->setPunchOption(static_cast<dune::imaging::types::PunchingOptions>(data->punchOption));
        intent->setJobOffsetMode(data->jobOffset);
        intent->setFoldOption(static_cast<dune::imaging::types::FoldingOptions>(data->foldOption));
        intent->setSheetsPerSetForCFold(data->cFoldSheets);
        intent->setSheetsPerSetForVFold(data->vFoldSheets);
        intent->setBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(data->bookletMakerOption));
        intent->setSheetsPerSetForFoldAndStitch(data->foldAndStitchSheets);
        intent->setDeviceSetsFoldAndStitchSheetsEnabled(data->deviceSetsFoldAndStitchSheetsEnabled);
        retVal |= dune::scan::Jobs::Scan::deserializeScanJobIntent(data->scanJobIntent,intent);
    }
    return retVal;
}

dune::framework::data::SerializedDataBufferPtr serializeTo(std::shared_ptr<ICopyJobTicket> ticket)
{
    flatbuffers::FlatBufferBuilder builder{};
    std::unique_ptr<CopyJobTicketFbT> CopyJobT = serializeCopyJobTicket(ticket);
    builder.Finish(CopyJobTicketFb::Pack(builder, CopyJobT.get()));

    flatbuffers::Verifier verifier(builder.GetBufferPointer(), builder.GetSize());
    bool                  ok = VerifyCopyJobTicketFbBuffer(verifier);
    CHECKPOINTA("CopyJobTicket::Ticket  has been serialized Verification %d ", ok);

    size_t size = builder.GetSize();
    uint8_t* pnew = new uint8_t[size];
    memcpy(pnew, builder.GetBufferPointer(), size);
    std::unique_ptr<uint8_t[]> p(pnew);

    auto retVal = std::make_pair(std::move(p), size);
    return retVal;
}

void validateTicketForPageBasedFinisher(std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<CopyJobIntentFbT> defaultIntentFromConfig, bool& intentWasUpdated)
{
    auto intent = ticket->getIntent();
    auto constraint = std::move(ticket->getConstraints());

    if(ticket->IsInstalledPageBasedFinisherDevice())
    {
        // OutputDestination
        intentWasUpdated = ticket->UpdateMediaOutputDestinationPageBasedFinisherInstalled();

        // Punch 
        if(intent->getPunchOption() != dune::imaging::types::PunchingOptions::NONE)
        {
            auto allPossiblePunchValueResult = ticket->getPossiblePunchingOptions();
            if(APIResult::OK == std::get<0>(allPossiblePunchValueResult))
            {
                auto punchOption = dune::job::cdm::mapToCdm(intent->getPunchOption());
                std::vector<dune::cdm::jobTicket_1::PunchOptions> retPossibleOptionsList = std::get<1>(allPossiblePunchValueResult);
                if(std::find(retPossibleOptionsList.begin(), retPossibleOptionsList.end(), punchOption)
                     == retPossibleOptionsList.end())
                {
                    intent->setPunchOption(dune::imaging::types::PunchingOptions::NONE);
                    intentWasUpdated = true;
                } 
            }
        }
    }
    else // Not Installed Page Based Finisher Device
    {
        //OutputDestination
        if(intent->getOutputDestination() != defaultIntentFromConfig->outputMediaDestination)
        {
            intent->setOutputDestination(defaultIntentFromConfig->outputMediaDestination);
            intentWasUpdated = true;
        }
        //Staple
        if(intent->getStapleOption() != dune::imaging::types::StapleOptions::NONE)
        {
            intent->setStapleOption(dune::imaging::types::StapleOptions::NONE);
            intentWasUpdated = true;
        }
        //Punch
        if(intent->getPunchOption() != dune::imaging::types::PunchingOptions::NONE)
        {
            intent->setPunchOption(dune::imaging::types::PunchingOptions::NONE);
            intentWasUpdated = true;
        }
        //Fold
        if(intent->getFoldOption() != dune::imaging::types::FoldingOptions::NONE)
        {
            intent->setFoldOption(dune::imaging::types::FoldingOptions::NONE);
            intentWasUpdated = true;
        }
        //Booklet
        if(intent->getBookletMakerOption() != dune::imaging::types::BookletMakingOptions::NONE)
        {
            intent->setBookletMakerOption(dune::imaging::types::BookletMakingOptions::NONE);
            intentWasUpdated = true;
        }
    }
}

void validateTicket(std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<CopyJobIntentFbT> defaultIntentFromConfig, bool& intentWasUpdated)
{
    // Next settings for the moment not need validation
    // intent->setResize ( ... )
    // intent->setLighterDarker( ... )
    // intent->setPlexSide( ... )
    // intent->setOutputMediaOrientation( ... )

    std::vector<dune::imaging::types::MediaSizeId> constraintMediaSize;
    std::vector<dune::imaging::types::MediaIdType> constraintMediaType;

    auto intent = ticket->getIntent();
    auto constraint = std::move(ticket->getConstraints());

    assert(constraint);
    if(!constraint)
    {
        CHECKPOINTB("CopyJobTicket::validateTicket No constraints! we can't validate");
        return;
    }

    CHECKPOINTC("CopyJobTicket::validateTicket previous any check");
    intent->dumpIntentToLog();

    if(!constraint->getMediaSupportedSizes().empty())
    {
        for(auto mediaSupportedSize : constraint->getMediaSupportedSizes())
        {
            dune::imaging::types::MediaSizeId mediaSizeValue = mediaSupportedSize.getId();
            if(constraintMediaSize.empty() ||
                std::find(constraintMediaSize.begin(), constraintMediaSize.end(), mediaSizeValue) == constraintMediaSize.end())
            {
                constraintMediaSize.push_back(mediaSizeValue);
            }
        }
    }

    if(!constraint->getMediaPrintSupportedSize().empty())
    {
        for(auto mediaSupportedSize : constraint->getMediaPrintSupportedSize())
        {
            dune::imaging::types::MediaSizeId mediaSizeValue = mediaSupportedSize;
            if(constraintMediaSize.empty() ||
                std::find(constraintMediaSize.begin(), constraintMediaSize.end(), mediaSizeValue) == constraintMediaSize.end())
            {
                constraintMediaSize.push_back(mediaSizeValue);
            }
        }
    }

    if(!constraint->getMediaSupportedTypes().empty())
    {
        for(auto mediaSupportedType : constraint->getMediaSupportedTypes())
        {
            dune::imaging::types::MediaIdType mediaIdType = mediaSupportedType.getId();
            if(constraintMediaType.empty() ||
                std::find(constraintMediaType.begin(), constraintMediaType.end(), mediaIdType) == constraintMediaType.end())
            {
                constraintMediaType.push_back(mediaIdType);
            }
        }
    }

    if(!constraint->getMediaPrintSupportedType().empty())
    {
        for(auto mediaSupportedType : constraint->getMediaPrintSupportedType())
        {
            dune::imaging::types::MediaIdType mediaIdType = mediaSupportedType;
            if(constraintMediaType.empty() ||
                std::find(constraintMediaType.begin(), constraintMediaType.end(), mediaIdType) == constraintMediaType.end())
            {
                constraintMediaType.push_back(mediaIdType);
            }
        }
    }

    auto checkpointFunction = [] (std::string settingName)
    {
        CHECKPOINTB("CopyJobTicket::validateIntent intent setting %s updated", settingName.c_str());
    };

    // Folding Style id is intentionally not validated here.
    intent->setOutputMediaSizeId(       dune::scan::Jobs::Scan::validateValueFromIntent(intent->getOutputMediaSizeId(),     constraintMediaSize,                            defaultIntentFromConfig->outputMediaSizeId, intentWasUpdated,   "outputMediaSizeId",checkpointFunction));
    intent->setOutputMediaIdType(       dune::scan::Jobs::Scan::validateValueFromIntent(intent->getOutputMediaIdType(),     constraintMediaType,                            defaultIntentFromConfig->outputMediaIdType, intentWasUpdated,   "outputMediaIdType",checkpointFunction));
    intent->setOutputMediaSource(       dune::scan::Jobs::Scan::validateValueFromIntent(intent->getOutputMediaSource(),     constraint->getMediaPrintSupportedSource(),     defaultIntentFromConfig->outputMediaSource, intentWasUpdated,   "outputMediaSource",checkpointFunction));
    intent->setOutputPlexMode(          dune::scan::Jobs::Scan::validateValueFromIntent(intent->getOutputPlexMode(),        constraint->getPlexMode(),                      defaultIntentFromConfig->outputPlexMode,    intentWasUpdated,   "outputPlexMode",   checkpointFunction));
    intent->setOutputPlexBinding(       dune::scan::Jobs::Scan::validateValueFromIntent(intent->getOutputPlexBinding(),     constraint->getPlexBinding(),                   defaultIntentFromConfig->outputPlexBinding, intentWasUpdated,   "outputPlexBinding",checkpointFunction));
    intent->setCollate(                 dune::scan::Jobs::Scan::validateValueFromIntent(intent->getCollate(),               constraint->getCollate(),                       defaultIntentFromConfig->collate,           intentWasUpdated,   "collate",          checkpointFunction));
    intent->setCopyQuality(             dune::scan::Jobs::Scan::validateValueFromIntent(intent->getCopyQuality(),           constraint->getPrintQuality(),                  defaultIntentFromConfig->copyQuality,       intentWasUpdated,   "copyQuality",      checkpointFunction));
    intent->setCopyMargins(             dune::scan::Jobs::Scan::validateValueFromIntent(intent->getCopyMargins(),           constraint->getCopyMargins(),                   defaultIntentFromConfig->copyMargins ,      intentWasUpdated,   "copyMargins",      checkpointFunction));
    intent->setPrintingOrder(           dune::scan::Jobs::Scan::validateValueFromIntent(intent->getPrintingOrder(),         constraint->getPrintingOrder(),                 defaultIntentFromConfig->printingOrder,     intentWasUpdated,   "printingOrder",    checkpointFunction));
    intent->setAutoRotate(              dune::scan::Jobs::Scan::validateValueFromIntent(intent->getAutoRotate(),            constraint->getAutoRotate(),                    defaultIntentFromConfig->autoRotate,        intentWasUpdated,   "autoRotate",       checkpointFunction));
    intent->setMediaFamily(             dune::scan::Jobs::Scan::validateValueFromIntent(intent->getMediaFamily(),           constraint->getMediaFamily(),                   defaultIntentFromConfig->mediaFamily,       intentWasUpdated,   "mediaFamily",      checkpointFunction));
 
    intent->setCopies(      dune::scan::Jobs::Scan::validateNumberValueFromIntent(intent->getCopies(),      constraint->getMinCopies(),      constraint->getMaxCopies(),    defaultIntentFromConfig->copies,    intentWasUpdated,           "copies",           checkpointFunction));
    intent->setRotation(    dune::scan::Jobs::Scan::validateNumberValueFromIntent(intent->getRotation(),    constraint->getMinRotation(),    constraint->getMaxRotation(),  defaultIntentFromConfig->rotation,  intentWasUpdated,           "rotation",         checkpointFunction));

    if(Product::ENTERPRISE == ticket->getPrePrintConfiguration())
    {
        validateTicketForPageBasedFinisher(ticket, defaultIntentFromConfig, intentWasUpdated);
    }
    else
    {
        intent->setOutputDestination(   dune::scan::Jobs::Scan::validateValueFromIntent(intent->getOutputDestination(),     constraint->getMediaDestinations(),             defaultIntentFromConfig->outputMediaDestination, intentWasUpdated,   "outputMediaDestination",checkpointFunction));
    }

    // Validate scan settings
    dune::scan::Jobs::Scan::validateIntent(intent, defaultIntentFromConfig->scanJobIntent.get(), constraint, intentWasUpdated);

    if(intentWasUpdated)
    {
        CHECKPOINTC("CopyJobTicket::validateTicket intent updated, dumping intent after changes");
        intent->dumpIntentToLog();
    }
}

bool compareIntents(std::shared_ptr<ICopyJobIntent> firstIntent, std::shared_ptr<ICopyJobIntent> secondIntent)
{
    bool result = false;
    auto checkFunction = [] (bool resultCheck,std::string settingName, std::string firstValue, std::string secondValue)
    {
        if(!resultCheck)
        {
            CHECKPOINTB("CopyJobTicket::compareIntents intent setting %s are not equal between intents with first value %s and second value %s", settingName.c_str(), firstValue.c_str(), secondValue.c_str());
        }
        return resultCheck;
    };

    if(firstIntent && secondIntent )
    {
        result = checkFunction(firstIntent->getOutputMediaSizeId()   == secondIntent->getOutputMediaSizeId(),   "Output MediaSizeId",   std::to_string(static_cast<int>(firstIntent->getOutputMediaSizeId())),  std::to_string(static_cast<int>(secondIntent->getOutputMediaSizeId())))
            && checkFunction(firstIntent->getOutputMediaIdType()     == secondIntent->getOutputMediaIdType(),   "Output MediaIdType",   std::to_string(static_cast<int>(firstIntent->getOutputMediaIdType())),  std::to_string(static_cast<int>(secondIntent->getOutputMediaIdType())))
            && checkFunction(firstIntent->getOutputMediaSource()     == secondIntent->getOutputMediaSource(),   "Output Media Source",  std::to_string(static_cast<int>(firstIntent->getOutputMediaSource())),  std::to_string(static_cast<int>(secondIntent->getOutputMediaSource())))
            && checkFunction(firstIntent->getOutputPlexMode()        == secondIntent->getOutputPlexMode(),      "Output Plex Mode",     std::to_string(static_cast<int>(firstIntent->getOutputPlexMode())),     std::to_string(static_cast<int>(secondIntent->getOutputPlexMode())))
            && checkFunction(firstIntent->getOutputPlexBinding()     == secondIntent->getOutputPlexBinding(),   "Output Plex Binding",  std::to_string(static_cast<int>(firstIntent->getOutputPlexBinding())),  std::to_string(static_cast<int>(secondIntent->getOutputPlexBinding())))
            && checkFunction(firstIntent->getFoldingStyleId()        == secondIntent->getFoldingStyleId(),      "FoldingStyle Id",      std::to_string(static_cast<short>(firstIntent->getFoldingStyleId())),   std::to_string(static_cast<short>(secondIntent->getFoldingStyleId())))
            && checkFunction(firstIntent->getCollate()               == secondIntent->getCollate(),             "Collate",              std::to_string(static_cast<int>(firstIntent->getCollate())),            std::to_string(static_cast<int>(secondIntent->getCollate())))
            && checkFunction(firstIntent->getCopyQuality()           == secondIntent->getCopyQuality(),         "Copy Quality",         std::to_string(static_cast<int>(firstIntent->getCopyQuality())),        std::to_string(static_cast<int>(secondIntent->getCopyQuality())))
            && checkFunction(firstIntent->getCopyMargins()           == secondIntent->getCopyMargins(),         "Copy Margins",         std::to_string(static_cast<int>(firstIntent->getCopyMargins())),        std::to_string(static_cast<int>(secondIntent->getCopyMargins())))
            && checkFunction(firstIntent->getOutputDestination()     == secondIntent->getOutputDestination(),   "Output Destination",   std::to_string(static_cast<int>(firstIntent->getOutputDestination())),  std::to_string(static_cast<int>(secondIntent->getOutputDestination())))
            && checkFunction(firstIntent->getPrintingOrder()         == secondIntent->getPrintingOrder(),       "Printing Order",       std::to_string(static_cast<int>(firstIntent->getPrintingOrder())),      std::to_string(static_cast<int>(secondIntent->getPrintingOrder())))
            && checkFunction(firstIntent->getAutoRotate()            == secondIntent->getAutoRotate(),          "AutoRotate",           std::to_string(firstIntent->getAutoRotate()),                           std::to_string(secondIntent->getAutoRotate()))
            && checkFunction(firstIntent->getMediaFamily()           == secondIntent->getMediaFamily(),         "MediaFamily",          std::to_string(static_cast<int>(firstIntent->getMediaFamily())),        std::to_string(static_cast<int>(secondIntent->getMediaFamily())))
            && checkFunction(firstIntent->getCopies()                == secondIntent->getCopies(),              "Copies",               std::to_string(firstIntent->getCopies()),                               std::to_string(secondIntent->getCopies()))
            && checkFunction(firstIntent->getRotation()              == secondIntent->getRotation(),            "Rotation",             std::to_string(firstIntent->getRotation()),                             std::to_string(secondIntent->getRotation()))
            && dune::scan::Jobs::Scan::compareIntents(firstIntent,secondIntent);
    }

    return result;
}

CopyJobTicket::SerializedDataBufferPtr CopyJobTicket::serialize() const {
    CopyJobTicketFbT ticketFbT{};
    ticketFbT.base = std::move(this->serializeBase());
    ticketFbT.intent = serializeCopyJobIntent(this->getIntent());
    ticketFbT.firstScanStarted = isFirstScanStarted();
    ticketFbT.pagesTickets = serializePages();
    ticketFbT.version = getVersion();
    // Generating SerializedDataBufferPtr
    FlatBufferDataObjectAdapterJobTicket fbAdapter{};
    SerializedDataBufferPtr serializedData{};
    fbAdapter.serialize(serializedData, ticketFbT);
    return serializedData;
}

bool CopyJobTicket::deserialize(const SerializedDataBufferPtr& buffer) {
    // Recovering JobTicketFbT
    FlatBufferDataObjectAdapterJobTicket fbAdapter{};
    CopyJobTicketFbT ticketFbT{};
    bool deserialized = fbAdapter.deserialize(buffer, ticketFbT);
    if(!deserialized) { return false; }
    // Setting JobTicket fields
    this->deserializeBase(ticketFbT.base);
    deserializePages(ticketFbT.pagesTickets);
    std::shared_ptr<CopyJobIntentFbT> intent = std::move(ticketFbT.intent);
    setFirstScanStarted(ticketFbT.firstScanStarted);
    setVersion(ticketFbT.version);
    // [Beam] SVE - This sets up the copy job with the incorrect output destination (OUTPUTBIN1)
    bool retValue = deserializeCopyJobIntent(intent, this->getIntent());
    handler_ = std::make_shared<CopyJobTicketHandler>(
        *this, CopyJobTicketHandler::JobTicketEvents{jobTicketChanged_, jobTicketPageChanged_}, threadPool_);
    return retValue;
}

void CopyJobTicket::setIntent(std::shared_ptr<CopyJobIntentFbT> intentFb)
{
    // [Beam] SVE - This sets up the copy job with the correct output destination (STANDARDBIN)
    deserializeCopyJobIntent(intentFb, this->getIntent());
}

void CopyJobTicket::validateMediaOutputDestination()
{
    if(dune::imaging::types::MediaDestinationId::STANDARDBIN == this->getIntent()->getOutputDestination()
        && true == IsInstalledPageBasedFinisherDevice())
    {
        UpdateMediaOutputDestinationPageBasedFinisherInstalled();
    }
}

bool deserializeConstraints(std::shared_ptr<CopyJobConstraintsFbT> data, std::shared_ptr<ICopyJobConstraints>&& constraint, uint32_t maxCopiesOverride)
{
    CHECKPOINTC("deserializeConstraints -- ENTER");
    bool retVal{false};

    if (constraint && data)
    {
        CHECKPOINTC("deserializeConstraints data and constraint exist.");
        /* Constraint for Copy */

        /* Set the plex mode. */
        if(!data->plexMode.empty())
        {
            for(auto iter = data->plexMode.begin() ; iter != data->plexMode.end(); iter++)
            {
                constraint->addPlexMode(*iter);
            }
        }

        /* Set copyMargins. */
        if(!data->copyMargins.empty())
        {
            for(auto iter = data->copyMargins.begin() ; iter != data->copyMargins.end(); iter++)
            {
                constraint->addCopyMargins(*iter);
            }
        }

        /* Set printingOrder. */
        if(!data->printingOrder.empty())
        {
            for(auto iter = data->printingOrder.begin() ; iter != data->printingOrder.end(); iter++)
            {
                constraint->addPrintingOrder(*iter);
            }
        }

        /* Set the rotation numbers related variables. */
        constraint->setMinRotation(data->minRotation);
        constraint->setMaxRotation(data->maxRotation);
        constraint->setStepRotation(data->stepRotation);

        /* Set mediaFamily. */
        if(!data->mediaFamily.empty())
        {
            for(auto iter = data->mediaFamily.begin() ; iter != data->mediaFamily.end(); iter++)
            {
                constraint->addMediaFamily(*iter);
            }
        }

        /* Set autoRotate. */
        if(!data->autoRotate.empty())
        {
            for(auto iter = data->autoRotate.begin() ; iter != data->autoRotate.end(); iter++)
            {
                constraint->addAutoRotate(*iter);
            }
        }

        /* Set the plex binding. */
        if(!data->plexBinding.empty())
        {
            for(auto iter = data->plexBinding.begin() ; iter != data->plexBinding.end(); iter++)
            {
                constraint->addPlexBinding(*iter);
            }
        }

        /* Set the collate. */
        if(!data->collate.empty())
        {
            for(auto iter = data->collate.begin() ; iter != data->collate.end(); iter++)
            {
                constraint->addCollate(*iter);
            }
        }

        /* Set the copy numbers related variables. */
        constraint->setMinCopies(data->minCopies);
        if (maxCopiesOverride)
            constraint->setMaxCopies(maxCopiesOverride);
        else
            constraint->setMaxCopies(data->maxCopies);
        constraint->setStepCopies(data->stepCopies);

        /* Set the print quality. */
        if(!data->printQuality.empty())
        {
            for(auto iter = data->printQuality.begin() ; iter != data->printQuality.end(); iter++)
            {
                constraint->addPrintQuality(*iter);
            }
        }

        /* Set the media supported sizes. */
        if(!data->mediaSupportedSize.empty())
        {
            for(auto iter = data->mediaSupportedSize.begin() ; iter != data->mediaSupportedSize.end() ; iter++)
            {
                CopyJobMediaSupportedSize mediaSupportedSize;
                mediaSupportedSize.addId(iter->get()->size->id);
                mediaSupportedSize.addMediaOrientation(iter->get()->size->mediaOrientation);
                mediaSupportedSize.addSupportedMediaSource(iter->get()->supportedMediaSource);
                mediaSupportedSize.addDuplex(iter->get()->duplex);
                constraint->addMediaSupportedSize(mediaSupportedSize);
            }
        }

        /* Set the media supported types. */
        if(!data->mediaSupportedType.empty())
        {
            for(auto iter = data->mediaSupportedType.begin() ; iter != data->mediaSupportedType.end() ; iter++)
            {
                CopyJobMediaSupportedType mediaSupportedType;
                mediaSupportedType.addId(iter->get()->type->id);
                mediaSupportedType.addSupportedMediaSource(iter->get()->supportedMediaSource);
                mediaSupportedType.addDuplex(iter->get()->duplex);
                mediaSupportedType.addColorMode(iter->get()->colorMode);
                constraint->addMediaSupportedType(mediaSupportedType);
            }
        }

        /* Set the media print supported Sources. */
        if(!data->mediaPrintSupportedSource.empty())
        {
            for(auto iter = data->mediaPrintSupportedSource.begin() ; iter != data->mediaPrintSupportedSource.end(); iter++)
            {
                constraint->addMediaPrintSupportedSource(*iter);
            }
        }

        /* Set the media print supported Sizes. */
        if(!data->mediaPrintSupportedSize.empty())
        {
            for(auto iter = data->mediaPrintSupportedSize.begin() ; iter != data->mediaPrintSupportedSize.end(); iter++)
            {
                constraint->addMediaPrintSupportedSize(*iter);
            }
        }

        /* Set the media print supported types. */
        if(!data->mediaPrintSupportedType.empty())
        {
            for(auto iter = data->mediaPrintSupportedType.begin() ; iter != data->mediaPrintSupportedType.end(); iter++)
            {
                constraint->addMediaPrintSupportedType(*iter);
            }
        }

        /* Set print media destination valid supported. */
        if(!data->mediaPrintSupportedDestinations.empty())
        {
            for(auto iter = data->mediaPrintSupportedDestinations.begin() ; iter != data->mediaPrintSupportedDestinations.end(); iter++)
            {
                CHECKPOINTC_STR("Adding media destination constraint: %s", EnumNameMediaDestinationId(*iter));
                constraint->addMediaDestinations(*iter);
            }
        }

        /* Set stapleOptions: This value must be recreated as a value through the helper function from printer. */
        if(!data->stapleOption.empty())
        {
            for(auto iter = data->stapleOption.begin() ; iter != data->stapleOption.end(); iter++)
            {
                constraint->addStapleOption(static_cast<dune::imaging::types::StapleOptions>(*iter));
            }
        }

        /* Set punchOptions: : This value must be recreated as a value through the helper function from printer. */
        if(!data->punchOption.empty())
        {
            for(auto iter = data->punchOption.begin() ; iter != data->punchOption.end(); iter++)
            {
                constraint->addPunchOption(static_cast<dune::imaging::types::PunchingOptions>(*iter));
            }
        }

        /* Set FoldOptions: This value must be recreated as a value through the helper function from printer. */
        if(!data->foldOption.empty())
        {
            for(auto iter = data->foldOption.begin() ; iter != data->foldOption.end(); iter++)
            {
                constraint->addFoldOption(static_cast<dune::imaging::types::FoldingOptions>(*iter));
            }

            /* Set the sheets numbers related variables. */
            constraint->setMinSheetsPerSetForCFold(data->minSheetsPerSetForCFold);
            constraint->setMaxSheetsPerSetForCFold(data->maxSheetsPerSetForCFold);
            
            constraint->setMinSheetsPerSetForVFold(data->minSheetsPerSetForVFold);
            constraint->setMaxSheetsPerSetForVFold(data->maxSheetsPerSetForVFold);
        }

        /* Set BookletMakingOptions: This value must be recreated as a value through the helper function from printer. */
        if(!data->bookletMakerOption.empty())
        {
            for(auto iter = data->bookletMakerOption.begin() ; iter != data->bookletMakerOption.end(); iter++)
            {
                constraint->addBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(*iter));
            }

            /* Set the sheets numbers related variables. */
            constraint->setMinSheetsPerSetForFoldAndStitch(data->minSheetsPerSetForFoldAndStitch);
            constraint->setMaxSheetsPerSetForFoldAndStitch(data->maxSheetsPerSetForFoldAndStitch);
            
            for(auto iter = data->deviceSetsFoldAndStitchSheetsEnabled.begin() ; iter != data->deviceSetsFoldAndStitchSheetsEnabled.end(); iter++)
            {
                constraint->addDeviceSetsFoldAndStitchSheetsEnabled(static_cast<bool>(*iter));
            }
        }

        /* Set the folding style Ids */
        if(!data->foldingStyleIds.empty())
        {
            for(auto iter = data->foldingStyleIds.begin() ; iter != data->foldingStyleIds.end(); ++iter )
            {
                constraint->addFoldingStyle(*iter);
            }
        }

        /* Set the Job Offset */
        if(!data->jobOffset.empty())
        {
            for(auto iter = data->jobOffset.begin() ; iter != data->jobOffset.end(); ++iter )
            {
                constraint->addJobOffsetMode(*iter);
            }
        }

        /* Constraint for Scan */
        constraint->parseScanJobConstraint(data->scanJobConstraint.get());
    }
    CHECKPOINTC("deserializeConstraints -- EXIT");
    return retVal;
}

void CopyJobTicket::setConstraintsFromFb(std::shared_ptr<CopyJobConstraintsFbT> constraintsFb)
{
    if(  dune::copy::Jobs::Copy::constraintsFb_ == nullptr)
    {
        // The first time this function is called it will be called from
        // JobServiceStandard; and we need to stash a reference to the
        // constraints form the .csf file.
        // This is probably not a pattern that you should follow (#SideEffects).
         dune::copy::Jobs::Copy::constraintsFb_ = constraintsFb;
    }

    // Get Maximum Copies from derivative if it is set
    const Uuid devinfo = dune::framework::storage::DEVICE_INFO_GUID;
    uint32_t maxCopiesOverride = 0;
    if (nvramInterface_)
    {
        if (nvramInterface_->doesVariableExist((const char *) "MaxCopies", &devinfo))
        {
            if (nvramInterface_->getVariable((const char *) "MaxCopies", &devinfo, maxCopiesOverride) == 0)
            {
                CHECKPOINTC("CopyJobTicket::setConstraintsFromFb: maxCopiesOverride variable = %d from NVRAM", (int32_t)maxCopiesOverride);
            }
            else
            {
                CHECKPOINTA("CopyJobTicket::setConstraintsFromFb: Unable to read maxCopiesOverride variable from NVRAM");
            }
        }
    }
    else
    {
        CHECKPOINTA("CopyJobTicket::setConstraintsFromFb: nvramInterface_ is null!");
    }

    deserializeConstraints(constraintsFb, this->getConstraints(), maxCopiesOverride);
}

void CopyJobTicket::clearConstraintsFromFb(void)
{
    dune::copy::Jobs::Copy::constraintsFb_ = nullptr;
}

std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>> CopyJobTicket::getAllSupportedMediaSizes() const
{
    /*
        Step : 1. Get getAllSupportedMediaSizes though MediaHelper.
               2. Convert Media Size from 'dune::imaging::types::MediaSizeId' to 'dune::cdm::glossary_1::MediaSize'.
    */
    dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
    std::vector<dune::cdm::glossary_1::MediaSize> retSupportedMediaSizesList;

    const auto result = dune::print::engine::MediaHelper::getAllSupportedOrientedMediaSizes(mediaInterface_);
    const auto retValue = std::get<0>(result);
    if (retValue != APIResult::OK)
    {
        CHECKPOINTA("CopyJobTicket::getAllSupportedMediaSizes(): ERROR getAllSupportedMediaSizes");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>>(APIResult::ERROR, retSupportedMediaSizesList);
    }
    const auto mediaSizesFromHelper = std::get<1>(result);
    if (getPrePrintConfiguration() == Product::ENTERPRISE)
    {
        retSupportedMediaSizesList.push_back(dune::cdm::glossary_1::MediaSize::any);
    }
    for (const auto& orientedMediaSize : mediaSizesFromHelper)
    {
        auto type = orientedMediaSize.getMediaSize().getType();
        if (type != dune::imaging::types::MediaSizeId::ANY)
        {
            for (const auto& orientation: orientedMediaSize.getOrientation())
            {
                auto curMediaSize = mediaCdmHelper.convertDuneMediaIdSizeToCdm(type, orientation);
                if (std::find(retSupportedMediaSizesList.begin(), retSupportedMediaSizesList.end(), curMediaSize)
                    == retSupportedMediaSizesList.end())
                {
                    retSupportedMediaSizesList.push_back(curMediaSize);
                }
            }
        }
    }

    return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>>(APIResult::OK, retSupportedMediaSizesList);;
}

std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> CopyJobTicket::getAllSupportedMediaTypes() const
{
    /*
        Step : 1. Get getAllSupportedMediaTypes though MediaHelper.
               2. Convert Media Type from 'dune::imaging::types::MediaIdType' to 'dune::cdm::glossary_1::MediaType'.
    */
    dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
    std::vector<dune::cdm::glossary_1::MediaType> retSupportedMediaTypesList;

    const auto result = dune::print::engine::MediaHelper::getAllSupportedMediaTypes(mediaInfoPtr_, mediaInterface_);
    const auto retValue = std::get<0>(result);
    if (retValue != APIResult::OK)
    {
        CHECKPOINTA("CopyJobTicket::getAllSupportedMediaTypes(): ERROR getAllSupportedMediaTypes");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>(APIResult::ERROR, retSupportedMediaTypesList);
    }
    const auto mediaTypesFromHelper = std::get<1>(result);
    for(auto it = mediaTypesFromHelper.begin(); it != mediaTypesFromHelper.end(); it++)
    {
        auto curMediaType = mediaCdmHelper.convertDuneMediaIdTypeToCdm(it->getType());
        retSupportedMediaTypesList.push_back(curMediaType);
    }

    return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>(APIResult::OK, retSupportedMediaTypesList);;
}

bool CopyJobTicket::isMediaTypeVisibilityTogglingSupported() const
{
    CHECKPOINTB("CopyJobTicket::isMediaTypeVisibilityTogglingSupported(): %d", isMediaTypeVisibilityTogglingSupported_);
    return isMediaTypeVisibilityTogglingSupported_;
}

void CopyJobTicket::setisMediaTypeVisibilityTogglingSupported(bool isMediaTypeVisibilityTogglingSupported)
{
    CHECKPOINTB("CopyJobTicket::setisMediaTypeVisibilityTogglingSupported(): %d", isMediaTypeVisibilityTogglingSupported);
    isMediaTypeVisibilityTogglingSupported_ = isMediaTypeVisibilityTogglingSupported;
}

std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> CopyJobTicket::getEnabledMediaTypes() const
{
    /*
        Step : 1. Get getAllSupportedMediaTypes though MediaHelper.
               2. Convert Media Type from 'dune::imaging::types::MediaIdType' to 'dune::cdm::glossary_1::MediaType'.
    */
    dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
    std::vector<dune::cdm::glossary_1::MediaType> retSupportedMediaTypesList;
    CHECKPOINTA("CopyJobTicket::getEnabledMediaTypes(): ENTER log");
    const auto result = dune::print::engine::MediaHelper::getEnabledMediaTypes(mediaInfoPtr_, mediaInterface_);

    const auto retValue = std::get<0>(result);
    if (retValue != APIResult::OK)
    {
        CHECKPOINTA("CopyJobTicket::getEnabledMediaTypes(): ERROR getAllSupportedMediaTypes");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>(APIResult::ERROR, retSupportedMediaTypesList);
    }
    const auto mediaTypesFromHelper = std::get<1>(result);
    for(auto it = mediaTypesFromHelper.begin(); it != mediaTypesFromHelper.end(); it++)
    {
        auto curMediaType = mediaCdmHelper.convertDuneMediaIdTypeToCdm(it->getType());
        retSupportedMediaTypesList.push_back(curMediaType);
    }
    CHECKPOINTA("CopyJobTicket::getEnabledMediaTypes(): EXIT log with %d media types", retSupportedMediaTypesList.size());
    return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>(APIResult::OK, retSupportedMediaTypesList);;
}

std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>> CopyJobTicket::getSupportedMediaSizes(dune::imaging::types::MediaSource mediaSource) const
{
    /*
        Step : 1. 1. Get supportedMediaSizes corresponding to a MediaSource.
               2. Convert Media Size from 'dune::imaging::types::MediaSizeId' to 'dune::cdm::glossary_1::MediaSize'.
    */
    dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
    std::vector<dune::cdm::glossary_1::MediaSize> supportedMediaSizesList;
    if (mediaInterface_ == nullptr)
    {
        CHECKPOINTA("CopyJobTicket::getSupportedMediaSizes(): ERROR mediaInterface_ is null");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>>(APIResult::ERROR, supportedMediaSizesList);
    }

    const auto inputDevice = dune::print::engine::MediaHelper::getInputDevice(mediaSource, mediaInterface_);
    if(inputDevice == nullptr)
    {
        CHECKPOINTA("CopyJobTicket::getSupportedMediaSizes(): ERROR inputDevice is null");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>>(APIResult::ERROR, supportedMediaSizesList);
    }

    auto supportedSizeByDevice = dune::print::engine::MediaHelper::getAllSupportedOrientedMediaSizes(inputDevice);
    if (getPrePrintConfiguration() == Product::ENTERPRISE)
    {
        supportedMediaSizesList.push_back(dune::cdm::glossary_1::MediaSize::any);
    }
    for (const auto& orientedMediaSize : supportedSizeByDevice)
    {
        auto type = orientedMediaSize.getMediaSize().getType();
        if (type != dune::imaging::types::MediaSizeId::ANY)
        {
            for (const auto& orientation: orientedMediaSize.getOrientation())
            {
                auto curMediaSize = mediaCdmHelper.convertDuneMediaIdSizeToCdm(type, orientation);
                if (std::find(supportedMediaSizesList.begin(), supportedMediaSizesList.end(), curMediaSize) ==
                    supportedMediaSizesList.end())
                {
                    supportedMediaSizesList.push_back(curMediaSize);
                }
            }
        }
    }

    auto customSizeSupported = inputDevice->isCustomSizeSupported();
    if (std::get<0>(customSizeSupported) == APIResult::OK)
    {
        if (std::get<1>(customSizeSupported))
        {
            auto customMediaSize = mediaCdmHelper.convertDuneMediaIdSizeToCdm(dune::imaging::types::MediaSizeId::CUSTOM);
            if (std::find(supportedMediaSizesList.begin(), supportedMediaSizesList.end(), customMediaSize) ==
                supportedMediaSizesList.end())
            {
                CHECKPOINTD("CopyJobTicket::getSupportedMediaSizes(): Adding CUSTOM to supportedMediaSizesList");
                supportedMediaSizesList.push_back(customMediaSize);
            }
        }
    }

    for (auto cdmSize : supportedMediaSizesList)
    {
        CHECKPOINTD_STR("CopyJobTicket::getSupportedMediaSizes(): supportedMediaSizesList: %s", dune::cdm::glossary_1::MediaSize::valueToString(cdmSize).c_str());
    }

    return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>>(APIResult::OK, supportedMediaSizesList);
}

void CopyJobTicket::updateSupportedPageBasedFinisherValidMediaSizes(std::vector<dune::cdm::glossary_1::MediaSize>& validMediaSizesList) const
{
    // Helper lambda to check if a media size exists in the list
    auto hasMediaSize = [&validMediaSizesList](dune::cdm::glossary_1::MediaSize size) {
        return std::any_of(validMediaSizesList.begin(), validMediaSizesList.end(),
                          [size](dune::cdm::glossary_1::MediaSize listSize) { return listSize == size; });
    };
    
    // Helper lambda to add media size if it doesn't exist
    auto addMediaSizeIfNotExists = [&validMediaSizesList, &hasMediaSize](dune::cdm::glossary_1::MediaSize size) {
        if (!hasMediaSize(size)) {
            validMediaSizesList.push_back(size);
        }
    };
    
    // Check for iso_a4_210x297mm and add rotated version if missing
    if (hasMediaSize(dune::cdm::glossary_1::MediaSize::iso_a4_210x297mm)) {
        addMediaSizeIfNotExists(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_iso_a4_210x297mm_dot_rotated);
    }
    
    // Check for rotated iso_a4_210x297mm and add normal version if missing
    if (hasMediaSize(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_iso_a4_210x297mm_dot_rotated)) {
        addMediaSizeIfNotExists(dune::cdm::glossary_1::MediaSize::iso_a4_210x297mm);
    }
    
    // Check for na_letter_8_5x11in and add rotated version if missing
    if (hasMediaSize(dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in)) {
        addMediaSizeIfNotExists(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_na_letter_8_dot_5x11in_dot_rotated);
    }
    
    // Check for rotated na_letter_8_5x11in and add normal version if missing
    if (hasMediaSize(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_na_letter_8_dot_5x11in_dot_rotated)) {
        addMediaSizeIfNotExists(dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in);
    }
}

std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaSize>> CopyJobTicket::getPageBasedFinisherValidMediaSizes() const
{
    if(IsInstalledPageBasedFinisherDevice())
    {
        if(copyJobIntent_->getStapleOption() != StapleOptions::NONE || copyJobIntent_->getPunchOption() != PunchingOptions::NONE 
            || copyJobIntent_->getFoldOption() != FoldingOptions::NONE || copyJobIntent_->getBookletMakerOption() != BookletMakingOptions::NONE)
        {   
            MediaId mediaType(copyJobIntent_->getOutputMediaIdType());
            StapleOptions stapleOption = copyJobIntent_->getStapleOption();
            PunchingOptions punchOption = copyJobIntent_->getPunchOption();
            FoldingOptions foldingOption = copyJobIntent_->getFoldOption();
            BookletMakingOptions bookletMakingOption = copyJobIntent_->getBookletMakerOption();
            MediaDestinationId mediaDestinationId = MediaDestinationId::AUTOSELECT;
            ContentOrientation originalOrientation = copyJobIntent_->getContentOrientation();

            CHECKPOINTC("CopyJobTicket::getPageBasedFinisherValidMediaSizes:: stapleOption %s, punchOption %s, foldingOption %s, mediaType %s, originalOrientation %s",
                dune::imaging::types::EnumNameStapleOptions(stapleOption),dune::imaging::types::EnumNamePunchingOptions(punchOption), 
                dune::imaging::types::EnumNameFoldingOptions(foldingOption), dune::imaging::types::EnumNameContentOrientation(originalOrientation),
                dune::imaging::types::EnumNameMediaIdType(mediaType.getType()));

            const auto result = dune::print::engine::MediaFinisherHelper::getAllValidMediaSizes(mediaInterface_, 
                mediaType, originalOrientation, stapleOption, punchOption, foldingOption, bookletMakingOption, mediaDestinationId, true);
            const auto retValue = std::get<0>(result);
            CHECKPOINTC("CopyJobTicket::getPageBasedFinisherValidMediaSizes:: retValue %d, size %d", retValue, std::get<1>(result).size());

            if(retValue == APIResult::OK)
            {
                dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
                std::vector<dune::cdm::glossary_1::MediaSize> validMediaSizesList;

                const auto validOptionsFromHelper = std::get<1>(result);
                validMediaSizesList.push_back(dune::cdm::glossary_1::MediaSize::any);
                for (const auto& orientedMediaSize : validOptionsFromHelper)
                {
                    auto type = orientedMediaSize.getMediaSize().getType();
                    if (type != dune::imaging::types::MediaSizeId::ANY)
                    {
                        for (const auto& orientation: orientedMediaSize.getOrientation())
                        {
                            auto curMediaSize = mediaCdmHelper.convertDuneMediaIdSizeToCdm(type, orientation);
                            if (std::find(validMediaSizesList.begin(), validMediaSizesList.end(), curMediaSize) ==
                                    validMediaSizesList.end())
                            {
                                validMediaSizesList.push_back(curMediaSize);
                            }
                        }
                    }
                }
                updateSupportedPageBasedFinisherValidMediaSizes(validMediaSizesList);
                return std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaSize>>(true, validMediaSizesList);
            }
        }    
    }
    return std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaSize>>(false, std::vector<dune::cdm::glossary_1::MediaSize>());
}

std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> CopyJobTicket::getSupportedMediaTypes(dune::imaging::types::MediaSource mediaSource) const
{
    /*
        Step : 1. Get getAllSupportedMediaTypes though MediaHelper.
               2. Convert Media Type from 'dune::imaging::types::MediaIdType' to 'dune::cdm::glossary_1::MediaType'.
    */
    dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
    std::vector<dune::cdm::glossary_1::MediaType> supportedMediaTypesList;
    if (mediaInterface_ == nullptr)
    {
        CHECKPOINTA("CopyJobTicket::getSupportedMediaTypes(): ERROR mediaInterface_ is null");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>(APIResult::ERROR, supportedMediaTypesList);
    }

    const auto inputDevice = dune::print::engine::MediaHelper::getInputDevice(mediaSource, mediaInterface_);
    if(inputDevice == nullptr)
    {
        CHECKPOINTA("CopyJobTicket::getSupportedMediaTypes(): ERROR inputDevice is null");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>(APIResult::ERROR, supportedMediaTypesList);
    }

    const auto supportedTypesTuple = inputDevice->getMediaSupportedTypes();
    const auto retSupportedTypes = std::get<0>(supportedTypesTuple);

    if (retSupportedTypes == APIResult::OK)
    {
        auto supportedTypeByDevice = std::get<1>(supportedTypesTuple);
        for (const auto& type : supportedTypeByDevice)
        {
            auto curMediaType = mediaCdmHelper.convertDuneMediaIdTypeToCdm(type.getType());
            if (std::find(supportedMediaTypesList.begin(), supportedMediaTypesList.end(), curMediaType) ==
                supportedMediaTypesList.end())
            {
                supportedMediaTypesList.push_back(curMediaType);
            }
        }
    }
    else
    {
        CHECKPOINTA("CopyJobTicket::getSupportedMediaTypes(): getMediaSupportedTypes() bad result");
    }

    return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>(APIResult::OK, supportedMediaTypesList);
}

std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaType>> CopyJobTicket::getPageBasedFinisherValidMediaTypes() const
{
    if(IsInstalledPageBasedFinisherDevice())
    {
        MediaSizeId OutputMediaSizeId{copyJobIntent_->getOutputMediaSizeId()};
        MediaOrientation OutputMediaOrientation{copyJobIntent_->getOutputMediaOrientation()};
        bool isPossibleBothOrientation = false;
        getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);
        OrientedMediaSize outputOrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation(OutputMediaOrientation)});
        if(isPossibleBothOrientation)
        {
            outputOrientedMediaSize = OrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE});
        }
        StapleOptions stapleOption = copyJobIntent_->getStapleOption();
        PunchingOptions punchOption = copyJobIntent_->getPunchOption();
        FoldingOptions foldingOption = copyJobIntent_->getFoldOption();
        BookletMakingOptions bookletMakingOption = copyJobIntent_->getBookletMakerOption();
        MediaDestinationId mediaDestinationId = copyJobIntent_->getOutputDestination();
        ContentOrientation originalOrientation = ContentOrientation::UNDEFINED;

        if(stapleOption != StapleOptions::NONE || punchOption != PunchingOptions::NONE 
            || foldingOption != FoldingOptions::NONE || bookletMakingOption != BookletMakingOptions::NONE)
        {                     
            const auto result = dune::print::engine::MediaFinisherHelper::getAllValidMediaTypes(mediaInterface_, 
                outputOrientedMediaSize, originalOrientation, stapleOption, punchOption, foldingOption, bookletMakingOption, mediaDestinationId, true);
            const auto retValue = std::get<0>(result);

            if(retValue == APIResult::OK)
            {
                dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
                std::vector<dune::cdm::glossary_1::MediaType> validMediaTypesList;

                const auto validOptionsFromHelper = std::get<1>(result);
                for (const auto& type : validOptionsFromHelper)
                {
                    auto curMediaType = mediaCdmHelper.convertDuneMediaIdTypeToCdm(type.getType());
                    if (std::find(validMediaTypesList.begin(), validMediaTypesList.end(), curMediaType) ==
                            validMediaTypesList.end())
                    {
                        validMediaTypesList.push_back(curMediaType);
                    }
                }
                return std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaType>>(true, validMediaTypesList);
            }
        }    
    }
    return std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaType>>(false, std::vector<dune::cdm::glossary_1::MediaType>());
}

std::tuple<bool, std::vector<dune::cdm::glossary_1::ContentOrientation>> CopyJobTicket::getPageBasedFinisherValidContentOrientation() const
{
    if(IsInstalledPageBasedFinisherDevice())
    {
        if(copyJobIntent_->getStapleOption() != StapleOptions::NONE || copyJobIntent_->getPunchOption() != PunchingOptions::NONE 
            || copyJobIntent_->getFoldOption() != FoldingOptions::NONE || copyJobIntent_->getBookletMakerOption() != BookletMakingOptions::NONE)
        { 
            MediaSizeId OutputMediaSizeId{copyJobIntent_->getOutputMediaSizeId()};
            MediaOrientation OutputMediaOrientation{copyJobIntent_->getOutputMediaOrientation()};
            bool isPossibleBothOrientation = false;
            getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);
            OrientedMediaSize outputOrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation(OutputMediaOrientation)});
            if(isPossibleBothOrientation)
            {
                outputOrientedMediaSize = OrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE});
            }
            MediaId mediaType = copyJobIntent_->getOutputMediaIdType();
            StapleOptions stapleOption = copyJobIntent_->getStapleOption();
            PunchingOptions punchOption = copyJobIntent_->getPunchOption();
            FoldingOptions foldingOption = copyJobIntent_->getFoldOption();
            BookletMakingOptions bookletMakingOption = copyJobIntent_->getBookletMakerOption();
            MediaDestinationId mediaDestinationId = copyJobIntent_->getOutputDestination();

            CHECKPOINTC("CopyJobTicket::getPageBasedFinisherValidContentOrientation():OuputMediaSizeId %s, OutputMediaOrientation %s, isPossibleBothOrientation %d",
                dune::imaging::types::EnumNameMediaSizeId(OutputMediaSizeId), dune::imaging::types::EnumNameMediaOrientation(OutputMediaOrientation),
                isPossibleBothOrientation); 

            CHECKPOINTC("CopyJobTicket::getPageBasedFinisherValidContentOrientation(): stapleOption %s, punchOption %s, foldingOption %s, mediaType %s",
                dune::imaging::types::EnumNameStapleOptions(stapleOption),dune::imaging::types::EnumNamePunchingOptions(punchOption), 
                dune::imaging::types::EnumNameFoldingOptions(foldingOption), dune::imaging::types::EnumNameMediaIdType(mediaType.getType()));

         
            const auto result = dune::print::engine::MediaFinisherHelper::getAllValidContentOrientations(mediaInterface_, 
                outputOrientedMediaSize, mediaType, stapleOption, punchOption, foldingOption, bookletMakingOption, mediaDestinationId);
            const auto retValue = std::get<0>(result);

            if(retValue == APIResult::OK)
            {
                std::vector<dune::cdm::glossary_1::ContentOrientation> validContentOrientationList;

                const auto validOptionsFromHelper = std::get<1>(result);
                for (const auto& orientation : validOptionsFromHelper)
                {
                    auto mapped = (orientation == dune::imaging::types::ContentOrientation::REVERSEPORTRAIT)
                                    ? ContentOrientation::PORTRAIT
                                : (orientation == dune::imaging::types::ContentOrientation::REVERSELANDSCAPE)
                                    ? ContentOrientation::LANDSCAPE
                                : orientation;
                    auto curOrientation =  dune::job::cdm::mapToCdm(mapped);
                    if (std::find(validContentOrientationList.begin(), validContentOrientationList.end(), curOrientation) ==
                            validContentOrientationList.end())
                    {
                        validContentOrientationList.push_back(curOrientation);
                    }
                }
                return std::tuple<bool, std::vector<dune::cdm::glossary_1::ContentOrientation>>(true, validContentOrientationList);
            }
        }    
    }
    return std::tuple<bool, std::vector<dune::cdm::glossary_1::ContentOrientation>>(false, std::vector<dune::cdm::glossary_1::ContentOrientation>());
}

std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>> CopyJobTicket::getAllSupportedMediaSources() const
{
    // Get the list of devices dynamically using imdia interface.
    std::vector<dune::cdm::glossary_1::MediaSourceId> supportedMediaSourcesList;

    if (mediaInterface_ == nullptr)
    {
        CHECKPOINTA("CopyJobTicket::getAllSupportedMediaSources(): ERROR mediaInterface_ is null");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>>(APIResult::ERROR, supportedMediaSourcesList);
    }

    const auto inputDevicesListTuple = mediaInterface_->getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE);
    const auto inputDevicesList = std::get<1>(inputDevicesListTuple);
    const APIResult retInputDeviceList = std::get<0>(inputDevicesListTuple);
    if(retInputDeviceList == APIResult::ERROR){
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>>(APIResult::ERROR, supportedMediaSourcesList);
    }
    else if((inputDevicesList.size() > 0) && (retInputDeviceList == APIResult::OK)){
        dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
        //auto is default
        supportedMediaSourcesList.push_back(dune::cdm::glossary_1::MediaSourceId::auto_);
        for(auto it : inputDevicesList){
            auto inputType = it->getType();
            if(inputType == dune::print::engine::InputType::TRAY)
            {
                auto inputTray = it->getTray();
                if(inputTray){
                    auto snapTuple = inputTray->getSnapShot();
                    if(std::get<0>(snapTuple) == APIResult::OK){
                        auto snap = std::get<1>(snapTuple);
                        dune::imaging::types::MediaSource mediaSourceId = inputTray->getMediaSource();
                        dune::cdm::glossary_1::MediaSourceId cdmSourceId = mediaCdmHelper.convertDuneMediaSourceToCdm(mediaSourceId);
                        if (cdmSourceId == dune::cdm::glossary_1::MediaSourceId::tray_dash_1 &&
                            getPrePrintConfiguration() == Product::ENTERPRISE)
                        {
                            // Manual feed is logically another name for Tray1 in Enterprise.
                            supportedMediaSourcesList.push_back(dune::cdm::glossary_1::MediaSourceId::manual);
                        }
                        supportedMediaSourcesList.push_back(cdmSourceId);
                    }
                }
            }
            else if(inputType == dune::print::engine::InputType::ROLL)
            {
                auto inputRoll = it->getRoll();
                if(inputRoll){
                    auto snapTuple = inputRoll->getSnapShot();
                    if(std::get<0>(snapTuple) == APIResult::OK){
                        auto snap = std::get<1>(snapTuple);
                        dune::imaging::types::MediaSource mediaSourceId = inputRoll->getMediaSource();
                        dune::cdm::glossary_1::MediaSourceId cdmSourceId = mediaCdmHelper.convertDuneMediaSourceToCdm(mediaSourceId);
                        supportedMediaSourcesList.push_back(cdmSourceId);
                    }
                }
            }
        }
    }
    else
    {
        CHECKPOINTA("CopyJobTicket::getAllSupportedMediaSources(): getAllSupportedMediaSources() bad result");
        std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>>(APIResult::ERROR, supportedMediaSourcesList);
    }
    for (auto iter = supportedMediaSourcesList.begin(); iter != supportedMediaSourcesList.end(); iter++)
    {
        CHECKPOINTC("CopyJobTicket::getAllSupportedMediaSources(): - SupportedMediaSource is %s", (*iter).toString().c_str());
    }
    return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>>(APIResult::OK, supportedMediaSourcesList);
}

bool CopyJobTicket::IsInstalledPageBasedFinisherDevice() const
{
    if (mediaInterface_ == nullptr)
    {
        CHECKPOINTA("CopyJobTicket::IsInstalledPageBasedFinisherDevice(): ERROR mediaInterface_ is null");
        return false;
    }
    const auto finisherDevicesTuple = mediaInterface_->getFinisherDevices();
    const auto finisherDevices = std::get<1>(finisherDevicesTuple);
    const auto retValue = std::get<0>(finisherDevicesTuple);
    if (retValue != APIResult::OK || finisherDevices.size() == 0) {
        CHECKPOINTA("CopyJobTicket::IsInstalledPageBasedFinisherDevice: ERROR getFinisherDevices() failed! - [%d/%d]", static_cast<int32_t>(retValue), finisherDevices.size());
        return false;
    }
    else
    {
        for (const auto & finisherDevice : finisherDevices) {
            if (dune::print::engine::FinisherType::PAGEBASED_FINISHER != finisherDevice->getType()) {
                CHECKPOINTC("CopyJobTicket::IsInstalledPageBasedFinisherDevice: finisherDevice->getType() %d ", static_cast<int32_t>(finisherDevice->getType()));
                return false;
            }
        }
    }
    CHECKPOINTA("CopyJobTicket::IsInstalledPageBasedFinisherDevice: OK - %d", finisherDevices.size());
    return true;
}

bool CopyJobTicket::IsInstalledSpecificPageBasedFinisherDevice(MediaProcessingTypes mediaProcessingType) const
{
    bool retValue = false;

    if (mediaInterface_ == nullptr)
    {
        CHECKPOINTA("CopyJobTicket::IsInstalledSpecificPageBasedFinisherDevice(): ERROR mediaInterface_ is null");
        return false;
    }

    if(mediaProcessingType == MediaProcessingTypes::STAPLE)
    {
        retValue = std::get<1>(dune::print::engine::MediaFinisherHelper::isStaplerInstalled(mediaInterface_));
    }
    else if(mediaProcessingType == MediaProcessingTypes::PUNCH)
    {
        retValue = std::get<1>(dune::print::engine::MediaFinisherHelper::isPunchingSupported(mediaInterface_));
    }
    else if(mediaProcessingType == MediaProcessingTypes::FOLD)
    {
        retValue = std::get<1>(dune::print::engine::MediaFinisherHelper::isFoldingSupported(mediaInterface_));
    }
    else if(mediaProcessingType == MediaProcessingTypes::BOOKLET_MAKING)
    {
        retValue = std::get<1>(dune::print::engine::MediaFinisherHelper::isBookletMakerSupported(mediaInterface_));
    }
    else
    {
        CHECKPOINTA("CopyJobTicket::IsInstalledSpecificPageBasedFinisherDevice: ERROR Invalid mediaProcessingType");
        return false;
    }
    CHECKPOINTC("CopyJobTicket::IsInstalledSpecificPageBasedFinisherDevice - type: %d /ret: %d ", mediaProcessingType, retValue);
    return retValue; 
}

bool CopyJobTicket::UpdateMediaOutputDestinationPageBasedFinisherInstalled() const
{
    auto allPossibleOutputBinValueResult = getPossibleOutputBins();

    if (APIResult::OK == std::get<0>(allPossibleOutputBinValueResult))
    {
        std::vector<dune::cdm::glossary_1::MediaDestinationId> retPossibleOptionsListCdm = std::get<1>(allPossibleOutputBinValueResult);

        auto outputDestination = dune::job::cdm::mapToCdm(this->getIntent()->getOutputDestination());
        bool notExistValueInCurrentDestination = (std::find(retPossibleOptionsListCdm.begin(), retPossibleOptionsListCdm.end(), outputDestination)
                                                                        == retPossibleOptionsListCdm.end());

        if(outputDestination == dune::cdm::glossary_1::MediaDestinationId::standard_dash_bin || notExistValueInCurrentDestination )
        {
            auto outputDestination = dune::cdm::glossary_1::MediaDestinationId::alternate;
            if(std::find(retPossibleOptionsListCdm.begin(), retPossibleOptionsListCdm.end(), outputDestination)
                == retPossibleOptionsListCdm.end())
            {
                this->getIntent()->setOutputDestination(dune::imaging::types::MediaDestinationId::AUTOSELECT);
            }
            else
            {
                this->getIntent()->setOutputDestination(dune::imaging::types::MediaDestinationId::OUTPUTBIN1);
            }
            CHECKPOINTA("CopyJobTicket::UpdateMediaOutputDestinationPageBasedFinisherInstalled() set %d", this->getIntent()->getOutputDestination());
            return true;
        }
    }
    return false;
}

std::string CopyJobTicket::getConstraintsMsgBetweenFinisherOption(MediaProcessingTypes mediaProcessingType) const
{
    StapleOptions stapleOption = copyJobIntent_->getStapleOption();
    PunchingOptions punchOption = copyJobIntent_->getPunchOption();
    FoldingOptions foldOption = copyJobIntent_->getFoldOption();
    BookletMakingOptions bookletMakerOption = copyJobIntent_->getBookletMakerOption();
    std::string selectOptionStr = "";
    std::string constraintsMsg = "";

    if(localization_ == nullptr)
    {
        CHECKPOINTA("getConstraintsMsgBetweenFinisherOption: ERROR localization_ is null");
        return constraintsMsg;
    }
    
    if(dune::copy::Jobs::Copy::constraintsFb_)
    {
        if(MediaProcessingTypes::STAPLE == mediaProcessingType)
        {
            if(foldOption != FoldingOptions::NONE)
            {
                selectOptionStr = "FOLD_STAPLE";
            }
            else if(bookletMakerOption != BookletMakingOptions::NONE)
            {
                selectOptionStr = "BOOKLET_STAPLE";
            }
        }
        else if(MediaProcessingTypes::PUNCH == mediaProcessingType)
        {
            if(foldOption != FoldingOptions::NONE)
            {
                selectOptionStr = "FOLD_PUNCH";
            }
            else if(bookletMakerOption != BookletMakingOptions::NONE)
            {
                selectOptionStr = "BOOKLET_PUNCH";
            }
        }
        else if(MediaProcessingTypes::FOLD == mediaProcessingType)
        {
            if(stapleOption != StapleOptions::NONE && punchOption != PunchingOptions::NONE)
            {
                selectOptionStr = "STAPLE_PUNCH_FOLD";
            }
            else if(stapleOption != StapleOptions::NONE)
            {
                selectOptionStr = "STAPLE_FOLD";
            }
            else if(punchOption != PunchingOptions::NONE)
            {
                selectOptionStr = "PUNCH_FOLD";
            }
            else if(bookletMakerOption != BookletMakingOptions::NONE)
            {
                selectOptionStr = "BOOKLET_FOLD";
            }
        }
        else if(MediaProcessingTypes::BOOKLET_MAKING == mediaProcessingType)
        {
            if(stapleOption != StapleOptions::NONE && punchOption != PunchingOptions::NONE)
            {
                selectOptionStr = "STAPLE_PUNCH_BOOKLET";
            }
            else if(stapleOption != StapleOptions::NONE)
            {
                selectOptionStr = "STAPLE_BOOKLET";
            }
            else if(punchOption != PunchingOptions::NONE)
            {
                selectOptionStr = "PUNCH_BOOKLET";
            }
            else if(foldOption != FoldingOptions::NONE)
            {
                selectOptionStr = "FOLD_BOOKLET";
            }
        }
        else
        {
            ;
        }

        std::shared_ptr<dune::copy::Jobs::Copy::CopyJobConstraintsFbT> constraintsFb = dune::copy::Jobs::Copy::constraintsFb_;
        if(!constraintsFb->finisherOptionStrings.empty())
        {
            std::vector<std::shared_ptr<NameValueMatchingIdFbT>> vectorMap = constraintsFb->finisherOptionStrings;
            std::vector<std::shared_ptr<NameValueMatchingIdFbT>>::iterator iteratorVectorMap = std::find_if(vectorMap.begin(), vectorMap.end(),
                [&](std::shared_ptr<NameValueMatchingIdFbT> keyValue)
                {
                    return (keyValue->nameValue == selectOptionStr);
                }
            );

            // Take value from map if setting value exist
            if(iteratorVectorMap != vectorMap.end())
            {
                std::string stringFromCsf = (*iteratorVectorMap)->stringId;
                CHECKPOINTC("getConstraintsMsgBetweenFinisherOption string id from csf %s", stringFromCsf.c_str());
                constraintsMsg = localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly(stringFromCsf.c_str()));
                CHECKPOINTC("getConstraintsMsgBetweenFinisherOption constraintsMsg %s", constraintsMsg.c_str());
            }
        }
    }
    return constraintsMsg;
}

void CopyJobTicket::getOutputMediaSizeIdTypeforFinisher(MediaSizeId& OutputMediaSizeId, MediaOrientation& OutputMediaOrientation, bool &isPossibleBothOrientation) const
{
    isPossibleBothOrientation = false;
    CHECKPOINTC("CopyJobTicket::getOutputMediaSizeIdTypeforFinisher() scan %d/%d  print %d/%d", 
                static_cast<int>(copyJobIntent_->getInputMediaSizeId()), static_cast<int>(copyJobIntent_->getScanFeedOrientation()),
                static_cast<int>(OutputMediaSizeId), static_cast<int>(OutputMediaOrientation));

    if(MediaSizeId::ANY == OutputMediaSizeId)
    {
        switch(copyJobIntent_->getInputMediaSizeId())
        {
            case MediaSizeId::ANY:
                OutputMediaSizeId = MediaSizeId::LETTER;
                OutputMediaOrientation = MediaOrientation::LANDSCAPE; 
                break;
            case MediaSizeId::MIXED_LETTER_LEGAL:
                OutputMediaSizeId = MediaSizeId::LEGAL;           
                OutputMediaOrientation = MediaOrientation::PORTRAIT;
                break;
            case MediaSizeId::MIXED_LETTER_LEDGER:
                OutputMediaSizeId = MediaSizeId::LEDGER;           
                OutputMediaOrientation = MediaOrientation::PORTRAIT;
                break;
            case MediaSizeId::MIXED_A4_A3:
                OutputMediaSizeId = MediaSizeId::A3;           
                OutputMediaOrientation = MediaOrientation::PORTRAIT;
                break;
            default:
                OutputMediaSizeId = copyJobIntent_->getInputMediaSizeId();
                if(dune::scan::types::ScanFeedOrientation::SHORTEDGE == copyJobIntent_->getScanFeedOrientation())     
                {
                    OutputMediaOrientation = MediaOrientation::PORTRAIT;
                }
                else
                {
                    OutputMediaOrientation = MediaOrientation::LANDSCAPE;
                }           
                break;
        }
    }

    if(OutputMediaSizeId == MediaSizeId::LETTER || OutputMediaSizeId == MediaSizeId::A4 
             || OutputMediaSizeId == MediaSizeId::A5 || OutputMediaSizeId == MediaSizeId::JIS_B5)
    {
        isPossibleBothOrientation = true;
    }
}

std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>> CopyJobTicket::getPossibleOutputBins() const
{
    const auto allPossibleOutputBinValueResult = dune::print::engine::MediaFinisherHelper::getAllPossibleOutputBins(mediaInterface_);
    std::vector<dune::cdm::glossary_1::MediaDestinationId> retPossibleOptionsList;

    if (APIResult::OK != std::get<0>(allPossibleOutputBinValueResult))
    {
        CHECKPOINTA("CopyJobTicket::getPossibleOutputBins(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>>(APIResult::ERROR, retPossibleOptionsList);
    }
    const auto possibleOptionsFromHelper = std::get<1>(allPossibleOutputBinValueResult);
    retPossibleOptionsList.push_back(dune::cdm::glossary_1::MediaDestinationId::auto_);
    for (const auto& OutputBin : possibleOptionsFromHelper)
    {
        auto curOutputBin = dune::job::cdm::mapToCdm(OutputBin);
        CHECKPOINTD("CopyJobTicket::getPossibleOutputBins() curOutputBin %d ", static_cast<int32_t>(curOutputBin));
        if (std::find(retPossibleOptionsList.begin(), retPossibleOptionsList.end(), curOutputBin)
            == retPossibleOptionsList.end())
        {
            retPossibleOptionsList.push_back(curOutputBin);
        }
    }
    return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>>(APIResult::OK, retPossibleOptionsList);
}

std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>> CopyJobTicket::getValidOutputBins() const
{
    std::vector<dune::cdm::glossary_1::MediaDestinationId> retValidOptionsList;

    dune::imaging::types::ContentOrientation originalOrientation = copyJobIntent_->getContentOrientation();
 
    MediaSizeId OutputMediaSizeId{copyJobIntent_->getOutputMediaSizeId()};
    MediaOrientation OutputMediaOrientation{copyJobIntent_->getOutputMediaOrientation()};
    bool isPossibleBothOrientation = false;
    getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);
    OrientedMediaSize outputOrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation(OutputMediaOrientation)});
    if(isPossibleBothOrientation)
    {
        outputOrientedMediaSize = OrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE});
    }

    MediaId mediaType(copyJobIntent_->getOutputMediaIdType());

    // TODO :: The code below will be modified after all finisher options are developed.
    StapleOptions stapleOption = copyJobIntent_->getStapleOption();
    PunchingOptions punchingOption = copyJobIntent_->getPunchOption();
    FoldingOptions foldingOption = copyJobIntent_->getFoldOption();
    BookletMakingOptions bookletMakingOption = copyJobIntent_->getBookletMakerOption();

    CHECKPOINTC("CopyJobTicket::getValidOutputBins(): OutputMediaSize %d/%d ", OutputMediaSizeId, OutputMediaOrientation);
    CHECKPOINTC("CopyJobTicket::getValidOutputBins(): originalOrientation %d", static_cast<int>(originalOrientation));
    CHECKPOINTC("CopyJobTicket::getValidOutputBins(): stapleOption  %d", static_cast<int>(stapleOption));
    CHECKPOINTC("CopyJobTicket::getValidOutputBins(): punchingOption %d", static_cast<int>(punchingOption));
    CHECKPOINTC("CopyJobTicket::getValidOutputBins(): foldingOption  %d", static_cast<int>(foldingOption));
    CHECKPOINTC("CopyJobTicket::getValidOutputBins(): bookletMakingOption %d", static_cast<int>(bookletMakingOption));

    const auto result = dune::print::engine::MediaFinisherHelper::getAllValidOutputBins(mediaInterface_, 
                                        outputOrientedMediaSize,mediaType,originalOrientation, stapleOption, punchingOption, foldingOption,bookletMakingOption,true);
    const auto retValue = std::get<0>(result);

    if (retValue != APIResult::OK)
    {
        CHECKPOINTA("CopyJobTicket::getValidOutputBins(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>>(APIResult::ERROR, retValidOptionsList);
    }
    const auto validOptionsFromHelper = std::get<1>(result);
    retValidOptionsList.push_back(dune::cdm::glossary_1::MediaDestinationId::auto_);
    for (const auto& OutputBin : validOptionsFromHelper)
    {
        auto curOutputBin = dune::job::cdm::mapToCdm(OutputBin);
        CHECKPOINTD("CopyJobTicket::getValidOutputBins() curOutputBin %d ", static_cast<int32_t>(curOutputBin));
        if (std::find(retValidOptionsList.begin(), retValidOptionsList.end(), curOutputBin)
            == retValidOptionsList.end())
        {
            retValidOptionsList.push_back(curOutputBin);
        }
    }
    return std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>>(APIResult::OK, retValidOptionsList);
}

std::string CopyJobTicket::getStapleString(dune::imaging::types::StapleOptions stapleOption) const
{
    if(dune::copy::Jobs::Copy::constraintsFb_)
    {
        std::shared_ptr<dune::copy::Jobs::Copy::CopyJobConstraintsFbT> constraintsFb = dune::copy::Jobs::Copy::constraintsFb_;
        std::string cdmStapleOptionstr = dune::cdm::jobTicket_1::StapleOptionsEnum::valueToString(dune::job::cdm::mapToCdm(stapleOption));

        if(!constraintsFb->stapleOptionStr.empty())
        {
            std::vector<std::shared_ptr<NameValueMatchingIdFbT>> vectorMap = constraintsFb->stapleOptionStr;
            std::vector<std::shared_ptr<NameValueMatchingIdFbT>>::iterator iteratorVectorMap = std::find_if(vectorMap.begin(), vectorMap.end(),
                [&](std::shared_ptr<NameValueMatchingIdFbT> keyValue)
                {
                    CHECKPOINTD("getStapleString keyValue->nameValue %s, cdmStapleOptionstr %s", keyValue->nameValue.c_str(), cdmStapleOptionstr.c_str());
                    return (keyValue->nameValue == cdmStapleOptionstr);
                }
            );

            // Take value from map if setting value exist
            if(iteratorVectorMap != vectorMap.end())
            {
                std::string stringFromCsf = (*iteratorVectorMap)->stringId;
                CHECKPOINTC("getStapleString string id from csf %s", stringFromCsf.c_str());
                return stringFromCsf;
            }
            return nullptr;
        }
        return nullptr;
    }
    return nullptr;
}

std::string CopyJobTicket::getHolePunchString(dune::imaging::types::PunchingOptions punchOption) const
{
    if(dune::copy::Jobs::Copy::constraintsFb_)
    {
        std::shared_ptr<dune::copy::Jobs::Copy::CopyJobConstraintsFbT> constraintsFb = dune::copy::Jobs::Copy::constraintsFb_;
        std::string cdmPunchOptionstr = dune::cdm::jobTicket_1::PunchOptionsEnum::valueToString(dune::job::cdm::mapToCdm(punchOption));

        if(!constraintsFb->punchOptionStr.empty())
        {
            std::vector<std::shared_ptr<NameValueMatchingIdFbT>> vectorMap = constraintsFb->punchOptionStr;
            std::vector<std::shared_ptr<NameValueMatchingIdFbT>>::iterator iteratorVectorMap = std::find_if(vectorMap.begin(), vectorMap.end(),
                [&](std::shared_ptr<NameValueMatchingIdFbT> keyValue)
                {
                    CHECKPOINTD("getHolePunchString keyValue->nameValue %s, cdmPunchOptionstr %s", keyValue->nameValue.c_str(), cdmPunchOptionstr.c_str());
                    return (keyValue->nameValue == cdmPunchOptionstr);
                }
            );

            // Take value from map if setting value exist
            if(iteratorVectorMap != vectorMap.end())
            {
                std::string stringFromCsf = (*iteratorVectorMap)->stringId;
                CHECKPOINTC("getHolePunchString string id from csf %s", stringFromCsf.c_str());
                return stringFromCsf;
            }
            return nullptr;
        }
        return nullptr;
    }
    return nullptr;
}

std::string CopyJobTicket::getFinisherConstraintString(std::string constraintString) const
{
    std::string stringFromCsf;

    if(dune::copy::Jobs::Copy::constraintsFb_)
    {
        std::shared_ptr<dune::copy::Jobs::Copy::CopyJobConstraintsFbT> constraintsFb = dune::copy::Jobs::Copy::constraintsFb_;

        if(!constraintsFb->finisherConstraintString.empty())
        {
            std::vector<std::shared_ptr<NameValueMatchingIdFbT>> vectorMap = constraintsFb->finisherConstraintString;
            std::vector<std::shared_ptr<NameValueMatchingIdFbT>>::iterator iteratorVectorMap = std::find_if(vectorMap.begin(), vectorMap.end(),
                [&](std::shared_ptr<NameValueMatchingIdFbT> keyValue)
                {
                    CHECKPOINTD("getFinisherConstraintString keyValue->nameValue %s, constraintString %s", keyValue->nameValue.c_str(), constraintString.c_str());
                    return (keyValue->nameValue == constraintString);
                }
            );

            // Take value from map if setting value exist
            if(iteratorVectorMap != vectorMap.end())
            {
                stringFromCsf = (*iteratorVectorMap)->stringId;
                CHECKPOINTC("getFinisherConstraintString string id from csf %s", stringFromCsf.c_str());
                return stringFromCsf;
            }
            return nullptr;
        }
        return nullptr;
    }
    return nullptr;
}

bool CopyJobTicket::isValidStaplingOptionForCopy(dune::cdm::jobTicket_1::StapleOptions stapleOption) const
{
     return stapleOption != dune::cdm::jobTicket_1::StapleOptions::leftTwoPointsAny;
}

std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>> CopyJobTicket::getPossibleStaplingOptions() const
{
    std::vector<dune::cdm::jobTicket_1::StapleOptions> retPossibleOptionsList;
    const auto result = dune::print::engine::MediaFinisherHelper::getAllPossibleStaplingOptions(mediaInterface_);
    const auto retValue = std::get<0>(result);

    if (retValue != APIResult::OK)
    {
        CHECKPOINTA("CopyJobTicket::getPossibleStaplingOptions(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>>(APIResult::ERROR, retPossibleOptionsList);
    }
    const auto possibleOptionsFromHelper = std::get<1>(result);
    for (const auto& stapleOption : possibleOptionsFromHelper)
    {
        auto curStapleOption = dune::job::cdm::mapToCdm(stapleOption);
        if ( isValidStaplingOptionForCopy(curStapleOption) &&
            std::find(retPossibleOptionsList.begin(), retPossibleOptionsList.end(), curStapleOption) == retPossibleOptionsList.end())
        {
            retPossibleOptionsList.push_back(curStapleOption);
        }
    }
    return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>>(APIResult::OK, retPossibleOptionsList);
}

std::string CopyJobTicket::getStapleConstraintsString(std::vector<StapleOptions> validOptionsFromHelper) const
{
    PunchingOptions punchOption = copyJobIntent_->getPunchOption();
    std::string message;
    std::string options;

    CHECKPOINTD("CopyJobTicket::getStapleConstraintsString(): Enter [%d]",validOptionsFromHelper.size());

    if((punchOption != PunchingOptions::NONE) && (1 != validOptionsFromHelper.size()))
    {
        dune::localization::ParameterizedStringType* parameterizedIncompatibleSettingString;

        if(2 == validOptionsFromHelper.size()) /* Only one Valid option without NONE */
        {
            parameterizedIncompatibleSettingString = new dune::localization::ParameterizedStringType(
                localization_->deviceLocale()->getStringIdForCsfOnly(getFinisherConstraintString("cStapleConstraint").c_str()),
                localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly(getHolePunchString(punchOption).c_str())));
        }
        else
        {
            parameterizedIncompatibleSettingString = new dune::localization::ParameterizedStringType(
                localization_->deviceLocale()->getStringIdForCsfOnly(getFinisherConstraintString("cHolePunchStapleConstraint").c_str()),
                localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly(getHolePunchString(punchOption).c_str())));
        }

        message = localization_->deviceLocale()->format(parameterizedIncompatibleSettingString);
        delete parameterizedIncompatibleSettingString;

        for (const auto& stapleOption : validOptionsFromHelper)
        {
            if(StapleOptions::NONE != stapleOption)
            {
                options = options + "\n * " + localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly(getStapleString(stapleOption).c_str()));
            }
        }
        message = message + options;
    }
    else
    {
        message = localization_->deviceLocale()->get(dune::localization::string_id::cUnavailable);
    }
    CHECKPOINTD("CopyJobTicket::getStapleConstraintsString(): exit message %s", message.c_str());
    return message;
}

std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>> CopyJobTicket::getValidStaplingOptions(std::string &constraintsmsg) const
{
    std::vector<dune::cdm::jobTicket_1::StapleOptions> retValidOptionsList;
    dune::imaging::types::ContentOrientation originalOrientation = copyJobIntent_->getContentOrientation();
    if(copyJobIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp)
    {
        if(originalOrientation == dune::imaging::types::ContentOrientation::LANDSCAPE)
        {
            originalOrientation = dune::imaging::types::ContentOrientation::PORTRAIT;
        }
        else
        {
            originalOrientation = dune::imaging::types::ContentOrientation::LANDSCAPE;
        }
    }
    MediaSizeId OutputMediaSizeId{copyJobIntent_->getOutputMediaSizeId()};
    MediaOrientation OutputMediaOrientation{copyJobIntent_->getOutputMediaOrientation()};
    bool isPossibleBothOrientation = false;
    getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);
    OrientedMediaSize outputOrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation(OutputMediaOrientation)});
    if(isPossibleBothOrientation)
    {
        outputOrientedMediaSize = OrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE});
    }

    MediaId mediaType(copyJobIntent_->getOutputMediaIdType());
    PunchingOptions punchingOption = copyJobIntent_->getPunchOption();
    FoldingOptions foldingOption =  copyJobIntent_->getFoldOption();
    BookletMakingOptions bookletMakingOption = copyJobIntent_->getBookletMakerOption();
    MediaDestinationId mediaDestinationId = copyJobIntent_->getOutputDestination();

    CHECKPOINTC("CopyJobTicket::getValidStaplingOptions(): OutputMediaSize %d/%d ", OutputMediaSizeId, OutputMediaOrientation);
    CHECKPOINTC("CopyJobTicket::getValidStaplingOptions(): copyJobIntent_->getOutputMediaOrientation() %d", static_cast<int>(copyJobIntent_->getOutputMediaOrientation()));
    CHECKPOINTC("CopyJobTicket::getValidStaplingOptions(): mediaType %d", static_cast<int>(mediaType.getType()));
    CHECKPOINTC("CopyJobTicket::getValidStaplingOptions(): originalOrientation %d", static_cast<int>(originalOrientation));
    CHECKPOINTC("CopyJobTicket::getValidStaplingOptions(): punchingOption %d", static_cast<int>(punchingOption));
    CHECKPOINTC("CopyJobTicket::getValidStaplingOptions(): foldingOption  %d", static_cast<int>(foldingOption));
    CHECKPOINTC("CopyJobTicket::getValidStaplingOptions(): bookletMakingOption %d", static_cast<int>(bookletMakingOption));
    CHECKPOINTC("CopyJobTicket::getValidStaplingOptions(): mediaDestinationId  %d", static_cast<int>(mediaDestinationId));

    const auto result = dune::print::engine::MediaFinisherHelper::getAllValidStaplingOptions(mediaInterface_, 
                                        outputOrientedMediaSize,mediaType,originalOrientation, punchingOption, foldingOption, bookletMakingOption,mediaDestinationId,true);
    const auto retValue = std::get<0>(result);
    const auto validOptionsFromHelper = std::get<1>(result);

    if (retValue != APIResult::OK || 1 == validOptionsFromHelper.size())
    {
        CHECKPOINTA("CopyJobTicket::getValidStaplingOptions(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>>(APIResult::ERROR, retValidOptionsList);
    }
    
    constraintsmsg = getStapleConstraintsString(std::get<1>(result));
    for (const auto& stapleOption : validOptionsFromHelper)
    {
        auto curStapleOption = dune::job::cdm::mapToCdm(stapleOption);
        if (isValidStaplingOptionForCopy(curStapleOption) &&
            std::find(retValidOptionsList.begin(), retValidOptionsList.end(), curStapleOption) == retValidOptionsList.end())
        {
            retValidOptionsList.push_back(curStapleOption);
        }
    }
    return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>>(APIResult::OK, retValidOptionsList);
}

bool CopyJobTicket::isValidPunchingOptionForCopy(dune::cdm::jobTicket_1::PunchOptions punchOption) const
{
     return punchOption != dune::cdm::jobTicket_1::PunchOptions::fourPointDin &&
            punchOption != dune::cdm::jobTicket_1::PunchOptions::twoPointDin &&
            punchOption != dune::cdm::jobTicket_1::PunchOptions::threePointUs &&
            punchOption != dune::cdm::jobTicket_1::PunchOptions::twoPointUs &&
            punchOption != dune::cdm::jobTicket_1::PunchOptions::fourPointSwd;
}

std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>> CopyJobTicket::getPossiblePunchingOptions() const
{
    std::vector<dune::cdm::jobTicket_1::PunchOptions> retPossibleOptionsList;

    const auto result = dune::print::engine::MediaFinisherHelper::getAllPossiblePunchingOptions(mediaInterface_);
    const auto retValue = std::get<0>(result);

    if (retValue != APIResult::OK)
    {
        CHECKPOINTA("CopyJobTicket::getPossiblePunchingOptions(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>>(APIResult::ERROR, retPossibleOptionsList);
    }
    const auto possibleOptionsFromHelper = std::get<1>(result);
    for (const auto& punchOption : possibleOptionsFromHelper)
    {
        auto curPunchOption = dune::job::cdm::mapToCdm(punchOption);
        if ( isValidPunchingOptionForCopy(curPunchOption) &&
            (std::find(retPossibleOptionsList.begin(), retPossibleOptionsList.end(), curPunchOption) == retPossibleOptionsList.end()))
        {
            retPossibleOptionsList.push_back(curPunchOption);
        }
    }
    return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>>(APIResult::OK, retPossibleOptionsList);
}

std::string CopyJobTicket::getHolePunchConstraintsString(std::vector<PunchingOptions> validOptionsFromHelper) const
{
    StapleOptions stapleOption = copyJobIntent_->getStapleOption();
    std::string message;
    std::string options;

    CHECKPOINTD("CopyJobTicket::getHolePunchConstraintsString(): Enter [%d]",validOptionsFromHelper.size());

    if((stapleOption != StapleOptions::NONE) && (1 != validOptionsFromHelper.size()))
    {
        dune::localization::ParameterizedStringType* parameterizedIncompatibleSettingString;

        if(2 == validOptionsFromHelper.size()) /* Only one Valid option without NONE */
        {
            parameterizedIncompatibleSettingString = new dune::localization::ParameterizedStringType(
                localization_->deviceLocale()->getStringIdForCsfOnly(getFinisherConstraintString("cHolePunchConstraint").c_str()),
                localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly( getStapleString(stapleOption).c_str())));// getStapleString(stapleOption));
        }
        else
        {
            parameterizedIncompatibleSettingString = new dune::localization::ParameterizedStringType(
                localization_->deviceLocale()->getStringIdForCsfOnly(getFinisherConstraintString("cStapleHolePunchConstraint").c_str()),
                localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly( getStapleString(stapleOption).c_str())));//getStapleString(stapleOption));
        }

        message = localization_->deviceLocale()->format(parameterizedIncompatibleSettingString);
        delete parameterizedIncompatibleSettingString;

        for (const auto& punchOption : validOptionsFromHelper)
        {
            if(PunchingOptions::NONE != punchOption)
            {
                options = options + "\n * " + localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly(getHolePunchString(punchOption).c_str()));
            }
        }
        message = message + options;
    }
    else
    {
        message = localization_->deviceLocale()->get(dune::localization::string_id::cUnavailable);
    }
    CHECKPOINTD("CopyJobTicket::getHolePunchConstraintsString(): exit message %s", message.c_str());
    return message;
}

std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>> CopyJobTicket::getValidPunchingOptions(std::string &constraintsmsg) const
{
    std::vector<dune::cdm::jobTicket_1::PunchOptions> retValidOptionsList;

    dune::imaging::types::ContentOrientation originalOrientation = copyJobIntent_->getContentOrientation();
    if(copyJobIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp)
    {
        if(originalOrientation == dune::imaging::types::ContentOrientation::LANDSCAPE)
        {
            originalOrientation = dune::imaging::types::ContentOrientation::PORTRAIT;
        }
        else
        {
            originalOrientation = dune::imaging::types::ContentOrientation::LANDSCAPE;
        }
    }
    MediaSizeId OutputMediaSizeId{copyJobIntent_->getOutputMediaSizeId()};
    MediaOrientation OutputMediaOrientation{copyJobIntent_->getOutputMediaOrientation()};
    bool isPossibleBothOrientation = false;
    getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);
    OrientedMediaSize outputOrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation(OutputMediaOrientation)});
    if(isPossibleBothOrientation)
    {
        outputOrientedMediaSize = OrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE});
    }

    MediaId mediaType(copyJobIntent_->getOutputMediaIdType());
    StapleOptions stapleOption = copyJobIntent_->getStapleOption();
    FoldingOptions foldingOption = copyJobIntent_->getFoldOption();
    BookletMakingOptions bookletMakingOption = copyJobIntent_->getBookletMakerOption();
    MediaDestinationId mediaDestinationId = copyJobIntent_->getOutputDestination();

    CHECKPOINTC("CopyJobTicket::getValidPunchingOptions(): OutputMediaSize %d/%d ", OutputMediaSizeId, OutputMediaOrientation);
    CHECKPOINTC("CopyJobTicket::getValidPunchingOptions(): mediaType %d", static_cast<int>(mediaType.getType()));
    CHECKPOINTC("CopyJobTicket::getValidPunchingOptions(): originalOrientation %d", static_cast<int>(originalOrientation));
    CHECKPOINTC("CopyJobTicket::getValidPunchingOptions(): stapleOption %d", static_cast<int>(stapleOption));
    CHECKPOINTC("CopyJobTicket::getValidPunchingOptions(): foldingOption  %d", static_cast<int>(foldingOption));
    CHECKPOINTC("CopyJobTicket::getValidPunchingOptions(): bookletMakingOption %d", static_cast<int>(bookletMakingOption));
    CHECKPOINTC("CopyJobTicket::getValidPunchingOptions(): mediaDestinationId  %d", static_cast<int>(mediaDestinationId));

    const auto result = dune::print::engine::MediaFinisherHelper::getAllValidPunchingOptions(mediaInterface_, 
                                        outputOrientedMediaSize,mediaType,originalOrientation, stapleOption, foldingOption, bookletMakingOption,mediaDestinationId,true);
    const auto retValue = std::get<0>(result);
    const auto validOptionsFromHelper = std::get<1>(result);

    if (retValue != APIResult::OK || 1 == validOptionsFromHelper.size())
    {
        CHECKPOINTA("CopyJobTicket::getValidPunchingOptions(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>>(APIResult::ERROR, retValidOptionsList);
    }

    constraintsmsg = getHolePunchConstraintsString(std::get<1>(result));
    for (const auto& punchOption : validOptionsFromHelper)
    {
        auto curPunchOption = dune::job::cdm::mapToCdm(punchOption);
        if ( isValidPunchingOptionForCopy(curPunchOption) && 
            (std::find(retValidOptionsList.begin(), retValidOptionsList.end(), curPunchOption) == retValidOptionsList.end()))
        {
            retValidOptionsList.push_back(curPunchOption);
        }
    }
    return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>>(APIResult::OK, retValidOptionsList);
}

std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>> CopyJobTicket::getPossibleFoldingOptions() const
{
    std::vector<dune::cdm::jobTicket_1::FoldOptions> retPossibleOptionsList;

    const auto result = dune::print::engine::MediaFinisherHelper::getAllPossibleFoldingOptions(mediaInterface_);
    const auto retValue = std::get<0>(result);

    if (retValue != APIResult::OK)
    {
        CHECKPOINTA("CopyJobTicket::getPossibleFoldingOptions(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>>(APIResult::ERROR, retPossibleOptionsList);
    }
    const auto possibleOptionsFromHelper = std::get<1>(result);
    for (const auto& foldOption : possibleOptionsFromHelper)
    {
        auto curFoldOption = dune::job::cdm::mapToCdm(foldOption);
        if (std::find(retPossibleOptionsList.begin(), retPossibleOptionsList.end(), curFoldOption)
            == retPossibleOptionsList.end())
        {
            retPossibleOptionsList.push_back(curFoldOption);
        }

    }
    return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>>(APIResult::OK, retPossibleOptionsList);
}

std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>> CopyJobTicket::getValidFoldingOptions(std::string &constraintsmsg) const
{
    std::vector<dune::cdm::jobTicket_1::FoldOptions> retValidOptionsList;

    dune::imaging::types::ContentOrientation originalOrientation = copyJobIntent_->getContentOrientation();
    MediaSizeId OutputMediaSizeId{copyJobIntent_->getOutputMediaSizeId()};
    MediaOrientation OutputMediaOrientation{copyJobIntent_->getOutputMediaOrientation()};
    bool isPossibleBothOrientation = false;
    getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);
    OrientedMediaSize outputOrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation(OutputMediaOrientation)});
    if(isPossibleBothOrientation)
    {
        outputOrientedMediaSize = OrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE});
    }
    
    MediaId mediaType(copyJobIntent_->getOutputMediaIdType());
    StapleOptions stapleOption = copyJobIntent_->getStapleOption();
    PunchingOptions punchingOption = copyJobIntent_->getPunchOption();
    BookletMakingOptions bookletMakingOption = copyJobIntent_->getBookletMakerOption();
    MediaDestinationId mediaDestinationId = copyJobIntent_->getOutputDestination();

    CHECKPOINTC("CopyJobTicket::getValidFoldOptions(): OutputMediaSize %d/%d ", OutputMediaSizeId, OutputMediaOrientation);
    CHECKPOINTC("CopyJobTicket::getValidFoldOptions(): mediaType %d", static_cast<int>(mediaType.getType()));
    CHECKPOINTC("CopyJobTicket::getValidFoldOptions(): originalOrientation %d", static_cast<int>(originalOrientation));
    CHECKPOINTC("CopyJobTicket::getValidFoldOptions(): stapleOption %d", static_cast<int>(stapleOption));
    CHECKPOINTC("CopyJobTicket::getValidFoldOptions(): punchingOption  %d", static_cast<int>(punchingOption));
    CHECKPOINTC("CopyJobTicket::getValidFoldOptions(): bookletMakingOption %d", static_cast<int>(bookletMakingOption));
    CHECKPOINTC("CopyJobTicket::getValidFoldOptions(): mediaDestinationId  %d", static_cast<int>(mediaDestinationId));

    const auto result = dune::print::engine::MediaFinisherHelper::getAllValidFoldingOptions(mediaInterface_, 
                                        outputOrientedMediaSize,mediaType,originalOrientation, stapleOption, punchingOption, bookletMakingOption,mediaDestinationId,true);
    const auto retValue = std::get<0>(result);
    const auto validOptionsFromHelper = std::get<1>(result);

    if (retValue != APIResult::OK || 1 == validOptionsFromHelper.size())
    {
        CHECKPOINTA("CopyJobTicket::getValidFoldOptions(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>>(APIResult::ERROR, retValidOptionsList);
    }

    CHECKPOINTA("CopyJobTicket::getValidFoldOptions(): validOptionsFromHelper size[%d] ",validOptionsFromHelper.size());
    //constraintsmsg = getHolePunchConstraintsString(std::get<1>(result));
    for (const auto& foldOption : validOptionsFromHelper)
    {
        auto curFoldOption = dune::job::cdm::mapToCdm(foldOption);
        if (std::find(retValidOptionsList.begin(), retValidOptionsList.end(), curFoldOption) == retValidOptionsList.end())
        {
            if(!((copyJobIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::FourUp
                || copyJobIntent_->getBookletFormat() == dune::imaging::types::BookletFormat::LeftEdge)
                && (curFoldOption == dune::cdm::jobTicket_1::FoldOptions::cInwardTop 
                || curFoldOption == dune::cdm::jobTicket_1::FoldOptions::cInwardBottom
                || curFoldOption == dune::cdm::jobTicket_1::FoldOptions::cOutwardTop
                || curFoldOption == dune::cdm::jobTicket_1::FoldOptions::cOutwardBottom)))
            {
                retValidOptionsList.push_back(curFoldOption);
            }    
        }
    }
    return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>>(APIResult::OK, retValidOptionsList);
}

std::tuple<int, int> CopyJobTicket::getPagesPerSetLimitForFinishingOption(FoldingOptions foldingOption, BookletMakingOptions bookletMakingOption) const
{
    int minVal;
    int maxVal;

    if(foldingOption != FoldingOptions::NONE)
    {
        const auto result = dune::print::engine::MediaFinisherHelper::getPagesPerSetLimitForFinishingOption(mediaInterface_,foldingOption);
        const auto retValue = std::get<0>(result);

        if (retValue != APIResult::OK)
        {
            if(dune::copy::Jobs::Copy::constraintsFb_)
            {
                if(foldingOption == FoldingOptions::C_INWARD_TOP)
                {
                    minVal = constraintsFb_->minSheetsPerSetForCFold; 
                    maxVal = constraintsFb_->maxSheetsPerSetForCFold; 
                }
                else
                {
                    minVal = constraintsFb_->minSheetsPerSetForVFold; 
                    maxVal = constraintsFb_->maxSheetsPerSetForVFold; 
                }
            }
        }
        else
        {
            minVal = std::get<1>(result).min.get(1);
            maxVal = std::get<1>(result).max.get(1);
        }
    }
    else
    {
        const auto result = dune::print::engine::MediaFinisherHelper::getPagesPerSetLimitForFinishingOption(mediaInterface_,bookletMakingOption);
        const auto retValue = std::get<0>(result);

        if (retValue != APIResult::OK)
        {
            if(dune::copy::Jobs::Copy::constraintsFb_)
            {
                minVal = constraintsFb_->minSheetsPerSetForFoldAndStitch; 
                maxVal = constraintsFb_->maxSheetsPerSetForFoldAndStitch; 
            }
        }
        else
        {
            minVal = std::get<1>(result).min.get(1);
            maxVal = std::get<1>(result).max.get(1);
        }
    }
    return std::tuple<int, int>(minVal, maxVal);
}

std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>> CopyJobTicket::getPossibleBookletMakingOptions() const
{
    std::vector<dune::cdm::jobTicket_1::BookletMakerOptions> retPossibleOptionsList;

    const auto result = dune::print::engine::MediaFinisherHelper::getAllPossibleBookletMakingOptions(mediaInterface_);
    const auto retValue = std::get<0>(result);

    if (retValue != APIResult::OK)
    {
        CHECKPOINTA("CopyJobTicket::getPossibleBookletMakingOptions(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>>(APIResult::ERROR, retPossibleOptionsList);
    }
    const auto possibleOptionsFromHelper = std::get<1>(result);
    for (const auto& bookletOption : possibleOptionsFromHelper)
    {
        auto curBookletOption = dune::job::cdm::mapToCdm(bookletOption);
        if (std::find(retPossibleOptionsList.begin(), retPossibleOptionsList.end(), curBookletOption)
            == retPossibleOptionsList.end())
        {
            retPossibleOptionsList.push_back(curBookletOption);
        }

    }
    return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>>(APIResult::OK, retPossibleOptionsList);
}

std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>> CopyJobTicket::getValidBookletMakingOptions(std::string &constraintsmsg) const
{
    std::vector<dune::cdm::jobTicket_1::BookletMakerOptions> retValidOptionsList;

    dune::imaging::types::ContentOrientation originalOrientation = copyJobIntent_->getContentOrientation();
    MediaSizeId OutputMediaSizeId{copyJobIntent_->getOutputMediaSizeId()};
    MediaOrientation OutputMediaOrientation{copyJobIntent_->getOutputMediaOrientation()};
    bool isPossibleBothOrientation = false;
    getOutputMediaSizeIdTypeforFinisher(OutputMediaSizeId, OutputMediaOrientation, isPossibleBothOrientation);
    OrientedMediaSize outputOrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation(OutputMediaOrientation)});
    if(isPossibleBothOrientation)
    {
        outputOrientedMediaSize = OrientedMediaSize(MediaSize(OutputMediaSizeId), {MediaOrientation::PORTRAIT, MediaOrientation::LANDSCAPE});
    }

    MediaId mediaType(copyJobIntent_->getOutputMediaIdType());
    StapleOptions stapleOption = copyJobIntent_->getStapleOption();
    PunchingOptions punchingOption = copyJobIntent_->getPunchOption();
    FoldingOptions foldingOption = copyJobIntent_->getFoldOption();
    MediaDestinationId mediaDestinationId =  copyJobIntent_->getOutputDestination();

    CHECKPOINTC("CopyJobTicket::getValidBookletMakingOptions(): OutputMediaSize %d/%d ", OutputMediaSizeId, OutputMediaOrientation);
    CHECKPOINTC("CopyJobTicket::getValidBookletMakingOptions(): mediaType %d", static_cast<int>(mediaType.getType()));
    CHECKPOINTC("CopyJobTicket::getValidBookletMakingOptions(): originalOrientation %d", static_cast<int>(originalOrientation));
    CHECKPOINTC("CopyJobTicket::getValidBookletMakingOptions(): stapleOption %d", static_cast<int>(stapleOption));
    CHECKPOINTC("CopyJobTicket::getValidBookletMakingOptions(): punchingOption  %d", static_cast<int>(punchingOption));
    CHECKPOINTC("CopyJobTicket::getValidBookletMakingOptions(): foldingOption %d", static_cast<int>(foldingOption));
    CHECKPOINTC("CopyJobTicket::getValidBookletMakingOptions(): mediaDestinationId  %d", static_cast<int>(mediaDestinationId));

    const auto result = dune::print::engine::MediaFinisherHelper::getAllValidBookletMakingOptions(mediaInterface_, 
                                        outputOrientedMediaSize,mediaType,originalOrientation, stapleOption, punchingOption, foldingOption, mediaDestinationId, true);
    const auto retValue = std::get<0>(result);
    const auto validOptionsFromHelper = std::get<1>(result);

    if (retValue != APIResult::OK || 1 == validOptionsFromHelper.size())
    {
        CHECKPOINTA("CopyJobTicket::getValidBookletMakingOptions(): APIResult::ERROR");
        return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>>(APIResult::ERROR, retValidOptionsList);
    }

    CHECKPOINTA("CopyJobTicket::getValidBookletMakingOptions(): validOptionsFromHelper size[%d] ",validOptionsFromHelper.size());
    //constraintsmsg = getHolePunchConstraintsString(std::get<1>(result));
    for (const auto& bookletOption : validOptionsFromHelper)
    {
        auto curBookletOption = dune::job::cdm::mapToCdm(bookletOption);
        if (std::find(retValidOptionsList.begin(), retValidOptionsList.end(), curBookletOption) == retValidOptionsList.end())
        {
            retValidOptionsList.push_back(curBookletOption);

        }
    }
    return std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>>(APIResult::OK, retValidOptionsList);
}

std::tuple<APIResult, std::vector<dune::imaging::types::MediaDestinationId>> CopyJobTicket::getOutputList() const
{
    return dune::print::engine::MediaHelper::getOutputList(mediaInterface_);
}

std::shared_ptr<ICopyPageTicket> CopyJobTicket::getCopyPageTicket(const dune::framework::core::Uuid& pageId)
{
    std::lock_guard<std::mutex> lock(copyTicketMutex_);
    CHECKPOINTD("CopyJobTicket::getCopyPageTicket() PageId: %s", pageId.toString().c_str());

    auto it = findPageTicket(pageId);
    if (it == copyPageTickets_.end())
    {
        return nullptr;
    }
    return *it;
}

std::shared_ptr<IPageTicket> CopyJobTicket::addPage(const Uuid& pageId)
{
    return addPage(pageId, nullptr);
}

std::shared_ptr<IPageTicket> CopyJobTicket::addPage(const Uuid&                                          pageId,
                                                    std::shared_ptr<dune::imaging::types::PageMetaInfoT> pageMetaInfo)
{
    std::lock_guard<std::mutex> lock(copyTicketMutex_);
    CHECKPOINTD("CopyJobTicket::addPage() PageId: %s", pageId.toString().c_str());

    // Check if pageId id has been added
    auto it = findPageTicket(pageId);
    if (it != copyPageTickets_.end())
    {
        CHECKPOINTD("CopyJobTicket::addPage() Page exists");
        return *it;
    }

    // Create a new pageId ticket for the pageId
    std::shared_ptr<CopyPageTicket> copyPageTicket = pageMetaInfo
                                                         ? std::make_shared<CopyPageTicket>(threadPool_, pageMetaInfo)
                                                         : std::make_shared<CopyPageTicket>(threadPool_);
    copyPageTicket->setPageId(pageId);
    copyPageTicket->setPageNumber(pageCount_);
    copyPageTickets_.emplace_back(copyPageTicket);

    auto pageTicketHandler = copyPageTicket->getHandler();

    if(pageMetaInfo && copyJobIntent_->getOutputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY)
    {
        auto orientation = dune::scan::types::ScanFeedOrientation::SHORTEDGE;
        if (pageMetaInfo->mediaOrientation == dune::imaging::types::MediaOrientation::LANDSCAPE)
        {
            orientation = dune::scan::types::ScanFeedOrientation::LONGEDGE;
        }
        copyJobIntent_->setScanFeedOrientation(orientation);
        copyJobIntent_->setMatchOriginalOutputMediaSizeId(pageMetaInfo->mediaSize);
        CHECKPOINTD("CopyJobTicket::addPage()  outputmediaSize: %d and MatchOriginalOutputMediaSize %d and orientation %d", copyJobIntent_->getOutputMediaSizeId(), 
                    copyJobIntent_->getMatchOriginalOutputMediaSizeId(), copyJobIntent_->getScanFeedOrientation());
    }

    // Create intents for the new page
    createIntents(copyPageTicket);

    updatePageIntents(copyPageTicket);

    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanPageIntent =
        std::static_pointer_cast<dune::scan::types::ScanTicketStruct>(
            pageTicketHandler->getIntent(dune::job::IntentType::SCAN));
    dune::job::IPageTicketHandler::InputDetails inputDetails{};
    inputDetails.requestedCopies = 1;
    if (scanPageIntent != nullptr)
    {
        inputDetails.resolution = scanPageIntent->getXImageQuality();
    }
    pageTicketHandler->setInputDetails(inputDetails);
    pageCount_++;

    return copyPageTicket;
}

void CopyJobTicket::removePage(const Uuid& pageId)
{
    {
        std::lock_guard<std::mutex> lock(copyTicketMutex_);
        CHECKPOINTD("CopyJobTicket::removePage() PageId: %s", pageId.toString().c_str());

        // Check if pageId id has been added
        auto it = findPageTicket(pageId);
        if (it == copyPageTickets_.end())
        {
            CHECKPOINTA("CopyJobTicket::removePage() Page doesn't exists");
            return;
        }

        copyPageTickets_.erase(it);
    }
    getHandler()->removePage(pageId);
}

std::shared_ptr<IPageTicket> CopyJobTicket::getPage(const Uuid& pageId)
{
    CHECKPOINTD("CopyJobTicket::getPage() PageId: %s", pageId.toString().c_str());
    return getCopyPageTicket(pageId);
}

std::vector<Uuid> CopyJobTicket::getPagesIds(dune::job::PageOrder orderBy) const
{
    std::lock_guard<std::mutex> lock(copyTicketMutex_);
    CHECKPOINTD("CopyJobTicket::getPagesIds() size: %d orderBy: %u", copyPageTickets_.size(), orderBy);
    return JobTicket::getPagesIds(copyPageTickets_, orderBy);
}

std::vector<std::shared_ptr<CopyPageTicket>>::iterator CopyJobTicket::findPageTicket(const Uuid& pageId)
{
    return std::find_if(
        copyPageTickets_.begin(), copyPageTickets_.end(),
        [pageId](const std::shared_ptr<CopyPageTicket>& pageTicket) { return pageId == pageTicket->getPageId(); });
}

std::vector<std::unique_ptr<CopyPageTicketFbT>> CopyJobTicket::serializePages() const
{
    std::lock_guard<std::mutex> lock(copyTicketMutex_);
    std::vector<std::unique_ptr<CopyPageTicketFbT>> pages;
    for (const auto& copyPageTicket : copyPageTickets_)
    {
        pages.emplace_back(copyPageTicket->serializeToFb());
    }
    return pages;
}

void CopyJobTicket::deserializePages(const std::vector<std::unique_ptr<CopyPageTicketFbT>>& pages)
{
    std::lock_guard<std::mutex> lock(copyTicketMutex_);
    for (const auto& page : pages)
    {
        std::shared_ptr<CopyPageTicket> copyPageTicket{std::make_shared<CopyPageTicket>()};
        copyPageTicket->deserializeFromFb(*page);
        copyPageTickets_.emplace_back(copyPageTicket);
    }
}

void CopyJobTicket::setPrintIntentsFactory(dune::print::engine::IPrintIntentsFactory* printIntentsFactory)
{
    printIntentsFactory_ = printIntentsFactory;
}

void CopyJobTicket::createIntents(std::shared_ptr<ICopyPageTicket> pageTicket)
{
    std::shared_ptr<dune::print::engine::PrintIntents> printIntent;

    if(printIntentsFactory_ != nullptr)
    {
        CHECKPOINTC("CopyJobTicket::createIntents Creating print inntent with the factory");
        printIntent = printIntentsFactory_->createPrintIntentsPage();
        //Update print intent with copy ticket settings
        updatePrintIntent(printIntent, pageTicket->getPageId());
    }
    else
    {
        CHECKPOINTC("CopyJobTicket::createIntents Creating default print intent");
        //Get default print intent
        printIntent = createDefaultPrintIntent();
    }

    //Set print intento to the page ticket
    pageTicket->setPrintIntent(printIntent);

    // Needed for ImageProcessor, nowdays created by default is enough, in future will be filled with print info
    std::shared_ptr<dune::imaging::types::IImagingIntent> imagingIntent =
        std::make_shared<dune::imaging::types::ImagingIntent>();
    pageTicket->setImagingIntent(imagingIntent);

    //Create scan page intent and set it to the page ticket
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanPageIntent = createScanPageIntent();
    pageTicket->setScanIntent(scanPageIntent);
}

void CopyJobTicket::updatePageIntents(std::shared_ptr<ICopyPageTicket> pageTicket)
{
    if(intentsManager_ != nullptr)
    {
        dune::job::IIntentsManager::IntentsMap intentsMap;
        intentsMap.addIntent(dune::job::IntentType::PRINT, pageTicket->getIntent(dune::job::IntentType::PRINT));
        intentsMap.addIntent(dune::job::IntentType::IMAGING, pageTicket->getIntent(dune::job::IntentType::IMAGING));

        pageIntent_.rotationCW = dune::imaging::ImagingUtilities::convertAnglesToRotationCW(copyJobIntent_->getRotation());
        pageIntent_.autoRotate = copyJobIntent_->getAutoRotate();
        pageIntent_.mediaFamily = copyJobIntent_->getMediaFamily();

        intentsManager_->updatePageIntents(pageIntent_, intentsMap);
    }
    else
    {
        CHECKPOINTC("CopyJobTicket::updatePageIntents() PageIntents not updated");
    }

}

bool CopyJobTicket::isRestrictColorPrint() 
{
    dune::imaging::ColorAccess colorAccess = dune::imaging::ColorAccess::ENABLED; // Default to enabled, if no access control is available.
    bool colorRestricted = false; // Default to not restricted.
    if (colorAccessControl_ != nullptr)
    {
        CHECKPOINTB("CopyJobTicket::isColorRestricted: checking color access control");
        dune::imaging::ColorAccess colorAccess = colorAccessControl_->getColorAccess();
        switch (colorAccess)
        {
            case dune::imaging::ColorAccess::ENABLED:
                CHECKPOINTB("CopyJobTicket::isColorRestricted: color access is ENABLED");
                colorRestricted=false; // Not restricted, color access is enabled.
                break;
            case dune::imaging::ColorAccess::DISABLED:
                CHECKPOINTB("CopyJobTicket::isColorRestricted: color access is DISABLED");
                colorRestricted=true; // Restricted, color access is disabled.
                break;
            default:
                CHECKPOINTA("CopyJobTicket::isColorRestricted: color access is UNKNOWN");
                break;
        }

    }
    return colorRestricted;
}
std::shared_ptr<dune::scan::types::ScanTicketStruct> CopyJobTicket::createScanPageIntent()
{
    std::shared_ptr<dune::scan::types::ScanTicketStruct> scanPageIntent = std::make_shared<dune::scan::types::ScanTicketStruct>();

    //Set copy as scan image profile
    scanPageIntent->setScanType(convertScanTypeEnumFromImagingProfileType(dune::scan::types::ScanImagingProfileType::COPY));
    Product prePrintConfiguration = getPrePrintConfiguration();
    //Auto crop
    if(isAutoCropSupportedOnScanDevice())
    {
        scanPageIntent->setAutoCrop(true);
    }

    auto defaultMediaSize = getDefaultMediaSize();
    //Check if prescan job
    if(isPreScanJob())
    {
            //In this section a prescan was done and we are attempting to use the edge detection values.
        auto preScanWidth = getPrescannedWidth();
        auto preScanHeight = getPrescannedHeight();
        CHECKPOINTC("CopyJobTicket: createScanPageIntent - prescanHeight: %d, prescanWidth: %d", (int)preScanHeight, (int)preScanWidth);

        if (preScanWidth == 0 || preScanHeight == 0)
        {
            CHECKPOINTC("CopyJobTicket: createScanPageIntent - ERROR prescan results returned with zero values");
            copyJobIntent_->setInputMediaSizeId(defaultMediaSize);
        }
        else
        {
            //Create bucketlist for prescan original size
            std::vector<dune::imaging::types::MediaSizeId> AutoSizeBucketListConfig;
            AutoSizeBucketListConfig.push_back(defaultMediaSize);
            AutoSizeBucketListConfig.push_back(dune::imaging::types::MediaSizeId::LEGAL);
            AutoSizeBucketListConfig.push_back(dune::imaging::types::MediaSizeId::A3);
            AutoSizeBucketListConfig.push_back(dune::imaging::types::MediaSizeId::LEDGER);

            copyJobIntent_->setInputMediaSizeId(ConvertToScanTypeHelper::getClosestMediaSizeInBucketList(AutoSizeBucketListConfig, preScanWidth,
                                                                                                         preScanHeight, dune::imaging::types::Resolution::E300DPI));
        }

        CHECKPOINTC("CopyJobTicket: createScanPageIntent - mediaSize bucketized from prescan as: %d", (int)copyJobIntent_->getInputMediaSizeId());
        scanPageIntent->setAutoCrop(false);
    }

    //original content orientation
    auto contentOrientation = copyJobIntent_->getContentOrientation();
    if (dune::imaging::types::ContentOrientation::LANDSCAPE == contentOrientation)
    {
        scanPageIntent->setContentOrientation(dune::scan::types::ContentOrientationEnum::Landscape);
    }
    else
    {
        scanPageIntent->setContentOrientation(dune::scan::types::ContentOrientationEnum::Portrait);
    }

    //Original content type
    auto originalContentType = copyJobIntent_->getOriginalContentType();
    scanPageIntent->setOriginalType(convertOriginalTypeEnumFromOriginalContentType(originalContentType));

    //Scan source
    auto scanSource = ConvertToScanTypeHelper::resolveScanSource(copyJobIntent_->getInputPlexMode(), copyJobIntent_->getScanSource());
    if (prePrintConfiguration != Product::HOME_PRO) //HOME_PRO simulator should ignore these changes to interleaved
    {
        if (dune::scan::types::ScanSource::MDF != scanSource)
        {
            CHECKPOINTA("CopyJobTicket:: setInterleaved to false");
            scanPageIntent->setInterleaved(false);
        }
        else
        {
            CHECKPOINTA("CopyJobTicket:: setInterleaved to true");
            scanPageIntent->setInterleaved(true);
        }
    }

    // Set flatbed when no adf on use or mdf installed
    if(dune::scan::types::ScanSource::ADF_SIMPLEX == scanSource || dune::scan::types::ScanSource::ADF_DUPLEX == scanSource)
    {
        scanPageIntent->setScanSource(dune::scan::types::ScanSourceEnum::ADF);
        CHECKPOINTA("CopyJobTicket:: ScanSourceEnum  is set to ADF");
    }
    else if(dune::scan::types::ScanSource::MDF == scanSource)
    {
        scanPageIntent->setScanSource(dune::scan::types::ScanSourceEnum::MDF);
        CHECKPOINTA("CopyJobTicket:: ScanSourceEnum is set to MDF");
    }
    else
    {
        scanPageIntent->setScanSource(dune::scan::types::ScanSourceEnum::Flatbed);
        CHECKPOINTA("CopyJobTicket:: ScanSourceEnum is set to Flatbed");
    }

    //Color mode
    scanPageIntent->setColorSpace(convertColorSpaceFromColorMode(copyJobIntent_->getColorMode()));

    //Input Media Type
    scanPageIntent->setInputMediaType(copyJobIntent_->getOriginalMediaType());

    //Check Valid OutputMediaSize
    if (copyJobIntent_->getOutputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY &&  prePrintConfiguration == Product::HOME_PRO
        && copyJobIntent_->getScanSource() != dune::scan::types::ScanSource::MDF)
    {
        CHECKPOINTA("CopyJobTicket: ERROR: ANY cannot be used as an output media size");
        copyJobIntent_->setOutputMediaSizeId(defaultMediaSize);
        assert(false); // ?????????
    }

    //Margins
    MarginsParameters marginParams;
    marginParams.setMediaSource(copyJobIntent_->getOutputMediaSource());
    Margins mediaMargins = std::get<1>(mediaInterface_->getMargins(marginParams));

    auto orientation = dune::imaging::types::MediaOrientation::PORTRAIT;
    if (copyJobIntent_->getScanFeedOrientation() == dune::scan::types::ScanFeedOrientation::LONGEDGE)
    {
        orientation = dune::imaging::types::MediaOrientation::LANDSCAPE;
    }

    uint32_t topMargin = 0;
    uint32_t bottomMargin = 0;
    uint32_t leftMargin = 0;
    uint32_t rightMargin = 0;

    //OuyXExtent and OutYExtent
    if ((copyJobIntent_->getInputMediaSizeId() != copyJobIntent_->getOutputMediaSizeId()) && copyJobIntent_->getScaleToFitEnabled())
    {
        if (copyJobIntent_->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY && scanSource != dune::scan::types::ScanSource::GLASS)
        {
            CHECKPOINTA("CopyJobTicket::createScanPageIntent - scaleToFitEnabled is set but inputMediaSize is 'ANY' and scan source is not the flatbed. Please fix this.");
        }
        else
        {
            int dpi = 0;
            if (prePrintConfiguration == Product::HOME_PRO)
            {
                dpi = ConvertToScanTypeHelper::getResolutionIntFromEnum(dune::imaging::types::Resolution::E300DPI);
            }
            else
            {
                dpi = ConvertToScanTypeHelper::getResolutionIntFromEnum(copyJobIntent_->getOutputXResolution());
            }

            //setup prescan if input media size is automatic
            if (copyJobIntent_->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY && scanSource == dune::scan::types::ScanSource::GLASS)
            {
                scanPageIntent->setAutoCrop(true);
            }

            //Give the output region to the scan device ticket for scaleToFit calculations
            topMargin = mediaMargins.getTop().get(dpi);
            bottomMargin = mediaMargins.getBottom().get(dpi);
            leftMargin = mediaMargins.getLeft().get(dpi);
            rightMargin = mediaMargins.getRight().get(dpi);

            auto outWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(copyJobIntent_->getOutputMediaSizeId(), orientation);
            scanPageIntent->setOutXExtent(outWidthAndHeight.width.get(dpi) - (leftMargin + rightMargin));
            scanPageIntent->setOutYExtent(outWidthAndHeight.height.get(dpi) - (topMargin + bottomMargin));
            CHECKPOINTC("CopyJobTicket: createScanPageIntent: scaleToFit: dpi = %d, margin = %d, outXExtent = %d, outYExtent = %d"
                        , dpi, (leftMargin + rightMargin), scanPageIntent->getOutXExtent(), scanPageIntent->getOutYExtent());
        }
    }

    // Setup output resolution differently for Home/Pro based on UI selected Quality Mode option.
    // DRAFT/NORMAL mode = 300 dpi requested and BEST = 600 dpi.  This is true for both ADF and Glass scans
    dune::imaging::types::Resolution scanXResolution, scanYResolution;
    if (prePrintConfiguration == Product::HOME_PRO)
    {
        dune::imaging::types::PrintQuality copyQuality = copyJobIntent_->getCopyQuality();
        if (copyQuality == dune::imaging::types::PrintQuality::DRAFT || copyQuality == dune::imaging::types::PrintQuality::NORMAL)
        {
            scanXResolution = dune::imaging::types::Resolution::E300DPI;
            scanYResolution = dune::imaging::types::Resolution::E300DPI;
        }
        else if (copyQuality == dune::imaging::types::PrintQuality::BEST)
        {
            scanXResolution = dune::imaging::types::Resolution::E600DPI;
            scanYResolution = dune::imaging::types::Resolution::E600DPI;
        }
        else
        {
            CHECKPOINTA("CopypipelineBuilder::setScanDevice - Quality mode %d not supported on HOME_PRO products, setting to 300DPI.  Please fix this.", (uint32_t)copyQuality);
            scanXResolution = dune::imaging::types::Resolution::E300DPI;
            scanYResolution = dune::imaging::types::Resolution::E300DPI;
        }

        if(getSegmentType() == dune::job::SegmentType::PrepareSegment)
        {
            scanXResolution = dune::imaging::types::Resolution::E100DPI;
            scanYResolution = dune::imaging::types::Resolution::E100DPI;
        }

        scanPageIntent->setOutputXImageQuality(convertOutputResolutionToImageQualityEnum(scanXResolution));
        scanPageIntent->setOutputYImageQuality(convertOutputResolutionToImageQualityEnum(scanYResolution));
    }
    // For all other products currently
    else
    {
        scanXResolution = copyJobIntent_->getOutputXResolution();
        scanYResolution = copyJobIntent_->getOutputYResolution();
        scanPageIntent->setOutputXImageQuality(convertOutputResolutionToImageQualityEnum(scanXResolution));
        scanPageIntent->setOutputYImageQuality(convertOutputResolutionToImageQualityEnum(scanYResolution));
    }

    //Set scan capute mode to scan page intent
    dune::scan::types::ScanCaptureModeType captureMode = copyJobIntent_->getScanCaptureMode();
    scanPageIntent->setScanCaptureMode(captureMode);

    //set the scan data output to interleaved if needed - ALWAYS SET TO FALSE
    //sdIntent->setScanOutputInterleaved(false);
    //CHECKPOINTA("CopyPipelineBuilder:: Scan data interleaved = %d", sdIntent->getScanOutputInterleaved());

    //Scan region
    MaxLengthConfig maxLengthConfig = getMaxLengthConfig();
    if(scanSource == dune::scan::types::ScanSource::GLASS && copyJobIntent_->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::LEGAL)
    {
        if (prePrintConfiguration == Product::HOME_PRO)
        {
            setupScanRegion(scanPageIntent, dune::imaging::types::MediaSizeId::LETTER, copyJobIntent_->getScanFeedOrientation(), dune::imaging::types::Resolution::E300DPI, captureMode,
                            maxLengthConfig.scanMaxCm, topMargin, bottomMargin, leftMargin, rightMargin);
        }
        else
        {
            setupScanRegion(scanPageIntent, dune::imaging::types::MediaSizeId::LETTER, copyJobIntent_->getScanFeedOrientation(), scanXResolution, captureMode,
                            maxLengthConfig.scanMaxCm, topMargin, bottomMargin, leftMargin, rightMargin);
        }
    }
    else
    {
        if (prePrintConfiguration == Product::HOME_PRO)
        {
            setupScanRegion(scanPageIntent, copyJobIntent_->getInputMediaSizeId(), copyJobIntent_->getScanFeedOrientation(), dune::imaging::types::Resolution::E300DPI, captureMode,
                            maxLengthConfig.scanMaxCm, topMargin, bottomMargin, leftMargin, rightMargin);
        }
        else
        {
            setupScanRegion(scanPageIntent, copyJobIntent_->getInputMediaSizeId(), copyJobIntent_->getScanFeedOrientation(), scanXResolution, captureMode,
                            maxLengthConfig.scanMaxCm, topMargin, bottomMargin, leftMargin, rightMargin);
        }
    }

    // Set Scan Feed Orientation
    auto scanOrientation = copyJobIntent_->getScanFeedOrientation();
    if (scanOrientation == dune::scan::types::ScanFeedOrientation::SHORTEDGE)
    {
        scanPageIntent->setScanOrientation(dune::scan::types::ScanOrientationEnum::ShortEdgeFeed);
    }
    else
    {
        scanPageIntent->setScanOrientation(dune::scan::types::ScanOrientationEnum::LongEdgeFeed);
    }

    //XScale and YScale percent
    if(isScaleSupportedOnScanDevice())
    {
        scanPageIntent->setScaleXFactor(copyJobIntent_->getXScalePercent() * 1000);
        scanPageIntent->setScaleYFactor(copyJobIntent_->getYScalePercent() * 1000);
        CHECKPOINTD("CopyJobTicket: copyIntent_ scale: %d, %d", copyJobIntent_->getXScalePercent(), copyJobIntent_->getYScalePercent());

        if (copyJobIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp)
        {
            int dpi = 0;
            dpi = (prePrintConfiguration == Product::HOME_PRO) ? ConvertToScanTypeHelper::getResolutionIntFromEnum(dune::imaging::types::Resolution::E300DPI) :
                                                     ConvertToScanTypeHelper::getResolutionIntFromEnum(copyJobIntent_->getOutputXResolution());

            topMargin = mediaMargins.getTop().get(dpi);
            bottomMargin = mediaMargins.getBottom().get(dpi);
            leftMargin = mediaMargins.getLeft().get(dpi);
            rightMargin = mediaMargins.getRight().get(dpi);

            if(prePrintConfiguration == Product::ENTERPRISE)
            {
                CHECKPOINTD("CopyJobTicket: use the scalefactor in copjobintent");
            }
            else
            {
                //Give the output region to the scan device ticket for scaleToFit calculations
                auto outWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(copyJobIntent_->getOutputMediaSizeId(), orientation);
                uint32_t rotatedX = (outWidthAndHeight.height.get(dpi) - (bottomMargin + topMargin)) / 2;  //The desired width output of the scaled image is equal to the output media size height divided by 2 because of the rotation.
                uint32_t rotatedY = outWidthAndHeight.width.get(dpi) - (leftMargin + rightMargin);         //The desired height output of the scaled image is equal to the width of the output media size.
                uint64_t scaleFactor = ConvertToScanTypeHelper::getScalingForScaleToFit(scanPageIntent->getXMediaSize(), scanPageIntent->getYMediaSize(), rotatedX, rotatedY);

                scanPageIntent->setScaleXFactor(scaleFactor / 1000);
                scanPageIntent->setScaleYFactor(scaleFactor / 1000);
            }
            CHECKPOINTD("CopyJobTicket:: scale %d, %d", scanPageIntent->getScaleXFactor(), scanPageIntent->getScaleYFactor());
        }
    }
    else
    {
        scanPageIntent->setScaleXFactor(100 * 1000);
        scanPageIntent->setScaleYFactor(100 * 1000);
    }

    // These attributes are being hard coded for now.  Eventually we'll want to query
    // these values from the page assembler.
    scanPageIntent->setCompressionMode(dune::scan::types::CompressionModeEnum::Uncompressed); //Always set to NONE
    //sdIntent->setInterleavedObjectMap(true); NOT USED
    scanPageIntent->setMultipleNumberOfLinesRequired(256);
    //sdIntent->setRequiredWidthAlignment(32); NOT USED
    scanPageIntent->setBrightness(copyJobIntent_->getBrightness());
    scanPageIntent->setAutoRelease(copyJobIntent_->getAutoRelease());
    scanPageIntent->setScanAcquisitionsSpeed(copyJobIntent_->getScanAcquisitionsSpeed());

    //Input duplex mode for ADF or duplex side for Flatbed
    if (scanSource == dune::scan::types::ScanSource::ADF_DUPLEX)
    {
        scanPageIntent->setInputDuplexMode(dune::scan::types::DuplexSideEnum::BackSide);
    }
    else if (scanSource == dune::scan::types::ScanSource::ADF_SIMPLEX)
    {
        scanPageIntent->setInputDuplexMode(dune::scan::types::DuplexSideEnum::FrontSide);
    }
    else if (scanSource == dune::scan::types::ScanSource::GLASS)
    {
        scanPageIntent->setScanDuplexSide(getFlatbedDuplexScanSide());
    }
    else
    {
        scanPageIntent->setScanDuplexSide(dune::scan::types::DuplexSideEnum::FrontSide);
    }

    //Input FilpUp
    scanPageIntent->setScanPagesFlipUpEnabled(copyJobIntent_->getScanPagesFlipUpEnabled());

    //Others settings that have vlues by default
    scanPageIntent->setSharpness(0);
    scanPageIntent->setBackgroundRemoval(2);
    scanPageIntent->setBackgroundCleanup(2);
    scanPageIntent->setJobScanLimit(0);
    scanPageIntent->setContrast(0);
    scanPageIntent->setTransferObjectTypeMap(false);
    scanPageIntent->setCcdChannel(dune::scan::types::CcdChannelEnum::GrayCcdEmulated);
    scanPageIntent->setBinaryRendering(dune::scan::types::BinaryRenderingEnum::Halftone);
    scanPageIntent->setDescreen(false);
    scanPageIntent->setFeederPickStop(false);
    scanPageIntent->setShadow(0);
    scanPageIntent->setCompressionFactor(copyJobIntent_->getCompressionFactor());
    scanPageIntent->setThreshold(0);
    scanPageIntent->setScanAutoColorDetect(dune::scan::types::AutoColorDetectEnum::DetectOnly);
    scanPageIntent->setScanBlackBackground(false);
    scanPageIntent->setScanNumberPages(0);
    scanPageIntent->setScanAutoExposure(false);
    scanPageIntent->setScanGamma(100);
    scanPageIntent->setScanHighlight(0);
    scanPageIntent->setScanColorSensitivity(0);
    scanPageIntent->setScanColorRange(0);
    scanPageIntent->setImagePreview(dune::scan::types::ImagePreview::Disable);
    scanPageIntent->setAutoToneScale(false);
    scanPageIntent->setAutoToneScaleRange(2);
    scanPageIntent->setAutoWhiteColorRemoval(false);
    scanPageIntent->setAutoWhiteColorRemovalRange(1);
    scanPageIntent->setDetectBlankPage(dune::scan::types::BlankDetectEnum::Disable);
    scanPageIntent->setOverScan(dune::scan::types::OverScanType::TOPANDBOTTOM);
    scanPageIntent->setScanNoiseRemoval(0);
    scanPageIntent->setScanBlankPageSensitivity(0);
    scanPageIntent->setDeskew(true);
    scanPageIntent->setXImageQuality(convertScanResToInt(dune::imaging::types::Resolution::E600DPI));
    scanPageIntent->setYImageQuality(convertScanResToInt(dune::imaging::types::Resolution::E600DPI));
    scanPageIntent->setStripHeight(0);

    // In future we might need to check this feature on the basis of capability
    scanPageIntent->setDisableMultiPickSensing(true);

    // In future we might need to check this feature on the basis of capability
    scanPageIntent->setPageBindingMode(dune::scan::types::PageBindingModeEnum::HorizontalBinding);

    scanPageIntent->setTextGraphicsPriority(2);
    scanPageIntent->setPhotoModeType(dune::scan::types::PhotoModeEnum::Glossy);
    scanPageIntent->setMixedMediaInput(false);
    scanPageIntent->setScannerMedia(dune::scan::types::ScanMediaEnum::Normal);
    scanPageIntent->setDigitalSendFileSize(1);
    scanPageIntent->setCounterfeitDetection(0);
    scanPageIntent->setBitDepth(dune::scan::types::ScanBitDepthEnum::Depth8Bits);
    scanPageIntent->setNoImagePadding(0);
    if(prePrintConfiguration == Product::HOME_PRO && dune::scan::types::ScanSource::MDF == scanSource)
    {
        scanPageIntent->setFilePath(getStorePath());
    }
    //Log scan page intent
    scanPageIntentDumper(scanPageIntent);

    return scanPageIntent;
}

std::shared_ptr<dune::print::engine::PrintIntents> CopyJobTicket::createDefaultPrintIntent()
{
    //Create default print intent
    const std::map<dune::print::engine::PrintIntentFieldType, dune::print::engine::Variant> printIntentFields =
    {
        { dune::print::engine::PrintIntentFieldType::PAGE_WIDTH,    dune::print::engine::Variant(1)                                             },
        { dune::print::engine::PrintIntentFieldType::PAGE_HEIGHT,   dune::print::engine::Variant(1)                                             },
        { dune::print::engine::PrintIntentFieldType::PAGE_UNITS,    dune::print::engine::Variant(copyJobIntent_->getOutputXResolution())        },
        { dune::print::engine::PrintIntentFieldType::PRINT_AREA,    dune::print::engine::Variant(dune::imaging::types::PrintArea::FULLSIZE)     },
        { dune::print::engine::PrintIntentFieldType::TOP_MARGIN,    dune::print::engine::Variant(0)                                             },
        { dune::print::engine::PrintIntentFieldType::BOTTOM_MARGIN, dune::print::engine::Variant(0)                                             },
        { dune::print::engine::PrintIntentFieldType::LEFT_MARGIN,   dune::print::engine::Variant(0)                                             },
        { dune::print::engine::PrintIntentFieldType::RIGHT_MARGIN,  dune::print::engine::Variant(0)                                             },
        { dune::print::engine::PrintIntentFieldType::CUTTER,        dune::print::engine::Variant(true)                                          }
    };

    return std::make_shared<dune::print::engine::PrintIntents>(printIntentFields);
}

void CopyJobTicket::updatePrintIntent(std::shared_ptr<dune::print::engine::PrintIntents>& printIntent, dune::framework::core::Uuid pageId)
{
    bool alignmentChangeRequired{false};
    uint32_t resolution = ConvertToScanTypeHelper::getResolutionIntFromEnum(copyJobIntent_->getOutputXResolution());
    auto mediaSizeId = copyJobIntent_->getOutputMediaSizeId();
    uint32_t finalPrintPageCount;
    if (mediaSizeId == dune::imaging::types::MediaSizeId::ANY && getPrePrintConfiguration() == Product::ENTERPRISE 
        && copyJobIntent_->getMatchOriginalOutputMediaSizeId() != dune::imaging::types::MediaSizeId::ANY)
    {
        CHECKPOINTC("CopyJobTicket::updatePrintIntent set the MediaSize to ANY_OUTPUT_MEDIA_SIZE_ID"); 
        mediaSizeId = copyJobIntent_->getMatchOriginalOutputMediaSizeId();
    }
    else if (mediaSizeId == dune::imaging::types::MediaSizeId::ANY)
    {
        CHECKPOINTA("CopyJobTicket::updatePrintIntent set the MediaSize to Custom");
        mediaSizeId = dune::imaging::types::MediaSizeId::CUSTOM;
    }

    auto orientation = dune::imaging::types::MediaOrientation::PORTRAIT;
    if (copyJobIntent_->getScanFeedOrientation() == dune::scan::types::ScanFeedOrientation::LONGEDGE)
    {
        orientation = dune::imaging::types::MediaOrientation::LANDSCAPE;
        
    }
    
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::INTENDED_FEED_ORIENTATION, orientation);

    if(copyJobIntent_->getOutputMediaSizeId() != dune::imaging::types::MediaSizeId::ANY)
    {
        CHECKPOINTD("CopyJobTicket::updatePrintIntent get orientation from outputMediaOrientation");
        orientation = copyJobIntent_->getOutputMediaOrientation();
    }
    //TODO: set Early Copy job value to true if it's a early copy job to improve performance in Enteprise
    CHECKPOINTC("CopyJobTicket::updatePrintIntent mediaSizeId: %d, orientation: %d", (int)mediaSizeId, (int)orientation);
    bool rotate180 = false;

    // For Early Copy job, Rotate 180 is calculated based on the scan intent values
    if(isEarlyCopyJob())
    {
        rotate180 = calculateRotationAngle();
    }
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::ROTATE_180, rotate180);
    CHECKPOINTC("CopyJobTicket::updatePrintIntent set rotate180 to %d", rotate180);
    dune::imaging::types::WidthAndHeight widthAndHeight;
    if (mediaSizeId == dune::imaging::types::MediaSizeId::CUSTOM && getPrePrintConfiguration() == Product::ENTERPRISE)
    {
        widthAndHeight = dune::imaging::types::convertCustomMediaSizeIdToWidthAndHeight(copyJobIntent_->getCustomMediaXDimension(), copyJobIntent_->getCustomMediaYDimension());
    }
    else
    {
        if (copyJobIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::OneUp
            && copyJobIntent_->getScanCaptureMode() != dune::scan::types::ScanCaptureModeType::IDCARD)
        {
            widthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(mediaSizeId, orientation);
        }
        else
        {
            // For N-up job including IDCard, output image will be generated always as portrait by LayoutFilter
            widthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(mediaSizeId);
        }
    }
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PAGE_WIDTH, widthAndHeight.width.get(resolution));
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PAGE_HEIGHT, widthAndHeight.height.get(resolution));
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PAGE_UNITS, resolution);
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, copyJobIntent_->getOutputMediaSource());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::MEDIA_TYPE, copyJobIntent_->getOutputMediaIdType());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::MEDIA_SIZE, mediaSizeId);
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PAGE_TICKET_ID, pageId);
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::CONTENT_ORIENTATION, copyJobIntent_->getContentOrientation());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PAGE_ID, pageId);
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PRINT_QUALITY, copyJobIntent_->getCopyQuality());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::BIN_TYPE, copyJobIntent_->getOutputDestination());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, copyJobIntent_->getColorMode());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PRINTING_ORDER, copyJobIntent_->getPrintingOrder());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PAGE_NUMBER , pageCount_);
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::ORIGINAL_CONTENT_TYPE, copyJobIntent_->getOriginalContentType());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, copyJobIntent_->getOutputPlexBinding());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, copyJobIntent_->getOutputPlexMode());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::STAPLE_OPTION, copyJobIntent_->getStapleOption());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::PUNCH_OPTION, copyJobIntent_->getPunchOption());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::FOLD_OPTION, copyJobIntent_->getFoldOption());
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::BOOKLET_MAKER_OPTION, copyJobIntent_->getBookletMakerOption());
    //SheetPerSet
    {
        if(copyJobIntent_->getFoldOption() == FoldingOptions::C_INWARD_TOP || copyJobIntent_->getFoldOption() ==FoldingOptions::C_INWARD_BOTTOM
            || copyJobIntent_->getFoldOption() == FoldingOptions::C_OUTWARD_TOP || copyJobIntent_->getFoldOption() == FoldingOptions::C_OUTWARD_BOTTOM)
        {
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::SHEETS_PER_SET, copyJobIntent_->getSheetsPerSetForCFold());
        }
        else if(copyJobIntent_->getFoldOption() == FoldingOptions::V_INWARD_TOP || copyJobIntent_->getFoldOption() == FoldingOptions::V_INWARD_BOTTOM
            || copyJobIntent_->getFoldOption() == FoldingOptions::V_OUTWARD_TOP || copyJobIntent_->getFoldOption() == FoldingOptions::V_OUTWARD_BOTTOM)
        {
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::SHEETS_PER_SET, copyJobIntent_->getSheetsPerSetForVFold());
        }
        else if(copyJobIntent_->getBookletMakerOption() == BookletMakingOptions::SADDLE_STITCH)
        {
            if(copyJobIntent_->getDeviceSetsFoldAndStitchSheetsEnabled())
            {
                auto resSheets = getPagesPerSetLimitForFinishingOption(FoldingOptions::NONE, BookletMakingOptions::SADDLE_STITCH);
                printIntent->setValue(dune::print::engine::PrintIntentFieldType::SHEETS_PER_SET, std::get<1>(resSheets));
            }
            else
            {
                printIntent->setValue(dune::print::engine::PrintIntentFieldType::SHEETS_PER_SET, copyJobIntent_->getSheetsPerSetForFoldAndStitch());
            }
        }
        else
        {
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::SHEETS_PER_SET, 1);
        }
    }

    // Folding style and folding style id checks.
    {
        dune::imaging::types::FoldingStyle foldingStyle{dune::imaging::types::FoldingStyle::UNDEFINED};
        int32_t foldingStyleId = copyJobIntent_->getFoldingStyleId();

        // Check PrintIntents fbs. These are the cases of folder-defined styles.
        if( foldingStyleId == FOLDING_STYLE_FOLDER_DEFAULT || (foldingStyleId >= FOLDING_STYLE_MIN_ALLOWED_ID && foldingStyleId <= FOLDING_STYLE_MAX_ALLOWED_ID) )
        {
            foldingStyle = dune::imaging::types::FoldingStyle::STANDARD;
        }

        printIntent->setValue(dune::print::engine::PrintIntentFieldType::FOLDING_STYLE, foldingStyle);
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::STANDARD_FOLDING_STYLE, copyJobIntent_->getFoldingStyleId());
    }

    if (getPrePrintConfiguration() == Product::ENTERPRISE)
    {
        if (copyJobIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp)
        {
            // change content orientation for 2 up case, 
            // if original scan image has portrait content orientation, 2up output will have landscape content orientation.
            if (copyJobIntent_->getContentOrientation() == ContentOrientation::PORTRAIT)
            {
                printIntent->setValue(dune::print::engine::PrintIntentFieldType::CONTENT_ORIENTATION, ContentOrientation::LANDSCAPE);
            }
            else
            {
                printIntent->setValue(dune::print::engine::PrintIntentFieldType::CONTENT_ORIENTATION, ContentOrientation::PORTRAIT);
            }
        }

        // Set duplex bindng
        if (copyJobIntent_->getOutputPlexMode() == dune::imaging::types::Plex::DUPLEX)
        {
            ContentOrientation outContentOrientation = ContentOrientation::PORTRAIT;
            printIntent->getValue(dune::print::engine::PrintIntentFieldType::CONTENT_ORIENTATION, outContentOrientation);
            if (outContentOrientation == ContentOrientation::PORTRAIT)
            {
                printIntent->setValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, PlexBinding::LONG_EDGE);
            }
            else
            {
                printIntent->setValue(dune::print::engine::PrintIntentFieldType::PLEX_BINDING, PlexBinding::SHORT_EDGE);
            }
        }
    }

    // Set the Copy Margins for Page Sensor device
    if(copyJobIntent_->getScanSource() != dune::scan::types::ScanSource::MDF)
    {
        MarginLayout effectiveMarginLayout = copyJobIntent_->determineMarginLayoutOrDefault(MarginLayout::STANDARD);
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, effectiveMarginLayout);
        switch (effectiveMarginLayout)
        {
            case MarginLayout::STANDARD :
                CHECKPOINTC("CopyJobTicket::updatePrintIntent set margin layout Standard");
                break;

            case MarginLayout::OVERSIZE :
                CHECKPOINTC("CopyJobTicket::updatePrintIntent set margin layout Oversize");
                break;

            case MarginLayout::CLIPINSIDE :
                CHECKPOINTC("CopyJobTicket::updatePrintIntent set margin layout ClipInside");
                break;

            case MarginLayout::ADDTOCONTENTS :
                CHECKPOINTC("CopyJobTicket::updatePrintIntent set margin layout AddToContents");
                break;
        }

        if (copyJobIntent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp)
        {
            CHECKPOINTC("CopyJobTicket::updatePrintIntent set the Content Alignment value Center and top (nup case)");
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, dune::imaging::types::HorizontalContentAlignment::CENTER);
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, dune::imaging::types::VerticalContentAlignment::CENTER);
            alignmentChangeRequired = true;
        }
        else if ( copyJobIntent_->getScaleToFitEnabled()  || (
						copyJobIntent_->getInputMediaSizeId() == mediaSizeId &&
						copyJobIntent_->getScaleSelection() != dune::scan::types::ScanScaleSelectionEnum::CUSTOM &&
                        copyJobIntent_->getScaleSelection() != dune::scan::types::ScanScaleSelectionEnum::FULLPAGE
					)
			   )
        {
            CHECKPOINTC("CopyJobTicket::updatePrintIntent set the Content Alignment value Center ");
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, dune::imaging::types::HorizontalContentAlignment::CENTER);
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, dune::imaging::types::VerticalContentAlignment::CENTER);
        }
        else
        {
            CHECKPOINTC("CopyJobTicket::updatePrintIntent set the Content Alignment value top left ");
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT);
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, dune::imaging::types::VerticalContentAlignment::TOP);
            alignmentChangeRequired = true;
        }
    }
    else
    {
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE, dune::job::JobType::COPY);
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, convertToMarginLayout(copyJobIntent_->getCopyMargins()));
        CHECKPOINTC("CopyJobTicket::updatePrintIntent set the MDF Content Alignment value top left ");
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, dune::imaging::types::HorizontalContentAlignment::KEEP_LEFT);
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, dune::imaging::types::VerticalContentAlignment::TOP);
    }



    //If duplex printing is selected, then PlexSide must be appropriately for 2 consective pages
    if(copyJobIntent_->getOutputPlexMode()== dune::imaging::types::Plex::DUPLEX)
    {
        if(copyJobIntent_->getPlexSide() == dune::imaging::types::PlexSide::FIRST)
        {
            bool isCollateLongEdge = (copyJobIntent_->getCollate() == SheetCollate::Collate &&
                 copyJobIntent_->getOutputPlexBinding() == dune::imaging::types::PlexBinding::LONG_EDGE);
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::PLEX_SIDE,dune::imaging::types::PlexSide::FIRST);
            copyJobIntent_->setPlexSide(dune::imaging::types::PlexSide::SECOND);
            CHECKPOINTA("CopyJobTicket updatePrintIntent - Print Front Side");

            // for printer like MMK alignment needs to be defined for each side
            if(alignmentChangeRequired && isPrintAlignmentChangeRequired() && isCollateLongEdge)
            {
                CHECKPOINTC("CopyJobTicket::updatePrintIntent set the Content Alignment value top left ");
                printIntent->setValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, dune::imaging::types::VerticalContentAlignment::BOTTOM);
                if (copyJobIntent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp)
                {
                     printIntent->setValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, dune::imaging::types::HorizontalContentAlignment::CENTER);
                     printIntent->setValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT,   dune::imaging::types::HorizontalContentAlignment::CENTER);

                }
                else
                {
                     printIntent->setValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, dune::imaging::types::HorizontalContentAlignment::KEEP_RIGHT);
                }
            }
        }
        else
        {
            bool isUncollateLongEdge = (copyJobIntent_->getCollate() == SheetCollate::Uncollate && copyJobIntent_->getOutputPlexBinding() == dune::imaging::types::PlexBinding::LONG_EDGE);
            printIntent->setValue(dune::print::engine::PrintIntentFieldType::PLEX_SIDE,dune::imaging::types::PlexSide::SECOND);
            copyJobIntent_->setPlexSide(dune::imaging::types::PlexSide::FIRST);
            CHECKPOINTA("CopyJobTicket updatePrintIntent - Print Back Side");

            // for printer like MMK alignment needs to be defined for each side
            if(alignmentChangeRequired && isPrintAlignmentChangeRequired() && isUncollateLongEdge)
            {
                CHECKPOINTC("CopyJobTicket::updatePrintIntent set the Content Alignment value bottom right ");
                printIntent->setValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, dune::imaging::types::VerticalContentAlignment::BOTTOM);
                if (copyJobIntent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp)
                {
                     printIntent->setValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, dune::imaging::types::HorizontalContentAlignment::CENTER);
                     printIntent->setValue(dune::print::engine::PrintIntentFieldType::VERTICAL_CONTENT_ALIGNMENT, dune::imaging::types::VerticalContentAlignment::CENTER);

                }
                else
                {
                     printIntent->setValue(dune::print::engine::PrintIntentFieldType::HORIZONTAL_CONTENT_ALIGNMENT, dune::imaging::types::HorizontalContentAlignment::KEEP_RIGHT);
                }
            }
        }
    }
    else
    {
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::PLEX_SIDE, dune::imaging::types::PlexSide::FIRST);
        copyJobIntent_->setPlexSide(dune::imaging::types::PlexSide::FIRST);
    }

    MarginsParameters marginParams;
    marginParams.setMediaSource(copyJobIntent_->getOutputMediaSource());
    Margins mediaMargins = std::get<1>(mediaInterface_->getMargins(marginParams));

    uint32_t topMargin_ = mediaMargins.getTop().get(resolution);
    uint32_t bottomMargin_ = mediaMargins.getBottom().get(resolution);
    uint32_t leftMargin_ = mediaMargins.getLeft().get(resolution);
    uint32_t rightMargin_ = mediaMargins.getRight().get(resolution);

    printIntent->setValue(dune::print::engine::PrintIntentFieldType::TOP_MARGIN, topMargin_);
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::BOTTOM_MARGIN, bottomMargin_);
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::LEFT_MARGIN, leftMargin_);
    printIntent->setValue(dune::print::engine::PrintIntentFieldType::RIGHT_MARGIN, rightMargin_);

    if (copyJobIntent_->getScanSource() == dune::scan::types::ScanSource::GLASS)
    {
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::COPY_FROM_GLASS, true);
    }
    else
    {
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::COPY_FROM_GLASS, false);
    }

    if (copyJobIntent_->getCollate() == SheetCollate::Uncollate && copyJobIntent_->getScanSource() != dune::scan::types::ScanSource::GLASS)
    {
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::UNCOLLATED_COPIES_COUNT, copyJobIntent_->getCopies());
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::COLLATED_COPIES_COUNT, 1);
    }
    else
    {
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::UNCOLLATED_COPIES_COUNT, 1);
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::COLLATED_COPIES_COUNT, copyJobIntent_->getCopies());
    }

    if (getSegmentType() != dune::job::SegmentType::PrepareSegment)
    {
        printPageCount_++;

        if(copyJobIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp)
            finalPrintPageCount = (printPageCount_ + 1) / 2;
        else
            finalPrintPageCount = printPageCount_;

        if (getMaxCollatePages() > 0 && finalPrintPageCount > getMaxCollatePages() && copyJobIntent_->getCollate() == SheetCollate::Collate)
        {
            finalPrintPageCount = finalPrintPageCount - getMaxCollatePages();
        }

        printIntent->setValue(dune::print::engine::PrintIntentFieldType::JOB_PAGE_COUNT, finalPrintPageCount * copyJobIntent_->getCopies());
    }

    bool borderless = shouldBeBorderless();
    if (borderless)
    {
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::MARGIN_SETTING, dune::imaging::types::MarginSettings::NOMARGINS);
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::BORDERLESS_METHOD, dune::imaging::types::Borderless::AUTOFIT);
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::MARGIN_LAYOUT, MarginLayout::STANDARD);
    }

    if (copyJobIntent_->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL || 
        copyJobIntent_->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER || 
        copyJobIntent_->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_A4_A3)
    {
        CHECKPOINTA("CopyJobTicket::updatePrintIntent set the MixedMediaInput value to true");
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::FORCE_FEED_ORIENTATION, dune::imaging::types::ForceFeedOrientationType::NOTOKTOOVERRIDE);
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::INTENDED_FEED_ORIENTATION, dune::imaging::types::MediaOrientation::PORTRAIT);
    }
    else
    {
        printIntent->setValue(dune::print::engine::PrintIntentFieldType::FORCE_FEED_ORIENTATION, dune::imaging::types::ForceFeedOrientationType::OKTOOVERRIDE);
    }


    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: Print Quality: %d", static_cast<uint32_t>(copyJobIntent_->getCopyQuality()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: Output Media Source: %d", static_cast<uint32_t>(copyJobIntent_->getOutputMediaSource()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: Copy Margins: %d", static_cast<uint32_t>(copyJobIntent_->getCopyMargins()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: Output Media destination: %d", static_cast<uint32_t>(copyJobIntent_->getOutputDestination()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: Margins Top - %d , Bottom - %d, Left - %d, Right - %d",topMargin_, bottomMargin_, leftMargin_, rightMargin_);
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: Output Media Type : %d", static_cast<uint32_t>(copyJobIntent_->getOutputMediaIdType()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: resolution : %d", static_cast<uint32_t>(copyJobIntent_->getOutputXResolution()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: plexMode : %d", static_cast<uint32_t>(copyJobIntent_->getOutputPlexMode()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: plexBinding : %d", static_cast<uint32_t>(copyJobIntent_->getOutputPlexBinding()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: foldingStyle : %d", static_cast<uint32_t>(copyJobIntent_->getFoldingStyleId()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: printingOrder : %d", static_cast<uint32_t>(copyJobIntent_->getPrintingOrder()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: pageCount : %d", static_cast<uint32_t>(pageCount_));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: Borderless : %d", static_cast<uint32_t>(borderless));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: Width : %d", static_cast<uint32_t>(widthAndHeight.width.get(resolution)));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: Height : %d", static_cast<uint32_t>(widthAndHeight.height.get(resolution)));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: StapleOption : %d", static_cast<uint32_t>(copyJobIntent_->getStapleOption()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: PunchOption : %d", static_cast<uint32_t>(copyJobIntent_->getPunchOption()));
    CHECKPOINTC("CopyJobTicket::updatePrintIntent COPY job: BookletMakerOption : %d", static_cast<uint32_t>(copyJobIntent_->getBookletMakerOption()));
}

bool CopyJobTicket::calculateRotationAngle()
{
    bool rotate180 = false;

    auto scanSource = copyJobIntent_->getScanSource();
    auto contentOrientation= copyJobIntent_->getContentOrientation();
    auto scanFeedOrientation = copyJobIntent_->getScanFeedOrientation();
    auto nupSetting = copyJobIntent_->getPagesPerSheet();

    bool isScanSourceAdf = (scanSource == ScanSource::ADF_DUPLEX || scanSource == ScanSource::ADF_SIMPLEX);

    if((scanSource == ScanSource::GLASS && scanFeedOrientation == ScanFeedOrientation::LONGEDGE && contentOrientation == ContentOrientation::PORTRAIT)
        || ( isScanSourceAdf && (scanFeedOrientation == ScanFeedOrientation::SHORTEDGE) && (contentOrientation == ContentOrientation::LANDSCAPE)))
    {
        rotate180 = true;
    }

    if(nupSetting == dune::imaging::types::CopyOutputNumberUpCount::TwoUp)
    {
        rotate180 = !rotate180;
    }

    return rotate180;

}

dune::imaging::types::MarginLayout CopyJobTicket::convertToMarginLayout(dune::imaging::types::CopyMargins copyMargins)
{
    switch(copyMargins)
    {
        case dune::imaging::types::CopyMargins::OVERSIZE:
            return dune::imaging::types::MarginLayout::OVERSIZE;

        case dune::imaging::types::CopyMargins::CLIPCONTENT:
            return dune::imaging::types::MarginLayout::CLIPINSIDE;

        case dune::imaging::types::CopyMargins::ADDTOCONTENT:
            return dune::imaging::types::MarginLayout::ADDTOCONTENTS;

        default:
            return dune::imaging::types::MarginLayout::STANDARD;
    }
}

dune::imaging::types::MediaSizeId CopyJobTicket::getMediaSizeFromMediaSource(dune::imaging::types::MediaSource source) const
{

    dune::imaging::types::MediaSizeId result = dune::imaging::types::MediaSizeId::ANY;

    if (mediaInterface_ == nullptr)
    {
        CHECKPOINTA("CopyJobTicket::getMediaSizeFromMediaSource(): ERROR mediaInterface_ is null");
        return result;
    }

    const auto inputDevicesListTuple = mediaInterface_->getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE);
    const auto inputDevicesList = std::get<1>(inputDevicesListTuple);
    const APIResult retInputDeviceList = std::get<0>(inputDevicesListTuple);
    if(retInputDeviceList == APIResult::ERROR){
        return result;
    }
    else if((inputDevicesList.size() > 0) && (retInputDeviceList == APIResult::OK)){
        for(auto it : inputDevicesList){
            auto inputType = it->getType();
            if(inputType == dune::print::engine::InputType::TRAY)
            {
                auto inputTray = it->getTray();
                if(inputTray){
                    auto snapTuple = inputTray->getSnapShot();
                    if(std::get<0>(snapTuple) == APIResult::OK){
                        auto snap = std::get<1>(snapTuple);

                        dune::imaging::types::MediaSource mediaSourceId = inputTray->getMediaSource();

                        if(mediaSourceId == source)
                        {
                            result = std::get<1>(snap->getMediaSize()).getType();
                        }

                    }
                }
            }
            else if(inputType == dune::print::engine::InputType::ROLL)
            {
                auto inputRoll = it->getRoll();
                if(inputRoll){
                    auto snapTuple = inputRoll->getSnapShot();
                    if(std::get<0>(snapTuple) == APIResult::OK){
                        auto snap = std::get<1>(snapTuple);

                        dune::imaging::types::MediaSource mediaSourceId = inputRoll->getMediaSource();

                        if(mediaSourceId == source)
                        {
                            auto mediaSize = snap->getMediaSize();
                            if (std::get<0>(mediaSize))
                            {
                                result = std::get<1>(mediaSize).getType();
                                CHECKPOINTD("CopyJobTicket::getMediaSizeFromMediaSource(): Returning %d media size for roll", result);
                            }
                            else
                            {
                                auto customSizeSupported = inputRoll->isCustomSizeSupported();
                                if (std::get<0>(customSizeSupported) == APIResult::OK)
                                {
                                    if (std::get<1>(customSizeSupported))
                                    {
                                        CHECKPOINTD("CopyJobTicket::getMediaSizeFromMediaSource(): Returning CUSTOM media size for roll");
                                        result = dune::imaging::types::MediaSizeId::CUSTOM;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return result;
}

bool CopyJobTicket::isAutoCropSupportedOnScanDevice()
{
   bool isSupported = false;
    auto scanCapabilities = getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop, isSupported);
        CHECKPOINTC("CopyPipelineBuilder::isAutoCropSupportedOnScanDevice - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTC("CopyPipelineBuilder::isAutoCropSupportedOnScanDevice - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

// Check if scale is supported
bool CopyJobTicket::isScaleSupportedOnScanDevice()
{
    bool isSupported = false;
    auto scanCapabilities = getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale, isSupported);
        CHECKPOINTC("CopyJobTicket::isScaleSupportedOnScanDevice - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTB("CopyJobTicket::isScaleSupportedOnScanDevice - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

dune::scan::types::OriginalTypeEnum CopyJobTicket::convertOriginalTypeEnumFromOriginalContentType(dune::imaging::types::OriginalContentType contentType)
{
    // TODO - Maybe we should be using dune::imaging::types::OriginalContentType instead of OriginalTypeEnum
    using OriginalContentType = dune::imaging::types::OriginalContentType;

    dune::scan::types::OriginalTypeEnum originalTypeEnum = dune::scan::types::OriginalTypeEnum::AutoDetect;

    switch(contentType)
    {
        case OriginalContentType::AUTO:
            originalTypeEnum = dune::scan::types::OriginalTypeEnum::AutoDetect;
            break;
        case OriginalContentType::TEXT:
            originalTypeEnum = dune::scan::types::OriginalTypeEnum::Text;
            break;
        case OriginalContentType::LINE_DRAWING:
            // TODO Need the enum type at OriginalTypeEnum.
            break;
        case OriginalContentType::PHOTO:
            originalTypeEnum = dune::scan::types::OriginalTypeEnum::Photo;
            break;
        case OriginalContentType::IMAGE:
            // TODO Need the enum type at OriginalTypeEnum.
            break;
        case OriginalContentType::MIXED:
            originalTypeEnum = dune::scan::types::OriginalTypeEnum::Mixed;
            break;
        default:
            originalTypeEnum = dune::scan::types::OriginalTypeEnum::AutoDetect;
            break;
    }
    return originalTypeEnum;
}

dune::scan::types::ScanTypeEnum CopyJobTicket::convertScanTypeEnumFromImagingProfileType(dune::scan::types::ScanImagingProfileType profileType)
{
    // TODO - maybe we should use  dune::scan::types::ScanImagingProfileType instead of ScanTypeEnum
    using ScanImagingProfileType = dune::scan::types::ScanImagingProfileType;

    dune::scan::types::ScanTypeEnum scanTypeEnum = dune::scan::types::ScanTypeEnum::Copy;

    switch(profileType)
    {
        case ScanImagingProfileType::COPY:
            scanTypeEnum = dune::scan::types::ScanTypeEnum::Copy;
            break;
        case ScanImagingProfileType::SEND:
            scanTypeEnum = dune::scan::types::ScanTypeEnum::DigitalSend;
            break;
        case ScanImagingProfileType::RAW_SCAN_CAPTURE:
            scanTypeEnum = dune::scan::types::ScanTypeEnum::ScanCapture;
            break;
        case ScanImagingProfileType::FAX:
            scanTypeEnum = dune::scan::types::ScanTypeEnum::Fax;
            break;
        default:
            scanTypeEnum = dune::scan::types::ScanTypeEnum::Copy;
    }

    return scanTypeEnum;
}

dune::scan::types::ColorSpaceEnum CopyJobTicket::convertColorSpaceFromColorMode(dune::imaging::types::ColorMode colorMode)
{
    // TODO - Maybe we should use dune::imaging::types::ColorMode instead of ColorSpaceEnum
    using ColorMode = dune::imaging::types::ColorMode;

    dune::scan::types::ColorSpaceEnum colorSpace = dune::scan::types::ColorSpaceEnum::AutoDetectColorSpace;

    switch(colorMode)
    {
        case ColorMode::AUTODETECT:
            colorSpace = dune::scan::types::ColorSpaceEnum::AutoDetectColorSpace;
            break;
        case ColorMode::MONOCHROME:
            colorSpace = dune::scan::types::ColorSpaceEnum::BiLevel;
            break;
        case ColorMode::COLOR:
            colorSpace = dune::scan::types::ColorSpaceEnum::RGB;
            break;
        case ColorMode::GRAYSCALE:
            colorSpace = dune::scan::types::ColorSpaceEnum::Gray;
            break;
        case ColorMode::BLACKANDWHITE:
            colorSpace = dune::scan::types::ColorSpaceEnum::BiLevel;
            break;
        case ColorMode::AUTO_COLORANDBLACK:
        case ColorMode::AUTO_COLORANDGRAY:
            // TODO : It need to check the spec.
            break;
        default:
            colorSpace = dune::scan::types::ColorSpaceEnum::AutoDetectColorSpace;
            break;
    }

    return colorSpace;
}

dune::scan::types::ImageQualityEnum CopyJobTicket::convertOutputResolutionToImageQualityEnum(dune::imaging::types::Resolution resolution)
{
    // TODO - Maybe we should use dune::imaging::types::Resolution instead of ImageQualityEnum
    using Resolution = dune::imaging::types::Resolution;
    dune::scan::types::ImageQualityEnum imageQuality = dune::scan::types::ImageQualityEnum::DPI300;

    switch(resolution)
    {
        case Resolution::E75DPI:
            imageQuality = dune::scan::types::ImageQualityEnum::DPI75;
            break;
        case Resolution::E100DPI:
            imageQuality = dune::scan::types::ImageQualityEnum::DPI100;
            break;
        case Resolution::E150DPI:
            imageQuality = dune::scan::types::ImageQualityEnum::DPI150;
            break;
        case Resolution::E200DPI:
            imageQuality = dune::scan::types::ImageQualityEnum::DPI200;
            break;
        case Resolution::E240DPI:
            // need to imageQuality enum
            break;
        case Resolution::E300DPI:
            imageQuality = dune::scan::types::ImageQualityEnum::DPI300;
            break;
        case Resolution::E400DPI:
            imageQuality = dune::scan::types::ImageQualityEnum::DPI400;
            break;
        case Resolution::E500DPI:
            // need to imageQuality enum
            break;
        case Resolution::E600DPI:
            imageQuality = dune::scan::types::ImageQualityEnum::DPI600;
            break;
        case Resolution::E1200DPI:
            imageQuality = dune::scan::types::ImageQualityEnum::DPI1200;
            break;
        default:
            imageQuality = dune::scan::types::ImageQualityEnum::DPI300;
            break;
    }

    return imageQuality;
}

uint32_t CopyJobTicket::convertScanResToInt(dune::imaging::types::Resolution resolution)
{
    uint32_t res;

    using Resolution = dune::imaging::types::Resolution;

    switch(resolution)
    {
        case Resolution::E75DPI:
            res = 75;
            break;
        case Resolution::E100DPI:
            res = 100;
            break;
        case Resolution::E150DPI:
            res = 150;
            break;
        case Resolution::E200DPI:
            res = 200;
            break;
        case Resolution::E240DPI:
            res = 240;
            break;
        case Resolution::E300DPI:
            res = 300;
            break;
        case Resolution::E400DPI:
            res = 400;
            break;
        case Resolution::E500DPI:
            res = 500;
            break;
        case Resolution::E600DPI:
            res = 600;
            break;
        case Resolution::E1200DPI:
            res = 1200;
            break;
        default:
            res = 300;
            break;
    }
    return res;
}

void CopyJobTicket::setupScanRegion(std::shared_ptr<dune::scan::types::ScanTicketStruct>    scanPageIntent,
                                    dune::imaging::types::MediaSizeId                       mediaSize,
                                    dune::scan::types::ScanFeedOrientation                  orientation,
                                    dune::imaging::types::Resolution                        resolution,
                                    dune::scan::types::ScanCaptureModeType                  mode,
                                    u_int32_t                                               scanMaxCm,
                                    u_int32_t                                               topMargin,
                                    u_int32_t                                               bottomMargin,
                                    u_int32_t                                               leftMargin,
                                    u_int32_t                                               rightMargin)
{
    uint32_t resolutionInt = ConvertToScanTypeHelper::getResolutionIntFromEnum(resolution);
    // TODO - resolution split into X and Y, calculation below needs update
    // TODO - Scan Margins are not implemented yet, Hardcoding the margins
    uint32_t margin = ConvertToScanTypeHelper::getExtent(2, resolutionInt);
    if ((getPrePrintConfiguration() == Product::HOME_PRO) &&
        (scanPageIntent->getScanSource() == dune::scan::types::ScanSourceEnum::MDF))
    {
        // For Beam set margin to 0
        margin = ConvertToScanTypeHelper::getExtent(0, resolutionInt);
    }

    auto xyExtent = ConvertToScanTypeHelper::resolveXYExtent(mediaSize, orientation, resolution);
    uint32_t width = std::get<0>(xyExtent);
    uint32_t height = std::get<1>(xyExtent);
    height = ConvertToScanTypeHelper::resolveMaxExtentWithLength(height, scanMaxCm, resolutionInt); //copy only has a max length so no more parameters needed
    CHECKPOINTC("CopyJobTicket::setupScanRegion Height after maxExtent Validation: %d", height);

    // Set the origin points to the margin values
    if(margin > leftMargin)
    {
        scanPageIntent->setXScanOriginSide(margin);
    }
    else
    {
        scanPageIntent->setXScanOriginSide(leftMargin);
    }
    if(margin > topMargin)
    {
        scanPageIntent->setYScanOriginSide(margin);
    }
    else
    {
        scanPageIntent->setYScanOriginSide(topMargin);
    }

    // If edgeToEdgeScan is true, xExtend_ option changes to MAX
    bool edgeToEdgeScanOption = copyJobIntent_->getEdgeToEdgeScan();
    if(edgeToEdgeScanOption == true)
    {
        CHECKPOINTC("CopyJobTicket: setupScanRegion: edgeToEdge is true -> MAX XExtent");
        // Let the scan to set the MAX
        scanPageIntent->setXScanSizeSide(0);
        scanPageIntent->setXMediaSize(0);
    }
    else if(width > (leftMargin + rightMargin)) // Configure the extents in 600 units
    {
        uint32_t xExtent = width - (leftMargin + rightMargin);
        scanPageIntent->setXScanSizeSide(xExtent);
        scanPageIntent->setXMediaSize(xExtent);
    }
    else
    {
        //
        // Should throw exception if the resulting margin*2 is greater than the width
        // something has gone wrong.
    }

    if(height > (bottomMargin + topMargin))
    {
        uint32_t yExtent;
        if (mode == dune::scan::types::ScanCaptureModeType::IDCARD)
        {
            yExtent = (height / 2) - (bottomMargin + topMargin);
        }
        else
        {
            yExtent = (height - (bottomMargin + topMargin));
        }

        scanPageIntent->setYScanSizeSide(yExtent);
        scanPageIntent->setYMediaSize(yExtent);
    }
    else
    {
        //
        // Should throw exception if the resulting margin*2 is greater than the height
        // something has gone wrong.
    }
}

void CopyJobTicket::scanPageIntentDumper(const std::shared_ptr<dune::scan::types::ScanTicketStruct> &scanPageIntent)
{
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanType : %d", static_cast<int>(scanPageIntent->getScanType()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanSource : %d", static_cast<int>(scanPageIntent->getScanSource()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanOrientation : %d", static_cast<int>(scanPageIntent->getScanOrientation()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : InputDuplexMode : %d", static_cast<int>(scanPageIntent->getInputDuplexMode()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : InputMediaType: %d", static_cast<int>(scanPageIntent->getInputMediaType()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : XScanOriginSide : %d", static_cast<int>(scanPageIntent->getXScanOriginSide()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : YScanOriginSide : %d", static_cast<int>(scanPageIntent->getYScanOriginSide()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : XScanSizeSide : %d", static_cast<int>(scanPageIntent->getXScanSizeSide()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : YScanSizeSide : %d", static_cast<int>(scanPageIntent->getYScanSizeSide()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : XScanScaledSize: %d",    static_cast<int>(scanPageIntent->getXScanScaledSize()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : YScanScaledSize: %d",    static_cast<int>(scanPageIntent->getYScanScaledSize()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : OutXExtent : %d", static_cast<int>(scanPageIntent->getOutXExtent()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : OutYExtent : %d", static_cast<int>(scanPageIntent->getOutYExtent()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Brightness : %d", static_cast<int>(scanPageIntent->getBrightness()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : OriginalType : %d", static_cast<int>(scanPageIntent->getOriginalType()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : OriginalSubType : %d", static_cast<int>(scanPageIntent->getOriginalSubType()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ColorSpace : %d", static_cast<int>(scanPageIntent->getColorSpace()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : XImageQuality : %d", static_cast<int>(scanPageIntent->getXImageQuality()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : YImageQuality : %d", static_cast<int>(scanPageIntent->getYImageQuality()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : OutputXImageQuality : %d", static_cast<int>(scanPageIntent->getOutputXImageQuality()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : OutputYImageQuality : %d", static_cast<int>(scanPageIntent->getOutputYImageQuality()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Sharpness : %d", static_cast<int>(scanPageIntent->getSharpness()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : TextGraphicsPriority : %d", static_cast<int>(scanPageIntent->getTextGraphicsPriority()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : BackgroundRemoval : %d", static_cast<int>(scanPageIntent->getBackgroundRemoval()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : XMediaSize : %d", static_cast<int>(scanPageIntent->getXMediaSize()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : YMediaSize : %d", static_cast<int>(scanPageIntent->getYMediaSize()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : PhotoModeType : %d", static_cast<int>(scanPageIntent->getPhotoModeType()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : JobScanLimit : %d", static_cast<int>(scanPageIntent->getJobScanLimit()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScaleXFactor : %d", static_cast<int>(scanPageIntent->getScaleXFactor()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScaleYFactor : %d", static_cast<int>(scanPageIntent->getScaleYFactor()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Contrast : %d", static_cast<int>(scanPageIntent->getContrast()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : TransferObjectTypeMap : %d", static_cast<int>(scanPageIntent->getTransferObjectTypeMap()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : DigitalSendOutputBitDepth : %d", static_cast<int>(scanPageIntent->getDigitalSendOutputBitDepth()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : MixedMediaInput : %d", static_cast<int>(scanPageIntent->getMixedMediaInput()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScannerMedia : %d", static_cast<int>(scanPageIntent->getScannerMedia()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ContentOrientation : %d", static_cast<int>(scanPageIntent->getContentOrientation()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : BookMode : %d", static_cast<int>(scanPageIntent->getBookMode()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : PageBindingMode : %d", static_cast<int>(scanPageIntent->getPageBindingMode()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : StripHeight: %d", static_cast<int>(scanPageIntent->getStripHeight()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : StripWidth: %d", static_cast<int>(scanPageIntent->getStripWidth()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : DigitalSendFileSize : %d", static_cast<int>(scanPageIntent->getDigitalSendFileSize()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : CounterfeitDetection : %d", static_cast<int>(scanPageIntent->getCounterfeitDetection()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : BitDepth : %d", static_cast<int>(scanPageIntent->getBitDepth()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : CompressionMode : %d", static_cast<int>(scanPageIntent->getCompressionMode()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : MultipleNumberOfLinesRequired : %d", static_cast<int>(scanPageIntent->getMultipleNumberOfLinesRequired()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : AutoToneScale : %d", static_cast<int>(scanPageIntent->getAutoToneScale()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : AutoToneScaleRange : %d", static_cast<int>(scanPageIntent->getAutoToneScaleRange()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : AutoWhiteColorRemoval : %d", static_cast<int>(scanPageIntent->getAutoWhiteColorRemoval()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : AutoWhiteColorRemovalRange : %d", static_cast<int>(scanPageIntent->getAutoWhiteColorRemovalRange()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : NoImagePadding : %d", static_cast<int>(scanPageIntent->getNoImagePadding()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : DisableMultiPickSensing : %d", static_cast<int>(scanPageIntent->getDisableMultiPickSensing()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : MultiPickSensingAction : %d", static_cast<int>(scanPageIntent->getMultiPickSensingAction()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Deskew : %d", static_cast<int>(scanPageIntent->getDeskew()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : DustDetection : %d", static_cast<int>(scanPageIntent->getDustDetection()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : DetectBlankPage : %d", static_cast<int>(scanPageIntent->getDetectBlankPage()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Saturation : %d", static_cast<int>(scanPageIntent->getSaturation()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : PageCrop : %d", static_cast<int>(scanPageIntent->getPageCrop()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ContentCrop : %d", static_cast<int>(scanPageIntent->getContentCrop()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Negative : %d", static_cast<int>(scanPageIntent->getNegative()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanPagesFlipUpEnabled : %d", static_cast<int>(scanPageIntent->getScanPagesFlipUpEnabled()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ImagePreview : %d", static_cast<int>(scanPageIntent->getImagePreview()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Interleaved : %d", static_cast<int>(scanPageIntent->getInterleaved()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : CcdChannel : %d", static_cast<int>(scanPageIntent->getCcdChannel()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : BinaryRendering : %d", static_cast<int>(scanPageIntent->getBinaryRendering()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Descreen : %d", static_cast<int>(scanPageIntent->getDescreen()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : FeederPickStop : %d", static_cast<int>(scanPageIntent->getFeederPickStop()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Shadow : %d", static_cast<int>(scanPageIntent->getShadow()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : CompressionFactor : %d", static_cast<int>(scanPageIntent->getCompressionFactor()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : Threshold : %d", static_cast<int>(scanPageIntent->getThreshold()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanAutoColorDetect : %d", static_cast<int>(scanPageIntent->getScanAutoColorDetect()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanBlackBackground : %d", static_cast<int>(scanPageIntent->getScanBlackBackground()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanNumberPages : %d", static_cast<int>(scanPageIntent->getScanNumberPages()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanAutoExposure : %d", static_cast<int>(scanPageIntent->getScanAutoExposure()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanGamma : %d", static_cast<int>(scanPageIntent->getScanGamma()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanHighlight : %d", static_cast<int>(scanPageIntent->getScanHighlight()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanColorSensitivity : %d", static_cast<int>(scanPageIntent->getScanColorSensitivity()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanColorRange : %d", static_cast<int>(scanPageIntent->getScanColorRange()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : OverScan : %d", static_cast<int>(scanPageIntent->getOverScan()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : AutoCrop : %d", static_cast<int>(scanPageIntent->getAutoCrop()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanNoiseRemoval: %d",  static_cast<int>(scanPageIntent->getScanNoiseRemoval()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanBlankPageSensitivity: %d",    static_cast<int>(scanPageIntent->getScanBlankPageSensitivity()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanCaptureMode: %d",    static_cast<int>(scanPageIntent->getScanCaptureMode()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : AutoRelease: %d",    static_cast<int>(scanPageIntent->getAutoRelease()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanAcquisitionsSpeed: %d",    static_cast<int>(scanPageIntent->getScanAcquisitionsSpeed()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : IsCalibrationJob: %d",    static_cast<int>(scanPageIntent->getIsCalibrationJob()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : TopOffsetOversize: %d",    static_cast<int>(scanPageIntent->getTopOffsetOversize()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : BottomOffsetOversize: %d",    static_cast<int>(scanPageIntent->getBottomOffsetOversize()));
    CHECKPOINTC("CopyJobTicket::scanPageIntentDumper : ScanInYcc: %d",    static_cast<int>(scanPageIntent->getScanInYcc()));
}

dune::framework::data::backup::OperationResult CopyJobTicket::writeSettingsToFile(std::string filepath)
{
    CHECKPOINTC("CopyJobTicket:: writeSettingsToFile");
    dune::framework::data::backup::OperationResult result;
    char * path = const_cast<char*>(filepath.c_str());
    auto intent = this->getIntent();
    auto copyJobTicket = std::make_shared<CopyJobTicket>(*this);

    std::ofstream outfile(path, std::ios::out | std::ios::app | std::ios::binary | std::ios::ate);

    if (outfile.is_open())
    {
        flatbuffers::FlatBufferBuilder configFbb;
        auto flatBufferT = std::make_unique<dune::copy::Jobs::Copy::CopyJobTicketFbT>();
        flatBufferT->intent = serializeCopyJobIntent(this->getIntent());
        flatBufferT = serializeCopyJobTicket(copyJobTicket);

        configFbb.Finish(CreateCopyJobTicketFb(configFbb, flatBufferT.get(), nullptr));
        outfile.write((const char*)configFbb.GetBufferPointer(), configFbb.GetSize());
        if(outfile.good())
        {
            CHECKPOINTC("CopyJobTicket:: writeSettingsToFile SUCCESS");
            result = dune::framework::data::backup::OperationResult::SUCCESS;
        }
        else
        {
            CHECKPOINTA("CopyJobTicket:: writeSettingsToFile FAILED");
            result = dune::framework::data::backup::OperationResult::ERROR;
        }
    }
    else
    {
        CHECKPOINTA("CopyJobTicket:: writeSettingsToFile Could not open backup file");
        result = dune::framework::data::backup::OperationResult::ERROR;
    }
    outfile.close();
    return result;

}

dune::framework::data::backup::OperationResult CopyJobTicket::readSettingsFromFile(const std::string& filePath)
{
    CHECKPOINTC("CopyJobTicket:: readSettingsFromFile");
    dune::framework::data::backup::OperationResult result(dune::framework::data::backup::OperationResult::ERROR);
    auto flatBufferT = std::make_unique<dune::copy::Jobs::Copy::CopyJobTicketFbT>();
    auto jobTicket = std::make_shared<CopyJobTicket>(*this);

    std::ifstream infile(filePath.c_str(), std::ios::in | std::ios::binary | std::ios::ate);

    if (infile.is_open())
    {
        std::streampos begin, end;
        infile.seekg(0, std::ios::beg);
        begin = infile.tellg();
        infile.seekg(0, std::ios::end);
        end = infile.tellg();

        std::streamsize size = end - begin;
        infile.seekg(0, std::ios::beg);

        std::vector<char> buffer(size);
        if (infile.read(buffer.data(), size))
        {
            const CopyJobTicketFb *configData =
                dune::framework::utils::FlatbufferHelper::verifyAndGetFlatbuffer<CopyJobTicketFb>(
                    (const uint8_t*)buffer.data(), (size_t)size);

            /* Verify the persisted configuration */
            if (configData)
            {
                CHECKPOINTC("CopyJobTicket::readSettingsFromFile: calling configData->UnPackTo ");
                configData->UnPackTo(flatBufferT.get());
            }
            else
            {
                CHECKPOINTA("CopyJobTicket::readSettingsFromFile:  configData read failed ");
                return dune::framework::data::backup::OperationResult::ERROR;
            }
            result = dune::framework::data::backup::OperationResult::SUCCESS;
            CHECKPOINTC("CopyJobTicket::readSettingsFromFile: SUCCESS");
        }
    }
    else
    {
        CHECKPOINTA("CopyJobTicket::readSettingsFromFile - Could not open backup file.");
        result = dune::framework::data::backup::OperationResult::ERROR;
    }
    infile.close();
    if(result == dune::framework::data::backup::OperationResult::SUCCESS)
    {
        std::shared_ptr<CopyJobIntentFbT> intent = std::move(flatBufferT->intent);
        if(deserializeCopyJobIntent(intent, this->getIntent()))
        {
            result = dune::framework::data::backup::OperationResult::SUCCESS;
        }
        else
        {
            result = dune::framework::data::backup::OperationResult::ERROR;
        }
    }

    return result;
}

CopyJobResult::CopyJobResult()
    : completedPages_{0},
      completedCopies_{0},
      currentPage_{0},
      remainingPrintingTime_{0},
      progress_{0},
      currentCuringTemperature_{0},
      allPagesDiscovered_{false},
      pixelCounts_{}
{
}

CopyJobResult::CopyJobResult(const ICopyJobResult& copyJobResult)
    : completedPages_{copyJobResult.getCompletedImpressions()},
      completedCopies_{copyJobResult.getCompletedCopies()},
      currentPage_{copyJobResult.getCurrentPage()},
      remainingPrintingTime_{copyJobResult.getRemainingPrintingTime()},
      progress_{copyJobResult.getProgress()},
      currentCuringTemperature_{copyJobResult.getCurrentCuringTemperature()},
      allPagesDiscovered_{copyJobResult.areAllPagesDiscovered()},
      pixelCounts_{copyJobResult.getPixelCounts()} 
      {};

std::unique_ptr<ICopyJobResult> CopyJobResult::clone()
{
    std::unique_ptr<CopyJobResult> copyJobResult = std::make_unique<CopyJobResult>();
    copyJobResult->completedPages_ = getCompletedImpressions();
    copyJobResult->completedCopies_ = getCompletedCopies();
    copyJobResult->currentPage_ = getCurrentPage();
    copyJobResult->remainingPrintingTime_ = getRemainingPrintingTime();
    copyJobResult->progress_ = getProgress();
    copyJobResult->currentCuringTemperature_ = getCurrentCuringTemperature();
    copyJobResult->remainingPrintingTime_ = getRemainingPrintingTime();
    copyJobResult->pixelCounts_ = getPixelCounts();
    return copyJobResult;
}

std::unique_ptr<CopyJobResultFbT> CopyJobResult::serialize() const
{
    std::unique_ptr<CopyJobResultFbT> data = std::make_unique<CopyJobResultFbT>();
    data->completedImpressions = getCompletedImpressions();
    data->completedCopies = getCompletedCopies();
    data->currentPage = getCurrentPage();
    data->remainingPrintingTime = getRemainingPrintingTime();
    const auto pixelCounts = getPixelCounts();
    std::unique_ptr<dune::job::PixelCountsFbT> pixelCountsFbt = std::make_unique<dune::job::PixelCountsFbT>();
    pixelCountsFbt->nonWhitePixelCount = pixelCounts.nonWhitePixelCount;
    pixelCountsFbt->colorPixelCount = pixelCounts.colorPixelCount;
    pixelCountsFbt->totalPixelCount = pixelCounts.totalPixelCount;
    data->pixelCounts = std::move(pixelCountsFbt);
    return data;
}

void CopyJobResult::deserialize(const CopyJobResultFbT& data)
{
    setCompletedCopies(data.completedCopies);
    setCompletedImpressions(data.completedImpressions);
    setCurrentPage(data.currentPage);
    setRemainingPrintingTime(data.remainingPrintingTime);
    if(data.pixelCounts)
    {
        setPixelCounts({data.pixelCounts->nonWhitePixelCount, data.pixelCounts->colorPixelCount, 
                        data.pixelCounts->totalPixelCount});
    }
}

}}}};
