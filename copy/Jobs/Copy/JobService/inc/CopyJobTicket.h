/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPYJOB_TICKET_H
#define DUNE_COPY_JOBS_COPY_COPYJOB_TICKET_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobTicket.h
 * @date   Wed, 08 May 2019 06:49:54 -0700
 * @brief  Copy Job Ticket
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////
#include <mutex>

#include "IDataStore.h"
#include "CopyJobTicket_generated.h"
#include "ICopyJobTicket.h"
#include "JobTicket.h"
#include "ScanJobIntent.h"
#include "DataObject.h"
#include "CopyJobConstraint.h"
#include "CopyJobTicketHandler.h"
#include "MediaHelper.h"
#include "MediaFinisherHelper.h"
#include "CopyPageTicket.h"
#include "MarginLayout_generated.h"
#include "ScanCalibrationTypes_generated.h"
#include "IExportImport.h"
#include "INvram.h"
#include "IPipeMetaInfo.h"

using MarginsParameters = dune::print::engine::IMedia::MarginsParameters;
using Margins = dune::imaging::types::Margins;
using MarginLayout = dune::imaging::types::MarginLayout;


static constexpr const char* _VERSION_ = "1.0";

namespace dune { namespace framework { namespace core {
class ThreadPool;
}}}
namespace dune { namespace copy { namespace Jobs { namespace Copy {

bool deserializeCopyJobIntent(std::shared_ptr<CopyJobIntentFbT> data, std::shared_ptr<ICopyJobIntent>&& intent);
bool deserializeConstraints(std::shared_ptr<CopyJobConstraintsFbT> data, std::shared_ptr<ICopyJobConstraints>&& constraint, uint32_t maxCopiesOverride=0);

/**
 * @brief Method to validate a Copy Job Ticket to ensure that internal data is ok
 * @param ticket current ticket to validate
 * @param defaultIntentFromConfig default values accepted
 * @param intentWasUpdated boolean to notify if intent was updated
 */
void validateTicket(std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<CopyJobIntentFbT> defaultIntentFromConfig, bool& intentWasUpdated);

void validateTicketForPageBasedFinisher(std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<CopyJobIntentFbT> defaultIntentFromConfig, bool& intentWasUpdated);

/**
 * @brief Method to compare two intent values
 * @param firstIntent intent to check
 * @param secondIntent intent to check
 * @return true intents are equal
 * @return false intents are not equal
 */
bool compareIntents(std::shared_ptr<ICopyJobIntent> firstIntent = nullptr, std::shared_ptr<ICopyJobIntent> secondIntent = nullptr);

static std::shared_ptr<CopyJobConstraintsFbT> constraintsFb_ = nullptr;


/**
 * @class CopyJobIntent
 * @brief Copy Job Intent
 *
 */
class CopyJobIntent : public dune::scan::Jobs::Scan::ScanJobIntent<ICopyJobIntent>
{
private:
    dune::imaging::types::MediaSizeId       outputMediaSizeId_{dune::imaging::types::MediaSizeId::LETTER};
    dune::imaging::types::MediaOrientation  outputMediaOrientation_{dune::imaging::types::MediaOrientation::PORTRAIT};
    dune::imaging::types::MediaIdType       outputMediaIdType_{dune::imaging::types::MediaIdType::STATIONERY};
    dune::imaging::types::MediaSource       outputMediaSource_{dune::imaging::types::MediaSource::TRAY1};
    short                                   foldingStyleId_{0};
    dune::imaging::types::Plex              outputPlexMode_{dune::imaging::types::Plex::SIMPLEX};
    dune::imaging::types::PlexBinding       outputPlexBinding_{dune::imaging::types::PlexBinding::LONG_EDGE};
    int                                     copies_{1};
    int                                     resize_{100};
    int                                     lighterDarker_{0};
    dune::copy::SheetCollate                collate_{dune::copy::SheetCollate::Collate};
    dune::imaging::types::PrintQuality      copyQuality_{dune::imaging::types::PrintQuality::NORMAL};
    dune::imaging::types::CopyMargins       copyMargins_{dune::imaging::types::CopyMargins::CLIPCONTENT};
    dune::imaging::types::MediaDestinationId outputDestination_{dune::imaging::types::MediaDestinationId::STACKER};
    dune::imaging::types::PlexSide            plexSide_{dune::imaging::types::PlexSide::FIRST};
    int                                     requestedPages_{0};
    dune::imaging::types::PrintingOrder     printingOrder_{dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP};
    int                                     rotation_{0};
    bool                                    autoRotate_{false};
    dune::imaging::types::MediaFamily       mediaFamily_{dune::imaging::types::MediaFamily::ADHESIVE};
    dune::imaging::types::ScanCalibrationType calibrationType_{dune::imaging::types::ScanCalibrationType::UNKNOWN};
    double                                  customMediaXDimension_{0.0};
    double                                  customMediaYDimension_{0.0};
    dune::imaging::types::StapleOptions     stapleOption_{dune::imaging::types::StapleOptions::NONE};
    dune::imaging::types::PunchingOptions   punchOption_{dune::imaging::types::PunchingOptions::NONE};
    dune::imaging::types::JobOffsetMode     jobOffsetMode_{dune::imaging::types::JobOffsetMode::MODE_DISABLE};
    dune::imaging::types::FoldingOptions    foldOption_{dune::imaging::types::FoldingOptions::NONE};
    int                                     sheetsPerSetForCFold_{1};
    int                                     sheetsPerSetForVFold_{1};
    dune::imaging::types::BookletMakingOptions bookletMakerOption_{dune::imaging::types::BookletMakingOptions::NONE};
    int                                     sheetsPerSetForFoldAndStitch_{1};
    bool                                    deviceSetsFoldAndStitchSheetsEnabled_{false};
    dune::imaging::types::MediaSizeId       anyOutputMediaSizeId_{dune::imaging::types::MediaSizeId::ANY};

public:
    CopyJobIntent();
    CopyJobIntent(const CopyJobIntent& oldCopyJobIntent) : ScanJobIntent(oldCopyJobIntent)
    {
        // TODO - Add the setting which can be copied from an existing object
        outputMediaSizeId_      = oldCopyJobIntent.getOutputMediaSizeId();
        outputMediaOrientation_ = oldCopyJobIntent.getOutputMediaOrientation();
        outputMediaIdType_      = oldCopyJobIntent.getOutputMediaIdType();
        outputMediaSource_      = oldCopyJobIntent.getOutputMediaSource();
        outputPlexMode_         = oldCopyJobIntent.getOutputPlexMode();
        outputPlexBinding_      = oldCopyJobIntent.getOutputPlexBinding();
        copies_                 = oldCopyJobIntent.getCopies();
        collate_                = oldCopyJobIntent.getCollate();
        copyQuality_            = oldCopyJobIntent.getCopyQuality();
        resize_                 = oldCopyJobIntent.getResize();
        lighterDarker_          = oldCopyJobIntent.getLighterDarker();
        copyMargins_            = oldCopyJobIntent.getCopyMargins();
        outputDestination_      = oldCopyJobIntent.getOutputDestination();
        plexSide_               = oldCopyJobIntent.getPlexSide();
        requestedPages_         = oldCopyJobIntent.getRequestedPages();
        printingOrder_          = oldCopyJobIntent.getPrintingOrder();
        rotation_               = oldCopyJobIntent.getRotation();
        autoRotate_             = oldCopyJobIntent.getAutoRotate();
        mediaFamily_            = oldCopyJobIntent.getMediaFamily();
        customMediaXDimension_  = oldCopyJobIntent.getCustomMediaXDimension();
        customMediaYDimension_  = oldCopyJobIntent.getCustomMediaYDimension();
        stapleOption_           = oldCopyJobIntent.getStapleOption();
        punchOption_            = oldCopyJobIntent.getPunchOption();
        foldOption_             = oldCopyJobIntent.getFoldOption();
        foldingStyleId_         = oldCopyJobIntent.getFoldingStyleId();
        jobOffsetMode_          = oldCopyJobIntent.getJobOffsetMode();
        sheetsPerSetForCFold_   = oldCopyJobIntent.getSheetsPerSetForCFold();
        sheetsPerSetForVFold_   = oldCopyJobIntent.getSheetsPerSetForVFold();
        bookletMakerOption_     = oldCopyJobIntent.getBookletMakerOption();
        sheetsPerSetForFoldAndStitch_ = oldCopyJobIntent.getSheetsPerSetForFoldAndStitch();
        deviceSetsFoldAndStitchSheetsEnabled_ = oldCopyJobIntent.getDeviceSetsFoldAndStitchSheetsEnabled();
    }

