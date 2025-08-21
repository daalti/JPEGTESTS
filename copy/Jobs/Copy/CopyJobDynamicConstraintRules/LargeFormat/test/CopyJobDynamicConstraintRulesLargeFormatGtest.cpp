/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormatGtest.cpp
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesLargeFormat.h"
#include "StringIds.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "TestSystemServices.h"
#include "GTestConfigHelper.h"
#include "EventSource.h"
#include "CopyJobTicket.h"
#include "MediaCdmHelper.h"

#include "CopyJobDynamicConstraintRulesLargeFormatConfig_generated.h"
#include "CopyJobConstraints_generated.h"

#include "MockILocale.h"
#include "MockICopyJobTicket.h"
#include "MockILocaleProvider.h"
#include "MockIMedia.h"
#include "MockICopyAdapter.h"

#include "IMedia.h"
#include "Media_generated.h"
#include "CopyJobDynamicConstraintRulesLargeFormatMapper.h"
#include "CopyJobDynamicConstraintRulesLargeFormatParserHelper.h"

using TestSystemServices                        = dune::framework::component::TestingUtil::TestSystemServices;
using IComponent                                = dune::framework::component::IComponent;
using IComponentManager                         = dune::framework::component::IComponentManager;
using SystemServices                            = dune::framework::component::SystemServices;
using SysTrace                                  = dune::framework::core::dbg::SysTrace;
using CheckpointLevel                           = SysTrace::CheckpointLevel;
using ColorModes                                = dune::cdm::jobTicket_1::ColorModes;
using ContentType                               = dune::cdm::jobTicket_1::ContentType;
using ScanMediaType                             = dune::cdm::glossary_1::ScanMediaType;
using DeviceState                               = dune::print::engine::DeviceState;
using DeviceStatus                              = dune::print::engine::DeviceStatus;
using IMedia                                    = dune::print::engine::IMedia;
using InputType                                 = dune::print::engine::InputType;
using MediaSource                               = dune::imaging::types::MediaSource;
using FinisherType                              = dune::print::engine::FinisherType;
using FoldingStyle                              = dune::print::engine::IMedia::ILargeFormatFolder::Properties::FoldingStyle;
using ILargeFormatFolder                        = dune::print::engine::IMedia::ILargeFormatFolder;
using MockILocale                       = dune::localization::MockILocale;
using MockILocaleProvider               = dune::localization::MockILocaleProvider;
using MockIMedia                        = dune::print::engine::MockIMedia;
using MockIMediaIInput                  = dune::print::engine::MockIMediaIInput;
using MockIMediaIInputRoll              = dune::print::engine::MockIMediaIInputRoll;
using MockIMediaILargeFormatFolder      = dune::print::engine::MockIMediaILargeFormatFolder;
using MockICopyAdapter                  = dune::copy::cdm::MockICopyAdapter;
using MockIMediaICutter                 = dune::print::engine::MockIMediaICutter;
using TrimmingStyles                    = dune::print::engine::IMedia::ICutter::Properties::TrimmingStyles;

using ReferenceEdge = dune::print::engine::ReferenceEdge;
using TrimmingWhen = dune::print::engine::TrimmingWhen;
using TrimmingType = dune::print::engine::TrimmingType;

using IMedia = dune::print::engine::IMedia;

using testing::_;
using testing::Return;
using testing::ReturnRef;
using ::testing::SetArgPointee;
using ::testing::WithArgs;

using namespace dune::framework::data::constraints;

///////////////////////////////////////////////////////////////////////////////
//
// class GivenANewCopyJobDynamicConstraintRulesLargeFormat : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenANewCopyJobDynamicConstraintRulesLargeFormat : public ::testing::Test
{
public:

    GivenANewCopyJobDynamicConstraintRulesLargeFormat() : systemServices_(nullptr), component_(nullptr),  componentManager_(nullptr) {};
    virtual void SetUp() override;

    virtual void TearDown() override;

    void createMockIMediaInputDevices();
    void createMockIFinishersDevices();
    void createMultipleMockIFinishersDevices();

    std::shared_ptr<MockIMediaIInputRoll> createMockIMediaIInputRoll(const std::vector<DeviceStatus>& status, MediaSource mediaSource);
    std::shared_ptr<IMedia::IFinisher> createMockIFinishersDevice();
    std::shared_ptr<IMedia::IFinisher> createMockIFInishersDeviceCutter();

    template<typename T>
    void checkConstraintResult(std::vector<T> expectedValidValues,std::shared_ptr<dune::framework::data::constraints::Constraints> constraints);
    void checkConstraintResultShort(std::vector<short> expectedValidValues,std::shared_ptr<dune::framework::data::constraints::Constraints> constraints);
    template<typename T>
    void checkValidValuesOnConstraintsIsEmpty(std::shared_ptr<dune::framework::data::constraints::Constraints> constraints);

    void checkIsLocked(std::shared_ptr<dune::framework::data::constraints::Constraints> constraints, bool expectedLocked = true);
    void unloadRolls();

    void invertStatusOnRolls();

    /**
     * @brief Method to generate a job ticket table
     * @return std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> result
     */
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> givenJobTicketTable();

    /**
     * @brief Method to generate a job ticket table with a copy intent as base
     * @param intent values expected to inject in job ticket table
     * @return std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> result
     */
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> givenJobTicketTable(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobIntent> intent);

    /**
     * @brief Method to generate an empty job ticket table
     * @return std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> 
     */
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> givenEmptyJobTicketTable();

    /**
     * @brief Generate mocks to call to job intent
     * @param copyIntent intent to setup
     */
    void givenJobTicketIntent(std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobIntent> copyIntent);

    /**
     * @brief Serialize data of intent into Print Table part
     * @param intent values expected to inject
     * @return std::unique_ptr<dune::cdm::jobTicket_1::PrintTable> result
     */
    std::unique_ptr<dune::cdm::jobTicket_1::PrintTable> serializePrintInfoTable(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobIntent> intent);

    std::shared_ptr<Constraints> getMediaStaticConstraints();
    std::shared_ptr<Constraints> getFoldingStyleStaticConstraints();
    std::shared_ptr<Constraints> getScaleToOutputStaticConstraints();
    std::shared_ptr<Constraints> getScaleSelectionStaticConstraints();
    std::shared_ptr<Constraints> getMediaDestinationStaticConstraints(bool isFolderAvailable);

protected:
    const char *                                                                        instanceName_{"CopyJobDynamicConstraintRules"};
    std::unique_ptr<TestSystemServices>                                                 systemServices_{nullptr};
    std::unique_ptr<dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat>   component_{nullptr};
    IComponent*                                                                         comp_{nullptr};
    dune::framework::component::IComponentManager*                                      componentManager_;
    std::shared_ptr<MockILocale>                                                        mockILocale_{};
    MockILocaleProvider                                                                 mockILocaleProvider_{};
    std::shared_ptr<MockIMedia>                                                         mockIMedia_{std::make_shared<MockIMedia>()};
    std::shared_ptr<MockICopyAdapter>                                                   mockICopyAdapter_{std::make_shared<MockICopyAdapter>()};
    dune::localization::StringId_Type                                                   localizationId{0};
    IMedia::InputList                                                                   inputList_{};
    std::map<int32_t, std::string>                                                      foldingStyleList_{{256, "Folding style 1"}, {259, "Folding style 2"}};
    std::map<MediaSource,std::shared_ptr<dune::framework::core::event::EventSource<IMedia::IInput, IMedia::InputSnapshotPtr>>> statusEventList_;  
    std::map<MediaSource,IMedia::InputRollSnapshotPtr>                                  snapshotPointerRollsMap_;
    std::map<MediaSource,std::shared_ptr<IMedia::InputRollSnapshot>>                    inputRollSnapshotsMap_;
    std::shared_ptr<MockIMediaIInputRoll>                                               mockInputRollOne_{nullptr};
    std::shared_ptr<MockIMediaIInputRoll>                                               mockInputRollTwo_{nullptr};
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket>                         mockICopyJobTicket_{nullptr};
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobIntent>                         jobIntent_{nullptr};
    std::shared_ptr<IMedia::IFinisher>                                                  mockIFinisher_{nullptr};
    std::shared_ptr<IMedia::IFinisher>                                                  mockICutter_{nullptr};
    MockIMediaILargeFormatFolder                                                        lfpFolderMock_;
    MockIMediaICutter                                                                   cutterMock_;
    std::shared_ptr<TrimmingStyles>                                                     trimmingStyle_;
    IMedia::CutterPtr                                                                   cutterPtr_;
    std::vector<std::shared_ptr<TrimmingStyles>>   styleVec_;
    IMedia::ICutter::Properties                    cutterProperties_;
    using FinisherStatusChangeEventSource = dune::framework::core::event::EventSource<IMedia::IFinisher, IMedia::FinisherSnapshotPtr>;
    FinisherStatusChangeEventSource                                                     finisherStatusChangeEvent_{&cutterMock_};
    IMedia::LargeFormatFolderPtr                                                        lfpFolderPtr_;
    IMedia::ILargeFormatFolder::Properties                                              lfpFolderProperties_;
    std::vector<FoldingStyle>                                                           lfpFoldingStyleVec_;
    IMedia::FinisherList                                                                finishers_;

    // Canvas table used on intent to not cause error 
    std::shared_ptr<dune::imaging::types::OutputCanvasT> outputCanvasTable_{nullptr};
};

void GivenANewCopyJobDynamicConstraintRulesLargeFormat::SetUp()
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/EmptyBaseDynamicContraintRules.json");

    component_ = std::make_unique<dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat>(instanceName_);
    ASSERT_TRUE(component_ != nullptr);
    comp_ = static_cast<IComponent*>(component_.get());

    mockILocale_ = std::make_shared<MockILocale>();
    ON_CALL(*mockILocale_, getStringIdForCsfOnly(_)).WillByDefault(Return(localizationId));
    ON_CALL(mockILocaleProvider_,deviceLocale()).WillByDefault(Return(mockILocale_));

    // fill here any setInterface required
    comp_->setInterface(GET_INTERFACE_UID(dune::localization::ILocaleProvider), "MockILocaleProvider",&mockILocaleProvider_);
    comp_->setInterface(GET_INTERFACE_UID(IMedia), "MockIMedia", mockIMedia_.get());
    comp_->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", mockICopyAdapter_.get());

    // Create mocks for IMediaInput
    createMockIMediaInputDevices();

    // initialize component
    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    jobIntent_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    mockICopyJobTicket_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();
}

void GivenANewCopyJobDynamicConstraintRulesLargeFormat::TearDown()
{
}

void GivenANewCopyJobDynamicConstraintRulesLargeFormat::createMockIMediaInputDevices()
{
    std::vector<DeviceStatus>  statusReady = {DeviceStatus::READY};
    mockInputRollOne_ = createMockIMediaIInputRoll(statusReady, MediaSource::ROLL1);

    std::vector<DeviceStatus>  statusOutOfMedia = {DeviceStatus::OUT_OF_MEDIA};
    mockInputRollTwo_ = createMockIMediaIInputRoll(statusOutOfMedia, MediaSource::ROLL2);

    inputList_ = { mockInputRollOne_, mockInputRollTwo_ };
    ON_CALL(*mockIMedia_, getInputDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputList_)));
}

std::shared_ptr<IMedia::IFinisher> GivenANewCopyJobDynamicConstraintRulesLargeFormat::createMockIFinishersDevice()
{
    ON_CALL(lfpFolderMock_, getType()).WillByDefault(Return(FinisherType::LFP_FOLDER));

    /* prepare the LargeFormatFolderPtr */
    lfpFolderPtr_ = IMedia::LargeFormatFolderPtr(&lfpFolderMock_, [](ILargeFormatFolder * p){} );
    ON_CALL(lfpFolderMock_, getLargeFormatFolder()).WillByDefault(Return(lfpFolderPtr_));

    /* set default folding styles */
    for (const auto & val : foldingStyleList_)
    {
        FoldingStyle style;
        style.setId(std::get<0>(val));
        style.setName(std::get<1>(val));
        lfpFoldingStyleVec_.emplace_back(style);
    }
    lfpFolderProperties_.setFoldingStyles(lfpFoldingStyleVec_);

    ON_CALL(lfpFolderMock_, getProperties()).WillByDefault(ReturnRef(lfpFolderProperties_));
    ON_CALL(lfpFolderMock_, getFoldingStyles()).WillByDefault(ReturnRef(lfpFoldingStyleVec_));

    return IMedia::FinisherPtr(&lfpFolderMock_, [](IMedia::IFinisher *) {});
}

std::shared_ptr<IMedia::IFinisher> GivenANewCopyJobDynamicConstraintRulesLargeFormat::createMockIFInishersDeviceCutter()
{
    /* set the default behaviour for get status change events */
    ON_CALL(cutterMock_, getFinisherStatusChangeEvent())
            .WillByDefault(ReturnRef(finisherStatusChangeEvent_));

    /* return CUTTER by default */
    ON_CALL(cutterMock_, getType()).WillByDefault(Return(FinisherType::CUTTER));

    /* prepare the CutterPtr */
    cutterPtr_ = IMedia::CutterPtr(&cutterMock_, [](IMedia::ICutter * p){} );
    ON_CALL(cutterMock_, getCutter()).WillByDefault(Return(cutterPtr_));

    /* prepare the cutter properties */
    trimmingStyle_ = std::make_shared<TrimmingStyles>();
    trimmingStyle_->setId(1);
    trimmingStyle_->setName("trim-after-pages");
    trimmingStyle_->setTrimmingOffsetInPageUnit(1416);
    trimmingStyle_->setReferenceEdge(ReferenceEdge::BOTTOM);
    trimmingStyle_->setTrimmingType(TrimmingType::FULL);
    trimmingStyle_->setTrimmingWhen(TrimmingWhen::AFTER_SHEETS);
    styleVec_.emplace_back(trimmingStyle_);

    cutterProperties_.setTrimmingStyles(styleVec_);
    cutterProperties_.setDefaultTrimmingStyleId(trimmingStyle_->getId());
    ON_CALL(cutterMock_, getProperties()).WillByDefault(ReturnRef(cutterProperties_));

    return IMedia::FinisherPtr(&cutterMock_, [](IMedia::IFinisher *) {});
}

void GivenANewCopyJobDynamicConstraintRulesLargeFormat::createMockIFinishersDevices()
{
    // override finishers list to only have lfp folder
    mockIFinisher_ = createMockIFinishersDevice();
    finishers_ = { mockIFinisher_ };
    ON_CALL(*mockIMedia_, getFinisherDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::OK, finishers_)));
}

void GivenANewCopyJobDynamicConstraintRulesLargeFormat::createMultipleMockIFinishersDevices()
{
    // override finishers list to have lfp folder and stacker
    mockIFinisher_ = createMockIFinishersDevice();
    mockICutter_ = createMockIFInishersDeviceCutter();
    finishers_ = { mockIFinisher_, mockICutter_ };
    ON_CALL(*mockIMedia_, getFinisherDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::OK, finishers_)));
}

std::shared_ptr<MockIMediaIInputRoll> GivenANewCopyJobDynamicConstraintRulesLargeFormat::createMockIMediaIInputRoll(
    const std::vector<DeviceStatus>& status, MediaSource mediaSource)
{
    // There is a ON_CALL getRoll() later where mockInputRoll is expected to return mockInputRoll
    // But this causes gtest to think there is a leak as the mockInputRoll 
    // because use count is higher than expected, meaning it isn't deleted properly.
    std::shared_ptr<MockIMediaIInputRoll> mockInputRoll = std::make_shared<MockIMediaIInputRoll>();
    std::shared_ptr<MockIMediaIInputRoll> mockInputRollAux = std::make_shared<MockIMediaIInputRoll>();

    // Create a roll ptr.
    IMedia::InputRollPtr inputRollPtr = IMedia::InputRollPtr(mockInputRollAux.get(), [](IMedia::IInputRoll *) {});

    DeviceState                state = DeviceState::OK;
    std::tuple<bool, uint32_t> levelPercentage{true, 50};

    // Create a snapshot from that roll.
    std::shared_ptr<IMedia::InputRollSnapshot> inputRollSnapshot = std::make_shared<IMedia::InputRollSnapshot>(inputRollPtr);

    // These aren't needed but I think it's a good idea to set them.
    inputRollSnapshot->setDeviceStatus(status);
    inputRollSnapshot->setDeviceState(state);
    inputRollSnapshot->setLevelPercentage(levelPercentage);
    inputRollSnapshotsMap_.insert(
        std::pair<MediaSource,std::shared_ptr<IMedia::InputRollSnapshot>>(mediaSource,inputRollSnapshot));
    
    IMedia::InputRollSnapshotPtr snapshotPtr = IMedia::InputRollSnapshotPtr(inputRollSnapshot.get(), [](IMedia::InputRollSnapshot*) {});
    snapshotPointerRollsMap_.insert(std::pair<MediaSource, IMedia::InputRollSnapshotPtr>(mediaSource,snapshotPtr));

    // Create status change event
    std::shared_ptr<dune::framework::core::event::EventSource<IMedia::IInput, IMedia::InputSnapshotPtr>> inputStatusChangeEvent
        = std::make_shared<dune::framework::core::event::EventSource<IMedia::IInput, IMedia::InputSnapshotPtr>>( mockInputRoll.get());
    dune::framework::core::event::EventSource<IMedia::IInput, IMedia::InputSnapshotPtr>* eventAsPointer = inputStatusChangeEvent.get();
    statusEventList_.insert(
        std::pair<MediaSource,std::shared_ptr<dune::framework::core::event::EventSource<IMedia::IInput, IMedia::InputSnapshotPtr>>>(
        mediaSource, inputStatusChangeEvent));

    ON_CALL( *mockInputRoll, getMediaSource())           .WillByDefault( Return   (mediaSource));
    ON_CALL( *mockInputRoll, getType())                  .WillByDefault( Return   (InputType::ROLL));
    ON_CALL( *mockInputRoll, getRoll())                  .WillByDefault( Return   (mockInputRollAux));
    ON_CALL( *mockInputRoll, getInputStatusChangeEvent()).WillByDefault( ReturnRef(*eventAsPointer));

    ON_CALL( *mockInputRollAux, getSnapShot()).WillByDefault(Return(std::tuple<APIResult, IMedia::InputRollSnapshotPtr>(APIResult::OK, snapshotPtr)));

    return mockInputRoll;
}

template<typename T>
void GivenANewCopyJobDynamicConstraintRulesLargeFormat::checkConstraintResult(std::vector<T> expectedValidValues,
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraints)
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
        ASSERT_EQ(expectedValidValues.size(), dynamicValidValues.size());

        for(auto expectedValue : expectedValidValues)
        {
            auto iteratorConstraintValues = std::find(dynamicValidValues.begin(), dynamicValidValues.end(), expectedValue);
            EXPECT_TRUE(iteratorConstraintValues != dynamicValidValues.end());
        }
    }
}
template<typename T>
void GivenANewCopyJobDynamicConstraintRulesLargeFormat::checkValidValuesOnConstraintsIsEmpty(
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraints)
{
    if(constraints != nullptr)
    {
        for(auto constraint : constraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
            {
                auto dynamicValidValues = (static_cast< dune::framework::data::constraints::ValidValuesEnum<T>*>(constraint))->getValidValues();
                EXPECT_TRUE(dynamicValidValues.empty());
                break;
            }
        }
    }
}
void GivenANewCopyJobDynamicConstraintRulesLargeFormat::checkConstraintResultShort(std::vector<short> expectedValidValues,
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraints)
{
    // Check Result for current type
    if(constraints != nullptr)
    {
        std::vector<short> dynamicValidValues;
        for(auto constraint : constraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_SHORT)
            {
                dynamicValidValues = (static_cast< dune::framework::data::constraints::ValidValuesShort*>(constraint))->getValidValues();
                break;
            }
        }

        // Check if number of constraints coincidence
        ASSERT_EQ(expectedValidValues.size(), dynamicValidValues.size());

        for(auto expectedValue : expectedValidValues)
        {
            auto iteratorConstraintValues = std::find(dynamicValidValues.begin(), dynamicValidValues.end(), expectedValue);
            EXPECT_TRUE(iteratorConstraintValues != dynamicValidValues.end());
        }
    }
}

void GivenANewCopyJobDynamicConstraintRulesLargeFormat::checkIsLocked(std::shared_ptr<dune::framework::data::constraints::Constraints> constraints, 
    bool expectedLocked)
{
    bool isLocked = false;

    if(constraints)
    {
        for(auto constraint : constraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::LOCK)
            {
                isLocked = true;
                break;
            }
        }
    }

    EXPECT_EQ(expectedLocked, isLocked);
}

void GivenANewCopyJobDynamicConstraintRulesLargeFormat::unloadRolls()
{
    // Iterate between rolls events
    for(auto pairStatusEvent : statusEventList_)
    {
        // Setup inverted status from setup
        std::vector<DeviceStatus> nextStatus;
        nextStatus.push_back(DeviceStatus::OUT_OF_MEDIA);

        // Create Auxiliar mocks
        std::shared_ptr<MockIMediaIInputRoll> mockInputRoll = std::make_shared<MockIMediaIInputRoll>();
        std::shared_ptr<MockIMediaIInputRoll> mockInputRollAux = std::make_shared<MockIMediaIInputRoll>();

        // Create a roll ptr.
        IMedia::InputRollPtr inputRollPtr = IMedia::InputRollPtr(mockInputRollAux.get(), [](IMedia::IInputRoll *) {});

        // Create a snapshot from that roll.
        std::shared_ptr<IMedia::InputRollSnapshot> inputRollSnapshot = std::make_shared<IMedia::InputRollSnapshot>(inputRollPtr);

        // Set values for set new snapshot
        DeviceState                state = DeviceState::OK;
        std::tuple<bool, uint32_t> levelPercentage{true, 50};
        inputRollSnapshot->setDeviceStatus(nextStatus);
        inputRollSnapshot->setDeviceState(state);
        inputRollSnapshot->setLevelPercentage(levelPercentage);        
        IMedia::InputRollSnapshotPtr snapshotPtr = IMedia::InputRollSnapshotPtr(inputRollSnapshot.get(), [](IMedia::InputRollSnapshot*) {});

        // After use snapshot on firesync action, shared pointer of snapshot will be removed when goes out of scope
        pairStatusEvent.second->fireSync(std::dynamic_pointer_cast<const dune::print::engine::IMedia::InputSnapshot>(snapshotPtr));
    }
}

void GivenANewCopyJobDynamicConstraintRulesLargeFormat::invertStatusOnRolls()
{
    // Iterate between rolls events
    for(auto pairStatusEvent : statusEventList_)
    {
        // Setup inverted status from setup
        std::vector<DeviceStatus> nextStatus;

        if(pairStatusEvent.first == MediaSource::ROLL1)
        {
            nextStatus.push_back(DeviceStatus::OUT_OF_MEDIA);
        }
        else
        {
            nextStatus.push_back(DeviceStatus::READY);
        }

        // Create Auxiliar mocks
        std::shared_ptr<MockIMediaIInputRoll> mockInputRoll = std::make_shared<MockIMediaIInputRoll>();
        std::shared_ptr<MockIMediaIInputRoll> mockInputRollAux = std::make_shared<MockIMediaIInputRoll>();

        // Create a roll ptr.
        IMedia::InputRollPtr inputRollPtr = IMedia::InputRollPtr(mockInputRollAux.get(), [](IMedia::IInputRoll *) {});

        // Create a snapshot from that roll.
        std::shared_ptr<IMedia::InputRollSnapshot> inputRollSnapshot = std::make_shared<IMedia::InputRollSnapshot>(inputRollPtr);

        // Set values for set new snapshot
        DeviceState                state = DeviceState::OK;
        std::tuple<bool, uint32_t> levelPercentage{true, 50};
        inputRollSnapshot->setDeviceStatus(nextStatus);
        inputRollSnapshot->setDeviceState(state);
        inputRollSnapshot->setLevelPercentage(levelPercentage);        
        IMedia::InputRollSnapshotPtr snapshotPtr = IMedia::InputRollSnapshotPtr(inputRollSnapshot.get(), [](IMedia::InputRollSnapshot*) {});

        // After use snapshot on firesync action, shared pointer of snapshot will be removed when goes out of scope
        pairStatusEvent.second->fireSync(std::dynamic_pointer_cast<const dune::print::engine::IMedia::InputSnapshot>(snapshotPtr));
    }
}

std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> GivenANewCopyJobDynamicConstraintRulesLargeFormat::givenJobTicketTable()
{
    // Setup intent base to use to serialization of info tables
    auto intent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    givenJobTicketIntent(intent);

    return givenJobTicketTable(intent);
}

std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> GivenANewCopyJobDynamicConstraintRulesLargeFormat::givenJobTicketTable(
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobIntent> intent)
{
    // Create a job ticket table with a non value rule currently supported
    auto serializedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    serializedJobTicketTable->beginMergePatch();
    serializedJobTicketTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    serializedJobTicketTable->src = *srcTable;
    serializedJobTicketTable->src.beginMergePatch();

    // src
    // src.scan
    //serializedJobTicketTable->src.get()->scan = *(serializeScanInfoTable(intent));
    serializedJobTicketTable->src.getMutable()->scan = *(dune::scan::Jobs::Scan::serializeScanInfoTable(intent));

    // pipelineOptions
    serializedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
    serializedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
    //pipelineOptions.imageModifications
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications = *(dune::scan::Jobs::Scan::serializeImageModsTable(intent));
    //pipelineOptions.manualUserOperations
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations = *(dune::scan::Jobs::Scan::serializeManualOpsTable(intent));
    //pipelineOptions.scaling
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling = *(dune::scan::Jobs::Scan::serializeScalingTable(intent));

    serializedJobTicketTable->pipelineOptions.getMutable()->generatePreview = (intent->getGeneratePreview())
        ? dune::cdm::glossary_1::FeatureEnabledEnum::Values::true_
        : dune::cdm::glossary_1::FeatureEnabledEnum::Values::false_;

    // dest
    auto destTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::DestTable>();
    serializedJobTicketTable->dest = *destTable;
    // dest.print
    serializedJobTicketTable->dest.getMutable()->print = *(serializePrintInfoTable(intent));

    return serializedJobTicketTable;
}

std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> GivenANewCopyJobDynamicConstraintRulesLargeFormat::givenEmptyJobTicketTable()
{
    // Setup job base update
    auto serializedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    serializedJobTicketTable->beginMergePatch();
    serializedJobTicketTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    // src
    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    serializedJobTicketTable->src = *srcTable;
    serializedJobTicketTable->src.beginMergePatch();

    // src
    // src.scan
    auto scanTable = std::make_unique<dune::cdm::jobTicket_1::ScanTable>();
    serializedJobTicketTable->src.getMutable()->scan = *(scanTable);
    serializedJobTicketTable->src.getMutable()->scan.beginMergePatch();

    // pipelineOptions
    serializedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
    serializedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
    //pipelineOptions.imageModifications
    auto imageModificationsTable = std::make_unique<dune::cdm::jobTicket_1::ImageModificationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications = *(imageModificationsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications.beginMergePatch();
    //pipelineOptions.manualUserOperations
    auto manualOpsTable = std::make_unique<dune::cdm::jobTicket_1::ManualUserOperationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations = *(manualOpsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.beginMergePatch();
    //pipelineOptions.scaling
    auto scalingTable = std::make_unique<dune::cdm::jobTicket_1::ScalingTable>();    
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling = *(scalingTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling.beginMergePatch();

    // dest
    auto destTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::DestTable>();
    serializedJobTicketTable->dest = *destTable;
    serializedJobTicketTable->dest.beginMergePatch();
    // dest.print
    auto printTable = std::make_unique<dune::cdm::jobTicket_1::PrintTable>();
    printTable->beginMergePatch();
    serializedJobTicketTable->dest.getMutable()->print = *(printTable);

    return serializedJobTicketTable;
}

void GivenANewCopyJobDynamicConstraintRulesLargeFormat::givenJobTicketIntent(
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobIntent> copyIntent)
{
    // Mock job ticket intent with non value currently supported
    EXPECT_CALL(*copyIntent, getOutputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A1));
    EXPECT_CALL(*copyIntent, getOutputMediaOrientation()).WillRepeatedly(Return(dune::imaging::types::MediaOrientation::LANDSCAPE));
    EXPECT_CALL(*copyIntent, getOutputMediaIdType()).WillRepeatedly(Return(dune::imaging::types::MediaIdType::BLUEPRINT));
    EXPECT_CALL(*copyIntent, getOutputMediaSource()).WillRepeatedly(Return(dune::imaging::types::MediaSource::ROLL2));
    EXPECT_CALL(*copyIntent, getOutputPlexMode()).WillRepeatedly(Return(dune::imaging::types::Plex::DUPLEX));
    EXPECT_CALL(*copyIntent, getOutputPlexBinding()).WillRepeatedly(Return(dune::imaging::types::PlexBinding::LONG_EDGE));
    EXPECT_CALL(*copyIntent, getCopies()).WillRepeatedly(Return(2));
    EXPECT_CALL(*copyIntent, getCollate()).WillRepeatedly(Return(dune::copy::SheetCollate::Uncollate));
    EXPECT_CALL(*copyIntent, getCopyQuality()).WillRepeatedly(Return(dune::imaging::types::PrintQuality::DRAFT));
    EXPECT_CALL(*copyIntent, getResize()).WillRepeatedly(Return(2));
    EXPECT_CALL(*copyIntent, getLighterDarker()).WillRepeatedly(Return(2));
    EXPECT_CALL(*copyIntent, getInputMediaSizeId()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A1));
    EXPECT_CALL(*copyIntent, getInputPlexMode()).WillRepeatedly(Return(dune::imaging::types::Plex::DUPLEX));
    EXPECT_CALL(*copyIntent, getOutputXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));
    EXPECT_CALL(*copyIntent, getOutputYResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));
    EXPECT_CALL(*copyIntent, getQualityMode()).WillRepeatedly(Return(dune::scan::types::AttachmentSize::LARGE));
    EXPECT_CALL(*copyIntent, getColorMode()).WillRepeatedly(Return(dune::imaging::types::ColorMode::BLACKANDWHITE));
    EXPECT_CALL(*copyIntent, getContentOrientation()).WillRepeatedly(Return(dune::imaging::types::ContentOrientation::PORTRAIT));
    EXPECT_CALL(*copyIntent, getBackSideContentOrientation()).WillRepeatedly(Return(dune::imaging::types::ContentOrientation::PORTRAIT));
    EXPECT_CALL(*copyIntent, getOriginalContentType()).WillRepeatedly(Return(dune::imaging::types::OriginalContentType::GLOSSY));
    EXPECT_CALL(*copyIntent, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::BLUEPRINTS));
    EXPECT_CALL(*copyIntent, getScanSource()).WillRepeatedly(Return(dune::scan::types::ScanSource::ADF_DUPLEX));
    EXPECT_CALL(*copyIntent, getXScalePercent()).WillRepeatedly(Return(50));
    EXPECT_CALL(*copyIntent, getYScalePercent()).WillRepeatedly(Return(50));
    EXPECT_CALL(*copyIntent, getScaleSelection()).WillRepeatedly(Return(dune::scan::types::ScanScaleSelectionEnum::A4TOLETTER));
    EXPECT_CALL(*copyIntent, getScaleToFitEnabled()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getGeneratePreview()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getAutoDeskew()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getScaleToSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::A1));
    EXPECT_CALL(*copyIntent, getScaleToOutput()).WillRepeatedly(Return(dune::imaging::types::MediaSource::ROLL2));
    EXPECT_CALL(*copyIntent, getScanFeedOrientation()).WillRepeatedly(Return(dune::scan::types::ScanFeedOrientation::LONGEDGE));
    EXPECT_CALL(*copyIntent, getScanXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));
    EXPECT_CALL(*copyIntent, getScanYResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));
    EXPECT_CALL(*copyIntent, getMultipickDetection()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getJobScanLimit()).WillRepeatedly(Return(2));
    EXPECT_CALL(*copyIntent, getAutoCrop()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getAutoTone()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getBlankPageDetection()).WillRepeatedly(Return(dune::scan::types::BlankDetectEnum::DetectAndSupress));
    EXPECT_CALL(*copyIntent, getBrightness()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getContrast()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getSharpen()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getXOffset()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getYOffset()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getXExtend()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getYExtend()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getBackgroundRemoval()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getBackgroundColorRemoval()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getBackgroundNoiseRemoval()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getBlackEnhancementLevel()).WillRepeatedly(Return(5));
    // EXPECT_CALL(*copyIntent, getOverScan()).WillRepeatedly(Return(dune::scan::types::OverScanType::MAX)); // Unsupported to test really, will never changes
    EXPECT_CALL(*copyIntent, getScanCaptureMode()).WillRepeatedly(Return(dune::scan::types::ScanCaptureModeType::BOOKMODE));
    EXPECT_CALL(*copyIntent, getScanImagingProfile()).WillRepeatedly(Return(dune::scan::types::ScanImagingProfileType::RAW_SCAN_CAPTURE));
    EXPECT_CALL(*copyIntent, getCcdChannel()).WillRepeatedly(Return(dune::scan::types::CcdChannelEnum::NTSC));
    EXPECT_CALL(*copyIntent, getBinaryRendering()).WillRepeatedly(Return(dune::scan::types::BinaryRenderingEnum::Halftone));
    EXPECT_CALL(*copyIntent, getDescreen()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getFeederPickStop()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getShadow()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getCompressionFactor()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getThreshold()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getScanAutoColorDetect()).WillRepeatedly(Return(dune::scan::types::AutoColorDetectEnum::TreatNonColorAsBlackAndWhite1));
    EXPECT_CALL(*copyIntent, getScanBlackBackground()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getScanNumberPages()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getScanAutoExposure()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getScanGamma()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getScanHighlight()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getScanColorSensitivity()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getScanColorRange()).WillRepeatedly(Return(5));
    EXPECT_CALL(*copyIntent, getScanPagesFlipUpEnabled()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getImagePreview()).WillRepeatedly(Return(dune::scan::types::ImagePreview::MakeOptional));
    EXPECT_CALL(*copyIntent, getPagesPerSheet()).WillRepeatedly(Return(dune::imaging::types::CopyOutputNumberUpCount::TwoUp));
    EXPECT_CALL(*copyIntent, getAutoRelease()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getScanAcquisitionsSpeed()).WillRepeatedly(Return(dune::scan::types::ScanAcquisitionsSpeedEnum::SLOW));
    EXPECT_CALL(*copyIntent, getEdgeToEdgeScan()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getLongPlotScan()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getPrintingOrder()).WillRepeatedly(Return(dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP));
    EXPECT_CALL(*copyIntent, getMediaFamily()).WillRepeatedly(Return(dune::imaging::types::MediaFamily::PHOTO));
    EXPECT_CALL(*copyIntent, getAutoRotate()).WillRepeatedly(Return(false));
    EXPECT_CALL(*copyIntent, getRotation()).WillRepeatedly(Return(static_cast<uint32_t>(0)));
    EXPECT_CALL(*copyIntent, getCopyMargins()).WillRepeatedly(Return(dune::imaging::types::CopyMargins::OVERSIZE));
    EXPECT_CALL(*copyIntent, getOutputDestination()).WillRepeatedly(Return(dune::imaging::types::MediaDestinationId::FOLDER2));
    EXPECT_CALL(*copyIntent, getInvertColors()).WillRepeatedly(Return(true));
    EXPECT_CALL(*copyIntent, getFoldingStyleId()).WillRepeatedly(Return(0));

    outputCanvasTable_ = std::make_shared<dune::imaging::types::OutputCanvasT>();    
    EXPECT_CALL(*copyIntent, getOutputCanvas()).WillRepeatedly(Return(*outputCanvasTable_));
}

std::unique_ptr<dune::cdm::jobTicket_1::PrintTable> GivenANewCopyJobDynamicConstraintRulesLargeFormat::serializePrintInfoTable(
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobIntent> intent)
{
    dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
    auto table = std::make_unique<dune::cdm::jobTicket_1::PrintTable>();
    table->beginMergePatch();

    table->copies = intent->getCopies();
    table->foldingStyleId = intent->getFoldingStyleId();
    table->collate = (intent->getCollate() == dune::copy::SheetCollate::Collate)
        ? dune::cdm::jobTicket_1::CollateModes::collated
        : dune::cdm::jobTicket_1::CollateModes::uncollated;
    
    table->mediaSource = dune::job::cdm::mapToCdm(intent->getOutputMediaSource()).toString();
    table->mediaSize = mediaCdmHelper.convertDuneMediaIdSizeToCdm(intent->getOutputMediaSizeId(), intent->getOutputMediaOrientation()).toString();
    table->mediaType = dune::job::cdm::mapToCdm(intent->getOutputMediaIdType()).toString();
    table->plexMode = dune::job::cdm::mapToCdm(intent->getOutputPlexMode());
    table->printingOrder = dune::job::cdm::mapToCdm(intent->getPrintingOrder());
    table->mediaFamily = dune::job::cdm::mapToCdm(intent->getMediaFamily());

    table->rotate = (intent->getAutoRotate())
        ? dune::job::cdm::mapToCdm(dune::imaging::types::Rotate::AUTO)
        : dune::job::cdm::mapToCdmRotate(intent->getRotation());

    table->printMargins = dune::job::cdm::mapToCdm(intent->getCopyMargins());
    table->mediaDestination = dune::job::cdm::mapToCdm(intent->getOutputDestination());
    table->duplexBinding = dune::job::cdm::mapToCdm(intent->getOutputPlexBinding());    
    table->printQuality = dune::job::cdm::mapToCdm(intent->getCopyQuality());

    return table;
}

std::shared_ptr<Constraints> GivenANewCopyJobDynamicConstraintRulesLargeFormat::getMediaStaticConstraints()
{     
    auto constraints = std::make_shared<Constraints>();

    std::vector<dune::cdm::glossary_1::MediaSourceId> enumMediaSources = {
        dune::cdm::glossary_1::MediaSourceId::auto_, 
        dune::cdm::glossary_1::MediaSourceId::roll_dash_1,
        dune::cdm::glossary_1::MediaSourceId::roll_dash_2
    };

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaSourceId>>(enumMediaSources, 
        &dune::cdm::glossary_1::MediaSourceId::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));
    
    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>>(enumMediaSources, 
        string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}
std::shared_ptr<Constraints> GivenANewCopyJobDynamicConstraintRulesLargeFormat::getScaleToOutputStaticConstraints()
{     
    auto constraints = std::make_shared<Constraints>();

    std::vector<dune::cdm::glossary_1::MediaSourceId> enumMediaSources = { 
        dune::cdm::glossary_1::MediaSourceId::roll_dash_1,
        dune::cdm::glossary_1::MediaSourceId::roll_dash_2
    };

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaSourceId>>(enumMediaSources, 
        &dune::cdm::glossary_1::MediaSourceId::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));
    
    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>>(enumMediaSources, 
        string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> GivenANewCopyJobDynamicConstraintRulesLargeFormat::getScaleSelectionStaticConstraints()
{     
    auto constraints = std::make_shared<Constraints>();

    std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection> enumScaleSelection = {
        dune::cdm::jobTicket_1::scaling::ScaleSelection::custom,
        dune::cdm::jobTicket_1::scaling::ScaleSelection::standardSizeScaling,
        dune::cdm::jobTicket_1::scaling::ScaleSelection::scaleToOutput
    };

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>>(enumScaleSelection, 
        &dune::cdm::jobTicket_1::scaling::ScaleSelection::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));
    
    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>>(enumScaleSelection, 
        string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> GivenANewCopyJobDynamicConstraintRulesLargeFormat::getFoldingStyleStaticConstraints()
{     
    auto staticConstraints = std::make_shared<Constraints>();

    std::vector<short> enumFoldingStyleSources = {0};

    auto enumValidValuesConstraint = std::make_unique<dune::framework::data::constraints::ValidValuesShort>(enumFoldingStyleSources, 
        string_id::cUndefined);
    auto enumPossibleValuesConstraint = std::make_unique<dune::framework::data::constraints::PossibleValuesShort>(enumFoldingStyleSources, 
        string_id::cUndefined);

    staticConstraints->add(std::move(enumValidValuesConstraint));
    staticConstraints->add(std::move(enumPossibleValuesConstraint));

    return staticConstraints;
}

std::shared_ptr<Constraints> GivenANewCopyJobDynamicConstraintRulesLargeFormat::getMediaDestinationStaticConstraints(bool isFolderAvailable)
{
    auto staticConstraints = std::make_shared<Constraints>();

    std::vector<dune::cdm::glossary_1::MediaDestinationId> enumMediaDestination = {dune::cdm::glossary_1::MediaDestinationId::stacker_dash_1};

    //Add folder if requested
    if(isFolderAvailable)
    {
        enumMediaDestination.push_back(dune::cdm::glossary_1::MediaDestinationId::folder_dash_1);
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>(enumMediaDestination, 
        &dune::cdm::glossary_1::MediaDestinationId::valueToString, string_id::cThisOptionUnavailable);
    staticConstraints->add(std::move(enumPossibleValueConstraint));
    
    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>(enumMediaDestination, 
        string_id::cThisOptionUnavailable);
    staticConstraints->add(std::move(enumValidValuesConstraint));

    return staticConstraints;
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesLargeFormat, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    comp_ = static_cast<IComponent*>(component_.get());
    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
}

TEST_F(GivenANewCopyJobDynamicConstraintRulesLargeFormat, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    comp_ = static_cast<IComponent*>(component_.get());

    comp_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_.get()));

    // fill here any setInterface required
    std::future<void> asyncCompletion;
    comp_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat :public GivenANewCopyJobDynamicConstraintRulesLargeFormat
{
  public:

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat() {};

    virtual void SetUp() override;

    virtual void TearDown() override;    

    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> givenEmptyJobTicketTableWithoutDest();
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> givenEmptyJobTicketTableWithoutPrint();

    std::vector<dune::cdm::glossary_1::MediaSourceId> expectedMediaConstraints_;
    std::vector<short> expectedFoldingStyleConstraints_;
    std::vector<dune::cdm::glossary_1::MediaDestinationId> expectedMediaDestinationConstraints_;
};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat::SetUp()
{
    GivenANewCopyJobDynamicConstraintRulesLargeFormat::SetUp();

    std::future<void> asyncCompletion;
    comp_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    expectedMediaConstraints_ = 
        {dune::cdm::glossary_1::MediaSourceId::auto_, dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat::TearDown()
{
    GivenANewCopyJobDynamicConstraintRulesLargeFormat::TearDown();
}

std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat::givenEmptyJobTicketTableWithoutDest()
{
    // Setup job base update
    auto serializedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    serializedJobTicketTable->beginMergePatch();
    serializedJobTicketTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    // src
    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    serializedJobTicketTable->src = *srcTable;
    serializedJobTicketTable->src.beginMergePatch();

    // src
    // src.scan
    auto scanTable = std::make_unique<dune::cdm::jobTicket_1::ScanTable>();
    serializedJobTicketTable->src.getMutable()->scan = *(scanTable);
    serializedJobTicketTable->src.getMutable()->scan.beginMergePatch();

    // pipelineOptions
    serializedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
    serializedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
    //pipelineOptions.imageModifications
    auto imageModificationsTable = std::make_unique<dune::cdm::jobTicket_1::ImageModificationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications = *(imageModificationsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications.beginMergePatch();
    //pipelineOptions.manualUserOperations
    auto manualOpsTable = std::make_unique<dune::cdm::jobTicket_1::ManualUserOperationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations = *(manualOpsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.beginMergePatch();
    //pipelineOptions.scaling
    auto scalingTable = std::make_unique<dune::cdm::jobTicket_1::ScalingTable>();    
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling = *(scalingTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling.beginMergePatch();

    return serializedJobTicketTable;
}

std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat::givenEmptyJobTicketTableWithoutPrint()
{
    // Setup job base update
    auto serializedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    serializedJobTicketTable->beginMergePatch();
    serializedJobTicketTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    // src
    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    serializedJobTicketTable->src = *srcTable;
    serializedJobTicketTable->src.beginMergePatch();

    // src
    // src.scan
    auto scanTable = std::make_unique<dune::cdm::jobTicket_1::ScanTable>();
    serializedJobTicketTable->src.getMutable()->scan = *(scanTable);
    serializedJobTicketTable->src.getMutable()->scan.beginMergePatch();

    // pipelineOptions
    serializedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
    serializedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
    //pipelineOptions.imageModifications
    auto imageModificationsTable = std::make_unique<dune::cdm::jobTicket_1::ImageModificationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications = *(imageModificationsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications.beginMergePatch();
    //pipelineOptions.manualUserOperations
    auto manualOpsTable = std::make_unique<dune::cdm::jobTicket_1::ManualUserOperationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations = *(manualOpsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.beginMergePatch();
    //pipelineOptions.scaling
    auto scalingTable = std::make_unique<dune::cdm::jobTicket_1::ScalingTable>();    
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling = *(scalingTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling.beginMergePatch();

    // dest
    auto destTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::DestTable>();
    serializedJobTicketTable->dest = *destTable;
    serializedJobTicketTable->dest.beginMergePatch();

    return serializedJobTicketTable;
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicket_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicket_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    // Setup static constraints
    expectedMediaConstraints_ = {dune::cdm::glossary_1::MediaSourceId::roll_dash_1,dune::cdm::glossary_1::MediaSourceId::roll_dash_2};
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoFoldingStylesAndConstraintsHaveZeroAndTicketHasStacker_ThenFoldingStyleValuesAreTwoAndLockedIsTrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::STACKER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {256, 259};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    createMockIFinishersDevices();

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoFoldingStylesButOneIsZeroAndConstraintsHaveZeroAndTicketHasStacker_ThenFoldingStyleValuesAreTwoAndLockedIsTrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::STACKER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0 , 256};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {{0, "Do Not Fold"}, {256, "Folding style 1"}};
    createMockIFinishersDevices();

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoFoldingStylesEmptyJobTicketTableWithoutDestination_ThenFoldingStyleValuesAreTwoAndLockedIstrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::STACKER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0 , 256};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {{0, "Do Not Fold"}, {256, "Folding style 1"}};
    createMockIFinishersDevices();

    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints, givenEmptyJobTicketTableWithoutDest());
    
    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints, true);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoFoldingStylesEmptyJobTicketTableWithoutPrint_ThenFoldingStyleValuesAreTwoAndLockedIstrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::STACKER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0 , 256};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {{0, "Do Not Fold"}, {256, "Folding style 1"}};
    createMockIFinishersDevices();

    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints, givenEmptyJobTicketTableWithoutPrint());
    
    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints, true);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoFoldingStylesEmptyJobTicketTable_ThenFoldingStyleValuesAreTwoAndLockedIstrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::STACKER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0 , 256};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {{0, "Do Not Fold"}, {256, "Folding style 1"}};
    createMockIFinishersDevices();

    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints, givenEmptyJobTicketTable());
    
    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints, true);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoFoldingStylesAndJobTicketTableWithMediaDestinationIdToFolder_ThenFoldingStyleValuesAreTwoAndLockedIsFalse)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::STACKER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0 , 256};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {{0, "Do Not Fold"}, {256, "Folding style 1"}};
    createMockIFinishersDevices();

    // Setup intent base to use to serialization of info tables
    auto intent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    givenJobTicketIntent(intent);
    EXPECT_CALL(*intent, getOutputDestination()).WillRepeatedly(Return(dune::imaging::types::MediaDestinationId::FOLDER2));

    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints, givenJobTicketTable(intent));
    
    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints, false);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoFoldingStylesAndJobTicketTableWithMediaDestinationIdToFolder_ThenFoldingStyleValuesAreTwoAndLockedIsTrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::STACKER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0 , 256};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {{0, "Do Not Fold"}, {256, "Folding style 1"}};
    createMockIFinishersDevices();

    // Setup intent base to use to serialization of info tables
    auto intent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    givenJobTicketIntent(intent);
    EXPECT_CALL(*intent, getOutputDestination()).WillRepeatedly(Return(dune::imaging::types::MediaDestinationId::STACKER));

    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints, givenJobTicketTable(intent));
    
    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat,
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithoutFoldingStylesAndConstraintsHaveZeroAndTicketHasStacker_ThenFoldingStyleValuesIsZeroAndLockedIsTrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::STACKER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {};
    createMockIFinishersDevices();

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithoutFoldingStylesAndNoStaticConstraints_ThenFoldingStyleValuesAreNull)
{   
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();

    foldingStyleList_ = {};
    createMockIFinishersDevices();

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    EXPECT_EQ(nullptr, constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedAndNoStaticConstraints_ThenFoldingStyleValuesAreNull)
{   
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();

    createMockIFinishersDevices();

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    EXPECT_EQ(nullptr, constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoFoldingStylesAndConstraintsHaveZeroAndTicketHasFolder_ThenFoldingStyleValuesAreTwoAndLockedIsTrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::FOLDER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {256, 259};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    createMockIFinishersDevices();

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints, false);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoFoldingStylesButOneIsZeroAndConstraintsHaveZeroAndTicketHasFolder_ThenFoldingStyleValuesAreTwoAndLockedIsTrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::FOLDER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0 , 256};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {{0, "Do Not Fold"}, {256, "Folding style 1"}};
    createMockIFinishersDevices();

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints, false);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithTwoDevicesAndTwoFoldingStylesButOneIsZeroAndConstraintsHaveZeroAndTicketHasFolder_ThenFoldingStyleValuesAreTwoAndLockedIsTrue)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::FOLDER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0 , 256};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {{0, "Do Not Fold"}, {256, "Folding style 1"}};
    
    createMultipleMockIFinishersDevices();

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints, false);
}


TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsMockedWithoutFoldingStylesAndConstraintsHaveZeroAndTicketHasFolder_ThenFoldingStyleValuesIsZeroAndLockedIsFalse)
{   
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::FOLDER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {};
    createMockIFinishersDevices();

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints, false);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenGetDynamicConstraintsIsCalledAndFinishersIsNotConnectedAndMockedOneFoldingStyleAndConstraintsHaveZeroAndTicketHasFolder_ThenFoldingStyleValuesIsZeroAndLockedIsFalse)
{
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::FOLDER));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));
    
    expectedFoldingStyleConstraints_ = {0};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    foldingStyleList_ = {{256, "Folding style 1"}};
    createMockIFinishersDevices();

    IMedia::LargeFormatFolderSnapshot largeFormatFolderSnapshot(lfpFolderPtr_);
    std::vector<DeviceStatus> status = {DeviceStatus::NOT_INSTALLED};
    largeFormatFolderSnapshot.setDeviceStatus(status);
    const IMedia::LargeFormatFolderSnapshotPtr pLargeFormatFolderSnapshot = 
        IMedia::LargeFormatFolderSnapshotPtr(&largeFormatFolderSnapshot,
                                             [](IMedia::LargeFormatFolderSnapshot *){});
    /* prepare the LargeFormatFolderSnapshot value */
    auto deviceTuple = std::make_tuple(APIResult::OK, pLargeFormatFolderSnapshot);
    EXPECT_CALL(lfpFolderMock_, getSnapShot()).WillRepeatedly(Return(deviceTuple));
    
    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for foldingStyleId
    auto constraints = staticConstraints->getConstraints("dest/print/foldingStyleId");
    
    checkConstraintResultShort(expectedFoldingStyleConstraints_, constraints);
    checkIsLocked(constraints, false);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    // Change status on event
    unloadRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateUndefinedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));

    // Change status on event
    unloadRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateReadyAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    // Expected media constraint changes
    expectedMediaConstraints_ = {dune::cdm::glossary_1::MediaSourceId::auto_};

    // Change status on event
    unloadRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    // Expected media constraint changes
    std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection> expectedMediaConstraintsScaleSelection = {
        dune::cdm::jobTicket_1::scaling::ScaleSelection::standardSizeScaling,
        dune::cdm::jobTicket_1::scaling::ScaleSelection::custom,
        dune::cdm::jobTicket_1::scaling::ScaleSelection::scaleToOutput
    };

    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    unloadRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);
    auto scaleSelectionStaticConstraints = getScaleSelectionStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleSelection", scaleSelectionStaticConstraints);
    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);

    constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleSelection");
    checkConstraintResult<dune::cdm::jobTicket_1::scaling::ScaleSelection>(expectedMediaConstraintsScaleSelection,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateUndefinedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));
    // Expected media constraint changes
    std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection> expectedMediaConstraintsScaleSelection = {
        dune::cdm::jobTicket_1::scaling::ScaleSelection::standardSizeScaling,
        dune::cdm::jobTicket_1::scaling::ScaleSelection::custom,
        dune::cdm::jobTicket_1::scaling::ScaleSelection::scaleToOutput
    };

    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    unloadRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);
    auto scaleSelectionStaticConstraints = getScaleSelectionStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleSelection", scaleSelectionStaticConstraints);
    
    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);

    constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleSelection");
    checkConstraintResult<dune::cdm::jobTicket_1::scaling::ScaleSelection>(expectedMediaConstraintsScaleSelection,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateReadyAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));

    // Expected media constraint changes
    std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection> expectedMediaConstraintsScaleSelection = {
        dune::cdm::jobTicket_1::scaling::ScaleSelection::standardSizeScaling,
        dune::cdm::jobTicket_1::scaling::ScaleSelection::custom
    };

    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    unloadRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);
    auto scaleSelectionStaticConstraints = getScaleSelectionStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleSelection", scaleSelectionStaticConstraints);
    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);

    constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleSelection");
    checkConstraintResult<dune::cdm::jobTicket_1::scaling::ScaleSelection>(expectedMediaConstraintsScaleSelection,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateUndefinedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateReadyAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    // Expected media constraint changes
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::auto_, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateUndefinedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));

    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateReadyAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    // Expected media constraint changes
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndFolderIsNotAvailableAndDirectCopyMode_ThenMediaDestinationConstraintsDoNotChange)
{
    ON_CALL(*mockICopyAdapter_, getCopyMode()).WillByDefault(Return(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning));
    // Expected media constraint changes
    expectedMediaDestinationConstraints_ = {dune::cdm::glossary_1::MediaDestinationId::stacker_dash_1};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaDestinationStaticConstraints = getMediaDestinationStaticConstraints(false);
    staticConstraints->set("dest/print/mediaDestination", mediaDestinationStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr, staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("dest/print/mediaDestination");
    checkConstraintResult<dune::cdm::glossary_1::MediaDestinationId>(expectedMediaDestinationConstraints_, constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndFolderIsAvailableAndInDirectCopyMode_ThenMediaDestinationConstraintsDoNotChange)
{
    ON_CALL(*mockICopyAdapter_, getCopyMode()).WillByDefault(Return(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning));
    // Expected media constraint changes
    expectedMediaDestinationConstraints_ = {
        dune::cdm::glossary_1::MediaDestinationId::stacker_dash_1, 
        dune::cdm::glossary_1::MediaDestinationId::folder_dash_1
    };

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaDestinationStaticConstraints = getMediaDestinationStaticConstraints(true);
    staticConstraints->set("dest/print/mediaDestination", mediaDestinationStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr, staticConstraints);

    // Check Result for mediaDestination
    auto constraints = staticConstraints->getConstraints("dest/print/mediaDestination");
    checkConstraintResult<dune::cdm::glossary_1::MediaDestinationId>(expectedMediaDestinationConstraints_, constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndFolderIsAvailableAndDirectCopyModeWithNullTicket_ThenMediaDestinationConstraintsDoNotChange)
{
    ON_CALL(*mockICopyAdapter_, getCopyMode()).WillByDefault(Return(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning));
    // Expected media constraint changes
    expectedMediaDestinationConstraints_ = {
        dune::cdm::glossary_1::MediaDestinationId::stacker_dash_1, 
        dune::cdm::glossary_1::MediaDestinationId::folder_dash_1
    };

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaDestinationStaticConstraints = getMediaDestinationStaticConstraints(true);
    staticConstraints->set("dest/print/mediaDestination", mediaDestinationStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr, staticConstraints);

    // Check Result for mediaDestination
    auto constraints = staticConstraints->getConstraints("dest/print/mediaDestination");
    checkConstraintResult<dune::cdm::glossary_1::MediaDestinationId>(expectedMediaDestinationConstraints_, constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndFolderIsAvailableAndDirectCopyModeWithoutJobStateInitialized_ThenMediaDestinationConstraintsDoNotChange)
{
    ON_CALL(*mockICopyAdapter_, getCopyMode()).WillByDefault(Return(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning));
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));
    // Expected media constraint changes
    expectedMediaDestinationConstraints_ = {
        dune::cdm::glossary_1::MediaDestinationId::stacker_dash_1, 
        dune::cdm::glossary_1::MediaDestinationId::folder_dash_1
    };

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaDestinationStaticConstraints = getMediaDestinationStaticConstraints(true);
    staticConstraints->set("dest/print/mediaDestination", mediaDestinationStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_, staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("dest/print/mediaDestination");
    checkConstraintResult<dune::cdm::glossary_1::MediaDestinationId>(expectedMediaDestinationConstraints_, constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat, 
    WhenCallToGetDynamicConstraintsIsCalledAndFolderIsAvailableAndDirectCopyModeWithJobStateInitialized_ThenMediaDestinationFolderIsRemovedFromConstraints)
{
    ON_CALL(*mockICopyAdapter_, getCopyMode()).WillByDefault(Return(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning));
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    // Expected media constraint changes
    expectedMediaDestinationConstraints_ = {dune::cdm::glossary_1::MediaDestinationId::stacker_dash_1};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaDestinationStaticConstraints = getMediaDestinationStaticConstraints(true);
    staticConstraints->set("dest/print/mediaDestination", mediaDestinationStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_, staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("dest/print/mediaDestination");
    checkConstraintResult<dune::cdm::glossary_1::MediaDestinationId>(expectedMediaDestinationConstraints_, constraints);
}

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot : public GivenANewCopyJobDynamicConstraintRulesLargeFormat
{
  public:

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    void createMockIMediaInputDevicesWithNullptrSnapshot();

    std::shared_ptr<MockIMediaIInputRoll> createMockIMediaIInputRollNullptrSnapshot(MediaSource mediaSource);

    std::vector<dune::cdm::glossary_1::MediaSourceId> expectedMediaConstraints_;

};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot::SetUp()
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/EmptyBaseDynamicContraintRules.json");

    component_ = std::make_unique<dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat>(instanceName_);
    ASSERT_TRUE(component_ != nullptr);
    comp_ = static_cast<IComponent*>(component_.get());

    mockILocale_ = std::make_shared<MockILocale>();
    ON_CALL(*mockILocale_, getStringIdForCsfOnly(_)).WillByDefault(Return(localizationId));
    ON_CALL(mockILocaleProvider_,deviceLocale()).WillByDefault(Return(mockILocale_));

    // fill here any setInterface required
    comp_->setInterface(GET_INTERFACE_UID(dune::localization::ILocaleProvider), "MockILocaleProvider",&mockILocaleProvider_);
    comp_->setInterface(GET_INTERFACE_UID(IMedia), "MockIMedia", mockIMedia_.get());
    comp_->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", mockICopyAdapter_.get());

    // Create mocks for IMediaInput
    createMockIMediaInputDevicesWithNullptrSnapshot();

    // initialize component
    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    std::future<void> asyncCompletion;
    comp_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
    expectedMediaConstraints_= 
        {dune::cdm::glossary_1::MediaSourceId::auto_, dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};
    mockICopyJobTicket_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot::TearDown()
{
    GivenANewCopyJobDynamicConstraintRulesLargeFormat::TearDown();
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot::createMockIMediaInputDevicesWithNullptrSnapshot()
{
    std::shared_ptr<MockIMediaIInputRoll> mockInputRollOne_ = createMockIMediaIInputRollNullptrSnapshot(MediaSource::ROLL1);

    std::vector<DeviceStatus>  statusOutOfMedia = {DeviceStatus::OUT_OF_MEDIA};
    std::shared_ptr<MockIMediaIInputRoll> mockInputRollTwo_ = createMockIMediaIInputRoll(statusOutOfMedia, MediaSource::ROLL2);

    inputList_ = { mockInputRollOne_, mockInputRollTwo_ };
    ON_CALL(*mockIMedia_, getInputDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputList_)));
}

std::shared_ptr<MockIMediaIInputRoll> 
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot::createMockIMediaIInputRollNullptrSnapshot(MediaSource mediaSource)
{
    // There is a ON_CALL getRoll() later where mockInputRoll is expected to return mockInputRoll
    // But this causes gtest to think there is a leak as the mockInputRoll 
    // because use count is higher than expected, meaning it isn't deleted properly.
    std::shared_ptr<MockIMediaIInputRoll> mockInputRoll = std::make_shared<MockIMediaIInputRoll>();
    std::shared_ptr<MockIMediaIInputRoll> mockInputRollAux = std::make_shared<MockIMediaIInputRoll>();

    // Create status change event
    std::shared_ptr<dune::framework::core::event::EventSource<IMedia::IInput, IMedia::InputSnapshotPtr>> inputStatusChangeEvent
        = std::make_shared<dune::framework::core::event::EventSource<IMedia::IInput, IMedia::InputSnapshotPtr>>( mockInputRoll.get());
    dune::framework::core::event::EventSource<IMedia::IInput, IMedia::InputSnapshotPtr>* eventAsPointer = inputStatusChangeEvent.get();
    statusEventList_.insert(
        std::pair<MediaSource,std::shared_ptr<dune::framework::core::event::EventSource<IMedia::IInput, IMedia::InputSnapshotPtr>>>(
        mediaSource,inputStatusChangeEvent));

    ON_CALL( *mockInputRoll, getMediaSource() ).WillByDefault( Return( mediaSource ) );
    ON_CALL( *mockInputRoll, getType()        ).WillByDefault( Return( InputType::ROLL ) );
    ON_CALL( *mockInputRoll, getRoll()        ).WillByDefault( Return( mockInputRollAux ) );
    ON_CALL( *mockInputRoll, getInputStatusChangeEvent()).WillByDefault(ReturnRef(*eventAsPointer));

    ON_CALL( *mockInputRollAux, getSnapShot()).WillByDefault(Return(std::tuple<APIResult, IMedia::InputRollSnapshotPtr>(APIResult::OK, nullptr)));

    return mockInputRoll;
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicket_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_, constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateUndefinedAndMediaIsMockedAndNoConstraintsToCheckOnTicket_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateReadyAndMediaIsMockedAndNoConstraintsToCheckOnTicket_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    expectedMediaConstraints_ = {dune::cdm::glossary_1::MediaSourceId::auto_};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicket_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    expectedMediaConstraints_ = {dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};
    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_, constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateUndefinedAndMediaIsMockedAndNoConstraintsToCheckOnTicket_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));
    expectedMediaConstraints_ = {dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};
    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateReadyAndMediaIsMockedAndNoConstraintsToCheckOnTicket_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    expectedMediaConstraints_ = {dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};
    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    // Change status on event
    unloadRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateUndefinedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));

    // Change status on event
    unloadRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndJobStateReadyAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    
    // Expected media constraint changes
    expectedMediaConstraints_ = {dune::cdm::glossary_1::MediaSourceId::auto_};
    
    // Change status on event
    unloadRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    // Change status on event
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateUndefinedAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));
    // Change status on event
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateReadyAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatusAllUnloaded_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    // Change status on event
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    // Expected media constraint changes
    expectedMediaConstraints_= {
        dune::cdm::glossary_1::MediaSourceId::auto_, 
        dune::cdm::glossary_1::MediaSourceId::roll_dash_1, 
        dune::cdm::glossary_1::MediaSourceId::roll_dash_2
    };

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateUndefinedAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));
    // Expected media constraint changes
    expectedMediaConstraints_= {
        dune::cdm::glossary_1::MediaSourceId::auto_, 
        dune::cdm::glossary_1::MediaSourceId::roll_dash_1, 
        dune::cdm::glossary_1::MediaSourceId::roll_dash_2
    };

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateReadyAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForOutputCanvasMediaIdReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    // Expected media constraint changes
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::auto_, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getMediaStaticConstraints();
    staticConstraints->set("pipelineOptions/imageModifications/outputCanvasMediaId", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for outputCanvasMediaId
    auto constraints = staticConstraints->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    // Expected media constraint changes
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(nullptr,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateUndefinedAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::UNDEFINED));
    // Expected media constraint changes
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_1, dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatMediaMockWithNullptrSnapshot, 
    WhenCallToGetDynamicConstraintsIsCalledAndJobStateReadyAndMediaIsMockedAndNoConstraintsToCheckOnTicketAndForcedChangesOnMediaStatus_ThenMediaRelatedConstraintForScaleToOutputReturnExpected)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));
    // Expected media constraint changes
    expectedMediaConstraints_={dune::cdm::glossary_1::MediaSourceId::roll_dash_2};

    // Change status on event
    invertStatusOnRolls();

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto mediaStaticConstraints = getScaleToOutputStaticConstraints();
    staticConstraints->set("pipelineOptions/scaling/scaleToOutput", mediaStaticConstraints);

    // Execute getter
    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check Result for scaleToOutput
    auto constraints = staticConstraints->getConstraints("pipelineOptions/scaling/scaleToOutput");
    checkConstraintResult<dune::cdm::glossary_1::MediaSourceId>(expectedMediaConstraints_,constraints);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatReadyToCallShutdown : shutdown case.
// Dummy class that inherits from GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat in order to reuse code
// and enable parametrized tests. 
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatReadyToCallShutdown : public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat,
    public ::testing::WithParamInterface<IComponent::ShutdownCause>
{
};

TEST_P(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatReadyToCallShutdown, whenShutdownIsCalled_TheComponentGetsShutdown)
{
    comp_ = static_cast<IComponent*>(component_.get());

    // Call GetParam() here to get the Row values
    IComponent::ShutdownCause const& p = GetParam();

    std::future<void> asyncCompletion;
    comp_->shutdown(p, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

INSTANTIATE_TEST_CASE_P(InstantiationName, GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatReadyToCallShutdown, ::testing::Values(
    IComponent::ShutdownCause(IComponent::ShutdownCause::POWER_OFF),
    IComponent::ShutdownCause(IComponent::ShutdownCause::REBOOT),
    IComponent::ShutdownCause(IComponent::ShutdownCause::SEVERE_ERROR),
    IComponent::ShutdownCause(IComponent::ShutdownCause::EMERGENCY_ERROR),
    IComponent::ShutdownCause(IComponent::ShutdownCause::CRITICAL_ERROR)
));

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////

class GivenACopyJobDynamicConstraintRulesLargeFormatWithConstraintGroup :public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat
{
public:

    GivenACopyJobDynamicConstraintRulesLargeFormatWithConstraintGroup() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup_;
};

void GivenACopyJobDynamicConstraintRulesLargeFormatWithConstraintGroup::SetUp()
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/CopyJobDynamicConstraintRulesLargeFormatTestData.json");

    component_ = std::make_unique<dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat>(instanceName_);
    ASSERT_TRUE(component_ != nullptr);
    comp_ = static_cast<IComponent*>(component_.get());

    mockILocale_ = std::make_shared<MockILocale>();
    ON_CALL(*mockILocale_, getStringIdForCsfOnly(_)).WillByDefault(Return(localizationId));
    ON_CALL(mockILocaleProvider_,deviceLocale()).WillByDefault(Return(mockILocale_));

    // fill here any setInterface required
    comp_->setInterface(GET_INTERFACE_UID(dune::localization::ILocaleProvider), "MockILocaleProvider",&mockILocaleProvider_);
    comp_->setInterface(GET_INTERFACE_UID(IMedia), "MockIMedia", mockIMedia_.get());
    comp_->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", mockICopyAdapter_.get());

    // Create mocks for IMediaInput
    createMockIMediaInputDevices();

    // initialize component
    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    std::future<void> asyncCompletion;
    comp_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    expectedMediaConstraints_= {dune::cdm::glossary_1::MediaSourceId::auto_, dune::cdm::glossary_1::MediaSourceId::roll_dash_1};

    constraintsGroup_ = std::make_shared<dune::framework::data::constraints::ConstraintsGroup>();
    mockICopyJobTicket_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();

    //Create a simulated constraint to add it in the constraints group
    auto newConstraint = std::make_shared<dune::framework::data::constraints::Constraints>();
    
    // Define possible values
    auto enumPossibleValues = { dune::cdm::glossary_1::FeatureEnabled::true_, dune::cdm::glossary_1::FeatureEnabled::false_ };
    auto enumPossibleValueConstraint =
        std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(enumPossibleValues, 
        &dune::cdm::glossary_1::FeatureEnabledEnum::valueToString, dune::localization::string_id::cThisOptionUnavailable);
    newConstraint->add(std::move(enumPossibleValueConstraint));
    
    // Define valid values
    auto invertColorOptions = std::vector<dune::cdm::glossary_1::FeatureEnabled>();
    invertColorOptions.push_back(dune::cdm::glossary_1::FeatureEnabled::false_);
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(invertColorOptions, 
        dune::localization::string_id::cThisOptionUnavailable);
    newConstraint->add(std::move(enumValidValuesConstraint));

    constraintsGroup_->set("src/scan/autoDeskew", newConstraint);

}

void GivenACopyJobDynamicConstraintRulesLargeFormatWithConstraintGroup::TearDown()
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormat::TearDown();
}

TEST_F(GivenACopyJobDynamicConstraintRulesLargeFormatWithConstraintGroup, WhenCopyJobIsNotInProcessingState_ThenTheSettingIsNotLocked)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::READY));

    component_->updateWithJobDynamicConstraints(mockICopyJobTicket_, constraintsGroup_);

    bool locked = false;
    //Check if the lock has been added
    auto constraints = constraintsGroup_->getConstraints("src/scan/autoDeskew");
    for (auto &constraint : constraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::LOCK)
        {
            locked = true;
        }
    }

    EXPECT_FALSE(locked);
}

TEST_F(GivenACopyJobDynamicConstraintRulesLargeFormatWithConstraintGroup, WhenCopyJobIsInProcessingState_ThenTheSettingIsLocked)
{
    ON_CALL(*mockICopyJobTicket_, getState()).WillByDefault(Return(dune::job::JobStateType::PROCESSING));

    component_->updateWithJobDynamicConstraints(mockICopyJobTicket_, constraintsGroup_);

    bool locked = false;
    //Check if the lock has been added
    auto constraints = constraintsGroup_->getConstraints("src/scan/autoDeskew");
    for (auto &constraint : constraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::LOCK)
        {
            locked = true;
        }
    }

    EXPECT_TRUE(locked);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase : Base case.
//
///////////////////////////////////////////////////////////////////////////////
class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase : public GivenANewCopyJobDynamicConstraintRulesLargeFormat
{
public:

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase() : GivenANewCopyJobDynamicConstraintRulesLargeFormat() {};

    virtual void SetUp() override;

    // virtual void TearDown() override;

    template<typename CdmType>
    std::shared_ptr<Constraints> createConstraintEnum(CdmType value);
    template<typename CdmType>
    std::shared_ptr<Constraints> createConstraintEnum(std::vector<CdmType> vectorValues);
    std::shared_ptr<Constraints> createConstraintShort(std::vector<short> vectorValues);
    std::shared_ptr<Constraints> createConstraintFeatureEnabledEnum(dune::cdm::glossary_1::FeatureEnabled value);
    std::shared_ptr<Constraints> createConstraintFeatureEnabledEnum();
    std::shared_ptr<Constraints> createConstraintRange(int32_t uniqueValueExpected);
    std::shared_ptr<Constraints> createConstraintRange(double uniqueValueExpected);
    std::shared_ptr<Constraints> createConstraintRange(int32_t minValueExpected, int32_t maxValueExpected, int32_t stepValueExpected);
    std::shared_ptr<Constraints> createConstraintRange(double minValueExpected, double maxValueExpected, double stepValueExpected);

};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::SetUp()
{
    GTEST_CHECKPOINTA("GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::SetUp -- ENTER\n");

    // NOT Set Up from parent

    component_ = std::make_unique<dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat>(instanceName_);
    ASSERT_TRUE(component_ != nullptr);    
    comp_ = static_cast<IComponent*>(component_.get());

    // fill here any setInterface required
    mockILocale_ = std::make_shared<MockILocale>();
    ON_CALL(*mockILocale_, getStringIdForCsfOnly(_)).WillByDefault(Return(localizationId));
    ON_CALL(mockILocaleProvider_,deviceLocale()).WillByDefault(Return(mockILocale_));
    ON_CALL(*mockIMedia_, getInputDevices(_)).WillByDefault(Return(std::make_tuple(APIResult::OK, inputList_)));

    // Mock response from ticket
    jobIntent_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    ON_CALL(*jobIntent_, getOriginalMediaType()).WillByDefault(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    mockICopyJobTicket_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));

    // fill here any setInterface required
    comp_->setInterface(GET_INTERFACE_UID(dune::localization::ILocaleProvider), "MockILocaleProvider",&mockILocaleProvider_);
    comp_->setInterface(GET_INTERFACE_UID(IMedia), "MockIMedia", (void*)mockIMedia_.get());
    comp_->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", mockICopyAdapter_.get());
}
template<typename CdmType>
std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::createConstraintEnum(CdmType value)
{
    auto constraints = std::make_shared<Constraints>();
    std::vector<CdmType> validValues = {value};

    // As far as I know, we wouldn't disable any of these content types, but I could be wrong.
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<CdmType>>(validValues, &CdmType::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<CdmType>>(validValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    return constraints;
}

std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::createConstraintShort(std::vector<short> vectorValues)
{
    auto constraints = std::make_shared<Constraints>();

    // As far as I know, we wouldn't disable any of these content types, but I could be wrong.
    auto enumPossibleValueConstraint = std::make_unique<dune::framework::data::constraints::ValidValuesShort>(vectorValues, 
        string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<dune::framework::data::constraints::PossibleValuesShort>(vectorValues, 
        string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    return constraints;
}

template<typename CdmType>
std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::createConstraintEnum(std::vector<CdmType> vectorValues)
{
    auto constraints = std::make_shared<Constraints>();

    // As far as I know, we wouldn't disable any of these content types, but I could be wrong.
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<CdmType>>(vectorValues, &CdmType::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<CdmType>>(vectorValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    return constraints;
}

std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::createConstraintFeatureEnabledEnum(
    dune::cdm::glossary_1::FeatureEnabled value)
{
    auto constraints = std::make_shared<Constraints>();
    std::vector<dune::cdm::glossary_1::FeatureEnabled> validValues = {value};

    // As far as I know, we wouldn't disable any of these content types, but I could be wrong.
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(validValues, 
        &dune::cdm::glossary_1::FeatureEnabledEnum::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(validValues, 
        string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    return constraints;
}

std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::createConstraintFeatureEnabledEnum()
{
    auto constraints = std::make_shared<Constraints>();
    std::vector<dune::cdm::glossary_1::FeatureEnabled> validValues = {
        dune::cdm::glossary_1::FeatureEnabled::true_, 
        dune::cdm::glossary_1::FeatureEnabled::false_
    };

    // As far as I know, we wouldn't disable any of these content types, but I could be wrong.
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(validValues, 
        &dune::cdm::glossary_1::FeatureEnabledEnum::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(validValues, 
        string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    return constraints;
}

std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::createConstraintRange(int32_t uniqueValueExpected)
{
    auto constraints = std::make_shared<Constraints>();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeInt>(uniqueValueExpected, uniqueValueExpected, uniqueValueExpected, string_id::cCheckInvalidEntries);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::createConstraintRange(double uniqueValueExpected)
{
    auto constraints = std::make_shared<Constraints>();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeDouble>(uniqueValueExpected, uniqueValueExpected, uniqueValueExpected, 
        string_id::cCheckInvalidEntries);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::createConstraintRange(int32_t minValueExpected, 
    int32_t maxValueExpected, int32_t stepValueExpected)
{
    auto constraints = std::make_shared<Constraints>();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeInt>(minValueExpected, maxValueExpected, stepValueExpected, string_id::cCheckInvalidEntries);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}
    
std::shared_ptr<Constraints> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::createConstraintRange(double minValueExpected, 
    double maxValueExpected, double stepValueExpected)
{
    auto constraints = std::make_shared<Constraints>();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeDouble>(minValueExpected, maxValueExpected, stepValueExpected, string_id::cCheckInvalidEntries);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, WhenInitializeIsCalledWithNonEmptyCsfFile_TheComponentGetsInitialized)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/ExampleBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
}

// Test an empty csf file when call to get dynamic constraints
TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, WhenLoadingANonExistentCsfFile_ThenResultOnAssert)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/NonExistent.json");

    // Assert death only apply on debug mode
    # ifndef NDEBUG
        ASSERT_DEATH_IF_SUPPORTED(comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get()),"");
    # else
        comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
        auto constraintsGroup = std::make_shared<ConstraintsGroup>();
        EXPECT_EQ(component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup),nullptr);
    # endif
}

// Test a malformed csf file
TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, WhenLoadingAMalformedCsfFile_ThenResultOnAssert)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/BadFormatBaseDynamicContraintRules.json");

    // Assert death only apply on debug mode
    # ifndef NDEBUG
        ASSERT_DEATH_IF_SUPPORTED(comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get()),"");
    # else
        comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
        auto constraintsGroup = std::make_shared<ConstraintsGroup>();
        EXPECT_EQ(component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup),nullptr);
    # endif
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, WhenCallToGetDynamicConstraintsWithNonEmptyCsfFile_ThenResultOnEmptyConstraintGroup)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/ExampleBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup);

    // Component Must to be empty
    EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToGetDynamicConstraintsWithNonEmptyCsfFileAndEmptyJobTicketTable_ThenResultOnEmptyConstraintGroup)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/ExampleBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintsGroup, givenEmptyJobTicketTable());

    // Component Must to be empty
    EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToGetDynamicConstraintsWithNonEmptyCsfFileAndJobTicketTable_ThenResultOnEmptyConstraintGroup)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/ExampleBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintsGroup, givenJobTicketTable());

    // Component Must to be empty
    EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, WhenCallToGetDynamicConstraintsWithEmptyCsfFile_ThenResultOnEmptyConstraintGroup)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/EmptyBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup);

    // Component Must to be empty
    EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToGetDynamicConstraintsWithEmptyCsfFileAndEmptyJobTicketTable_ThenResultOnEmptyConstraintGroup)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/EmptyBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintsGroup, givenEmptyJobTicketTable());

    // Component Must to be empty
    EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToGetDynamicConstraintsWithEmptyCsfFileAndJobTicketTable_ThenResultOnEmptyConstraintGroup)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/EmptyBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintsGroup, givenJobTicketTable());

    // Component Must to be empty
    EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, WhenCallToGetDynamicConstraintsWithNonEmptyCsfFileAndThenEmpty_ThenResultOnAssert)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/jsonTestPolicies/ResolvedIfThenEmpty.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({ColorModes::color, ColorModes::grayscale, ColorModes::blackAndWhite});
    constraintsGroup->set("src/scan/colorMode", colorConstraints);

    // Assert death only apply on debug mode
    # ifndef NDEBUG
        ASSERT_DEATH_IF_SUPPORTED(component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup),"");
    # else
        auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup);
        EXPECT_NE(constraintResult,nullptr);
        // Component Must to be empty
        EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
    # endif
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToGetDynamicConstraintsWithNonEmptyCsfFileAndThenEmptyAndEmptyJobTicketTable_ThenResultOnAssert)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/jsonTestPolicies/ResolvedIfThenEmpty.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({ColorModes::color, ColorModes::grayscale, ColorModes::blackAndWhite});
    constraintsGroup->set("src/scan/colorMode", colorConstraints);

    // Assert death only apply on debug mode
    # ifndef NDEBUG
        ASSERT_DEATH_IF_SUPPORTED(component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup, givenEmptyJobTicketTable()),"");
    # else
        auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup, givenEmptyJobTicketTable());
        EXPECT_NE(constraintResult,nullptr);
        // Component Must to be empty
        EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
    # endif
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToGetDynamicConstraintsWithNonEmptyCsfFileAndThenEmptyAndJobTicketTable_ThenResultOnAssert)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/jsonTestPolicies/ResolvedIfThenEmpty.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({ColorModes::color, ColorModes::grayscale, ColorModes::blackAndWhite});
    constraintsGroup->set("src/scan/colorMode", colorConstraints);

    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup, givenJobTicketTable());
    EXPECT_NE(constraintResult,nullptr);
    // Component Must to be empty
    EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToGetDynamicConstraintsWithNonEmptyCsfFileAndThenNotSupported_ThenResultOnAssert)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/jsonTestPolicies/FirstOkSecondThenNotSupported.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    constraintsGroup->set("src/scan/colorMode", colorConstraints);
    ASSERT_DEATH_IF_SUPPORTED(component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup),"");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToGetDynamicConstraintsWithNonEmptyCsfFileAndThenNotCombine_ThenResultOnAssert)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/jsonTestPolicies/FirstOkSecondOkNotCombine.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    constraintsGroup->set("src/scan/colorMode", colorConstraints);
    ASSERT_DEATH_IF_SUPPORTED(component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup),"");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithEmptyCsfFile_ThenReturnFalseAndNoAssertOccurs)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/EmptyBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    auto result = component_->checkAndApplyForceSets(jobTicketTable,mockICopyJobTicket_,constraintsGroup);
    EXPECT_FALSE(result);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithEmptyCsfFileAndStaticConstraints_ThenReturnFalseAndNoAssertOccurs)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/EmptyBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto constraintsGroup = std::make_shared<ConstraintsGroup>();
    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    auto result = component_->checkAndApplyForceSets(jobTicketTable,mockICopyJobTicket_,constraintsGroup,constraintsGroup);
    EXPECT_FALSE(result);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithConcatenatedRulesAndCurrentTicketInvokeLastRule_ThenTicketTableIsUpdatedAsExpected)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/ConcatenatedRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto staticConstraints = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    auto resolutionConstraints = createConstraintEnum<dune::cdm::jobTicket_1::Resolutions>({
        dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e300Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e600Dpi
    });
    auto originalMediaTypeConstraints = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>({
        dune::cdm::glossary_1::ScanMediaType::whitePaper, 
        dune::cdm::glossary_1::ScanMediaType::blueprints, 
        dune::cdm::glossary_1::ScanMediaType::translucentPaper
    });
    staticConstraints->set("src/scan/colorMode", colorConstraints);
    staticConstraints->set("src/scan/resolution", resolutionConstraints);
    staticConstraints->set("src/scan/mediaType", originalMediaTypeConstraints);

    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::TRANSLUCENT_PAPER)); // Type that start trigger of constraints
    EXPECT_CALL(*jobIntent_, getColorMode()).WillRepeatedly(Return(dune::imaging::types::ColorMode::BLACKANDWHITE));
    EXPECT_CALL(*jobIntent_, getScanXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));

    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    component_->checkAndApplyForceSets(jobTicketTable, mockICopyJobTicket_, staticConstraints);

    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e200Dpi);
    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->colorMode.get(),  dune::cdm::jobTicket_1::ColorModes::color);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithConcatenatedRulesAndCurrentTicketInvokeLastRuleAndStaticConstraints_ThenTicketTableIsUpdatedAsExpected)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/ConcatenatedRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto staticConstraints = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    auto resolutionConstraints = createConstraintEnum<dune::cdm::jobTicket_1::Resolutions>({
        dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e300Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e600Dpi
    });
    auto originalMediaTypeConstraints = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>({
        dune::cdm::glossary_1::ScanMediaType::whitePaper, 
        dune::cdm::glossary_1::ScanMediaType::blueprints, 
        dune::cdm::glossary_1::ScanMediaType::translucentPaper
    });
    staticConstraints->set("src/scan/colorMode", colorConstraints);
    staticConstraints->set("src/scan/resolution", resolutionConstraints);
    staticConstraints->set("src/scan/mediaType", originalMediaTypeConstraints);

    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::TRANSLUCENT_PAPER)); // Type that start trigger of constraints
    EXPECT_CALL(*jobIntent_, getColorMode()).WillRepeatedly(Return(dune::imaging::types::ColorMode::BLACKANDWHITE));
    EXPECT_CALL(*jobIntent_, getScanXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));

    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    component_->checkAndApplyForceSets(jobTicketTable, mockICopyJobTicket_, staticConstraints, staticConstraints);

    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e200Dpi);
    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->colorMode.get(),  dune::cdm::jobTicket_1::ColorModes::color);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithConcatenatedRulesAndCurrentTicketTableInvokeLastRule_ThenTicketTableIsUpdatedAsExpected)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/ConcatenatedRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto staticConstraints = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    auto resolutionConstraints = createConstraintEnum<dune::cdm::jobTicket_1::Resolutions>({
        dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e300Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e600Dpi
    });
    auto originalMediaTypeConstraints = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>({
        dune::cdm::glossary_1::ScanMediaType::whitePaper, 
        dune::cdm::glossary_1::ScanMediaType::blueprints, 
        dune::cdm::glossary_1::ScanMediaType::translucentPaper
    });
    staticConstraints->set("src/scan/colorMode", colorConstraints);
    staticConstraints->set("src/scan/resolution", resolutionConstraints);
    staticConstraints->set("src/scan/mediaType", originalMediaTypeConstraints);

    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::BLUEPRINTS));
    EXPECT_CALL(*jobIntent_, getColorMode()).WillRepeatedly(Return(dune::imaging::types::ColorMode::BLACKANDWHITE));
    EXPECT_CALL(*jobIntent_, getScanXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));

    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    jobTicketTable->beginMergePatch();
    // src
    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    jobTicketTable->src = *srcTable;
    jobTicketTable->src.beginMergePatch();
    // src
    // src.scan
    auto scanTable = std::make_unique<dune::cdm::jobTicket_1::ScanTable>();
    jobTicketTable->src.getMutable()->scan = *(scanTable);
    jobTicketTable->src.getMutable()->scan.beginMergePatch();
    jobTicketTable->src.getMutable()->scan.getMutable()->mediaType = dune::cdm::glossary_1::ScanMediaType::translucentPaper; // Type that start trigger of constraints

    component_->checkAndApplyForceSets(jobTicketTable, mockICopyJobTicket_, staticConstraints);

    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e200Dpi);
    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->colorMode.get(),  dune::cdm::jobTicket_1::ColorModes::color);
    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->mediaType.get(),  dune::cdm::glossary_1::ScanMediaType::translucentPaper);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithConcatenatedRulesAndCurrentTicketTableInvokeLastRuleAndStaticConstraint_ThenTicketTableIsUpdatedAsExpected)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/ConcatenatedRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto staticConstraints = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    auto resolutionConstraints = createConstraintEnum<dune::cdm::jobTicket_1::Resolutions>({
        dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e300Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e600Dpi
    });
    auto originalMediaTypeConstraints = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>({
        dune::cdm::glossary_1::ScanMediaType::whitePaper, 
        dune::cdm::glossary_1::ScanMediaType::blueprints, 
        dune::cdm::glossary_1::ScanMediaType::translucentPaper
    });
    staticConstraints->set("src/scan/colorMode", colorConstraints);
    staticConstraints->set("src/scan/resolution", resolutionConstraints);
    staticConstraints->set("src/scan/mediaType", originalMediaTypeConstraints);

    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::BLUEPRINTS));
    EXPECT_CALL(*jobIntent_, getColorMode()).WillRepeatedly(Return(dune::imaging::types::ColorMode::BLACKANDWHITE));
    EXPECT_CALL(*jobIntent_, getScanXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));

    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    jobTicketTable->beginMergePatch();
    // src
    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    jobTicketTable->src = *srcTable;
    jobTicketTable->src.beginMergePatch();
    // src
    // src.scan
    auto scanTable = std::make_unique<dune::cdm::jobTicket_1::ScanTable>();
    jobTicketTable->src.getMutable()->scan = *(scanTable);
    jobTicketTable->src.getMutable()->scan.beginMergePatch();
    jobTicketTable->src.getMutable()->scan.getMutable()->mediaType = dune::cdm::glossary_1::ScanMediaType::translucentPaper; // Type that start trigger of constraints

    component_->checkAndApplyForceSets(jobTicketTable, mockICopyJobTicket_, staticConstraints, staticConstraints);

    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e200Dpi);
    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->colorMode.get(),  dune::cdm::jobTicket_1::ColorModes::color);
    EXPECT_EQ(jobTicketTable->src.get()->scan.get()->mediaType.get(),  dune::cdm::glossary_1::ScanMediaType::translucentPaper);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithLoopedRulesAndCurrentTicketInvokeLastRule_ThenAssertOccurs)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/LoopedRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto staticConstraints = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    auto resolutionConstraints = createConstraintEnum<dune::cdm::jobTicket_1::Resolutions>({
        dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e300Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e600Dpi
    });
    auto originalMediaTypeConstraints = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>({
        dune::cdm::glossary_1::ScanMediaType::whitePaper, 
        dune::cdm::glossary_1::ScanMediaType::blueprints, 
        dune::cdm::glossary_1::ScanMediaType::translucentPaper
    });
    staticConstraints->set("src/scan/colorMode", colorConstraints);
    staticConstraints->set("src/scan/resolution", resolutionConstraints);
    staticConstraints->set("src/scan/mediaType", originalMediaTypeConstraints);

    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::TRANSLUCENT_PAPER)); // Type that start trigger of constraints
    EXPECT_CALL(*jobIntent_, getColorMode()).WillRepeatedly(Return(dune::imaging::types::ColorMode::BLACKANDWHITE));
    EXPECT_CALL(*jobIntent_, getScanXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));

    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    ASSERT_DEATH_IF_SUPPORTED(component_->checkAndApplyForceSets(jobTicketTable, mockICopyJobTicket_, staticConstraints), "");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithLoopedRulesAndCurrentTicketInvokeLastRuleAndStaticConstraints_ThenAssertOccurs)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/LoopedRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto staticConstraints = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    auto resolutionConstraints = createConstraintEnum<dune::cdm::jobTicket_1::Resolutions>({
        dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e300Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e600Dpi
    });
    auto originalMediaTypeConstraints = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>({
        dune::cdm::glossary_1::ScanMediaType::whitePaper, 
        dune::cdm::glossary_1::ScanMediaType::blueprints, 
        dune::cdm::glossary_1::ScanMediaType::translucentPaper
    });
    staticConstraints->set("src/scan/colorMode", colorConstraints);
    staticConstraints->set("src/scan/resolution", resolutionConstraints);
    staticConstraints->set("src/scan/mediaType", originalMediaTypeConstraints);

    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::TRANSLUCENT_PAPER)); // Type that start trigger of constraints
    EXPECT_CALL(*jobIntent_, getColorMode()).WillRepeatedly(Return(dune::imaging::types::ColorMode::BLACKANDWHITE));
    EXPECT_CALL(*jobIntent_, getScanXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));

    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    ASSERT_DEATH_IF_SUPPORTED(component_->checkAndApplyForceSets(jobTicketTable, mockICopyJobTicket_, staticConstraints, staticConstraints), "");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithLoopedRulesAndCurrentTicketTableInvokeLastRule_ThenAssertOccurs)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/LoopedRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto staticConstraints = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    auto resolutionConstraints = createConstraintEnum<dune::cdm::jobTicket_1::Resolutions>({
        dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e300Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e600Dpi
    });
    auto originalMediaTypeConstraints = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>({
        dune::cdm::glossary_1::ScanMediaType::whitePaper, 
        dune::cdm::glossary_1::ScanMediaType::blueprints, 
        dune::cdm::glossary_1::ScanMediaType::translucentPaper
    });
    staticConstraints->set("src/scan/colorMode", colorConstraints);
    staticConstraints->set("src/scan/resolution", resolutionConstraints);
    staticConstraints->set("src/scan/mediaType", originalMediaTypeConstraints);

    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::BLUEPRINTS));
    EXPECT_CALL(*jobIntent_, getColorMode()).WillRepeatedly(Return(dune::imaging::types::ColorMode::BLACKANDWHITE));
    EXPECT_CALL(*jobIntent_, getScanXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));

    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    jobTicketTable->beginMergePatch();
    // src
    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    jobTicketTable->src = *srcTable;
    jobTicketTable->src.beginMergePatch();
    // src
    // src.scan
    auto scanTable = std::make_unique<dune::cdm::jobTicket_1::ScanTable>();
    jobTicketTable->src.getMutable()->scan = *(scanTable);
    jobTicketTable->src.getMutable()->scan.beginMergePatch();
    jobTicketTable->src.getMutable()->scan.getMutable()->mediaType = dune::cdm::glossary_1::ScanMediaType::translucentPaper; // Type that start trigger of constraints

    ASSERT_DEATH_IF_SUPPORTED(component_->checkAndApplyForceSets(jobTicketTable, mockICopyJobTicket_, staticConstraints), "");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase, 
    WhenCallToApplyForceSetsWithLoopedRulesAndCurrentTicketTableInvokeLastRuleAndStaticConstraints_ThenAssertOccurs)
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/LoopedRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    auto staticConstraints = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    auto resolutionConstraints = createConstraintEnum<dune::cdm::jobTicket_1::Resolutions>({
        dune::cdm::jobTicket_1::Resolutions::e200Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e300Dpi, 
        dune::cdm::jobTicket_1::Resolutions::e600Dpi
    });
    auto originalMediaTypeConstraints = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>({
        dune::cdm::glossary_1::ScanMediaType::whitePaper, 
        dune::cdm::glossary_1::ScanMediaType::blueprints, 
        dune::cdm::glossary_1::ScanMediaType::translucentPaper
    });
    staticConstraints->set("src/scan/colorMode", colorConstraints);
    staticConstraints->set("src/scan/resolution", resolutionConstraints);
    staticConstraints->set("src/scan/mediaType", originalMediaTypeConstraints);

    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::BLUEPRINTS));
    EXPECT_CALL(*jobIntent_, getColorMode()).WillRepeatedly(Return(dune::imaging::types::ColorMode::BLACKANDWHITE));
    EXPECT_CALL(*jobIntent_, getScanXResolution()).WillRepeatedly(Return(dune::imaging::types::Resolution::E1200DPI));

    auto jobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    jobTicketTable->beginMergePatch();
    // src
    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    jobTicketTable->src = *srcTable;
    jobTicketTable->src.beginMergePatch();
    // src
    // src.scan
    auto scanTable = std::make_unique<dune::cdm::jobTicket_1::ScanTable>();
    jobTicketTable->src.getMutable()->scan = *(scanTable);
    jobTicketTable->src.getMutable()->scan.beginMergePatch();
    jobTicketTable->src.getMutable()->scan.getMutable()->mediaType = dune::cdm::glossary_1::ScanMediaType::translucentPaper; // Type that start trigger of constraints

    ASSERT_DEATH_IF_SUPPORTED(component_->checkAndApplyForceSets(jobTicketTable, mockICopyJobTicket_, staticConstraints, staticConstraints), "");
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithExistingStaticButNotInDynamicConstraint :
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithExistingStaticButNotInDynamicConstraint : 
    public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase
{
public:

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithExistingStaticButNotInDynamicConstraint() : 
        GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase() {};
    ~GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithExistingStaticButNotInDynamicConstraint(){};

    void SetUp() override;

    void TearDown() override;
};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithExistingStaticButNotInDynamicConstraint::SetUp()
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::SetUp();

    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/EmptyBaseDynamicContraintRules.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    std::future<void> asyncCompletion;
    comp_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithExistingStaticButNotInDynamicConstraint::TearDown()
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::SetUp();
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithExistingStaticButNotInDynamicConstraint, 
    WhenCallToGetDynamicConstraints_ThenResultIsConstraintEmpty)
{
    auto constraintsGroup = std::make_shared<ConstraintsGroup>();

    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    constraintsGroup->set("src/scan/colorMode", colorConstraints);

    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintsGroup);

    EXPECT_EQ(constraintResult->getAllConstraints().size(),0);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration :
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration : 
    public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase
{
public:

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration() : 
        GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase() {};
    ~GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration(){};

    void SetUp() override;

    void TearDown() override;

    std::shared_ptr<ConstraintsGroup> generateStaticConstraintGroupExpected();

    std::string getLocalized(dune::localization::StringId_Type id);

    dune::localization::StringId_Type getId(std::string idString);

    void checkConstraintMessage(std::shared_ptr<Constraints> constraints, 
        std::vector<dune::framework::data::constraints::ConstraintType> vectorTypes, 
        std::string textToCheck = "");

    std::shared_ptr<ConstraintsGroup> constraintGroup_{nullptr};
    std::unordered_map<dune::localization::StringId_Type,std::string> mapIdToString 
    {
        {
            dune::localization::string_id::cMessageNotAllowModifySettings.value(),
            std::string("%1$s is not available since the job has already started. To modify this setting, finish the job and start a new job.")
        },
        {
            dune::localization::string_id::cSettingsConfiguringIncompatible.value(),
            std::string("The settings that you are configuring are incompatible with those already set in the printer.")
        },
        {
            dune::localization::string_id::cIncompatibleSettings.value(),
            std::string("Incompatible Settings")
        },
        {
            dune::localization::string_id::cStringColon.value(),
            std::string("%1$s:")
        },
        {
            dune::localization::string_id::cStringBullet.value(),
            std::string("*%1$s")
        },
        {
            dune::localization::string_id::cValueOtherThanDigit.value(),
            std::string("Value other than %1$d")
        },
        {
            dune::localization::string_id::cMultilevelSettingSeparator.value(),
            std::string("%1$s > %2$s")
        },
        {
            dune::localization::string_id::cLessThanX.value(),
            std::string("less than %1$d")
        },
        {
            dune::localization::string_id::cMoreThanX.value(),
            std::string("more than %1$d")
        },
        {
            dune::localization::string_id::cInputInvalidPattern.value(),
            std::string("Invalid characters")
        },
        {
            dune::localization::string_id::cCopies.value(),
            std::string("Copies")
        },
        {
            dune::localization::string_id::cOriginalPaperType.value(),
            std::string("Original Paper Type")
        },
        {
            dune::localization::string_id::cUndefined.value(),
            std::string("Undefined")
        },
        {
            dune::localization::string_id::cBlueprint.value(),
            std::string("Blueprint")
        },
        {
            dune::localization::string_id::cAmmoniaOldBlueprint.value(),
            std::string("Ammonia")
        },
        {
            dune::localization::string_id::cPaperTypeOldRecycled.value(),
            std::string("Old Recycled")
        },
        {
            dune::localization::string_id::cPhoto.value(),
            std::string("Photo paper")
        },
        {
            dune::localization::string_id::cPaperTypeTranslucent.value(),
            std::string("Translucent")
        },
        {
            dune::localization::string_id::cColorWhite.value(),
            std::string("White")
        },
        {
            dune::localization::string_id::cContentType.value(),
            std::string("Content Type")
        },
        {
            dune::localization::string_id::cMixed.value(),
            std::string("Mixed")
        },
        {
            dune::localization::string_id::cImage.value(),
            std::string("Image")
        },
        {
            dune::localization::string_id::cLines.value(),
            std::string("Line Drawing")
        },
        {
            dune::localization::string_id::cDetailedBackgroundRemoval.value(),
            std::string("Background Color Removal")
        },
        {
            dune::localization::string_id::cLandscape.value(),
            std::string("Landscape")
        },
        {
            dune::localization::string_id::cPortrait.value(),
            std::string("Portrait")
        },
        {
            dune::localization::string_id::cOutputSize.value(),
            std::string("Output Size")
        },
        {
            dune::localization::string_id::cOrientation.value(),
            std::string("Orientation")
        },
        {
            dune::localization::string_id::cFoldingStyle.value(),
            std::string("Folding Style")
        },
        {
            dune::localization::string_id::cOutputDestination.value(),
            std::string("Output Destination")
        },
        {
            dune::localization::string_id::cStacker.value(),
            std::string("Stacker")
        }
    };

    std::unordered_map<std::string,dune::localization::StringId_Type> mapCsfStringToId
    {
        {
            "StringIds.cCopies",
            dune::localization::string_id::cCopies.value()
        },
        {
            "StringIds.cOriginalPaperType",
            dune::localization::string_id::cOriginalPaperType.value()
        },
        {
            "StringIds.cUndefined",
            dune::localization::string_id::cUndefined.value()
        },
        {
            "StringIds.cBlueprint",
            dune::localization::string_id::cBlueprint.value()
        },
        {
            "StringIds.cAmmoniaOldBlueprint",
            dune::localization::string_id::cAmmoniaOldBlueprint.value()
        },
        {
            "StringIds.cPaperTypeOldRecycled",
            dune::localization::string_id::cPaperTypeOldRecycled.value()
        },
        {
            "StringIds.cPhoto",
            dune::localization::string_id::cPhoto.value()
        },
        {
            "StringIds.cPaperTypeTranslucent",
            dune::localization::string_id::cPaperTypeTranslucent.value()
        },
        {
            "StringIds.cColorWhite",
            dune::localization::string_id::cColorWhite.value()
        },
        {
            "StringIds.cContentType",
            dune::localization::string_id::cContentType.value()
        },
        {
            "StringIds.cMixed",
            dune::localization::string_id::cMixed.value()
        },
        {
            "StringIds.cImage",
            dune::localization::string_id::cImage.value()
        },
        {
            "StringIds.cLines",
            dune::localization::string_id::cLines.value()
        },
        {
            "StringIds.cDetailedBackgroundRemoval",
            dune::localization::string_id::cDetailedBackgroundRemoval.value()
        },
        {
            "StringIds.cOutputSize",
            dune::localization::string_id::cOutputSize.value()
        },
        {
            "StringIds.cOrientation",
            dune::localization::string_id::cOrientation.value()
        },
        {
            "StringIds.cLandscape",
            dune::localization::string_id::cLandscape.value()
        },
        {
            "StringIds.cPortrait",
            dune::localization::string_id::cPortrait.value()
        },
        {
            "StringIds.cFoldingStyle",
            dune::localization::string_id::cFoldingStyle.value()
        },
        {
            "StringIds.cOutputDestination",
            dune::localization::string_id::cOutputDestination.value()
        },
        {
            "StringIds.cStacker",
            dune::localization::string_id::cStacker.value()
        }
    };
};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration::SetUp()
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::SetUp();

    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", 
        "./testResources/BaseDynamicContraintRulesWithDynamicString.json");

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    std::future<void> asyncCompletion;
    comp_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Set On calls for test
    ON_CALL(*mockILocale_, get(testing::Matcher<dune::localization::StringId>(_))).WillByDefault(        
        testing::Invoke([&](dune::localization::StringId id)
        {
            return getLocalized(id.value());
        })
    );
    ON_CALL(*mockILocale_, get(testing::Matcher<dune::localization::StringId_Type>(_))).WillByDefault(
        testing::Invoke([&](dune::localization::StringId_Type idType)
        {
            return getLocalized(idType);
        })
    );
    ON_CALL(*mockILocale_, getStringIdForCsfOnly(_)).WillByDefault(
        testing::Invoke([&](std::string stringId)
        {
            return getId(stringId);
        })
    );

    constraintGroup_ = generateStaticConstraintGroupExpected();
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration::TearDown()
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::TearDown();
}

std::shared_ptr<ConstraintsGroup> 
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration::generateStaticConstraintGroupExpected()
{
    auto constraintsGroup = std::make_shared<ConstraintsGroup>();

    std::vector<dune::cdm::glossary_1::ScanMediaType> vectorMediaConstraints{
        dune::cdm::glossary_1::ScanMediaType::whitePaper,
        dune::cdm::glossary_1::ScanMediaType::photoPaper,
        dune::cdm::glossary_1::ScanMediaType::oldRecycledPaper,
        dune::cdm::glossary_1::ScanMediaType::translucentPaper,
        dune::cdm::glossary_1::ScanMediaType::blueprints,
        dune::cdm::glossary_1::ScanMediaType::darkBlueprints
    };

    auto mediaTypeConstraints = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>(vectorMediaConstraints);
    constraintsGroup->set("src/scan/mediaType", mediaTypeConstraints);

    std::vector<dune::cdm::jobTicket_1::ContentType> vectorContentType{
        dune::cdm::jobTicket_1::ContentType::mixed,
        dune::cdm::jobTicket_1::ContentType::image,
        dune::cdm::jobTicket_1::ContentType::lineDrawing
    };

    auto contentConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ContentType>(vectorContentType);
    constraintsGroup->set("src/scan/contentType", contentConstraints);

    std::vector<dune::cdm::glossary_1::ContentOrientation> vectorContentOrientation{
        dune::cdm::glossary_1::ContentOrientation::landscape,
        dune::cdm::glossary_1::ContentOrientation::portrait
    };

    auto ContentOrientationConstraints = createConstraintEnum<dune::cdm::glossary_1::ContentOrientation>(vectorContentOrientation);
    constraintsGroup->set("pipelineOptions/imageModifications/outputCanvasOrientation", ContentOrientationConstraints); 

    auto rangeBackgroundConstraint = createConstraintRange(-6,6,1);
    constraintsGroup->set("pipelineOptions/imageModifications/backgroundColorRemovalLevel", rangeBackgroundConstraint);

    auto rangeCopiesConstraint = createConstraintRange(1,99,1);
    constraintsGroup->set("dest/print/copies", rangeCopiesConstraint);
    
    return constraintsGroup;
}

std::string GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration::getLocalized(
    dune::localization::StringId_Type id)
{
    std::string result = std::string("<TEST id_type " + std::to_string(id) + ">");

    auto pair = mapIdToString.find(id);
    // Prevent sucess when some values are not defined
    EXPECT_NE(pair, mapIdToString.end());

    if(pair != mapIdToString.end())
    {
        result = pair->second;
    }

    return result;
}

dune::localization::StringId_Type GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration::getId(
    std::string idString)
{
    dune::localization::StringId_Type id = 0;

    auto pair = mapCsfStringToId.find(idString);
    // Prevent sucess when some values are not defined
    EXPECT_NE(pair, mapCsfStringToId.end());

    if(pair != mapCsfStringToId.end())
    {
        id = pair->second;
    }

    return id;
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration::checkConstraintMessage(
    std::shared_ptr<Constraints> constraints, 
    std::vector<dune::framework::data::constraints::ConstraintType> vectorTypes, 
    std::string textToCheck)
{
    EXPECT_NE(constraints->getConstraints().size(),0);
    ASSERT_FALSE(vectorTypes.empty());

    int foundedCounter = 0;

    for(auto constraint : constraints->getConstraints())
    {
        auto iterator = std::find(vectorTypes.begin(),vectorTypes.end(),constraint->getConstraintType());

        if(iterator != vectorTypes.end())
        {
            EXPECT_NE("",constraint->getMessageLocalized());
            if(textToCheck != "")
            {
                EXPECT_EQ(textToCheck,constraint->getMessageLocalized());
            }
            foundedCounter++;
        }
    }

    EXPECT_EQ(foundedCounter,vectorTypes.size());
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketNoCauseNewConstraint_ThenResultIsEmpty)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_);

    ASSERT_EQ(constraintResult->getAllConstraints().size(),0);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketNoCauseNewConstraintAndEmptyJobTicketTable_ThenResultIsEmpty)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_, givenEmptyJobTicketTable());

    ASSERT_EQ(constraintResult->getAllConstraints().size(),0);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketNoCauseNewConstraintAndJobTicketTable_ThenResultIsEmpty)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_, givenJobTicketTable());

    ASSERT_EQ(constraintResult->getAllConstraints().size(),2);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/contentType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\nContent Type\n*Mixed\n*Image\n\n"
        "Incompatible Settings:\n\nOriginal Paper Type\n*Translucent\n*Blueprint");

    checkConstraintMessage(constraintResult->getConstraints("dest/print/copies"),
        {dune::framework::data::constraints::ConstraintType::RANGE_INT,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Copies\n*less than 0\n*more than 50\n\nIncompatible Settings:\n\nBackground Color Removal\nValue other than 4");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketNewConstraintAndDisabled_ThenResultIsTwoConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::BLUEPRINTS));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);
    
    checkConstraintMessage(constraintResult->getConstraints("src/scan/contentType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\nContent Type\n*Mixed\n*Image\n\n"
        "Incompatible Settings:\n\nOriginal Paper Type\n*Translucent\n*Blueprint");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketTableNewConstraintAndDisabled_ThenResultIsTwoConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::BLUEPRINTS));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));
    auto ticketTable = givenJobTicketTable(jobIntent_);

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);
    
    checkConstraintMessage(constraintResult->getConstraints("src/scan/contentType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\nContent Type\n*Mixed\n*Image\n\n"
        "Incompatible Settings:\n\nOriginal Paper Type\n*Translucent\n*Blueprint");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndOnlyTicketTableNewConstraintAndDisabled_ThenResultIsTwoConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    // With this settings in ticket table, there is dynamic constraint generated
    auto ticketTable = givenJobTicketTable(jobIntent_);
    assert_msg(ticketTable, "ticket is null");
    ticketTable->src.getMutable()->scan.getMutable()->mediaType = dune::job::cdm::mapToCdm(dune::scan::types::OriginalMediaType::BLUEPRINTS);

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(), 1);
    
    checkConstraintMessage(constraintResult->getConstraints("src/scan/contentType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\nContent Type\n*Mixed\n*Image\n\n"
        "Incompatible Settings:\n\nOriginal Paper Type\n*Translucent\n*Blueprint");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketCauseNewConstraintANDNotDisabled_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(1));

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/contentType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Content Type\n*Mixed\n\nIncompatible Settings:\n\nCopies\n*1");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketTableCauseNewConstraintANDNotDisabled_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(1));
    auto ticketTable = givenJobTicketTable(jobIntent_);    

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/contentType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Content Type\n*Mixed\n\nIncompatible Settings:\n\nCopies\n*1");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndOnlyTicketTableCauseNewConstraintANDNotDisabled_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    // With this settings on job intent, there is dynamic constraint generated
    auto jobIntent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    EXPECT_CALL(*jobIntent, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent, getCopies()).WillRepeatedly(Return(1));
    auto ticketTable = givenJobTicketTable(jobIntent);    

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/contentType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Content Type\n*Mixed\n\nIncompatible Settings:\n\nCopies\n*1");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketCauseNewConstraintORByNumberOfCopies_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(4));

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/mediaType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Original Paper Type\n*White\n*Photo paper\n*Old Recycled\n*Translucent\n*Blueprint\n\nIncompatible Settings:\n\nCopies\n*4");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketTableCauseNewConstraintORByNumberOfCopies_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(4));
    auto ticketTable = givenJobTicketTable(jobIntent_);    

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/mediaType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Original Paper Type\n*White\n*Photo paper\n*Old Recycled\n*Translucent\n*Blueprint\n\nIncompatible Settings:\n\nCopies\n*4");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndOnlyTicketTableCauseNewConstraintORByNumberOfCopies_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    // With this settings on job intent, there is dynamic constraint generated
    auto jobIntent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    EXPECT_CALL(*jobIntent, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent, getCopies()).WillRepeatedly(Return(4));
    auto ticketTable = givenJobTicketTable(jobIntent);

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/mediaType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Original Paper Type\n*White\n*Photo paper\n*Old Recycled\n*Translucent\n*Blueprint\n\nIncompatible Settings:\n\nCopies\n*4");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketCauseNewConstraintORbyContentType_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getOriginalContentType()).WillRepeatedly(Return(dune::imaging::types::OriginalContentType::MIXED));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/mediaType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Original Paper Type\n*White\n*Photo paper\n*Old Recycled\n*Translucent\n*Blueprint\n\nIncompatible Settings:\n\nContent Type\n*Mixed");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketTableCauseNewConstraintORbyContentType_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getOriginalContentType()).WillRepeatedly(Return(dune::imaging::types::OriginalContentType::MIXED));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));
    auto ticketTable = givenJobTicketTable(jobIntent_);    

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/mediaType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Original Paper Type\n*White\n*Photo paper\n*Old Recycled\n*Translucent\n*Blueprint\n\nIncompatible Settings:\n\nContent Type\n*Mixed");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndOnlyTicketTableCauseNewConstraintORbyContentType_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));
    // With this settings on job intent, there is dynamic constraint generated
    auto jobIntent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    EXPECT_CALL(*jobIntent, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent, getOriginalContentType()).WillRepeatedly(Return(dune::imaging::types::OriginalContentType::MIXED));
    EXPECT_CALL(*jobIntent, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent, getCopies()).WillRepeatedly(Return(2));
    auto ticketTable = givenJobTicketTable(jobIntent);

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/mediaType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Original Paper Type\n*White\n*Photo paper\n*Old Recycled\n*Translucent\n*Blueprint\n\nIncompatible Settings:\n\nContent Type\n*Mixed");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketCauseNewConstraintANDbyTwoSettings_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getOriginalContentType()).WillRepeatedly(Return(dune::imaging::types::OriginalContentType::MIXED));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(4));

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/mediaType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Original Paper Type\n*White\n*Photo paper\n*Old Recycled\n*Translucent\n*Blueprint\n\nIncompatible Settings:\n\nCopies\n*4\n\nContent Type\n*Mixed");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketTableCauseNewConstraintANDbyTwoSettings_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getOriginalContentType()).WillRepeatedly(Return(dune::imaging::types::OriginalContentType::MIXED));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(4));
    auto ticketTable = givenJobTicketTable(jobIntent_);    

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/mediaType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Original Paper Type\n*White\n*Photo paper\n*Old Recycled\n*Translucent\n*Blueprint\n\nIncompatible Settings:\n\nCopies\n*4\n\nContent Type\n*Mixed");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndOnlyTicketTableCauseNewConstraintANDbyTwoSettings_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));
    // With this settings on job intent, there is dynamic constraint generated
    auto jobIntent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    EXPECT_CALL(*jobIntent, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent, getOriginalContentType()).WillRepeatedly(Return(dune::imaging::types::OriginalContentType::MIXED));
    EXPECT_CALL(*jobIntent, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent, getCopies()).WillRepeatedly(Return(4));
    auto ticketTable = givenJobTicketTable(jobIntent);

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("src/scan/mediaType"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Original Paper Type\n*White\n*Photo paper\n*Old Recycled\n*Translucent\n*Blueprint\n\nIncompatible Settings:\n\nCopies\n*4\n\nContent Type\n*Mixed");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketNoCauseNewConstrainNAND_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::DARK_BLUEPRINTS));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("pipelineOptions/imageModifications/backgroundColorRemovalLevel"),
        {dune::framework::data::constraints::ConstraintType::RANGE_INT,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Background Color Removal\nValue other than 0\n\nIncompatible Settings:\n\nOriginal Paper Type\n*Translucent\n*Ammonia");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketTableNoCauseNewConstrainNAND_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::DARK_BLUEPRINTS));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));
    auto ticketTable = givenJobTicketTable(jobIntent_);    

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("pipelineOptions/imageModifications/backgroundColorRemovalLevel"),
        {dune::framework::data::constraints::ConstraintType::RANGE_INT,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Background Color Removal\nValue other than 0\n\nIncompatible Settings:\n\nOriginal Paper Type\n*Translucent\n*Ammonia");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndOnlyTicketTableNoCauseNewConstrainNAND_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));
    // With this settings on job intent, there is dynamic constraint generated
    auto jobIntent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    EXPECT_CALL(*jobIntent, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::DARK_BLUEPRINTS));
    EXPECT_CALL(*jobIntent, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent, getCopies()).WillRepeatedly(Return(2));
    auto ticketTable = givenJobTicketTable(jobIntent);

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("pipelineOptions/imageModifications/backgroundColorRemovalLevel"),
        {dune::framework::data::constraints::ConstraintType::RANGE_INT,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Background Color Removal\nValue other than 0\n\nIncompatible Settings:\n\nOriginal Paper Type\n*Translucent\n*Ammonia");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketNoCauseNewConstrainNOR_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(2));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));

    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("dest/print/copies"),
        {dune::framework::data::constraints::ConstraintType::RANGE_INT,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Copies\n*less than 0\n*more than 50\n\nIncompatible Settings:\n\nBackground Color Removal\nValue other than 4");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketTableNoCauseNewConstrainNOR_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(2));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));
    auto ticketTable = givenJobTicketTable(jobIntent_);    

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("dest/print/copies"),
        {dune::framework::data::constraints::ConstraintType::RANGE_INT,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Copies\n*less than 0\n*more than 50\n\nIncompatible Settings:\n\nBackground Color Removal\nValue other than 4");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndOnlyTicketTableNoCauseNewConstrainNOR_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));
    // With this settings on job intent, there is dynamic constraint generated
    auto jobIntent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    EXPECT_CALL(*jobIntent, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(2));
    EXPECT_CALL(*jobIntent, getCopies()).WillRepeatedly(Return(2));
    auto ticketTable = givenJobTicketTable(jobIntent);

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("dest/print/copies"),
        {dune::framework::data::constraints::ConstraintType::RANGE_INT,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Copies\n*less than 0\n*more than 50\n\nIncompatible Settings:\n\nBackground Color Removal\nValue other than 4");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketWithMultilevelConstrain_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::OLD_RECYCLED_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));

    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,constraintGroup_);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("pipelineOptions/imageModifications/outputCanvasOrientation"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Output Size > Orientation\n*Landscape\n\nIncompatible Settings:\n\nOriginal Paper Type\n*Old Recycled");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndTicketTableWithMultilevelConstrain_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::OLD_RECYCLED_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    auto ticketTable = givenJobTicketTable(jobIntent_);

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("pipelineOptions/imageModifications/outputCanvasOrientation"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Output Size > Orientation\n*Landscape\n\nIncompatible Settings:\n\nOriginal Paper Type\n*Old Recycled");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallToGetDynamicConstraintsAndOnlyTicketTableWithMultilevelConstrain_ThenResultIsConstraintsWithDynamicMessage)
{
    // With this settings on job intent, there is not dynamic constraint generated
    EXPECT_CALL(*jobIntent_, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::WHITE_PAPER));
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    EXPECT_CALL(*jobIntent_, getCopies()).WillRepeatedly(Return(2));
    // With this settings on job intent, there is dynamic constraint generated
    auto jobIntent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    EXPECT_CALL(*jobIntent, getOriginalMediaType()).WillRepeatedly(Return(dune::scan::types::OriginalMediaType::OLD_RECYCLED_PAPER));
    EXPECT_CALL(*jobIntent, getBackgroundColorRemovalLevel()).WillRepeatedly(Return(4));
    auto ticketTable = givenJobTicketTable(jobIntent);

    // Execute
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_, constraintGroup_, ticketTable);    

    // Check expectations
    ASSERT_EQ(constraintResult->getAllConstraints().size(),1);

    checkConstraintMessage(constraintResult->getConstraints("pipelineOptions/imageModifications/outputCanvasOrientation"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Output Size > Orientation\n*Landscape\n\nIncompatible Settings:\n\nOriginal Paper Type\n*Old Recycled");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenToGetDynamicConstraintsAndTicketWithFoldingStyleConstrained_ThenResultIsConstraintsWithDynamicMessage)
{
    ON_CALL(*jobIntent_, getOutputDestination()).WillByDefault(Return(dune::imaging::types::MediaDestinationId::STACKER));
    ON_CALL(*jobIntent_, getFoldingStyleId()).WillByDefault(Return(0));
    ON_CALL(*mockICopyJobTicket_, getIntent()).WillByDefault(Return(jobIntent_));

    // Setup static constraints
    std::shared_ptr<ConstraintsGroup> staticConstraints = std::make_shared<ConstraintsGroup>();
    auto foldingStyleStaticConstraints = getFoldingStyleStaticConstraints();
    staticConstraints->set("dest/print/foldingStyleId", foldingStyleStaticConstraints);

    createMockIFinishersDevices();

    component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints);

    // Check expectations
    ASSERT_EQ(staticConstraints->getAllConstraints().size(), 1); 

    checkConstraintMessage(staticConstraints->getConstraints("dest/print/foldingStyleId"),
        {dune::framework::data::constraints::ConstraintType::VALID_VALUE_SHORT,dune::framework::data::constraints::ConstraintType::LOCK},
        "The settings that you are configuring are incompatible with those already set in the printer.\n\n"
        "Folding Style\n*Folding style 1\n*Folding style 2\n\nIncompatible Settings:\n\nOutput Destination\n*Stacker");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallingParseCopyIntentTableValueToStringWithLocalizationProvider_TheResultIsLocalizedAndCorrect)
{
    auto internalTableInt8 = new dune::copy::Jobs::Copy::INT8T();
    internalTableInt8->value = 8;
    auto intentValueInt8 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::INT8T>(
        dune::copy::Jobs::Copy::CopyIntentValues::INT8,internalTableInt8);

    bool wasLocalizedInt8 = false;
    std::string valueAffectedInt8 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueInt8,
        wasLocalizedInt8,&mockILocaleProvider_);

    auto internalTableInt16 = new dune::copy::Jobs::Copy::INT16T();
    internalTableInt16->value = 16;
    auto intentValueInt16 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::INT16T>(
        dune::copy::Jobs::Copy::CopyIntentValues::INT16,internalTableInt16);

    bool wasLocalizedInt16 = false;
    std::string valueAffectedInt16 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueInt16,
        wasLocalizedInt16,&mockILocaleProvider_);

    auto internalTableInt32 = new dune::copy::Jobs::Copy::INT32T();
    internalTableInt32->value = 32;
    auto intentValueInt32 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::INT32T>(
        dune::copy::Jobs::Copy::CopyIntentValues::INT32,internalTableInt32);

    bool wasLocalizedInt32 = false;
    std::string valueAffectedInt32 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueInt32,
        wasLocalizedInt32,&mockILocaleProvider_);

    auto internalTableInt64 = new dune::copy::Jobs::Copy::INT64T();
    internalTableInt64->value = 64;
    auto intentValueInt64 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::INT64T>(
        dune::copy::Jobs::Copy::CopyIntentValues::INT64,internalTableInt64);

    bool wasLocalizedInt64 = false;
    std::string valueAffectedInt64 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueInt64,
        wasLocalizedInt64,&mockILocaleProvider_);

    auto internalTableUint8 = new dune::copy::Jobs::Copy::UINT8T();
    internalTableUint8->value = 8;
    auto intentValueUint8 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::UINT8T>(
        dune::copy::Jobs::Copy::CopyIntentValues::UINT8,internalTableUint8);

    bool wasLocalizedUint8 = false;
    std::string valueAffectedUint8 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUint8,
        wasLocalizedUint8,&mockILocaleProvider_);

    auto internalTableUint16 = new dune::copy::Jobs::Copy::UINT16T();
    internalTableUint16->value = 16;
    auto intentValueUint16 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::UINT16T>(
        dune::copy::Jobs::Copy::CopyIntentValues::UINT16,internalTableUint16);

    bool wasLocalizedUint16 = false;
    std::string valueAffectedUint16 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUint16,
        wasLocalizedUint16,&mockILocaleProvider_);

    auto internalTableUint32 = new dune::copy::Jobs::Copy::UINT32T();
    internalTableUint32->value = 32;
    auto intentValueUint32 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::UINT32T>(
        dune::copy::Jobs::Copy::CopyIntentValues::UINT32,internalTableUint32);

    bool wasLocalizedUint32 = false;
    std::string valueAffectedUint32 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUint32,
        wasLocalizedUint32,&mockILocaleProvider_);

    auto internalTableUint64 = new dune::copy::Jobs::Copy::UINT64T();
    internalTableUint64->value = 64;
    auto intentValueUint64 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::UINT64T>(
        dune::copy::Jobs::Copy::CopyIntentValues::UINT64,internalTableUint64);

    bool wasLocalizedUint64 = false;
    std::string valueAffectedUint64 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUint64,
        wasLocalizedUint64,&mockILocaleProvider_);

    auto internalTableDouble = new dune::copy::Jobs::Copy::DOUBLET();
    internalTableDouble->value = 5.5;
    auto intentValueUDouble = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::DOUBLET>(
        dune::copy::Jobs::Copy::CopyIntentValues::DOUBLE,internalTableDouble);

    bool wasLocalizedDouble = false;
    std::string valueAffectedDouble = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUDouble,
        wasLocalizedDouble,&mockILocaleProvider_);

    ASSERT_TRUE(wasLocalizedInt8);
    ASSERT_EQ(valueAffectedInt8, "*8");
    ASSERT_TRUE(wasLocalizedInt16);
    ASSERT_EQ(valueAffectedInt16, "*16");
    ASSERT_TRUE(wasLocalizedInt32);
    ASSERT_EQ(valueAffectedInt32, "*32");
    ASSERT_TRUE(wasLocalizedInt64);
    ASSERT_EQ(valueAffectedInt64, "*64");
    ASSERT_TRUE(wasLocalizedUint8);
    ASSERT_EQ(valueAffectedUint8, "*8");
    ASSERT_TRUE(wasLocalizedUint16);
    ASSERT_EQ(valueAffectedUint16, "*16");
    ASSERT_TRUE(wasLocalizedUint32);
    ASSERT_EQ(valueAffectedUint32, "*32");
    ASSERT_TRUE(wasLocalizedUint64);
    ASSERT_EQ(valueAffectedUint64, "*64");
    ASSERT_TRUE(wasLocalizedDouble);
    ASSERT_EQ(valueAffectedDouble, "*5.500000");
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectWithJsonWithDynamicStringGeneration, 
    WhenCallingParseCopyIntentTableValueToStringWithNoLocalizationProvider_TheResultIsNotLocalizedAndEmpty)
{
    auto internalTableInt8 = new dune::copy::Jobs::Copy::INT8T();
    internalTableInt8->value = 8;
    auto intentValueInt8 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::INT8T>(
        dune::copy::Jobs::Copy::CopyIntentValues::INT8,internalTableInt8);

    bool wasLocalizedInt8 = false;
    std::string valueAffectedInt8 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueInt8,
        wasLocalizedInt8,nullptr);

    auto internalTableInt16 = new dune::copy::Jobs::Copy::INT16T();
    internalTableInt16->value = 16;
    auto intentValueInt16 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::INT16T>(
        dune::copy::Jobs::Copy::CopyIntentValues::INT16,internalTableInt16);

    bool wasLocalizedInt16 = false;
    std::string valueAffectedInt16 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueInt16,
        wasLocalizedInt16,nullptr);

    auto internalTableInt32 = new dune::copy::Jobs::Copy::INT32T();
    internalTableInt32->value = 32;
    auto intentValueInt32 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::INT32T>(
        dune::copy::Jobs::Copy::CopyIntentValues::INT32,internalTableInt32);

    bool wasLocalizedInt32 = false;
    std::string valueAffectedInt32 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueInt32,
        wasLocalizedInt32,nullptr);

    auto internalTableInt64 = new dune::copy::Jobs::Copy::INT64T();
    internalTableInt64->value = 64;
    auto intentValueInt64 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::INT64T>(
        dune::copy::Jobs::Copy::CopyIntentValues::INT64,internalTableInt64);

    bool wasLocalizedInt64 = false;
    std::string valueAffectedInt64 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueInt64,
        wasLocalizedInt64,nullptr);

    auto internalTableUint8 = new dune::copy::Jobs::Copy::UINT8T();
    internalTableUint8->value = 8;
    auto intentValueUint8 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::UINT8T>(
        dune::copy::Jobs::Copy::CopyIntentValues::UINT8,internalTableUint8);

    bool wasLocalizedUint8 = false;
    std::string valueAffectedUint8 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUint8,
        wasLocalizedUint8,nullptr);

    auto internalTableUint16 = new dune::copy::Jobs::Copy::UINT16T();
    internalTableUint16->value = 16;
    auto intentValueUint16 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::UINT16T>(
        dune::copy::Jobs::Copy::CopyIntentValues::UINT16,internalTableUint16);

    bool wasLocalizedUint16 = false;
    std::string valueAffectedUint16 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUint16,
        wasLocalizedUint16,nullptr);

    auto internalTableUint32 = new dune::copy::Jobs::Copy::UINT32T();
    internalTableUint32->value = 32;
    auto intentValueUint32 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::UINT32T>(
        dune::copy::Jobs::Copy::CopyIntentValues::UINT32,internalTableUint32);

    bool wasLocalizedUint32 = false;
    std::string valueAffectedUint32 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUint32,
        wasLocalizedUint32,nullptr);

    auto internalTableUint64 = new dune::copy::Jobs::Copy::UINT64T();
    internalTableUint64->value = 64;
    auto intentValueUint64 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::UINT64T>(
        dune::copy::Jobs::Copy::CopyIntentValues::UINT64,internalTableUint64);

    bool wasLocalizedUint64 = false;
    std::string valueAffectedUint64 = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUint64,
        wasLocalizedUint64,nullptr);

    auto internalTableDouble = new dune::copy::Jobs::Copy::DOUBLET();
    internalTableDouble->value = 5.5;
    auto intentValueUDouble = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::createCopyIntentUnionValue<dune::copy::Jobs::Copy::DOUBLET>(
        dune::copy::Jobs::Copy::CopyIntentValues::DOUBLE,internalTableDouble);

    bool wasLocalizedDouble = false;
    std::string valueAffectedDouble = dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValueUDouble,
        wasLocalizedDouble,nullptr);

    ASSERT_FALSE(wasLocalizedInt8);
    ASSERT_EQ(valueAffectedInt8, "");
    ASSERT_FALSE(wasLocalizedInt16);
    ASSERT_EQ(valueAffectedInt16, "");
    ASSERT_FALSE(wasLocalizedInt32);
    ASSERT_EQ(valueAffectedInt32, "");
    ASSERT_FALSE(wasLocalizedInt64);
    ASSERT_EQ(valueAffectedInt64, "");
    ASSERT_FALSE(wasLocalizedUint8);
    ASSERT_EQ(valueAffectedUint8, "");
    ASSERT_FALSE(wasLocalizedUint16);
    ASSERT_EQ(valueAffectedUint16, "");
    ASSERT_FALSE(wasLocalizedUint32);
    ASSERT_EQ(valueAffectedUint32, "");
    ASSERT_FALSE(wasLocalizedUint64);
    ASSERT_EQ(valueAffectedUint64, "");
    ASSERT_FALSE(wasLocalizedDouble);
    ASSERT_EQ(valueAffectedDouble, "");
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized :
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized : 
    public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase,
    public ::testing::WithParamInterface< std::tuple<std::string, std::vector<ColorModes>>>
{
public:
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized() : 
        GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase() {};
    ~GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized(){};

    void SetUp() override;
    void TearDown() override;

    std::shared_ptr<ConstraintsGroup>   staticConstraints_{nullptr};
    std::string                         jsonToLoad_="";
    std::vector<ColorModes>             expectedConstraints_;
};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized::SetUp()
{
    GTEST_CHECKPOINTA("GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized::SetUp -- ENTER\n");

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::SetUp();

    // Get param values
    jsonToLoad_ = std::get<0>(GetParam());
    expectedConstraints_ = std::get<1>(GetParam());
  
    systemServices_ = std::make_unique<TestSystemServices>();    
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", jsonToLoad_);

    GTEST_CHECKPOINTA("json to be loaded %s\n",jsonToLoad_.c_str());

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    std::future<void> asyncCompletion;
    comp_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Setup static constraints
    staticConstraints_ = std::make_shared<ConstraintsGroup>();
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    staticConstraints_->set("src/scan/colorMode", colorConstraints);

    GTEST_CHECKPOINTA("GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized::SetUp -- EXIT");
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized::TearDown()
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::TearDown();
}

TEST_P(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized, WhenCallToGetDynamicConstraints_ThenResultIsConstraintExpected)
{
    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_);

    // Check Result
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(expectedConstraints_,constraints);
}

TEST_P(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized, WhenCallToGetDynamicConstraintsWithEmptyJobTicketTable_ThenResultIsConstraintExpected)
{
    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenEmptyJobTicketTable());

    // Check Result
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(expectedConstraints_,constraints);
}

TEST_P(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized, WhenCallToGetDynamicConstraintsWithJobTicketTable_ThenResultIsConstraintExpected)
{
    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenJobTicketTable());

    // Check Result
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(expectedConstraints_,constraints);
}

INSTANTIATE_TEST_CASE_P(, GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithTestRuleParametrized, ::testing::Values
(
    // jsonWithInputBehavior    ExpectedVectorResult
    std::make_tuple("./testResources/jsonTestPolicies/EmptyIf.json",std::vector<ColorModes>{}),
    // Policy Stop Not Resolved if
    std::make_tuple("./testResources/jsonTestPolicies/NotResolvedIf.json",std::vector<ColorModes>{}),
    // Policy Stop Resolved if then to supported value on static
    std::make_tuple("./testResources/jsonTestPolicies/ResolvedIfThenSupported.json",std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale}),
    // Policy Stop Resolved if then to not supported value on static
    std::make_tuple("./testResources/jsonTestPolicies/ResolvedIfThenNotSupported.json",std::vector<ColorModes>{}),
    // Policy Continue First rule Applied constraints second rule empty if
    std::make_tuple("./testResources/jsonTestPolicies/FirstOkSecondEmptyIf.json",std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale}),  
    // Policy Continue First rule Applied constraints second rule Not Resolved if
    std::make_tuple("./testResources/jsonTestPolicies/FirstOkSecondNotResolvedIf.json",std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale}),
    // Policy Continue First rule Applied constraints second rule Resolved if then to supported value on static
    std::make_tuple("./testResources/jsonTestPolicies/FirstOkSecondThenSupported.json",std::vector<ColorModes>{ColorModes::color}),
    // Policy Stop, AND operation - two works
    std::make_tuple("./testResources/jsonTestPolicies/AndOperationTwoOk.json",std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale}),
    // Policy Stop, AND operation - two fail
    std::make_tuple("./testResources/jsonTestPolicies/AndOperationTwoFail.json",std::vector<ColorModes>{}),
    // Policy Stop, AND operation - fist work, second fail
    std::make_tuple("./testResources/jsonTestPolicies/AndOperationFirstOkSecondFail.json",std::vector<ColorModes>{}),
    // Policy Stop, OR operation - two works
    std::make_tuple("./testResources/jsonTestPolicies/OrOperationTwoOk.json",std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale}),
    // Policy Stop, OR operation - two fail
    std::make_tuple("./testResources/jsonTestPolicies/OrOperationTwoFail.json",std::vector<ColorModes>{}),
    // Policy Stop, OR operation - fist work, second fail
    std::make_tuple("./testResources/jsonTestPolicies/OrOperationFirstOkSecondFail.json",std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale}),
    // Policy Stop, NAND operation - two works
    std::make_tuple("./testResources/jsonTestPolicies/NandOperationTwoOk.json",std::vector<ColorModes>{}),
    // Policy Stop, NAND operation - two fail
    std::make_tuple("./testResources/jsonTestPolicies/NandOperationTwoFail.json",std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale}),
    // Policy Stop, NAND operation - fist work, second fail
    std::make_tuple("./testResources/jsonTestPolicies/NandOperationFirstOkSecondFail.json",std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale}),
    // Policy Stop, NOR operation - two works
    std::make_tuple("./testResources/jsonTestPolicies/NorOperationTwoOk.json",std::vector<ColorModes>{}),
    // Policy Stop, NOR operation - two fail
    std::make_tuple("./testResources/jsonTestPolicies/NorOperationTwoFail.json",std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale}),
    // Policy Stop, NOR operation - fist work, second fail
    std::make_tuple("./testResources/jsonTestPolicies/NorOperationFirstOkSecondFail.json",std::vector<ColorModes>{})
));

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits :
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits : 
    public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase
{
public:
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits() : 
        GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase() {};
    ~GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits(){};

    void SetUp() override;
    void TearDown() override;
    void setValuesOnStaticConstraint();
    void setupComponent();

    std::string                         jsonToLoad_="";
    std::shared_ptr<ConstraintsGroup>   staticConstraints_{nullptr};
};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits::SetUp()
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::SetUp();

    staticConstraints_ = std::make_shared<ConstraintsGroup>();

    ON_CALL(mockILocaleProvider_,getMeasurmentUnit()).WillByDefault(Return(dune::localization::MeasurementUnit::METRIC));
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits::TearDown()
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::TearDown();
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits::setValuesOnStaticConstraint()
{
    auto colorConstraints = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>({
        ColorModes::color, 
        ColorModes::grayscale, 
        ColorModes::blackAndWhite
    });
    staticConstraints_->set("src/scan/colorMode", colorConstraints);
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits::setupComponent()
{
    systemServices_ = std::make_unique<TestSystemServices>();    
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", jsonToLoad_);

    GTEST_CHECKPOINTA("json to be loaded %s\n",jsonToLoad_.c_str());

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    std::future<void> asyncCompletion;
    comp_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticEmpty_ThenResultIsAnEmptyListOfConstraints)
{
    // Expectations
    jsonToLoad_ = "./testResources/EmptyBaseDynamicContraintRules.json";
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_);

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    EXPECT_TRUE(staticConstraints_->getAllConstraints().empty());
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticEmptyAndEmptyJobTicket_ThenResultIsAnEmptyListOfConstraints)
{
    // Expectations
    jsonToLoad_ = "./testResources/EmptyBaseDynamicContraintRules.json";
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenEmptyJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    EXPECT_TRUE(staticConstraints_->getAllConstraints().empty());
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticEmptyAndJobTicketTable_ThenResultIsAnEmptyListOfConstraints)
{
    // Expectations
    jsonToLoad_ = "./testResources/EmptyBaseDynamicContraintRules.json";
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    EXPECT_TRUE(staticConstraints_->getAllConstraints().empty());
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListIsEmpty_ThenResultIsAListWithEmptyListAndStaticConstraintConserveOriginalConstraint)
{
    // Expectations
    jsonToLoad_ = "./testResources/EmptyBaseDynamicContraintRules.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_);

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale, ColorModes::blackAndWhite},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListIsEmptyAndEmptyJobTicketTable_ThenResultIsAListWithEmptyListAndStaticConstraintConserveOriginalConstraint)
{
    // Expectations
    jsonToLoad_ = "./testResources/EmptyBaseDynamicContraintRules.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenEmptyJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale, ColorModes::blackAndWhite},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListIsEmptyAndJobTicketTable_ThenResultIsAListWithEmptyListAndStaticConstraintConserveOriginalConstraint)
{
    // Expectations
    jsonToLoad_ = "./testResources/EmptyBaseDynamicContraintRules.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale, ColorModes::blackAndWhite},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListHaveDifferentConstraints_ThenResultIsAListWithEmptyListAndStaticConstraintConserveOriginalConstraint)
{
    // Expectations
    jsonToLoad_ = "./testResources/UnitNotCompatibleConstraint.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_);

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale, ColorModes::blackAndWhite},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListHaveDifferentConstraintsAndEmptyJobTicketTable_ThenResultIsAListWithEmptyListAndStaticConstraintConserveOriginalConstraint)
{
    // Expectations
    jsonToLoad_ = "./testResources/UnitNotCompatibleConstraint.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenEmptyJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale, ColorModes::blackAndWhite},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListHaveDifferentConstraintsAndJobTicketTable_ThenResultIsAListWithEmptyListAndStaticConstraintConserveOriginalConstraint)
{
    // Expectations
    jsonToLoad_ = "./testResources/UnitNotCompatibleConstraint.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale, ColorModes::blackAndWhite},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListHaveSameConstraintToBeChangedAndUnitsIsMetric_ThenResultIsAnEmptyListButStaticConstraintsChanged)
{
    // Expectations
    jsonToLoad_ = "./testResources/UnitCompatibleConstraint.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_);

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::blackAndWhite},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListHaveSameConstraintToBeChangedAndUnitsIsMetricAndEmptyJobTicketTable_ThenResultIsAnEmptyListButStaticConstraintsChanged)
{
    // Expectations
    jsonToLoad_ = "./testResources/UnitCompatibleConstraint.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenEmptyJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::blackAndWhite},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListHaveSameConstraintToBeChangedAndUnitsIsMetricAndJobTicketTable_ThenResultIsAnEmptyListButStaticConstraintsChanged)
{
    // Expectations
    jsonToLoad_ = "./testResources/UnitCompatibleConstraint.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::blackAndWhite},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListHaveSameConstraintToBeChangedAndUnitsIsUS_ThenResultIsAnEmptyListButStaticConstraintsChanged)
{
    // Expectations
    EXPECT_CALL(mockILocaleProvider_,getMeasurmentUnit()).WillRepeatedly(Return(dune::localization::MeasurementUnit::US));
    jsonToLoad_ = "./testResources/UnitCompatibleConstraint.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_);

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListHaveSameConstraintToBeChangedAndUnitsIsUSAndEmptyJobTicketTable_ThenResultIsAnEmptyListButStaticConstraintsChanged)
{
    // Expectations
    EXPECT_CALL(mockILocaleProvider_,getMeasurmentUnit()).WillRepeatedly(Return(dune::localization::MeasurementUnit::US));
    jsonToLoad_ = "./testResources/UnitCompatibleConstraint.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenEmptyJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale},constraints);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithCheckListOfRulesAffectedByUnits,
    WhenCallToGetDynamicConstraintsWithStaticConstraintNonEmptyAndListHaveSameConstraintToBeChangedAndUnitsIsUSAndJobTicketTable_ThenResultIsAnEmptyListButStaticConstraintsChanged)
{
    // Expectations
    EXPECT_CALL(mockILocaleProvider_,getMeasurmentUnit()).WillRepeatedly(Return(dune::localization::MeasurementUnit::US));
    jsonToLoad_ = "./testResources/UnitCompatibleConstraint.json";
    setValuesOnStaticConstraint();
    setupComponent();

    // Execute getter
    auto constraintResult = component_->getDynamicConstraints(mockICopyJobTicket_,staticConstraints_, givenJobTicketTable());

    // Check Results
    EXPECT_TRUE(constraintResult->getAllConstraints().empty());
    auto constraints = constraintResult->getConstraints("src/scan/colorMode");
    checkConstraintResult<ColorModes>(std::vector<ColorModes>{ColorModes::color, ColorModes::grayscale},constraints);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket :
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket : 
    public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase
{
public:

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket() : 
        GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase() {};
    ~GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket(){};

    void SetUp() override;

    void TearDown() override;

    void setupComponent();
    std::shared_ptr<ConstraintsGroup> setUpConstraints();

    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> givenEmptyJobTicketTableWithoutSubTables();
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> givenEmptyJobTicketTableWithoutScan();
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> givenEmptyJobTicketTableWithoutPipelineOptions();
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> givenEmptyJobTicketTableWithoutPrint();

    void checkExpectedJobTicketTable(std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> updatedTable);

    std::shared_ptr<ConstraintsGroup> constraints_{nullptr};
    std::string jsonToLoad_="";
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketTable_{nullptr};
    std::shared_ptr<ConstraintsGroup> allConstraints_{nullptr};
};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::SetUp()
{
    GTEST_CHECKPOINTA("GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::SetUp -- ENTER\n");

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::SetUp();
  
    // setup component
    jsonToLoad_ = "./testResources/AllListOfSettings.json";

    // Setup static constraints
    allConstraints_ = setUpConstraints();

    GTEST_CHECKPOINTA("GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::SetUp -- EXIT");
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::TearDown()
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatConnectBase::TearDown();
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::setupComponent()
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyJobDynamicConstraintRulesLargeFormatConfig.fbs", jsonToLoad_);
    
    GTEST_CHECKPOINTA("json to be loaded %s\n",jsonToLoad_.c_str());

    comp_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    std::future<void> asyncCompletion;
    comp_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

std::shared_ptr<ConstraintsGroup> GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::setUpConstraints()
{
    // Setup all constraints currently supported with a unique option
    auto constraintGroup = std::make_shared<ConstraintsGroup>();

    auto tempConstraint = std::make_shared<Constraints>();

    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::MediaSize>(dune::cdm::glossary_1::MediaSize::iso_a0_841x1189mm);
    constraintGroup->set("src/scan/mediaSize", tempConstraint); 
    constraintGroup->set("pipelineOptions/imageModifications/outputCanvasMediaSize", tempConstraint);
    constraintGroup->set("pipelineOptions/scaling/scaleToSize", tempConstraint);
    constraintGroup->set("dest/print/mediaSize", tempConstraint);
    
    tempConstraint = createConstraintRange(0);
    constraintGroup->set("src/scan/xOffset", tempConstraint); 
    constraintGroup->set("src/scan/yOffset", tempConstraint);
    constraintGroup->set("src/scan/gamma", tempConstraint);
    constraintGroup->set("src/scan/highlight", tempConstraint);
    constraintGroup->set("src/scan/colorSensitivity", tempConstraint);
    constraintGroup->set("src/scan/colorRange", tempConstraint);
    constraintGroup->set("src/scan/shadow", tempConstraint);
    constraintGroup->set("src/scan/compressionFactor", tempConstraint);
    constraintGroup->set("src/scan/threshold", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/sharpness", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/backgroundCleanup", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/exposure", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/contrast", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/backgroundColorRemovalLevel", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/blackEnhancementLevel", tempConstraint);
    constraintGroup->set("pipelineOptions/scaling/xScalePercent", tempConstraint);
    constraintGroup->set("pipelineOptions/scaling/yScalePercent", tempConstraint);
    constraintGroup->set("dest/print/copies", tempConstraint);

    tempConstraint = createConstraintRange((double) 0.0);
    constraintGroup->set("pipelineOptions/imageModifications/outputCanvasCustomWidth", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/outputCanvasCustomLength", tempConstraint);

    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::PlexMode>(dune::cdm::glossary_1::PlexMode::simplex);
    constraintGroup->set("src/scan/plexMode", tempConstraint);
    constraintGroup->set("dest/print/plexMode", tempConstraint);

    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::ContentOrientation>(dune::cdm::glossary_1::ContentOrientation::landscape);
    constraintGroup->set("src/scan/contentOrientation", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/outputCanvasOrientation", tempConstraint);

    tempConstraint = createConstraintFeatureEnabledEnum(dune::cdm::glossary_1::FeatureEnabled::false_);
    constraintGroup->set("src/scan/pagesFlipUpEnabled", tempConstraint);
    constraintGroup->set("src/scan/blackBackground", tempConstraint);
    constraintGroup->set("src/scan/autoExposure", tempConstraint);
    constraintGroup->set("src/scan/descreen", tempConstraint);
    constraintGroup->set("src/scan/feederPickStop", tempConstraint);
    constraintGroup->set("src/scan/autoDeskew", tempConstraint);
    constraintGroup->set("src/scan/edgeToEdgeScan", tempConstraint);
    constraintGroup->set("src/scan/longPlotScan", tempConstraint);
    constraintGroup->set("src/scan/invertColors", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/blankPageSuppressionEnabled", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/backgroundNoiseRemoval", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/backgroundColorRemoval", tempConstraint);
    constraintGroup->set("pipelineOptions/manualUserOperations/autoRelease", tempConstraint);
    constraintGroup->set("pipelineOptions/scaling/scaleToFitEnabled", tempConstraint);

    std::vector<short> shortVector{0,256,259};
    tempConstraint = createConstraintShort(shortVector);
    constraintGroup->set("dest/print/foldingStyleId", tempConstraint);

    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::MediaSourceId>(dune::cdm::glossary_1::MediaSourceId::roll_dash_1);
    constraintGroup->set("pipelineOptions/scaling/scaleToOutput", tempConstraint);
    constraintGroup->set("pipelineOptions/imageModifications/outputCanvasMediaId", tempConstraint);
    constraintGroup->set("dest/print/mediaSource", tempConstraint);

    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::ColorModes>(dune::cdm::jobTicket_1::ColorModes::color);
    constraintGroup->set("src/scan/colorMode", tempConstraint); 
    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::ScanMediaSourceId>(dune::cdm::glossary_1::ScanMediaSourceId::mdf);
    constraintGroup->set("src/scan/mediaSource", tempConstraint); 
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::Resolutions>(dune::cdm::jobTicket_1::Resolutions::e600Dpi);
    constraintGroup->set("src/scan/resolution", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::ContentType>(dune::cdm::jobTicket_1::ContentType::mixed);
    constraintGroup->set("src/scan/contentType", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::AutoColorDetect>(dune::cdm::jobTicket_1::AutoColorDetect::detectOnly);
    constraintGroup->set("src/scan/autoColorDetect", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::ScanMediaType>(dune::cdm::glossary_1::ScanMediaType::whitePaper);
    constraintGroup->set("src/scan/mediaType", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::CcdChannel>(dune::cdm::jobTicket_1::CcdChannel::blue);
    constraintGroup->set("src/scan/ccdChannel", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::BinaryRendering>(dune::cdm::jobTicket_1::BinaryRendering::errorDiffusion);
    constraintGroup->set("src/scan/binaryRendering", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::ScanCaptureMode>(dune::cdm::jobTicket_1::ScanCaptureMode::standard);
    constraintGroup->set("src/scan/scanCaptureMode", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>(dune::cdm::jobTicket_1::ScanAcquisitionsSpeed::auto_);
    constraintGroup->set("src/scan/scanAcquisitionsSpeed", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::PagesPerSheet>(dune::cdm::jobTicket_1::PagesPerSheet::oneUp);
    constraintGroup->set("pipelineOptions/imageModifications/pagesPerSheet", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::OutputCanvasAnchor>(dune::cdm::jobTicket_1::OutputCanvasAnchor::middleLeft);
    constraintGroup->set("pipelineOptions/imageModifications/outputCanvasAnchor", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>(
        dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration::enable);
    constraintGroup->set("pipelineOptions/manualUserOperations/imagePreviewConfiguration", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>(dune::cdm::jobTicket_1::scaling::ScaleSelection::custom);
    constraintGroup->set("pipelineOptions/scaling/scaleSelection", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::CollateModes>(dune::cdm::jobTicket_1::CollateModes::collated);
    constraintGroup->set("dest/print/collate", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::MediaDestinationId>(dune::cdm::glossary_1::MediaDestinationId::bin);
    constraintGroup->set("dest/print/mediaDestination", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::MediaType>(dune::cdm::glossary_1::MediaType::any);
    constraintGroup->set("dest/print/mediaType", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::DuplexBinding>(dune::cdm::glossary_1::DuplexBinding::oneSided);
    constraintGroup->set("dest/print/duplexBinding", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::glossary_1::PrintQuality>(dune::cdm::glossary_1::PrintQuality::best);
    constraintGroup->set("dest/print/printQuality", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::PrintingOrder>(dune::cdm::jobTicket_1::PrintingOrder::firstPageOnTop);
    constraintGroup->set("dest/print/printingOrder", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::mediaProfile_1::MediaFamilyEnum>(dune::cdm::mediaProfile_1::MediaFamily::plain);
    constraintGroup->set("dest/print/mediaFamily", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::RotateEnum>(dune::cdm::jobTicket_1::Rotate::auto_);
    constraintGroup->set("dest/print/rotate", tempConstraint);
    tempConstraint = createConstraintEnum<dune::cdm::jobTicket_1::PrintMargins>(dune::cdm::jobTicket_1::PrintMargins::clipContents);
    constraintGroup->set("dest/print/printMargins", tempConstraint);

    return constraintGroup;
}

std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> 
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::givenEmptyJobTicketTableWithoutSubTables()
{
    // Setup job base update
    auto serializedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    serializedJobTicketTable->beginMergePatch();
    serializedJobTicketTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    return serializedJobTicketTable;
}

std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> 
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::givenEmptyJobTicketTableWithoutScan()
{
    // Setup job base update
    auto serializedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    serializedJobTicketTable->beginMergePatch();
    serializedJobTicketTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    // pipelineOptions
    serializedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
    serializedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
    //pipelineOptions.imageModifications
    auto imageModificationsTable = std::make_unique<dune::cdm::jobTicket_1::ImageModificationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications = *(imageModificationsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications.beginMergePatch();
    //pipelineOptions.manualUserOperations
    auto manualOpsTable = std::make_unique<dune::cdm::jobTicket_1::ManualUserOperationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations = *(manualOpsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.beginMergePatch();
    //pipelineOptions.scaling
    auto scalingTable = std::make_unique<dune::cdm::jobTicket_1::ScalingTable>();    
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling = *(scalingTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling.beginMergePatch();

    // dest
    auto destTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::DestTable>();
    serializedJobTicketTable->dest = *destTable;
    serializedJobTicketTable->dest.beginMergePatch();
    // dest.print
    auto printTable = std::make_unique<dune::cdm::jobTicket_1::PrintTable>();
    printTable->beginMergePatch();
    serializedJobTicketTable->dest.getMutable()->print = *(printTable);

    return serializedJobTicketTable;
}

std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> 
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::givenEmptyJobTicketTableWithoutPipelineOptions()
{
    // Setup job base update
    auto serializedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    serializedJobTicketTable->beginMergePatch();
    serializedJobTicketTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    // src
    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    serializedJobTicketTable->src = *srcTable;
    serializedJobTicketTable->src.beginMergePatch();

    // src
    // src.scan
    auto scanTable = std::make_unique<dune::cdm::jobTicket_1::ScanTable>();
    serializedJobTicketTable->src.getMutable()->scan = *(scanTable);
    serializedJobTicketTable->src.getMutable()->scan.beginMergePatch();

    // dest
    auto destTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::DestTable>();
    serializedJobTicketTable->dest = *destTable;
    serializedJobTicketTable->dest.beginMergePatch();
    // dest.print
    auto printTable = std::make_unique<dune::cdm::jobTicket_1::PrintTable>();
    printTable->beginMergePatch();
    serializedJobTicketTable->dest.getMutable()->print = *(printTable);

    return serializedJobTicketTable;
}

std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> 
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::givenEmptyJobTicketTableWithoutPrint()
{
    // Setup job base update
    auto serializedJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    serializedJobTicketTable->beginMergePatch();
    serializedJobTicketTable->ticketId = dune::framework::core::Uuid::createUuid().toString(false);

    // src
    auto srcTable = std::make_unique<dune::cdm::jobTicket_1::jobTicket::SrcTable>();
    serializedJobTicketTable->src = *srcTable;
    serializedJobTicketTable->src.beginMergePatch();

    // src
    // src.scan
    auto scanTable = std::make_unique<dune::cdm::jobTicket_1::ScanTable>();
    serializedJobTicketTable->src.getMutable()->scan = *(scanTable);
    serializedJobTicketTable->src.getMutable()->scan.beginMergePatch();

    // pipelineOptions
    serializedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
    serializedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
    //pipelineOptions.imageModifications
    auto imageModificationsTable = std::make_unique<dune::cdm::jobTicket_1::ImageModificationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications = *(imageModificationsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications.beginMergePatch();
    //pipelineOptions.manualUserOperations
    auto manualOpsTable = std::make_unique<dune::cdm::jobTicket_1::ManualUserOperationsTable>();
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations = *(manualOpsTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations.beginMergePatch();
    //pipelineOptions.scaling
    auto scalingTable = std::make_unique<dune::cdm::jobTicket_1::ScalingTable>();    
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling = *(scalingTable);
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling.beginMergePatch();

    return serializedJobTicketTable;
}

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::checkExpectedJobTicketTable(
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> updatedTable)
{
    EXPECT_EQ(updatedTable->src.get()->scan.get()->colorMode.get(), dune::cdm::jobTicket_1::ColorModes::color);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->mediaSource.get(), dune::cdm::glossary_1::ScanMediaSourceId::mdf);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->mediaSize.get(), dune::cdm::glossary_1::MediaSize::iso_a0_841x1189mm);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->xOffset.get(), 0);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->yOffset.get(), 0);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->plexMode.get(), dune::cdm::glossary_1::PlexMode::simplex);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->resolution.get(), dune::cdm::jobTicket_1::Resolutions::e600Dpi);
    // EXPECT_EQ(updatedTable->src.get()->scan.get()->pageBinding.get(), ); // Not supported at ticket level
    EXPECT_EQ(updatedTable->src.get()->scan.get()->contentType.get(), dune::cdm::jobTicket_1::ContentType::mixed);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->contentOrientation.get(), dune::cdm::glossary_1::ContentOrientation::landscape);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->pagesFlipUpEnabled.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->autoColorDetect.get(), dune::cdm::jobTicket_1::AutoColorDetect::detectOnly);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->blackBackground.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->mediaType.get(), dune::cdm::glossary_1::ScanMediaType::whitePaper);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->autoExposure.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->gamma.get(), 0);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->highlight.get(), 0);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->colorSensitivity.get(), 0);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->colorRange.get(), 0);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->ccdChannel.get(), dune::cdm::jobTicket_1::CcdChannel::blue);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->binaryRendering.get(), dune::cdm::jobTicket_1::BinaryRendering::errorDiffusion);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->descreen.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->feederPickStop.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->shadow.get(), 0);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->compressionFactor.get(), 0);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->threshold.get(), 0);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->scanCaptureMode.get(), dune::cdm::jobTicket_1::ScanCaptureMode::standard);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->scanAcquisitionsSpeed.get(), dune::cdm::jobTicket_1::ScanAcquisitionsSpeed::auto_);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->autoDeskew.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->edgeToEdgeScan.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->longPlotScan.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->src.get()->scan.get()->invertColors.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->sharpness.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->backgroundCleanup.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->exposure.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->contrast.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->blankPageSuppressionEnabled.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->pagesPerSheet.get(), dune::cdm::jobTicket_1::PagesPerSheet::oneUp);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->outputCanvasMediaSize.get(), dune::cdm::glossary_1::MediaSize::iso_a0_841x1189mm);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->outputCanvasMediaId.get(), dune::cdm::glossary_1::MediaSourceId::roll_dash_1);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomLength.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->outputCanvasAnchor.get(), dune::cdm::jobTicket_1::OutputCanvasAnchor::middleLeft);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->outputCanvasOrientation.get(), dune::cdm::glossary_1::ContentOrientation::landscape);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->backgroundNoiseRemoval.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemovalLevel.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->imageModifications.get()->blackEnhancementLevel.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->manualUserOperations.get()->imagePreviewConfiguration.get(), dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration::enable);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->manualUserOperations.get()->autoRelease.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->scaling.get()->scaleToFitEnabled.get(), dune::cdm::glossary_1::FeatureEnabled::false_);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->scaling.get()->xScalePercent.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->scaling.get()->yScalePercent.get(), 0);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->scaling.get()->scaleSelection.get(), dune::cdm::jobTicket_1::scaling::ScaleSelection::custom);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->scaling.get()->scaleToOutput.get(), dune::cdm::glossary_1::MediaSourceId::roll_dash_1);
    EXPECT_EQ(updatedTable->pipelineOptions.get()->scaling.get()->scaleToSize.get(), dune::cdm::glossary_1::MediaSize::iso_a0_841x1189mm);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->collate.get(), dune::cdm::jobTicket_1::CollateModes::collated);
    // EXPECT_EQ(updatedTable->dest.get()->print.get()->colorMode.get(), ); // Not supported
    EXPECT_EQ(updatedTable->dest.get()->print.get()->copies.get(), 0);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->foldingStyleId.get(), 0);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->mediaSource.get(), dune::cdm::glossary_1::MediaSourceId::roll_dash_1);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->mediaDestination.get(), dune::cdm::glossary_1::MediaDestinationId::bin);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->mediaSize.get(), dune::cdm::glossary_1::MediaSize::iso_a0_841x1189mm);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->mediaType.get(), dune::cdm::glossary_1::MediaType::any);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->plexMode.get(), dune::cdm::glossary_1::PlexMode::simplex);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->duplexBinding.get(), dune::cdm::glossary_1::DuplexBinding::oneSided);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->printQuality.get(), dune::cdm::glossary_1::PrintQuality::best);
    // EXPECT_EQ(updatedTable->dest.get()->print.get()->resolution.get(),); // Not supported yet
    EXPECT_EQ(updatedTable->dest.get()->print.get()->printingOrder.get(), dune::cdm::jobTicket_1::PrintingOrder::firstPageOnTop);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->mediaFamily.get(), dune::cdm::mediaProfile_1::MediaFamily::plain);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->rotate.get(), dune::cdm::jobTicket_1::Rotate::auto_);
    EXPECT_EQ(updatedTable->dest.get()->print.get()->printMargins.get(), dune::cdm::jobTicket_1::PrintMargins::clipContents);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnTable_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job base update
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenJobTicketTable();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnTableAndStaticConstraints_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job base update
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenJobTicketTable();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicket_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketAndStaticConstraints_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketAndTableWithoutSubTables_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTableWithoutSubTables();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketAndTableWithoutSubTablesAndStaticConstraints_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTableWithoutSubTables();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithScanTableNull_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTableWithoutScan();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithScanTableNullAndStaticConstraints_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTableWithoutScan();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithPipelineOptionsTableNull_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTableWithoutPipelineOptions();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithPipelineOptionsTableNullAndStaticConstraints_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTableWithoutPipelineOptions();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithDestTableNullAnd_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTableWithoutPrint();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithDestTableNullAndStaticConstraints_ThenExpectedForChangesOnTicketOccurs)
{
    setupComponent();
    // Setup job ticket & job base update
    givenJobTicketIntent(jobIntent_);
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTableWithoutPrint();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Expected check
    checkExpectedJobTicketTable(serializedJobTicketTable);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithDesiredForceSetsNonEmptyAndListHaveDifferentConstraintToBeChanged_ThenExpectedNoChangesOnTicketOccurs)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/DynamicForceSets.json";
    setupComponent(); 
    givenJobTicketIntent(jobIntent_);

    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();
    // ContentType didn't change
    // `backgroundColorRemoval` on the ticket is true

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Check Results
    bool settingUpdated = false;
    dune::copy::Jobs::Copy::Map2CheckerCdmTableProperty::executeMapFunction("pipelineOptions/imageModifications/backgroundColorRemoval", 
        serializedJobTicketTable, settingUpdated);
    EXPECT_EQ(settingUpdated, false); // no changes
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithDesiredForceSetsNonEmptyAndListHaveDifferentConstraintToBeChangedAndStaticConstraints_ThenExpectedNoChangesOnTicketOccurs)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/DynamicForceSets.json";
    setupComponent(); 
    givenJobTicketIntent(jobIntent_);

    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();
    // ContentType didn't change
    // `backgroundColorRemoval` on the ticket is true

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Check Results
    bool settingUpdated = false;
    dune::copy::Jobs::Copy::Map2CheckerCdmTableProperty::executeMapFunction("pipelineOptions/imageModifications/backgroundColorRemoval", 
        serializedJobTicketTable, settingUpdated);
    EXPECT_EQ(settingUpdated, false); // no changes
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithDesiredForceSetsNonEmptyAndListHaveSameConstraintToBeChanged_ThenExpectedForChangesOnTicketOccurs)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/DynamicForceSets.json";
    setupComponent();

    givenJobTicketIntent(jobIntent_);

    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();
    EXPECT_FALSE(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.isSet(
        dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH)); // just in case; we aren't changing `backgroundColorRemoval`
    serializedJobTicketTable->src.getMutable()->scan.getMutable()->contentType.getMutable() = dune::cdm::jobTicket_1::ContentType::image; // we're changing to image
    // `backgroundColorRemoval` on the ticket is true, and wasn't changed
    
    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Check Results
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.get(), 
        dune::cdm::glossary_1::FeatureEnabled::false_);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithDesiredForceSetsNonEmptyAndListHaveSameConstraintToBeChangedAndStaticConstraints_ThenExpectedForChangesOnTicketOccurs)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/DynamicForceSets.json";
    setupComponent();

    givenJobTicketIntent(jobIntent_);

    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();
    EXPECT_FALSE(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.isSet(
        dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH)); // just in case; we aren't changing `backgroundColorRemoval`
    serializedJobTicketTable->src.getMutable()->scan.getMutable()->contentType.getMutable() = dune::cdm::jobTicket_1::ContentType::image; // we're changing to image
    // `backgroundColorRemoval` on the ticket is true, and wasn't changed
    
    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Check Results
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.get(), 
        dune::cdm::glossary_1::FeatureEnabled::false_);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithDesiredForceSetsNonEmptyAndListHaveSameConstraintCandidateToBeChanged_ThenExpectedNoChangesOnTicket)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/DynamicForceSets.json";
    setupComponent();

    givenJobTicketIntent(jobIntent_);
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemoval()).WillRepeatedly(Return(false)); // we have `backgroundColorRemoval` disabled
    
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->backgroundColorRemoval = 
        dune::cdm::glossary_1::FeatureEnabled::true_; // we're changing the `backgroundColorRemoval`
    // ContentType didn't change

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Check Results
    EXPECT_TRUE(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.isSet(
        dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH));
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.get(), 
        dune::cdm::glossary_1::FeatureEnabled::true_);
}

TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyWithValuesOnJobTicketWithDesiredForceSetsNonEmptyAndListHaveSameConstraintCandidateToBeChangedAndStaticConstraints_ThenExpectedNoChangesOnTicket)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/DynamicForceSets.json";
    setupComponent();

    givenJobTicketIntent(jobIntent_);
    EXPECT_CALL(*jobIntent_, getBackgroundColorRemoval()).WillRepeatedly(Return(false)); // we have `backgroundColorRemoval` disabled
    
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->backgroundColorRemoval = 
        dune::cdm::glossary_1::FeatureEnabled::true_; // we're changing the `backgroundColorRemoval`
    // ContentType didn't change

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Check Results
    EXPECT_TRUE(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.isSet(
        dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH));
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->backgroundColorRemoval.get(), 
        dune::cdm::glossary_1::FeatureEnabled::true_);
}

// Value in Output Canvas Custom Width, when is in intent, is expected that is in a proper accepted value, so check and apply force set wont be checked
TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyForceSetsAndCustomWidthIsModifiedInCurrentIntent_ThenExpectedNoChangesOnTicket)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/UnitNotCompatibleConstraint.json";
    setupComponent();

    givenJobTicketIntent(jobIntent_);
    outputCanvasTable_->outputCanvasXExtent = 10;
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Check Results
    EXPECT_FALSE(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.isSet(
        dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH));
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get(), 0);
}

// Value in Output Canvas Custom Width, when is in intent, is expected that is in a proper accepted value, so check and apply force set wont be checked
TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyForceSetsAndCustomWidthIsModifiedInCurrentIntentAndStaticConstraints_ThenExpectedNoChangesOnTicket)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/UnitNotCompatibleConstraint.json";
    setupComponent();

    givenJobTicketIntent(jobIntent_);
    outputCanvasTable_->outputCanvasXExtent = 10;
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Check Results
    EXPECT_FALSE(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.isSet(
        dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH));
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get(), 0);
}

// Value in Output Canvas Custom Length, when is in intent, is expected that is in a proper accepted value, so check and apply force set wont be checked
TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyForceSetsAndCustomLengthIsModifiedInCurrentIntent_ThenExpectedNoChangesOnTicket)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/UnitNotCompatibleConstraint.json";
    setupComponent();

    givenJobTicketIntent(jobIntent_);
    outputCanvasTable_->outputCanvasYExtent = 10;
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Check Results
    EXPECT_FALSE(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomLength.isSet(
        dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH));
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomLength.get(), 0);
}

// Value in Output Canvas Custom Length, when is in intent, is expected that is in a proper accepted value, so check and apply force set wont be checked
TEST_F(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket,
    WhenCallToForApplyForceSetsAndCustomLengthIsModifiedInCurrentIntentAndStaticConstraints_ThenExpectedNoChangesOnTicket)
{
    // Setup job ticket & job base update
    jsonToLoad_ = "./testResources/UnitNotCompatibleConstraint.json";
    setupComponent();

    givenJobTicketIntent(jobIntent_);
    outputCanvasTable_->outputCanvasYExtent = 10;
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenEmptyJobTicketTable();

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Check Results
    EXPECT_FALSE(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomLength.isSet(
        dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH));
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomLength.get(), 0);
}

template<typename NumberType>
class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized : 
    public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket
    , public ::testing::WithParamInterface< std::tuple<NumberType, NumberType, NumberType, NumberType, NumberType>>
{
public:
    void SetUp() override;
    NumberType currentValue_ = 0;
    NumberType expectedValue_ = 0;
    std::string constraintName_ = "";
};

template <typename NumberType>
void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized<NumberType>::SetUp() 
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicket::SetUp();

    currentValue_ = std::get<0>(::testing::WithParamInterface< std::tuple<NumberType, NumberType, NumberType, NumberType, NumberType>>::GetParam());
    NumberType minValue = std::get<1>(::testing::WithParamInterface< std::tuple<NumberType, NumberType, NumberType, NumberType, NumberType>>::GetParam());
    NumberType maxValue = std::get<2>(::testing::WithParamInterface< std::tuple<NumberType, NumberType, NumberType, NumberType, NumberType>>::GetParam());
    NumberType stepValue = std::get<3>(::testing::WithParamInterface< std::tuple<NumberType, NumberType, NumberType, NumberType, NumberType>>::GetParam());    
    expectedValue_ = std::get<4>(::testing::WithParamInterface< std::tuple<NumberType, NumberType, NumberType, NumberType, NumberType>>::GetParam());

    ASSERT_NE(constraintName_, "");
    auto tempConstraint = createConstraintRange(minValue, maxValue, stepValue);
    allConstraints_ = std::make_shared<ConstraintsGroup>();
    allConstraints_->set(constraintName_, tempConstraint); 
}

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeIntParametrized :
    public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized<int> 
{
public:
    void SetUp() override;
};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeIntParametrized::SetUp()
{
    constraintName_ = "src/scan/xOffset";
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized<int>::SetUp();
}

TEST_P(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeIntParametrized, 
    WhenCallToCheckAndApplyForceSetsConstraintsAndIntentValueExpectation_ThenJobTicketValueIsAsExpected)
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized<int>::setupComponent();
    // Setup job base update
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenJobTicketTable();
    // Setup intent base to use to serialization of info tables
    auto intent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    givenJobTicketIntent(intent);
    EXPECT_CALL(*intent, getXOffset()).WillRepeatedly(Return(currentValue_));

    // src
    // src.scan
    //serializedJobTicketTable->src.get()->scan = *(serializeScanInfoTable(intent));
    serializedJobTicketTable->src.getMutable()->scan = *(dune::scan::Jobs::Scan::serializeScanInfoTable(intent));
    ASSERT_EQ(serializedJobTicketTable->src.get()->scan.get()->xOffset.get(), currentValue_);

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Expected check
    EXPECT_EQ(serializedJobTicketTable->src.get()->scan.get()->xOffset.get(), expectedValue_);
}

TEST_P(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeIntParametrized, 
    WhenCallToCheckAndApplyForceSetsConstraintsAndIntentValueExpectationAndStaticConstraints_ThenJobTicketValueIsAsExpected)
{
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized<int>::setupComponent();
    // Setup job base update
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenJobTicketTable();
    // Setup intent base to use to serialization of info tables
    auto intent = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    givenJobTicketIntent(intent);
    EXPECT_CALL(*intent, getXOffset()).WillRepeatedly(Return(currentValue_));

    // src
    // src.scan
    //serializedJobTicketTable->src.get()->scan = *(serializeScanInfoTable(intent));
    serializedJobTicketTable->src.getMutable()->scan = *(dune::scan::Jobs::Scan::serializeScanInfoTable(intent));
    ASSERT_EQ(serializedJobTicketTable->src.get()->scan.get()->xOffset.get(), currentValue_);

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Expected check
    EXPECT_EQ(serializedJobTicketTable->src.get()->scan.get()->xOffset.get(), expectedValue_);
}

INSTANTIATE_TEST_CASE_P(, GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeIntParametrized, ::testing::Values
(
                    // CurrentValue -   MinValue -  MaxValue -  StepValue - ExpectedValue
    std::make_tuple(0,                  0,          100,        1,          0),     // Min value accepted
    std::make_tuple(100,                0,          100,        1,          100),   // Max Value accepted
    std::make_tuple(50,                 0,          100,        1,          50),    // Intermediate value accepted
    std::make_tuple(51,                 0,          100,        2,          50),    // Intermediate value not accepted FAIL
    std::make_tuple(-1,                 0,          100,        1,          0),     // Value out of min bound FAIL
    std::make_tuple(101,                0,          100,        1,          100),   // value ouf of max bound FAIL
    std::make_tuple(51,                 0,          100,        0,          51)     // value with zero step so accepted value
));

class GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeDoubleParametrized :
    public GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized<double> 
{
public:
    void SetUp() override;
};

void GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeDoubleParametrized::SetUp()
{
    constraintName_ = "pipelineOptions/imageModifications/outputCanvasCustomWidth";
    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized<double>::SetUp();
}

TEST_P(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeDoubleParametrized, 
    WhenCallToCheckAndApplyForceSetsConstraintsAndIntentValueExpectation_ThenJobTicketValueIsAsExpected)
{

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized<double>::setupComponent();
    // Setup job base update
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenJobTicketTable();

    //pipelineOptions.imageModifications
    auto imageTable = std::make_unique<dune::cdm::jobTicket_1::ImageModificationsTable>();    
    imageTable->outputCanvasCustomWidth = currentValue_;
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications = *imageTable;
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications.beginMergePatch();
    ASSERT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get(), currentValue_);

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_);

    // Expected check
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get(), expectedValue_);
}

TEST_P(GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeDoubleParametrized, 
    WhenCallToCheckAndApplyForceSetsConstraintsAndIntentValueExpectationAndStaticConstraints_ThenJobTicketValueIsAsExpected)
{

    GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeParametrized<double>::setupComponent();
    // Setup job base update
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> serializedJobTicketTable = givenJobTicketTable();

    //pipelineOptions.imageModifications
    auto imageTable = std::make_unique<dune::cdm::jobTicket_1::ImageModificationsTable>();    
    imageTable->outputCanvasCustomWidth = currentValue_;
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications = *imageTable;
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications.beginMergePatch();
    ASSERT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get(), currentValue_);

    // Execute test
    component_->checkAndApplyForceSets(serializedJobTicketTable,mockICopyJobTicket_,allConstraints_,allConstraints_);

    // Expected check
    EXPECT_EQ(serializedJobTicketTable->pipelineOptions.get()->imageModifications.get()->outputCanvasCustomWidth.get(), expectedValue_);
}


INSTANTIATE_TEST_CASE_P(, GivenAConnectedCopyJobDynamicConstraintRulesLargeFormatWithUpdateJobTicketConstraintRangeDoubleParametrized, ::testing::Values
(
                    // CurrentValue -   MinValue -  MaxValue -  StepValue - ExpectedValue
    std::make_tuple(0.0,                0.0,        1.0,        0.1,        0),     // Min value accepted
    std::make_tuple(1.0,                0.0,        1.0,        0.1,        1.0),   // Max Value accepted
    std::make_tuple(0.5,                0.0,        1.0,        0.1,        0.5),   // Intermediate value accepted
    std::make_tuple(0.51,               0.0,        1.0,        0.1,        0.5),   // Intermediate value not accepted FAIL
    std::make_tuple(-1.0,               0.0,        1.0,        0.1,        0),     // Value out of min bound 
    std::make_tuple(1.1,                0.0,        1.0,        0.1,        1.0),   // value ouf of max bound FAIL
    std::make_tuple(0.51,               0.0,        1.0,        0,          0.51)   // value with zero step so accepted value
));