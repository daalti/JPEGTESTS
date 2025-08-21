/* -*- c -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   GivenConstraintsProvider.cpp
 * @date   20 Dec. 2023
 * @brief  Unit tests for CopyConfigurationConstraintsProviderGtest.cpp class
 *
 * (C) Copyright 2023 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAdapterStandard.h"
#include "CopyConstraintsProvider.h"
#include "MockIMicroServiceFactory.h"
#include "MockICopyAdapter.h"
#include "MockILocaleProvider.h"
#include "MockILocale.h"
#include "MockIDataChangeEvent.h"
#include "MockIDataChangeEvent.h"
#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "TestSystemServices.h"
#include "GTestConfigHelper.h"


using MockICopyAdapter              = dune::copy::cdm::MockICopyAdapter;
using CopyConfigurationConstraintsProvider     = dune::copy::cdm::CopyConfigurationConstraintsProvider;
using CopyConfigurationResourceData = dune::cdm::copy_1::configuration::ResourceData;
using GTestConfigHelper             = dune::framework::core::gtest::GTestConfigHelper;
using testing::Return;
using testing::ReturnRef;

using namespace dune::copy::cdm;
using namespace dune::framework::core::stdext;
using OperationResult   = dune::ws::cdm::OperationResult;
using ResponseMetadata  = dune::ws::cdm::OperationResponseMetadataT;
using RequestParameters = dune::ws::cdm::OperationParametersT;

using dune::framework::core::event::Event;
using ICopyAdapterDataChangeEventSource = dune::framework::core::event::EventSource<dune::copy::cdm::CopyConfigurationEventType>;
using MockIDataChangeEventReceiver = dune::ws::cdm::MockIDataChangeEventReceiver;

using CopyModeConfig =  dune::cdm::copy_1::configuration::CopyMode;
using CopyModeEvent  =  dune::copy::cdm::CopyConfigurationEventType;


class GivenConstraintsProvider : public ::testing::Test
{
  public:
    GivenConstraintsProvider(){}

    ~GivenConstraintsProvider(){}

    virtual void SetUp() override;

    virtual void TearDown() override;
    
  protected:

    MockICopyAdapter                           mockICopyAdapter_;
    std::shared_ptr<CopyConfigurationConstraintsProvider> copyConfigurationConstraintsProvider_ {nullptr};
    
    ICopyAdapterDataChangeEventSource           mockedIDataChangeEventReceiverSource_;
    MockIDataChangeEventReceiver                mockedIDataChangeEventReceiver_;

    MockILocaleProvider            mockILocaleProvider_;
    std::shared_ptr<MockILocale>                   mockILocaleEnglish;
};

void GivenConstraintsProvider::SetUp()
{
    //Setup  Locale
    mockILocaleEnglish = std::make_shared<MockILocale>();
    ON_CALL(*mockILocaleEnglish, localeId()).WillByDefault(Return(LocaleId::en_US));
    ON_CALL(mockILocaleProvider_, deviceLocale()).WillByDefault(Return(mockILocaleEnglish));
    ON_CALL(mockILocaleProvider_, getLocale(LocaleId::en_US)).WillByDefault(Return(mockILocaleEnglish));
    
    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent()).WillByDefault(testing::ReturnRef(mockedIDataChangeEventReceiverSource_));

    copyConfigurationConstraintsProvider_ = std::make_shared<CopyConfigurationConstraintsProvider>(&mockICopyAdapter_, &mockILocaleProvider_, nullptr);
}

void GivenConstraintsProvider::TearDown()
{
    copyConfigurationConstraintsProvider_.reset();
}

TEST_F(GivenConstraintsProvider, WhenHandleCopyAdapterDataChangeEventIsCalledAndThereIsNoSubscription_ThenPushDataChangeEventIsNotCalled)
{
    EXPECT_CALL(mockedIDataChangeEventReceiver_, onDataChangeEvent(testing::_)).Times(0);

    copyConfigurationConstraintsProvider_->handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType::COPY_INTERRUPT_MODE);
}

TEST_F(GivenConstraintsProvider, WhenHandleCopyAdapterDataChangeEventIsCalledAndThereIsSubscription_ThenPushDataChangeEventIsCalled)
{

    copyConfigurationConstraintsProvider_->onDataChangeEventSubscription(true);

    bool result = copyConfigurationConstraintsProvider_->handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType::COPY_MODE);

    EXPECT_EQ(result, true);
}


//##################### TEST GET IMPLEMENTATION ##########################
class GivenConstraintsProviderForTestGetImplementation : public GivenConstraintsProvider,
                                  public ::testing::WithParamInterface< std::tuple<CopyModeConfig, OperationResult, int>>
{
  public:
    GivenConstraintsProviderForTestGetImplementation(){}

    ~GivenConstraintsProviderForTestGetImplementation(){}

    virtual void SetUp()
    {
        GivenConstraintsProvider::SetUp();

        copyModeConfig_ = std::get<0>(GetParam());
        expectedOpResult_ = std::get<1>(GetParam());
        expectedHttpResponseCode_ = std::get<2>(GetParam());
    }    
    
    virtual void TearDown()
    {
        GivenConstraintsProvider::TearDown();
    }

    CopyModeConfig copyModeConfig_{CopyModeConfig::printAfterScanning};

    int expectedHttpResponseCode_{0};
    OperationResult expectedOpResult_{OperationResult::_UNDEFINED_};
};

INSTANTIATE_TEST_CASE_P(, GivenConstraintsProviderForTestGetImplementation, ::testing::Values
(
   //CopyModeConfiguration, Expected Http response and code  
   std::make_tuple(CopyModeConfig::printAfterScanning, OperationResult::SUCCESS,    200),
   std::make_tuple(CopyModeConfig::printWhileScanning, OperationResult::SUCCESS,    200),
   std::make_tuple(CopyModeConfig::_undefined_,        OperationResult::SUCCESS,    200)
));


TEST_P(GivenConstraintsProviderForTestGetImplementation, WhenGetImplementationAndPrintWhileScanning_ThenSuccessShouldBeReturned)
{
    ON_CALL(mockICopyAdapter_, getCopyMode()).WillByDefault(Return(copyModeConfig_));

    RequestParameters params;
    OperationResult result{OperationResult::_UNDEFINED_};
    OperationResponseMetadataT responseMetadata;

    auto response = copyConfigurationConstraintsProvider_->getImplementation(params, result, responseMetadata);

    EXPECT_TRUE(response != nullptr);
    EXPECT_EQ(responseMetadata.httpStatusCode, expectedHttpResponseCode_);
    EXPECT_EQ(result, expectedOpResult_);
}

TEST_P(GivenConstraintsProviderForTestGetImplementation, WhenGetImplementationAndUndefined_ThenSuccessShouldBeReturned)
{
    ON_CALL(mockICopyAdapter_, getCopyMode()).WillByDefault(Return(CopyModeConfig::_undefined_));

    RequestParameters params;
    OperationResult result{OperationResult::_UNDEFINED_};
    OperationResponseMetadataT responseMetadata;

    auto response = copyConfigurationConstraintsProvider_->getImplementation(params, result, responseMetadata);

    ASSERT_NE(response, nullptr);
    EXPECT_EQ(responseMetadata.httpStatusCode, expectedHttpResponseCode_);
    EXPECT_EQ(result, expectedOpResult_);
    EXPECT_EQ(response->getFlatBufferT()->validators.size(), 1);
}

//##################### TEST GET handleCopyAdapterDataChangeEvent ##########################
class GivenConstraintsProviderForTestHandleDataChangeEvent : public GivenConstraintsProvider,
                                  public ::testing::WithParamInterface< std::tuple<CopyModeEvent, CopyModeConfig, bool>>

{
  public:
    GivenConstraintsProviderForTestHandleDataChangeEvent(){}

    ~GivenConstraintsProviderForTestHandleDataChangeEvent(){}

    virtual void SetUp()
    {
        GivenConstraintsProvider::SetUp();
    }    
    
    virtual void TearDown()
    {
        GivenConstraintsProvider::TearDown();

        copyModeEvent_ = std::get<0>(GetParam());
        copyModeConfig_ = std::get<1>(GetParam());
        expectedSuccess_ = std::get<2>(GetParam());
    }

    CopyModeEvent copyModeEvent_{CopyModeEvent::COPY_INTERRUPT_MODE};
    CopyModeConfig copyModeConfig_{CopyModeConfig::printAfterScanning};
    bool expectedSuccess_{false};
};

INSTANTIATE_TEST_CASE_P(, GivenConstraintsProviderForTestHandleDataChangeEvent, ::testing::Values
(
   //EventType, CopyModeConfiguration, ExpectedReturn of HandleDataChangeEvent  
   std::make_tuple(CopyModeEvent::COPY_INTERRUPT_MODE,             CopyModeConfig::printAfterScanning, false),
   std::make_tuple(CopyModeEvent::COPY_INTERRUPT_MODE,             CopyModeConfig::printWhileScanning, false),
   std::make_tuple(CopyModeEvent::COLOR_COPY_ENABLE_STATE_CHANGE,  CopyModeConfig::printAfterScanning, false),
   std::make_tuple(CopyModeEvent::COLOR_COPY_ENABLE_STATE_CHANGE,  CopyModeConfig::printWhileScanning, false),
   std::make_tuple(CopyModeEvent::COPY_ENABLE_STATE_CHANGE,        CopyModeConfig::printAfterScanning, false),
   std::make_tuple(CopyModeEvent::COPY_ENABLE_STATE_CHANGE,        CopyModeConfig::printWhileScanning, false),

   std::make_tuple(CopyModeEvent::COPY_MODE, CopyModeConfig::printAfterScanning, true),
   std::make_tuple(CopyModeEvent::COPY_MODE, CopyModeConfig::printWhileScanning, true),
   std::make_tuple(CopyModeEvent::COPY_MODE, CopyModeConfig::_undefined_,       false)
));

TEST_P(GivenConstraintsProviderForTestHandleDataChangeEvent, WhenHandleCopyAdapterDataChangeEventIsCalledAndThereIsDataChangeSubscriptionActive_ThenPushDataChangeEventShouldBeCalledWithCurrentConfiguration)
{

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

            EXPECT_EQ(configuration->allowInterrupt, interruptMode);
        }));

    ON_CALL(mockICopyAdapter_, getCopyMode()).WillByDefault(Return(copyModeConfig_));


    copyConfigurationConstraintsProvider_->subscribeEventReceiver(&mockedIDataChangeEventReceiver_);

    bool isSuccess = copyConfigurationConstraintsProvider_->handleCopyAdapterDataChangeEvent( copyModeEvent_ );

    EXPECT_EQ(isSuccess, expectedSuccess_ );

}
