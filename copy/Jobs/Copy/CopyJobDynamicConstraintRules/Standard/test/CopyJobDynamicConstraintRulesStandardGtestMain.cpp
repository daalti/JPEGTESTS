/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesStandardGtestMain.cpp
 * @date   Mon, 11 Jul 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesStandard.h"
#include "ForceSets.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "TestSystemServices.h"
#include "GTestConfigHelper.h"
#include "CopyJobTicket.h"
#include "SecurityContexts.h"
#include "SecurityContextImpl.h"

#include <iostream>
#include <sstream>
#include "flatbuffers/flatbuffers.h"
#include "flatbuffers/idl.h"
#include "flatbuffers/util.h"
#include "flatbuffers/reflection.h"
#include "flatbuffers/minireflect.h"
#include "CopyJobConstraints_generated.h"
#include <iostream>
#include <sstream>
#include "MockSecurityContexts.h"
#include "MockICopyAdapter.h"
#include "MockIMedia.h"
#include "MockICopyJobTicket.h"
#include "MockIMediaConstraints.h"
#include "StringIds.h"
#include "MockICapabilities.h"
#include "MockIScanConstraints.h"
#include "MockIPageBasedFinisher.h"
#include "MockIFinisherCombination.h"
#include "MockIColorAccessControl.h"

using CopyJobDynamicConstraintRulesStandard              = dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard;
using ForceSets             = dune::copy::Jobs::Copy::ForceSets;
using FeatureEnabled        = dune::cdm::glossary_1::FeatureEnabled;
using TestSystemServices    = dune::framework::component::TestingUtil::TestSystemServices;
using IComponent            = dune::framework::component::IComponent;
using IComponentManager     = dune::framework::component::IComponentManager;
using SystemServices        = dune::framework::component::SystemServices;
using SysTrace              = dune::framework::core::dbg::SysTrace;
using CheckpointLevel       = SysTrace::CheckpointLevel;
using MockICopyAdapter      = dune::copy::cdm::MockICopyAdapter;
using MockIScanConstraints  = dune::scan::MockIScanConstraints;
using IMedia = dune::print::engine::IMedia;
using MockIMediaIInput = dune::print::engine::MockIMediaIInput;
using MockIMediaIInputTray = dune::print::engine::MockIMediaIInputTray;
using MockIScannerCapabilities = dune::scan::scanningsystem::MockIScannerCapabilities;
using MockIColorAccessControl = dune::imaging::MockIColorAccessControl;

using GTestConfigHelper     = dune::framework::core::gtest::GTestConfigHelper;
using namespace dune::copy::Jobs::Copy;
using namespace ::testing;


#include <sys/types.h>
#include <dirent.h>
#include <stdio.h>
#include <libgen.h>
#include <stdlib.h>
#include <string.h>


void listFiles(const char* theDir)
{
   DIR *dir;
   struct dirent *dp;
   //char* theDir = "./testResources";
    if((dir = opendir(theDir)) == NULL){
        fprintf (stderr, "Cannot open %s\n", theDir);
        return;
    }
    fprintf (stderr, "Listing:  %s\n", theDir);
    while ((dp = readdir(dir)) != NULL) {
        fprintf(stderr, "%s\n",(*dp).d_name);
    }
}

GTestConfigHelper testConfigOptions_;

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

int main(int argc, char  *argv[])
{
    // run google tests
    //
    std::cout << "Main:  " << argv[0] << std::endl;

    testConfigOptions_.parse(argc, argv);
    testConfigOptions_.Configure();

    ::testing::FLAGS_gmock_catch_leaked_mocks = true;
    ::testing::FLAGS_gmock_verbose = "error";

    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenANewCopyJobDynamicConstraintRulesStandard : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenANewCopyJobDynamicConstraintRulesStandard : public ::testing::Test
{
  public:

    GivenANewCopyJobDynamicConstraintRulesStandard() : component_(nullptr), systemServices_(nullptr), componentManager_(nullptr) {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    std::shared_ptr<Constraints> createConstraintRange(double uniqueMinValueExpected, double uniqueMaxValueExpected, double uniqueStepValueExpected);

  protected:

    dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard                          * component_;
    TestSystemServices                              * systemServices_;
    dune::framework::component::IComponentManager   * componentManager_;
    dune::scan::MockIScanConstraints                * scanConstraints_{nullptr};
    std::string                                       productTestFileName{"./testResources/CopyJobDynamicConstraintRulesEnterprise.json"};    

};

void GivenANewCopyJobDynamicConstraintRulesStandard::SetUp()
{
    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesStandardTest.fbs", productTestFileName.c_str());

    component_ = new CopyJobDynamicConstraintRulesStandard("myInstance");
    ASSERT_TRUE(component_ != nullptr);
}

void GivenANewCopyJobDynamicConstraintRulesStandard::TearDown()
{
    delete component_;
    delete systemServices_;
}

std::shared_ptr<Constraints> GivenANewCopyJobDynamicConstraintRulesStandard::createConstraintRange(double uniqueMinValueExpected, double uniqueMaxValueExpected, double uniqueStepValueExpected)
{
    auto constraints = std::make_shared<Constraints>();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeDouble>(uniqueMinValueExpected, uniqueMaxValueExpected, uniqueStepValueExpected, string_id::cCheckInvalidEntries);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_);

    ASSERT_TRUE(true);
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, JustCreateACopyJob)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, TestConstraintsLoad)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
    "              { "
    "                \"plexMode\": [ "
    "                    \"SIMPLEX\", "
    "                    \"DUPLEX\" "
    "                ], "
    "                \"plexBinding\": [ "
    "                    \"ONE_SIDED\", "
    "                    \"LONG_EDGE\", "
    "                    \"SHORT_EDGE\" "
    "                ], "
    "                \"collate\": [ "
    "                    \"Collate\", "
    "                    \"Uncollate\" "
    "                ], "
    "                \"minCopies\": 1, "
    "                \"maxCopies\": 999, "
    "                \"stepCopies\": 1.0, "
    "                \"printQuality\": [ "
    "                    \"DRAFT\", "
    "                    \"NORMAL\", "
    "                    \"BEST\" "
    "                ], "
    "					\"scanJobConstraint\": {  "
    "                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
    "                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
    "                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
    "                        \"scanPagesFlipUpEnabled\": [ false, true ], "
    "                        \"minScanExposure\": 1, "
    "                        \"maxScanExposure\": 9, "
    "                        \"stepScanExposure\": 1.0, "
    "                        \"minScalePercent\": 25, "
    "                        \"maxScalePercent\": 400, "
    "                        \"step\":1.0, "
    "                      }"
    "              } "
    ;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenMediaSupportsDuplex_ThenDuplexIsAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						{ \"size\":{ \"id\":\"PHOTO5X8\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                        } "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"                        \"bookletFormat\":[ \"Off\", \"LeftEdge\"], "
"						 \"adfOriginalSizes\":[ "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"US_EXECUTIVE\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"FOOLSCAP\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"						], "
"						\"flatbedOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"US_EXECUTIVE\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"PHOTO4X6\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"PHOTO5X8\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"						] "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    // ********** Test Case 1 (both size and type are duplex-able) *******
    std::cerr << "Testing  STATIONERY,  LETTER \n";
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    std::shared_ptr<Constraints> plexConstraints =  dynamicConstraintRules->getPlexModeConstraints(ticket);
    std::vector<IConstraint*> thePlexConstraints = plexConstraints->getConstraints();
    IConstraint* validPlexModes = thePlexConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::PlexMode>* theDude = static_cast<ValidValuesEnum<dune::cdm::glossary_1::PlexMode>*>(validPlexModes);
    std::cerr << "theDude->getValidValues().size(): " << theDude->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)theDude->getValidValues().size());
    // ********************************************************

    // ********** Test Case 2 (type is not duplex-able) *******
    std::cerr << "Testing  TRANSPARENCY,  LETTER \n";
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::TRANSPARENCY);

    // now get the constraints ...
    plexConstraints =  dynamicConstraintRules->getPlexModeConstraints(ticket);
    thePlexConstraints = plexConstraints->getConstraints();
    validPlexModes = thePlexConstraints[1];

    theDude = static_cast<ValidValuesEnum<dune::cdm::glossary_1::PlexMode>*>(validPlexModes);
    std::cerr << "theDude->getValidValues().size(): " << theDude->getValidValues().size() << "\n";
    EXPECT_EQ(1, (int)theDude->getValidValues().size());
    // ********************************************************

    // ********** Test Case 3 (size is not duplex-able) *******
    std::cerr << "Testing  STATIONARY,  PHOTO5X8 \n";
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::PHOTO5X8);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    plexConstraints =  dynamicConstraintRules->getPlexModeConstraints(ticket);
    thePlexConstraints = plexConstraints->getConstraints();
    validPlexModes = thePlexConstraints[1];

    theDude = static_cast<ValidValuesEnum<dune::cdm::glossary_1::PlexMode>*>(validPlexModes);
    std::cerr << "theDude->getValidValues().size(): " << theDude->getValidValues().size() << "\n";
    EXPECT_EQ(1, (int)theDude->getValidValues().size());
    // ********************************************************

    // ********** Test Case 4  (both are duplex-able) (ensure the first test case passes again) *******
    std::cerr << "Testing  STATIONARY,  LETTER  again\n";
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    plexConstraints =  dynamicConstraintRules->getPlexModeConstraints(ticket);
    thePlexConstraints = plexConstraints->getConstraints();
    validPlexModes = thePlexConstraints[1];

    theDude = static_cast<ValidValuesEnum<dune::cdm::glossary_1::PlexMode>*>(validPlexModes);
    std::cerr << "theDude->getValidValues().size(): " << theDude->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)theDude->getValidValues().size());
    // ********************************************************

    // ********** Test Case 5  (booklet format on are simplex-able) (ensure the first test case passes again) *******
    std::cerr << "Testing  booklet format on \n";
    ticket->getIntent()->setBookletFormat(dune::imaging::types::BookletFormat::LeftEdge);

    // now get the constraints ...
    plexConstraints =  dynamicConstraintRules->getPlexModeConstraints(ticket);
    thePlexConstraints = plexConstraints->getConstraints();
    validPlexModes = thePlexConstraints[1];

    theDude = static_cast<ValidValuesEnum<dune::cdm::glossary_1::PlexMode>*>(validPlexModes);
    std::cerr << "theDude->getValidValues().size(): " << theDude->getValidValues().size() << "\n";
    EXPECT_EQ(1, (int)theDude->getValidValues().size());
    // ********************************************************

    // ********** Test Case 4  (both are simplex-able) (ensure the first test case passes again) *******
    std::cerr << "Testing  booklet format off  again\n";
    ticket->getIntent()->setBookletFormat(dune::imaging::types::BookletFormat::Off);

    // now get the constraints ...
    plexConstraints =  dynamicConstraintRules->getPlexModeConstraints(ticket);
    thePlexConstraints = plexConstraints->getConstraints();
    validPlexModes = thePlexConstraints[1];

    theDude = static_cast<ValidValuesEnum<dune::cdm::glossary_1::PlexMode>*>(validPlexModes);
    std::cerr << "theDude->getValidValues().size(): " << theDude->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)theDude->getValidValues().size());
    // ********************************************************
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenMediaSizeShouldBeDisabled_ThenDisableIt)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						{ \"size\":{ \"id\":\"PHOTO5X8\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\"], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        } "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
    std::cerr << "ticket->getConstraints()->getMediaSupportedSizes().size(): " << ticket->getConstraints()->getMediaSupportedSizes().size() << "\n";
    EXPECT_EQ(3,(int) ticket->getConstraints()->getMediaSupportedSizes().size());
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    // ********** Test Case 1 *******
    std::cerr << "Testing Tray1, LETTER, STATIONARY \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    std::shared_ptr<Constraints> SizeConstraints =  dynamicConstraintRules->getMediaSizeIdConstraints(ticket);
    std::vector<IConstraint*> theSizeConstraints = SizeConstraints->getConstraints();
    IConstraint* validSizes = theSizeConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaSize>* validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>*>(validSizes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    //EXPECT_EQ(3, (int)possibleDudes->getPossibleValues().size());
    EXPECT_EQ(3, (int)validDudes->getValidValues().size());
    // ********************************************************
    // ********** Test Case 2 (tray3 -> only 2 valid options) *******
    std::cerr << "Testing Tray3 LETTER, STATIONARY \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY3 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    SizeConstraints =  dynamicConstraintRules->getMediaSizeIdConstraints(ticket);
    theSizeConstraints = SizeConstraints->getConstraints();
    validSizes = theSizeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>*>(validSizes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************
    // ********** Test Case 3 (1 of the sizes can't duplex -> only 2 valid options ) *******
    std::cerr << "Testing DUPLEX, Tray2 Case \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY2 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    SizeConstraints =  dynamicConstraintRules->getMediaSizeIdConstraints(ticket);
    theSizeConstraints = SizeConstraints->getConstraints();
    validSizes = theSizeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>*>(validSizes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************
}


TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenMediaTypeShouldBeDisabled_ThenDisableIt)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						{ \"size\":{ \"id\":\"PHOTO5X8\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\"], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        } "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
    //std::cerr << "ticket->getConstraints()->getMediaSupportedSizes().size(): " << ticket->getConstraints()->getMediaSupportedSizes().size() << "\n";
    EXPECT_EQ(5,(int) ticket->getConstraints()->getMediaSupportedTypes().size());
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    // ********* Test Case  1 TRAY1, LETTER, STATIONARY, SIMPLEX   => 5 options
    std::cerr << "Testing TRAY1, LETTER, STATIONARY, SIMPLEX   => 5 options \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);
    ticket->getIntent()->setColorMode(dune::imaging::types::ColorMode::COLOR);

    // now get the constraints ...
    std::shared_ptr<Constraints> TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    std::vector<IConstraint*> theTypeConstraints = TypeConstraints->getConstraints();
    IConstraint* validTypes = theTypeConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaType>* validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(5, (int)validDudes->getValidValues().size());
    // ********************************************************

    // ********* Test Case TRAY1, LETTER, STATIONARY, DUPLEX    => 3 options
    std::cerr << "Testing TRAY1, LETTER, STATIONARY, DUPLEX \n";
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    ticket->getIntent()->setColorMode(dune::imaging::types::ColorMode::COLOR);

    // now get the constraints ...
    TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    theTypeConstraints = TypeConstraints->getConstraints();
    validTypes = theTypeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(3, (int)validDudes->getValidValues().size());
    // ********************************************************
    // ********* Test Case TRAY3, LETTER, STATIONARY, SIMLEX    => 4 options
    std::cerr << "Testing TRAY3, LETTER, STATIONARY, SIMLEX Case \n";
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY3 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setColorMode(dune::imaging::types::ColorMode::COLOR);

    // now get the constraints ...
    TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    theTypeConstraints = TypeConstraints->getConstraints();
    validTypes = theTypeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(4, (int)validDudes->getValidValues().size());
    // ********************************************************
    // ********* Test Case TRAY3, LETTER, STATIONARY, DUPLEX    => 3 options
    std::cerr << "Testing TRAY3, LETTER, STATIONARY, DUPLEX Case \n";
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY3 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    ticket->getIntent()->setColorMode(dune::imaging::types::ColorMode::COLOR);

    // now get the constraints ...
    TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    theTypeConstraints = TypeConstraints->getConstraints();
    validTypes = theTypeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(3, (int)validDudes->getValidValues().size());
    // ********************************************************
}


TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenMediaTypeShouldBeDisabledByColorMode_ThenDisableIt)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						{ \"size\":{ \"id\":\"PHOTO5X8\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\"], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"GRAYSCALE\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ ] "
"                        } "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
    //std::cerr << "ticket->getConstraints()->getMediaSupportedSizes().size(): " << ticket->getConstraints()->getMediaSupportedSizes().size() << "\n";
    EXPECT_EQ(5,(int) ticket->getConstraints()->getMediaSupportedTypes().size());
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    // ********* Test Case  1 TRAY1, LETTER, STATIONARY, SIMPLEX, COLOR   => 2 options
    std::cerr << "Testing TRAY1, LETTER, STATIONARY, SIMPLEX, COLOR  => 2 options \n";
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setColorMode(dune::imaging::types::ColorMode::COLOR);

    // now get the constraints ...
    std::shared_ptr<Constraints> TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    std::vector<IConstraint*> theTypeConstraints = TypeConstraints->getConstraints();
    IConstraint* validTypes = theTypeConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaType>* validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    // ********* Test Case TRAY1, LETTER, STATIONARY, SIMPLEX, GRAYSCALE    => 3 options
    std::cerr << "Testing TRAY1, LETTER, STATIONARY, SIMPLEX, GRAYSCALE   => 3 options\n";
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setColorMode(dune::imaging::types::ColorMode::GRAYSCALE);

    // now get the constraints ...
    TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    theTypeConstraints = TypeConstraints->getConstraints();
    validTypes = theTypeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(3, (int)validDudes->getValidValues().size());
    // ********************************************************}
}


TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhengetMediaIdTypeConstraintsIsCalled_WithMediaTypeVisibilityTogglingSupported_ThenOnlyEnabledMediaTypesAreReturned)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						{ \"size\":{ \"id\":\"PHOTO5X8\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\"], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"USER_DEFINED_1\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }  "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
    ticket->setisMediaTypeVisibilityTogglingSupported(true);
    //std::cerr << "ticket->getConstraints()->getMediaSupportedSizes().size(): " << ticket->getConstraints()->getMediaSupportedSizes().size() << "\n";
    EXPECT_EQ(3,(int) ticket->getConstraints()->getMediaSupportedSizes().size());
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();

    dune::print::engine::MockIMedia mockIMedia;
    //ensure mediaInterface not null
    ticket->setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket->getMediaInterface() != NULL);
    IMedia::InputList inputs;
    inputs.push_back(mockIMediaIInput);
    EXPECT_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillRepeatedly(Return(std::make_tuple(APIResult::OK, inputs)));

    std::vector<dune::imaging::types::MediaIdType> mediaIdTypes;
    mediaIdTypes.push_back(dune::imaging::types::MediaIdType::STATIONERY);
    mediaIdTypes.push_back(dune::imaging::types::MediaIdType::HPECOFFICIENT);
    mediaIdTypes.push_back(dune::imaging::types::MediaIdType::TRANSPARENCY);
    std::vector<dune::print::engine::MediaId> mediaIds;
    for(auto mediaType: mediaIdTypes)
    {
        dune::imaging::types::MediaId med(mediaType);
        mediaIds.push_back(med);
    }
    // ********* Test Case  1 TRAY1, LETTER, STATIONARY, SIMPLEX   => 3 options
    std::cerr << "Testing TRAY1, LETTER, STATIONARY, SIMPLEX   => 3 options \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    EXPECT_CALL(*mockIMediaIInput, getMediaSupportedTypes()).WillOnce(Return(std::make_tuple(APIResult::OK, mediaIds)));
    std::shared_ptr<Constraints> TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    std::vector<IConstraint*> theTypeConstraints = TypeConstraints->getConstraints();
    IConstraint* validTypes = theTypeConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaType>* validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(3, (int)validDudes->getValidValues().size());
    // ********************************************************
    // ********* Test Case  2 TRAY1, LETTER, STATIONARY, SIMPLEX, Enable user type 1  => 4 options
    std::cerr << "Testing TRAY1, LETTER, STATIONARY, SIMPLEX   => 4 options \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    mediaIds.push_back(dune::print::engine::MediaId(dune::imaging::types::MediaIdType::USER_DEFINED_1));
    // now get the constraints ...
    EXPECT_CALL(*mockIMediaIInput, getMediaSupportedTypes()).WillOnce(Return(std::make_tuple(APIResult::OK, mediaIds)));
    TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    theTypeConstraints = TypeConstraints->getConstraints();
    validTypes = theTypeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(4, (int)validDudes->getValidValues().size());
    // ********************************************************

    // ********* Test Case  3 TRAY1, LETTER, USER_DEFINED_1, SIMPLEX  => 4 options
    std::cerr << "Testing TRAY1, LETTER, STATIONARY, SIMPLEX   => 4 options \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::USER_DEFINED_1);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );

    // now get the constraints ...
    EXPECT_CALL(*mockIMediaIInput, getMediaSupportedTypes()).WillOnce(Return(std::make_tuple(APIResult::OK, mediaIds)));
    TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    theTypeConstraints = TypeConstraints->getConstraints();
    validTypes = theTypeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(4, (int)validDudes->getValidValues().size());

    //now check media source constraints
    std::shared_ptr<Constraints> SourceConstraints =  dynamicConstraintRules->getMediaSourceConstraints(ticket);
    std::vector<IConstraint*> theSourceConstraints = SourceConstraints->getConstraints();
    IConstraint* validSources = theSourceConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>* validSourceDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>*>(validSources);
    std::cerr << "ConstraintType:" << (int) validSourceDudes->getConstraintType() << " , validSourceDudes->getValidValues().size(): " << validSourceDudes->getValidValues().size() << "\n";
    EXPECT_EQ(1, (int)validSourceDudes->getValidValues().size());
    // ********************************************************

}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenColorShouldBeDisabled_ThenDisableIt)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    EXPECT_EQ(2,(int) ticket->getConstraints()->getColorMode().size());

    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // Test case 1, COLOR and GRAYSCALE are enabled
    // now get the constraints ...
    std::shared_ptr<Constraints> ColorModeConstraints =  dynamicConstraintRules->getPrintColorModeConstraints(ticket);
    std::vector<IConstraint*> theColorModeConstraints = ColorModeConstraints->getConstraints();
    IConstraint* validModes = theColorModeConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>* validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>*>(validModes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 2, COLOR is disabled
    // ********* disable Color
    MockICopyAdapter* mockICopyAdapter_true = new MockICopyAdapter();
    EXPECT_CALL(*mockICopyAdapter_true, getColorCopyEnabled()).WillRepeatedly(Return(true));
    MockICopyAdapter* mockICopyAdapter_false = new MockICopyAdapter();
    EXPECT_CALL(*mockICopyAdapter_false, getColorCopyEnabled()).WillRepeatedly(Return(false));
    dynamicConstraintRules->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter),"ICopyAdapter",mockICopyAdapter_false);

    // now get the constraints ...
    ColorModeConstraints =  dynamicConstraintRules->getPrintColorModeConstraints(ticket);
    theColorModeConstraints = ColorModeConstraints->getConstraints();
    validModes = theColorModeConstraints[1];
    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>*>(validModes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 3, COLOR and GRAYSCALE are both enabled again
    // ********* enable Color
    dynamicConstraintRules->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter),"ICopyAdapter",mockICopyAdapter_true);

    // now get the constraints ...
    ColorModeConstraints =  dynamicConstraintRules->getPrintColorModeConstraints(ticket);
    theColorModeConstraints = ColorModeConstraints->getConstraints();
    validModes = theColorModeConstraints[1];
    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>*>(validModes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************
    delete mockICopyAdapter_false;
    delete mockICopyAdapter_true;
}


TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenColorShouldBeDisabledByMediaType_ThenDisableIt)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"GRAYSCALE\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ ] "
"                        }, "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    EXPECT_EQ(2,(int) ticket->getConstraints()->getColorMode().size());

    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // Test case 1, COLOR and GRAYSCALE are enabled
    // now get the constraints ...
    std::shared_ptr<Constraints> ColorModeConstraints =  dynamicConstraintRules->getPrintColorModeConstraints(ticket);
    std::vector<IConstraint*> theColorModeConstraints = ColorModeConstraints->getConstraints();
    IConstraint* validModes = theColorModeConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>* validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>*>(validModes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::HPECOFFICIENT);

    // Test case 2, only COLOR is enabled
    // now get the constraints ...
    ColorModeConstraints =  dynamicConstraintRules->getPrintColorModeConstraints(ticket);
    theColorModeConstraints = ColorModeConstraints->getConstraints();
    validModes = theColorModeConstraints[1];
    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>*>(validModes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    // ********************************************************

    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::HPMATTE90G);

    // Test case 3, only GRAYSCALE is enabled
    // now get the constraints ...
    ColorModeConstraints =  dynamicConstraintRules->getPrintColorModeConstraints(ticket);
    theColorModeConstraints = ColorModeConstraints->getConstraints();
    validModes = theColorModeConstraints[1];
    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>*>(validModes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    // ********************************************************

    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::TRANSPARENCY);

    // Test case 4, neither COLOR nor GRAYSCALE are enabled!!
    // now get the constraints ...
    ColorModeConstraints =  dynamicConstraintRules->getPrintColorModeConstraints(ticket);
    theColorModeConstraints = ColorModeConstraints->getConstraints();
    validModes = theColorModeConstraints[1];
    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>*>(validModes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(0, (int)validDudes->getValidValues().size());
    // ********************************************************
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenRestrictPrintIsSet_ThenColorIsRestricted)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"GRAYSCALE\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ ] "
"                        }, "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [\"AUTODETECT\", \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    EXPECT_EQ(3,(int) ticket->getConstraints()->getColorMode().size());

    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);
    
    MockIColorAccessControl mockIColorAccessControl_;
    // Set the interface on both the constraint rules AND the ticket
    dynamicConstraintRules->setInterface(GET_INTERFACE_UID(IColorAccessControl), "MockIColorAccessControl", &mockIColorAccessControl_);
    ticket->setColorAccessControlInterface(&mockIColorAccessControl_);
    
    // For isRestrictColorPrint() to return true, we need getColorAccess() to return DISABLED
    EXPECT_CALL(mockIColorAccessControl_, getColorAccess())
        .WillRepeatedly(Return(ColorAccess::DISABLED));
    EXPECT_CALL(mockIColorAccessControl_, cannotPrintInColor(_, _))
        .WillRepeatedly(Return(true));  // true means color printing is NOT allowed
    bool colorAccess = dynamicConstraintRules->checkIfColorIsNotRestricted(ticket);
    EXPECT_EQ(colorAccess, false);
    EXPECT_EQ(true, ticket->isRestrictColorPrint());
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenRestrictPrintIsDisabled_ThenColorIsNotRestricted)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"GRAYSCALE\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ ] "
"                        }, "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [\"AUTODETECT\", \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    EXPECT_EQ(3,(int) ticket->getConstraints()->getColorMode().size());

    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);
    ticket->setRestrictColorPrint(false);
    MockIColorAccessControl mockIColorAccessControl_;
    dynamicConstraintRules->setInterface(GET_INTERFACE_UID(IColorAccessControl), "MockIColorAccessControl", &mockIColorAccessControl_);
    ON_CALL(mockIColorAccessControl_, getColorAccess())
        .WillByDefault(Return(ColorAccess::ENABLED));
    bool colorAccess = dynamicConstraintRules->checkIfColorIsNotRestricted(ticket);

    EXPECT_EQ(colorAccess, true);
    EXPECT_EQ(false, ticket->isRestrictColorPrint());
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenMediaSupportedSizeIsNotSet_ThenAnyIsValid)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                       \"plexMode\": [ "
"                       \"SIMPLEX\" "
"                       ], "
"                       \"plexBinding\": [ "
"                       \"ONE_SIDED\" "
"                       ], "
"                       \"collate\": [ "
"                       \"Collate\", "
"                       \"Uncollate\" "
"                       ], "
"                       \"copyMargins\": [ "
"                       \"CLIPCONTENT\", "
"                       \"ADDTOCONTENT\" "
"                       ], "
"                       \"minCopies\": 1, "
"                       \"maxCopies\": 99, "
"                       \"stepCopies\": 1.0, "
"                       \"printQuality\": [ "
"                       \"DRAFT\", "
"                       \"NORMAL\", "
"                       \"BEST\" "
"                       ], "
"                       \"mediaPrintSupportedSource\": [ "
"                       \"AUTOSELECT\", "
"                       \"MAINROLL\", "
"                       \"MAIN\", "
"                       \"TOP\" "
"                       ], "
"                       \"mediaPrintSupportedDestinations\": [ "
"                       \"STANDARDBIN\" "
"                       ], "
"                       \"mediaPrintSupportedSize\": [ "
"                       \"ANY\" "
"                       ], "
"                       \"mediaSupportedType\": [ "
"                       { "
"                           \"type\": { "
"                           \"id\": \"STATIONERY\" "
"                           }, "
"                           \"supportedMediaSource\": [ "
"                           \"MAINROLL\", "
"                           \"MAIN\", "
"                           \"TOP\" "
"                           ], "
"                           \"duplex\": [ "
"                           \"SIMPLEX\" "
"                           ], "
"                           \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                       }, "
"                       { "
"                           \"type\": { "
"                           \"id\": \"HP_BRIGHT_WHITE\" "
"                           }, "
"                           \"supportedMediaSource\": [ "
"                           \"MAINROLL\", "
"                           \"MAIN\", "
"                           \"TOP\" "
"                           ], "
"                           \"duplex\": [ "
"                           \"SIMPLEX\" "
"                           ], "
"                           \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                       } "
"                       ], "
"                       \"scanJobConstraint\": { "
"                       \"inputPlexMode\": [ "
"                           \"SIMPLEX\" "
"                       ], "
"                       \"colorMode\": [ "
"                           \"COLOR\", "
"                           \"GRAYSCALE\", "
"                           \"BLACKANDWHITE\" "
"                       ], "
"                       \"originalContentType\": [ "
"                           \"LINE_DRAWING\", "
"                           \"MIXED\", "
"                           \"IMAGE\" "
"                       ], "
"                       \"supportedMediaTypes\": [ "
"                           \"WHITE_PAPER\", "
"                           \"BLUEPRINTS\", "
"                           \"TRANSLUCENT_PAPER\" "
"                       ], "
"                       \"scanPagesFlipUpEnabled\": [ "
"                           false, "
"                           true "
"                       ], "
"                       \"pagesPerSheet\": [ "
"                           \"OneUp\" "
"                       ], "
"                       \"minScanExposure\": 1, "
"                       \"maxScanExposure\": 9, "
"                       \"stepScanExposure\": 1.0, "
"                       \"minScalePercent\": 25, "
"                       \"maxScalePercent\": 400, "
"                       \"step\": 1.0, "
"                       \"scaleSelection\": [ "
"                           \"NONE\", "
"                           \"CUSTOM\", "
"                           \"STANDARD_SIZE_SCALING\", "
"                           \"SCALE_TO_OUTPUT\" "
"                       ], "
"                       \"scaleToSizes\": [ "
"                           \"A0\", "
"                           \"A1\", "
"                           \"A2\", "
"                           \"A3\", "
"                           \"A4\", "
"                           \"B1\", "
"                           \"B2\", "
"                           \"B3\", "
"                           \"B4\", "
"                           \"LETTER\", "
"                           \"LEDGER\", "
"                           \"C_SIZE\", "
"                           \"D_SIZE\", "
"                           \"E_SIZE\", "
"                           \"ARCH_A\", "
"                           \"ARCH_B\", "
"                           \"ARCH_C\", "
"                           \"ARCH_D\", "
"                           \"ARCH_E\" "
"                       ], "
"                       \"mdfResolutions\": [ "
"                           200, "
"                           300, "
"                           600 "
"                       ], "
"                       \"mdfOriginalSizes\": [ "
"                           { "
"                           \"id\": \"ANY\", "
"                           \"mediaOrientation\": \"PORTRAIT\" "
"                           } "
"                       ] "
"                       } "
"                   } "
;

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    EXPECT_EQ(1, ticket->getConstraints()->getMediaPrintSupportedSize().size());
    EXPECT_EQ(0, ticket->getConstraints()->getMediaSupportedSizes().size());

    const char *componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::AUTOSELECT);
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    std::shared_ptr<Constraints> mediaSizeIdConstraints = dynamicConstraintRules->getMediaSizeIdConstraints(ticket);
    std::vector<IConstraint *> theMediaSizeIdConstraints = mediaSizeIdConstraints->getConstraints();
    IConstraint *validSizes = theMediaSizeIdConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaSize> *validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>*>(validSizes);

    std::cerr << "ConstraintType: " << (int) validDudes->getConstraintType() << ", validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    EXPECT_EQ(dune::cdm::glossary_1::MediaSize::any, validDudes->getValidValues().at(0));
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenPlexModeisDuplex_ThenMixedSizesIsDisable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);
    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaPrintSupportedSource\": [ \"AUTOSELECT\", \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                    ], "
"                    \"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                   ], "
"                        \"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"AUTODETECT\", \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\", \"IMAGE\" ], "
"                        \"pagesPerSheet\": [ \"OneUp\", \"TwoUp\" ], "
"                        \"bookletFormat\": [ \"Off\", \"LeftEdge\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"                        \"adfOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"                        ], "
"                        \"flatbedOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"                       ]"
"                       } "
"				} "
;


    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    EXPECT_EQ(4, ticket->getConstraints()->getAdfOriginalSizes().size());
    EXPECT_EQ(2, ticket->getConstraints()->getPagesPerSheet().size());

    ticket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    ticket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);

    const char *componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);
    
    auto constraints = std::make_shared<Constraints>();
    std::vector<dune::cdm::glossary_1::MediaSize> enumPossibleValues;
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::any);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_ledger);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_a4_dash_a3);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_legal);

    std::vector<dune::cdm::glossary_1::MediaSize> enumValidValues = enumPossibleValues;

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumPossibleValues, &dune::cdm::glossary_1::MediaSize::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumValidValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    std::shared_ptr<ConstraintsGroup> constraintsGroup = std::make_shared<ConstraintsGroup>();
    constraintsGroup->set("src/scan/mediaSize", constraints);

    std::shared_ptr<Constraints> mediaSizeIdConstraints = dynamicConstraintRules->getInputMediaSizeIdConstraints(ticket, constraints);
    std::vector<IConstraint *> theMediaSizeIdConstraints = mediaSizeIdConstraints->getConstraints();
    IConstraint *validSizes = theMediaSizeIdConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaSize> *validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>*>(validSizes);

    std::cerr << "ConstraintType: " << (int) validDudes->getConstraintType() << ", validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    EXPECT_EQ(dune::cdm::glossary_1::MediaSize::any, validDudes->getValidValues().at(0));
}


TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenInBookMode_ThenOnlyTwoSizesAreAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);
    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaPrintSupportedSource\": [ \"AUTOSELECT\", \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                    ], "
"                    \"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                   ], "
"                        \"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"AUTODETECT\", \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\", \"IMAGE\" ], "
"                        \"pagesPerSheet\": [ \"OneUp\", \"TwoUp\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"                        \"adfOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"                        ], "
"                        \"flatbedOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"LANDSCAPE\" "
"                            }, "
"                            { "
"                                \"id\":\"A4\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"A4\", "
"                                \"mediaOrientation\":\"LANDSCAPE\" "
"                            }, "
"                            { "
"                                \"id\":\"A5\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"                       ]"
"                       } "
"				} "
;


    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    ticket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    ticket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);

    const char *componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);
    
    auto constraints = std::make_shared<Constraints>();
    std::vector<dune::cdm::glossary_1::MediaSize> enumPossibleValues;
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::any);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_ledger);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_a4_dash_a3);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_legal);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::iso_a4_210x297mm);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::iso_a5_148x210mm);

    std::vector<dune::cdm::glossary_1::MediaSize> enumValidValues = enumPossibleValues;

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumPossibleValues, &dune::cdm::glossary_1::MediaSize::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumValidValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    std::shared_ptr<ConstraintsGroup> constraintsGroup = std::make_shared<ConstraintsGroup>();
    constraintsGroup->set("src/scan/mediaSize", constraints);

    // Check for only Letter and A4 available.
    std::shared_ptr<Constraints> mediaSizeIdConstraints = dynamicConstraintRules->getInputMediaSizeIdConstraints(ticket, constraints);
    std::vector<IConstraint *> theMediaSizeIdConstraints = mediaSizeIdConstraints->getConstraints();
    IConstraint *validSizes = theMediaSizeIdConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaSize> *validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>*>(validSizes);

    std::cerr << "ConstraintType: " << (int) validDudes->getConstraintType() << ", validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
}



TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    ASSERT_TRUE(true);
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenMediaSizeCalledWithManualFeed_ThenConstraintsShouldBeTheSameWithTray1)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                             \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						 { \"size\":{ \"id\":\"PHOTO5X8\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\"], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"						 { "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        } "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
    std::cerr << "ticket->getConstraints()->getMediaSupportedSizes().size(): " << ticket->getConstraints()->getMediaSupportedSizes().size() << "\n";
    EXPECT_EQ(3,(int) ticket->getConstraints()->getMediaSupportedSizes().size());
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    // ********** Test Case 1 *******
    std::cerr << "Testing Tray1, LETTER, STATIONARY \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    std::shared_ptr<Constraints> SizeConstraints =  dynamicConstraintRules->getMediaSizeIdConstraints(ticket);
    std::vector<IConstraint*> theSizeConstraints = SizeConstraints->getConstraints();
    IConstraint* validSizes = theSizeConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaSize>* validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>*>(validSizes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    //EXPECT_EQ(3, (int)possibleDudes->getPossibleValues().size());
    EXPECT_EQ(3, (int)validDudes->getValidValues().size());
    // ********************************************************
    // ********** Test Case 2 (ManualFeed -> same with Tray1) *******
    std::cerr << "Testing ManualFeed LETTER, STATIONARY \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::MANUALFEED );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    SizeConstraints =  dynamicConstraintRules->getMediaSizeIdConstraints(ticket);
    theSizeConstraints = SizeConstraints->getConstraints();
    validSizes = theSizeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>*>(validSizes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(3, (int)validDudes->getValidValues().size());

}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenMediaTypeCalledWithManualFeed_ThenConstraintsShouldBeTheSameWithTray1)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						 { \"size\":{ \"id\":\"PHOTO5X8\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\"], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"						 { "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        } "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
    //std::cerr << "ticket->getConstraints()->getMediaSupportedSizes().size(): " << ticket->getConstraints()->getMediaSupportedSizes().size() << "\n";
    EXPECT_EQ(3,(int) ticket->getConstraints()->getMediaSupportedSizes().size());
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    // ********* Test Case TRAY1, LETTER, STATIONARY, SIMPLEX  => 5 options
    std::cerr << "Testing TRAY1, LETTER, STATIONARY, SIMPLEX   => 5 options \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY1 );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    std::shared_ptr<Constraints> TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    std::vector<IConstraint*> theTypeConstraints = TypeConstraints->getConstraints();
    IConstraint* validTypes = theTypeConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaType>* validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(5, (int)validDudes->getValidValues().size());

    // ********************************************************
    // ********* Test Case MANUALFEED, LETTER, STATIONARY, SIMPLEX  => 5 options
    std::cerr << "Testing TRAY1, LETTER, STATIONARY, DUPLEX \n";
    ticket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setOutputMediaSource(dune::imaging::types::MediaSource::MANUALFEED );
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::STATIONERY);

    // now get the constraints ...
    TypeConstraints =  dynamicConstraintRules->getMediaIdTypeConstraints(ticket);
    theTypeConstraints = TypeConstraints->getConstraints();
    validTypes = theTypeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(5, (int)validDudes->getValidValues().size());
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenGettingDynamicConstraints_ThenCheckConstraintValueOfCustomMediaXFeedDimension)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    // set customMediaXFeedDimension value in copy job ticket.
    double customMediaXFeedDimension = 40000;
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::CUSTOM);
    ticket->getIntent()->setCustomMediaXDimension(customMediaXFeedDimension);

    // create constraint range for MockIMediaConstraints.
    double minValue = 38600;
    double maxValue = 125900;
    double stepValue = 1;
    auto tempConstraint = createConstraintRange(minValue, maxValue, stepValue);

    dune::print::engine::constraints::MockIMediaConstraints mockIMediaConstraints{};
    // expected call for mediaConstraints during getDynamicMediaConstraints
    EXPECT_CALL(mockIMediaConstraints, getMediaWidthConstraintsForMediaSource(testing::_)).WillRepeatedly(Return(std::tuple<APIResult, std::shared_ptr<Constraints>>{APIResult::OK, tempConstraint}));

    // get dynamic constraint
    std::shared_ptr<Constraints> customMediaXFeedDimensionConstraints = dynamicConstraintRules->getCustomMediaXFeedDimension(&mockIMediaConstraints);
    std::vector<IConstraint*> theCustomMediaXFeedDimensionConstraints = customMediaXFeedDimensionConstraints->getConstraints();
    RangeDouble *constraint = static_cast<RangeDouble *>(theCustomMediaXFeedDimensionConstraints.front());

    // check values.
    EXPECT_EQ(constraint->getMin(), (double) 38600);
    EXPECT_EQ(constraint->getMax(), (double) 125900);
    EXPECT_EQ(constraint->getStep(), (double) 1);
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenGettingDynamicConstraints_ThenCheckConstraintValueOfCustomMediaYFeedDimension)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    // set customMediaYFeedDimension value in copy job ticket.
    double customMediaYFeedDimension = 70000;
    ticket->getIntent()->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::CUSTOM);
    ticket->getIntent()->setCustomMediaYDimension(customMediaYFeedDimension);

    // create constraint range for MockIMediaConstraints.
    double minValue = 55000;
    double maxValue = 180000;
    double stepValue = 1;
    auto tempConstraint = createConstraintRange(minValue, maxValue, stepValue);

    dune::print::engine::constraints::MockIMediaConstraints mockIMediaConstraints{};
    // expected call for mediaConstraints during getDynamicMediaConstraints
    EXPECT_CALL(mockIMediaConstraints, getMediaLengthConstraintsForMediaSource(testing::_)).WillRepeatedly(Return(std::tuple<APIResult, std::shared_ptr<Constraints>>{APIResult::OK, tempConstraint}));

    // get dynamic constraint
    std::shared_ptr<Constraints> customMediaYFeedDimensionConstraints = dynamicConstraintRules->getCustomMediaYFeedDimension(&mockIMediaConstraints);
    std::vector<IConstraint*> theCustomMediaYFeedDimensionConstraints = customMediaYFeedDimensionConstraints->getConstraints();
    RangeDouble *constraint = static_cast<RangeDouble *>(theCustomMediaYFeedDimensionConstraints.front());

    // check values.
    EXPECT_EQ(constraint->getMin(), (double) 55000);
    EXPECT_EQ(constraint->getMax(), (double) 180000);
    EXPECT_EQ(constraint->getStep(), (double) 1);
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenInIdCardMode_ThenOnlyTwoSizesAreAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);
    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaPrintSupportedSource\": [ \"AUTOSELECT\", \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                    ], "
"                    \"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                   ], "
"                        \"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"AUTODETECT\", \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\", \"IMAGE\" ], "
"                        \"pagesPerSheet\": [ \"OneUp\", \"TwoUp\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"                        \"adfOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"                        ], "
"                        \"flatbedOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"A4\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"A5\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"                       ]"
"                       } "
"				} "
;


    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    ticket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    ticket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);

    const char *componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);
    
    auto constraints = std::make_shared<Constraints>();
    std::vector<dune::cdm::glossary_1::MediaSize> enumPossibleValues;
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::any);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_ledger);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_a4_dash_a3);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_legal);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::iso_a4_210x297mm);
    enumPossibleValues.push_back(dune::cdm::glossary_1::MediaSize::iso_a5_148x210mm);

    std::vector<dune::cdm::glossary_1::MediaSize> enumValidValues = enumPossibleValues;

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumPossibleValues, &dune::cdm::glossary_1::MediaSize::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumValidValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    std::shared_ptr<ConstraintsGroup> constraintsGroup = std::make_shared<ConstraintsGroup>();
    constraintsGroup->set("src/scan/mediaSize", constraints);

    // Check for only Letter and A4 available.
    std::shared_ptr<Constraints> mediaSizeIdConstraints = dynamicConstraintRules->getInputMediaSizeIdConstraints(ticket, constraints);
    std::vector<IConstraint *> theMediaSizeIdConstraints = mediaSizeIdConstraints->getConstraints();
    IConstraint *validSizes = theMediaSizeIdConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaSize> *validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>*>(validSizes);

    std::cerr << "ConstraintType: " << (int) validDudes->getConstraintType() << ", validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesStandard : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyJobDynamicConstraintRulesStandard :public GivenANewCopyJobDynamicConstraintRulesStandard
{
  public:

    GivenAConnectedCopyJobDynamicConstraintRulesStandard() {};

    template<typename T>
    std::shared_ptr<Constraints> getEnumConstraints(std::vector<T> enumValues);

    template<typename T>
    void checkConstraintResult(std::vector<T> expectedValidValues,std::shared_ptr<dune::framework::data::constraints::Constraints> constraints);

    virtual void SetUp() override;

    virtual void TearDown() override;

    std::shared_ptr<ConstraintsGroup>       staticConstraints_{nullptr};
    std::shared_ptr<MockICopyJobTicket>     mockICopyJobTicket_;
    std::shared_ptr<ICopyJobConstraints>    copyJobConstraints_{nullptr};

};

void GivenAConnectedCopyJobDynamicConstraintRulesStandard::SetUp()
{
    GivenANewCopyJobDynamicConstraintRulesStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    scanConstraints_ = new dune::scan::MockIScanConstraints();

    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockIScanConstraints", scanConstraints_);
    
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // setup constraints expected on ticket
    copyJobConstraints_ = std::make_shared<CopyJobConstraint>();
    mockICopyJobTicket_ = std::make_shared<MockICopyJobTicket>();
    ON_CALL(*mockICopyJobTicket_,getConstraints()).WillByDefault(Return(copyJobConstraints_));
    ON_CALL(*mockICopyJobTicket_,getSecurityContext()).WillByDefault(Return(nullptr));
}

void GivenAConnectedCopyJobDynamicConstraintRulesStandard::TearDown()
{
    delete scanConstraints_;
    GivenANewCopyJobDynamicConstraintRulesStandard::TearDown();
}

