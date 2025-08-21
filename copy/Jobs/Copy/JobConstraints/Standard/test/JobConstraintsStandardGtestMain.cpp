/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobConstraintsStandardGtestMain.cpp
 * @date   Tue, 05 Jul 2022 08:29:10 +0200
 * @brief  Component used to manage the Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include <limits>

#include "JobConstraintsStandard.h"
#include "JobConstraintsStandardGtestMain_TraceAutogen.h"
#include "CopyJobTicket.h"
#include "CopyJobStaticConstraintRules.h"
#include "CopyTicketAdapter.h"
#include "flatbuffers/flatbuffers.h"
#include "flatbuffers/idl.h"
#include "flatbuffers/util.h"
#include "flatbuffers/reflection.h"
#include "flatbuffers/minireflect.h"
#include "CopyJobConstraints_generated.h"
#include "SecurityContexts.h"
#include "SecurityContextImpl.h"
#include "FoldingStyle_generated.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "TestSystemServices.h"
#include "GTestConfigHelper.h"
#include "MockICopyJobDynamicConstraintRules.h"
#include "MockIScanConstraints.h"
#include "MockSecurityContexts.h"
#include "MockICopyAdapter.h"
#include "MockIMedia.h"
#include "MockICopyJobTicket.h"
#include "ICopyJobDynamicConstraintRules.h"
#include "MockIJobServiceFactory.h"
#include "MockIPageBasedFinisher.h"

using JobConstraintsStandard              = dune::copy::Jobs::Copy::JobConstraintsStandard;
using TestSystemServices    = dune::framework::component::TestingUtil::TestSystemServices;
using IComponent            = dune::framework::component::IComponent;
using IComponentManager     = dune::framework::component::IComponentManager;
using SystemServices        = dune::framework::component::SystemServices;
using SysTrace              = dune::framework::core::dbg::SysTrace;
using CheckpointLevel       = SysTrace::CheckpointLevel;
using CopyJobConstraintsFb = dune::copy::Jobs::Copy::CopyJobConstraintsFb;
using MockICopyJobDynamicConstraintRules = dune::copy::Jobs::Copy::MockICopyJobDynamicConstraintRules;
using ICopyJobDynamicConstraintRules = dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules;
using IMedia = dune::print::engine::IMedia;
using MockIMediaIInput = dune::print::engine::MockIMediaIInput;
using MockIScanConstraints = dune::scan::MockIScanConstraints;

using GTestConfigHelper     = dune::framework::core::gtest::GTestConfigHelper;
using namespace dune::copy::Jobs::Copy;
using namespace ::testing;

GTestConfigHelper testConfigOptions_;

bool loadCopyJobConstraintsFbT(
   std::shared_ptr<CopyJobConstraintsFbT>& tableT,
   const std::string& pathToResources,
   const std::string& loadedFbsSchema,
   const std::string& jsonDataString)
{
   bool resultOp = true;
   flatbuffers::Parser parser;
   std::string path1 = ".";
   std::string path2 = pathToResources;
   const char* includePaths[] = {
       (const char*)path1.c_str(),
       (const char*)path2.c_str(),
       nullptr
   };

   std::string schemafile;
   std::string schemaPath = "testResources/" + loadedFbsSchema;
   resultOp = flatbuffers::LoadFile(schemaPath.c_str(), false, &schemafile);

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
// class GivenANewJobConstraintsStandardMediaPrintSupportedSize : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////
class GivenANewJobConstraintsStandardMediaPrintSupportedSize : public ::testing::Test
{
    public:
        GivenANewJobConstraintsStandardMediaPrintSupportedSize() : component_(nullptr), systemServices_(nullptr), componentManager_(nullptr) {};

        virtual void SetUp() override;

        virtual void TearDown() override;

    protected:

        dune::copy::Jobs::Copy::JobConstraintsStandard *component_;
        TestSystemServices                             *systemServices_;
        dune::framework::component::IComponentManager  *componentManager_;
};

void GivenANewJobConstraintsStandardMediaPrintSupportedSize::SetUp()
{
    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobConstraintsStandardConfig.fbs", "./testResources/JobConstraintsStandardMediaPrintSupportedSizeTestData.json");

    component_ = new JobConstraintsStandard("myInstance");
    ASSERT_TRUE(component_ != nullptr);
}

void GivenANewJobConstraintsStandardMediaPrintSupportedSize::TearDown()
{
    delete component_;
    delete systemServices_;
}

TEST_F(GivenANewJobConstraintsStandardMediaPrintSupportedSize, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_);

    std::shared_ptr<CopyJobConstraintsFbT> constraints = component_->getFbConstraintsTableFromConfiguration();

    ASSERT_TRUE(constraints != nullptr); // constraints should not be null if the component is initialized.
}

