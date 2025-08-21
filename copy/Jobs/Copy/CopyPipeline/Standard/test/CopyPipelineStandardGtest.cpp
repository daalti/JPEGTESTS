/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineStandardGtestMain.cpp
 * @date   Mon, 27 Feb 2023 13:43:04 +0530
 * @brief   Configurable Copy Pipeline 
 *
 * (C) Copyright 2023 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "CopyPipelineUwAdapter.h"
#include "common_debug.h"

#include "ConstraintsGroup.h"
#include "ConvertToScanTypeHelper.h"
#include "CopyConfigurablePipelineBuilder.h"
#include "CopyPipelineStandard.h"
#include "CopyPipelineTestFixture.h"
#include "Fs.h"
#include "GTestConfigHelper.h"
#include "MockICopyAdapter.h"
#include "MockIImagePersister.h"
#include "MockILayoutFilterIntent.h"
#include "MockIMediaAttributes.h"
#include "MockIMediaHandlingMgr.h"
#include "MockIPageAssembler.h"
#include "MockIPrintDevice.h"
#include "MockIPrintIntentsFactory.h"
#include "MockIResourceManagerClient.h"
#include "MockIResourceService.h"
#include "MockICopyJobTicket.h"
#include "IScanPipeline.h"
#include "MockIScanPipelineBuilder.h"

#include "ConvertToScanTypeHelper.h"
#include "Fs.h"
#include "MockIScanDevice.h"
#include "MockIScanPipeline.h"
#include "TestSystemServices.h"

using ComponentFlavorUid                = dune::framework::component::ComponentFlavorUid;
using MockIPageAssembler                = dune::imaging::Resources::MockIPageAssembler;
using MockIPrintDevice                  = dune::print::Resources::MockIPrintDevice;
using MockIPrintIntentsFactory          = dune::print::engine::MockIPrintIntentsFactory;
using MockIResourceManagerClient        = dune::job::MockIResourceManagerClient;
using MockIResourceService              = dune::job::MockIResourceService;
using MockIScanDevice                   = dune::scan::Resources::MockIScanDevice;
using MockIPrintMedia                   = dune::print::engine::MockIMedia;
using MockIMediaAttributes              = dune::imaging::asset::MockIMediaAttributes;
using CopyPipelineStandard              = dune::copy::Jobs::Copy::CopyPipelineStandard;
using MockICopyAdapter                  = dune::copy::cdm::MockICopyAdapter;

using TestSystemServices    = dune::framework::component::TestingUtil::TestSystemServices;
// General namespaces
using ComponentFlavorUid    = dune::framework::component::ComponentFlavorUid;
using IComponent            = dune::framework::component::IComponent;
using IComponentManager     = dune::framework::component::IComponentManager;
using SysTrace              = dune::framework::core::dbg::SysTrace;
using CheckpointLevel       = SysTrace::CheckpointLevel;
using SystemServices        = dune::framework::component::SystemServices;

// Mock namespaces
using MockIPageAssembler            = dune::imaging::Resources::MockIPageAssembler;
using MockIImagePersister           = dune::imaging::Resources::MockIImagePersister;
using MockIPrintDevice              = dune::print::Resources::MockIPrintDevice;
using MockIPrintIntentsFactory      = dune::print::engine::MockIPrintIntentsFactory;
using MockIResourceManagerClient    = dune::job::MockIResourceManagerClient;
using MockIResourceService          = dune::job::MockIResourceService;
using MockIScanDevice               = dune::scan::Resources::MockIScanDevice;
using MockIPrintMedia               = dune::print::engine::MockIMedia;
using MockIMediaAttributes          = dune::imaging::asset::MockIMediaAttributes;
using MockIMediaHandlingMgr         = dune::print::mediaHandlingAssets::MockIMediaHandlingMgr;
using MockIScanPipelineBuilder      = dune::scan::Jobs::Scan::MockIScanPipelineBuilder;

using ConvertToScanTypeHelper = dune::scan::types::ConvertToScanTypeHelper;

///////////////////////////////////////////////////////////////////////////////
//
// class GivenCopyPipelineBuilder : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////


class GivenCopyPipelineBuilder : public GivenCopyPipelineResources
{
  public:

    GivenCopyPipelineBuilder() : component_(nullptr), systemServices_(nullptr), componentManager_(nullptr) {};

    virtual void SetUp() override;

    virtual void TearDown() override;

