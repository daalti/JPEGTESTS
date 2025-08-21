/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyConfigurationProviderTest.cpp
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyConfigurationProvider.h"

#include "SecurityContextImpl.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "GTestConfigHelper.h"
#include "EventSource.h"

#include "MockICopyAdapter.h"
#include "MockIDataChangeEvent.h"

using CopyConfigurationProvider = dune::copy::cdm::CopyConfigurationProvider;
using GTestConfigHelper         = dune::framework::core::gtest::GTestConfigHelper;
using MockICopyAdapter          = dune::copy::cdm::MockICopyAdapter;
using RequestParameters         = dune::ws::cdm::OperationParametersT;
using OperationResult           = dune::ws::cdm::OperationResult;
using MockIDataChangeEventReceiver = dune::ws::cdm::MockIDataChangeEventReceiver;
using DataChangeEvent           = dune::ws::cdm::DataChangeEvent;
using TypeDefinitionT           = dune::ws::cdm::TypeDefinitionT;
using ICopyAdapterDataChangeEventSource = dune::framework::core::event::EventSource<dune::copy::cdm::CopyConfigurationEventType>;
using ConfigurationData = dune::cdm::copy_1::configuration::ResourceData;

GTestConfigHelper testConfigOptions_;

int main(int argc, char  *argv[])
{
    // run google tests
    //

    testConfigOptions_.parse(argc, argv);
    testConfigOptions_.Configure();

    ::testing::FLAGS_gmock_catch_leaked_mocks = true;
    ::testing::FLAGS_gmock_verbose = "error";

    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenACopyConfigurationProvider : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenACopyConfigurationProvider : public ::testing::Test
{
public:
    GivenACopyConfigurationProvider() {};

    virtual void SetUp() override;
    virtual void TearDown() override;

protected:
    MockICopyAdapter                            mockCopyAdapter_;
    std::shared_ptr<CopyConfigurationProvider>  configurationProvider_{nullptr};
    MockIDataChangeEventReceiver                mockedIDataChangeEventReceiver_;
    ICopyAdapterDataChangeEventSource           mockedIDataChangeEventReceiverSource_;
};

void GivenACopyConfigurationProvider::SetUp()
{
    ON_CALL(mockCopyAdapter_, getCopyAdapterDataChangeEvent()).WillByDefault(testing::ReturnRef(mockedIDataChangeEventReceiverSource_));
    configurationProvider_ = std::make_shared<CopyConfigurationProvider>(&mockCopyAdapter_);

    ASSERT_TRUE(configurationProvider_ != nullptr);
}

void GivenACopyConfigurationProvider::TearDown()
{
    configurationProvider_.reset();
}

TEST_F(GivenACopyConfigurationProvider, WhenGetImplementationIsCalled_ThenSuccessShouldBeReturned)
{
    RequestParameters params;
    OperationResult result{OperationResult::_UNDEFINED_};
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();

    EXPECT_CALL(mockCopyAdapter_, getCopyEnabled())
        .Times(1)
        .WillRepeatedly(testing::Return(true));
    EXPECT_CALL(mockCopyAdapter_, getColorCopyEnabled())
        .Times(1)
        .WillRepeatedly(testing::Return(true));
    EXPECT_CALL(mockCopyAdapter_, getCopyMode())
        .Times(2)
        .WillRepeatedly(testing::Return(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning));
    EXPECT_CALL(mockCopyAdapter_, getInterruptMode())
        .Times(2)
        .WillRepeatedly(testing::Return(dune::cdm::glossary_1::FeatureEnabled::false_));        

    auto response = configurationProvider_->getImplementation(params, result, responseMetadata);

    EXPECT_TRUE(response != nullptr);
    EXPECT_EQ(responseMetadata.httpStatusCode, 200);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::SUCCESS);
}