TEST_F(GivenANewJobConstraintsStandardMediaPrintSupportedSize, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    IComponent * comp = static_cast<IComponent*>(component_);
    MockIScanConstraints mockScanConstraints_;
    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    MockICopyJobDynamicConstraintRules mockDynamicConstraintRules;
    comp->setInterface(GET_INTERFACE_UID(ICopyJobDynamicConstraintRules), "", &mockDynamicConstraintRules);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints", &mockScanConstraints_);

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    ASSERT_FALSE(asyncCompletion.valid());

    // Get the Flatbuffer constraints
    std::shared_ptr<CopyJobConstraintsFbT> constraints = component_->getFbConstraintsTableFromConfiguration();

    assert(constraints);

    // Randomly check on a constraint
    ASSERT_EQ(constraints->plexMode[0], dune::imaging::types::Plex::SIMPLEX);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedJobConstraintsStandardMediaPrintSupportedSize : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////
class GivenAConnectedJobConstraintsStandardMediaPrintSupportedSize : public GivenANewJobConstraintsStandardMediaPrintSupportedSize
{
    public:
        GivenAConnectedJobConstraintsStandardMediaPrintSupportedSize() {};

        virtual void SetUp() override;

        virtual void TearDown() override;

    protected:
        MockICopyJobDynamicConstraintRules mockDynamicConstraints;
        MockIScanConstraints mockScanConstraints_;
};

void GivenAConnectedJobConstraintsStandardMediaPrintSupportedSize::SetUp()
{
    GivenANewJobConstraintsStandardMediaPrintSupportedSize::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->setInterface(GET_INTERFACE_UID(ICopyJobDynamicConstraintRules), "", &mockDynamicConstraints);

    
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints", &mockScanConstraints_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

void GivenAConnectedJobConstraintsStandardMediaPrintSupportedSize::TearDown()
{
    GivenANewJobConstraintsStandardMediaPrintSupportedSize::TearDown();
}

TEST_F(GivenAConnectedJobConstraintsStandardMediaPrintSupportedSize, WhenGetConstraintsFromConfigurationIsCalled_TheConstraintsObtainedAreCorrect)
{
    // Get the Flatbuffer constraints
    std::shared_ptr<CopyJobConstraintsFbT> constraints = component_->getFbConstraintsTableFromConfiguration();

    assert(constraints);

    ASSERT_EQ(constraints->plexMode[0], dune::imaging::types::Plex::SIMPLEX);
    ASSERT_EQ(constraints->plexBinding[0], dune::imaging::types::PlexBinding::ONE_SIDED);
    ASSERT_EQ(constraints->minCopies, 1);
    ASSERT_EQ(constraints->maxCopies, 99);
    ASSERT_EQ(constraints->mediaPrintSupportedSize[0], dune::imaging::types::MediaSizeId::ANY);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenANewJobConstraintsStandard : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenANewJobConstraintsStandard : public ::testing::Test
{
public:

    GivenANewJobConstraintsStandard() : component_(nullptr), systemServices_(nullptr), componentManager_(nullptr) {};
    virtual void SetUp() override;
    virtual void TearDown() override;

    std::string getGeneralConstraintJsonWithoutMainBrackets();
    std::string getGeneralConstraintJson();

protected:

    dune::copy::Jobs::Copy::JobConstraintsStandard                          * component_;
    TestSystemServices                              * systemServices_;
    dune::framework::component::IComponentManager   * componentManager_;
    MockIScanConstraints mockScanConstraints_;
};

void GivenANewJobConstraintsStandard::SetUp()
{
    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobConstraintsStandardConfig.fbs", "./testResources/JobConstraintsStandardTestData.json");

    component_ = new JobConstraintsStandard("myInstance");
    ASSERT_TRUE(component_ != nullptr);

    component_->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints", &mockScanConstraints_);
}

void GivenANewJobConstraintsStandard::TearDown()
{
    delete component_;
    delete systemServices_;
}

std::string GivenANewJobConstraintsStandard::getGeneralConstraintJsonWithoutMainBrackets()
{
    return "                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
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
        "					}";
}

std::string GivenANewJobConstraintsStandard::getGeneralConstraintJson()
{
    return "{ " + getGeneralConstraintJsonWithoutMainBrackets() +" } ";
}

TEST_F(GivenANewJobConstraintsStandard, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_);

    ASSERT_TRUE(true);
}

TEST_F(GivenANewJobConstraintsStandard, WhenGetConstraintsFromConfigurationIsCalled_ThePlexModeConstraintsisAvailable)
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
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
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
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT = component_->getFbConstraintsTableFromConfiguration();
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    // Check if the plex mode Valid value of the job ticket is configured as [Simplex, Duplex].
    auto staticPlexModeConstraints = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getPlexModeConstraints(ticket);
    std::vector<IConstraint*>                      ThePlexModeConstraints = staticPlexModeConstraints->getConstraints();
    IConstraint*                                   validModes             = ThePlexModeConstraints[1];
    ValidValuesEnum<dune::cdm::glossary_1::PlexMode>* validDudes          = static_cast<ValidValuesEnum<dune::cdm::glossary_1::PlexMode>*>(validModes);
    EXPECT_EQ(2, (int)validDudes->getValidValues().size());
}

TEST_F(GivenANewJobConstraintsStandard, WhenGetConstraintsFromConfigurationIsCalled_ThenConstraintsAreAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints =
"				{ "
"                    \"plexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                    \"plexBinding\": [ \"ONE_SIDED\", \"LONG_EDGE\", \"SHORT_EDGE\" ], "
"                    \"collate\": [ \"Collate\", \"Uncollate\" ], "
"                    \"copyMargins\":[ \"CLIPCONTENT\", \"ADDTOCONTENT\" ], "
"                    \"minCopies\": 1, "
"                    \"maxCopies\": 999, "
"                    \"stepCopies\": 1.0, "
"                    \"printQuality\": [ \"DRAFT\", \"NORMAL\", \"BEST\" ], "
"                    \"printingOrder\": [ \"FIRST_PAGE_ON_TOP\", \"LAST_PAGE_ON_TOP\" ], "
"                    \"minRotation\": 0, "
"                    \"maxRotation\": 270, "
"                    \"stepRotation\": 90, "
"                    \"mediaFamily\": [ \"ADHESIVE\", \"BACKLIT\", \"BANNERANDSIGN\", \"BONDANDCOATED\", \"BLUEPRINT\",  "
"                    \"CANVAS\", \"CUSTOM\", \"FILM\", \"HEATTRANSFER\", \"PLAIN\", \"PHOTO\", \"TECHNICAL\", \"TEXTILE\", \"WALLCOVERING\", \"UNKNOWN\" ],"
"                    \"autoRotate\": [ false, true], "
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
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
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
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT = component_->getFbConstraintsTableFromConfiguration();
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket->setConstraintsFromFb(tableT);

    // Check if the printing Order Valid value of the job ticket is configured as [FIRST_PAGE_ON_TOP, LAST_PAGE_ON_TOP].
    auto staticPrintingOrderConstraints = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getPrintingOrderConstraints(ticket);
    std::vector<IConstraint*>                               ThePrintingOrderConstraints  = staticPrintingOrderConstraints->getConstraints();
    IConstraint*                                            validModesPrintingOrder      = ThePrintingOrderConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::PrintingOrder>* validDudesPrintingOrder      = static_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PrintingOrder>*>(validModesPrintingOrder);
    EXPECT_EQ(2, (int)validDudesPrintingOrder->getValidValues().size());

    // Check if the MediaFamily Valid value of the job ticket is configured correctly.
    auto                      staticMediaFamilyConstraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getMediaFamilyConstraints(ticket);
    std::vector<IConstraint*> TheMediaFamilyConstraints     = staticMediaFamilyConstraints->getConstraints();
    IConstraint*              validModesMediaFamily         = TheMediaFamilyConstraints[1];
    ValidValuesEnum<dune::cdm::mediaProfile_1::MediaFamily>* validDudesMediaFamily = static_cast<ValidValuesEnum<dune::cdm::mediaProfile_1::MediaFamily>*>(validModesMediaFamily);
    EXPECT_EQ(15, (int)validDudesMediaFamily->getValidValues().size());

    // Check if the Rotate Valid value of the job ticket is configured correctly.
    auto                      staticRotateConstraints = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getRotateConstraints(ticket);
    std::vector<IConstraint*> TheRotateConstraints    = staticRotateConstraints->getConstraints();
    IConstraint*              validModesRotate        = TheRotateConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::Rotate>* validDudesRotate = static_cast<ValidValuesEnum<dune::cdm::jobTicket_1::Rotate>*>(validModesRotate);
    EXPECT_EQ(5,   (int)validDudesRotate->getValidValues().size());

    // Check if the copy margins Valid value of the job ticket is configured correctly.
    auto                      staticCopyMarginConstraints = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getCopyMarginsConstraints(ticket);
    std::vector<IConstraint*> TheCopyMarginConstraints    = staticCopyMarginConstraints->getConstraints();
    IConstraint*              validCopyMargins            = TheCopyMarginConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::PrintMargins>* validDudesCopyMargins = static_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PrintMargins>*>(validCopyMargins);
    EXPECT_EQ(2,   (int)validDudesCopyMargins->getValidValues().size());
}


TEST_F(GivenANewJobConstraintsStandard, WhenGetOutputPrintMediaConstraintsIsCalledWithFinisherAvailable_ThenConstraintsAreAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();

    std::vector<dune::cdm::glossary_1::MediaDestinationId> outputBins {
        dune::cdm::glossary_1::MediaDestinationId::tray_dash_1,
        dune::cdm::glossary_1::MediaDestinationId::tray_dash_2,
        dune::cdm::glossary_1::MediaDestinationId::tray_dash_3
    };

    ON_CALL(*ticket, IsInstalledPageBasedFinisherDevice()).WillByDefault(Return(true));
    ON_CALL(*ticket, getPossibleOutputBins()).WillByDefault(Return(std::make_tuple(APIResult::OK, outputBins)));
    ON_CALL(*ticket, getValidOutputBins()).WillByDefault(Return(std::make_tuple(APIResult::OK, outputBins)));

    // Check if the StapleOption Valid value of the job ticket is configured correctly.
    auto                      staticOutputPrintMediaConstraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getOutputPrintMediaConstraints(ticket);
    std::vector<IConstraint*> TheOutputPrintMediaConstraints     = staticOutputPrintMediaConstraints->getConstraints();
    IConstraint*              validOutputPrintMediaOptions       = TheOutputPrintMediaConstraints[1];
    ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>* validDudesOutputPrintMedia = static_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>(validOutputPrintMediaOptions);
    EXPECT_EQ(3, (int)validDudesOutputPrintMedia->getValidValues().size());
}


TEST_F(GivenANewJobConstraintsStandard, WhenGetOutputPrintMediaConstraintsIsCalledWithNoFinisherAvailable_ThenConstraintsAreAvailable)
{

    // The realTicket is only used by the mockTicket ON_CALL() to get the constraints.
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> realTicket =
        std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints ="{ " + getGeneralConstraintJsonWithoutMainBrackets() +
                                 ", \"mediaPrintSupportedDestinations\": [ \"STANDARDBIN\" ], }";

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_TRUE(ok);
    realTicket->setConstraintsFromFb(tableT);

    // This mockTicket is passed to the CUT.
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket> mockTicket =
            std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();

    std::vector<dune::imaging::types::MediaDestinationId> outputList {
        dune::imaging::types::MediaDestinationId::STANDARDBIN,
    };

    ON_CALL(*mockTicket, IsInstalledPageBasedFinisherDevice()).WillByDefault(Return(false));
    ON_CALL(*mockTicket, getOutputList()).WillByDefault(Return(std::make_tuple(APIResult::OK, outputList)));
    ON_CALL(*mockTicket, getConstraints()).WillByDefault(Return(realTicket->getConstraints()));

    auto constraints = CopyJobStaticConstraintRules::getFoldingStyleIdConstraints(mockTicket);

    // Check if the StapleOption Valid value of the job ticket is configured correctly.
    auto                      staticOutputPrintMediaConstraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getOutputPrintMediaConstraints(mockTicket);
    std::vector<IConstraint*> TheOutputPrintMediaConstraints     = staticOutputPrintMediaConstraints->getConstraints();
    IConstraint*              validOutputPrintMediaOptions       = TheOutputPrintMediaConstraints[1];
    ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>* validDudesOutputPrintMedia = static_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>(validOutputPrintMediaOptions);
    EXPECT_EQ(1, (int)validDudesOutputPrintMedia->getValidValues().size());
}

TEST_F(GivenANewJobConstraintsStandard, WhenGetOutputPrintMediaConstraintsIsCalledWithNoFinisherAvailable_ThenPossibleValuesOrderMustBeTheDefinedInJobConstraints)
{

    // The realTicket is only used by the mockTicket ON_CALL() to get the constraints.
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> realTicket =
        std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints ="{ " + getGeneralConstraintJsonWithoutMainBrackets() +
                                 ", \"mediaPrintSupportedDestinations\": [ \"STACKER\",\"BIN\",\"FOLDER\" ] }";

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_TRUE(ok);
    realTicket->setConstraintsFromFb(tableT);

    // This mockTicket is passed to the CUT.
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket> mockTicket =
            std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();

    std::vector<dune::imaging::types::MediaDestinationId> outputList {
        dune::imaging::types::MediaDestinationId::BIN,
        dune::imaging::types::MediaDestinationId::STACKER
    };

    ON_CALL(*mockTicket, IsInstalledPageBasedFinisherDevice()).WillByDefault(Return(false));
    ON_CALL(*mockTicket, getOutputList()).WillByDefault(Return(std::make_tuple(APIResult::OK, outputList)));
    ON_CALL(*mockTicket, getConstraints()).WillByDefault(Return(realTicket->getConstraints()));

    // Check if the StapleOption Valid value of the job ticket is configured correctly.
    auto                      staticOutputPrintMediaConstraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getOutputPrintMediaConstraints(mockTicket);
    std::vector<IConstraint*> TheOutputPrintMediaConstraints     = staticOutputPrintMediaConstraints->getConstraints();
    IConstraint*              possibleOutputPrintMediaOptions    = TheOutputPrintMediaConstraints[0];
    PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>* possibleDudesOutputPrintMedia = static_cast<PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>(possibleOutputPrintMediaOptions);
    EXPECT_EQ(2, (int)possibleDudesOutputPrintMedia->getPossibleValues().size());
    EXPECT_EQ( "bin",(std::string)possibleDudesOutputPrintMedia->getPossibleValues().back());
    EXPECT_EQ( "stacker-1",(std::string)possibleDudesOutputPrintMedia->getPossibleValues().front());
}

TEST_F(GivenANewJobConstraintsStandard, WhenGetOutputPrintMediaConstraintsIsCalledWithNoconstraints_ThenPossibleAndValidValuesAreDefault)
{
    // The realTicket is only used by the mockTicket ON_CALL() to get the constraints.
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> realTicket =
        std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    auto ok = loadCopyJobConstraintsFbT(tableT, 
        "./testResources",
        "CopyJobConstraints.fbs", 
        "{ " + getGeneralConstraintJsonWithoutMainBrackets() + ", }");
    ASSERT_TRUE(ok);
    realTicket->setConstraintsFromFb(tableT);

    // This mockTicket is passed to the CUT.
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket> mockTicket = 
        std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();

    std::vector<dune::imaging::types::MediaDestinationId> outputList {};
    ON_CALL(*mockTicket, IsInstalledPageBasedFinisherDevice()).WillByDefault(Return(false));
    ON_CALL(*mockTicket, getOutputList()).WillByDefault(Return(std::make_tuple(APIResult::OK, outputList)));
    ON_CALL(*mockTicket, getConstraints()).WillByDefault(Return(realTicket->getConstraints()));

    auto staticOutputPrintMediaConstraints = 
        dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getOutputPrintMediaConstraints(mockTicket);
    auto outputPrintMediaConstraints = staticOutputPrintMediaConstraints->getConstraints();
    auto possibleDudesOutputPrintMedia = 
        static_cast<PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>(outputPrintMediaConstraints[0]);
    auto validDudesOutputPrintMedia = 
        static_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>(outputPrintMediaConstraints[1]);

    EXPECT_EQ(1, (int)possibleDudesOutputPrintMedia->getPossibleValues().size());
    EXPECT_EQ( "default",(std::string)possibleDudesOutputPrintMedia->getPossibleValues().front());
    EXPECT_EQ(1, (int)validDudesOutputPrintMedia->getValidValues().size());
    EXPECT_EQ( "default",(std::string)validDudesOutputPrintMedia->getValidValues().front());
}

TEST_F(GivenANewJobConstraintsStandard, WhenGetOutputPrintMediaConstraintsIsCalledWithNoconstraintsAndMediaSettingDefault_ThenPossibleAndValidValuesAreMediaSettingDefault)
{
    // The realTicket is only used by the mockTicket ON_CALL() to get the constraints.
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> realTicket =
        std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    auto ok = loadCopyJobConstraintsFbT(tableT, 
        "./testResources",
        "CopyJobConstraints.fbs", 
        "{ " + getGeneralConstraintJsonWithoutMainBrackets() + ", }");
    ASSERT_TRUE(ok);
    realTicket->setConstraintsFromFb(tableT);

    // This mockTicket is passed to the CUT.
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket> mockTicket = 
        std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();

    std::vector<dune::imaging::types::MediaDestinationId> outputList {};
    ON_CALL(*mockTicket, IsInstalledPageBasedFinisherDevice()).WillByDefault(Return(false));
    ON_CALL(*mockTicket, getOutputList()).WillByDefault(Return(std::make_tuple(APIResult::OK, outputList)));
    ON_CALL(*mockTicket, getConstraints()).WillByDefault(Return(realTicket->getConstraints()));

    auto staticOutputPrintMediaConstraints = 
        dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getOutputPrintMediaConstraints(mockTicket, dune::imaging::types::MediaDestinationId::STACKER);
    auto outputPrintMediaConstraints = staticOutputPrintMediaConstraints->getConstraints();
    auto possibleDudesOutputPrintMedia = 
        static_cast<PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>(outputPrintMediaConstraints[0]);
    auto validDudesOutputPrintMedia = 
        static_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>(outputPrintMediaConstraints[1]);

    EXPECT_EQ(1, (int)possibleDudesOutputPrintMedia->getPossibleValues().size());
    EXPECT_EQ( "stacker-1",(std::string)possibleDudesOutputPrintMedia->getPossibleValues().front());
    EXPECT_EQ(1, (int)validDudesOutputPrintMedia->getValidValues().size());
    EXPECT_EQ( "stacker-1",(std::string)validDudesOutputPrintMedia->getValidValues().front());
}

TEST_F(GivenANewJobConstraintsStandard, WhengGetStapleOptionConstraintsIsCalled_ThenConstraintsAreAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    //ticket->getIntent()->setStapleOption(dune::imaging::types::TOP_LEFT_ONE_POINT_ANGLED);
    ticket->getIntent()->setPunchOption(dune::imaging::types::PunchingOptions::NONE);

    dune::print::engine::MockIMedia mockIMedia;
    //ensure mediaInterface not null
    ticket->setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket->getMediaInterface() != NULL);

    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock1_;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher *) {} ) // stapling
    };

    const std::vector<dune::imaging::types::MediaDestinationId> allPossibleDestinationsList_ = {
        dune::imaging::types::MediaDestinationId::OUTPUTBIN1,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN2,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN3
    };

    ON_CALL(mockIMedia, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, pageBasedFinishers)));

    std::tuple<APIResult, std::vector<dune::imaging::types::MediaProcessingTypes>> mediaProcessingTypes{APIResult::OK, {dune::imaging::types::MediaProcessingTypes::STAPLE}};
    IMedia::PageBasedFinisherPtr pageBasedFinisherPtr = IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher * p){} );

    /** Stapling */
    ON_CALL(pageBasedFinisherMock1_, getType())
        .WillByDefault(Return(dune::print::engine::FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock1_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[0]));
    ON_CALL(pageBasedFinisherMock1_, getMediaProcessingTypes())
        .WillByDefault(ReturnRef(mediaProcessingTypes));

    // Check if the StapleOption Valid value of the job ticket is configured correctly.
    auto                      staticStapleConstraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getStapleOptionConstraints(ticket);
    std::vector<IConstraint*> TheStapleConstraints     = staticStapleConstraints->getConstraints();
    IConstraint*              validStapleOptions        = TheStapleConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::StapleOptions>* validDudesStaple = static_cast<ValidValuesEnum<dune::cdm::jobTicket_1::StapleOptions>*>(validStapleOptions);
    EXPECT_NE(0, (int)validDudesStaple->getValidValues().size());
}