template<typename T>
std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesStandard::getEnumConstraints(std::vector<T> enumValues)
{
    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<T>>(enumValues,
                                        &T::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<T>>(enumValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

template<typename T>
void GivenAConnectedCopyJobDynamicConstraintRulesStandard::checkConstraintResult(std::vector<T> expectedValidValues,std::shared_ptr<dune::framework::data::constraints::Constraints> constraints)
{
    // Check Result for current type
    if(expectedValidValues.size() > 0 && constraints != nullptr)
    {
        std::vector<T> dynamicValidValues;
        for(auto constraint : constraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
            {
                dynamicValidValues = (static_cast< dune::framework::data::constraints::ValidValuesEnum<T>*>(constraint))->getValidValues();
                break;
            }
        }

        // Check if number of constraints coincidence
        EXPECT_EQ(expectedValidValues.size(), dynamicValidValues.size());

        for(auto expectedValue : expectedValidValues)
        {
            auto iteratorConstraintValues = std::find(dynamicValidValues.begin(), dynamicValidValues.end(), expectedValue);
            EXPECT_TRUE(iteratorConstraintValues != dynamicValidValues.end());
        }
    }
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesStandard, WhenUpdateWithJobDynamicConstraintIscalled_ThenItCallsScanConstraintMethod)
{
    std::shared_ptr<dune::job::IJobTicket> jobTicket;
    jobTicket = mockICopyJobTicket_;
    std::vector<std::string> blockedSettingsBetweenPages;
    std::vector<std::pair<std::string, std::string>> vectorMapStringIdForSettings;
    ON_CALL(*mockICopyJobTicket_,getState()).WillByDefault(Return(dune::job::JobStateType::PROCESSING));
    EXPECT_CALL(*scanConstraints_, updateWithJobDynamicConstraints(testing::_,testing::_,testing::_,testing::_))
    .Times(1)
    .WillOnce(DoAll(
        testing::SaveArg<2>(&blockedSettingsBetweenPages),
        testing::SaveArg<3>(&vectorMapStringIdForSettings)
    ));
    auto constraintsGroup = std::make_shared<dune::framework::data::constraints::ConstraintsGroup>();
    component_->updateWithJobDynamicConstraints(mockICopyJobTicket_, constraintsGroup);
    // Print captured parameters for debugging
    EXPECT_EQ(7, blockedSettingsBetweenPages.size());
    EXPECT_EQ(7, vectorMapStringIdForSettings.size());
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesStandard, WhenUpdateWithJobDynamicConstraintIscalledWithEmptyJobTicket_ThenItNotCallsScanConstraintMethod)
{
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket;
    EXPECT_CALL(*scanConstraints_, updateWithJobDynamicConstraints(testing::_,testing::_,testing::_,testing::_))
    .Times(0);
    auto constraintsGroup = std::make_shared<dune::framework::data::constraints::ConstraintsGroup>();
    component_->updateWithJobDynamicConstraints(jobTicket, constraintsGroup);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesStandard, WhenUpdateWithJobDynamicConstraintIscalledWithEmptyConstraintGroup_ThenItNotCallsScanConstraintMethod)
{
    ON_CALL(*mockICopyJobTicket_,getState()).WillByDefault(Return(dune::job::JobStateType::PROCESSING));
    EXPECT_CALL(*scanConstraints_, updateWithJobDynamicConstraints(testing::_,testing::_,testing::_,testing::_))
    .Times(0);
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroupEmpty;
    component_->updateWithJobDynamicConstraints(mockICopyJobTicket_, constraintsGroupEmpty);
}
///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesStandardReadyToCallShutdown : shutdown case.
// Dummy class that inherits from GivenAConnectedCopyJobDynamicConstraintRulesStandard in order to reuse code
// and enable parametrized tests.
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyJobDynamicConstraintRulesStandardReadyToCallShutdown : public GivenAConnectedCopyJobDynamicConstraintRulesStandard,
                           public ::testing::WithParamInterface<IComponent::ShutdownCause>
{

};


TEST_P(GivenAConnectedCopyJobDynamicConstraintRulesStandardReadyToCallShutdown, whenShutdownIsCalled_TheComponentGetsShutdown)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    // Call GetParam() here to get the Row values
    IComponent::ShutdownCause const& p = GetParam();

    std::future<void> asyncCompletion;
    comp->shutdown(p, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

     ASSERT_TRUE(true);
}

INSTANTIATE_TEST_CASE_P(InstantiationName, GivenAConnectedCopyJobDynamicConstraintRulesStandardReadyToCallShutdown, ::testing::Values(
 IComponent::ShutdownCause(IComponent::ShutdownCause::POWER_OFF),
 IComponent::ShutdownCause(IComponent::ShutdownCause::REBOOT),
 IComponent::ShutdownCause(IComponent::ShutdownCause::SEVERE_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::EMERGENCY_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::CRITICAL_ERROR)
));

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenPagesPerSheetShouldBeDisabled_ThenDisableIt)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"pagesPerSheet\": [ \"OneUp\", \"TwoUp\" ], "
"                        \"bookletFormat\": [ \"Off\", \"LeftEdge\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"                        \"adfOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"						], "
"						\"flatbedOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"                       ]"
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    // Test case 1, ONEUP and TWOUP are enabled
    // checking to make sure there is more than 1 enabled pages per sheet setting
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    std::shared_ptr<Constraints>                            PagesPerSheetConstraints    = dynamicConstraintRules->getPagesPerSheetConstraints(ticket);
    std::vector<IConstraint*>                               ThePagesPerSheetConstraints = PagesPerSheetConstraints->getConstraints();
    IConstraint*                                            validModes                  = ThePagesPerSheetConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>* validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());

    // ********************************************************

    // Test case 2, TWOUP is disabled after enabling ScaleSelection
    // enable scaleSelection
    ticket->getIntent()->setScaleSelection(dune::scan::types::ScanScaleSelectionEnum::FITTOPAGE);

    // now get the constraints ... TwoUp Should be disabled
    PagesPerSheetConstraints    = dynamicConstraintRules->getPagesPerSheetConstraints(ticket);
    ThePagesPerSheetConstraints = PagesPerSheetConstraints->getConstraints();
    validModes                  = ThePagesPerSheetConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>*>(validModes);
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 3, ONEUP and TWOUP are both enabled again
    // disable ScaleSelection
    ticket->getIntent()->setScaleSelection(dune::scan::types::ScanScaleSelectionEnum::NONE);

    // now get the constraints ... TwoUp Should be disabled
    PagesPerSheetConstraints    = dynamicConstraintRules->getPagesPerSheetConstraints(ticket);
    ThePagesPerSheetConstraints = PagesPerSheetConstraints->getConstraints();
    validModes                  = ThePagesPerSheetConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 4, TWOUP is disabled after enabling originalSize MIXED_A4_A3
    // enable originalSize Mixed-A4-A3
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_A4_A3);

    // now get the constraints ... TwoUp Should be disabled
    PagesPerSheetConstraints    = dynamicConstraintRules->getPagesPerSheetConstraints(ticket);
    ThePagesPerSheetConstraints = PagesPerSheetConstraints->getConstraints();
    validModes                  = ThePagesPerSheetConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>*>(validModes);
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 5, TWOUP is disabled after enabling originalSize MIXED_LETTER_LEGAL
    // enable originalSize MIXED_LETTER_LEGAL
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL);

    // now get the constraints ... TwoUp Should be disabled
    PagesPerSheetConstraints    = dynamicConstraintRules->getPagesPerSheetConstraints(ticket);
    ThePagesPerSheetConstraints = PagesPerSheetConstraints->getConstraints();
    validModes                  = ThePagesPerSheetConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>*>(validModes);
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 6, TWOUP is disabled after enabling originalSize MIXED_LETTER_LEDGER
    // enable originalSize MIXED_LETTER_LEDGER
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER);

    // now get the constraints ... TwoUp Should be disabled
    PagesPerSheetConstraints    = dynamicConstraintRules->getPagesPerSheetConstraints(ticket);
    ThePagesPerSheetConstraints = PagesPerSheetConstraints->getConstraints();
    validModes                  = ThePagesPerSheetConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>*>(validModes);
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 7, ONEUP and TWOUP are both enabled again
    // disable originalSize MIXED and enable originalSize Any
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);

    // now get the constraints ... TwoUp Should be disabled
    PagesPerSheetConstraints    = dynamicConstraintRules->getPagesPerSheetConstraints(ticket);
    ThePagesPerSheetConstraints = PagesPerSheetConstraints->getConstraints();
    validModes                  = ThePagesPerSheetConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());

    // ********************************************************
    ticket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);

    // now get the constraints ... Pages perSheet Should be disabled
    PagesPerSheetConstraints    = dynamicConstraintRules->getPagesPerSheetConstraints(ticket);
    ThePagesPerSheetConstraints = PagesPerSheetConstraints->getConstraints();
    validModes                  = ThePagesPerSheetConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>*>(validModes);

    auto lockConstraint = PagesPerSheetConstraints->getConstraints(dune::framework::data::constraints::ConstraintType::LOCK);
    EXPECT_NE(nullptr, lockConstraint);
    // ********************************************************
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenWatermarkTypeIsSet_ThenWatermarkTypeConstraintsAreReturned)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"pagesPerSheet\": [ \"OneUp\", \"TwoUp\" ], "
"                        \"bookletFormat\": [ \"Off\", \"LeftEdge\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"                        \"watermarkType\": [ \"NONE\", \"TEXT_WATERMARK\"], "
"                        \"watermarkId\": [ \"NONE\", \"DRAFT\", \"CONFIDENTIAL\", \"SECRET\", \"TOP_SECRET\", \"URGENT\", \"USER_DEFINED_1\", \"ADMIN_DEFINED_1\", \"ADMIN_DEFINED_2\", \"ADMIN_DEFINED_3\", \"ADMIN_DEFINED_4\", \"ADMIN_DEFINED_5\", \"ADMIN_DEFINED_6\", \"ADMIN_DEFINED_7\", \"ADMIN_DEFINED_8\" ], "
"                        \"watermarkTextColor\": [ \"BLACK\", \"YELLOW\", \"GREEN\", \"RED\", \"BLUE\", \"SKY_BLUE\", \"PURPLE\" ], "
"                        \"watermarkTextSize\": [ \"THIRTY_POINT\", \"FORTY_POINT\", \"SIXTY_POINT\" ], "
"                        \"watermarkTextFont\": [ \"LETTER_GOTHIC\", \"ANTIQUE_OLIVE\", \"CENTURY_SCHOOLBOOK\", \"GARAMOND\" ], "
"                        \"watermarkBackgroundColor\": [ \"GRAY\", \"CYAN\", \"MAGENTA\" ], "
"                        \"watermarkBackgroundPattern\": [ \"FLAT\", \"LEAF\", \"SCROLL\" ], "
"                        \"adfOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"						], "
"						\"flatbedOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"                       ]"
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    // Test case 1, ONEUP and TWOUP are enabled
    // checking to make sure there is more than 1 enabled pages per sheet setting
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    std::shared_ptr<Constraints>                            WatermarkTypeConstraints     = dynamicConstraintRules->getWatermarkTypeConstraints(ticket);
    std::vector<IConstraint*>                               TheWatermarkTypeConstraints  = WatermarkTypeConstraints->getConstraints();
    IConstraint*                                            validModes                   = TheWatermarkTypeConstraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::watermarkDetails::WatermarkType>* validTypeDudes   = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::watermarkDetails::WatermarkType>*>(validModes);
    EXPECT_EQ(2, (int)validTypeDudes->getValidValues().size());

    std::shared_ptr<Constraints>                            WatermarkIdConstraints       = dynamicConstraintRules->getWatermarkIdConstraints(ticket);
    std::vector<IConstraint*>                               TheWatermarkIdConstraints    = WatermarkIdConstraints->getConstraints();
    IConstraint*                                            validIdModes                 = TheWatermarkIdConstraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::WatermarkTextType>* validTextTypeDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::WatermarkTextType>*>(validIdModes);
    EXPECT_EQ(15, (int)validTextTypeDudes->getValidValues().size());

    std::shared_ptr<Constraints>                            WatermarkTextColorConstraints = dynamicConstraintRules->getWatermarkTextColorConstraints(ticket);
    std::vector<IConstraint*>                               TheWatermarkTextColorConstraints = WatermarkTextColorConstraints->getConstraints();
    IConstraint*                                            validTextColorModes = TheWatermarkTextColorConstraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextColor>* validTextColorDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextColor>*>(validTextColorModes);
    EXPECT_EQ(7, (int)validTextColorDudes->getValidValues().size());

    std::shared_ptr<Constraints>                            WatermarkTextSizeConstraints = dynamicConstraintRules->getWatermarkTextSizeConstraints(ticket);
    std::vector<IConstraint*>                               TheWatermarkTextSizeConstraints = WatermarkTextSizeConstraints->getConstraints();
    IConstraint*                                            validTextSizeModes = TheWatermarkTextSizeConstraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextSize>* validTextSizeDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextSize>*>(validTextSizeModes);
    EXPECT_EQ(3, (int)validTextSizeDudes->getValidValues().size());
    
    std::shared_ptr<Constraints>                            WatermarkTextFontConstraints = dynamicConstraintRules->getWatermarkTextFontConstraints(ticket);
    std::vector<IConstraint*>                               TheWatermarkTextFontConstraints = WatermarkTextFontConstraints->getConstraints();
    IConstraint*                                            validTextFontModes = TheWatermarkTextFontConstraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextFont>* validTextFontDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextFont>*>(validTextFontModes);
    EXPECT_EQ(4, (int)validTextFontDudes->getValidValues().size());
    
    std::shared_ptr<Constraints>                            WatermarkBackgroundColorConstraints = dynamicConstraintRules->getWatermarkBackgroundColorConstraints(ticket);
    std::vector<IConstraint*>                               TheWatermarkBackgroundColorConstraints = WatermarkBackgroundColorConstraints->getConstraints();
    IConstraint*                                            validBackgroundColorModes = TheWatermarkBackgroundColorConstraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::watermarkDetails::BackgroundColor>* validBackgroundColorDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::watermarkDetails::BackgroundColor>*>(validBackgroundColorModes);
    EXPECT_EQ(3, (int)validBackgroundColorDudes->getValidValues().size());
    
    std::shared_ptr<Constraints>                            WatermarkBackgroundPatternConstraints = dynamicConstraintRules->getWatermarkBackgroundPatternConstraints(ticket);
    std::vector<IConstraint*>                               TheWatermarkBackgroundPatternConstraints = WatermarkBackgroundPatternConstraints->getConstraints();
    IConstraint*                                            validBackgroundPatternModes = TheWatermarkBackgroundPatternConstraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::watermarkDetails::BackgroundPattern>* validBackgroundPatternDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::watermarkDetails::BackgroundPattern>*>(validBackgroundPatternModes);
    EXPECT_EQ(3, (int)validBackgroundPatternDudes->getValidValues().size());
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenScaleSelectionShouldBeDisabled_ThenDisableIt)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);
    
    ticket->setPrePrintConfiguration(Product::ENTERPRISE);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"pagesPerSheet\": [ \"OneUp\", \"TwoUp\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"                        \"adfOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"						], "