    /**
     * @brief Get the Output Media Size Id object
     * Media Size for Print Image
     * @return dune::imaging::types::MediaSizeId
     */
    inline dune::imaging::types::MediaSizeId getOutputMediaSizeId() const override { return outputMediaSizeId_; }
    inline void setOutputMediaSizeId(dune::imaging::types::MediaSizeId value) override { outputMediaSizeId_ = value; }

    inline void setMatchOriginalOutputMediaSizeId(dune::imaging::types::MediaSizeId mediaSizeId) override { anyOutputMediaSizeId_ = mediaSizeId; }
    inline dune::imaging::types::MediaSizeId getMatchOriginalOutputMediaSizeId() const override { return anyOutputMediaSizeId_; }

    /**
     * @brief Get the Output Media Orientation object
     * Media Orientation for Print Image
     * @return dune::imaging::types::MediaOrientation
     */
    inline dune::imaging::types::MediaOrientation getOutputMediaOrientation() const override { return outputMediaOrientation_; }
    inline void setOutputMediaOrientation(dune::imaging::types::MediaOrientation value) override { outputMediaOrientation_ = value; }

    /**
     * @brief Get the Output Media Id Type object
     * Media Type for Print Image
     * @return dune::imaging::types::MediaIdType
     */
    inline dune::imaging::types::MediaIdType getOutputMediaIdType() const override { return outputMediaIdType_; }
    inline void setOutputMediaIdType(dune::imaging::types::MediaIdType value) override { outputMediaIdType_ = value; }