TEST_F(GivenANewJobConstraintsStandard, WhengGetPunchOptionConstraintsIsCalled_ThenConstraintsAreAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    //ticket->getIntent()->setStapleOption(dune::imaging::types::TOP_LEFT_ONE_POINT_ANGLED);
    ticket->getIntent()->setPunchOption(dune::imaging::types::PunchingOptions::NONE);

    dune::print::engine::MockIMedia mockIMedia;
    //ensure mediaInterface not null
    ticket->setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket->getMediaInterface() != NULL);

    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock1_, pageBasedFinisherMock2_, pageBasedFinisherMock3_;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher *) {} ), // stapling
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock2_, [](IMedia::IPageBasedFinisher *) {} ), // stapling  & Punching
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock3_, [](IMedia::IPageBasedFinisher *) {} ) // punching
    };

    const std::vector<dune::imaging::types::MediaDestinationId> allPossibleDestinationsList_ = {
        dune::imaging::types::MediaDestinationId::OUTPUTBIN1,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN2,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN3
    };

    ON_CALL(mockIMedia, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, pageBasedFinishers)));

    /** Stapling */
    ON_CALL(pageBasedFinisherMock1_, getType())
        .WillByDefault(Return(dune::print::engine::FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock1_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[0]));

    // Check if the StapleOption Valid value of the job ticket is configured correctly.
    auto                      staticPunchConstraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getPunchOptionConstraints(ticket);
    std::vector<IConstraint*> ThePunchConstraints     = staticPunchConstraints->getConstraints();
    IConstraint*              validPunchOptions        = ThePunchConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::PunchOptions>* validDudesPunch = static_cast<ValidValuesEnum<dune::cdm::jobTicket_1::PunchOptions>*>(validPunchOptions);
    EXPECT_NE(0, (int)validDudesPunch->getValidValues().size());
}

