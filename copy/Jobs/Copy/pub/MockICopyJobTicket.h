#pragma once

#include <gmock/gmock.h>

#include "CopyJobTicket_generated.h"
#include "ICopyJobConstraints.h"
#include "ICopyJobTicket.h"
#include "IJobTicket.h"
#include "ISerializable.h"
#include "JobFrameworkTypes.h"
#include "MockIJobTicket.h"
#include "ITicketAdapter.h"
#include "IColorAccessControl.h"

using namespace dune::job;

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class MockICopyJobTicket : public ICopyJobTicket
{
  public:
    using FbT = CopyJobTicketFbT;
    using Constraints = ICopyJobConstraints;

    MockICopyJobTicket() {}

    MOCK_CONST_METHOD0(getJobInFinalStage, bool());
    MOCK_METHOD1(setJobInFinalStage, void(const bool jobInFinalStage));
    MOCK_CONST_METHOD0(getApplicationName, const std::string&());
    MOCK_METHOD1(setApplicationName, void(const std::string& applicationName));
    MOCK_CONST_METHOD0(getApplicationFileName, const std::string&());
    MOCK_METHOD1(setApplicationFileName, void(const std::string& applicationFileName));
    MOCK_CONST_METHOD0(getApplicationJobUUID, const std::string&());
    MOCK_METHOD1(setApplicationJobUUID, void(const std::string& applicationJobUUID));
    MOCK_CONST_METHOD0(getIntent, std::shared_ptr<ICopyJobIntent>());
    MOCK_METHOD1(setIntent, void(std::shared_ptr<ICopyJobIntent> intent));
    MOCK_CONST_METHOD0(getResult, std::shared_ptr<ICopyJobResult>());
    MOCK_METHOD1(setResult, void(const std::shared_ptr<ICopyJobResult>& result));
    MOCK_CONST_METHOD0(getIntentsManager, dune::job::IIntentsManager*());
    MOCK_METHOD1(setIntentsManager, void(dune::job::IIntentsManager* intentsManager));
    MOCK_METHOD0(getPageIntent, dune::job::IIntentsManager::PageIntent&());
    MOCK_METHOD1(setPageIntent, void(dune::job::IIntentsManager::PageIntent));
    MOCK_CONST_METHOD0(getConstraints, std::shared_ptr<Constraints>());
    MOCK_METHOD1(setConstraints, void(std::shared_ptr<Constraints> constraints));
    MOCK_CONST_METHOD0(getJobId, Uuid());
    MOCK_METHOD1(setJobId, void(const Uuid& jobId));
    MOCK_CONST_METHOD0(isFirstScanStarted, bool());
    MOCK_METHOD1(setFirstScanStarted, void(bool firstScanStarted));
    MOCK_CONST_METHOD0(getPreviewMode, bool());
    MOCK_METHOD1(setPreviewMode, void(bool preview));
    MOCK_CONST_METHOD0(getOrdinal, uint32_t());
    MOCK_METHOD1(setOrdinal, void(uint32_t ordinal));
    MOCK_CONST_METHOD0(getState, dune::job::JobStateType());
    MOCK_METHOD1(setState, void(const dune::job::JobStateType& state));
    MOCK_CONST_METHOD0(getPriority, dune::job::JobPriorityType());
    MOCK_METHOD1(setPriority, void(const dune::job::JobPriorityType& priority));
    MOCK_CONST_METHOD0(getCompletionState, dune::job::CompletionStateType());
    MOCK_METHOD1(setCompletionState, void(const dune::job::CompletionStateType& completionState));
    MOCK_CONST_METHOD0(getStorePath, const std::string&());
    MOCK_METHOD1(setStorePath, void(const std::string& storePath));
    MOCK_CONST_METHOD0(getJobName, const std::string&());
    MOCK_METHOD1(setJobName, void(const std::string& jobName));
    MOCK_METHOD1(getCopyPageTicket, std::shared_ptr<ICopyPageTicket>(const dune::framework::core::Uuid& pageId));
    MOCK_METHOD0(getPageChangedEvent, dune::job::JobTicketPageEvent&());
    MOCK_METHOD1(addPage, std::shared_ptr<dune::job::IPageTicket>(const dune::framework::core::Uuid& pageId));
    MOCK_METHOD2(addPage, std::shared_ptr<dune::job::IPageTicket>(
                              const dune::framework::core::Uuid&                   pageId,
                              std::shared_ptr<dune::imaging::types::PageMetaInfoT> pageMetaInfo));
    MOCK_METHOD1(removePage, void(const dune::framework::core::Uuid& pageId));
    MOCK_METHOD1(getPage, std::shared_ptr<dune::job::IPageTicket>(const dune::framework::core::Uuid& pageId));
    MOCK_CONST_METHOD1(getPagesIds, std::vector<dune::framework::core::Uuid>(PageOrder orderBy));

    MOCK_CONST_METHOD0(getNvramInterface, dune::framework::storage::INvram*());
    MOCK_METHOD1(setNvramInterface, void(dune::framework::storage::INvram* nvramInterface));

    MOCK_CONST_METHOD0(getLocalizationInterface, dune::localization::ILocaleProvider*());
    MOCK_METHOD1(setLocalizationInterface, void(dune::localization::ILocaleProvider* locale));

    MOCK_CONST_METHOD0(getMediaInterface, dune::print::engine::IMedia*());
    MOCK_METHOD1(setMediaInterface, void(dune::print::engine::IMedia* mediaInterface));

    MOCK_CONST_METHOD0(getColorAccessControlInterface, dune::imaging::IColorAccessControl*());
    MOCK_METHOD1(setColorAccessControlInterface, void(dune::imaging::IColorAccessControl* colorAccessControl));

    MOCK_CONST_METHOD0(getMediaInfoInterface, dune::print::engine::IMediaInfo*());
    MOCK_METHOD1(setMediaInfoInterface, void(dune::print::engine::IMediaInfo* mediaInfoInterface));

    MOCK_CONST_METHOD0(getAllSupportedMediaSizes,
                       std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>>());
    MOCK_CONST_METHOD1(getSupportedMediaSizes, std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>>(
                                                   dune::imaging::types::MediaSource mediaSource));
    MOCK_CONST_METHOD1(updateSupportedPageBasedFinisherValidMediaSizes, void(
                                                   std::vector<dune::cdm::glossary_1::MediaSize>& validMediaSizesList));
    MOCK_CONST_METHOD0(getPageBasedFinisherValidMediaSizes,
                          std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaSize>>());
    MOCK_CONST_METHOD0(getAllSupportedMediaTypes,
                       std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>());
    MOCK_CONST_METHOD0(getEnabledMediaTypes, std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>());
    MOCK_CONST_METHOD0(isMediaTypeVisibilityTogglingSupported, bool());
    MOCK_METHOD1(setisMediaTypeVisibilityTogglingSupported, void(bool isMediaTypeVisibilityTogglingSupported));
    MOCK_CONST_METHOD1(getSupportedMediaTypes, std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>>(
                                                   dune::imaging::types::MediaSource mediaSource));
    MOCK_CONST_METHOD0(getPageBasedFinisherValidMediaTypes,
                          std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaType>>());
    MOCK_CONST_METHOD0(getPageBasedFinisherValidContentOrientation, 
                          std::tuple<bool, std::vector<dune::cdm::glossary_1::ContentOrientation>>());
    MOCK_CONST_METHOD0(getAllSupportedMediaSources,
                       std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>>());
    MOCK_CONST_METHOD0(getOutputList,
                       std::tuple<APIResult, std::vector<dune::imaging::types::MediaDestinationId>>());

    MOCK_CONST_METHOD1(getMediaSizeFromMediaSource, dune::imaging::types::MediaSizeId(
                                                    dune::imaging::types::MediaSource source));
    MOCK_CONST_METHOD0(getScanMediaInterface, dune::scan::scanningsystem::IMedia*());

    MOCK_CONST_METHOD0(IsInstalledPageBasedFinisherDevice, bool());
    MOCK_CONST_METHOD1(IsInstalledSpecificPageBasedFinisherDevice, bool(dune::imaging::types::MediaProcessingTypes mediaProcssingType)); 
    MOCK_CONST_METHOD0(UpdateMediaOutputDestinationPageBasedFinisherInstalled, bool());
    MOCK_CONST_METHOD1(getConstraintsMsgBetweenFinisherOption, std::string(dune::imaging::types::MediaProcessingTypes mediaProcssingType)); 

    MOCK_CONST_METHOD3(getOutputMediaSizeIdTypeforFinisher, void(dune::imaging::types::MediaSizeId& OutputMediaSizeId,
                                                             dune::imaging::types::MediaOrientation& OutputMediaOrientation, bool &isPossibleBothOrientation));
    MOCK_CONST_METHOD1(getStapleString, std::string(dune::imaging::types::StapleOptions stapleOption));
    MOCK_CONST_METHOD1(getHolePunchString, std::string(dune::imaging::types::PunchingOptions punchOption));
    MOCK_CONST_METHOD1(getFinisherConstraintString, std::string(std::string constraintString));

    MOCK_CONST_METHOD0(getPossibleOutputBins, std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>>());
    MOCK_CONST_METHOD0(getValidOutputBins, std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>>());

    MOCK_CONST_METHOD1(getStapleConstraintsString,  std::string(std::vector<dune::imaging::types::StapleOptions> validOptionsFromHelper));
    MOCK_CONST_METHOD1(getHolePunchConstraintsString,  std::string(std::vector<dune::imaging::types::PunchingOptions> validOptionsFromHelper));

    MOCK_CONST_METHOD1(isValidStaplingOptionForCopy, bool(dune::cdm::jobTicket_1::StapleOptions stapleOption));
    MOCK_CONST_METHOD0(getPossibleStaplingOptions, std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>>());
    MOCK_CONST_METHOD1(getValidStaplingOptions, std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>>(std::string &constraintsmsg));

    MOCK_CONST_METHOD1(isValidPunchingOptionForCopy, bool(dune::cdm::jobTicket_1::PunchOptions punchOption));
    MOCK_CONST_METHOD0(getPossiblePunchingOptions, std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>>());
    MOCK_CONST_METHOD1(getValidPunchingOptions, std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>>(std::string &constraintsmsg));
   
    MOCK_CONST_METHOD0(getPossibleFoldingOptions, std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>>());
    MOCK_CONST_METHOD1(getValidFoldingOptions, std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>>(std::string &constraintsmsg));

    MOCK_CONST_METHOD2(getPagesPerSetLimitForFinishingOption, std::tuple<int, int>(dune::imaging::types::FoldingOptions foldingOption, dune::imaging::types::BookletMakingOptions bookletMakingOption));

    MOCK_CONST_METHOD0(getPossibleBookletMakingOptions, std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>>());
    MOCK_CONST_METHOD1(getValidBookletMakingOptions, std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>>(std::string &constraintsmsg));

    MOCK_METHOD1(setScanMediaInterface, void(dune::scan::scanningsystem::IMedia* scanMediaInterface));
    MOCK_CONST_METHOD0(getScanCapabilitiesInterface, dune::scan::scanningsystem::IScannerCapabilities*());
    MOCK_METHOD1(setScanCapabilitiesInterface,
                 void(dune::scan::scanningsystem::IScannerCapabilities* scanMediaInterface));
    MOCK_CONST_METHOD0(clone, std::shared_ptr<ICopyJobTicket>());
    MOCK_METHOD0(getHandler, std::shared_ptr<dune::job::IJobTicketHandler>());
    MOCK_METHOD1(setPrintIntentsFactory, void(dune::print::engine::IPrintIntentsFactory* printIntentsFactory));;

    MOCK_METHOD1(setJobInFinalStageOverride, void(const bool jobInFinalStageOverride));
    MOCK_CONST_METHOD0(getJobInFinalStageOverride, bool());

    MOCK_CONST_METHOD0(getTicketId, Uuid());
    MOCK_METHOD1(setTicketId, void(const Uuid& id));
    MOCK_CONST_METHOD0(getProcessingDetailedState, ProcessingDetailedState());
    MOCK_METHOD1(setProcessingDetailedState, void(const ProcessingDetailedState& processingDetailedState));
    MOCK_CONST_METHOD0(serialize, SerializedDataBufferPtr());
    MOCK_METHOD1(deserialize, bool(const SerializedDataBufferPtr&));
    MOCK_CONST_METHOD0(serializeBase, std::unique_ptr<JobTicketFbT>());
    MOCK_METHOD1(deserializeBase, void(const std::unique_ptr<JobTicketFbT>&));
    MOCK_CONST_METHOD0(getType, JobType());
    MOCK_METHOD1(setType, void(const JobType& type));
    MOCK_CONST_METHOD0(getExecutionMode, dune::job::ExecutionMode());
    MOCK_METHOD1(setExecutionMode, void(const dune::job::ExecutionMode& mode));
    MOCK_CONST_METHOD0(getSegmentType, dune::job::SegmentType());
    MOCK_METHOD1(setSegmentType, void(const dune::job::SegmentType& segmentType));
    MOCK_CONST_METHOD0(getJobDelayedDuringExecution, bool());
    MOCK_METHOD1(setJobDelayedDuringExecution, void(const bool& jobDelayedDuringExecution));
    MOCK_CONST_METHOD0(getParentJobId, Uuid());
    MOCK_METHOD1(setParentJobId, void(const Uuid& parentJobId));
    MOCK_CONST_METHOD0(getUserName, const std::string());
    MOCK_CONST_METHOD0(getJobServiceId, JobServiceId());
    MOCK_METHOD1(setJobServiceId, void(const JobServiceId& jobServiceId));
    MOCK_CONST_METHOD0(getStartTime, time_t());
    MOCK_METHOD1(setStartTime, void(const time_t& startTime));
    MOCK_CONST_METHOD0(getCompletionTime, time_t());
    MOCK_METHOD1(setCompletionTime, void(const time_t& completionTime));
    MOCK_CONST_METHOD0(getScheduledTime, time_t());
    MOCK_METHOD1(setScheduledTime, void(const time_t& scheduledTime));
    MOCK_CONST_METHOD0(getHpTimeOffset, time_t());
    MOCK_METHOD1(setHpTimeOffset, void(const time_t& hpTimeOffset));
    MOCK_CONST_METHOD0(isHeldJob, bool());
    MOCK_CONST_METHOD0(getHeldTime, time_t());
    MOCK_METHOD1(setHeldTime, void(const time_t& heldTime));
    MOCK_CONST_METHOD0(getStoreJobDetails, std::shared_ptr<IStoreJobDetails>());
    MOCK_METHOD1(setStoreJobDetails, void(const std::shared_ptr<IStoreJobDetails>& storeJobDetails));
    MOCK_CONST_METHOD0(getCompletionCode, EventInternalCode());
    MOCK_METHOD1(setCompletionCode, void(EventInternalCode completionCode));
    MOCK_CONST_METHOD0(getSourceJobStorePath, const std::string&());
    MOCK_METHOD1(setSourceJobStorePath, void(const std::string& sourceJobStorePath));
    MOCK_CONST_METHOD0(getPersistentPipePath, const std::string&());
    MOCK_METHOD1(setPersistentPipePath, void(const std::string&));
    MOCK_CONST_METHOD0(isVisible, bool());
    MOCK_METHOD1(setVisible, void(bool isVisible));
    MOCK_CONST_METHOD0(isJobPromotable, bool());
    MOCK_METHOD1(setJobPromotable, void(bool isJobPromotable));
    MOCK_CONST_METHOD0(getPromoteOptions, dune::job::PromoteOptions());
    MOCK_METHOD1(setPromoteOptions, void(const dune::job::PromoteOptions promoteOptions));
    MOCK_CONST_METHOD0(isRestrictedJob, bool());
    MOCK_METHOD1(setRestrictedJob, void(bool isRestrictedJob));
    MOCK_CONST_METHOD0(isJobReprintable, bool());
    MOCK_METHOD1(setJobReprintable, void(bool isJobReprintable));
    MOCK_CONST_METHOD0(isJobResourcePaused, bool());
    MOCK_METHOD1(setJobResourcePaused, void(bool isJobResourcePaused));
    MOCK_CONST_METHOD0(getPauseReason, JobPauseReason());
    MOCK_METHOD1(setPauseReason, void(const JobPauseReason& pauseReason));
    MOCK_CONST_METHOD0(getJobNotificationDetails, std::shared_ptr<IJobNotificationDetails>());
    MOCK_METHOD1(setJobNotificationDetails,
                 void(const std::shared_ptr<IJobNotificationDetails>& jobNotificationDetails));
    MOCK_CONST_METHOD0(getSecurityContext, std::shared_ptr<dune::security::ac::ISecurityContext>());
    MOCK_METHOD1(setSecurityContext,
                 void(const std::shared_ptr<dune::security::ac::ISecurityContext>& securityContext));
    MOCK_CONST_METHOD0(getSortOrder, int32_t());
    MOCK_METHOD1(setSortOrder, void(const int32_t& sortOrder));

    MOCK_METHOD1(setCleanupHandler, void(std::shared_ptr<IJobTicket::CleanupHandler> cleanupHandler));
    MOCK_METHOD0(getJobTicketChanged, JobTicketEvent&());

    MOCK_CONST_METHOD0(getDataSource, DataSource());
    MOCK_METHOD1(setDataSource, void(const DataSource& dataSource));
    MOCK_METHOD0(populateDefaultConstraints, void());

    MOCK_CONST_METHOD0(getStoreJobPassword, const std::string&());
    MOCK_METHOD1(setStoreJobPassword, void(const std::string& password));

    MOCK_CONST_METHOD0(getHostName, const std::string&());
    MOCK_METHOD1(setHostName, void(const std::string& hostName));
    MOCK_CONST_METHOD0(getResumeMode, dune::job::JobResumeMode());
    MOCK_METHOD1(setResumeMode, void(const dune::job::JobResumeMode resumeMode));
    MOCK_CONST_METHOD0(getJobCategory, dune::job::JobCategory());
    MOCK_METHOD1(setJobCategory, void(const dune::job::JobCategory& jobCategory));

    MOCK_CONST_METHOD0(getPriorityModeSessionId, dune::framework::core::Uuid());
    MOCK_METHOD1(setPriorityModeSessionId, void(const dune::framework::core::Uuid& token));

    MOCK_METHOD1(setHoldDetailedMessageHelper, void(const std::shared_ptr<IHoldDetailedMessageHelper>& holdDetailedMessageHelper));
    MOCK_CONST_METHOD0(getHoldDetailedMessageHelper, std::shared_ptr<IHoldDetailedMessageHelper>());

    MOCK_CONST_METHOD0(isPreScanJob, bool());
    MOCK_METHOD1(setPreScanJob, void(bool value));

    MOCK_CONST_METHOD0(isPrintAlignmentChangeRequired, bool());
    MOCK_METHOD1(setPrintAlignmentChangeRequired, void(bool value));

    MOCK_CONST_METHOD0(getDefaultMediaSize, dune::imaging::types::MediaSizeId());
    MOCK_METHOD1(setDefaultMediaSize, void(dune::imaging::types::MediaSizeId value));
    MOCK_METHOD1(setPrescannedWidth, void(uint32_t value));
    MOCK_CONST_METHOD0(getPrescannedWidth, uint32_t());
    MOCK_METHOD1(setPrescannedHeight, void(uint32_t value));
    MOCK_CONST_METHOD0(getPrescannedHeight, uint32_t());
    MOCK_METHOD1(setMaxLengthConfig, void(dune::copy::Jobs::Copy::MaxLengthConfig value));
    MOCK_CONST_METHOD0(getMaxLengthConfig, dune::copy::Jobs::Copy::MaxLengthConfig());
    MOCK_METHOD1(setPrePrintConfiguration, void(dune::copy::Jobs::Copy::Product value));
    MOCK_CONST_METHOD0(getPrePrintConfiguration, dune::copy::Jobs::Copy::Product());
    MOCK_CONST_METHOD0(getPageCount, uint32_t());
    MOCK_CONST_METHOD0(getJobCompleting, bool());
    MOCK_METHOD1(setJobCompleting, void(bool value));

    MOCK_CONST_METHOD0(getSolutionId, dune::framework::core::Uuid());
    MOCK_METHOD1(setSolutionId, void(const dune::framework::core::Uuid& solutionId));
    MOCK_CONST_METHOD0(getSolutionContext, const std::string&());
    MOCK_METHOD1(setSolutionContext, void(const std::string& context));
    MOCK_CONST_METHOD0(getAccountId, std::string());
    MOCK_CONST_METHOD0(areNativeJobStatusAlertsEnabled, bool());
    MOCK_METHOD1(setNativeJobStatusAlertsStatus, void(const bool status));
    MOCK_METHOD1(setJobSuppressed, void(const bool jobSuppressed));
    MOCK_CONST_METHOD0(isJobSuppressed, bool());
    MOCK_CONST_METHOD0(getSourceIpAddress, const std::string&());
    MOCK_METHOD1(setSourceIpAddress, void(const std::string& hostName));
    MOCK_CONST_METHOD0(getPipeListOperations, std::shared_ptr<dune::job::IPipeListOperations>());
    MOCK_METHOD1(setPipeListOperations, void(std::shared_ptr<dune::job::IPipeListOperations> pipeListOperations));

    MOCK_METHOD1(setVersion, void(uint value));
    MOCK_CONST_METHOD0(getVersion, uint());
    MOCK_CONST_METHOD0(shouldBeBorderless, bool());
    MOCK_METHOD1(setScanCalibrationType, void(dune::imaging::types::ScanCalibrationType calibrationType));
    MOCK_CONST_METHOD0(getScanCalibrationType, dune::imaging::types::ScanCalibrationType());
    MOCK_CONST_METHOD0(getMaxCollatePages, uint32_t());
    MOCK_METHOD1(setMaxCollatePages, void(uint32_t value));
    MOCK_METHOD1(writeSettingsToFile, dune::framework::data::backup::OperationResult(std::string filePath));
    MOCK_METHOD1(readSettingsFromFile, dune::framework::data::backup::OperationResult (const std::string& filePath));
    MOCK_CONST_METHOD0(isEarlyCopyJob, bool());
    MOCK_METHOD1(setEarlyCopyJob, void(bool value));
    MOCK_METHOD0(isRestrictColorPrint, bool());
    MOCK_METHOD1(setRestrictColorPrint, void(bool isColorRestricted));

    MOCK_CONST_METHOD0(getAllPromptsCompleted, bool());
    MOCK_METHOD1(setAllPromptsCompleted, void(const bool allPromptsCompleted));
    MOCK_METHOD0(getAllPromptsCompletedEvent, JobTicketPromptCompletedEvent&());
    MOCK_CONST_METHOD0(getIntentsValidated, bool());
    MOCK_METHOD1(setIntentsValidated, void(const bool intentsValidated));
    MOCK_METHOD0(getIntentsValidatedEvent, JobTicketIntentsValidatedEvent&());
    MOCK_CONST_METHOD0(getInputPipeMetaInfo, std::shared_ptr<dune::job::IPipeMetaInfo>());
    MOCK_METHOD1(setInputPipeMetaInfo, void(const std::shared_ptr<dune::job::IPipeMetaInfo>& inputPipeMetaInfo));
    MOCK_CONST_METHOD0(getOutputPipeMetaInfo, std::shared_ptr<dune::job::IPipeMetaInfo>());
    MOCK_METHOD1(setOutputPipeMetaInfo, void(const std::shared_ptr<dune::job::IPipeMetaInfo>& outputPipeMetaInfo));
    MOCK_CONST_METHOD0(getInputPipePath, const std::string&());
    MOCK_METHOD1(setInputPipePath, void(const std::string& inputPipePath));
    MOCK_CONST_METHOD0(getOutputPipePath, const std::string&());
    MOCK_METHOD1(setOutputPipePath, void(const std::string& outputPipePath));

    MOCK_CONST_METHOD0(getFlatbedDuplexScanSide,  dune::scan::types::DuplexSideEnum());
    MOCK_METHOD1(setFlatbedDuplexScanSide, void(const dune::scan::types::DuplexSideEnum flatbedDuplexScanSide));

};