    /**
     * @brief Get the Output Media Source object
     * Media Source for Print Image
     * @return dune::imaging::types::MediaSource
     */
    inline dune::imaging::types::MediaSource getOutputMediaSource() const override { return outputMediaSource_; }
    inline void setOutputMediaSource(dune::imaging::types::MediaSource value) override { outputMediaSource_ = value; }

    /**
     * @brief Get the Output Folding Style Id object
     * Folding Style for Print Image
     * @return dune::imaging::types::FoldingStyleId
     */
    inline short getFoldingStyleId() const override { return foldingStyleId_; }

    /**
     * @brief Sets the folding style ID.
     *
     * This method sets the folding style ID for the copy job ticket.
     * The folding style ID determines how the output is folded.
     *
     * @param value The folding style ID. This should be a short integer.
     */
    inline void setFoldingStyleId(short value) override { foldingStyleId_ = value; }

    /**
     * @brief Get the Output Plex Mode object
     * Output Plex for Print Image
     * simplex to simplex, simplex to duplex,
     * duplex to simplex, duplex to duplex
     * @return dune::imaging::types::Plex
     */
    inline dune::imaging::types::Plex getOutputPlexMode() const override { return outputPlexMode_; }
    inline void setOutputPlexMode(dune::imaging::types::Plex value) override { outputPlexMode_ = value; }

    /**
     * @brief Get the Output Plex Binding object
     * The Plex Binding specifying long edge or short edge
     * @return dune::imaging::types::PlexBinding
     */
    inline dune::imaging::types::PlexBinding getOutputPlexBinding() const override { return outputPlexBinding_; }
    inline void setOutputPlexBinding(dune::imaging::types::PlexBinding value) override { outputPlexBinding_ = value; }

    /**
     * @brief Get and Set Copies.
     */
    inline int getCopies() const override { return copies_; }
    inline void setCopies(int value) override { copies_ = value; }

    /**
     * @brief Get and Set Collate.
     */
    inline dune::copy::SheetCollate getCollate() const override { return collate_; }
    inline void setCollate(dune::copy::SheetCollate value) override { collate_ = value; }

    /**
     *  @brief Get and Set Copy Quality.
     */
    inline dune::imaging::types::PrintQuality getCopyQuality() const override { return copyQuality_; }
    inline void setCopyQuality(dune::imaging::types::PrintQuality value) override { copyQuality_ = value; }

    /**
     *  @brief Get and Set Copy Resize.
     */
    inline int getResize() const override { return resize_; }
    inline void setResize (int value) override { resize_ = value; }

    /**
     *  @brief Get and Set Copy lighter/Darker
     */
    inline int getLighterDarker() const override { return lighterDarker_; }
    inline void setLighterDarker (int value) override { lighterDarker_ = value; }

    /**
     * @brief Get the Copy Margins object
     * Output CopyMargins option for Print Image
     * @return dune::imaging::types::CopyMargins
     */
    inline dune::imaging::types::CopyMargins getCopyMargins() const override { return copyMargins_; }
    inline void setCopyMargins(dune::imaging::types::CopyMargins value) override { copyMargins_ = value; }

    inline int getRotation() const override { return rotation_; }
    inline void setRotation(int value) override { rotation_ = value; }

    inline bool getAutoRotate() const override { return autoRotate_; }
    inline void setAutoRotate(bool value) override { autoRotate_ = value; }

    inline dune::imaging::types::MediaFamily getMediaFamily() const override { return mediaFamily_; }
    inline void setMediaFamily(dune::imaging::types::MediaFamily value) override { mediaFamily_ = value; }

    inline dune::imaging::types::StapleOptions getStapleOption() const override { return stapleOption_; }
    inline void setStapleOption(dune::imaging::types::StapleOptions value) override { stapleOption_ = value; }

    inline dune::imaging::types::PunchingOptions getPunchOption() const override { return punchOption_; }
    inline void setPunchOption(dune::imaging::types::PunchingOptions value) override { punchOption_ = value; }

    inline dune::imaging::types::MediaDestinationId getOutputDestination() const override { return outputDestination_; }
    inline void setOutputDestination(dune::imaging::types::MediaDestinationId value) override { outputDestination_ = value; }

    inline dune::imaging::types::PlexSide getPlexSide() const override { return plexSide_; };
    inline void setPlexSide(dune::imaging::types::PlexSide value) override { plexSide_ = value; };

    inline dune::imaging::types::JobOffsetMode getJobOffsetMode() const override { return jobOffsetMode_; };
    inline void setJobOffsetMode(dune::imaging::types::JobOffsetMode value) override { jobOffsetMode_ = value; };

    inline dune::imaging::types::FoldingOptions getFoldOption() const override { return foldOption_; }
    inline void setFoldOption(dune::imaging::types::FoldingOptions value) override { foldOption_ = value; }