TEST_F(GivenANewJobConstraintsStandard, WhengGetFoldOptionConstraintsIsCalled_ThenConstraintsAreAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    //ticket->getIntent()->setStapleOption(dune::imaging::types::TOP_LEFT_ONE_POINT_ANGLED);
    //ticket->getIntent()->setPunchOption(dune::imaging::types::PunchingOptions::NONE);

    dune::print::engine::MockIMedia mockIMedia;
    //ensure mediaInterface not null
    ticket->setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket->getMediaInterface() != NULL);

    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock1_, pageBasedFinisherMock2_, pageBasedFinisherMock3_;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher *) {} ), // stapling
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock2_, [](IMedia::IPageBasedFinisher *) {} ), // stapling  & Punching
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock3_, [](IMedia::IPageBasedFinisher *) {} ) // punching
    };

    const std::vector<dune::imaging::types::MediaDestinationId> allPossibleDestinationsList_ = {
        dune::imaging::types::MediaDestinationId::OUTPUTBIN1,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN2,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN3
    };

    ON_CALL(mockIMedia, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, pageBasedFinishers)));

    /** Stapling */
    ON_CALL(pageBasedFinisherMock1_, getType())
        .WillByDefault(Return(dune::print::engine::FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock1_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[0]));

    // Check if the StapleOption Valid value of the job ticket is configured correctly.
    auto                      staticFoldConstraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getFoldOptionConstraints(ticket);
    std::vector<IConstraint*> TheFoldConstraints     = staticFoldConstraints->getConstraints();
    IConstraint*              validFoldOptions        = TheFoldConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::FoldOptions>* validDudesFold = static_cast<ValidValuesEnum<dune::cdm::jobTicket_1::FoldOptions>*>(validFoldOptions);
    EXPECT_NE(0, (int)validDudesFold->getValidValues().size());
}