"						\"flatbedOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_A4_A3\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"MIXED_LETTER_LEDGER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"                       ]"
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    // Test case 1, CUSTOM is enabled
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    std::shared_ptr<Constraints>                                      ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    std::vector<IConstraint*>                                         TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    IConstraint*                                                      validModes                  = TheScaleSelectionConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>* validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(7, (int)validDudes->getValidValues().size());

    // ********************************************************

    // Test case 2, CUSTOM is disabled after enabling TWOUP
    // enable TWOUP
    ticket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    // now get the constraints ... CUSTOM Should be disabled
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    validModes                  = TheScaleSelectionConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 3, CUSTOM is disabled after enabling FourUp
    // enable FourUp
    ticket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::FourUp);

    // now get the constraints ... CUSTOM Should be disabled
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    validModes                  = TheScaleSelectionConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 4, CUSTOM is enabled again after enabling OneUp
    // enable OneUp
    ticket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::OneUp);

    // now get the constraints ... TwoUp Should be disabled
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    validModes                  = TheScaleSelectionConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(7, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 5, CUSTOM is disabled after enabling originalSize MIXED_A4_A3
    // enable originalSize Mixed-A4-A3
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_A4_A3);

    // now get the constraints ... CUSTOM Should be disabled
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    validModes                  = TheScaleSelectionConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 6, CUSTOM is disabled after enabling originalSize MIXED_LETTER_LEGAL
    // enable originalSize MIXED_LETTER_LEGAL
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL);

    // now get the constraints ... CUSTOM Should be disabled
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    validModes                  = TheScaleSelectionConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 7, CUSTOM is disabled after enabling originalSize MIXED_LETTER_LEDGER
    // enable originalSize MIXED_LETTER_LEDGER
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER);

    // now get the constraints ... CUSTOM Should be disabled
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    validModes                  = TheScaleSelectionConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 8, CUSTOM is enabled again after enabling originalSize Any
    // enable originalSize Any
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);

    // now get the constraints ... TwoUp Should be disabled
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    validModes                  = TheScaleSelectionConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(7, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 9, CUSTOM is disabled after enabling Booklet Format On
    // enable FourUp
    ticket->getIntent()->setBookletFormat(dune::imaging::types::BookletFormat::LeftEdge);

    // now get the constraints ... CUSTOM Should be disabled
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    validModes                  = TheScaleSelectionConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
    // ********************************************************

    // Test case 10, CUSTOM is enabled again after enabling Booklet Format Off
    // enable FourUp
    ticket->getIntent()->setBookletFormat(dune::imaging::types::BookletFormat::Off);

    // now get the constraints ... CUSTOM Should be disabled
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    TheScaleSelectionConstraints = ScaleSelectionConstraints->getConstraints();
    validModes                  = TheScaleSelectionConstraints[1];
    validDudes                  = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>(validModes);
    EXPECT_EQ(7, (int)validDudes->getValidValues().size());
    // ********************************************************

    ticket->setPrePrintConfiguration(Product::HOME_PRO);
    ticket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    ScaleSelectionConstraints    = dynamicConstraintRules->getScaleSelectionConstraints(ticket);
    EXPECT_NE(nullptr,  ScaleSelectionConstraints->getConstraints(dune::framework::data::constraints::ConstraintType::LOCK));

}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenGetStampTypeConstraintsIsCalledAndIfStampTypeOfStampTicketIsNotNone_ThenStampTypeOrderIsNotDefault)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"					\"scanJobConstraint\": {  "
"                        \"stampType\": [ "
"                            \"NONE\", "
"                            \"IP_ADDRESS\", "
"                            \"USER_NAME\", "
"                            \"PRODUCT_INFORMATION\", "
"                            \"PAGE_NUMBER\", "
"                            \"DATE_AND_TIME\", "
"                            \"DATE\" "
"                        ] "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    dune::imaging::types::ScanStampLocationFbT stampLocationFbT;
    std::vector<std::unique_ptr<dune::imaging::types::StampContentT>> stampContents{};

    auto content1 = std::make_unique<dune::imaging::types::StampContentT>();
    content1->stampId = dune::imaging::types::StampType::USER_NAME;
    stampContents.emplace_back(std::move(content1));

    auto content2 = std::make_unique<dune::imaging::types::StampContentT>();
    content2->stampId = dune::imaging::types::StampType::PAGE_NUMBER;
    stampContents.emplace_back(std::move(content2));

    stampLocationFbT.stampContents = std::move(stampContents);
    ticket->getIntent()->setStampTopLeft(stampLocationFbT);
    
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    std::shared_ptr<Constraints> dynamicConstraints = dynamicConstraintRules->getStampTypeConstraints(dune::cdm::overlay_1::StampLocation::topLeft, ticket, dune::imaging::types::StampPolicy::NONE);

    EXPECT_TRUE(dynamicConstraints != nullptr);

    std::vector<IConstraint*> constraints = dynamicConstraints->getConstraints();
    IConstraint* validValue   = constraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampType>* stampType_valid = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampType>*>(validValue);
    
    std::vector<dune::cdm::overlay_1::StampType> expectValues = { 
        dune::cdm::overlay_1::StampType::none,
        dune::cdm::overlay_1::StampType::userName,
        dune::cdm::overlay_1::StampType::pageNumber,
        dune::cdm::overlay_1::StampType::ipAddress,
        dune::cdm::overlay_1::StampType::productInformation,
        dune::cdm::overlay_1::StampType::dateAndTime, 
        dune::cdm::overlay_1::StampType::date
    };

    for (std::vector<dune::cdm::overlay_1::StampType>::size_type i = 0; i < expectValues.size(); ++i)
    {
        EXPECT_EQ(expectValues[i], stampType_valid->getValidValues()[i]);
    }
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenGetStampTypeConstraintsIsCalledAndIfStampTypeOfStampTicketIsNone_ThenStampTypeOrderIsDefault)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"					\"scanJobConstraint\": {  "
"                        \"stampType\": [ "
"                            \"NONE\", "
"                            \"IP_ADDRESS\", "
"                            \"USER_NAME\", "
"                            \"PRODUCT_INFORMATION\", "
"                            \"PAGE_NUMBER\", "
"                            \"DATE_AND_TIME\", "
"                            \"DATE\" "
"                        ] "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    std::shared_ptr<Constraints> dynamicConstraints = dynamicConstraintRules->getStampTypeConstraints(dune::cdm::overlay_1::StampLocation::topLeft, ticket, dune::imaging::types::StampPolicy::NONE);

    EXPECT_TRUE(dynamicConstraints != nullptr);

    std::vector<IConstraint*> constraints = dynamicConstraints->getConstraints();
    IConstraint* validValue   = constraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampType>* stampType_valid = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampType>*>(validValue);
    
    std::vector<dune::cdm::overlay_1::StampType> expectValues = { 
        dune::cdm::overlay_1::StampType::none,
        dune::cdm::overlay_1::StampType::ipAddress,
        dune::cdm::overlay_1::StampType::userName,
        dune::cdm::overlay_1::StampType::productInformation,
        dune::cdm::overlay_1::StampType::pageNumber,
        dune::cdm::overlay_1::StampType::dateAndTime, 
        dune::cdm::overlay_1::StampType::date
    };

    for (std::vector<dune::cdm::overlay_1::StampType>::size_type i = 0; i < expectValues.size(); ++i)
    {
        EXPECT_EQ(expectValues[i], stampType_valid->getValidValues()[i]);
    }
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenGetConstraintsOnStampOptions_ThenValideValueIsCorrect)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"					\"scanJobConstraint\": {  "
"                        \"stampLocation\": [ "
"                            \"TOP_LEFT\", "
"                            \"TOP_CENTER\", "
"                            \"TOP_RIGHT\", "
"                            \"BOTTOM_LEFT\", "
"                            \"BOTTOM_CENTER\", "
"                            \"BOTTOM_RIGHT\" "
"                        ], "
"                        \"stampPolicy\": [ "
"                            \"NONE\", "
"                            \"ENFORCED\", "
"                            \"GUIDED\" "
"                        ], "
"                        \"stampType\": [ "
"                            \"NONE\", "
"                            \"ADMIN_DEFINED_1\", "
"                            \"ADMIN_DEFINED_2\", "
"                            \"ADMIN_DEFINED_3\", "
"                            \"IP_ADDRESS\", "
"                            \"USER_NAME\", "
"                            \"PRODUCT_INFORMATION\", "
"                            \"PAGE_NUMBER\", "
"                            \"DATE_AND_TIME\", "
"                            \"DATE\", "
"                            \"USER_DEFINED_1\", "
"                            \"USER_DEFINED_2\" "
"                        ], "
"                        \"stampTextColor\": [ "
"                            \"BLACK\", "
"                            \"BLUE\", "
"                            \"GREEN\", "
"                            \"PURPLE\", "
"                            \"RED\", "
"                            \"SKY_BLUE\", "
"                            \"YELLOW\" "
"                        ], "
"                        \"stampTextFont\": [ "
"                            \"ANTIQUE_OLIVE\", "
"                            \"CENTURY_SCHOOLBOOK\", "
"                            \"GARAMOND\", "
"                            \"LETTER_GOTHIC\" "
"                        ], "
"                        \"stampTextSize\": [ "
"                            \"EIGHT_POINT\", "
"                            \"TWELVE_POINT\", "
"                            \"TWENTY_POINT\" "
"                        ], "
"                        \"stampPageNumberingStyle\": [ "
"                            \"NUMBER\", "
"                            \"PAGE_PLUS_NUMBER\", "
"                            \"HYPHEN_NUMBER_HYPHEN\" "
"                        ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    dune::imaging::types::ScanStampLocationFbT stampLocation;
    std::vector<std::unique_ptr<dune::imaging::types::StampContentT>> stampContents{};
    auto contentFBT = std::make_unique<dune::imaging::types::StampContentT>();
    contentFBT->stampId = dune::imaging::types::StampType::NONE;
    stampContents.emplace_back(std::move(contentFBT));

    stampLocation.stampLocation = dune::imaging::types::StampLocation ::TOP_LEFT;
    stampLocation.stampContents = std::move(stampContents);

    ticket->getIntent()->setStampTopLeft(stampLocation);

    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    // ********************************************************
    // Test case 1, verify stamp location
    std::shared_ptr<Constraints>                                      dynamicConstraints    = dynamicConstraintRules->getStampLocationConstraints(dune::cdm::overlay_1::StampLocation::topLeft, ticket);
    std::vector<IConstraint*>                                         constraints           = dynamicConstraints->getConstraints();
    IConstraint*                                                      validModes            = constraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampLocation>*             validDudes            = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampLocation>*>(validModes);
    EXPECT_EQ(1, (int)validDudes->getValidValues().size());
    // ********************************************************

    // ********************************************************
    // Test case 2, verify stamp policy
    dynamicConstraints = dynamicConstraintRules->getStampPolicyConstraints(ticket);
    constraints        = dynamicConstraints->getConstraints();
    validModes         = constraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampPolicy>* valiPolicydDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampPolicy>*>(validModes);
    EXPECT_EQ(3, (int)valiPolicydDudes->getValidValues().size());
    // ********************************************************

    // ********************************************************
    // Test case 3, verify stamp type
    dynamicConstraints = dynamicConstraintRules->getStampTypeConstraints(dune::cdm::overlay_1::StampLocation::topLeft, ticket, dune::imaging::types::StampPolicy::NONE);
    constraints        = dynamicConstraints->getConstraints();
    validModes         = constraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampType>* validTypeDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampType>*>(validModes);
    EXPECT_EQ(12, (int)validTypeDudes->getValidValues().size());
    // ********************************************************

    // ********************************************************
    // Test case 4, verify stamp text color
    dynamicConstraints    = dynamicConstraintRules->getStampTextColorConstraints(ticket);
    constraints           = dynamicConstraints->getConstraints();
    validModes            = constraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextColor>* validTextColorDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextColor>*>(validModes);
    EXPECT_EQ(7, (int)validTextColorDudes->getValidValues().size());
    // ********************************************************

    // ********************************************************
    // Test case 5, verify stamp text font
    dynamicConstraints    = dynamicConstraintRules->getStampTextFontConstraints(ticket);
    constraints           = dynamicConstraints->getConstraints();
    validModes            = constraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextFont>* validTextFontDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextFont>*>(validModes);
    EXPECT_EQ(4, (int)validTextFontDudes->getValidValues().size());
    // ********************************************************

    // ********************************************************
    // Test case 6, verify stamp text size
    dynamicConstraints    = dynamicConstraintRules->getStampTextSizeConstraints(ticket);
    constraints           = dynamicConstraints->getConstraints();
    validModes            = constraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextSize>* validTextSizeDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextSize>*>(validModes);
    EXPECT_EQ(3, (int)validTextSizeDudes->getValidValues().size());
    // ********************************************************

    // ********************************************************
    // Test case 7, verify stamp page numbering style
    dynamicConstraints    = dynamicConstraintRules->getStampPageNumberingStyleConstraints(ticket);
    constraints           = dynamicConstraints->getConstraints();
    validModes            = constraints[1];
    ValidValuesEnum<dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle>* validPageNumberDudes = dynamic_cast<ValidValuesEnum<dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle>*>(validModes);
    EXPECT_EQ(3, (int)validPageNumberDudes->getValidValues().size());
    // ********************************************************
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenStampOptionShouldShow_checkIfConstraintIsSupportedReturnsTrue)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"					\"scanJobConstraint\": {  "
"                        \"stampLocation\": [ "
"                            \"TOP_LEFT\", "
"                            \"TOP_CENTER\", "
"                            \"TOP_RIGHT\", "
"                            \"BOTTOM_LEFT\", "
"                            \"BOTTOM_CENTER\", "
"                            \"BOTTOM_RIGHT\" "
"                        ], "
"                        \"stampPolicy\": [ "
"                            \"NONE\", "
"                            \"ENFORCED\", "
"                            \"GUIDED\" "
"                        ], "
"                        \"stampType\": [ "
"                            \"NONE\", "
"                            \"ADMIN_DEFINED_1\", "
"                            \"ADMIN_DEFINED_2\", "
"                            \"ADMIN_DEFINED_3\", "
"                            \"IP_ADDRESS\", "
"                            \"USER_NAME\", "
"                            \"PRODUCT_INFORMATION\", "
"                            \"PAGE_NUMBER\", "
"                            \"DATE_AND_TIME\", "
"                            \"DATE\", "
"                            \"USER_DEFINED_1\", "
"                            \"USER_DEFINED_2\" "
"                        ], "
"                        \"stampTextColor\": [ "
"                            \"BLACK\", "
"                            \"BLUE\", "
"                            \"GREEN\", "
"                            \"PURPLE\", "
"                            \"RED\", "
"                            \"SKY_BLUE\", "
"                            \"YELLOW\" "
"                        ], "
"                        \"stampTextFont\": [ "
"                            \"ANTIQUE_OLIVE\", "
"                            \"CENTURY_SCHOOLBOOK\", "
"                            \"GARAMOND\", "
"                            \"LETTER_GOTHIC\" "
"                        ], "
"                        \"stampTextSize\": [ "
"                            \"EIGHT_POINT\", "
"                            \"TWELVE_POINT\", "
"                            \"TWENTY_POINT\" "
"                        ], "
"                        \"stampStartingPageMin\": 1, "
"                        \"stampStartingPageMax\": 1000000, "
"                        \"stampStartingPageStep\": 1, "
"                        \"stampStartingNumberMin\": 1, "
"                        \"stampStartingNumberMax\": 1000000, "
"                        \"stampStartingNumberStep\": 1, "
"                        \"stampNumberOfDigitsMin\": 1, "
"                        \"stampNumberOfDigitsMax\": 10, "
"                        \"stampNumberOfDigitsStep\": 1, "
"                        \"stampPageNumberingStyle\": [ "
"                            \"NUMBER\", "
"                            \"PAGE_PLUS_NUMBER\", "
"                            \"HYPHEN_NUMBER_HYPHEN\" "
"                        ], "
"					} "
"				} "
;

    std::shared_ptr<MockICopyAdapter> mockICopyAdapter = std::make_shared<MockICopyAdapter>();
    ON_CALL(*mockICopyAdapter, getColorCopyEnabled()).WillByDefault(Return(true));

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);
    dynamicConstraintRules->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    dynamicConstraintRules->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter),"ICopyAdapter",mockICopyAdapter.get());

    std::future<void> asyncCompletion;
    dynamicConstraintRules->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // checkIfConstraintIsSupported tests
    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>  dynamicConstraints = dynamicConstraintRules->getDynamicConstraints(ticket,constraintsGroup);
    auto c = dynamicConstraints->getConstraints("pipelineOptions/stampTopLeft/locationId") ;
    EXPECT_NE(nullptr, c);
    c = dynamicConstraints->getConstraints("pipelineOptions/stampTopLeft/policy") ;
    EXPECT_NE(nullptr, c);
    c = dynamicConstraints->getConstraints("pipelineOptions/stampTopLeft/stampContent/stampId") ;
    EXPECT_NE(nullptr, c);
    c = dynamicConstraints->getConstraints("pipelineOptions/stampTopLeft/textColor") ;
    EXPECT_NE(nullptr, c);
    c = dynamicConstraints->getConstraints("pipelineOptions/stampTopLeft/textFont") ;
    EXPECT_NE(nullptr, c);
    c = dynamicConstraints->getConstraints("pipelineOptions/stampTopLeft/textSize") ;
    EXPECT_NE(nullptr, c);
    c = dynamicConstraints->getConstraints("pipelineOptions/stampTopLeft/pageNumberingStyle") ;
    EXPECT_NE(nullptr, c);
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenOptionShouldShow_checkIfConstraintIsSupportedReturnsTrue)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"mediaSupportedSize\": [ "
"                        { "
"                            \"size\":{ \"id\":\"LETTER\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"size\":{ \"id\":\"LEGAL\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						{ \"size\":{ \"id\":\"PHOTO5X8\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"					], "
"					\"mediaSupportedType\": [ "
"                        { "
"                            \"type\":{ \"id\":\"STATIONERY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ], "
"                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
"                        } "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
"                        \"scanPagesFlipUpEnabled\": [ false, true ], "
"                        \"minScanExposure\": 1, "
"                        \"maxScanExposure\": 9, "
"                        \"stepScanExposure\": 1.0, "
"                        \"minScalePercent\": 25, "
"                        \"maxScalePercent\": 400, "
"                        \"step\":1.0, "
"                        \"adfResolutions\" : [75, 150, 200, 300], "
"                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
"						\"adfOriginalSizes\":[ "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LEGAL\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"US_EXECUTIVE\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"FOOLSCAP\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"						], "
"						\"flatbedOriginalSizes\":[ "
"                            { "
"                                \"id\":\"ANY\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"LETTER\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"US_EXECUTIVE\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"PHOTO4X6\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            }, "
"                            { "
"                                \"id\":\"PHOTO5X8\", "
"                                \"mediaOrientation\":\"PORTRAIT\" "
"                            } "
"						] "
"					} "
"				} "
;
    //testing::internal::CaptureStdout();

    std::shared_ptr<MockICopyAdapter> mockICopyAdapter = std::make_shared<MockICopyAdapter>();
    ON_CALL(*mockICopyAdapter, getColorCopyEnabled()).WillByDefault(Return(true));

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);
    const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);
    dynamicConstraintRules->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    dynamicConstraintRules->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter),"ICopyAdapter",mockICopyAdapter.get());

    std::future<void> asyncCompletion;
    dynamicConstraintRules->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // checkIfConstraintIsSupported tests
    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>  dynamicConstraints = dynamicConstraintRules->getDynamicConstraints(ticket,constraintsGroup);
    auto c = dynamicConstraints->getConstraints("dest/print/colorMode") ;
    EXPECT_EQ(nullptr, c);
    c = dynamicConstraints->getConstraints("src/scan/colorMode") ;
    EXPECT_NE(nullptr, c);
    c = dynamicConstraints->getConstraints("dest/print/plexMode") ;
    EXPECT_NE(nullptr, c);
    c = dynamicConstraints->getConstraints("dest/print/printMargins") ;
    EXPECT_EQ(nullptr, c);
    c = dynamicConstraints->getConstraints("dest/print/mediaSource") ;
    EXPECT_NE(nullptr, c);
    c = dynamicConstraints->getConstraints("dest/print/mediaSize") ;
    EXPECT_NE(nullptr, c);

    //std::string output = testing::internal::GetCapturedStdout();
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenupdateOrientationConstraintsIsCalled_withoutFinisher_ThenTheConstraintsAreUpdated)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    auto constraintGroup = std::make_shared<ConstraintsGroup>();
    auto constraints = std::make_shared<Constraints>();

    auto possibleOption = std::vector<dune::cdm::glossary_1::ContentOrientation>();
    auto validOption = std::vector<dune::cdm::glossary_1::ContentOrientation>();

    possibleOption.push_back(dune::cdm::glossary_1::ContentOrientation::portrait);
    possibleOption.push_back(dune::cdm::glossary_1::ContentOrientation::landscape);

    validOption.push_back(dune::cdm::glossary_1::ContentOrientation::portrait);
    validOption.push_back(dune::cdm::glossary_1::ContentOrientation::landscape);

    // As far as I know, we wouldn't disable any of these content types, but I could be wrong.
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::ContentOrientation>>(possibleOption, &dune::cdm::glossary_1::ContentOrientation::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::ContentOrientation>>(validOption, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    constraintGroup->set("src/scan/contentOrientation", constraints);         


       const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();

    dune::print::engine::MockIMedia mockIMedia;
    //ensure mediaInterface not null
    ticket->setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket->getMediaInterface() != NULL);
    IMedia::InputList inputs;
    inputs.push_back(mockIMediaIInput);
    EXPECT_CALL(mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillRepeatedly(Return(std::make_tuple(APIResult::OK, inputs)));

    dynamicConstraintRules->updateScanContentOrientationConstraints(constraintGroup, ticket);

}

TEST_F(GivenANewCopyJobDynamicConstraintRulesStandard, WhenupdateOrientationConstraintsIsCalled_withFinisher_ThenTheConstraintsAreUpdated)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    auto constraintGroup = std::make_shared<ConstraintsGroup>();
    auto constraints = std::make_shared<Constraints>();

    auto possibleOption = std::vector<dune::cdm::glossary_1::ContentOrientation>();
    auto validOption = std::vector<dune::cdm::glossary_1::ContentOrientation>();

    possibleOption.push_back(dune::cdm::glossary_1::ContentOrientation::portrait);
    possibleOption.push_back(dune::cdm::glossary_1::ContentOrientation::landscape);

    validOption.push_back(dune::cdm::glossary_1::ContentOrientation::portrait);
    validOption.push_back(dune::cdm::glossary_1::ContentOrientation::landscape);

    // As far as I know, we wouldn't disable any of these content types, but I could be wrong.
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::ContentOrientation>>(possibleOption, &dune::cdm::glossary_1::ContentOrientation::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::ContentOrientation>>(validOption, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    constraintGroup->set("src/scan/contentOrientation", constraints);         

       const char* componentName = "test";
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules =
         std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();

    dune::print::engine::MockIMedia* mockIMedia = new dune::print::engine::MockIMedia();
    //ensure mediaInterface not null
    ticket->setMediaInterface(mockIMedia);
    EXPECT_TRUE(ticket->getMediaInterface() != NULL);
    IMedia::InputList inputs;
    inputs.push_back(mockIMediaIInput);
    EXPECT_CALL(*mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillRepeatedly(Return(std::make_tuple(APIResult::OK, inputs)));

    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock1_;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher *) {} ) // stapling
    };

    const std::vector<dune::imaging::types::MediaDestinationId> allPossibleDestinationsList_ = {
        dune::imaging::types::MediaDestinationId::OUTPUTBIN1,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN2,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN3
    };

    ON_CALL(*mockIMedia, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, pageBasedFinishers)));

    IMedia::PageBasedFinisherPtr pageBasedFinisherPtr = IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher * p){} );

    ON_CALL(pageBasedFinisherMock1_, getType()).WillByDefault(Return(dune::print::engine::FinisherType::PAGEBASED_FINISHER));

    dynamicConstraintRules->updateScanContentOrientationConstraints(constraintGroup, ticket);

    delete mockIMedia;
}

