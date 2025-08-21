/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_ICOPY_JOB_TICKET_H
#define DUNE_COPY_JOBS_COPY_ICOPY_JOB_TICKET_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   ICopyJobTicket.h
 * @date   Wed, 08 May 2019 06:49:54 -0700
 * @brief  Copy Job Ticket Interface
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IJobTicket.h"
#include "IScanJobIntent.h"
#include "IIntentsManager.h"
#include "CopyJobTicket_generated.h"
#include "ExportImportTypes_generated.h"
#include "MarginLayout_generated.h"
#include "ScanCalibrationTypes_generated.h"
#include "JobResultDataTypes.h"
#include "IColorAccessControl.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {
  class ICopyJobConstraints;
}}}} // namespace dune::copy::Jobs::Copy

namespace dune { namespace print { namespace engine {
  class IMedia;
  class IMediaInfo;
  class IPrintIntentsFactory;
}}} // namespace dune::print::engine

namespace dune { namespace scan { namespace scanningsystem {
  class IMedia;
  class IScannerCapabilities;
}}} // namespace dune::scan::scanningsystem

namespace dune { namespace framework { namespace storage {
  class INvram;
}}} // namespace dune::framework::storage

namespace dune { namespace localization {
  class ILocaleProvider;
}} // namespase dune::localization

using APIResult = dune::framework::core::APIResult;
using MarginLayout = dune::imaging::types::MarginLayout;
using PromptType = dune::job::PromptType;

namespace dune { namespace copy { namespace Jobs { namespace Copy {

struct MaxLengthConfig
{
  u_int32_t                                         scanMaxCm;
  u_int32_t                                         jpegMaxLines;
  u_int32_t                                         tiffMaxMb;
  u_int32_t                                         pdfMaxCm;
  u_int32_t                                         pdfaMaxCm;
  u_int32_t                                         longPlotMaxCm;
};

enum Product
{
  HOME_PRO = 0,
  LFP = 1,
  ENTERPRISE = 2,
  MIN = HOME_PRO,
  MAX = ENTERPRISE
};

/**
 * @class ICopyJobIntent
 * @brief Copy Job Intent Interface
 *
 */
class ICopyJobIntent : public dune::scan::Jobs::Scan::IScanJobIntent
{
public:
    virtual dune::imaging::types::MediaSizeId getOutputMediaSizeId() const = 0;
    virtual void setOutputMediaSizeId(dune::imaging::types::MediaSizeId value) = 0;

    virtual dune::imaging::types::MediaOrientation getOutputMediaOrientation() const = 0;
    virtual void setOutputMediaOrientation(dune::imaging::types::MediaOrientation value) = 0;

    virtual dune::imaging::types::MediaIdType getOutputMediaIdType() const = 0;
    virtual void setOutputMediaIdType(dune::imaging::types::MediaIdType value) = 0;

    virtual dune::imaging::types::MediaSource getOutputMediaSource() const = 0;
    virtual void setOutputMediaSource(dune::imaging::types::MediaSource value) = 0;

    /**
     * @brief Gets the folding style ID.
     *
     * It's used to retrieve the folding style ID from the copy job ticket.
     *
     * @return A short integer representing the folding style ID.
     *         The folding style ID can be one of the following:
     *         0: Do not fold
     *         1: User Defined
     *         2: Folder Selected
     *         3: Stack
     *         4 - 255: Reserved, Do Not Use
     *         256 - 65535: Use freely
     */
    virtual short getFoldingStyleId() const = 0;

    /**
     * @brief Sets the folding style ID.
     *
     * It's used to set the folding style ID for the copy job ticket.
     *
     * @param value The folding style ID. This should be a short integer.
     *              0: Do not fold
     *              1: User Defined
     *              2: Folder Selected
     *              3: Stack
     *              4 - 255: Reserved, Do Not Use
     *              256 - 65535: Use freely
     */
    virtual void setFoldingStyleId(short value) = 0;

    virtual dune::imaging::types::Plex getOutputPlexMode() const = 0;
    virtual void setOutputPlexMode(dune::imaging::types::Plex value) = 0;