TEST_F(GivenANewJobConstraintsStandard, WhenIsStampEnabledIsCalledAndStampContentsAreNotNone_ThenReturnIsTrue)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    dune::imaging::types::ScanStampLocationFbT stampTopLeftLocation;
    std::vector<std::unique_ptr<dune::imaging::types::StampContentT>> stampTopLeftContents{};
    auto contentFBT1 = std::make_unique<dune::imaging::types::StampContentT>();

    contentFBT1->stampId = dune::imaging::types::StampType::NONE;
    stampTopLeftContents.emplace_back(std::move(contentFBT1));

    stampTopLeftLocation.stampLocation = dune::imaging::types::StampLocation::TOP_LEFT;
    stampTopLeftLocation.stampContents = std::move(stampTopLeftContents);

    ticket->getIntent()->setStampTopLeft(stampTopLeftLocation);

    dune::imaging::types::ScanStampLocationFbT stampBottomLeftLocation;
    std::vector<std::unique_ptr<dune::imaging::types::StampContentT>> stampBottomLeftContents{};
    auto contentFBT2 = std::make_unique<dune::imaging::types::StampContentT>();

    contentFBT2->stampId = dune::imaging::types::StampType::IP_ADDRESS;
    stampBottomLeftContents.emplace_back(std::move(contentFBT2));

    stampBottomLeftLocation.stampLocation = dune::imaging::types::StampLocation::BOTTOM_LEFT;
    stampBottomLeftLocation.stampContents = std::move(stampBottomLeftContents);

    ticket->getIntent()->setStampBottomLeft(stampBottomLeftLocation);

    auto isStampEnabled  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::isStampEnabled(ticket);
    EXPECT_EQ(true, isStampEnabled);
}

TEST_F(GivenANewJobConstraintsStandard, WhenIsStampEnabledIsCalledAndStampContentsAreNone_ThenReturnIsFalse)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    dune::imaging::types::ScanStampLocationFbT stampTopLeftLocation;
    std::vector<std::unique_ptr<dune::imaging::types::StampContentT>> stampTopLeftContents{};
    auto contentFBT1 = std::make_unique<dune::imaging::types::StampContentT>();

    contentFBT1->stampId = dune::imaging::types::StampType::NONE;
    stampTopLeftContents.emplace_back(std::move(contentFBT1));

    stampTopLeftLocation.stampLocation = dune::imaging::types::StampLocation ::TOP_LEFT;
    stampTopLeftLocation.stampContents = std::move(stampTopLeftContents);

    ticket->getIntent()->setStampTopLeft(stampTopLeftLocation);

    dune::imaging::types::ScanStampLocationFbT stampBottomLeftLocation;
    std::vector<std::unique_ptr<dune::imaging::types::StampContentT>> stampBottomLeftContents{};
    auto contentFBT2 = std::make_unique<dune::imaging::types::StampContentT>();

    contentFBT2->stampId = dune::imaging::types::StampType::NONE;
    stampBottomLeftContents.emplace_back(std::move(contentFBT2));

    stampBottomLeftLocation.stampLocation = dune::imaging::types::StampLocation ::TOP_LEFT;
    stampBottomLeftLocation.stampContents = std::move(stampBottomLeftContents);

    ticket->getIntent()->setStampBottomLeft(stampBottomLeftLocation);

    auto isStampEnabled  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::isStampEnabled(ticket);
    EXPECT_EQ(false, isStampEnabled);
}

TEST_F(GivenANewJobConstraintsStandard, WhenIsStampEnabledIsCalledAndStampPolicyIsNotNone_ThenReturnIsTrue)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    dune::imaging::types::ScanStampLocationFbT stampTopLeftLocation;
    stampTopLeftLocation.stampLocation = dune::imaging::types::StampLocation::TOP_LEFT;
    stampTopLeftLocation.stampPolicy = dune::imaging::types::StampPolicy::GUIDED;

    ticket->getIntent()->setStampTopLeft(stampTopLeftLocation);

    dune::imaging::types::ScanStampLocationFbT stampBottomLeftLocation;
    stampBottomLeftLocation.stampLocation = dune::imaging::types::StampLocation::BOTTOM_LEFT;
    stampBottomLeftLocation.stampPolicy = dune::imaging::types::StampPolicy::GUIDED;

    ticket->getIntent()->setStampBottomLeft(stampBottomLeftLocation);

    auto isStampEnabled  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::isStampEnabled(ticket);
    EXPECT_EQ(true, isStampEnabled);
}

TEST_F(GivenANewJobConstraintsStandard, WhenIsStampEnabledIsCalledAndStampPolicyIsNone_ThenReturnIsTrue)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    dune::imaging::types::ScanStampLocationFbT stampTopLeftLocation;
    stampTopLeftLocation.stampLocation = dune::imaging::types::StampLocation::TOP_LEFT;
    stampTopLeftLocation.stampPolicy = dune::imaging::types::StampPolicy::NONE;

    ticket->getIntent()->setStampTopLeft(stampTopLeftLocation);

    dune::imaging::types::ScanStampLocationFbT stampBottomLeftLocation;
    stampBottomLeftLocation.stampLocation = dune::imaging::types::StampLocation::BOTTOM_LEFT;
    stampBottomLeftLocation.stampPolicy = dune::imaging::types::StampPolicy::NONE;

    ticket->getIntent()->setStampBottomLeft(stampBottomLeftLocation);

    auto isStampEnabled  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::isStampEnabled(ticket);
    EXPECT_EQ(false, isStampEnabled);
}

TEST_F(GivenANewJobConstraintsStandard, WhenStampIsEnabledAndGetFoldOptionConstraintsIsCalled_ThenConstraintsIsLock)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    dune::imaging::types::ScanStampLocationFbT stampLocation;
    std::vector<std::unique_ptr<dune::imaging::types::StampContentT>> stampContents{};
    auto contentFBT = std::make_unique<dune::imaging::types::StampContentT>();

    contentFBT->stampId = dune::imaging::types::StampType::IP_ADDRESS;
    stampContents.emplace_back(std::move(contentFBT));

    stampLocation.stampLocation = dune::imaging::types::StampLocation ::TOP_LEFT;
    stampLocation.stampContents = std::move(stampContents);

    ticket->getIntent()->setStampTopLeft(stampLocation);

    // Check fold constraint is locked when stamp is enabled
    auto staticFoldConstraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getFoldOptionConstraints(ticket);
    bool locked = false;
    for(auto &constraint : staticFoldConstraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::LOCK)
        {
            locked = true;
        }
    }
    EXPECT_EQ(true, locked);
}

TEST_F(GivenANewJobConstraintsStandard, WhengGetBookletMakerOptionConstraintsIsCalled_ThenConstraintsAreAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    //ticket->getIntent()->setStapleOption(dune::imaging::types::TOP_LEFT_ONE_POINT_ANGLED);
    //ticket->getIntent()->setPunchOption(dune::imaging::types::PunchingOptions::NONE);

    dune::print::engine::MockIMedia mockIMedia;
    //ensure mediaInterface not null
    ticket->setMediaInterface(&mockIMedia);
    EXPECT_TRUE(ticket->getMediaInterface() != NULL);

    dune::print::engine::MockIPageBasedFinisher pageBasedFinisherMock1_, pageBasedFinisherMock2_, pageBasedFinisherMock3_;

    const IMedia::FinisherList pageBasedFinishers = {
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock1_, [](IMedia::IPageBasedFinisher *) {} ), // stapling
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock2_, [](IMedia::IPageBasedFinisher *) {} ), // stapling  & Punching
        IMedia::PageBasedFinisherPtr(&pageBasedFinisherMock3_, [](IMedia::IPageBasedFinisher *) {} ) // punching
    };

    const std::vector<dune::imaging::types::MediaDestinationId> allPossibleDestinationsList_ = {
        dune::imaging::types::MediaDestinationId::OUTPUTBIN1,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN2,
        dune::imaging::types::MediaDestinationId::OUTPUTBIN3
    };

    ON_CALL(mockIMedia, getFinisherDevices(_))
        .WillByDefault(Return(std::make_tuple(APIResult::OK, pageBasedFinishers)));

    /** Stapling */
    ON_CALL(pageBasedFinisherMock1_, getType())
        .WillByDefault(Return(dune::print::engine::FinisherType::PAGEBASED_FINISHER));
    ON_CALL(pageBasedFinisherMock1_, getMediaDestinationId())
        .WillByDefault(Return(allPossibleDestinationsList_[0]));

    // Check if the StapleOption Valid value of the job ticket is configured correctly.
    auto                      staticBookletMakerConstraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getBookletMakerOptionConstraints(ticket);
    std::vector<IConstraint*> TheBookletMakerConstraints     = staticBookletMakerConstraints->getConstraints();
    IConstraint*              validBookletMakerOptions        = TheBookletMakerConstraints[1];
    ValidValuesEnum<dune::cdm::jobTicket_1::BookletMakerOptions>* validDudesBookletMaker = static_cast<ValidValuesEnum<dune::cdm::jobTicket_1::BookletMakerOptions>*>(validBookletMakerOptions);
    EXPECT_NE(0, (int)validDudesBookletMaker->getValidValues().size());
}

