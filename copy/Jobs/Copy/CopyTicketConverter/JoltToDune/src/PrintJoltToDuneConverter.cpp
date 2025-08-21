/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   PrintJoltToDuneConverter.cpp
 * @date   Tue, 06 May 2025
 * @brief  Implementation for Jolt to Dune print data converter
 *
 * (C) Copyright 2025 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "PrintJoltToDuneConverter.h"
#include "common_debug.h"
#include "PrintJoltToDuneConverter_TraceAutogen.h"
#include "typeMappers.h"

using APIResult = dune::framework::core::APIResult;

namespace dune { namespace copy { namespace Jobs { namespace Copy {

PrintJoltToDuneConverter::PrintJoltToDuneConverter() {
    // Initialize converters
}

PrintJoltToDuneConverter::~PrintJoltToDuneConverter() {
    // Clean up resources
}


template <typename T, typename ConversionFunc>
void PrintJoltToDuneConverter::convertXml(
    dune::framework::utils::XmlUtils& xml,
    const std::string& xpath,
    dune::cdm::easyBuffers::OptionalProperty<T>& property,
    ConversionFunc mapper)
{
    CHECKPOINTA_STR("PrintJoltToDuneConverter::convertXml: %s", xpath.c_str());
    if(property.isSet()) return;

    if (xml.isKeyAvailable(xpath))
    {
        CHECKPOINTB_STR("PrintJoltToDuneConverter::Key available in XML: %s", xpath.c_str());
        std::string xmlValue = xml[xpath].front();
        property.set(mapper(xmlValue));
    }
    else
    {
        CHECKPOINTA_STR("PrintJoltToDuneConverter::Key not available in XML: %s", xpath.c_str());
    }
}


//ChromaticMode needs to be added in convert as in Dune we take scan values for color mode
/*
ChromaticMode mapStringToChromaticMode(const std::string& value) {
    if (value == "autoDetect") return ChromaticMode::AutoDetect;
    if (value == "monochrome") return ChromaticMode::Monochrome;
    if (value == "color") return ChromaticMode::Color;
    if (value == "grayscale") return ChromaticMode::Grayscale;
    if (value == "minimalColor") return ChromaticMode::MinimalColor;
    if (value == "other") return ChromaticMode::Other;
    return ChromaticMode::AutoDetect; // default
}
*/

// SheetCollate
dune::copy::SheetCollate PrintJoltToDuneConverter::mapStringToSheetCollate(const std::string& value) {
    if (value == "Collated") return dune::copy::SheetCollate::Collate;
    if (value == "Uncollated") return dune::copy::SheetCollate::Uncollate;
    return dune::copy::SheetCollate::Collate;
}


// CopyOriginalOutputBinding Correct Mapping needs to be checked as duplexBinding is not matching
/*CopyOriginalOutputBinding PrintJoltToDuneConverter::mapStringToCopyOriginalOutputBinding(const std::string& value) {
    if (value == "sideToSide") return CopyOriginalOutputBinding::SideToSide;
    if (value == "sideToTop") return CopyOriginalOutputBinding::SideToTop;
    if (value == "topToSide") return CopyOriginalOutputBinding::TopToSide;
    if (value == "topToTop") return CopyOriginalOutputBinding::TopToTop;
    return CopyOriginalOutputBinding::SideToSide;
}*/

// MediaInputID
dune::imaging::types::MediaSource PrintJoltToDuneConverter::mapStringToMediaInputId(const std::string& value)
{
    CHECKPOINTA_STR("PrintJoltToDuneConverter::mapStringToMediaInputId: %s", value.c_str());
    if (value == "ADF") return dune::imaging::types::MediaSource::ADF;
    if (value == "EnvFeed") return dune::imaging::types::MediaSource::ENVFEED;
    if (value == "Flatbed") return dune::imaging::types::MediaSource::FLATBED;
    if (value == "PrinterSelect") return dune::imaging::types::MediaSource::AUTOSELECT;
    if (value == "Tray1") return dune::imaging::types::MediaSource::TRAY1;
    if (value == "Tray2") return dune::imaging::types::MediaSource::TRAY2;
    if (value == "Tray3") return dune::imaging::types::MediaSource::TRAY3;
    if (value == "Tray4") return dune::imaging::types::MediaSource::TRAY4;
    if (value == "Tray5") return dune::imaging::types::MediaSource::TRAY5;
    if (value == "Tray6") return dune::imaging::types::MediaSource::TRAY6;
    if (value == "Tray7") return dune::imaging::types::MediaSource::TRAY7;
    if (value == "Tray8") return dune::imaging::types::MediaSource::TRAY8;
    if (value == "Tray9") return dune::imaging::types::MediaSource::TRAY9;
    if (value == "Tray10") return dune::imaging::types::MediaSource::TRAY10;
    if (value == "Tray11") return dune::imaging::types::MediaSource::TRAY11;
    if (value == "Tray12") return dune::imaging::types::MediaSource::TRAY12;
    if (value == "Tray13") return dune::imaging::types::MediaSource::TRAY13;
    if (value == "Roll1") return dune::imaging::types::MediaSource::ROLL1;
    if (value == "Roll2") return dune::imaging::types::MediaSource::ROLL2;
    if (value == "Roll3") return dune::imaging::types::MediaSource::ROLL3;
    if (value == "Roll4") return dune::imaging::types::MediaSource::ROLL4;
    if (value == "ManualFeed") return dune::imaging::types::MediaSource::MANUALFEED;
    if (value == "RearManualFeed") return dune::imaging::types::MediaSource::REAR;
    if (value == "PhotoTray") return dune::imaging::types::MediaSource::PHOTO;
    if (value == "MultiPurpose_Tray") return dune::imaging::types::MediaSource::TRAY1;
    //Correspondng Fbs values are not present for these Jolt Enums
    //if (value == "Tray14") return dune::imaging::types::MediaSource::TRAY14;
    //if (value == "Tray15") return dune::imaging::types::MediaSource::TRAY15;
    //if (value == "MultiPurpose_Tray") return MediaInputId::MultipurposeTray;
    //if (value == "External") return MediaInputId::External;
    //if (value == "Other") return MediaInputId::Other;
    //if (value == "Duplexer") return dune::imaging::types::MediaSource::Duplexer;
    //if (value == "ExternalTray1") return MediaInputId::ExternalTray1;
    //if (value == "ExternalTray2") return MediaInputId::ExternalTray2;
    //if (value == "ExternalTray3") return MediaInputId::ExternalTray3;
    //if (value == "ExternalTray4") return MediaInputId::ExternalTray4;
    //if (value == "ExternalTray5") return MediaInputId::ExternalTray5;
    //if (value == "ExternalTray6") return MediaInputId::ExternalTray6;
    //if (value == "ExternalTray7") return MediaInputId::ExternalTray7;
    //if (value == "ExternalTray8") return MediaInputId::ExternalTray8;
    //if (value == "ExternalTray9") return MediaInputId::ExternalTray9;
    //if (value == "ExternalTray10") return MediaInputId::ExternalTray10;
    //if (value == "Tray1JobSettings") return MediaInputId::Tray1JobSettings;
    //if (value == "EnvFeedJobSettings") return MediaInputId::EnvelopeFeedJobSettings;
    return dune::imaging::types::MediaSource::AUTOSELECT; // default
}

dune::imaging::types::MediaDestinationId PrintJoltToDuneConverter::mapStringToMediaOutputId(const std::string& value) {
    using dune::imaging::types::MediaDestinationId;
    if (value == "OutputBin1") return MediaDestinationId::OUTPUTBIN1;
    if (value == "OutputBin2") return MediaDestinationId::OUTPUTBIN2;
    if (value == "OutputBin3") return MediaDestinationId::OUTPUTBIN3;
    if (value == "OutputBin4") return MediaDestinationId::OUTPUTBIN4;
    if (value == "OutputBin5") return MediaDestinationId::OUTPUTBIN5;
    if (value == "OutputBin6") return MediaDestinationId::OUTPUTBIN6;
    if (value == "OutputBin7") return MediaDestinationId::OUTPUTBIN7;
    if (value == "OutputBin8") return MediaDestinationId::OUTPUTBIN8;
    if (value == "Stacker") return MediaDestinationId::STACKER;
    if (value == "Stacker-Staples") return MediaDestinationId::STACKER2; //check mapping
    if (value == "StackerFaceUp") return MediaDestinationId::STACKER3; //check mapping
    if (value == "StackerFaceDown") return MediaDestinationId::STACKER4; //check mapping
    if (value == "PrinterSelect") return MediaDestinationId::AUTOSELECT;
    if (value == "Accessory") return MediaDestinationId::GENERIC_ACCESSORY;
    if (value == "StandardCorrectOrder") return MediaDestinationId::DEFAULT;
    if (value == "RearStraightestPath") return MediaDestinationId::DEFAULT;
    if (value == "LeftStraightestPath") return MediaDestinationId::DEFAULT;
    if (value == "UpperLeftBins") return MediaDestinationId::DEFAULT;
    if (value == "Standard") return MediaDestinationId::STANDARDBIN;
    if (value == "Alternate") return MediaDestinationId::ALTERNATE;
    
    //Correspondng Fbs values are not present for these Jolt Enums
    if (value == "Bottom") return MediaDestinationId::DEFAULT;
    if (value == "Center") return MediaDestinationId::DEFAULT;
    if (value == "Face-down") return MediaDestinationId::DEFAULT;
    if (value == "Face-up") return MediaDestinationId::DEFAULT;
    if (value == "Large-capacity") return MediaDestinationId::DEFAULT;
    if (value == "Left") return MediaDestinationId::DEFAULT;
    if (value == "Middle") return MediaDestinationId::DEFAULT;
    if (value == "My-mailbox") return MediaDestinationId::DEFAULT;
    if (value == "Rear") return MediaDestinationId::DEFAULT;
    if (value == "Right") return MediaDestinationId::DEFAULT;
    if (value == "Side") return MediaDestinationId::DEFAULT;
    if (value == "Top") return MediaDestinationId::DEFAULT;
    if (value == "Stapler") return MediaDestinationId::DEFAULT; // not in .fbs
    if (value == "Collator") return MediaDestinationId::DEFAULT; // not in .fbs
    if (value == "VirtualBins1To3") return MediaDestinationId::DEFAULT;
    if (value == "VirtualBins1To5") return MediaDestinationId::DEFAULT;
    if (value == "VirtualBins1To8") return MediaDestinationId::DEFAULT;
    if (value == "VirtualBins1To10") return MediaDestinationId::DEFAULT;
    if (value == "VirtualBins2To8") return MediaDestinationId::DEFAULT;
    if (value == "VirtualFinisherBins") return MediaDestinationId::DEFAULT;
    if (value == "VirtualLeftBins") return MediaDestinationId::DEFAULT;
    if (value == "StandardTop") return MediaDestinationId::DEFAULT;
    if (value == "Upper") return MediaDestinationId::DEFAULT;
    if (value == "Lower") return MediaDestinationId::DEFAULT;
    if (value == "LowerBooklet") return MediaDestinationId::DEFAULT;
    if (value == "EngineOptionalBin1") return MediaDestinationId::DEFAULT;
    if (value == "VirtualBins1To4") return MediaDestinationId::DEFAULT;
    if (value == "VirtualBins3To4") return MediaDestinationId::DEFAULT;
    
    //if (value == "Booklet") return MediaDestinationId::BOOKLET;
    //if (value == "External") return MediaDestinationId::EXTERNAL;
    //if (value == "UniversalOutputBin") return MediaDestinationId::UNIVERSALOUTPUTBIN;
    //if (value == "Other") return MediaDestinationId::OTHER;
    //if (value == "Duplexer") return MediaDestinationId::DUPLEXER;
    //if (value == "LowerLeft") return MediaDestinationId::LOWERLEFT;
    //if (value == "MiddleLeft") return MediaDestinationId::MIDDLELEFT;
    //if (value == "UpperLeft") return MediaDestinationId::UPPERLEFT;
    
    //Corresponding JOLT XML Values not present for these FBS values
    // MediaDestinationId::DEFAULT;
    // MediaDestinationId::BIN;
    // MediaDestinationId::OUTPUTBIN9;
    // MediaDestinationId::OUTPUTBIN10;
    // MediaDestinationId::FOLDER;
    // MediaDestinationId::FOLDER2;
    // MediaDestinationId::FOLDER3;
    // MediaDestinationId::FOLDER4;
    // MediaDestinationId::ACCESSORY_STACKER;
    // MediaDestinationId::TAKE_UP_REEL;
    // MediaDestinationId::HORIZONTAL_CUTTER;
    // MediaDestinationId::VERTICAL_CUTTER;

    return MediaDestinationId::DEFAULT;
}

dune::imaging::types::StapleOptions PrintJoltToDuneConverter::mapStringToStaple(const std::string& value) {
    using dune::imaging::types::StapleOptions;
    if (value == "none") return StapleOptions::NONE;
    if (value == "default") return StapleOptions::DEFAULT;
    if (value == "topAnyOnePointAny") return StapleOptions::TOP_ANY_ONE_POINT_ANY;
    if (value == "topAnyOnePointAngled") return StapleOptions::TOP_ANY_ONE_POINT_ANGLED;
    if (value == "topLeftOnePointAny") return StapleOptions::TOP_LEFT_ONE_POINT_ANY;
    if (value == "topLeftOnePointAngled") return StapleOptions::TOP_LEFT_ONE_POINT_ANGLED;
    if (value == "topLeftOnePointHorizontal") return StapleOptions::TOP_LEFT_ONE_POINT_HORIZONTAL;
    if (value == "topLeftOnePointVertical") return StapleOptions::TOP_LEFT_ONE_POINT_VERTICAL;
    if (value == "topRightOnePointAny") return StapleOptions::TOP_RIGHT_ONE_POINT_ANY;
    if (value == "topRightOnePointAngled") return StapleOptions::TOP_RIGHT_ONE_POINT_ANGLED;
    if (value == "topRightOnePointHorizontal") return StapleOptions::TOP_RIGHT_ONE_POINT_HORIZONTAL;
    if (value == "topRightOnePointVertical") return StapleOptions::TOP_RIGHT_ONE_POINT_VERTICAL;
    if (value == "bottomLeftOnePointAny") return StapleOptions::BOTTOM_LEFT_ONE_POINT_ANY;
    if (value == "bottomLeftOnePointAngled") return StapleOptions::BOTTOM_LEFT_ONE_POINT_ANGLED;
    if (value == "bottomLeftOnePointHorizontal") return StapleOptions::BOTTOM_LEFT_ONE_POINT_HORIZONTAL;
    if (value == "bottomLeftOnePointVertical") return StapleOptions::BOTTOM_LEFT_ONE_POINT_VERTICAL;
    if (value == "bottomRightOnePointAny") return StapleOptions::BOTTOM_RIGHT_ONE_POINT_ANY;
    if (value == "bottomRightOnePointAngled") return StapleOptions::BOTTOM_RIGHT_ONE_POINT_ANGLED;
    if (value == "bottomRightOnePointHorizontal") return StapleOptions::BOTTOM_RIGHT_ONE_POINT_HORIZONTAL;
    if (value == "bottomRightOnePointVertical") return StapleOptions::BOTTOM_RIGHT_ONE_POINT_VERTICAL;
    if (value == "centerOnePoint") return StapleOptions::CENTER_POINT_POINT;
    if (value == "leftTwoPoints") return StapleOptions::LEFT_TWO_POINTS;
    if (value == "leftTwoPointsAny") return StapleOptions::LEFT_TWO_POINTS_ANY;
    if (value == "rightTwoPoints") return StapleOptions::RIGHT_TWO_POINTS;
    if (value == "topTwoPoints") return StapleOptions::TOP_TWO_POINTS;
    if (value == "bottomTwoPoints") return StapleOptions::BOTTOM_TWO_POINTS;
    if (value == "centerTwoPoints") return StapleOptions::CENTER_TWO_POINTS;
    if (value == "leftThreePoints") return StapleOptions::LEFT_THREE_POINTS;
    if (value == "leftThreePointsAny") return StapleOptions::LEFT_THREE_POINTS_ANY;
    if (value == "rightThreePoints") return StapleOptions::RIGHT_THREE_POINTS;
    if (value == "topThreePoints") return StapleOptions::TOP_THREE_POINTS;
    if (value == "bottomThreePoints") return StapleOptions::BOTTOM_THREE_POINTS;
    if (value == "centerThreePoints") return StapleOptions::CENTER_THREE_POINTS;
    if (value == "leftSixPoints") return StapleOptions::LEFT_SIX_POINTS;
    if (value == "leftSixPointsAny") return StapleOptions::LEFT_SIX_POINTS_ANY;
    if (value == "rightSixPoints") return StapleOptions::RIGHT_SIX_POINTS;
    if (value == "topSixPoints") return StapleOptions::TOP_SIX_POINTS;
    if (value == "bottomSixPoints") return StapleOptions::BOTTOM_SIX_POINTS;
    if (value == "centerSixPoints") return StapleOptions::CENTER_SIX_POINTS;

    // The following StapleOptions from FinishingOptions.fbs do not have a corresponding value in xmlvalues:
    // if (value == "customLegacy") return ...;
    // if (value == "customPointsOption1") return ...;
    // if (value == "customPointsOption2") return ...;
    // if (value == "customPointsOption3") return ...;
    // if (value == "customPointsOption4") return ...;
    // if (value == "customPointsOption5") return ...;
    // if (value == "customPointsOption6") return ...;
    // if (value == "customPointsOption7") return ...;
    // if (value == "customPointsOption8") return ...;
    // if (value == "customPointsOption9") return ...;
    // if (value == "customPointsOption10") return ...;
    // if (value == "extraOption1") return ...;
    // if (value == "extraOption2") return ...;
    // if (value == "extraOption3") return ...;
    // if (value == "extraOption4") return ...;
    // if (value == "extraOption5") return ...;
    // if (value == "extraOption6") return ...;
    // if (value == "extraOption7") return ...;
    // if (value == "extraOption8") return ...;
    // if (value == "extraOption9") return ...;
    // if (value == "extraOption10") return ...;

    return StapleOptions::NONE;
}

dune::imaging::types::PunchingOptions PrintJoltToDuneConverter::mapStringToPunchingOptions(const std::string& value) {
    using dune::imaging::types::PunchingOptions;
    if (value == "none") return PunchingOptions::NONE;
    if (value == "default") return PunchingOptions::DEFAULT;
    if (value == "twoPointAny") return PunchingOptions::TWO_POINT_ANY;
    if (value == "leftTwoPointDin") return PunchingOptions::LEFT_TWO_POINT_DIN;
    if (value == "rightTwoPointDin") return PunchingOptions::RIGHT_TWO_POINT_DIN;
    if (value == "topTwoPointDin") return PunchingOptions::TOP_TWO_POINT_DIN;
    if (value == "bottomTwoPointDin") return PunchingOptions::BOTTOM_TWO_POINT_DIN;
    if (value == "twoPointDin") return PunchingOptions::TWO_POINT_DIN;
    if (value == "leftTwoPointUs") return PunchingOptions::LEFT_TWO_POINT_US;
    if (value == "rightTwoPointUs") return PunchingOptions::RIGHT_TWO_POINT_US;
    if (value == "topTwoPointUs") return PunchingOptions::TOP_TWO_POINT_US;
    if (value == "bottomTwoPointUs") return PunchingOptions::BOTTOM_TWO_POINT_US;
    if (value == "twoPointUs") return PunchingOptions::TWO_POINT_US;
    if (value == "leftThreePointUs") return PunchingOptions::LEFT_THREE_POINT_US;
    if (value == "rightThreePointUs") return PunchingOptions::RIGHT_THREE_POINT_US;
    if (value == "topThreePointUs") return PunchingOptions::TOP_THREE_POINT_US;
    if (value == "bottomThreePointUs") return PunchingOptions::BOTTOM_THREE_POINT_US;
    if (value == "threePointUs") return PunchingOptions::THREE_POINT_US;
    if (value == "threePointAny") return PunchingOptions::THREE_POINT_ANY;
    if (value == "leftFourPointDin") return PunchingOptions::LEFT_FOUR_POINT_DIN;
    if (value == "rightFourPointDin") return PunchingOptions::RIGHT_FOUR_POINT_DIN;
    if (value == "topFourPointDin") return PunchingOptions::TOP_FOUR_POINT_DIN;
    if (value == "bottomFourPointDin") return PunchingOptions::BOTTOM_FOUR_POINT_DIN;
    if (value == "fourPointDin") return PunchingOptions::FOUR_POINT_DIN;
    if (value == "leftFourPointSwd") return PunchingOptions::LEFT_FOUR_POINT_SWD;
    if (value == "rightFourPointSwd") return PunchingOptions::RIGHT_FOUR_POINT_SWD;
    if (value == "topFourPointSwd") return PunchingOptions::TOP_FOUR_POINT_SWD;
    if (value == "bottomFourPointSwd") return PunchingOptions::BOTTOM_FOUR_POINT_SWD;
    if (value == "fourPointSwd") return PunchingOptions::FOUR_POINT_SWD;
    if (value == "fourPointAny") return PunchingOptions::FOUR_POINT_ANY;
    if (value == "leftTwoPoint") return PunchingOptions::LEFT_TWO_POINT;
    if (value == "rightTwoPoint") return PunchingOptions::RIGHT_TWO_POINT;
    if (value == "topTwoPoint") return PunchingOptions::TOP_TWO_POINT;
    if (value == "bottomTwoPoint") return PunchingOptions::BOTTOM_TWO_POINT;
    if (value == "jediUnknown") return PunchingOptions::NONE; // No direct mapping, fallback

    return PunchingOptions::NONE;
}

dune::imaging::types::BookletMakingOptions PrintJoltToDuneConverter::mapStringToBookletMaker(const std::string& value) {
    using dune::imaging::types::BookletMakingOptions;
    if (value == "None") return BookletMakingOptions::NONE;
    if (value == "BookletMaker") return BookletMakingOptions::BOOKLET_MAKER;
    if (value == "jediUnknown") return BookletMakingOptions::NONE; // No direct mapping, fallback

    // The following BookletMakingOptions from FinishingOptions.fbs do not have a corresponding value in xmlvalues:
    // DEFAULT
    // SADDLE_STITCH

    return BookletMakingOptions::NONE;
}

dune::imaging::types::PrintQuality PrintJoltToDuneConverter::mapStringToPrintQuality(const std::string& value) {
    using dune::imaging::types::PrintQuality;
    if (value == "Draft") return PrintQuality::DRAFT;
    if (value == "High") return PrintQuality::UNDEFINED; // Not in .fbs
    if (value == "Normal") return PrintQuality::NORMAL;
    if (value == "Best") return PrintQuality::BEST;
    if (value == "Custom") return PrintQuality::UNDEFINED; // Not in .fbs
    if (value == "Default") return PrintQuality::UNDEFINED; // Not in .fbs
    if (value == "FastNormal") return PrintQuality::FAST_NORMAL;
    if (value == "Fast") return PrintQuality::UNDEFINED; // Not in .fbs
    if (value == "Good") return PrintQuality::UNDEFINED; // Not in .fbs
    if (value == "Marvelous") return PrintQuality::MARVELOUS;
    if (value == "SuperDraft") return PrintQuality::UNDEFINED; // Not in .fbs
    if (value == "Any") return PrintQuality::UNDEFINED; // Not in .fbs
    if (value == "Economode") return PrintQuality::ECONOMODE;
    if (value == "Depleted") return PrintQuality::DEPLETED;

    // The following PrintQuality options from PrintQuality.fbs do not have a corresponding value in xmlvalues:
    // MAXIMUM
    // AUTOSELECT
    // UNDEFINED

    return PrintQuality::UNDEFINED;
}

dune::imaging::types::FoldingOptions PrintJoltToDuneConverter::mapStringToFolding(const std::string& value) {
    using dune::imaging::types::FoldingOptions;
    if (value == "none") return FoldingOptions::NONE;
    if (value == "default") return FoldingOptions::DEFAULT;
    if (value == "cInwardTop") return FoldingOptions::C_INWARD_TOP;
    if (value == "cInwardBottom") return FoldingOptions::C_INWARD_BOTTOM;
    if (value == "cOutwardTop") return FoldingOptions::C_OUTWARD_TOP;
    if (value == "cOutwardBottom") return FoldingOptions::C_OUTWARD_BOTTOM;
    if (value == "vInwardTop") return FoldingOptions::V_INWARD_TOP;
    if (value == "vInwardBottom") return FoldingOptions::V_INWARD_BOTTOM;
    if (value == "vOutwardTop") return FoldingOptions::V_OUTWARD_TOP;
    if (value == "vOutwardBottom") return FoldingOptions::V_OUTWARD_BOTTOM;

    return FoldingOptions::NONE;
}

dune::imaging::types::MediaIdType PrintJoltToDuneConverter::mapStringToMediaTypeId(const std::string& value) {
    using dune::imaging::types::MediaIdType;
    if (value == "anySupportedType") return MediaIdType::ANY;
    if (value == "plain") return MediaIdType::STATIONERY;
    if (value == "HPMatte90gsm") return MediaIdType::HPMATTE90G;
    if (value == "HPMatte105gsm") return MediaIdType::HPMATTE105G;
    if (value == "HPMatte120gsm") return MediaIdType::HPMATTE120G;
    if (value == "HPPremiumPresentationMatte") return MediaIdType::HP_MATTE_PRESENTATION;
    if (value == "HPMatteBrochureAndFlyer") return MediaIdType::HPBROCHURE_MATTE;
    if (value == "HPMatteCover200gsm") return MediaIdType::HPGLOSSY200G;
    if (value == "HPMatte200gsm") return MediaIdType::HPMATTE200G;
    if (value == "HPSoftGloss120gsm") return MediaIdType::HPSOFTGLOSS120G;
    if (value == "HPGlossy220gsm") return MediaIdType::HPGLOSSY200G; 
    if (value == "light") return MediaIdType::LIGHT;
    if (value == "intermediate") return MediaIdType::INTERMEDIATE;
    if (value == "midweight") return MediaIdType::MIDWEIGHT;
    if (value == "heavy") return MediaIdType::HEAVY;
    if (value == "extraHeavy") return MediaIdType::EXTRAHEAVY;
    if (value == "cardstock") return MediaIdType::CARDSTOCK;
    if (value == "matte") return MediaIdType::HP_MATTE_FILM; // check correct mapping alternate matte_film
    if (value == "matteBrochure") return MediaIdType::HPMATTE_BROCHURE; 
    if (value == "midweightGlossy") return MediaIdType::MIDWEIGHTGLOSSY;
    if (value == "heavyGlossy") return MediaIdType::HEAVYGLOSSY;
    if (value == "extraHeavyGloss") return MediaIdType::EXTRAHEAVYGLOSSY;
    if (value == "cardstockGlossy") return MediaIdType::CARDGLOSSY;
    if (value == "transparency") return MediaIdType::TRANSPARENCY;
    if (value == "labels") return MediaIdType::LABELS;
    if (value == "stationery-letterhead") return MediaIdType::LETTERHEAD;
    if (value == "envelope") return MediaIdType::ENVELOPE;
    if (value == "heavyEnvelope") return MediaIdType::HEAVYENVELOPE;
    if (value == "stationery-preprinted") return MediaIdType::PREPRINTED;
    if (value == "stationery-prepunched") return MediaIdType::PREPUNCHED;
    if (value == "color") return MediaIdType::COLORED;
    if (value == "bond") return MediaIdType::BOND;
    if (value == "recycled") return MediaIdType::RECYCLED;
    if (value == "rough") return MediaIdType::ROUGH;
    if (value == "heavyRough") return MediaIdType::HEAVYROUGH;
    if (value == "filmOpaque") return MediaIdType::OPAQUEFILM;
    if (value == "userDefined1") return MediaIdType::USER_DEFINED_1;
    if (value == "userDefined2") return MediaIdType::USER_DEFINED_2;
    if (value == "userDefined3") return MediaIdType::USER_DEFINED_3;
    if (value == "userDefined4") return MediaIdType::USER_DEFINED_4;
    if (value == "userDefined5") return MediaIdType::USER_DEFINED_5;
    if (value == "userDefined6") return MediaIdType::USER_DEFINED_6;
    if (value == "userDefined7") return MediaIdType::USER_DEFINED_7;
    if (value == "userDefined8") return MediaIdType::USER_DEFINED_8;
    if (value == "userDefined9") return MediaIdType::USER_DEFINED_9;
    if (value == "userDefined10") return MediaIdType::USER_DEFINED_10;
    if (value == "other") return MediaIdType::OTHERMATTE; //check Mapping custom also option
    if (value == "auto") return MediaIdType::ANY; // Check mapping
    if (value == "HPEcoSMARTLite") return MediaIdType::HPECOFFICIENT; // Check Mapping
    if (value == "HPBrochureMatte") return MediaIdType::HPBROCHURE_MATTE;
    if (value == "HPBrochureGlossy") return MediaIdType::HPBROCHURE_GLOSSY;
    if (value == "HPAdvancedPhoto") return MediaIdType::HPPHOTO; //Check mapping
    if (value == "lightBond") return MediaIdType::LIGHTBOND;
    if (value == "lightPaperboard") return MediaIdType::LIGHTPAPERBOARD;
    if (value == "paperboard") return MediaIdType::PAPERBOARD;
    if (value == "heavyPaperboard") return MediaIdType::HEAVYPAPERBOARD;


    //if (value == "HPMatte160gsm") return ...; // Not in .fbs
    // if (value == "HPGlossy130gsm") return ...; // Not in .fbs
    // if (value == "HPGlossy160gsm") return ...; // Not in .fbs
    // if (value == "HPGlossyEdgeline180g") return ...; // Not in .fbs
    // if (value == "vellum") return ...; // Not in .fbs
    // if (value == "tab-stock") return ...; // Not in .fbs
    // if (value == "HPToughPaper") return ...; // Not in .fbs
    // if (value == "matteCover") return ...; // Not in .fbs
    // if (value == "HPTransparencyInkjet") return ...; // Not in .fbs
    // if (value == "shelfEdgeLabel") return ...; // Not in .fbs
    // if (value == "heavyBond") return ...; // Not in .fbs
    // if (value == "lightRough") return ...; // Not in .fbs
    
    // The following MediaIdType options from MediaType.fbs do not have a corresponding value in xmlvalues:
    // CUSTOM
    // HPMATTE150G
    // HPGLOSSY120G
    // HPGLOSSY150G
    // HPTRIFOLDGLOSSY150G
    // HPGLOSSY200G
    // PLAIN_PAPER_GRAPHICS
    // BLUEPRINT
    // BLUEPRINT_WITH_RED_STAMP
    // UNIVERSAL_BOND
    // COATED
    // UNIVERSAL_COATED
    // HEAVY_COATED
    // UNIVERSAL_HEAVYWEIGHT_COATED
    // GENERIC_COATED
    // GENERIC_HEAVY_COATED
    // NATURAL_TRACING
    // GENERIC_NATL_TRACING_LITE
    // GENERIC_NATL_TRACING
    // GENERIC_NTP_RUBBER_RESISTANT
    // PHOTO_GLOSSY
    // UNIVERSAL_GLOSS
    // UNIVERSAL_SATIN
    // UNIVERSAL_INSTANT_DRY_GLOSS
    // UNIVERSAL_INSTANT_DRY_SATIN
    // PHOTO_SATIN
    // POLY_SATIN
    // HP_CLEAR_FILM
    // HP_MATTE_FILM
    // CLEAR_FILM_KOD
    // MATTE_FILM
    // UNIVERSAL_ADHESIVE_VINYL
    // EVERYDAY_ADHESIVE_GLOSS_POLY
    // ADHESIVE
    // ADHESIVE_POLY_SATIN
    // HP_BRIGHT_WHITE
    // EVERYDAY_ADHESIVE_MATTE_POLY
    // ADHESIVE_MATTE_POLY
    // EVERYDAY_MATTE_POLY
    // PREMIUM_MATTE_POLY
    // MATTE_POLY
    // PLAIN_PAPER_RETAIL
    // ADHESIVE_BACKLIT
    // ADHESIVE_CAST
    // ADHESIVE_TRANSPARENT
    // CANVAS
    // HP_MATTE_PRESENTATION
    // PET_BACKLIT
    // PET_FRONTLIT
    // PET_FRONTLIT_TRANSPARENT
    // PPPE_BANNER
    // PVC_BANNER
    // PVC_BANNER_BACKLIT
    // STATIONERY_BACKLIT
    // STATIONERY_BLUEBACK
    // SYNTHETIC
    // SYNTHETIC_BACKLIT
    // TEXTILE
    // TEXTILE_BACKLIT
    // UNCOATED
    // WALLPAPER_NON_WOVEN
    // WALLPAPER_WOVEN
    // SATIN_WRAPPING_PAPER
    // DARK_BLUEPRINT
    // WHITE_PAPER
    // WHITE_PAPER_ENHANCED
    // IRON_ON_TRANSFER
    // UNDEFINED
    // COATED_CAD
    // POLYESTER_BACKLIT
    // HEAT_TRANSFER
    // WALLPAPER
    // SUPER_HEAVY_COATED
    // HPSOFTGLOSS120G
    // HP20BOND_COLORPRO_TECHNOLOGY
    // PREMIUM_BOND
    // BRIGHT_WHITE_BOND
    // PRODUCTION_MATTE_POSTER
    // PRODUCTION_SATIN_POSTER
    // GLOSS_POSTER
    // PHOTO_SEMI_GLOSS_SATIN
    // DOUBLE_MATTE_FILM
    // BACKLIT_MATERIAL
    // SUPER_HEAVYWEIGHT_COATED_MATTE_PLUS_AREA_FILLS
    // HPSPECIALTY_GLOSSY
    // HPMATTE_BROCHURE
    // PHOTO_MATTE_PAPER
    // PRODUCTION_MATTE_POLY
    // SUPER_HEAVYWEIGHT_PLUS_MATTE
    // POLY
    // HP_POLYESTER_BACKLIT
    // LIGHTBOND
    // YELLOW_PAPER
    // GENERIC_SAV
    // HP_FOLDABLE_DOCUMENT_MATERIAL
    // GENERIC_NATURAL_TRACING
    // RECOVERED
    // PRODUCTION_SATIN_PHOTO_PAPER
    // PRODUCTION_GLOSS_PHOTO_PAPER
    // PLAIN_PAPER_50PCT_INK_DENSITY
    // PLAIN_PAPER_60PCT_INK_DENSITY
    // PLAIN_PAPER_70PCT_INK_DENSITY
    // PLAIN_PAPER_80PCT_INK_DENSITY
    // PLAIN_PAPER_90PCT_INK_DENSITY
    // PLAIN_PAPER_100PCT_INK_DENSITY
    // PRODUCTION_GLOSS_PHOTO_PAPER_UNATTENDED
    // PRODUCTION_SATIN_PHOTO_PAPER_UNATTENDED
    // SUPER_HEAVY_COATED_UNATTENDED
    // HP_OPAQUE_SCRIM_BANNER
    // REMOVABLE_ADHESIVE_FABRIC
    // HP_RECYCLED_REMOVABLE_ADHESIVE_FABRIC
    // PRODUCTION_MATTE_CANVAS
    // HP_OPAQUE_SCRIM_BANNER_UNATTENDED
    // YB_STATIONARY
    // YB_HEAVY_COATED
    // YB_COATED
    // YB_PHOTO_GLOSS
    // YB_PHOTO_SATIN

    return MediaIdType::ANY;
}

dune::imaging::types::MediaSizeId PrintJoltToDuneConverter::mapStringToMediaSizeId(const std::string& value) {
    using dune::imaging::types::MediaSizeId;
    if (value == "any") return MediaSizeId::ANY;
    if (value == "na_letter_8.5x11in") return MediaSizeId::LETTER;
    if (value == "letter_or_legal") return MediaSizeId::MIXED_LETTER_LEGAL;
    if (value == "na_legal_8.5x14in") return MediaSizeId::LEGAL;
    if (value == "na_executive_7.25x10.5in") return MediaSizeId::US_EXECUTIVE;
    if (value == "na_invoice_5.5x8.5in") return MediaSizeId::STATEMENT;
    if (value == "na_ledger_11x17in") return MediaSizeId::LEDGER;
    if (value == "na_tabloid-extra_12x18in") return MediaSizeId::ARCH_B;
    if (value == "na_index-3x5_3x5in") return MediaSizeId::PHOTO3X5;
    if (value == "na_index-4x6_4x6in") return MediaSizeId::PHOTO4X6;
    if (value == "na_5x7_5x7in") return MediaSizeId::PHOTO5X7;
    if (value == "na_index-5x8_5x8in") return MediaSizeId::PHOTO5X8;
    if (value == "iso_a3_297x420mm") return MediaSizeId::A3;
    if (value == "iso_a4_210x297mm") return MediaSizeId::A4;
    if (value == "iso_a5_148x210mm") return MediaSizeId::A5;
    if (value == "iso_a6_105x148mm") return MediaSizeId::A6;
    if (value == "iso_ra3_305x430mm") return MediaSizeId::RA3;
    if (value == "iso_sra3_320x450mm") return MediaSizeId::SRA3;
    if (value == "iso_ra4_215x305mm") return MediaSizeId::RA4;
    if (value == "iso_sra4_225x320mm") return MediaSizeId::SRA4;
    if (value == "jis_b4_257x364mm") return MediaSizeId::JIS_B4;
    if (value == "jis_b5_182x257mm") return MediaSizeId::JIS_B5;
    if (value == "jis_b6_128x182mm") return MediaSizeId::JIS_B6;
    if (value == "iso_b6_125x176mm") return MediaSizeId::B6;
    if (value == "iso_indexcard_100x150mm") return MediaSizeId::MEDIA100X150;
    if (value == "iso_8k_270x390mm") return MediaSizeId::MEDIA8K_270X390;
    if (value == "iso_16k_195x270mm") return MediaSizeId::MEDIA16K_195X270;
    if (value == "iso_8k_260x368mm") return MediaSizeId::MEDIA8K_260x368;
    if (value == "iso_16k_184x260mm") return MediaSizeId::MEDIA16K_184X260;
    if (value == "prc_8k_273x394mm") return MediaSizeId::ROC8K;
    if (value == "prc_16k_197x273mm") return MediaSizeId::ROC16K;
    if (value == "jis_hagaki_100x148mm") return MediaSizeId::HAGAKI_POSTCARD;
    if (value == "jpn_oufuku_148x200mm") return MediaSizeId::HAGAKI_OUFUKU;
    if (value == "na_number-9_3.875x8.875in") return MediaSizeId::COM9ENVELOPE;
    if (value == "na_number-10_4.125x9.5in") return MediaSizeId::COM10ENVELOPE;
    if (value == "na_monarch_3.875x7.5in") return MediaSizeId::MONARCHENVELOPE;
    if (value == "iso_b5_176x250mm") return MediaSizeId::B5ENVELOPE;
    if (value == "iso_c5_162x229mm") return MediaSizeId::C5ENVELOPE;
    if (value == "iso_envelope_114x162mm") return MediaSizeId::C6ENVELOPE;
    if (value == "iso_dl_110x220mm") return MediaSizeId::DLENVELOPE;
    if (value == "na_longscansize_8.5x34in") return MediaSizeId::LONG_SCAN;
    if (value == "custom") return MediaSizeId::CUSTOM;
    if (value == "any_custom") return MediaSizeId::ANYCUSTOM;
    if (value == "na_foolscap_8.5x13in") return MediaSizeId::FOOLSCAP;
    if (value == "na_arch-b_12x18in") return MediaSizeId::ARCH_B;
    if (value == "na_legal_216x340mm") return MediaSizeId::OFICIO_216X340;
    if (value == "letter_or_ledger") return MediaSizeId::MIXED_LETTER_LEDGER;
    if (value == "a4_or_a3") return MediaSizeId::MIXED_A4_A3;
    if (value == "om_photo_89x127mm") return MediaSizeId::PHOTO_L;
    if (value == "jpn_chou3_120x235mm") return MediaSizeId::CHOU3_ENVELOPE;
    if (value == "jpn_chou4_90x205mm") return MediaSizeId::CHOU4_ENVELOPE;

    // The following MediaSizeId options from MediaSizeId.fbs do not have a corresponding value in xmlvalues:
    //if (value == "na_letter-rot_8.5x11in") return MediaSizeId::LETTER; // No rotated variant in .fbs, map to LETTER
    //if (value == "na_eightpointfivebythirteen_8.5x13in") return MediaSizeId::FOOLSCAP;
    //if (value == "iso_a4-rot_210x297mm") return MediaSizeId::A4; // No rotated variant in .fbs, map to A4
    //if (value == "iso_a5-rot_148x210mm") return MediaSizeId::A5; // No rotated variant in .fbs, map to A5
    //if (value == "jis_b5-rot_182x257mm") return MediaSizeId::JIS_B5; // No rotated variant in .fbs, map to JIS_B5
    //if (value == "businessCard_2.16x3.58in") return MediaSizeId::UNDEFINED; // No direct mapping
    // if (value == "unknown") return MediaSizeId::UNDEFINED;
    // if (value == "unknownenvelope") return MediaSizeId::UNDEFINED;
    // if (value == "multiple_length") return MediaSizeId::UNDEFINED; // No direct mapping
    
    // The following MediaSizeId options from MediaSizeId.fbs do not have a corresponding value in xmlvalues:
    // A0, A1, A2, B1, B2, B3, C0, C1, C2, C3, C4, GOVT_LETTER, EDP, PHOTO5X5, PHOTO_L, JIS_B1, JIS_B2, JIS_B3,
    // PERSONAL_ENVELOPE, A2ENVELOPE, PHOTO_2L, F_SIZE, JIS_B0, ISO_B0, PHOTO_10x12IN, PHOTO_10X15IN, PHOTO_12X16IN,
    // PHOTO_14X17IN, PHOTO_14X18IN, PHOTO_16X20IN, PHOTO_18X22IN, PHOTO_20X24IN, PHOTO_22X28IN, PHOTO_24X30IN,
    // PHOTO_30X40CM, PHOTO_30X45CM, PHOTO_35X46CM, PHOTO_40X60CM, PHOTO_50X76CM, PHOTO_60X90CM, SUPER_B, C_SIZE,
    // D_SIZE, E_SIZE, ARCH_A, ARCH_C, ARCH_D, ARCH_E, ARCH_E1, ARCH_E2, ARCH_E3

    return MediaSizeId::ANY;
}

dune::cdm::glossary_1::PlexMode PrintJoltToDuneConverter::mapStringToPlexMode(const std::string& copySides)
{
    if (copySides == "simplexToSimplex" || copySides == "duplexToSimplex") 
    {
        CHECKPOINTA("PrintJoltToDuneConverter: convertStringToPlex: CopySides is simplex, returning simplex mode");
        return dune::cdm::glossary_1::PlexMode::simplex;
    } else if (copySides == "simplexToDuplex" || 
               copySides == "duplexToDuplex") {
        CHECKPOINTA("PrintJoltToDuneConverter: convertStringToPlex: CopySides is duplex, returning duplex mode");                
        return dune::cdm::glossary_1::PlexMode::duplex;
    } else {
        CHECKPOINTB_STR("PrintJoltToDuneConverter: Unknown CopySides value %s, defaulting to simplex", copySides.c_str());
        return dune::cdm::glossary_1::PlexMode::simplex;
    }
}

CustomMediaDimensionUnit PrintJoltToDuneConverter::convertMediaSizeUnit(dune::framework::utils::XmlUtils& xml, const std::string& xPath)
{
    auto customMediaDimensionUnit = CustomMediaDimensionUnit::MM;
    if (xml.isKeyAvailable(xPath))
    {
        CHECKPOINTB_STR("PrintJoltToDuneConverter::Key available in XML: %s", xPath.c_str());
        std::string xmlValue = xml[xPath].front();
        customMediaDimensionUnit = (xmlValue == "millimeters") ? CustomMediaDimensionUnit::MM : CustomMediaDimensionUnit::INCHES;
    }
    return customMediaDimensionUnit;
}

static constexpr float MM_PER_INCH = 25.4;

double mmToDpi(double val, double resolution = 10000)
{
    return val * resolution / MM_PER_INCH;
}

double inchToDpi(double val, double resolution = 10000)
{
    return val * resolution;
}

dune::framework::core::APIResult PrintJoltToDuneConverter::readXml(dune::framework::utils::XmlUtils& xml, const dune::framework::data::conversion::DataDescriptor& fileDescriptor,
            std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& jobTicketTable)
{
    CHECKPOINTB("PrintJoltToDuneConverter: ReadXml: Processing file %s with xpath %s", fileDescriptor.fileName_.c_str(),
                fileDescriptor.dataNodePath_.c_str());
    if (!xml.load(fileDescriptor.fileName_, fileDescriptor.dataNodePath_))
    {
        return dune::framework::core::APIResult::ERROR;
    }
    return dune::framework::core::APIResult::OK;
}

dune::framework::core::APIResult PrintJoltToDuneConverter::performConversion(dune::framework::utils::XmlUtils& xml,
            dune::cdm::jobTicket_1::PrintTable* printOptions)
{
    CHECKPOINTA("PrintJoltToDuneConverter: PerformConversion: Converting XML to PrintTable");

    // Convert the XML data to the PrintTable structure
    convertXml(xml, "/dd:DefaultPrintCopies", printOptions->copies, [](const std::string& v) { return std::stoi(v); });
    // convertXml(xml, "/dd:ChromaticMode", dest.printOptions->colorMode, mapStringToChromaticMode);
    convertXml(xml, "/dd:SheetCollate", printOptions->collate,
               [](const std::string& v) { return dune::job::cdm::mapToCdm(mapStringToSheetCollate(v)); });
    // convertXml(xml, "/dd:CopyOriginalOutputBindings", dest.printOptions->duplexBinding,
    // mapStringToCopyOriginalOutputBinding);
    convertXml(xml, "/dd:MediaInputID", printOptions->mediaSource,
               [](const std::string& v) { return dune::job::cdm::mapToCdm(mapStringToMediaInputId(v)); });
    convertXml(xml, "/dd:MediaOutputID", printOptions->mediaDestination,
               [](const std::string& v) { return dune::job::cdm::mapToCdm(mapStringToMediaOutputId(v)); });
    convertXml(xml, "/finishing:Staple", printOptions->stapleOption,
               [](const std::string& v) { return dune::job::cdm::mapToCdm(mapStringToStaple(v)); });
    convertXml(xml, "/copy:PunchingOption", printOptions->punchOption,
               [](const std::string& v) { return dune::job::cdm::mapToCdm(mapStringToPunchingOptions(v)); });
    convertXml(xml, "/copy:BookletMarkerOption", printOptions->bookletMakerOption,
               [](const std::string& v) { return dune::job::cdm::mapToCdm(mapStringToBookletMaker(v)); });
    convertXml(xml, "/dd:PrintQuality", printOptions->printQuality,
               [](const std::string& v) { return dune::job::cdm::mapToCdm(mapStringToPrintQuality(v)); });
    convertXml(xml, "/copy:FoldingProcessingOption", printOptions->foldOption,
               [](const std::string& v) { return dune::job::cdm::mapToCdm(mapStringToFolding(v)); });
    // convertXml(xml, "/dd:SheetsPerFold", printOptions->sheetsPerFoldSet, [](const std::string& v) { return
    // std::stoi(v); });
    convertXml(xml, "/copy:PaperSelection/dd:MediaTypeID", printOptions->mediaType,
               [](const std::string& v) { 
                auto mediaId = mapStringToMediaTypeId(v);    
                CHECKPOINTA("PrintJoltToDuneConverter: Convert: MediaTypeID is %d", (int)mediaId);
                return dune::job::cdm::mapToCdm(mediaId);             
            
            });
    convertXml(xml, "/copy:PaperSelection/copy:MediaSizeSettings/dd:MediaSizeID", printOptions->mediaSize,
               [](const std::string& v) {
                auto mediaSizeId = mapStringToMediaSizeId(v);
                CHECKPOINTA("PrintJoltToDuneConverter: Convert: MediaSizeID is %d", (int)mediaSizeId);
                return dune::job::cdm::mapToCdm(mediaSizeId); });

    auto customMediaDimensionUnit =
        convertMediaSizeUnit(xml, "/copy:PaperSelection/copy:MediaSizeSettings/dd:CustomMediaSizeSettings/dd:Unit");

    auto mapToDpi = [unit = customMediaDimensionUnit](const std::string& v) {
        double val = std::stod(v);
        CHECKPOINTC("PrintJoltToDuneConverter: convertMediaSizeUnit: value in units =%lf ", val);
        switch (unit)
        {
            case CustomMediaDimensionUnit::MM:
                val = mmToDpi(val);
                break;
            case CustomMediaDimensionUnit::INCHES:
                val = inchToDpi(val);
                break;
            default:
                CHECKPOINTC("PrintJoltToDuneConverter: convertMediaSizeUnit: Unknown unit %d, defaulting to mm", static_cast<int>(unit));
                val = mmToDpi(val);
                break;
        }
        CHECKPOINTC("PrintJoltToDuneConverter: convertMediaSizeUnit: val in dpi =%lf ", val);
        return val;
    };
    convertXml(xml, "/copy:PaperSelection/copy:MediaSizeSettings/copy:CustomMediaSizeSettings/dd:Length",
               printOptions->customMediaYFeedDimension, mapToDpi);
    convertXml(xml, "/copy:PaperSelection/copy:MediaSizeSettings/copy:CustomMediaSizeSettings/dd:Width",
               printOptions->customMediaXFeedDimension, mapToDpi);

    convertXml(xml, "/dd:CopySides", printOptions->plexMode,
               [](const std::string& v) { return (mapStringToPlexMode(v)); });
    

    // Additional conversion logic can be added here as needed

    return dune::framework::core::APIResult::OK;
}

dune::framework::core::APIResult PrintJoltToDuneConverter::convert(const dune::framework::data::conversion::DataDescriptor& fileDescriptor,
            std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& jobTicketTable)
{
    CHECKPOINTB("PrintJoltToDuneConverter: Convert: Processing file %s with xpath %s", fileDescriptor.fileName_.c_str(),
                fileDescriptor.dataNodePath_.c_str());

    dune::framework::utils::XmlUtils xml;
    
    dune::framework::core::APIResult result = readXml(xml, fileDescriptor, jobTicketTable);
    if (result != dune::framework::core::APIResult::OK)
    {
        CHECKPOINTA("PrintJoltToDuneConverter: Convert: Failed to read XML");
        return result;
    }
    if (jobTicketTable == nullptr)
    {
        CHECKPOINTA("PrintJoltToDuneConverter: Convert: jobTicketTable is null");
        return dune::framework::core::APIResult::ERROR;
    }

    if (!jobTicketTable->dest.get()) jobTicketTable->dest = dune::cdm::jobTicket_1::jobTicket::DestTable();

    if (!jobTicketTable->dest.getMutable()->print.get())
    {
        jobTicketTable->dest.getMutable()->print = dune::cdm::jobTicket_1::PrintTable();
        jobTicketTable->dest.getMutable()->print.getMutable()->beginMergePatch();
    }

    auto printOptions = jobTicketTable->dest.getMutable()->print.getMutable();

    result = performConversion(xml, printOptions);
    // Convert print settings with correct mappers
    CHECKPOINTC("PrintJoltToDuneConverter: Convert: Conversion successful");
    return dune::framework::core::APIResult::OK;
}

}}}}  // namespace dune::print::Jobs::Print