    virtual dune::imaging::types::PlexBinding getOutputPlexBinding() const = 0;
    virtual void setOutputPlexBinding (dune::imaging::types::PlexBinding value) = 0;

    virtual int  getCopies() const = 0;
    virtual void setCopies(int value) = 0;

    virtual dune::copy::SheetCollate getCollate() const = 0;
    virtual void setCollate(dune::copy::SheetCollate value) = 0;

    virtual dune::imaging::types::PrintQuality getCopyQuality() const = 0;
    virtual void setCopyQuality (dune::imaging::types::PrintQuality value) = 0;

    //TODO: Need to update resize once  it is added in jobTicket
    virtual int getResize() const = 0;
    virtual void setResize (int value) = 0;

    //TODO: Need to update lighter/Darker once it is added in jobTicket
    virtual int getLighterDarker() const = 0;
    virtual void setLighterDarker (int value) = 0;

    virtual dune::imaging::types::CopyMargins getCopyMargins() const = 0;
    virtual void setCopyMargins(dune::imaging::types::CopyMargins value) = 0;

    virtual dune::imaging::types::MediaDestinationId getOutputDestination() const = 0;
    virtual void setOutputDestination(dune::imaging::types::MediaDestinationId value) = 0;

    virtual dune::imaging::types::PlexSide getPlexSide() const = 0;
    virtual void setPlexSide(dune::imaging::types::PlexSide value) = 0;

    virtual int  getRequestedPages() const = 0;
    virtual void setRequestedPages(int value) = 0;

    virtual dune::imaging::types::PrintingOrder getPrintingOrder() const = 0;
    virtual void setPrintingOrder(dune::imaging::types::PrintingOrder value) = 0;

    virtual int getRotation() const = 0;
    virtual void setRotation(int value) = 0;

    /**
     * @brief Get the Auto Rotate current value
     * @return true if auto rotation of job is enabled
     * @return false if not
     */
    virtual bool getAutoRotate() const = 0;

    /**
     * @brief Enable/Disable Auto Rotation on Copy Ticket
     * @param value boolean value
     */
    virtual void setAutoRotate(bool value) = 0;

    virtual dune::imaging::types::MediaFamily getMediaFamily() const = 0;
    virtual void setMediaFamily(dune::imaging::types::MediaFamily value) = 0;

    virtual MarginLayout determineMarginLayoutOrDefault(MarginLayout defaultMarginLayout) const = 0;

    virtual dune::imaging::types::StapleOptions getStapleOption() const = 0;
    virtual void setStapleOption(dune::imaging::types::StapleOptions value) = 0;

    virtual dune::imaging::types::PunchingOptions getPunchOption() const = 0;
    virtual void setPunchOption(dune::imaging::types::PunchingOptions value) = 0;

    virtual dune::imaging::types::JobOffsetMode getJobOffsetMode() const = 0;
    virtual void setJobOffsetMode(dune::imaging::types::JobOffsetMode value) = 0;

    virtual dune::imaging::types::FoldingOptions getFoldOption() const = 0;
    virtual void setFoldOption(dune::imaging::types::FoldingOptions value) = 0;

    virtual int getSheetsPerSetForCFold() const = 0;
    virtual void setSheetsPerSetForCFold(int value) = 0;

    virtual int getSheetsPerSetForVFold() const  = 0;
    virtual void setSheetsPerSetForVFold(int value)  = 0;

    virtual dune::imaging::types::BookletMakingOptions getBookletMakerOption() const = 0;
    virtual void setBookletMakerOption(dune::imaging::types::BookletMakingOptions value) = 0;

    virtual int getSheetsPerSetForFoldAndStitch() const  = 0;
    virtual void setSheetsPerSetForFoldAndStitch(int value) = 0;

    virtual bool getDeviceSetsFoldAndStitchSheetsEnabled() const = 0;
    virtual void setDeviceSetsFoldAndStitchSheetsEnabled(int value) = 0;

    /**
     * @brief Method to print complete current values of ticket on log
     */
    virtual void dumpIntentToLog() = 0;