TEST_F(GivenANewJobConstraintsStandard, WhengGetJobOffsetConstraintsIsCalled_ThenConstraintsAreAvailable)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket = 
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    auto constraints  = dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getJobOffsetConstraints(ticket);
    auto validValuefalse = dune::cdm::glossary_1::FeatureEnabled::false_;
    auto validValuetrue = dune::cdm::glossary_1::FeatureEnabled::true_;

    bool validateRet = constraints->tryValidate(&validValuefalse);
    EXPECT_TRUE(validateRet);
    validateRet = constraints->tryValidate(&validValuetrue);
    EXPECT_TRUE(validateRet);
}


TEST_F(GivenANewJobConstraintsStandard, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    MockICopyJobDynamicConstraintRules mockDynamicConstraintRules;
    comp->setInterface(GET_INTERFACE_UID(ICopyJobDynamicConstraintRules), "", &mockDynamicConstraintRules);
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    ASSERT_TRUE(true);
}

TEST_F(GivenANewJobConstraintsStandard, WhenGettingFoldingStyleIdConstraints_ThenOnlyZeroIsValid)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
        std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    short validValue = 1;
    short invalidNegativeValue = -1;
    short invalidValueZero = 0;

    std::string jsonConstraints ="{ " + getGeneralConstraintJsonWithoutMainBrackets() +", \"foldingStyleIds\":["
        + std::to_string(validValue)+"] }";

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_TRUE(ok);
    ticket->setConstraintsFromFb(tableT);

    auto constraints = CopyJobStaticConstraintRules::getFoldingStyleIdConstraints(ticket);

    bool validateRet = constraints->tryValidate(&validValue);
    EXPECT_TRUE(validateRet);
    validateRet = constraints->tryValidate(&invalidNegativeValue);
    EXPECT_FALSE(validateRet);
    validateRet = constraints->tryValidate(&invalidValueZero);
    EXPECT_FALSE(validateRet);
}

TEST_F(GivenANewJobConstraintsStandard, WhenGettingFoldingStyleIdConstraintHasLimitValues_ThenValuesIsValid)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
        std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    auto minValueExpected = std::numeric_limits<short>::min();
    auto maxValueExpected = std::numeric_limits<short>::max();

    std::string jsonConstraints ="{ " + getGeneralConstraintJsonWithoutMainBrackets() +", \"foldingStyleIds\": ["+
        std::to_string(minValueExpected)+","+ std::to_string(maxValueExpected)+"] } ";

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_TRUE(ok);
    ticket->setConstraintsFromFb(tableT);
    auto constraints = CopyJobStaticConstraintRules::getFoldingStyleIdConstraints(ticket);

    // Validate limits values
    bool validateRet = constraints->tryValidate(&minValueExpected);
    EXPECT_TRUE(validateRet);
    validateRet = constraints->tryValidate(&maxValueExpected);
    EXPECT_TRUE(validateRet);
}

TEST_F(GivenANewJobConstraintsStandard, WhenGettingFoldingStyleIdConstraintsWithoutConstraintsFromJson_ThenOnlyUndefinedZeroValueIsValid)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
        std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints = getGeneralConstraintJson();

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_TRUE(ok);
    ticket->setConstraintsFromFb(tableT);

    short validValue = static_cast<short>(dune::imaging::types::FoldingStyle::UNDEFINED);
    short invalidValue = 1;
    auto constraints = CopyJobStaticConstraintRules::getFoldingStyleIdConstraints(ticket);

    bool validateRet = constraints->tryValidate(&validValue);
    EXPECT_TRUE(validateRet);
    validateRet = constraints->tryValidate(&invalidValue);
    EXPECT_FALSE(validateRet);
}

TEST_F(GivenANewJobConstraintsStandard, WhenGettingFoldingStyleIdConstraintsWithoutConstraintsFromJson_ThenCheckThatLimitShortValidateAsZero)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket =
        std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(nullptr);

    std::string jsonConstraints = getGeneralConstraintJson();

    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_TRUE(ok);
    ticket->setConstraintsFromFb(tableT);
    auto constraints = CopyJobStaticConstraintRules::getFoldingStyleIdConstraints(ticket);

    // Validate limits values
    short invalidMinValue = std::numeric_limits<short>::min();
    short invalidMaxValue = std::numeric_limits<short>::max();
    bool validateRet = constraints->tryValidate(&invalidMinValue);
    EXPECT_FALSE(validateRet);
    validateRet = constraints->tryValidate(&invalidMaxValue);
    EXPECT_FALSE(validateRet);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedJobConstraintsStandard : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedJobConstraintsStandard :public GivenANewJobConstraintsStandard
{
  public:

    GivenAConnectedJobConstraintsStandard() {};

    virtual void SetUp() override;

    virtual void TearDown() override;
    protected:
        MockICopyJobDynamicConstraintRules mockDynamicConstraints_;
        MockIScanConstraints mockScanConstraints_;
        std::shared_ptr<ConstraintsGroup> constraintsGroup_;
        std::shared_ptr<dune::scan::Jobs::Scan::IScanJobConstraints> constraintFromJobService;
        std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> intentFromJobService;
};

