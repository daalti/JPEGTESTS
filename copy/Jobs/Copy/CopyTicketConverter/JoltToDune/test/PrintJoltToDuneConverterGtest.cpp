#include <gtest/gtest.h>
#include <fstream>
#include <cstdio>
#include <chrono>
#include <iomanip>
#include <sstream>
#include "PrintJoltToDuneConverter.h"

using namespace dune::copy::Jobs::Copy;

// Helper to create a sample XML file
void createSampleXml(const std::string& filename, const std::string& settingsXml) {
    std::ofstream file(filename);
    file << R"(<?xml version="1.0" encoding="UTF-8"?>)"
         << "<copy:CopyService "
         << "xmlns:finishing=\"http://www.hp.com/schemas/imaging/con/finishing/2009/01/08\" "
         << "xmlns:dd=\"http://www.hp.com/schemas/imaging/con/dictionaries/1.0/\" "
         << "xmlns:dsd=\"http://www.hp.com/schemas/imaging/con/digitalsending/2009/02/11\" "
         << "xmlns:copy=\"http://www.hp.com/schemas/imaging/con/service/copy/2009/08/14\">"
         << "<copy:DefaultJob>"
         << "<copy:CopySettings>"
         << settingsXml
         << "</copy:CopySettings>"
         << "</copy:DefaultJob>"
         << "</copy:CopyService>";
    file.close();
}

//Gtests for all mapper functions
class PrintJoltToDuneConverterMapperTest : public ::testing::Test {};


// --- SheetCollate ---
TEST_F(PrintJoltToDuneConverterMapperTest, SheetCollate_AllValues) {
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToSheetCollate("Collated"), dune::copy::SheetCollate::Collate);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToSheetCollate("Uncollated"), dune::copy::SheetCollate::Uncollate);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToSheetCollate("invalid"), dune::copy::SheetCollate::Collate); // default
}

// --- MediaInputID ---
TEST_F(PrintJoltToDuneConverterMapperTest, MediaInputId_AllValues) {
    using MS = dune::imaging::types::MediaSource;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("ADF"), MS::ADF);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("EnvFeed"), MS::ENVFEED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Flatbed"), MS::FLATBED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray1"), MS::TRAY1);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray2"), MS::TRAY2);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray3"), MS::TRAY3);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray4"), MS::TRAY4);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray5"), MS::TRAY5);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray6"), MS::TRAY6);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray7"), MS::TRAY7);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray8"), MS::TRAY8);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray9"), MS::TRAY9);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray10"), MS::TRAY10);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray11"), MS::TRAY11);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray12"), MS::TRAY12);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Tray13"), MS::TRAY13);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Roll1"), MS::ROLL1);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Roll2"), MS::ROLL2);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Roll3"), MS::ROLL3);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("Roll4"), MS::ROLL4);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("ManualFeed"), MS::MANUALFEED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("RearManualFeed"), MS::REAR);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("PhotoTray"), MS::PHOTO);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("MultiPurpose_Tray"), MS::TRAY1);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaInputId("invalid"), MS::AUTOSELECT); // default
}

// --- MediaOutputID ---
TEST_F(PrintJoltToDuneConverterMapperTest, MediaOutputId_AllValues) {
    using MO = dune::imaging::types::MediaDestinationId;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("OutputBin1"), MO::OUTPUTBIN1);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("OutputBin2"), MO::OUTPUTBIN2);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("OutputBin3"), MO::OUTPUTBIN3);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("OutputBin4"), MO::OUTPUTBIN4);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("OutputBin5"), MO::OUTPUTBIN5);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("OutputBin6"), MO::OUTPUTBIN6);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("OutputBin7"), MO::OUTPUTBIN7);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("OutputBin8"), MO::OUTPUTBIN8);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("Stacker"), MO::STACKER);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("Stacker-Staples"), MO::STACKER2);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("StackerFaceUp"), MO::STACKER3);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("StackerFaceDown"), MO::STACKER4);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("Accessory"), MO::GENERIC_ACCESSORY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("Alternate"), MO::ALTERNATE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("Standard"), MO::STANDARDBIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("PrinterSelect"), MO::AUTOSELECT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaOutputId("invalid"), MO::DEFAULT); // default
}

