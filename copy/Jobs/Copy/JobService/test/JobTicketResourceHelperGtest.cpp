#include "JobTicketResourceHelper.h"
#include "MockIJobTicketResourceManager.h"
#include "MockIJobServiceFactory.h"
#include "MockICopyJobTicket.h"
#include "CopyTicketAdapter.h"
#include "MockICopyJobTicket.h"
#include "MockIJobConstraints.h"
#include "MockICopyJobDynamicConstraintRules.h"
#include "MockICopyAdapter.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"

using namespace dune::copy::Jobs::Copy;

// Test fixture for JobTicketResourceHelper
class JobTicketResourceHelperTest : public ::testing::Test
{
    public:
    JobTicketResourceHelperTest() {}
    virtual void SetUp() override;

    virtual void TearDown() override;
    MockIJobServiceFactory<MockICopyJobTicket>*     mockIJobService_;
    MockIJobTicketResourceManager*                  mockIJobTicketResourceManager_;
    std::shared_ptr<MockICopyJobTicket>             mockIJobTicket_{std::make_shared<MockICopyJobTicket>()};
    JobTicketResourceHelper*                        jobTicketResourceHelper_;
    std::shared_ptr<dune::copy::cdm::MockICopyAdapter> moclICopyAdapter_{
        std::make_shared<dune::copy::cdm::MockICopyAdapter>()};
    std::shared_ptr<MockIJobConstraints>                mockIJobConstraints_{std::make_shared<MockIJobConstraints>()};
    std::shared_ptr<MockICopyJobDynamicConstraintRules> mockICopyJobDynamicConstraintRules_{
        std::make_shared<MockICopyJobDynamicConstraintRules>()};
};

void JobTicketResourceHelperTest::SetUp()
{
    mockIJobService_ = new MockIJobServiceFactory<MockICopyJobTicket>();
    mockIJobTicketResourceManager_ = new MockIJobTicketResourceManager();
    jobTicketResourceHelper_ = new JobTicketResourceHelper((JobServiceFactory<ICopyJobTicket>*)mockIJobService_);
}

void JobTicketResourceHelperTest::TearDown()
{
    delete mockIJobService_;
    delete mockIJobTicketResourceManager_;
    delete jobTicketResourceHelper_;
}
// Test case for registerHelper method
TEST_F(JobTicketResourceHelperTest, RegisterHelper)
{
    std::cout<<"\nPrashant";
    EXPECT_CALL(*mockIJobTicketResourceManager_, registerResourceHelper(::testing::_)).Times(1);
    jobTicketResourceHelper_->registerHelper(mockIJobTicketResourceManager_);   
}

TEST_F(JobTicketResourceHelperTest, CreateTicketAdapter_DefaultJobTicket)
{
    Configuration configuration{JobSourceDestinationType::SCAN, JobSourceDestinationType::PRINT, JobType::COPY, "copy", nullptr};
    JobTicketType jobTicketType = JobTicketType::DEFAULT;
    EXPECT_CALL(*mockIJobService_, getDefaultJobTicket()).WillOnce(::testing::Return(mockIJobTicket_));
    jobTicketResourceHelper_->setCopyJobConstraintsHelper(mockIJobConstraints_.get());
    jobTicketResourceHelper_->setCopyDynamicConstraintsHelper(mockICopyJobDynamicConstraintRules_.get());
    jobTicketResourceHelper_->setCopyConfigurationHelper(moclICopyAdapter_.get());
    jobTicketResourceHelper_->setLocaleProvider(nullptr);
    std::shared_ptr<ITicketAdapter> adapter_ = jobTicketResourceHelper_->createTicketAdapter(configuration, jobTicketType);
    EXPECT_NE(adapter_, nullptr);
}

TEST_F(JobTicketResourceHelperTest, CreateTicketAdapter_DefaultJobTicketJobTypeQuickset)
{
    Configuration configuration{JobSourceDestinationType::SCAN, JobSourceDestinationType::PRINT, JobType::COPY, "copy", nullptr};
    JobTicketType jobTicketType = JobTicketType::QUICKSET;
    EXPECT_CALL(*mockIJobService_, getDefaultJobTicket()).Times(0);
    std::shared_ptr<ITicketAdapter> adapter_ = jobTicketResourceHelper_->createTicketAdapter(configuration, jobTicketType);
    EXPECT_EQ(adapter_, nullptr);
}

TEST_F(JobTicketResourceHelperTest, CreateTicketAdapter_UUID)
{
    Configuration configuration{JobSourceDestinationType::SCAN, JobSourceDestinationType::PRINT, JobType::COPY, "copy", nullptr};
    JobTicketType jobTicketType = JobTicketType::DEFAULT;
    const Uuid& ticketId = Uuid::createUuid();
    EXPECT_CALL(*mockIJobService_, getTicketFromCache(ticketId)).WillOnce(::testing::Return(mockIJobTicket_));
    jobTicketResourceHelper_->setCopyJobConstraintsHelper(mockIJobConstraints_.get());
    jobTicketResourceHelper_->setCopyDynamicConstraintsHelper(mockICopyJobDynamicConstraintRules_.get());
    jobTicketResourceHelper_->setCopyConfigurationHelper(moclICopyAdapter_.get());
    jobTicketResourceHelper_->setLocaleProvider(nullptr);
    std::shared_ptr<ITicketAdapter> adapter_ = jobTicketResourceHelper_->createTicketAdapter(ticketId);
    EXPECT_NE(adapter_, nullptr);
}

TEST_F(JobTicketResourceHelperTest, CreateTicketAdapter_SerializedBuffer)
{
    Configuration configuration{JobSourceDestinationType::SCAN, JobSourceDestinationType::PRINT, JobType::COPY, "copy", nullptr};
    JobTicketType jobTicketType = JobTicketType::DEFAULT;
    const dune::framework::data::SerializedDataBufferPtr& buff = std::make_pair(nullptr, 0);
    EXPECT_CALL(*mockIJobService_, deserializeJobTicket(::testing::_)).Times(1).WillRepeatedly(::testing::Return(mockIJobTicket_));
    jobTicketResourceHelper_->setCopyJobConstraintsHelper(mockIJobConstraints_.get());
    jobTicketResourceHelper_->setCopyDynamicConstraintsHelper(mockICopyJobDynamicConstraintRules_.get());
    jobTicketResourceHelper_->setCopyConfigurationHelper(moclICopyAdapter_.get());
    jobTicketResourceHelper_->setLocaleProvider(nullptr);
    std::shared_ptr<ITicketAdapter> adapter_ = jobTicketResourceHelper_->createTicketAdapter(buff);
    EXPECT_NE(adapter_, nullptr);
}