    virtual dune::imaging::types::ScanCalibrationType getScanCalibrationType() const = 0;
    virtual void setScanCalibrationType(dune::imaging::types::ScanCalibrationType calibrationType) = 0;

    /**
     * @brief Get/Set the custom paper size X dimension
     */
    virtual double getCustomMediaXDimension() const = 0;
    virtual void setCustomMediaXDimension(double dimension) = 0;

    /**
     * @brief Get/Set the custom paper size Y dimension
     */
    virtual double getCustomMediaYDimension() const = 0;
    virtual void setCustomMediaYDimension(double dimension) = 0;

    virtual void setMatchOriginalOutputMediaSizeId(dune::imaging::types::MediaSizeId mediaSizeId) = 0;
    virtual dune::imaging::types::MediaSizeId getMatchOriginalOutputMediaSizeId() const = 0;
};

class ICopyJobResult
{
  public:
    /**
     * @brief Destroy the ICopyJobResult object
     */
    virtual ~ICopyJobResult(){};

    /**
     * @brief Get CompletedPages
     *
     * @return CompletedPages
     */
    virtual uint32_t getCompletedImpressions() const = 0;

    /**
     * @brief Set CompletedPages
     *
     * @param completedPages CompletedPages
     */
    virtual void setCompletedImpressions(const uint32_t completedPages) = 0;

    /**
     * @brief Get CompletedCopies
     *
     * @return CompletedCopies
     */
    virtual uint32_t getCompletedCopies() const = 0;

    /**
     * @brief Set CompletedCopies
     *
     * @param completedCopies CompletedCopies
     */
    virtual void setCompletedCopies(const uint32_t completedCopies) = 0;

    /**
     * @brief Get the current page being processed / printed
     *
     * @return Current page being processed / printed
     */
    virtual uint32_t getCurrentPage() const = 0;

    /**
     * @brief Set the current page being processed / printed
     *
     * @param currentPage current page being processed / printed
     */
    virtual void setCurrentPage(const uint32_t currentPage) = 0;

    /**
     * @brief Get the current page RemainingPrintingTime
     *
     * @return Current page RemainingPrintingTime in milliseconds
     */
    virtual uint32_t getRemainingPrintingTime() const = 0;

    /**
     * @brief Set the current page RemainingPrintingTime
     *
     * @param currentPage current page RemainingPrintingTime
     */
    virtual void setRemainingPrintingTime(const uint32_t remainingPrintingTime) = 0;

    /* @brief Get the progress of the current job being processed / printed
     *
     * @return Progress of the current job being processed / printed
     */
    virtual uint32_t getProgress() const = 0;

    /**
     * @brief Set the progress of the current job being processed / printed
     *
     * @param progress Progress of the current job being processed / printed
     */
    virtual void setProgress(const uint32_t progress) = 0;

    /**
     * @brief Get the curing temperature of the current job being cured
     *
     * @return Curing Temperature of the current job being cured
     */
    virtual uint32_t getCurrentCuringTemperature() const = 0;

    /**
     * @brief Set the curing temperature of the current job being cured
     *
     * @param currentCuringTemperature Curing Temperature of the current job being cured
     */
    virtual void setCurrentCuringTemperature(const uint32_t currentCuringTemperature) = 0;

    /**
     * @brief Get if all pages have been discovered in the job
     *
     * @return true if all pages have been discovered in the job, false otherwise
     */
    virtual bool areAllPagesDiscovered() const = 0;

    /**
     * @brief Set if all pages have been discovered in the job
     *
     * @param allPagesDiscovered Indicates if all pages have been discovered in the job
     */
    virtual void setAllPagesDiscovered(const bool allPagesDiscovered) = 0;

    /**
     * @brief Gets the pixel counts for the print job.
     * 
     * This function returns the number of pixels in the print job.
     * 
     * @return The pixel counts for the print job.
     */
    virtual dune::job::PixelCounts getPixelCounts() const = 0;
    
    /**
     * @brief Sets the pixel counts for the print job ticket.
     *
     * @param pixelCounts The pixel counts to be set.
     */
    virtual void setPixelCounts(const dune::job::PixelCounts pixelCounts) = 0;

