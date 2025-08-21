/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyTicketConverterJoltToDuneGtest.cpp
 * @date   Fri, 02 May 2025 23:00:09 +0530
 * @brief  Unit tests for the CopyTicketConverterJoltToDune component
 *
 * (C) Copyright 2025 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyTicketConverterJoltToDune.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "TestSystemServices.h"
#include "GTestConfigHelper.h"
#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "MockIScanJoltToDuneConverter.h"
#include "XmlUtils.h"
#include "MockIPrintIntentsConverter.h"
#include "MockIPipelineOptionsConvertionAdapter.h"

#include <fstream>
#include <chrono>
#include <string>
#include <memory>

using namespace dune::copy::Jobs::Copy;
using namespace dune::framework::component;
using namespace dune::framework::data::conversion;
using namespace dune::scan;
using CopyTicketConverterJoltToDune = dune::copy::Jobs::Copy::CopyTicketConverterJoltToDune;
using TestSystemServices = dune::framework::component::TestingUtil::TestSystemServices;
using IComponent = dune::framework::component::IComponent;
using IComponentManager = dune::framework::component::IComponentManager;
using SystemServices = dune::framework::component::SystemServices;
using SysTrace = dune::framework::core::dbg::SysTrace;
using CheckpointLevel = SysTrace::CheckpointLevel;
using GTestConfigHelper = dune::framework::core::gtest::GTestConfigHelper;
using APIResult = dune::framework::core::APIResult;

GTestConfigHelper testConfigOptions_;

#include <gtest/gtest.h>

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenANewCopyTicketConverterJoltToDune : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenANewCopyTicketConverterJoltToDune : public ::testing::Test
{
  public:

    GivenANewCopyTicketConverterJoltToDune() : component_(nullptr), systemServices_(nullptr),
    componentManager_(nullptr) {};

    virtual void SetUp() override;

    virtual void TearDown() override;

  protected:

    dune::copy::Jobs::Copy::CopyTicketConverterJoltToDune                          * component_;
    TestSystemServices                              * systemServices_;
    dune::framework::component::IComponentManager   * componentManager_;
    dune::scan::MockIScanJoltToDuneConverter         mockIScanJoltToDuneConverter;
};

void GivenANewCopyTicketConverterJoltToDune::SetUp()
{
    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyTicketConverterJoltToDuneConfig.fbs",
    "./testResources/CopyTicketConverterJoltToDuneTestData.json");

    component_ = new CopyTicketConverterJoltToDune("myInstance");
    ASSERT_NE(nullptr, component_);
}

void GivenANewCopyTicketConverterJoltToDune::TearDown()
{
    delete component_;
    delete systemServices_;
}

TEST_F(GivenANewCopyTicketConverterJoltToDune, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_);
}

TEST_F(GivenANewCopyTicketConverterJoltToDune, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanJoltToDuneConverter), "MockIScanJoltToDuneConverter", &mockIScanJoltToDuneConverter);

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
    ASSERT_TRUE(true);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyTicketConverterJoltToDune : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////

class TestableCopyTicketConverterJoltToDune : public CopyTicketConverterJoltToDune
{
  public:
    TestableCopyTicketConverterJoltToDune(const char* instanceName) : CopyTicketConverterJoltToDune(instanceName) {}
    
    IPipelineOptionsConvertionAdapter* getPipelineOptionConverter() const { return pipelineOptionsConverter_; }

    IPrintIntentsConverter* getPrintJoltToDuneConverter() const { return printJoltToDuneConverter_; }

    void setPipelineOptionConverter(IPipelineOptionsConvertionAdapter* pipelineOptionsConverter)
    {
        if(pipelineOptionsConverter)
        {
            if(pipelineOptionsConverter_) delete pipelineOptionsConverter_;
            pipelineOptionsConverter_ = pipelineOptionsConverter;
        }
    }

    void setPrintJoltToDuneConverter(IPrintIntentsConverter* printJoltToDuneConverter)
    {
        if(printJoltToDuneConverter)
        {
            if(printJoltToDuneConverter_) delete printJoltToDuneConverter_;
            printJoltToDuneConverter_ = printJoltToDuneConverter;
        }
    }
};

class GivenAConnectedCopyTicketConverterJoltToDune: public ::testing::Test
{
  public:

    GivenAConnectedCopyTicketConverterJoltToDune() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    std::string createTestXmlFile(const std::string& prefix, const std::string& content)
    {
        auto now = std::chrono::system_clock::now();
        auto now_ms = std::chrono::time_point_cast<std::chrono::milliseconds>(now);
        auto timestamp = now_ms.time_since_epoch().count();
        
        std::string uniqueFile = prefix + "_" + std::to_string(timestamp) + ".xml";
        testFilePath_ = uniqueFile;
        
        std::ofstream outFile(testFilePath_);
        outFile << content;
        outFile.close();
        
        return testFilePath_;
    }

  protected:
    TestableCopyTicketConverterJoltToDune * component_;
    TestSystemServices                              * systemServices_;
    dune::framework::component::IComponentManager   * componentManager_;
    dune::scan::MockIScanJoltToDuneConverter         mockIScanJoltToDuneConverter;
    dune::copy::Jobs::Copy::MockIPrintIntentsConverter* mockPrintIntentsConverter_;
    dune::imaging::Jobs::MockIPipelineOptionsConvertionAdapter* mockPipelineOptionsConverter_;
    std::string testFilePath_;
    dune::framework::data::conversion::DataDescriptor fileDescriptor_;
};