struct ScanCaptureModeTestParams {
    dune::imaging::types::Plex plexMode;
    dune::imaging::types::MediaSizeId mediaSizeId;
    int expectedValidValuesSize;
    std::vector<dune::cdm::jobTicket_1::ScanCaptureMode> expectedValidValues;
    dune::imaging::types::CopyOutputNumberUpCount pagesPerSheet;
};

class CopyJobDynamicConstraintRulesStandardTest : public ::testing::TestWithParam<ScanCaptureModeTestParams>{
protected:
    void SetUp() override {
        ticket = std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

        std::string jsonConstraints =
        "				{ "
        "                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
        "                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
        "                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
        "                    \"minCopies\": 1, "
        "                    \"maxCopies\": 999, "
        "                    \"stepCopies\": 1.0, "
        "                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
        "                    \"mediaSupportedSize\": [ "
        "                        { "
        "                            \"size\":{ \"id\":\"LETTER\" }, "
        "                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
        "                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
        "                        }, "
        "                        { "
        "                            \"size\":{ \"id\":\"LEGAL\" }, "
        "                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
        "                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
        "                        }, "
        "					], "
        "					\"mediaSupportedType\": [ "
        "                        { "
        "                            \"type\":{ \"id\":\"STATIONERY\" }, "
        "                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
        "                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
        "                            \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ] "
        "                        }, "
        "                        { "
        "                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
        "                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
        "                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
        "                            \"colorMode\": [ \"COLOR\" ] "
        "                        }, "
        "                        { "
        "                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
        "                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
        "                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ], "
        "                            \"colorMode\": [ \"GRAYSCALE\" ] "
        "                        }, "
        "						{ "
        "                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
        "                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
        "                            \"duplex\": [ \"SIMPLEX\" ], "
        "                            \"colorMode\": [ ] "
        "                        }, "
        "					], "
        "					\"scanJobConstraint\": {  "
        "                        \"scanCaptureModes\": [ \"STANDARD\", \"BOOKMODE\" , \"IDCARD\" ], "
        "                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
        "                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
        "                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
        "                        \"scanPagesFlipUpEnabled\": [ false, true ], "
        "                        \"minScanExposure\": 1, "
        "                        \"maxScanExposure\": 9, "
        "                        \"stepScanExposure\": 1.0, "
        "                        \"minScalePercent\": 25, "
        "                        \"maxScalePercent\": 400, "
        "                        \"step\":1.0, "
        "                        \"adfResolutions\" : [75, 150, 200, 300], "
        "                        \"flatbedResolutions\" : [75, 150, 200, 300, 400, 600], "
        "                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"FULLPAGE\", \"LEGALTOLETTER\", \"A4TOLETTER\", \"LETTERTOA4\" ], "
        "					} "
        "				} "
        ;
        std::shared_ptr<CopyJobConstraintsFbT> tableT;
        bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
        EXPECT_EQ(ok, true);
        ticket->setConstraintsFromFb(tableT);

        EXPECT_EQ(2,(int) ticket->getConstraints()->getColorMode().size());

        const char* componentName = "test";
        dynamicConstraintRules = std::make_shared<CopyJobDynamicConstraintRulesStandard>(componentName);
    }

    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket;
    std::shared_ptr<CopyJobDynamicConstraintRulesStandard> dynamicConstraintRules;
};