    /**
    * @brief set the total scan duration for the copy job. This is the total time the job is using the scanner
    * @param totalScanDuration The total scan duration in milliseconds
    */
    virtual void setTotalScanDuration(const uint32_t totalScanDuration) = 0;

    /**
     * @brief get the total scan duration for the copy job. This is the total time the job is using the scanner
     * @return The total scan duration in milliseconds
     */
    virtual uint32_t getTotalScanDuration() const = 0;

    /**
     * @brief set the active scan duration for the copy job. This is the total time the job is actively scanning
     * @param activeScanDuration The active scan duration in milliseconds
     */
    virtual void setActiveScanDuration(const uint32_t activeScanDuration) = 0;

    /**
     * @brief get the active scan duration for the copy job. This is the total time the job is actively scanning
     * @return The active scan duration in milliseconds
     */
    virtual uint32_t getActiveScanDuration() const = 0;
    

    virtual std::unique_ptr<ICopyJobResult> clone() = 0;

    /**
     * @brief Serialize / Deserialize Print job result
     */
    virtual std::unique_ptr<CopyJobResultFbT> serialize() const = 0;
    virtual void                              deserialize(const CopyJobResultFbT& data) = 0;
};

/**
 * @class ICopyJobTicket
 * @brief Base Interface for the CopytJobTicket
 *
 */
class ICopyPageTicket;
class ICopyJobTicket : public dune::job::IJobTicket
{
public:
    using FbT = CopyJobTicketFbT;
    using Fb  = CopyJobTicketFb;
    using IntentType = dune::copy::Jobs::Copy::ICopyJobIntent;
    using Constraints = dune::copy::Jobs::Copy::ICopyJobConstraints;
    virtual std::shared_ptr<IntentType> getIntent() const = 0;
    virtual void setIntent(std::shared_ptr<IntentType> intent) = 0;
    virtual std::shared_ptr<ICopyJobResult> getResult() const = 0;
    virtual void setResult(const std::shared_ptr<ICopyJobResult>& result) = 0;
    virtual std::shared_ptr<Constraints> getConstraints() const =0;
    virtual void setConstraints(std::shared_ptr<Constraints> constraints) = 0;
    virtual dune::job::IIntentsManager*     getIntentsManager() const = 0;
    virtual void                            setIntentsManager(dune::job::IIntentsManager* intentsManager) = 0;
    /**
     * @brief Get the Page Intent from the ticket
     *
     * @return dune::job::IIntentsManager::PageIntent Page Intent
     */
    virtual dune::job::IIntentsManager::PageIntent& getPageIntent() = 0;
    /**
     * @brief Set the Page Intent from the ticket
     *
     * @param pageIntent Page Intent
     */
    virtual void                         setPageIntent(dune::job::IIntentsManager::PageIntent pageIntent) = 0;
    virtual bool isFirstScanStarted() const = 0;
    virtual void setFirstScanStarted(const bool firstScanStarted) = 0;
    virtual void setMediaInterface(dune::print::engine::IMedia* mediaInterface) = 0;
    virtual dune::print::engine::IMedia* getMediaInterface() const = 0;
    virtual void setColorAccessControlInterface(dune::imaging::IColorAccessControl* colorAccessControl) = 0;
    virtual dune::imaging::IColorAccessControl* getColorAccessControlInterface() const = 0;
    virtual void setMediaInfoInterface(dune::print::engine::IMediaInfo* mediaInfoInterface) = 0;
    virtual dune::print::engine::IMediaInfo* getMediaInfoInterface() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>> getAllSupportedMediaSizes() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>> getSupportedMediaSizes(dune::imaging::types::MediaSource mediaSource) const = 0;
    virtual void updateSupportedPageBasedFinisherValidMediaSizes(std::vector<dune::cdm::glossary_1::MediaSize>& validMediaSizesList) const = 0;
    virtual std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaSize>> getPageBasedFinisherValidMediaSizes() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> getAllSupportedMediaTypes() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> getSupportedMediaTypes(dune::imaging::types::MediaSource mediaSource) const = 0;
    virtual std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaType>> getPageBasedFinisherValidMediaTypes() const = 0;
    virtual std::tuple<bool, std::vector<dune::cdm::glossary_1::ContentOrientation>> getPageBasedFinisherValidContentOrientation() const = 0;
    virtual void setisMediaTypeVisibilityTogglingSupported(bool isMediaTypeVisibilityTogglingSupported) = 0;
    virtual bool isMediaTypeVisibilityTogglingSupported() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> getEnabledMediaTypes() const = 0;
    virtual void setScanMediaInterface(dune::scan::scanningsystem::IMedia* scanMediaInterface) = 0;
    virtual dune::scan::scanningsystem::IMedia* getScanMediaInterface() const = 0;
    virtual void setScanCapabilitiesInterface(dune::scan::scanningsystem::IScannerCapabilities* scanCapabilitiesInterface) = 0;
    virtual dune::scan::scanningsystem::IScannerCapabilities* getScanCapabilitiesInterface() const = 0;
    virtual void setPreviewMode(bool preview) = 0;
    virtual bool getPreviewMode() const = 0;
    virtual uint32_t getPageCount() const = 0;