    inline int getSheetsPerSetForCFold() const override { return sheetsPerSetForCFold_; }
    inline void setSheetsPerSetForCFold(int value) override { sheetsPerSetForCFold_ = value; }

    inline int getSheetsPerSetForVFold() const override { return sheetsPerSetForVFold_; }
    inline void setSheetsPerSetForVFold(int value) override { sheetsPerSetForVFold_ = value; }

    inline dune::imaging::types::BookletMakingOptions getBookletMakerOption() const override { return bookletMakerOption_; }
    inline void setBookletMakerOption(dune::imaging::types::BookletMakingOptions value) override { bookletMakerOption_ = value; }

    inline int getSheetsPerSetForFoldAndStitch() const override { return sheetsPerSetForFoldAndStitch_; }
    inline void setSheetsPerSetForFoldAndStitch(int value) override { sheetsPerSetForFoldAndStitch_ = value; }

    inline bool getDeviceSetsFoldAndStitchSheetsEnabled() const override { return deviceSetsFoldAndStitchSheetsEnabled_; }
    inline void setDeviceSetsFoldAndStitchSheetsEnabled(int value) override { deviceSetsFoldAndStitchSheetsEnabled_ = value; }

    /**
     * @brief Get and Set Copies.
     */
    inline int getRequestedPages() const override { return requestedPages_; }
    inline void setRequestedPages(int value) override { requestedPages_ = value; }

    /**
     * @brief Get/Set the custom paper size X dimension
     */
    inline double getCustomMediaXDimension() const override { return customMediaXDimension_; }
    inline void setCustomMediaXDimension(double dimension) override { customMediaXDimension_ = dimension; }

    /**
     * @brief Get/Set the custom paper size Y dimension
     */
    inline double getCustomMediaYDimension() const override { return customMediaYDimension_; }
    inline void setCustomMediaYDimension(double dimension) override { customMediaYDimension_ = dimension; }

    MarginLayout determineMarginLayoutOrDefault(MarginLayout defaultMarginLayout) const override;

    inline void setPrintingOrder(dune::imaging::types::PrintingOrder printingOrder) override
    {
        printingOrder_ = printingOrder;
    }
    inline dune::imaging::types::PrintingOrder getPrintingOrder() const override { return printingOrder_; }

    /**
     * @brief Method to print complete current values of ticket on log
     */
    void dumpIntentToLog() override;
    /**
     * @brief Get and Set calibration type.
     */
    inline dune::imaging::types::ScanCalibrationType getScanCalibrationType() const override { return calibrationType_; };
    inline void setScanCalibrationType(dune::imaging::types::ScanCalibrationType calibrationType) override { calibrationType_ =  calibrationType; };
};

class CopyJobResult : public ICopyJobResult
{
    public:
      CopyJobResult();
      explicit CopyJobResult(const ICopyJobResult& copyJobResult);
      inline uint32_t getCompletedImpressions() const override { return completedPages_; };
      inline void     setCompletedImpressions(const uint32_t completedPages) override { completedPages_ = completedPages; };
      inline uint32_t getCompletedCopies() const override { return completedCopies_; };
      inline void setCompletedCopies(const uint32_t completedCopies) override { completedCopies_ = completedCopies; };
      inline uint32_t getCurrentPage() const override { return currentPage_; };
      inline void     setCurrentPage(const uint32_t currentPage) override { currentPage_ = currentPage; };
      inline uint32_t getRemainingPrintingTime() const override { return remainingPrintingTime_; };
      inline void     setRemainingPrintingTime(const uint32_t remainingPrintingTime) override { remainingPrintingTime_ = remainingPrintingTime; };
      inline uint32_t getProgress() const override { return progress_; };
      inline void     setProgress(const uint32_t progress) override { progress_ = progress; };
      inline uint32_t getCurrentCuringTemperature() const override { return currentCuringTemperature_; };
      inline void     setCurrentCuringTemperature(const uint32_t currentCuringTemperature) override { currentCuringTemperature_ = currentCuringTemperature; };
      bool areAllPagesDiscovered() const override { return allPagesDiscovered_; };
      void setAllPagesDiscovered(const bool allPagesDiscovered) override { allPagesDiscovered_ = allPagesDiscovered; };
      dune::job::PixelCounts getPixelCounts() const override { return pixelCounts_; };
      void setPixelCounts(const dune::job::PixelCounts pixelCounts) override { pixelCounts_ = pixelCounts; };
      void setTotalScanDuration(const uint32_t totalScanDuration) override { totalScanDuration_ = totalScanDuration; };
      uint32_t getTotalScanDuration() const override { return totalScanDuration_; };
      void setActiveScanDuration(const uint32_t activeScanDuration) override { activeScanDuration_ = activeScanDuration; };
      uint32_t getActiveScanDuration() const override { return activeScanDuration_; };
      std::unique_ptr<ICopyJobResult> clone() override;