TEST_P(CopyJobDynamicConstraintRulesStandardTest, WhenScanCaptureModeIsCahnged_ConstraintAppliedCorrectly) {
    const ScanCaptureModeTestParams& params = GetParam();

    ticket->getIntent()->setInputPlexMode(params.plexMode);
    ticket->getIntent()->setInputMediaSizeId(params.mediaSizeId);
    ticket->getIntent()->setPagesPerSheet(params.pagesPerSheet);

    std::shared_ptr<Constraints> ScanCaptureModeConstraints = dynamicConstraintRules->getScanCaptureModeConstraints(ticket);
    std::vector<IConstraint*> theScanCaptureModeConstraints = ScanCaptureModeConstraints->getConstraints();
    IConstraint* validModes = theScanCaptureModeConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::ScanCaptureMode>* validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::jobTicket_1::ScanCaptureMode>*>(validModes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(params.expectedValidValuesSize, (int)validDudes->getValidValues().size());

    for (size_t i = 0; i < params.expectedValidValues.size(); ++i) {
        EXPECT_EQ(params.expectedValidValues[i], validDudes->getValidValues()[i]);
    }
}

INSTANTIATE_TEST_CASE_P(
    CopyJobDynamicConstraintRulesStandardTests,
    CopyJobDynamicConstraintRulesStandardTest,
    ::testing::Values(
        ScanCaptureModeTestParams{dune::imaging::types::Plex::SIMPLEX, dune::imaging::types::MediaSizeId::LETTER, 3, {dune::cdm::jobTicket_1::ScanCaptureMode::standard, dune::cdm::jobTicket_1::ScanCaptureMode::bookMode, dune::cdm::jobTicket_1::ScanCaptureMode::idCard}, dune::imaging::types::CopyOutputNumberUpCount::OneUp},
        ScanCaptureModeTestParams{dune::imaging::types::Plex::SIMPLEX, dune::imaging::types::MediaSizeId::A5, 3, {dune::cdm::jobTicket_1::ScanCaptureMode::standard, dune::cdm::jobTicket_1::ScanCaptureMode::bookMode, dune::cdm::jobTicket_1::ScanCaptureMode::idCard}, dune::imaging::types::CopyOutputNumberUpCount::OneUp},
        ScanCaptureModeTestParams{dune::imaging::types::Plex::DUPLEX, dune::imaging::types::MediaSizeId::A4, 2, {dune::cdm::jobTicket_1::ScanCaptureMode::standard, dune::cdm::jobTicket_1::ScanCaptureMode::idCard}, dune::imaging::types::CopyOutputNumberUpCount::OneUp},
        ScanCaptureModeTestParams{dune::imaging::types::Plex::SIMPLEX, dune::imaging::types::MediaSizeId::LETTER, 2, {dune::cdm::jobTicket_1::ScanCaptureMode::standard, dune::cdm::jobTicket_1::ScanCaptureMode::bookMode}, dune::imaging::types::CopyOutputNumberUpCount::TwoUp}
    )
);


class GivenForceSets : public ::testing::Test
{
};


/*
  test cases:
// case 1
    dest.print.printQuality = 'best'
    src.scan.source = 'flatbed'
        Test(src.scan.resolution == 600dpi )

// case 2
    dest.print.printQuality = 'normal'
    src.scan.source = 'flatbed'
        Test(src.scan.resolution == 300dpi )

// case 3
    dest.print.printQuality = 'draft'
    src.scan.source = 'flatbed'
        Test(src.scan.resolution == 300dpi )

// case 4
    src.scan.source = 'adf'
        Test(src.scan.resolution == 300dpi )

// case 5
    dest.print.printQuality = 'best'
        Test(src.scan.resolution == 300dpi )

// case 6
    src.scan.source = 'flatbed'
        Test(src.scan.resolution == 600dpi )
*/
TEST_F(GivenForceSets, WhenSettingPrintQuality_ThenScanResolutionIsUpdatedCorrectly)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    auto patchTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    patchTable->beginMergePatch();
    patchTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    // setup patch object
    //ticket->getIntent()->setScanSource(dune::cdm::glossary_1::ScanMediaSourceId::adf);
    patchTable->dest = dune::cdm::jobTicket_1::jobTicket::DestTable();
    patchTable->dest.getMutable()->print = dune::cdm::jobTicket_1::PrintTable();
    patchTable->src = dune::cdm::jobTicket_1::jobTicket::SrcTable();
    patchTable->src.getMutable()->scan = dune::cdm::jobTicket_1::ScanTable();

    // case 1
    patchTable->dest.getMutable()->print.getMutable()->printQuality = dune::cdm::glossary_1::PrintQuality::best;
    patchTable->src.getMutable()->scan.getMutable()->mediaSource =  dune::cdm::glossary_1::ScanMediaSourceId::flatbed;
    ForceSets::checkAndApplyPrintQualityForceSets(patchTable, ticket);
    EXPECT_EQ(patchTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e600Dpi);
    ticket->getIntent()->setOutputXResolution( dune::imaging::types::Resolution::E600DPI);// update the ticket without calling the ticketAdapter stuff

    // case 2
    patchTable->dest.getMutable()->print.getMutable()->printQuality = dune::cdm::glossary_1::PrintQuality::normal;
    patchTable->src.getMutable()->scan.getMutable()->mediaSource =  dune::cdm::glossary_1::ScanMediaSourceId::flatbed;
    ForceSets::checkAndApplyPrintQualityForceSets(patchTable, ticket);
    EXPECT_EQ(patchTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e300Dpi);
    ticket->getIntent()->setOutputXResolution( dune::imaging::types::Resolution::E300DPI);// update the ticket without calling the ticketAdapter stuff

    // case 3
    patchTable->dest.getMutable()->print.getMutable()->printQuality = dune::cdm::glossary_1::PrintQuality::draft;
    patchTable->src.getMutable()->scan.getMutable()->mediaSource =  dune::cdm::glossary_1::ScanMediaSourceId::flatbed;
    ForceSets::checkAndApplyPrintQualityForceSets(patchTable, ticket);
    EXPECT_EQ(patchTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e300Dpi);
    ticket->getIntent()->setOutputXResolution( dune::imaging::types::Resolution::E300DPI);// update the ticket without calling the ticketAdapter stuff

    // case 4
    patchTable->src.getMutable()->scan.getMutable()->mediaSource =  dune::cdm::glossary_1::ScanMediaSourceId::adf;
    ForceSets::checkAndApplyPrintQualityForceSets(patchTable, ticket);
    EXPECT_EQ(patchTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e300Dpi);
    ticket->getIntent()->setOutputXResolution( dune::imaging::types::Resolution::E300DPI);// update the ticket without calling the ticketAdapter stuff

    // case 5
    patchTable->dest.getMutable()->print.getMutable()->printQuality = dune::cdm::glossary_1::PrintQuality::best;
    ForceSets::checkAndApplyPrintQualityForceSets(patchTable, ticket);
    EXPECT_EQ(patchTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e300Dpi);
    ticket->getIntent()->setOutputXResolution( dune::imaging::types::Resolution::E300DPI);// update the ticket without calling the ticketAdapter stuff

    // case 6
    patchTable->src.getMutable()->scan.getMutable()->mediaSource =  dune::cdm::glossary_1::ScanMediaSourceId::flatbed;
    ForceSets::checkAndApplyPrintQualityForceSets(patchTable, ticket);
    EXPECT_EQ(patchTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e600Dpi);
    ticket->getIntent()->setOutputXResolution( dune::imaging::types::Resolution::E600DPI);// update the ticket without calling the ticketAdapter stuff
}

TEST_F(GivenForceSets, WhenFlatbedIsEnabled_MixedOriginalSizeChangedToAnyByForceset)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);
    ticket->setPrePrintConfiguration(Product::ENTERPRISE);

    auto updatedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    updatedJobTicketTable->beginMergePatch();
    updatedJobTicketTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    updatedJobTicketTable->src = dune::cdm::jobTicket_1::jobTicket::SrcTable();
    updatedJobTicketTable->src.getMutable()->scan = dune::cdm::jobTicket_1::ScanTable();
    updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSource = dune::cdm::glossary_1::ScanMediaSourceId::flatbed;
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL);
    //updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSize = dune::cdm::glossary_1::MediaSize::com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_legal;

    ForceSets::checkAndApplyScanMediaSourceForceSets(updatedJobTicketTable, ticket);

    dune::cdm::glossary_1::MediaSize originalsizeState = updatedJobTicketTable->src.get()->scan.get()->mediaSize.get();
    EXPECT_EQ(dune::cdm::glossary_1::MediaSize::any, originalsizeState);
}

TEST_F(GivenForceSets, WhenSetToAdfAndAny_ForcesetNotReflectedIfEnterpriseModel)
{
    //Set the prePrintConfiguration of copyjobticket to Enterprise.
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);
    ticket->setPrePrintConfiguration(Product::ENTERPRISE);
    //auto prePrintConfiguration = ticket->getPrePrintConfiguration();
    auto updatedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();

    //Perform a deserialize and verify that the force set is not performed.
    updatedJobTicketTable->src = dune::cdm::jobTicket_1::jobTicket::SrcTable();
    updatedJobTicketTable->src.getMutable()->scan = dune::cdm::jobTicket_1::ScanTable();
    updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSource = dune::cdm::glossary_1::ScanMediaSourceId::adf;
    updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSize = dune::cdm::glossary_1::MediaSize::any;
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);

    ForceSets::checkAndApplyScanMediaSourceForceSets(updatedJobTicketTable, ticket);

    dune::cdm::glossary_1::MediaSize originalsizeState = updatedJobTicketTable->src.get()->scan.get()->mediaSize.get();
    EXPECT_EQ(dune::cdm::glossary_1::MediaSize::any, originalsizeState);
}

TEST_F(GivenForceSets, WhenSetToAdfAndAny_ForcesetAppliedForNonEnterpriseModel)
{
    auto mockIScannerCapabilities = std::make_shared<MockIScannerCapabilities>();

    ON_CALL(*mockIScannerCapabilities, hasDuplexSupport(_)).WillByDefault(DoAll(SetArgReferee<0>(false), Return(dune::framework::core::APIResult::OK)));

    //Set the prePrintConfiguration of copyjobticket to Enterprise.
    auto ticket = std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);
    ticket->setPrePrintConfiguration(Product::HOME_PRO);
    ticket->setScanCapabilitiesInterface(mockIScannerCapabilities.get());
    ticket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);

    auto updatedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();

    //Perform a deserialize and verify that the force set is not performed.
    updatedJobTicketTable->src = dune::cdm::jobTicket_1::jobTicket::SrcTable();
    updatedJobTicketTable->src.getMutable()->scan = dune::cdm::jobTicket_1::ScanTable();
    updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSource = dune::cdm::glossary_1::ScanMediaSourceId::adf;
    updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSize = dune::cdm::glossary_1::MediaSize::any;
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);

    ForceSets::checkAndApplyScanMediaSourceForceSets(updatedJobTicketTable, ticket);

    dune::cdm::glossary_1::PlexMode originalPlexState = updatedJobTicketTable->src.get()->scan.get()->plexMode.get();
    EXPECT_EQ(dune::cdm::glossary_1::PlexMode::simplex, originalPlexState);
    dune::cdm::glossary_1::MediaSize originalsizeState = updatedJobTicketTable->src.get()->scan.get()->mediaSize.get();
    EXPECT_EQ(dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in, originalsizeState);
}


TEST_F(GivenForceSets, WhenCollateIsOn_ThenSettingTwoPagesPerSheetIsOff)
{
    // Add a print table to the patch.
    auto patchTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    patchTable->dest = dune::cdm::jobTicket_1::jobTicket::DestTable();
    patchTable->dest.getMutable()->print = dune::cdm::jobTicket_1::PrintTable();

    // Set collate on.
    patchTable->dest.getMutable()->print.getMutable()->collate = dune::cdm::jobTicket_1::CollateModes::collated;

    // Verify two pages per sheet is forced off.
    ForceSets::checkAndApplyTwoPagesPerSheetForceSets(patchTable,  dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH);
    ASSERT_NE(patchTable->pipelineOptions.get(), nullptr);
    ASSERT_NE(patchTable->pipelineOptions.get()->imageModifications.get(), nullptr);
    EXPECT_EQ(patchTable->pipelineOptions.get()->imageModifications.get()->pagesPerSheet.get(), dune::cdm::jobTicket_1::PagesPerSheet::oneUp);
}

TEST_F(GivenForceSets, WhenSettingTwoPagesPerSheet_ThenCollateIsOff)
{
    // Add an imageModifications table to the patch.
    auto patchTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    patchTable->pipelineOptions = dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable();
    patchTable->pipelineOptions.getMutable()->imageModifications = dune::cdm::jobTicket_1::ImageModificationsTable();

    // Set two pages per sheet.
    patchTable->pipelineOptions.getMutable()->imageModifications.getMutable()->pagesPerSheet = dune::cdm::jobTicket_1::PagesPerSheet::twoUp;

    // Verify collate is forced off.
    ForceSets::checkAndApplyTwoPagesPerSheetForceSets(patchTable,  dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH);
    ASSERT_NE(patchTable->dest.get(), nullptr);
    ASSERT_NE(patchTable->dest.get()->print.get(), nullptr);
    EXPECT_EQ(patchTable->dest.get()->print.get()->collate.get(), dune::cdm::jobTicket_1::CollateModes::uncollated);
}


TEST_F(GivenForceSets, WhenSettingOnePagesPerSheet_ThenCollateIsOn)
{
    // Add an imageModifications table to the patch.
    auto patchTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    patchTable->pipelineOptions = dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable();
    patchTable->pipelineOptions.getMutable()->imageModifications = dune::cdm::jobTicket_1::ImageModificationsTable();

    // Set two pages per sheet.
    patchTable->pipelineOptions.getMutable()->imageModifications.getMutable()->pagesPerSheet = dune::cdm::jobTicket_1::PagesPerSheet::oneUp;

    // Verify collate is forced on.
    ForceSets::checkAndApplyTwoPagesPerSheetForceSets(patchTable,  dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH);
    ASSERT_NE(patchTable->dest.get(), nullptr);
    ASSERT_NE(patchTable->dest.get()->print.get(), nullptr);
    EXPECT_EQ(patchTable->dest.get()->print.get()->collate.get(), dune::cdm::jobTicket_1::CollateModes::collated);
}

TEST_F(GivenForceSets, WhenSettingScanModes_ScanConstraintsCheckAndApplyForceSetsCalled)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);
    dune::scan::MockIScanConstraints*  mockIScanConstraints = new dune::scan::MockIScanConstraints();
    auto constraintsGroup = std::make_shared<ConstraintsGroup>();

    ON_CALL(*mockIScanConstraints, checkAndApplyScanForceSets(_, _, _)).WillByDefault(Return(true));

    auto patchTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    patchTable->beginMergePatch();
    patchTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    ticket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    ticket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    ticket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    ticket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LEGAL);

    // setup patch object
    patchTable->dest = dune::cdm::jobTicket_1::jobTicket::DestTable();
    patchTable->dest.getMutable()->print = dune::cdm::jobTicket_1::PrintTable();
    patchTable->src = dune::cdm::jobTicket_1::jobTicket::SrcTable();
    patchTable->src.getMutable()->scan = dune::cdm::jobTicket_1::ScanTable();

    patchTable->src.getMutable()->scan.getMutable()->scanCaptureMode =  dune::cdm::jobTicket_1::ScanCaptureMode::bookMode;
    ForceSets::checkAndApplyForceSets(patchTable, ticket, constraintsGroup, mockIScanConstraints);
    delete mockIScanConstraints;
}