    virtual void setNvramInterface(dune::framework::storage::INvram* nvramInterface) = 0;
    virtual dune::framework::storage::INvram* getNvramInterface() const = 0;
    virtual void setLocalizationInterface(dune::localization::ILocaleProvider* locale) = 0;
    virtual dune::localization::ILocaleProvider* getLocalizationInterface() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>> getAllSupportedMediaSources() const = 0;
    virtual dune::imaging::types::MediaSizeId getMediaSizeFromMediaSource(dune::imaging::types::MediaSource source) const = 0;
    virtual bool IsInstalledPageBasedFinisherDevice() const = 0;
    virtual bool IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes mediaProcssingType) const = 0;
    virtual bool UpdateMediaOutputDestinationPageBasedFinisherInstalled() const = 0;
    virtual std::string getConstraintsMsgBetweenFinisherOption(dune::imaging::types::MediaProcessingTypes mediaProcessingType) const = 0;
    virtual void getOutputMediaSizeIdTypeforFinisher(dune::imaging::types::MediaSizeId &outputMediaSizeId, dune::imaging::types::MediaOrientation &outputMediaOrientation, bool &isPossibleBothOrientation) const = 0;
    virtual std::string getStapleString(dune::imaging::types::StapleOptions stapleOption) const = 0;
    virtual std::string getHolePunchString(dune::imaging::types::PunchingOptions punchOption) const = 0;
    virtual std::string getFinisherConstraintString(std::string constraintString) const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>> getPossibleOutputBins() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>> getValidOutputBins() const = 0;
    virtual std::string getStapleConstraintsString(std::vector<dune::imaging::types::StapleOptions> validOptionsFromHelper) const = 0;
    virtual std::string getHolePunchConstraintsString(std::vector<dune::imaging::types::PunchingOptions> validOptionsFromHelper) const = 0;
    virtual bool isValidStaplingOptionForCopy(dune::cdm::jobTicket_1::StapleOptions stapleOption) const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>> getPossibleStaplingOptions() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>> getValidStaplingOptions(std::string &constraintsmsg) const = 0;
    virtual bool isValidPunchingOptionForCopy(dune::cdm::jobTicket_1::PunchOptions punchOption) const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>> getPossiblePunchingOptions() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>> getValidPunchingOptions(std::string &constraintsmsg) const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>> getPossibleFoldingOptions() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>> getValidFoldingOptions(std::string &constraintsmsg) const = 0;
    virtual std::tuple<int, int> getPagesPerSetLimitForFinishingOption(dune::imaging::types::FoldingOptions foldingOption, dune::imaging::types::BookletMakingOptions bookletMakingOption) const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>> getPossibleBookletMakingOptions() const = 0;
    virtual std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>> getValidBookletMakingOptions(std::string &constraintsmsg) const = 0;
    /**
     * @brief Return a list of the output supported from media engine
     * @return std::tuple<APIResult, std::vector<dune::imaging::types::MediaDestinationId>>  result with API Result to know if
     * method execution was correct
     */
    virtual std::tuple<APIResult, std::vector<dune::imaging::types::MediaDestinationId>> getOutputList() const = 0;