void GivenAConnectedCopyTicketConverterJoltToDune::SetUp()
{
    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyTicketConverterJoltToDuneConfig.fbs",
    "./testResources/CopyTicketConverterJoltToDuneTestData.json");

    component_ = new TestableCopyTicketConverterJoltToDune("myInstance");

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanJoltToDuneConverter), "MockIScanJoltToDuneConverter", &mockIScanJoltToDuneConverter);

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    
    mockPrintIntentsConverter_ = new MockIPrintIntentsConverter();
    mockPipelineOptionsConverter_ = new dune::imaging::Jobs::MockIPipelineOptionsConvertionAdapter();
    component_->setPrintJoltToDuneConverter(mockPrintIntentsConverter_); 
    component_->setPipelineOptionConverter(mockPipelineOptionsConverter_);

    std::string xmlContent = "<root><copy:CopySettings>"
                            "<dd:Sharpness>4</dd:Sharpness>"
                            "<dd:BackgroundRemoval>2</dd:BackgroundRemoval>"
                            "</copy:CopySettings></root>";
    std::string testXmlFile = createTestXmlFile("copy_test", xmlContent);

    fileDescriptor_.fileName_ = testXmlFile;
    fileDescriptor_.dataNodePath_ = "/root";
}

void GivenAConnectedCopyTicketConverterJoltToDune::TearDown()
{
    // Clean up any test file created
    if (!testFilePath_.empty() && std::ifstream(testFilePath_).good()) {
        std::remove(testFilePath_.c_str());
    }
    
    delete component_;
    delete systemServices_;
}

///////////////////////////////////////////////////////////////////////////////
//
// Tests for the Convert method
//
///////////////////////////////////////////////////////////////////////////////

TEST_F(GivenAConnectedCopyTicketConverterJoltToDune, WhenConvertCalledWithNullJobTicketTable_ReturnsError)
{
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketTable = nullptr;
    
    auto result = component_->convert(fileDescriptor_, jobTicketTable);
    
    ASSERT_EQ(ConversionResult::ERROR, result);
}

TEST_F(GivenAConnectedCopyTicketConverterJoltToDune, WhenConvertCalledWithValidInput_ConvertsSuccessfully)
{
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketTable = 
        std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    
    EXPECT_CALL(mockIScanJoltToDuneConverter, convert(::testing::_, ::testing::_))
        .Times(3)
        .WillRepeatedly(::testing::Return(APIResult::OK));
    
    EXPECT_CALL(*mockPipelineOptionsConverter_, convert(::testing::_, ::testing::_, ::testing::_))
        .Times(1)
        .WillOnce(::testing::Return(APIResult::OK));
    
    EXPECT_CALL(*mockPrintIntentsConverter_, convert(::testing::_, ::testing::_))
        .Times(1)
        .WillOnce(::testing::Return(APIResult::OK));
    
    auto result = component_->convert(fileDescriptor_, jobTicketTable);
    
    ASSERT_EQ(ConversionResult::SUCCESS, result);
}

TEST_F(GivenAConnectedCopyTicketConverterJoltToDune, WhenScanConverterFails_ReturnsError)
{
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketTable = 
        std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    
    EXPECT_CALL(mockIScanJoltToDuneConverter, convert(::testing::_, ::testing::_))
        .WillOnce(::testing::Return(APIResult::ERROR));
    
    auto result = component_->convert(fileDescriptor_, jobTicketTable);
    
    ASSERT_EQ(ConversionResult::ERROR, result);
}

TEST_F(GivenAConnectedCopyTicketConverterJoltToDune, WhenPipelineOptionsConverterFails_ReturnsError)
{
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketTable = 
        std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    
    EXPECT_CALL(mockIScanJoltToDuneConverter, convert(::testing::_, ::testing::_))
        .Times(3)
        .WillRepeatedly(::testing::Return(APIResult::OK));
    
    EXPECT_CALL(*mockPipelineOptionsConverter_, convert(::testing::_, ::testing::_, ::testing::_))
        .WillOnce(::testing::Return(APIResult::ERROR));
    
    auto result = component_->convert(fileDescriptor_, jobTicketTable);
    
    ASSERT_EQ(ConversionResult::ERROR, result);
}

TEST_F(GivenAConnectedCopyTicketConverterJoltToDune, WhenPrintConverterFails_ReturnsError)
{
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketTable = 
        std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    
    EXPECT_CALL(mockIScanJoltToDuneConverter, convert(::testing::_, ::testing::_))
        .Times(3)
        .WillRepeatedly(::testing::Return(APIResult::OK));
    
    EXPECT_CALL(*mockPipelineOptionsConverter_, convert(::testing::_, ::testing::_, ::testing::_))
        .WillOnce(::testing::Return(APIResult::OK));
    
    EXPECT_CALL(*mockPrintIntentsConverter_, convert(::testing::_, ::testing::_))
        .WillOnce(::testing::Return(APIResult::ERROR));
    
    auto result = component_->convert(fileDescriptor_, jobTicketTable);
    
    ASSERT_EQ(ConversionResult::ERROR, result);
}