TEST_F(GivenACopyConfigurationProvider, WhenGetImplementationIsCalledAndDuneExceptionIsRaised_ThenErrorIPCShouldBeReturned)
{
    RequestParameters params;
    OperationResult result{OperationResult::_UNDEFINED_};
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();

    // Checking for dune::framework::core::DuneException case
    EXPECT_CALL(mockCopyAdapter_, getColorCopyEnabled())
        .Times(1)
        .WillRepeatedly(testing::Return(false));
    EXPECT_CALL(mockCopyAdapter_, getCopyMode())
        .Times(1)
        .WillRepeatedly(testing::Throw(dune::framework::core::DuneException("Unable to get data from getCopyMode()")));    

    auto dunExceptionResponse = configurationProvider_->getImplementation(params, result, responseMetadata);

    EXPECT_TRUE(dunExceptionResponse != nullptr);
    EXPECT_EQ(responseMetadata.httpStatusCode, 500);
    EXPECT_EQ(result, OperationResult::ERROR_IPC);
}

TEST_F(GivenACopyConfigurationProvider, WhenGetImplementationIsCalledAndStdExceptionIsRaised_ThenErrorIPCShouldBeReturned)
{
    RequestParameters params;
    OperationResult result{OperationResult::_UNDEFINED_};
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();

    // Checking for std::exception case
    EXPECT_CALL(mockCopyAdapter_, getInterruptMode())
        .Times(1)
        .WillRepeatedly(testing::Throw(std::exception()));   

    auto dunExceptionResponse = configurationProvider_->getImplementation(params, result, responseMetadata);

    EXPECT_TRUE(dunExceptionResponse != nullptr);
    EXPECT_EQ(responseMetadata.httpStatusCode, 500);
    EXPECT_EQ(result, OperationResult::ERROR_IPC);
}

TEST_F(GivenACopyConfigurationProvider, WhenSetImplementationIsCalled_ThenSuccessShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    EXPECT_CALL(mockCopyAdapter_, setCopyEnabled(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return());
    EXPECT_CALL(mockCopyAdapter_, setColorCopyEnabled(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return());
    EXPECT_CALL(mockCopyAdapter_, setCopyMode(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return());
    EXPECT_CALL(mockCopyAdapter_, setInterruptMode(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return());        

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->copyEnabled = dune::cdm::glossary_1::FeatureEnabled::true_;
    reqestConfiguration->colorCopyEnabled = dune::cdm::glossary_1::FeatureEnabled::false_;
    reqestConfiguration->copyMode = dune::cdm::copy_1::configuration::CopyMode::printAfterScanning;
    reqestConfiguration->allowInterrupt = dune::cdm::glossary_1::FeatureEnabled::true_;   
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->setImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 204);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::SUCCESS);
}

TEST_F(GivenACopyConfigurationProvider, WhenSetImplementationIsCalledAndDuneExceptionIsRaised_ThenIPCErrorShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();

    // Checking for dune::framework::core::DuneException case
    EXPECT_CALL(mockCopyAdapter_, setCopyMode(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Throw(dune::framework::core::DuneException("Unable to set data from setCopyMode()")));    

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->copyEnabled = dune::cdm::glossary_1::FeatureEnabled::true_;
    reqestConfiguration->colorCopyEnabled = dune::cdm::glossary_1::FeatureEnabled::false_;
    reqestConfiguration->copyMode = dune::cdm::copy_1::configuration::CopyMode::printAfterScanning;
    reqestConfiguration->allowInterrupt = dune::cdm::glossary_1::FeatureEnabled::true_;   
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->setImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 500);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::ERROR_IPC);
}

TEST_F(GivenACopyConfigurationProvider, WhenSetImplementationIsCalledAndDataIsNull_ThenParsingErrorShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    result = configurationProvider_->setImplementation(params, nullptr, responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 400);
    EXPECT_EQ(result, OperationResult::ERROR_PARSING_ERROR);
}

TEST_F(GivenACopyConfigurationProvider, WhenSetImplementationIsCalledAndStdExceptionIsRaised_ThenIPCErrorShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();

    // Checking for dune::framework::core::DuneException case
    EXPECT_CALL(mockCopyAdapter_, setCopyMode(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Throw(std::exception()));    

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->copyEnabled = dune::cdm::glossary_1::FeatureEnabled::true_;
    reqestConfiguration->colorCopyEnabled = dune::cdm::glossary_1::FeatureEnabled::false_;
    reqestConfiguration->copyMode = dune::cdm::copy_1::configuration::CopyMode::printAfterScanning;
    reqestConfiguration->allowInterrupt = dune::cdm::glossary_1::FeatureEnabled::true_;   
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->setImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 500);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::ERROR_IPC);
}