      std::unique_ptr<CopyJobResultFbT> serialize() const override;
      void                              deserialize(const CopyJobResultFbT& data) override;

    private:
      uint32_t completedPages_;   ///< Number of completed impressions
      uint32_t completedCopies_;  ///< Number of completed job copies
      uint32_t currentPage_;      ///< Actual page being processed / printed
      uint32_t remainingPrintingTime_;  ///< Actual page remainingPrintingTime
      uint32_t progress_;        ///< Actual progress of the job being processed / printed
      uint32_t currentCuringTemperature_; ///< Actual Cruing temperature
      bool     allPagesDiscovered_;       ///< Indicates if all the pages in the job have been discovered
      dune::job::PixelCounts pixelCounts_;           ///< Pixel counts for the job.
      uint32_t totalScanDuration_; ///< Total scan duration
      uint32_t activeScanDuration_; ///< Active scan duration
};

/**
 * @class CopyJobTicket
 * @brief Copy Job Ticket
 *
 */
class CopyJobTicket : public dune::job::JobTicket<ICopyJobTicket>
{
  private:
    using FlatBufferDataObjectAdapterJobTicket = dune::framework::data::FlatBufferDataObjectAdapter<CopyJobTicketFbT>;
    using SerializedDataBufferPtr = dune::framework::data::SerializedDataBufferPtr;

    /**
     * @brief Find if job has the requested pageTicket
     *
     * @param pageId Id of the page
     * @return iterator to Ticket associated to the page
     */
    std::vector<std::shared_ptr<CopyPageTicket>>::iterator findPageTicket(const Uuid& pageId);

    /**
     * @brief Serialize / Deserialize Copy Pages Tickets
     */
    std::vector<std::unique_ptr<CopyPageTicketFbT>> serializePages() const;
    void deserializePages(const std::vector<std::unique_ptr<CopyPageTicketFbT>>& pages);

    /**
     * @brief Create all the needed intents for the new page
     */
    void createIntents(std::shared_ptr<ICopyPageTicket> pageTicket);

    /**
     * @brief Update Intents in PageTicket
     *
     * @param std::shared_ptr<ICopyPageTicket> PageTicket to update
     */
    void updatePageIntents(std::shared_ptr<ICopyPageTicket> PageTicket);

    //Create scan page intent
    std::shared_ptr<dune::scan::types::ScanTicketStruct> createScanPageIntent();

    //Creates default print intent
    std::shared_ptr<dune::print::engine::PrintIntents> createDefaultPrintIntent();

    //Update print intent with copy job ticket settings
    void updatePrintIntent(std::shared_ptr<dune::print::engine::PrintIntents>& printIntent, dune::framework::core::Uuid pageId);

    // Convert copy margins to maring layout type
    dune::imaging::types::MarginLayout convertToMarginLayout(dune::imaging::types::CopyMargins copyMargins);

    bool calculateRotationAngle();

    // Check if auto crop is supported
    bool isAutoCropSupportedOnScanDevice();

    // Check if scale is supported
    bool isScaleSupportedOnScanDevice();

    static dune::scan::types::OriginalTypeEnum convertOriginalTypeEnumFromOriginalContentType(dune::imaging::types::OriginalContentType contentType);

    dune::scan::types::ScanTypeEnum convertScanTypeEnumFromImagingProfileType(dune::scan::types::ScanImagingProfileType profileType);

    dune::scan::types::ColorSpaceEnum convertColorSpaceFromColorMode(dune::imaging::types::ColorMode colorMode);

    dune::scan::types::ImageQualityEnum convertOutputResolutionToImageQualityEnum(dune::imaging::types::Resolution resolution);

    uint32_t convertScanResToInt(dune::imaging::types::Resolution resolution);

    void setupScanRegion(std::shared_ptr<dune::scan::types::ScanTicketStruct>     scanPageIntent,
                          dune::imaging::types::MediaSizeId                       mediaSize,
                          dune::scan::types::ScanFeedOrientation                  orientation,
                          dune::imaging::types::Resolution                        resolution,
                          dune::scan::types::ScanCaptureModeType                  mode,
                          u_int32_t                                               scanMaxCm,
                          u_int32_t                                               topMargin,
                          u_int32_t                                               bottomMargin,
                          u_int32_t                                               leftMargin,
                          u_int32_t                                               rightMargin);

    void scanPageIntentDumper(const std::shared_ptr<dune::scan::types::ScanTicketStruct> &scanTicketStruct);