void GivenAConnectedJobConstraintsStandard::SetUp()
{
    GivenANewJobConstraintsStandard::SetUp();

    constraintsGroup_ = std::make_shared<ConstraintsGroup>();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->setInterface(GET_INTERFACE_UID(ICopyJobDynamicConstraintRules), "", &mockDynamicConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints", &mockScanConstraints_);

    ON_CALL(mockScanConstraints_, getScanConstraints(_, _)).WillByDefault(
        Invoke([&](std::shared_ptr<dune::scan::Jobs::Scan::IScanJobConstraints> constraints, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> intent) {
            constraintFromJobService = constraints;
            intentFromJobService = intent;
            return constraintsGroup_;
        })
    );

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

}

void GivenAConnectedJobConstraintsStandard::TearDown()
{
    GivenANewJobConstraintsStandard::TearDown();
}

TEST_F(GivenAConnectedJobConstraintsStandard, WhenGetConstraintsFromConfigurationIsCalled_TheConstraintsShouldHaveCustomMediaXYFeedDimention)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket1 =
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
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"USER_DEFINED_1\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }  "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
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
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"LEGALTOLETTER\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket1->setConstraintsFromFb(tableT);

    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(*(ticket1.get()));

    ticket->setPrePrintConfiguration(Product::ENTERPRISE);
    ticket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    MockIJobServiceFactory<MockICopyJobTicket>* mockIJobService;
    CopyTicketAdapter*                          copyTicketAdapter;

    mockIJobService   = new MockIJobServiceFactory<MockICopyJobTicket>();
    copyTicketAdapter = new dune::copy::Jobs::Copy::CopyTicketAdapter(ticket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService);

    // Call Test method
    auto constraintsGroup = component_->getConstraints(ticket, *copyTicketAdapter);

    // Check result
    auto constraints = constraintsGroup->getAllConstraints();
    bool foundCustomMediaXFeedDimension{false};
    bool foundCustomMediaYFeedDimension{false};
    
    for ( auto &constraint : constraints )
    {
        CHECKPOINTB("constraintsGroup %s", (constraint.first).c_str());
        if (constraint.first == "dest/print/customMediaXFeedDimension")
        {
            foundCustomMediaXFeedDimension = true;
        }
        if (constraint.first == "dest/print/customMediaYFeedDimension")
        {
            foundCustomMediaYFeedDimension = true;
        }
    }

    EXPECT_TRUE(foundCustomMediaXFeedDimension);
    EXPECT_TRUE(foundCustomMediaYFeedDimension);

    delete(mockIJobService);
    delete(copyTicketAdapter);
}

TEST_F(GivenAConnectedJobConstraintsStandard, WhenGetConstraintsFromConfigurationIsCalled_ThenScanConstraintShouldHaveMediaSourceIdAdded)
{
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicket> ticket1 =
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
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"USER_DEFINED_1\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }  "
"					], "
"					\"scanJobConstraint\": {  "
"                        \"inputPlexMode\": [ \"SIMPLEX\", \"DUPLEX\" ], "
"                        \"colorMode\": [ \"COLOR\", \"GRAYSCALE\" ], "
"                        \"originalContentType\": [ \"TEXT\", \"PHOTO\", \"MIXED\" ], "
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
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"LEGALTOLETTER\" ], "
"					} "
"				} "
;
    std::shared_ptr<CopyJobConstraintsFbT> tableT;
    bool ok = loadCopyJobConstraintsFbT(tableT, "./testResources", "CopyJobConstraints.fbs", jsonConstraints);
    EXPECT_EQ(ok, true);
    ticket1->setConstraintsFromFb(tableT);

    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket =
            std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(*(ticket1.get()));

    ticket->setPrePrintConfiguration(Product::ENTERPRISE);
    std::shared_ptr<dune::print::engine::MockIMediaIInputTray> mockIMediaIInputTray;
    mockIMediaIInputTray = std::make_shared<dune::print::engine::MockIMediaIInputTray>();
    std::shared_ptr<const dune::print::engine::MockIMediaIInputTray> cMockIMediaIInputTray;
    cMockIMediaIInputTray = std::make_shared<const dune::print::engine::MockIMediaIInputTray>();
    auto traySnapshot = std::make_shared<IMedia::InputTraySnapshot>(cMockIMediaIInputTray);

    dune::print::engine::MockIMedia* mockIMedia;
    mockIMedia = new dune::print::engine::MockIMedia();
    ticket->setMediaInterface(mockIMedia);
    EXPECT_TRUE(ticket->getMediaInterface() != NULL);

    std::shared_ptr<dune::print::engine::MockIMediaIInput> mockIMediaIInput;
    mockIMediaIInput = std::make_shared<dune::print::engine::MockIMediaIInput>();
    IMedia::InputList inputs{mockIMediaIInput};
    ON_CALL(*mockIMediaIInput, getType()).WillByDefault(Return(dune::print::engine::InputType::TRAY));
    ON_CALL(*mockIMediaIInput, getTray()).WillByDefault(Return(mockIMediaIInputTray));
    ON_CALL(*mockIMediaIInputTray, getSnapShot()).WillByDefault(Return(std::make_tuple(APIResult::OK, traySnapshot)));
    ON_CALL(*mockIMediaIInputTray, getMediaSource()).WillByDefault(Return(dune::print::engine::MediaSource::TRAY1));
    ON_CALL(*mockIMedia, getInputDevices(dune::print::engine::DeviceOrder::DONT_CARE)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputs)));

    MockIJobServiceFactory<MockICopyJobTicket>* mockIJobService;
    CopyTicketAdapter*                          copyTicketAdapter;

    mockIJobService   = new MockIJobServiceFactory<MockICopyJobTicket>();
    copyTicketAdapter = new dune::copy::Jobs::Copy::CopyTicketAdapter(ticket, (JobServiceFactory<ICopyJobTicket>*)mockIJobService);

    // Call Test method
    auto constraintsGroup = component_->getConstraints(ticket, *copyTicketAdapter);

    EXPECT_NE(constraintFromJobService->getOutputMediaSourceIds().size(), 0);

    delete mockIMedia;
    delete mockIJobService;
    delete copyTicketAdapter;
}

TEST_F(GivenAConnectedJobConstraintsStandard, WhenGetConstraintsFromConfigurationIsCalled_TheConstraintsObtainedAreCorrect)
{
    // Get the Flattbuffer constraints
    std::shared_ptr<CopyJobConstraintsFbT> constraints = component_->getFbConstraintsTableFromConfiguration();

    assert(constraints);

    ASSERT_EQ(constraints->minCopies, 1);
    ASSERT_EQ(constraints->plexMode[0], dune::imaging::types::Plex::SIMPLEX);
    ASSERT_EQ(constraints->printQuality[2], dune::imaging::types::PrintQuality::BEST);
    ASSERT_EQ(constraints->mediaSupportedSize[6]->size->id, dune::imaging::types::MediaSizeId::A4);
    ASSERT_EQ(constraints->mediaSupportedSize[6]->supportedMediaSource[0], dune::imaging::types::MediaSource::TRAY1);
    ASSERT_EQ(constraints->mediaSupportedSize[6]->duplex[1], dune::imaging::types::Plex::DUPLEX);
    ASSERT_EQ(constraints->mediaSupportedType[31]->type->id, dune::imaging::types::MediaIdType::HEAVYROUGH);
    ASSERT_EQ(constraints->scanJobConstraint->maxScalePercent, 400);
    ASSERT_EQ(constraints->scanJobConstraint->scaleSelection[4], dune::scan::types::ScanScaleSelectionEnum::LEGALTOLETTER);
    ASSERT_EQ(constraints->scanJobConstraint->adfOriginalSizes[9]->id, dune::imaging::types::MediaSizeId::OFICIO_216X340);
    ASSERT_EQ(constraints->scanJobConstraint->flatbedOriginalSizes[15]->id, dune::imaging::types::MediaSizeId::HAGAKI_POSTCARD);
}