TEST_F(GivenACopyConfigurationProvider, WhenSetImplementationIsCalledAndCopyModeIsUndefined_ThenNotAuthorizedShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();

    // Checking for dune::framework::core::DuneException case
    ON_CALL(mockCopyAdapter_, getCopyMode())
        .WillByDefault(testing::Return(dune::cdm::copy_1::configuration::CopyMode::_undefined_));

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->copyEnabled = dune::cdm::glossary_1::FeatureEnabled::true_;
    reqestConfiguration->colorCopyEnabled = dune::cdm::glossary_1::FeatureEnabled::false_;
    reqestConfiguration->copyMode = dune::cdm::copy_1::configuration::CopyMode::printAfterScanning;
    reqestConfiguration->allowInterrupt = dune::cdm::glossary_1::FeatureEnabled::true_;   
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->setImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode,400);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::ERROR_NOT_AUTHORIZED);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationIsCalled_ThenSuccessShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    EXPECT_CALL(mockCopyAdapter_, setCopyEnabled(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return());
    EXPECT_CALL(mockCopyAdapter_, setColorCopyEnabled(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return());

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->copyEnabled = dune::cdm::glossary_1::FeatureEnabled::true_;
    reqestConfiguration->colorCopyEnabled = dune::cdm::glossary_1::FeatureEnabled::false_;
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->modifyImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 204);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::SUCCESS);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationIsCalledAndDataIsNull_ThenParsingErrorShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    result = configurationProvider_->modifyImplementation(params, nullptr, responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 400);
    EXPECT_EQ(result, OperationResult::ERROR_PARSING_ERROR);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationIsCalledAndDuneExceptionIsRaised_ThenIPCErrorShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();

    // Checking for dune::framework::core::DuneException case
    EXPECT_CALL(mockCopyAdapter_, setCopyEnabled(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Throw(dune::framework::core::DuneException("Unable to modify data from setCopyMode()")));    

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->copyEnabled = dune::cdm::glossary_1::FeatureEnabled::true_;
    reqestConfiguration->colorCopyEnabled = dune::cdm::glossary_1::FeatureEnabled::false_;
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->modifyImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 500);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::ERROR_IPC);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationIsCalledAndStdExceptionIsRaised_ThenIPCErrorShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    auto configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();

    // Checking for dune::framework::core::DuneException case
    EXPECT_CALL(mockCopyAdapter_, setColorCopyEnabled(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Throw(std::exception()));    

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->copyEnabled = dune::cdm::glossary_1::FeatureEnabled::true_;
    reqestConfiguration->colorCopyEnabled = dune::cdm::glossary_1::FeatureEnabled::false_;
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->modifyImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 500);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::ERROR_IPC);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationWithCopyModeIsCalledAndCopyModeWasUndefined_ThenERROR_NOT_AUTHORIZEDShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    ON_CALL(mockCopyAdapter_, getCopyMode())
        .WillByDefault(testing::Return(dune::cdm::copy_1::configuration::CopyMode::_undefined_));

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->copyEnabled = dune::cdm::glossary_1::FeatureEnabled::true_;
    reqestConfiguration->colorCopyEnabled = dune::cdm::glossary_1::FeatureEnabled::false_;
	reqestConfiguration->copyMode = dune::cdm::copy_1::configuration::CopyMode::printAfterScanning;
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->modifyImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 403);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::ERROR_NOT_AUTHORIZED);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationWithCopyModeIsCalledWithoutModifyCopyModeAndCopyModeWasUndefined_ThenSuccessShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    ON_CALL(mockCopyAdapter_, getCopyMode())
        .WillByDefault(testing::Return(dune::cdm::copy_1::configuration::CopyMode::_undefined_));
    EXPECT_CALL(mockCopyAdapter_, setColorCopyEnabled(testing::Eq(dune::cdm::glossary_1::FeatureEnabled::false_)))
        .Times(1);
    EXPECT_CALL(mockCopyAdapter_, setCopyEnabled(testing::Eq(dune::cdm::glossary_1::FeatureEnabled::true_)))
        .Times(1);

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->copyEnabled = dune::cdm::glossary_1::FeatureEnabled::true_;
    reqestConfiguration->colorCopyEnabled = dune::cdm::glossary_1::FeatureEnabled::false_;
	reqestConfiguration->copyMode = dune::cdm::copy_1::configuration::CopyMode::_undefined_;
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->modifyImplementation(params, std::move(reqData), responseMetadata);


    EXPECT_EQ(responseMetadata.httpStatusCode, 204);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::SUCCESS);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationWithCopyModeIsCalledAndCopyModeWasNotUndefined_ThenSuccessShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    ON_CALL(mockCopyAdapter_, getCopyMode())
        .WillByDefault(testing::Return(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning));

    EXPECT_CALL(mockCopyAdapter_, setCopyMode(testing::Eq(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning)))
        .Times(1);

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
	reqestConfiguration->copyMode = dune::cdm::copy_1::configuration::CopyMode::printAfterScanning;
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->modifyImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 204);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::SUCCESS);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationWithInterruptIsCalledAndInterruptWasUndefined_ThenERROR_NOT_AUTHORIZEDShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    ON_CALL(mockCopyAdapter_, getInterruptMode())
        .WillByDefault(testing::Return(dune::cdm::glossary_1::FeatureEnabled::_undefined_));

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->allowInterrupt = dune::cdm::glossary_1::FeatureEnabled::true_;    
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->modifyImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 403);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::ERROR_NOT_AUTHORIZED);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationWithInterruptIsCalledAndInterruptWasNotUndefined_ThenSuccessShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    auto reqData = std::make_unique<dune::cdm::copy_1::configuration::ResourceData>();
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    ON_CALL(mockCopyAdapter_, getInterruptMode())
        .WillByDefault(testing::Return(dune::cdm::glossary_1::FeatureEnabled::false_));
    EXPECT_CALL(mockCopyAdapter_, setInterruptMode(testing::Eq(dune::cdm::glossary_1::FeatureEnabled::true_)))
        .Times(1);

    auto reqestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::FBT>();
    reqestConfiguration->allowInterrupt = dune::cdm::glossary_1::FeatureEnabled::true_;    
    reqData->setFlatBufferT(reqestConfiguration);

    result = configurationProvider_->modifyImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 204);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::SUCCESS);
}