using namespace dune::framework::data::constraints;

class MockCopyTicketAdapter : public ITicketAdapter
{
    MOCK_CONST_METHOD0(getConstraints, const dune::framework::data::constraints::ConstraintsGroup&());
};

class MockICopyJobIntent : public ICopyJobIntent
{
  public:
    MockICopyJobIntent() {}
    MOCK_CONST_METHOD0(getOutputMediaSizeId, dune::imaging::types::MediaSizeId());
    MOCK_METHOD1(setOutputMediaSizeId, void(dune::imaging::types::MediaSizeId value));
    MOCK_CONST_METHOD0(getOutputMediaOrientation, dune::imaging::types::MediaOrientation());
    MOCK_METHOD1(setOutputMediaOrientation, void(dune::imaging::types::MediaOrientation value));
    MOCK_CONST_METHOD0(getOutputMediaIdType, dune::imaging::types::MediaIdType());
    MOCK_METHOD1(setOutputMediaIdType, void(dune::imaging::types::MediaIdType value));
    MOCK_CONST_METHOD0(getOutputMediaSource, dune::imaging::types::MediaSource());
    MOCK_METHOD1(setOutputMediaSource, void(dune::imaging::types::MediaSource value));
    MOCK_CONST_METHOD0(getFoldingStyleId, short());
    MOCK_METHOD1(setFoldingStyleId, void(short value));
    MOCK_CONST_METHOD0(getOutputPlexMode, dune::imaging::types::Plex());
    MOCK_METHOD1(setOutputPlexMode, void(dune::imaging::types::Plex value));
    MOCK_CONST_METHOD0(getOutputPlexBinding, dune::imaging::types::PlexBinding());
    MOCK_METHOD1(setOutputPlexBinding, void(dune::imaging::types::PlexBinding value));
    MOCK_CONST_METHOD0(getCopies, int());
    MOCK_METHOD1(setCopies, void(int value));
    MOCK_CONST_METHOD0(getCollate, dune::copy::SheetCollate());
    MOCK_METHOD1(setCollate, void(dune::copy::SheetCollate value));
    MOCK_CONST_METHOD0(getCopyQuality, dune::imaging::types::PrintQuality());
    MOCK_METHOD1(setCopyQuality, void(dune::imaging::types::PrintQuality value));
    MOCK_CONST_METHOD0(getResize, int());
    MOCK_METHOD1(setResize, void(int value));
    MOCK_CONST_METHOD0(getLighterDarker, int());
    MOCK_METHOD1(setLighterDarker, void(int value));