TEST_F(GivenAConnectedJobConstraintsStandard, WhengetMediaIdTypeConstraintsisCalled_WithMediaTypeVisibilityTogglingSupported_ThenOnlyEnabledMediaTypesAreReturned)
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
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPECOFFICIENT\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"HPMATTE90G\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
"                        }, "
"						{ "
"                            \"type\":{ \"id\":\"TRANSPARENCY\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"LABELS\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\" ], "
"                            \"duplex\": [ \"SIMPLEX\" ] "
"                        }, "
"                        { "
"                            \"type\":{ \"id\":\"USER_DEFINED_1\" }, "
"                            \"supportedMediaSource\": [ \"TRAY1\", \"TRAY2\", \"TRAY3\" ], "
"                            \"duplex\": [ \"SIMPLEX\", \"DUPLEX\" ] "
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
"                        \"scaleSelection\": [ \"NONE\", \"CUSTOM\", \"FITTOPAGE\", \"LEGALTOLETTER\" ], "
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
    std::shared_ptr<Constraints> TypeConstraints =  CopyJobStaticConstraintRules::getMediaIdTypeConstraints(ticket);
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
    TypeConstraints =  CopyJobStaticConstraintRules::getMediaIdTypeConstraints(ticket);
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
    TypeConstraints =  CopyJobStaticConstraintRules::getMediaIdTypeConstraints(ticket);
    theTypeConstraints = TypeConstraints->getConstraints();
    validTypes = theTypeConstraints[1];

    validDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaType>*>(validTypes);
    std::cerr << "ConstraintType:" << (int) validDudes->getConstraintType() << " , validDudes->getValidValues().size(): " << validDudes->getValidValues().size() << "\n";
    EXPECT_EQ(4, (int)validDudes->getValidValues().size());

    //now check media source constraints
    std::shared_ptr<Constraints> SourceConstraints =  CopyJobStaticConstraintRules::getMediaSourceConstraints(ticket);
    std::vector<IConstraint*> theSourceConstraints = SourceConstraints->getConstraints();
    IConstraint* validSources = theSourceConstraints[1];

    ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>* validSourceDudes = dynamic_cast<ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>*>(validSources);
    std::cerr << "ConstraintType:" << (int) validSourceDudes->getConstraintType() << " , validSourceDudes->getValidValues().size(): " << validSourceDudes->getValidValues().size() << "\n";
    EXPECT_EQ(2, (int)validSourceDudes->getValidValues().size());
    // ********************************************************
}

TEST_F(GivenAConnectedJobConstraintsStandard, WhenGettingCustomMediaXFeedDimensionConstraints_ThenConstraintsAreGet)
{
    double validValue1 = 40000, validValue2 = 120000, invalidValue1 = 35000, invalidValue2 = 130000;
    auto constraints = CopyJobStaticConstraintRules::getCustomMediaXFeedDimensionConstraints();
    bool validateRet = constraints->tryValidate(&validValue1);
    EXPECT_EQ(validateRet, true);
    validateRet = constraints->tryValidate(&validValue2);
    EXPECT_EQ(validateRet, true);
    validateRet = constraints->tryValidate(&invalidValue1);
    EXPECT_EQ(validateRet, false);
    validateRet = constraints->tryValidate(&invalidValue2);
    EXPECT_EQ(validateRet, false);
}

TEST_F(GivenAConnectedJobConstraintsStandard, WhenGettingCustomMediaYFeedDimensionConstraints_ThenConstraintsAreGet)
{
    double validValue1 = 60000, validValue2 = 170000, invalidValue1 = 50000, invalidValue2 = 185000;
    auto constraints = CopyJobStaticConstraintRules::getCustomMediaYFeedDimensionConstraints();
    bool validateRet = constraints->tryValidate(&validValue1);
    EXPECT_EQ(validateRet, true);
    validateRet = constraints->tryValidate(&validValue2);
    EXPECT_EQ(validateRet, true);
    validateRet = constraints->tryValidate(&invalidValue1);
    EXPECT_EQ(validateRet, false);
    validateRet = constraints->tryValidate(&invalidValue2);
    EXPECT_EQ(validateRet, false);
}

TEST_F(GivenAConnectedJobConstraintsStandard, WhenGettingScaleToOutputConstraints_ThenConstraintsAreGet)
{
    std::vector<dune::cdm::glossary_1::MediaSourceId> enumPossibleValues{dune::cdm::glossary_1::MediaSourceId::tray_dash_1, dune::cdm::glossary_1::MediaSourceId::tray_dash_2};
    std::vector<dune::cdm::glossary_1::MediaSourceId> enumValidValues{dune::cdm::glossary_1::MediaSourceId::tray_dash_1, dune::cdm::glossary_1::MediaSourceId::tray_dash_2};
    auto constraints = CopyJobStaticConstraintRules::getScaleToOutputConstraints(enumPossibleValues, enumValidValues);
    auto validValue1 = dune::cdm::glossary_1::MediaSourceId::tray_dash_1;
    auto validValue2 = dune::cdm::glossary_1::MediaSourceId::tray_dash_2;
    auto invalidValue1 = dune::cdm::glossary_1::MediaSourceId::tray_dash_3;
    auto invalidValue2 = dune::cdm::glossary_1::MediaSourceId::tray_dash_4;
    bool validateRet = constraints->tryValidate(&validValue1);
    EXPECT_EQ(validateRet, true);
    validateRet = constraints->tryValidate(&validValue2);
    EXPECT_EQ(validateRet, true);
    validateRet = constraints->tryValidate(&invalidValue1);
    EXPECT_EQ(validateRet, false);
    validateRet = constraints->tryValidate(&invalidValue2);
    EXPECT_EQ(validateRet, false);
}

TEST_F(GivenAConnectedJobConstraintsStandard, WhenGettingScaleToOutputConstraints_ThenAutoIsNotAdded)
{
    std::vector<dune::cdm::glossary_1::MediaSourceId> enumPossibleValues{dune::cdm::glossary_1::MediaSourceId::tray_dash_1, dune::cdm::glossary_1::MediaSourceId::tray_dash_2, dune::cdm::glossary_1::MediaSourceId::auto_};
    std::vector<dune::cdm::glossary_1::MediaSourceId> enumValidValues{dune::cdm::glossary_1::MediaSourceId::tray_dash_1, dune::cdm::glossary_1::MediaSourceId::tray_dash_2, dune::cdm::glossary_1::MediaSourceId::auto_};
    auto constraints = CopyJobStaticConstraintRules::getScaleToOutputConstraints(enumPossibleValues, enumValidValues);
    auto validValue1 = dune::cdm::glossary_1::MediaSourceId::tray_dash_1;
    auto validValue2 = dune::cdm::glossary_1::MediaSourceId::tray_dash_2;
    auto invalidValue1 = dune::cdm::glossary_1::MediaSourceId::auto_;
    bool validateRet = constraints->tryValidate(&validValue1);
    EXPECT_EQ(validateRet, true);
    validateRet = constraints->tryValidate(&validValue2);
    EXPECT_EQ(validateRet, true);
    validateRet = constraints->tryValidate(&invalidValue1);
    EXPECT_EQ(validateRet, false);
}
///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedJobConstraintsStandardReadyToCallShutdown : shutdown case.
// Dummy class that inherits from GivenAConnectedJobConstraintsStandard in order to reuse code
// and enable parametrized tests.
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedJobConstraintsStandardReadyToCallShutdown : public GivenAConnectedJobConstraintsStandard,
                           public ::testing::WithParamInterface<IComponent::ShutdownCause>
{

};


TEST_P(GivenAConnectedJobConstraintsStandardReadyToCallShutdown, whenShutdownIsCalled_TheComponentGetsShutdown)
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

INSTANTIATE_TEST_CASE_P(InstantiationName, GivenAConnectedJobConstraintsStandardReadyToCallShutdown, ::testing::Values(
 IComponent::ShutdownCause(IComponent::ShutdownCause::POWER_OFF),
 IComponent::ShutdownCause(IComponent::ShutdownCause::REBOOT),
 IComponent::ShutdownCause(IComponent::ShutdownCause::SEVERE_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::EMERGENCY_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::CRITICAL_ERROR)
));