TEST_F(GivenACopyConfigurationProvider, WhenModifyImplementationWithInterrupIsCalledAndInteruptWasNotUndefinedEasyBuffer_ThenSuccessShouldBeReturned)
{
    OperationResult result{OperationResult::_UNDEFINED_};
    RequestParameters params;
    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    ON_CALL(mockCopyAdapter_, getInterruptMode())
        .WillByDefault(testing::Return(dune::cdm::glossary_1::FeatureEnabled::false_));
    EXPECT_CALL(mockCopyAdapter_, setInterruptMode(testing::Eq(dune::cdm::glossary_1::FeatureEnabled::true_)))
        .Times(1);

    auto requestConfiguration = std::make_shared<dune::cdm::copy_1::types::Configuration::EasyBufferTable>();
    requestConfiguration->allowInterrupt.set(dune::cdm::glossary_1::FeatureEnabled::true_);
    auto reqData = std::make_unique<ConfigurationData>(*requestConfiguration);

    result = configurationProvider_->modifyImplementation(params, std::move(reqData), responseMetadata);

    EXPECT_EQ(responseMetadata.httpStatusCode, 204);
    EXPECT_EQ(result, dune::ws::cdm::OperationResult::SUCCESS);
}

TEST_F(GivenACopyConfigurationProvider, WhenHandleCopyAdapterDataChangeEventIsCalledAndThereIsNoSubscription_ThenPushDataChangeEventIsNotCalled)
{
    EXPECT_CALL(mockedIDataChangeEventReceiver_, onDataChangeEvent(testing::_)).Times(0);

    configurationProvider_->handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType::COPY_INTERRUPT_MODE);
}

