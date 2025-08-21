////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPageTicketGtest.cpp
 * @brief  CopyPageTicket unit tests
 *
 * (C) Sampleright 2022 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////


#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "CopyPageTicket.h"
#include "CopyTicketGtestUtilities.h"
#include "GTestConfigHelper.h"

using namespace dune::framework::core;
using namespace dune::copy::Jobs::Copy;
using namespace dune::job;

using ::testing::_;
using ::testing::Return;
using ::testing::ReturnRef;

using GTestConfigHelper     = dune::framework::core::gtest::GTestConfigHelper;

GTestConfigHelper testConfigOptions_;

int main(int argc, char *argv[])
{
    // setup signal handler
    dune::framework::core::error::ErrorManager::installSignalsTrap();

    // ensure core dumps are enabled
    dune::framework::core::error::ErrorManager::enableCoreDumps();

    // run google tests
    std::cout << "Main:  " << argv[0] << std::endl;

    testConfigOptions_.parse(argc, argv);
    testConfigOptions_.Configure();

    //Ucomment for enable all logs channels for debugging
    testConfigOptions_.setNewFilter(GTestConfigHelper::SysTrace::CheckpointLevel::CheckpointA, true);
    testConfigOptions_.setNewFilter(GTestConfigHelper::SysTrace::CheckpointLevel::CheckpointB, true);
    testConfigOptions_.setNewFilter(GTestConfigHelper::SysTrace::CheckpointLevel::CheckpointC, true);
    testConfigOptions_.setNewFilter(GTestConfigHelper::SysTrace::CheckpointLevel::CheckpointD, true);
    ::testing::FLAGS_gmock_verbose = "error";

    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}

class GivenACopyPageTicket : public ::testing::Test
{
  public:
    std::unique_ptr<CopyPageTicket> ticket_{CopyTicketsUtilities::createDefaultPageTicket()};
};

TEST_F(GivenACopyPageTicket, WhenCloningPageTicket_ThenClonedTicketIsIdentical)
{
    std::unique_ptr<ICopyPageTicket> clonedTicket{ticket_->clone(false)};
    CopyTicketsUtilities::compareCopyPageTicket(*ticket_, *clonedTicket);
}

TEST_F(GivenACopyPageTicket, WhenCloningPageTicketForReprint_ThenClonedTicketIsIdentical)
{
    ticket_->getPageResult()->getPrintPageResult()->setEstimatedPrintTime(100);
    ticket_->getPageResult()->getPrintPageResult()->setCompletedCopies(1);
    ticket_->getPageResult()->getPrintPageResult()->setPrinted(true);
    std::unique_ptr<ICopyPageTicket> clonedTicket{ticket_->clone(true)};
    CopyTicketsUtilities::compareCopyPageTicket(*ticket_, *clonedTicket);
    EXPECT_EQ(clonedTicket->getIntent(dune::job::IntentType::PRINT), nullptr);
    EXPECT_EQ(clonedTicket->getPageResult()->getPrintPageResult()->getEstimatedPrintTime(), 0);
    EXPECT_EQ(clonedTicket->getPageResult()->getPrintPageResult()->getCompletedCopies(), 0);
    EXPECT_EQ(clonedTicket->getPageResult()->getPrintPageResult()->isPrinted(), false);
}

TEST_F(GivenACopyPageTicket, WhenGettingHandler_ThenHandlerIsValid)
{
    EXPECT_NE(nullptr, ticket_->getHandler());
}

TEST_F(GivenACopyPageTicket, WhenDeserializeFromFbIsCalled_ThenHandlerIsSet)
{
    std::unique_ptr<CopyPageTicket> copyPageTicket{CopyTicketsUtilities::createDefaultPageTicket()};
    copyPageTicket->setPageNumber(5);
    copyPageTicket->deserializeFromFb(*copyPageTicket->serializeToFb());

    std::shared_ptr<dune::job::IPageTicketHandler> copyPageTicketHandler = copyPageTicket->getHandler();

    // Validate pageTicket handler
    EXPECT_NE(nullptr, copyPageTicketHandler);
    EXPECT_EQ(copyPageTicketHandler->getPageNumber(), 5);
}

TEST_F(GivenACopyPageTicket, WhenGettingPageIntent_ThenPageIntentIsValid)
{
    std::unique_ptr<CopyPageTicket> copyPageTicket{CopyTicketsUtilities::createDefaultPageTicket()};
    std::shared_ptr<dune::job::CopyPageIntent> copyPageIntent = copyPageTicket->getPageIntent();

    EXPECT_NE(nullptr, copyPageIntent);
}

TEST_F(GivenACopyPageTicket, WhenGettingPageResult_ThenPageResultIsValid)
{
    std::unique_ptr<CopyPageTicket> copyPageTicket{CopyTicketsUtilities::createDefaultPageTicket()};
    std::shared_ptr<dune::job::CopyPageResult> copyPageResult = copyPageTicket->getPageResult();

    EXPECT_NE(nullptr, copyPageResult);
}