    MOCK_CONST_METHOD0(getInputMediaSizeId, dune::imaging::types::MediaSizeId());
    MOCK_METHOD1(setInputMediaSizeId, void(dune::imaging::types::MediaSizeId value));
    MOCK_CONST_METHOD0(getInputPlexMode, dune::imaging::types::Plex());
    MOCK_METHOD1(setInputPlexMode, void(dune::imaging::types::Plex value));
    MOCK_CONST_METHOD0(getOriginalSidesAuto, bool());
    MOCK_METHOD1(setOriginalSidesAuto, void(bool value));
    MOCK_CONST_METHOD0(getOutputXResolution, dune::imaging::types::Resolution());
    MOCK_METHOD1(setOutputXResolution, void(dune::imaging::types::Resolution outputXResolution));
    MOCK_CONST_METHOD0(getOutputYResolution, dune::imaging::types::Resolution());
    MOCK_METHOD1(setOutputYResolution, void(dune::imaging::types::Resolution outputYResolution));
    MOCK_CONST_METHOD0(getQualityMode, dune::scan::types::AttachmentSize());
    MOCK_METHOD1(setQualityMode, void(dune::scan::types::AttachmentSize value));
    MOCK_CONST_METHOD0(getColorMode, dune::imaging::types::ColorMode());
    MOCK_METHOD1(setColorMode, void(dune::imaging::types::ColorMode value));
    MOCK_CONST_METHOD0(getContentOrientation, dune::imaging::types::ContentOrientation());
    MOCK_METHOD1(setContentOrientation, void(dune::imaging::types::ContentOrientation value));
    MOCK_CONST_METHOD0(getBackSideContentOrientation, dune::imaging::types::ContentOrientation());
    MOCK_METHOD1(setBackSideContentOrientation, void(dune::imaging::types::ContentOrientation value));
    MOCK_CONST_METHOD0(getOriginalContentType, dune::imaging::types::OriginalContentType());
    MOCK_METHOD1(setOriginalContentType, void(dune::imaging::types::OriginalContentType value));
    MOCK_CONST_METHOD0(getOriginalMediaType, dune::scan::types::OriginalMediaType());
    MOCK_METHOD1(setOriginalMediaType, void(dune::scan::types::OriginalMediaType value));
    MOCK_CONST_METHOD0(getScanSource, dune::scan::types::ScanSource());
    MOCK_METHOD1(setScanSource, void(dune::scan::types::ScanSource value));
    MOCK_CONST_METHOD0(getXScalePercent, int64_t());
    MOCK_METHOD1(setXScalePercent, void(int64_t value));
    MOCK_CONST_METHOD0(getYScalePercent, int64_t());
    MOCK_METHOD1(setYScalePercent, void(int64_t value));
    MOCK_CONST_METHOD0(getScaleSelection, dune::scan::types::ScanScaleSelectionEnum());
    MOCK_METHOD1(setScaleSelection, void(dune::scan::types::ScanScaleSelectionEnum value));
    MOCK_CONST_METHOD0(getScaleToFitEnabled, bool());
    MOCK_METHOD1(setScaleToFitEnabled, void(bool value));
    MOCK_CONST_METHOD0(getFitToPageIncludeMargin, bool());
    MOCK_METHOD1(setFitToPageIncludeMargin, void(bool value));
    MOCK_CONST_METHOD0(getGeneratePreview, bool());
    MOCK_METHOD1(setGeneratePreview, void(bool value));
    MOCK_CONST_METHOD0(getAutoDeskew, bool());
    MOCK_METHOD1(setAutoDeskew, void(bool value));
    MOCK_CONST_METHOD0(getScaleToSize, dune::imaging::types::MediaSizeId());
    MOCK_METHOD1(setScaleToSize, void(dune::imaging::types::MediaSizeId value));
    MOCK_CONST_METHOD0(getScaleToOutput, dune::imaging::types::MediaSource());
    MOCK_METHOD1(setScaleToOutput, void(dune::imaging::types::MediaSource value));
    MOCK_CONST_METHOD0(getScanFeedOrientation, dune::scan::types::ScanFeedOrientation());
    MOCK_METHOD1(setScanFeedOrientation, void(dune::scan::types::ScanFeedOrientation value));
    MOCK_CONST_METHOD0(getScanXResolution, dune::imaging::types::Resolution());
    MOCK_METHOD1(setScanXResolution, void(dune::imaging::types::Resolution value));
    MOCK_CONST_METHOD0(getScanYResolution, dune::imaging::types::Resolution());
    MOCK_METHOD1(setScanYResolution, void(dune::imaging::types::Resolution value));
    MOCK_CONST_METHOD0(getMultipickDetection, bool());
    MOCK_METHOD1(setMultipickDetection, void(bool value));
    MOCK_CONST_METHOD0(getJobScanLimit, int());
    MOCK_METHOD1(setJobScanLimit, void(int value));
    MOCK_CONST_METHOD0(getAutoCrop, bool());
    MOCK_METHOD1(setAutoCrop, void(bool value));
    MOCK_CONST_METHOD0(getBlankPageDetection, dune::scan::types::BlankDetectEnum());
    MOCK_METHOD1(setBlankPageDetection, void(dune::scan::types::BlankDetectEnum value));
    MOCK_CONST_METHOD0(getBrightness, uint32_t());
    MOCK_METHOD1(setBrightness, void(uint32_t value));
    MOCK_CONST_METHOD0(getContrast, uint32_t());
    MOCK_METHOD1(setContrast, void(uint32_t value));
    MOCK_CONST_METHOD0(getSharpen, uint32_t());
    MOCK_METHOD1(setSharpen, void(uint32_t value));
    MOCK_CONST_METHOD0(getXOffset, uint32_t());
    MOCK_METHOD1(setXOffset, void(uint32_t value));
    MOCK_CONST_METHOD0(getYOffset, uint32_t());
    MOCK_METHOD1(setYOffset, void(uint32_t value));
    MOCK_CONST_METHOD0(getXExtend, uint32_t());
    MOCK_METHOD1(setXExtend, void(uint32_t value));
    MOCK_CONST_METHOD0(getYExtend, uint32_t());
    MOCK_METHOD1(setYExtend, void(uint32_t value));
    MOCK_CONST_METHOD0(getBackgroundRemoval, uint32_t());
    MOCK_METHOD1(setBackgroundRemoval, void(uint32_t value));
    MOCK_CONST_METHOD0(getBackgroundColorRemoval, bool());
    MOCK_METHOD1(setBackgroundColorRemoval, void(bool value));
    MOCK_CONST_METHOD0(getBackgroundNoiseRemoval, bool());
    MOCK_METHOD1(setBackgroundNoiseRemoval, void(bool value));
    MOCK_CONST_METHOD0(getBackgroundColorRemovalLevel, int32_t());
    MOCK_METHOD1(setBackgroundColorRemovalLevel, void(int32_t value));
    MOCK_CONST_METHOD0(getBlackEnhancementLevel, int32_t());
    MOCK_METHOD1(setBlackEnhancementLevel, void(int32_t value));
    MOCK_CONST_METHOD0(getOverScan, dune::scan::types::OverScanType());
    MOCK_METHOD1(setOverScan, void(dune::scan::types::OverScanType value));
    MOCK_CONST_METHOD0(getScanCaptureMode, dune::scan::types::ScanCaptureModeType());
    MOCK_METHOD1(setScanCaptureMode, void(dune::scan::types::ScanCaptureModeType value));
    MOCK_CONST_METHOD0(getScanImagingProfile, dune::scan::types::ScanImagingProfileType());
    MOCK_METHOD1(setScanImagingProfile, void(dune::scan::types::ScanImagingProfileType value));
    MOCK_CONST_METHOD0(getBookMode, dune::scan::types::BookModeEnum());
    MOCK_METHOD1(setBookMode, void(dune::scan::types::BookModeEnum value));