TEST_F(GivenACopyConfigurationProvider, WhenHandleCopyAdapterDataChangeEventIsCalledAndThereIsDataChangeSubscriptionActive_ThenPushDataChangeEventShouldBeCalledWithCurrentConfiguration)
{
    bool copyEnabled = true;
    bool colorCopyEnabled = true;
    dune::cdm::glossary_1::FeatureEnabled boolTrueInCdm = dune::cdm::glossary_1::FeatureEnabled::true_;
    dune::cdm::copy_1::configuration::CopyMode copyMode = dune::cdm::copy_1::configuration::CopyMode::printAfterScanning;
    dune::cdm::glossary_1::FeatureEnabled interruptMode = dune::cdm::glossary_1::FeatureEnabled::false_;

    EXPECT_CALL(mockedIDataChangeEventReceiver_, onDataChangeEvent(testing::_))
        .WillRepeatedly(testing::Invoke([&](std::shared_ptr<const DataChangeEvent> event) {
            ASSERT_TRUE(event != nullptr);
            ASSERT_TRUE(event->data != nullptr);
            ASSERT_TRUE(event->data->getSize() > 0);

            std::unique_ptr<TypeDefinitionT>    dataType = std::unique_ptr<TypeDefinitionT>(new TypeDefinitionT());
            ASSERT_TRUE(dataType != nullptr);

            std::unique_ptr<dune::cdm::copy_1::configuration::ResourceData> resourceDataFB(new dune::cdm::copy_1::configuration::ResourceData());
            ASSERT_TRUE(resourceDataFB != nullptr);

            dune::ws::cdm::ResourceDataBuffer resourceDataBuffer(*(event->data), *(dataType));
            resourceDataFB->moveBuffer(resourceDataBuffer.detachBuffer());

            std::shared_ptr<dune::cdm::copy_1::types::Configuration::FBT> configuration = resourceDataFB->getFlatBufferT();
            ASSERT_TRUE(configuration != nullptr);

            EXPECT_EQ(configuration->copyEnabled, boolTrueInCdm);
            EXPECT_EQ(configuration->colorCopyEnabled, boolTrueInCdm);
            EXPECT_EQ(configuration->copyMode, copyMode);
            EXPECT_EQ(configuration->allowInterrupt, interruptMode);
        }));

    EXPECT_CALL(mockCopyAdapter_, getCopyEnabled())
        .Times(1)
        .WillRepeatedly(testing::Return(copyEnabled));
    EXPECT_CALL(mockCopyAdapter_, getColorCopyEnabled())
        .Times(1)
        .WillRepeatedly(testing::Return(colorCopyEnabled));
    EXPECT_CALL(mockCopyAdapter_, getCopyMode())
        .Times(1)
        .WillRepeatedly(testing::Return(copyMode));
    EXPECT_CALL(mockCopyAdapter_, getInterruptMode())
        .Times(1)
        .WillRepeatedly(testing::Return(interruptMode));        

    configurationProvider_->subscribeEventReceiver(&mockedIDataChangeEventReceiver_);

    configurationProvider_->handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType::COPY_INTERRUPT_MODE);
}