    bool                                                    preview_{false};
    bool                                                    preScanJob_{false}; //copy job pipeline property
    bool                                                    marginAlignment_{false};
    uint32_t                                                preScannedWidth_{0}; //copy job pipeline property
    uint32_t                                                preScannedHeight_{0}; //copy job pipeline property
    dune::imaging::types::MediaSizeId                       defaultMediaSize_{dune::imaging::types::MediaSizeId::LETTER}; //copy job pipeline property
    MaxLengthConfig                                         maxLengthConfig_; //copy job pipeline property
    Product                                                 prePrintConfiguration_{Product::HOME_PRO}; //copy job pipeline property
    CopyJobTicketFbT                                        copyJobTicketFbT_;
    dune::print::engine::IMedia*                            mediaInterface_{nullptr};
    dune::print::engine::IMediaInfo*                        mediaInfoPtr_{nullptr};
    dune::scan::scanningsystem::IMedia*                     scanMediaInterface_{nullptr};
    dune::scan::scanningsystem::IScannerCapabilities*       scanCapabilitiesInterface_{nullptr};
    dune::scan::types::DuplexSideEnum                       flatbedDuplexScanSide_{dune::scan::types::DuplexSideEnum::FrontSide};
    dune::print::engine::IPrintIntentsFactory*              printIntentsFactory_;
    dune::framework::storage::INvram*                       nvramInterface_{nullptr};
    dune::localization::ILocaleProvider*                    localization_{nullptr};
    dune::framework::core::ThreadPool*                      threadPool_;
    std::shared_ptr<ICopyJobIntent>                         copyJobIntent_;
    std::shared_ptr<ICopyJobResult>                         copyJobResult_;
    std::shared_ptr<ICopyJobConstraints>                    copyJobConstraints_;
    std::shared_ptr<CopyJobTicketHandler>                   handler_{nullptr};
    std::vector<std::shared_ptr<CopyPageTicket>>            copyPageTickets_;
    mutable std::mutex                                      copyTicketMutex_;  ///< Mutex for syncronization
    uint32_t                                                pageCount_{0};
    uint32_t                                                printPageCount_{0};
    dune::job::IIntentsManager*                             intentsManager_{nullptr};
    dune::job::IIntentsManager::PageIntent                  pageIntent_{};
    uint                                                    version_{0}; ///< current ticket version
    dune::imaging::types::ScanCalibrationType               calibrationType_{dune::imaging::types::ScanCalibrationType::UNKNOWN};
    bool                                                    jobCompleting_{false};
    uint32_t                                                maxCollatePages_{0};
    bool                                                    isMediaTypeVisibilityTogglingSupported_{false};
    bool                                                    isEarlyCopyJob_{false};
    bool                                                    restrictColorPrint_{false}; // If true, restrict color print
    dune::imaging::IColorAccessControl                      *colorAccessControl_{nullptr}; 

  public:
    CopyJobTicket(dune::framework::core::ThreadPool* threadPool = nullptr);
    CopyJobTicket(const CopyJobTicket& oldCopyJobTicket);
    void populateDefaultConstraints() override;

    std::shared_ptr<ICopyJobTicket> clone() const override { return std::make_shared<CopyJobTicket>(*this); };

    std::shared_ptr<ICopyPageTicket> getCopyPageTicket(const dune::framework::core::Uuid& pageId) override;

    void setPrintIntentsFactory(dune::print::engine::IPrintIntentsFactory* printIntentsFactory) override;

    inline std::shared_ptr<ICopyJobIntent> getIntent() const override { return copyJobIntent_; }
    inline void setIntent(std::shared_ptr<ICopyJobIntent> intent) override { copyJobIntent_ = intent; }
    void setIntent(std::shared_ptr<CopyJobIntentFbT> intentFb);
    inline std::shared_ptr<ICopyJobResult> getResult() const override { return copyJobResult_; }
    inline void setResult(const std::shared_ptr<ICopyJobResult>& result) override { copyJobResult_ = result; }
    inline dune::job::IIntentsManager* getIntentsManager() const override { return intentsManager_;}
    inline void setIntentsManager(dune::job::IIntentsManager* intentsManager) override {intentsManager_ = intentsManager;}

    void validateMediaOutputDestination();

    /**
     * @brief Get the Page Intent from the ticket
     *
     * @return dune::job::IIntentsManager::PageIntent Page Intent
     */
    inline dune::job::IIntentsManager::PageIntent& getPageIntent() override { return pageIntent_;}

    /**
     * @brief Set the Page Intent from the ticket
     *
     * @param pageIntent Page Intent
     */
    inline void setPageIntent(dune::job::IIntentsManager::PageIntent pageIntent) override {pageIntent_ = pageIntent;}