  protected:
    MockIResourceManagerClient                                              mockIResourceManagerClient_;
    MockIImagePersister                                                     mockIImagePersister_;
    MockIPageAssembler                                                      mockIPageAssembler_;
    MockIPrintDevice                                                        mockIPrintDevice_;
    MockIPrintIntentsFactory                                                mockIPrintIntentsFactory_;
    MockIResourceService                                                    mockIResourceService_;
    MockIMediaAttributes                                                    mockIMediaAttributes_;
    MockIScanDevice                                                         mockIScanDevice_;
    MockIScanPipeline                                                       mockIScanPipeline_{};
    MockIPrintMedia                                                         mockIPrintMedia_{};
    MockICopyAdapter                                                        mockICopyAdapter_{};
    MockIIPADevice                                                          mockIIPADevice_{};
    dune::copy::Jobs::Copy::CopyPipelineStandard                            * component_;
    TestSystemServices                                                      * systemServices_;
    dune::framework::component::IComponentManager                           * componentManager_;
    std::string                                                             productTestFileName{"./testResources/CopyPipelineStandardMMK.json"};                        
};

void GivenCopyPipelineBuilder::SetUp()
{
    
    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyPipelineStandardConfig.fbs", productTestFileName.c_str());

    component_ = new CopyPipelineStandard("CopyPipelineStandard");
    ASSERT_TRUE(component_ != nullptr);
}

void GivenCopyPipelineBuilder::TearDown()
{
    delete component_;
    delete systemServices_;
}

TEST_F(GivenCopyPipelineBuilder, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_);

    ASSERT_TRUE(true);
}

TEST_F(GivenCopyPipelineBuilder, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MockIIPADevice", &mockIIPADevice_);

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    ASSERT_TRUE(true);
}

TEST_F(GivenCopyPipelineBuilder, WhenGetComponentInstanceNameCalled_ItWillBeReturnedInstanceName)
{
    const char *instanceName_{"CopyPipelineStandard"};
    const char *instanceName = component_->getComponentInstanceName();
    ASSERT_STREQ(instanceName, instanceName_);
}

TEST_F(GivenCopyPipelineBuilder, WhenTheGetInterfaceIsCalled_TheComponentGetsICopyPipeline)
{
    const char *                        instanceName_{"CopyPipelineStandard"};
    IComponent * comp = static_cast<IComponent*>(component_);

    const char *instanceName = comp->getComponentInstanceName();
    ASSERT_STREQ(instanceName, instanceName_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));
    void* interfacePtr = comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), instanceName_);
    ASSERT_TRUE(nullptr != interfacePtr);
}

TEST_F(GivenCopyPipelineBuilder, WhenGetComponentFlavorUidCalled_ItWillBeReturnedFlavorUid)
{
    ComponentFlavorUid flavorUid = component_->getComponentFlavorUid();
    ASSERT_EQ(flavorUid, 0x5c2e52);
}

class GivenAConnectedCopyPipelineStandard :public GivenCopyPipelineBuilder
{
  public:

    GivenAConnectedCopyPipelineStandard() {};

    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenAConnectedCopyPipelineStandard::SetUp()
{
    productTestFileName = "./testResources/CopyPipelineStandardMMK.json";
    GivenCopyPipelineBuilder::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    services_.resourceManager = managerClient_.get();
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

void GivenAConnectedCopyPipelineStandard::TearDown()
{
    GivenCopyPipelineBuilder::TearDown();
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyPipelineStandardOfMMKReadyToCallShutdown : shutdown case.
// Dummy class that inherits from GivenAConnectedCopyPipelineStandardOfMMK in order to reuse code
// and enable parametrized tests. 
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyPipelineStandardOfMMKReadyToCallShutdown : public GivenAConnectedCopyPipelineStandard,
                           public ::testing::WithParamInterface<IComponent::ShutdownCause>
{

};


TEST_P(GivenAConnectedCopyPipelineStandardOfMMKReadyToCallShutdown, whenShutdownIsCalled_TheComponentGetsShutdown)
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

INSTANTIATE_TEST_CASE_P(InstantiationName, GivenAConnectedCopyPipelineStandardOfMMKReadyToCallShutdown, ::testing::Values(
 IComponent::ShutdownCause(IComponent::ShutdownCause::POWER_OFF),
 IComponent::ShutdownCause(IComponent::ShutdownCause::REBOOT),
 IComponent::ShutdownCause(IComponent::ShutdownCause::SEVERE_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::EMERGENCY_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::CRITICAL_ERROR)
));