    virtual std::shared_ptr<ICopyJobTicket> clone() const = 0;

    /**
     * @brief Get the Copy Page Ticket object
     *
     * @return std::shared_ptr<ICopyPageTicket> Copy Page Ticket
     */
    virtual std::shared_ptr<ICopyPageTicket> getCopyPageTicket(const dune::framework::core::Uuid& pageId) = 0;

    /**
     * @brief Get a Handler to the job ticket.
     * Handler will be provided to job resources to update the ticket during their execution
     * @todo move to IJobTicket, so every jobtype does the same
     * @return new handler
     */
    virtual std::shared_ptr<dune::job::IJobTicketHandler> getHandler() = 0;

    /**
     * @brief To populate the base constraints
     *
     */
    virtual void populateDefaultConstraints() = 0;

    /**
     * @brief Set the Print Intents Factory object
     *
     * @param printIntentsFactory
     */
    virtual void setPrintIntentsFactory(dune::print::engine::IPrintIntentsFactory* printIntentsFactory) = 0;

    // Get if we are in a preScan job or not
    virtual bool isPreScanJob() const = 0;
    virtual void setPreScanJob(bool value) =0 ;

    // Get if we are in a preScan job or not
    virtual bool isPrintAlignmentChangeRequired() const = 0;
    virtual void setPrintAlignmentChangeRequired(bool value) =0 ;

    // Get default media size
    virtual dune::imaging::types::MediaSizeId getDefaultMediaSize() const = 0;
    virtual void setDefaultMediaSize(dune::imaging::types::MediaSizeId mediaSize) =0;

    //Get  prescanned width and heigth
    virtual uint32_t getPrescannedWidth() const = 0;
    virtual void setPrescannedWidth(uint32_t value) =0 ;

    virtual uint32_t getPrescannedHeight() const = 0;
    virtual void setPrescannedHeight(uint32_t value) =0 ;

    //Get preprint configuration
    virtual Product getPrePrintConfiguration() const = 0;
    virtual void setPrePrintConfiguration(Product value) = 0;

    //Get max length configuration
    virtual MaxLengthConfig getMaxLengthConfig() const = 0;
    virtual void setMaxLengthConfig(MaxLengthConfig value) = 0;

    //Get set jobCompleting methods
    virtual bool getJobCompleting() const = 0;
    virtual void setJobCompleting(bool value) = 0;

    //Get set maxCollatePages methods
    virtual uint32_t getMaxCollatePages() const = 0;
    virtual void setMaxCollatePages(uint32_t value) = 0;

    // get/set the flatbed duplex side
    virtual dune::scan::types::DuplexSideEnum getFlatbedDuplexScanSide() const = 0;
    virtual void setFlatbedDuplexScanSide(dune::scan::types::DuplexSideEnum flatbedDuplexScanSide) = 0;
    /**
     * @brief Get the Version of current ticket to report if is initial version or updated version.
     * Used for upgrades process
     * @return uint value
     */
    virtual uint getVersion() const = 0;

    /**
     * @brief Set the Version value of current ticket
     * @param value uint version
     */
    virtual void setVersion(uint value) = 0;

    virtual bool shouldBeBorderless() const = 0;


    //Getter & setter for scan calibration type
    virtual dune::imaging::types::ScanCalibrationType getScanCalibrationType() const = 0;
    virtual void setScanCalibrationType(dune::imaging::types::ScanCalibrationType calibrationType) = 0;
    virtual dune::framework::data::backup::OperationResult writeSettingsToFile(std::string filepath) = 0;
    virtual dune::framework::data::backup::OperationResult readSettingsFromFile(const std::string& filePath) = 0;

    // Get if we are in a earlyCopy job or not
    virtual bool isEarlyCopyJob() const = 0;
    virtual void setEarlyCopyJob(bool value) =0 ;

    virtual void setRestrictColorPrint(bool isColorRestricted) = 0;
    virtual bool isRestrictColorPrint() = 0;

};

}}}} // namespace dune::copy::Jobs::Copy

#endif