    inline std::shared_ptr<ICopyJobConstraints> getConstraints() const override { return copyJobConstraints_; }
    inline void setConstraints(std::shared_ptr<ICopyJobConstraints> constraints) override { copyJobConstraints_ = constraints; }
    void setConstraintsFromFb(std::shared_ptr<CopyJobConstraintsFbT> constraintsFb);
    void clearConstraintsFromFb(void);
    inline bool isFirstScanStarted() const override { return copyJobTicketFbT_.firstScanStarted; }
    inline void setFirstScanStarted(const bool firstScanStarted) override { copyJobTicketFbT_.firstScanStarted = firstScanStarted; }
    inline void setMediaInterface(dune::print::engine::IMedia* mediaInterface) override { mediaInterface_ = mediaInterface; }
    inline dune::print::engine::IMedia* getMediaInterface() const override { return mediaInterface_ ; }
    inline void setMediaInfoInterface(dune::print::engine::IMediaInfo* mediaInfoInterface) override { mediaInfoPtr_= mediaInfoInterface; }
    inline dune::print::engine::IMediaInfo* getMediaInfoInterface() const override {return mediaInfoPtr_; }
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>> getAllSupportedMediaSizes() const override;
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>> getSupportedMediaSizes(dune::imaging::types::MediaSource mediaSource) const override;
    void updateSupportedPageBasedFinisherValidMediaSizes(std::vector<dune::cdm::glossary_1::MediaSize>& validMediaSizesList) const override;
    std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaSize>> getPageBasedFinisherValidMediaSizes() const override;
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> getAllSupportedMediaTypes() const override;
    std::tuple<bool, std::vector<dune::cdm::glossary_1::MediaType>> getPageBasedFinisherValidMediaTypes() const override;
    std::tuple<bool, std::vector<dune::cdm::glossary_1::ContentOrientation>> getPageBasedFinisherValidContentOrientation() const override;
    bool isMediaTypeVisibilityTogglingSupported() const override;
    void setisMediaTypeVisibilityTogglingSupported(bool isMediaTypeVisibilityTogglingSupported) override;
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> getEnabledMediaTypes() const override;
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> getSupportedMediaTypes(dune::imaging::types::MediaSource mediaSource) const override;
    inline void setScanMediaInterface(dune::scan::scanningsystem::IMedia* scanMediaInterface) override { scanMediaInterface_ = scanMediaInterface; }
    inline dune::scan::scanningsystem::IMedia* getScanMediaInterface() const override { return scanMediaInterface_; }
    inline void setScanCapabilitiesInterface(dune::scan::scanningsystem::IScannerCapabilities* scanCapabilitiesInterface) override { scanCapabilitiesInterface_ = scanCapabilitiesInterface; }
    inline dune::scan::scanningsystem::IScannerCapabilities* getScanCapabilitiesInterface() const override { return scanCapabilitiesInterface_; }
    inline void setPreviewMode(bool preview) override { preview_ = preview; }
    inline bool getPreviewMode() const override { return preview_; }
    inline uint32_t getPageCount() const override { return pageCount_; }
    inline void setNvramInterface(dune::framework::storage::INvram* nvramInterface) override { nvramInterface_ = nvramInterface; }
    inline dune::framework::storage::INvram* getNvramInterface() const override { return nvramInterface_ ; }
    inline void setLocalizationInterface(dune::localization::ILocaleProvider* locale) override { localization_ = locale; }
    inline dune::localization::ILocaleProvider* getLocalizationInterface() const override { return localization_ ; }
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>> getAllSupportedMediaSources() const override;
    dune::imaging::types::MediaSizeId getMediaSizeFromMediaSource(dune::imaging::types::MediaSource source) const override;

    // regarding finisher options (staple, punch etc..)
    bool IsInstalledPageBasedFinisherDevice() const override;
    bool IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes mediaProcssingType) const override;
    bool UpdateMediaOutputDestinationPageBasedFinisherInstalled() const override;
    std::string getConstraintsMsgBetweenFinisherOption(dune::imaging::types::MediaProcessingTypes mediaProcessingType) const override;    
    void getOutputMediaSizeIdTypeforFinisher(dune::imaging::types::MediaSizeId &outputMediaSizeId, dune::imaging::types::MediaOrientation &outputMediaOrientation, bool &isPossibleBothOrientation) const override;
    std::string getStapleString(dune::imaging::types::StapleOptions stapleOption) const override;
    std::string getHolePunchString(dune::imaging::types::PunchingOptions punchOption) const override;
    std::string getFinisherConstraintString(std::string constraintString) const override;
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>> getPossibleOutputBins() const override;
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaDestinationId>> getValidOutputBins() const override;
    std::string getStapleConstraintsString(std::vector<dune::imaging::types::StapleOptions> validOptionsFromHelper) const override;
    std::string getHolePunchConstraintsString(std::vector<dune::imaging::types::PunchingOptions> validOptionsFromHelper) const override;
    bool isValidStaplingOptionForCopy(dune::cdm::jobTicket_1::StapleOptions stapleOption) const override;
    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>> getPossibleStaplingOptions() const override;
    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::StapleOptions>> getValidStaplingOptions(std::string &constraintsmsg) const override;
    bool isValidPunchingOptionForCopy(dune::cdm::jobTicket_1::PunchOptions punchOption) const override;
    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>> getPossiblePunchingOptions() const override;
    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::PunchOptions>> getValidPunchingOptions(std::string &constraintsmsg) const override;
    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>> getPossibleFoldingOptions() const override;
    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::FoldOptions>> getValidFoldingOptions(std::string &constraintsmsg) const override;
    std::tuple<int, int> getPagesPerSetLimitForFinishingOption(dune::imaging::types::FoldingOptions foldingOption, dune::imaging::types::BookletMakingOptions bookletMakingOption) const override;
    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>> getPossibleBookletMakingOptions() const override;
    std::tuple<APIResult, std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>> getValidBookletMakingOptions(std::string &constraintsmsg) const override;
    /**
     * @brief Return a list of the output supported from media engine
     * @return std::tuple<APIResult, std::vector<dune::imaging::types::MediaDestinationId>>  result with API Result to know if
     * method execution was correct
     */
    std::tuple<APIResult, std::vector<dune::imaging::types::MediaDestinationId>> getOutputList() const override;