    MOCK_CONST_METHOD0(getCcdChannel, dune::scan::types::CcdChannelEnum());
    MOCK_METHOD1(setCcdChannel, void(dune::scan::types::CcdChannelEnum value));
    MOCK_CONST_METHOD0(getBinaryRendering, dune::scan::types::BinaryRenderingEnum());
    MOCK_METHOD1(setBinaryRendering, void(dune::scan::types::BinaryRenderingEnum value));
    MOCK_CONST_METHOD0(getDescreen, bool());
    MOCK_METHOD1(setDescreen, void(bool value));
    MOCK_CONST_METHOD0(getFeederPickStop, bool());
    MOCK_METHOD1(setFeederPickStop, void(bool value));
    MOCK_CONST_METHOD0(getShadow, uint32_t());
    MOCK_METHOD1(setShadow, void(uint32_t value));
    MOCK_CONST_METHOD0(getCompressionFactor, int());
    MOCK_METHOD1(setCompressionFactor, void(int value));
    MOCK_CONST_METHOD0(getThreshold, uint32_t());
    MOCK_METHOD1(setThreshold, void(uint32_t value));

    MOCK_CONST_METHOD0(getScanAutoColorDetect, dune::scan::types::AutoColorDetectEnum());
    MOCK_METHOD1(setScanAutoColorDetect, void(dune::scan::types::AutoColorDetectEnum value));

    MOCK_CONST_METHOD0(getScanBlackBackground, bool());
    MOCK_METHOD1(setScanBlackBackground, void(bool value));

    MOCK_CONST_METHOD0(getScanNumberPages, uint());
    MOCK_METHOD1(setScanNumberPages, void(uint value));

    MOCK_CONST_METHOD0(getScanAutoExposure, bool());
    MOCK_METHOD1(setScanAutoExposure, void(bool value));

    MOCK_CONST_METHOD0(getScanGamma, uint());
    MOCK_METHOD1(setScanGamma, void(uint value));

    MOCK_CONST_METHOD0(getScanHighlight, int32_t());
    MOCK_METHOD1(setScanHighlight, void(int32_t value));

    MOCK_CONST_METHOD0(getScanColorSensitivity, int32_t());
    MOCK_METHOD1(setScanColorSensitivity, void(int32_t value));

    MOCK_CONST_METHOD0(getScanColorRange, int());
    MOCK_METHOD1(setScanColorRange, void(int value));

    MOCK_CONST_METHOD0(getScanPagesFlipUpEnabled, bool());
    MOCK_METHOD1(setScanPagesFlipUpEnabled, void(bool value));

    MOCK_CONST_METHOD0(getImagePreview, dune::scan::types::ImagePreview());
    MOCK_METHOD1(setImagePreview, void(dune::scan::types::ImagePreview value));

    MOCK_CONST_METHOD0(getNumberUpPresentationDirection, dune::imaging::types::NumberUpPresentationDirection());
    MOCK_METHOD1(setNumberUpPresentationDirection, void(dune::imaging::types::NumberUpPresentationDirection value));
 
    MOCK_CONST_METHOD0(getImageBorder, dune::imaging::types::ImageBorder());
    MOCK_METHOD1(setImageBorder, void(dune::imaging::types::ImageBorder value));
 
    MOCK_CONST_METHOD0(getBookletFormat, dune::imaging::types::BookletFormat());
    MOCK_METHOD1(setBookletFormat, void(dune::imaging::types::BookletFormat value));

    MOCK_CONST_METHOD0(getPagesPerSheet, dune::imaging::types::CopyOutputNumberUpCount());
    MOCK_METHOD1(setPagesPerSheet, void(dune::imaging::types::CopyOutputNumberUpCount value));

    MOCK_CONST_METHOD0(getAutoRelease, bool());
    MOCK_METHOD1(setAutoRelease, void(bool value));

    MOCK_CONST_METHOD0(getScanAcquisitionsSpeed, dune::scan::types::ScanAcquisitionsSpeedEnum());
    MOCK_METHOD1(setScanAcquisitionsSpeed, void(dune::scan::types::ScanAcquisitionsSpeedEnum value));

    MOCK_CONST_METHOD0(getEdgeToEdgeScan, bool());
    MOCK_METHOD1(setEdgeToEdgeScan, void(bool value));

    MOCK_CONST_METHOD0(getLongPlotScan, bool());
    MOCK_METHOD1(setLongPlotScan, void(bool value));

    MOCK_CONST_METHOD0(getCopyMargins, dune::imaging::types::CopyMargins());
    MOCK_METHOD1(setCopyMargins, void(dune::imaging::types::CopyMargins value));

    MOCK_CONST_METHOD0(getPrintingOrder, dune::imaging::types::PrintingOrder());
    MOCK_METHOD1(setPrintingOrder, void(dune::imaging::types::PrintingOrder value));

    MOCK_CONST_METHOD0(getRotation, int());
    MOCK_METHOD1(setRotation, void(int value));

    MOCK_CONST_METHOD0(getAutoRotate, bool());
    MOCK_METHOD1(setAutoRotate, void(bool value));

    MOCK_CONST_METHOD0(getMediaFamily, dune::imaging::types::MediaFamily());
    MOCK_METHOD1(setMediaFamily, void(dune::imaging::types::MediaFamily value));

    MOCK_CONST_METHOD0(getOutputDestination, dune::imaging::types::MediaDestinationId());
    MOCK_METHOD1(setOutputDestination, void(dune::imaging::types::MediaDestinationId value));

    MOCK_CONST_METHOD0(getInvertColors, bool());
    MOCK_METHOD1(setInvertColors, void(bool value));

    MOCK_CONST_METHOD0(getOutputCanvas, dune::imaging::types::OutputCanvasT());
    MOCK_METHOD1(setOutputCanvas, void(dune::imaging::types::OutputCanvasT valueTable));
    MOCK_CONST_METHOD0(getPlexSide, dune::imaging::types::PlexSide());
    MOCK_METHOD1(setPlexSide, void(dune::imaging::types::PlexSide value));

    MOCK_CONST_METHOD0(getRequestedPages, int());
    MOCK_METHOD1(setRequestedPages, void(int value));

    MOCK_CONST_METHOD0(getCompressionType, dune::scan::types::CompressionModeEnum());
    MOCK_METHOD1(setCompressionType, void(dune::scan::types::CompressionModeEnum value));

    MOCK_CONST_METHOD1(determineMarginLayoutOrDefault, MarginLayout(MarginLayout defaultMarginLayout));

    MOCK_METHOD0(dumpIntentToLog, void());
    MOCK_METHOD0(dumpScanIntentSettings, void());

    MOCK_CONST_METHOD0(getScanCalibrationType, dune::imaging::types::ScanCalibrationType());
    MOCK_METHOD1(setScanCalibrationType, void(dune::imaging::types::ScanCalibrationType calibrationType));

    MOCK_CONST_METHOD0(getCustomMediaXDimension, double());
    MOCK_METHOD1(setCustomMediaXDimension, void(double));
    MOCK_CONST_METHOD0(getCustomMediaYDimension, double());
    MOCK_METHOD1(setCustomMediaYDimension, void(double));

    MOCK_CONST_METHOD0(getStapleOption, dune::imaging::types::StapleOptions());
    MOCK_METHOD1(setStapleOption, void(dune::imaging::types::StapleOptions stapleOption));

    MOCK_CONST_METHOD0(getPunchOption, dune::imaging::types::PunchingOptions());
    MOCK_METHOD1(setPunchOption, void(dune::imaging::types::PunchingOptions punchOption));

    MOCK_CONST_METHOD0(getPromptForMorePages, bool());
    MOCK_METHOD1(setPromptForMorePages, void(bool value));

    MOCK_CONST_METHOD0(isFlatbedDuplexCompleted, bool());
    MOCK_METHOD1(setFlatbedDuplexCompleted, void(bool value));
    
    MOCK_CONST_METHOD0(getFoldOption, dune::imaging::types::FoldingOptions());
    MOCK_METHOD1(setFoldOption, void(dune::imaging::types::FoldingOptions foldOption));

    MOCK_CONST_METHOD0(getSheetsPerSetForCFold, int());
    MOCK_METHOD1(setSheetsPerSetForCFold, void(int value));

    MOCK_CONST_METHOD0(getSheetsPerSetForVFold, int());
    MOCK_METHOD1(setSheetsPerSetForVFold, void(int value));

    MOCK_CONST_METHOD0(getBookletMakerOption, dune::imaging::types::BookletMakingOptions());
    MOCK_METHOD1(setBookletMakerOption, void(dune::imaging::types::BookletMakingOptions bookeltMakerOption));

    MOCK_CONST_METHOD0(getSheetsPerSetForFoldAndStitch, int());
    MOCK_METHOD1(setSheetsPerSetForFoldAndStitch, void(int value));

    MOCK_CONST_METHOD0(getDeviceSetsFoldAndStitchSheetsEnabled, bool());
    MOCK_METHOD1(setDeviceSetsFoldAndStitchSheetsEnabled, void(int value));

    MOCK_CONST_METHOD0(getJobOffsetMode, dune::imaging::types::JobOffsetMode());
    MOCK_METHOD1(setJobOffsetMode, void(dune::imaging::types::JobOffsetMode jobOffsetMode));

    MOCK_CONST_METHOD0(getEraseEdgeEnabled, bool());
    MOCK_METHOD1(setEraseEdgeEnabled, void(bool value));

    MOCK_CONST_METHOD0(getSameValuesForAllEdgesEnabled, bool());
    MOCK_METHOD1(setSameValuesForAllEdgesEnabled, void(bool value));

    MOCK_CONST_METHOD0(getMirrorFrontSideEdgesEnabled, bool());
    MOCK_METHOD1(setMirrorFrontSideEdgesEnabled, void(bool value));

    MOCK_CONST_METHOD0(getEraseLeft, double());
    MOCK_METHOD1(setEraseLeft, void(double value));

    MOCK_CONST_METHOD0(getEraseTop, double());
    MOCK_METHOD1(setEraseTop, void(double value));

    MOCK_CONST_METHOD0(getEraseRight, double());
    MOCK_METHOD1(setEraseRight, void(double value));

    MOCK_CONST_METHOD0(getEraseBottom, double());
    MOCK_METHOD1(setEraseBottom, void(double value));

    MOCK_CONST_METHOD0(getEraseBackLeft, double());
    MOCK_METHOD1(setEraseBackLeft, void(double value));

    MOCK_CONST_METHOD0(getEraseBackTop, double());
    MOCK_METHOD1(setEraseBackTop, void(double value));

    MOCK_CONST_METHOD0(getEraseBackRight, double());
    MOCK_METHOD1(setEraseBackRight, void(double value));

    MOCK_CONST_METHOD0(getEraseBackBottom, double());
    MOCK_METHOD1(setEraseBackBottom, void(double value));

    MOCK_CONST_METHOD0(getAutoPaperColorRemovalLevel, uint32_t());
    MOCK_METHOD1(setAutoPaperColorRemovalLevel, void(uint32_t value));
    MOCK_CONST_METHOD0(getpromptForIdCardBothSide, bool());
    MOCK_METHOD1(setpromptForIdCardBothSide, void(bool value));
    MOCK_CONST_METHOD0(getAutoPaperColorRemoval, bool());
    MOCK_METHOD1(setAutoPaperColorRemoval, void(bool value));

    MOCK_CONST_METHOD0(getAutoToneLevel, uint32_t());
    MOCK_METHOD1(setAutoToneLevel, void(uint32_t value));
    MOCK_CONST_METHOD0(getAutoTone, bool());
    MOCK_METHOD1(setAutoTone, void(bool value));

    MOCK_CONST_METHOD0(getWatermarkSettings, dune::imaging::types::WatermarkSettingsT());
    MOCK_METHOD1(setWatermarkSettings, void(dune::imaging::types::WatermarkSettingsT value));

    MOCK_CONST_METHOD0(getStampTopLeft, dune::imaging::types::ScanStampLocationFbT());
    MOCK_METHOD1(setStampTopLeft, void(dune::imaging::types::ScanStampLocationFbT value));

    MOCK_CONST_METHOD0(getStampTopCenter, dune::imaging::types::ScanStampLocationFbT());
    MOCK_METHOD1(setStampTopCenter, void(dune::imaging::types::ScanStampLocationFbT value));
    
    MOCK_CONST_METHOD0(getStampTopRight, dune::imaging::types::ScanStampLocationFbT());
    MOCK_METHOD1(setStampTopRight, void(dune::imaging::types::ScanStampLocationFbT value));
    
    MOCK_CONST_METHOD0(getStampBottomLeft, dune::imaging::types::ScanStampLocationFbT());
    MOCK_METHOD1(setStampBottomLeft, void(dune::imaging::types::ScanStampLocationFbT value));
    
    MOCK_CONST_METHOD0(getStampBottomCenter, dune::imaging::types::ScanStampLocationFbT());
    MOCK_METHOD1(setStampBottomCenter, void(dune::imaging::types::ScanStampLocationFbT value));
    
    MOCK_CONST_METHOD0(getStampBottomRight, dune::imaging::types::ScanStampLocationFbT());
    MOCK_METHOD1(setStampBottomRight, void(dune::imaging::types::ScanStampLocationFbT value));

    MOCK_CONST_METHOD0(getAutoCropMode, dune::imaging::types::AutoCropMode());
    MOCK_METHOD1(setAutoCropMode, void(dune::imaging::types::AutoCropMode value));

    MOCK_CONST_METHOD0(getMatchOriginalOutputMediaSizeId, dune::imaging::types::MediaSizeId());
    MOCK_METHOD1(setMatchOriginalOutputMediaSizeId, void(dune::imaging::types::MediaSizeId value));
};
class MockICopyJobResult : public ICopyJobResult
{
  public:
    MOCK_CONST_METHOD0(getCompletedImpressions, uint32_t());
    MOCK_METHOD1(setCompletedImpressions, void(const uint32_t completedPages));
    MOCK_CONST_METHOD0(getCompletedCopies, uint32_t());
    MOCK_METHOD1(setCompletedCopies, void(const uint32_t completedCopies));
    MOCK_CONST_METHOD0(getCurrentPage, uint32_t());
    MOCK_METHOD1(setCurrentPage, void(const uint32_t currentPage));
    MOCK_CONST_METHOD0(getProgress, uint32_t());
    MOCK_METHOD1(setProgress, void(const uint32_t progress));
    MOCK_CONST_METHOD0(getCurrentCuringTemperature, uint32_t());
    MOCK_METHOD1(setCurrentCuringTemperature, void(const uint32_t currentCuringTemperature));
    MOCK_METHOD0(clone, std::unique_ptr<ICopyJobResult>());
    MOCK_CONST_METHOD0(getRemainingPrintingTime, uint32_t());
    MOCK_METHOD1(setRemainingPrintingTime, void(const uint32_t remainingPrintingTime));
    MOCK_CONST_METHOD0(serialize, std::unique_ptr<CopyJobResultFbT>());
    MOCK_METHOD1(deserialize, void(const CopyJobResultFbT&));
    MOCK_CONST_METHOD0(areAllPagesDiscovered, bool());
    MOCK_METHOD1(setAllPagesDiscovered, void(const bool allPagesDiscovered));
    MOCK_CONST_METHOD0(getPixelCounts, dune::job::PixelCounts());
    MOCK_METHOD1(setPixelCounts, void(const dune::job::PixelCounts pixelCounts));
    MOCK_CONST_METHOD0(getTotalScanDuration, uint32_t());
    MOCK_METHOD1(setTotalScanDuration, void(const uint32_t totalScanDuration));
    MOCK_CONST_METHOD0(getActiveScanDuration, uint32_t());
    MOCK_METHOD1(setActiveScanDuration, void(const uint32_t activeScanDuration));
};

}}}}  // namespace dune::copy::Jobs::Copy