// --- StapleOptions ---
TEST_F(PrintJoltToDuneConverterMapperTest, Staple_AllValues) {
    using SO = dune::imaging::types::StapleOptions;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("none"), SO::NONE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("default"), SO::DEFAULT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topAnyOnePointAny"), SO::TOP_ANY_ONE_POINT_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topAnyOnePointAngled"), SO::TOP_ANY_ONE_POINT_ANGLED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topLeftOnePointAny"), SO::TOP_LEFT_ONE_POINT_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topLeftOnePointAngled"), SO::TOP_LEFT_ONE_POINT_ANGLED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topLeftOnePointHorizontal"), SO::TOP_LEFT_ONE_POINT_HORIZONTAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topLeftOnePointVertical"), SO::TOP_LEFT_ONE_POINT_VERTICAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topRightOnePointAny"), SO::TOP_RIGHT_ONE_POINT_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topRightOnePointAngled"), SO::TOP_RIGHT_ONE_POINT_ANGLED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topRightOnePointHorizontal"), SO::TOP_RIGHT_ONE_POINT_HORIZONTAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topRightOnePointVertical"), SO::TOP_RIGHT_ONE_POINT_VERTICAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomLeftOnePointAny"), SO::BOTTOM_LEFT_ONE_POINT_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomLeftOnePointAngled"), SO::BOTTOM_LEFT_ONE_POINT_ANGLED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomLeftOnePointHorizontal"), SO::BOTTOM_LEFT_ONE_POINT_HORIZONTAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomLeftOnePointVertical"), SO::BOTTOM_LEFT_ONE_POINT_VERTICAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomRightOnePointAny"), SO::BOTTOM_RIGHT_ONE_POINT_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomRightOnePointAngled"), SO::BOTTOM_RIGHT_ONE_POINT_ANGLED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomRightOnePointHorizontal"), SO::BOTTOM_RIGHT_ONE_POINT_HORIZONTAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomRightOnePointVertical"), SO::BOTTOM_RIGHT_ONE_POINT_VERTICAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("centerOnePoint"), SO::CENTER_POINT_POINT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("leftTwoPoints"), SO::LEFT_TWO_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("leftTwoPointsAny"), SO::LEFT_TWO_POINTS_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("rightTwoPoints"), SO::RIGHT_TWO_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topTwoPoints"), SO::TOP_TWO_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomTwoPoints"), SO::BOTTOM_TWO_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("centerTwoPoints"), SO::CENTER_TWO_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("leftThreePoints"), SO::LEFT_THREE_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("leftThreePointsAny"), SO::LEFT_THREE_POINTS_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("rightThreePoints"), SO::RIGHT_THREE_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topThreePoints"), SO::TOP_THREE_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomThreePoints"), SO::BOTTOM_THREE_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("centerThreePoints"), SO::CENTER_THREE_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("leftSixPoints"), SO::LEFT_SIX_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("leftSixPointsAny"), SO::LEFT_SIX_POINTS_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("rightSixPoints"), SO::RIGHT_SIX_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("topSixPoints"), SO::TOP_SIX_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("bottomSixPoints"), SO::BOTTOM_SIX_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("centerSixPoints"), SO::CENTER_SIX_POINTS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToStaple("invalid"), SO::NONE); // default
}

// --- PunchingOptions ---
TEST_F(PrintJoltToDuneConverterMapperTest, PunchingOptions_AllValues) {
    using PO = dune::imaging::types::PunchingOptions;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("none"), PO::NONE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("default"), PO::DEFAULT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("twoPointAny"), PO::TWO_POINT_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("leftTwoPointDin"), PO::LEFT_TWO_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("rightTwoPointDin"), PO::RIGHT_TWO_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("topTwoPointDin"), PO::TOP_TWO_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("bottomTwoPointDin"), PO::BOTTOM_TWO_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("twoPointDin"), PO::TWO_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("leftTwoPointUs"), PO::LEFT_TWO_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("rightTwoPointUs"), PO::RIGHT_TWO_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("topTwoPointUs"), PO::TOP_TWO_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("bottomTwoPointUs"), PO::BOTTOM_TWO_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("twoPointUs"), PO::TWO_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("leftThreePointUs"), PO::LEFT_THREE_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("rightThreePointUs"), PO::RIGHT_THREE_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("topThreePointUs"), PO::TOP_THREE_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("bottomThreePointUs"), PO::BOTTOM_THREE_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("threePointUs"), PO::THREE_POINT_US);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("threePointAny"), PO::THREE_POINT_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("leftFourPointDin"), PO::LEFT_FOUR_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("rightFourPointDin"), PO::RIGHT_FOUR_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("topFourPointDin"), PO::TOP_FOUR_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("bottomFourPointDin"), PO::BOTTOM_FOUR_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("fourPointDin"), PO::FOUR_POINT_DIN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("leftFourPointSwd"), PO::LEFT_FOUR_POINT_SWD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("rightFourPointSwd"), PO::RIGHT_FOUR_POINT_SWD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("topFourPointSwd"), PO::TOP_FOUR_POINT_SWD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("bottomFourPointSwd"), PO::BOTTOM_FOUR_POINT_SWD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("fourPointSwd"), PO::FOUR_POINT_SWD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("fourPointAny"), PO::FOUR_POINT_ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("leftTwoPoint"), PO::LEFT_TWO_POINT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("rightTwoPoint"), PO::RIGHT_TWO_POINT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("topTwoPoint"), PO::TOP_TWO_POINT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("bottomTwoPoint"), PO::BOTTOM_TWO_POINT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("jediUnknown"), PO::NONE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPunchingOptions("invalid"), PO::NONE); // default
}

// --- BookletMaker ---
TEST_F(PrintJoltToDuneConverterMapperTest, BookletMaker_AllValues) {
    using BM = dune::imaging::types::BookletMakingOptions;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToBookletMaker("None"), BM::NONE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToBookletMaker("BookletMaker"), BM::BOOKLET_MAKER);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToBookletMaker("jediUnknown"), BM::NONE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToBookletMaker("invalid"), BM::NONE); // default
}

// --- PrintQuality ---
TEST_F(PrintJoltToDuneConverterMapperTest, PrintQuality_AllValues) {
    using PQ = dune::imaging::types::PrintQuality;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Draft"), PQ::DRAFT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("High"), PQ::UNDEFINED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Normal"), PQ::NORMAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Best"), PQ::BEST);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Custom"), PQ::UNDEFINED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Default"), PQ::UNDEFINED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("FastNormal"), PQ::FAST_NORMAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Fast"), PQ::UNDEFINED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Good"), PQ::UNDEFINED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Marvelous"), PQ::MARVELOUS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("SuperDraft"), PQ::UNDEFINED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Any"), PQ::UNDEFINED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Economode"), PQ::ECONOMODE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("Depleted"), PQ::DEPLETED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPrintQuality("invalid"), PQ::UNDEFINED); // default
}

// --- FoldingOptions ---
TEST_F(PrintJoltToDuneConverterMapperTest, Folding_AllValues) {
    using FO = dune::imaging::types::FoldingOptions;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("none"), FO::NONE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("default"), FO::DEFAULT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("cInwardTop"), FO::C_INWARD_TOP);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("cInwardBottom"), FO::C_INWARD_BOTTOM);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("cOutwardTop"), FO::C_OUTWARD_TOP);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("cOutwardBottom"), FO::C_OUTWARD_BOTTOM);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("vInwardTop"), FO::V_INWARD_TOP);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("vInwardBottom"), FO::V_INWARD_BOTTOM);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("vOutwardTop"), FO::V_OUTWARD_TOP);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("vOutwardBottom"), FO::V_OUTWARD_BOTTOM);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToFolding("invalid"), FO::NONE); // default
}

// --- MediaTypeID ---
TEST_F(PrintJoltToDuneConverterMapperTest, MediaTypeId_AllValues) {
    using MT = dune::imaging::types::MediaIdType;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("anySupportedType"), MT::ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("plain"), MT::STATIONERY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPMatte90gsm"), MT::HPMATTE90G);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPMatte105gsm"), MT::HPMATTE105G);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPMatte120gsm"), MT::HPMATTE120G);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPPremiumPresentationMatte"), MT::HP_MATTE_PRESENTATION);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPMatteBrochureAndFlyer"), MT::HPBROCHURE_MATTE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPMatteCover200gsm"), MT::HPGLOSSY200G);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPMatte200gsm"), MT::HPMATTE200G);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPSoftGloss120gsm"), MT::HPSOFTGLOSS120G);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPGlossy220gsm"), MT::HPGLOSSY200G);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("light"), MT::LIGHT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("intermediate"), MT::INTERMEDIATE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("midweight"), MT::MIDWEIGHT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("heavy"), MT::HEAVY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("extraHeavy"), MT::EXTRAHEAVY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("cardstock"), MT::CARDSTOCK);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("matte"), MT::HP_MATTE_FILM);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("matteBrochure"), MT::HPMATTE_BROCHURE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("midweightGlossy"), MT::MIDWEIGHTGLOSSY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("heavyGlossy"), MT::HEAVYGLOSSY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("extraHeavyGloss"), MT::EXTRAHEAVYGLOSSY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("cardstockGlossy"), MT::CARDGLOSSY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("transparency"), MT::TRANSPARENCY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("labels"), MT::LABELS);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("stationery-letterhead"), MT::LETTERHEAD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("envelope"), MT::ENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("heavyEnvelope"), MT::HEAVYENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("stationery-preprinted"), MT::PREPRINTED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("stationery-prepunched"), MT::PREPUNCHED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("color"), MT::COLORED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("bond"), MT::BOND);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("recycled"), MT::RECYCLED);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("rough"), MT::ROUGH);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("heavyRough"), MT::HEAVYROUGH);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("filmOpaque"), MT::OPAQUEFILM);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined1"), MT::USER_DEFINED_1);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined2"), MT::USER_DEFINED_2);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined3"), MT::USER_DEFINED_3);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined4"), MT::USER_DEFINED_4);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined5"), MT::USER_DEFINED_5);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined6"), MT::USER_DEFINED_6);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined7"), MT::USER_DEFINED_7);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined8"), MT::USER_DEFINED_8);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined9"), MT::USER_DEFINED_9);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("userDefined10"), MT::USER_DEFINED_10);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("other"), MT::OTHERMATTE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("auto"), MT::ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPEcoSMARTLite"), MT::HPECOFFICIENT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPBrochureMatte"), MT::HPBROCHURE_MATTE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPBrochureGlossy"), MT::HPBROCHURE_GLOSSY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("HPAdvancedPhoto"), MT::HPPHOTO);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("lightBond"), MT::LIGHTBOND);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("lightPaperboard"), MT::LIGHTPAPERBOARD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("paperboard"), MT::PAPERBOARD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("heavyPaperboard"), MT::HEAVYPAPERBOARD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaTypeId("invalid"), MT::ANY); // default
}

TEST_F(PrintJoltToDuneConverterMapperTest, PlexMode_AllValues) 
{
    using PM = dune::cdm::glossary_1::PlexMode;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPlexMode("simplexToSimplex"), PM::simplex);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPlexMode("duplexToSimplex"), PM::simplex);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPlexMode("simplexToDuplex"), PM::duplex);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPlexMode("duplexToDuplex"), PM::duplex);
    // unknown values default to simplex
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToPlexMode("invalidValue"), PM::simplex);
}

// --- MediaSizeID ---
TEST_F(PrintJoltToDuneConverterMapperTest, MediaSizeId_AllValues) 
{
    using MS = dune::imaging::types::MediaSizeId;
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("any"), MS::ANY);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_letter_8.5x11in"), MS::LETTER);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("letter_or_legal"), MS::MIXED_LETTER_LEGAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_legal_8.5x14in"), MS::LEGAL);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_executive_7.25x10.5in"), MS::US_EXECUTIVE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_invoice_5.5x8.5in"), MS::STATEMENT);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_ledger_11x17in"), MS::LEDGER);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_tabloid-extra_12x18in"), MS::ARCH_B);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_index-3x5_3x5in"), MS::PHOTO3X5);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_index-4x6_4x6in"), MS::PHOTO4X6);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_5x7_5x7in"), MS::PHOTO5X7);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_index-5x8_5x8in"), MS::PHOTO5X8);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_a3_297x420mm"), MS::A3);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_a4_210x297mm"), MS::A4);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_a5_148x210mm"), MS::A5);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_a6_105x148mm"), MS::A6);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_ra3_305x430mm"), MS::RA3);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_sra3_320x450mm"), MS::SRA3);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_ra4_215x305mm"), MS::RA4);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_sra4_225x320mm"), MS::SRA4);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("jis_b4_257x364mm"), MS::JIS_B4);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("jis_b5_182x257mm"), MS::JIS_B5);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("jis_b6_128x182mm"), MS::JIS_B6);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_b6_125x176mm"), MS::B6);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_indexcard_100x150mm"), MS::MEDIA100X150);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_8k_270x390mm"), MS::MEDIA8K_270X390);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_16k_195x270mm"), MS::MEDIA16K_195X270);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_8k_260x368mm"), MS::MEDIA8K_260x368);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_16k_184x260mm"), MS::MEDIA16K_184X260);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("prc_8k_273x394mm"), MS::ROC8K);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("prc_16k_197x273mm"), MS::ROC16K);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("jis_hagaki_100x148mm"), MS::HAGAKI_POSTCARD);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("jpn_oufuku_148x200mm"), MS::HAGAKI_OUFUKU);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_number-9_3.875x8.875in"), MS::COM9ENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_number-10_4.125x9.5in"), MS::COM10ENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_monarch_3.875x7.5in"), MS::MONARCHENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_b5_176x250mm"), MS::B5ENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_c5_162x229mm"), MS::C5ENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_envelope_114x162mm"), MS::C6ENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("iso_dl_110x220mm"), MS::DLENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_longscansize_8.5x34in"), MS::LONG_SCAN);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("custom"), MS::CUSTOM);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("any_custom"), MS::ANYCUSTOM);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_foolscap_8.5x13in"), MS::FOOLSCAP);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_arch-b_12x18in"), MS::ARCH_B);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("na_legal_216x340mm"), MS::OFICIO_216X340);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("letter_or_ledger"), MS::MIXED_LETTER_LEDGER);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("a4_or_a3"), MS::MIXED_A4_A3);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("om_photo_89x127mm"), MS::PHOTO_L);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("jpn_chou3_120x235mm"), MS::CHOU3_ENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("jpn_chou4_90x205mm"), MS::CHOU4_ENVELOPE);
    EXPECT_EQ(PrintJoltToDuneConverter::mapStringToMediaSizeId("invalid"), MS::ANY); // default
}

// Generates "prefix_YYYYMMDDHHMMSS.xml"
static std::string timestampedFileName(const std::string& prefix) {
    auto now = std::chrono::system_clock::now();
    auto t   = std::chrono::system_clock::to_time_t(now);
    std::tm tm;
    localtime_r(&t, &tm);
    std::ostringstream ss;
    ss << prefix << "_" << std::put_time(&tm, "%Y%m%d%H%M%S") << ".xml";
    return ss.str();
}

// 2. Gtest for full conversion with all properties set
class GivenAJoltConversionFile : public ::testing::Test {
protected:
    std::string xmlFile = "test_sample.xml";
    dune::framework::data::conversion::DataDescriptor fileDataDescriptor;
};



TEST_F(GivenAJoltConversionFile, WhenInValidXmlIsLoaded_ConversionFails) 
{
    PrintJoltToDuneConverter converter;
    dune::framework::utils::XmlUtils xml;
    fileDataDescriptor.fileName_     = "./nonexistent.xml";
    fileDataDescriptor.dataNodePath_ = "/any/path";
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketTable{std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>()};
    dune::framework::core::APIResult result = converter.readXml(xml, fileDataDescriptor, jobTicketTable);
    EXPECT_EQ(result, dune::framework::core::APIResult::ERROR);
}

TEST_F(GivenAJoltConversionFile, WhenValidXmlIsLoaded_ValuesAreConverted) 
{
    const std::string tmpFile = timestampedFileName("PrintJoltToDuneConverterTest");
    const std::string settingsXml = R"(
        <dd:DefaultPrintCopies>7</dd:DefaultPrintCopies>
        <dd:SheetCollate>Uncollated</dd:SheetCollate>
        <dd:MediaInputID>Flatbed</dd:MediaInputID>
        <dd:MediaOutputID>Accessory</dd:MediaOutputID>
        <dd:PrintQuality>Best</dd:PrintQuality>
        <copy:FoldingProcessingOption>cOutwardBottom</copy:FoldingProcessingOption>
        <dd:CopySides>simplexToDuplex</dd:CopySides>
    )";

    createSampleXml(tmpFile, settingsXml);

    fileDataDescriptor.fileName_     = tmpFile;
    fileDataDescriptor.dataNodePath_ = "copy:CopyService/copy:DefaultJob/copy:CopySettings";
    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();

    if (!jobTicketTable->dest.get()) {
        jobTicketTable->dest = dune::cdm::jobTicket_1::jobTicket::DestTable();
    }
    if (!jobTicketTable->dest.getMutable()->print.get()) {
        jobTicketTable->dest.getMutable()->print = dune::cdm::jobTicket_1::PrintTable();
        jobTicketTable->dest.getMutable()->print.getMutable()->beginMergePatch();
    }

    PrintJoltToDuneConverter converter;
    dune::framework::utils::XmlUtils xml;

    EXPECT_EQ(converter.readXml(xml, fileDataDescriptor, jobTicketTable),
              dune::framework::core::APIResult::OK);

    auto printTable = jobTicketTable->dest.getMutable()->print.getMutable();
    EXPECT_EQ(converter.performConversion(xml, printTable),
              dune::framework::core::APIResult::OK);

    EXPECT_EQ(printTable->copies.get(), 7);
    EXPECT_EQ(printTable->collate.get(),
              dune::job::cdm::mapToCdm(PrintJoltToDuneConverter::mapStringToSheetCollate("Uncollated")));
    EXPECT_EQ(printTable->mediaSource.get(),
              dune::job::cdm::mapToCdm(PrintJoltToDuneConverter::mapStringToMediaInputId("Flatbed")));
    EXPECT_EQ(printTable->mediaDestination.get(),
              dune::job::cdm::mapToCdm(PrintJoltToDuneConverter::mapStringToMediaOutputId("Accessory")));
    EXPECT_EQ(printTable->printQuality.get(),
              dune::job::cdm::mapToCdm(PrintJoltToDuneConverter::mapStringToPrintQuality("Best")));
    EXPECT_EQ(printTable->foldOption.get(),
              dune::job::cdm::mapToCdm(PrintJoltToDuneConverter::mapStringToFolding("cOutwardBottom")));
    EXPECT_EQ(printTable->plexMode.get(),
              dune::cdm::glossary_1::PlexMode::duplex);

    std::remove(tmpFile.c_str());
}

// // 3. Gtests for missing keys (loop over all keys)
TEST_F(GivenAJoltConversionFile, WhenSettingIsMissingCorrespondingSettingIsNotSet) {
    std::vector<std::string> keys = {
        "<dd:DefaultPrintCopies>5</dd:DefaultPrintCopies>",
        "<dd:SheetCollate>Collated</dd:SheetCollate>",
        "<dd:MediaInputID>ADF</dd:MediaInputID>",
        "<dd:MediaOutputID>OutputBin1</dd:MediaOutputID>",
        "<dd:Staple>none</dd:Staple>",
        "<dd:PunchingOption>none</dd:PunchingOption>",
        "<dd:BookletMarkerOption>None</dd:BookletMarkerOption>",
        "<dd:PrintQuality>Draft</dd:PrintQuality>",
        "<dd:FoldingProcessingOption>none</dd:FoldingProcessingOption>",
        "<copy:PaperSelection>"
        "<copy:MediaSizeSettings>"
        "<dd:MediaSizeID>any</dd:MediaSizeID>"
        "<copy:CustomMediaSizeSettings>"
        "<dd:Length>280</dd:Length>"
        "<dd:Width>215.9</dd:Width>"
        "<dd:Unit>millimeters</dd:Unit>"
        "</copy:CustomMediaSizeSettings>"
        "</copy:MediaSizeSettings>"
        "<dd:MediaTypeID>plain</dd:MediaTypeID>"
        "</copy:PaperSelection>"
    };

    for (size_t i = 0; i < keys.size(); ++i) {
        std::string settingsXml;
        std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketTable{std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>()};
        for (size_t j = 0; j < keys.size(); ++j) {
            if (i != j) settingsXml += keys[j];
        }
        createSampleXml(xmlFile, settingsXml);
        PrintJoltToDuneConverter converter;
        fileDataDescriptor.fileName_ = xmlFile;
        fileDataDescriptor.dataNodePath_ =  "copy:CopyService/copy:DefaultJob/copy:CopySettings";
        auto result = converter.convert(fileDataDescriptor, jobTicketTable);
        ASSERT_EQ(result, dune::framework::core::APIResult::OK);
        ASSERT_NE(jobTicketTable, nullptr);
        ASSERT_NE(jobTicketTable->dest.getMutable(), nullptr);
        ASSERT_NE(jobTicketTable->dest.getMutable()->print.getMutable(), nullptr);
        auto printTable = jobTicketTable->dest.getMutable()->print.getMutable();
        // Check that the omitted property is not set
        switch (i) {
            case 0: EXPECT_FALSE(printTable->copies.isSet()); break;
            case 1: EXPECT_FALSE(printTable->collate.isSet()); break;
            case 2: EXPECT_FALSE(printTable->mediaSource.isSet()); break;
            case 3: EXPECT_FALSE(printTable->mediaDestination.isSet()); break;
            case 4: EXPECT_FALSE(printTable->stapleOption.isSet()); break;
            case 5: EXPECT_FALSE(printTable->punchOption.isSet()); break;
            case 6: EXPECT_FALSE(printTable->bookletMakerOption.isSet()); break;
            case 7: EXPECT_FALSE(printTable->printQuality.isSet()); break;
            case 8: EXPECT_FALSE(printTable->foldOption.isSet()); break;
            case 9: {
                EXPECT_FALSE(printTable->mediaType.isSet()); break;
                EXPECT_FALSE(printTable->mediaSize.isSet()); break;
                EXPECT_FALSE(printTable->customMediaXFeedDimension.isSet());
                EXPECT_FALSE(printTable->customMediaYFeedDimension.isSet());
                break;
            }
        }
    }
    std::remove(xmlFile.c_str());
}