    /**
     * @name IJobTicket methods.
     * @{
     */
    std::shared_ptr<dune::job::IPageTicket> addPage(const Uuid& pageId) override;
    std::shared_ptr<dune::job::IPageTicket> addPage(
        const Uuid& pageId, std::shared_ptr<dune::imaging::types::PageMetaInfoT> pageMetaInfo) override;
    void                                    removePage(const Uuid& pageId) override;
    std::shared_ptr<dune::job::IPageTicket> getPage(const Uuid& pageId);
    std::vector<Uuid>                       getPagesIds(dune::job::PageOrder orderBy) const override;
    /**
     * @name ISerializable methods.
     * @{
     */
    virtual SerializedDataBufferPtr serialize() const override;
    virtual bool deserialize(const SerializedDataBufferPtr& buffer) override;

    inline std::shared_ptr<dune::job::IJobTicketHandler> getHandler() override { return handler_; }

    // Get if we are in a preScan job or not
    inline bool isPreScanJob() const override { return preScanJob_; };
    inline void setPreScanJob(bool value) override { preScanJob_ = value ;} ;

    inline bool isPrintAlignmentChangeRequired() const override { return marginAlignment_; };
    inline void setPrintAlignmentChangeRequired(bool value) override { marginAlignment_ = value ;} ;

    // Get default media size
    inline dune::imaging::types::MediaSizeId getDefaultMediaSize() const override { return defaultMediaSize_; };
    inline void setDefaultMediaSize(dune::imaging::types::MediaSizeId mediaSize) override { defaultMediaSize_= mediaSize; };

    //Get  prescanned width and heigth
    inline uint32_t getPrescannedWidth() const override { return preScannedWidth_;};
    inline void setPrescannedWidth(uint32_t value) override { preScannedWidth_ = value; };

    inline uint32_t getPrescannedHeight() const override {return preScannedHeight_;};
    inline void setPrescannedHeight(uint32_t value) override { preScannedHeight_ = value; };

    //Get preprint configuration
    inline Product getPrePrintConfiguration() const override { return prePrintConfiguration_;};
    inline void setPrePrintConfiguration(Product value) override { prePrintConfiguration_ = value;};

    //Get max length configuration
    inline MaxLengthConfig getMaxLengthConfig() const override {return maxLengthConfig_;};
    inline void setMaxLengthConfig(MaxLengthConfig value) override {maxLengthConfig_ = value;};

    // Get set ticket version methods
    inline uint getVersion() const override {return version_;};
    inline void setVersion(uint value) override {version_ = value;};

    //Get set jobCompleting methods
    inline bool getJobCompleting() const override {return jobCompleting_;};
    inline void setJobCompleting(bool value) override {jobCompleting_ = value;};

    // get/set flatbedDuplexScanSide
    inline dune::scan::types::DuplexSideEnum getFlatbedDuplexScanSide() const override {return flatbedDuplexScanSide_;}
    inline void setFlatbedDuplexScanSide(dune::scan::types::DuplexSideEnum flatbedDuplexScanSide) override {flatbedDuplexScanSide_ = flatbedDuplexScanSide;}

    bool shouldBeBorderless() const override;

    //Getter & setter for scan calibration type
    inline dune::imaging::types::ScanCalibrationType getScanCalibrationType() const override { return calibrationType_; };
    inline void setScanCalibrationType(dune::imaging::types::ScanCalibrationType calibrationType) override { calibrationType_ =  calibrationType; };

    //getter and setter for the maxCollatePages
    inline uint32_t getMaxCollatePages() const override { return maxCollatePages_;};

    inline void setMaxCollatePages(uint32_t value) { maxCollatePages_ = value;} ;

    dune::framework::data::backup::OperationResult writeSettingsToFile(std::string filepath) override;
    dune::framework::data::backup::OperationResult readSettingsFromFile(const std::string& filePath) override;

    inline bool isEarlyCopyJob() const override { return isEarlyCopyJob_; };
    inline void setEarlyCopyJob(bool value) override { isEarlyCopyJob_ = value; };

    inline void setRestrictColorPrint(bool isColorRestricted) override { restrictColorPrint_ = isColorRestricted; }
    bool isRestrictColorPrint() override;

    inline void setColorAccessControlInterface(dune::imaging::IColorAccessControl* colorAccessControl) { 
        colorAccessControl_ = colorAccessControl; 
    }
    inline dune::imaging::IColorAccessControl* getColorAccessControlInterface() const override { 
        return colorAccessControl_; 
    }
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif
