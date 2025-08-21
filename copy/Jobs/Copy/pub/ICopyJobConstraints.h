/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_ICOPY_JOB_CONSTRAINTS_H
#define DUNE_COPY_JOBS_COPY_ICOPY_JOB_CONSTRAINTS_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   ICopyJobConstraints.h
 * @date   Tue, 05 Jan 2021 14:47:38 -0700
 * @brief  Copy Job Constraints Interface
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////
#include "CopyJobConstraints_generated.h"
#include "IScanJobConstraint.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class CopyJobMediaSupportedSize
{
public:
    inline void addId(dune::imaging::types::MediaSizeId id) {id_ = id;}
    inline dune::imaging::types::MediaSizeId getId() const { return id_; }
    inline void addMediaOrientation(dune::imaging::types::MediaOrientation mediaOrientation)  {mediaOrientation_ = mediaOrientation; }
    inline dune::imaging::types::MediaOrientation getMediaOrientation() const { return mediaOrientation_; }
    void addSupportedMediaSource(std::vector<dune::imaging::types::MediaSource> supportedMediaSource);
    inline std::set<dune::imaging::types::MediaSource>  getSupportedMediaSource() const { return supportedMediaSource_; }
    void addDuplex(std::vector<dune::imaging::types::Plex> duplex);
    inline std::set<dune::imaging::types::Plex> getDuplex() const { return duplex_; }

    bool operator==(const CopyJobMediaSupportedSize &other) const {
        return this == &other || (id_ == other.getId() &&
                    mediaOrientation_ == other.getMediaOrientation() &&
                    supportedMediaSource_ == other.getSupportedMediaSource() &&
                    duplex_ == other.getDuplex());
    }
private:
    dune::imaging::types::MediaSizeId id_ = dune::imaging::types::MediaSizeId::ANY;
    dune::imaging::types::MediaOrientation mediaOrientation_ = dune::imaging::types::MediaOrientation::PORTRAIT;
    std::set<dune::imaging::types::MediaSource> supportedMediaSource_;
    std::set<dune::imaging::types::Plex> duplex_;
};

class CopyJobMediaSupportedType
{
public:
    inline void addId(dune::imaging::types::MediaIdType id) {id_ = id;}
    inline dune::imaging::types::MediaIdType getId() const {return id_;}
    void addSupportedMediaSource(std::vector<dune::imaging::types::MediaSource> supportedMediaSource);
    inline std::set<dune::imaging::types::MediaSource> getSupportedMediaSource() const { return supportedMediaSource_; }
    void addDuplex(std::vector<dune::imaging::types::Plex> duplex);
    inline std::set<dune::imaging::types::Plex> getDuplex() const { return duplex_; }
    void addColorMode(std::vector<dune::imaging::types::ColorMode> colorMode);
    inline std::set<dune::imaging::types::ColorMode> getColorMode() const { return colorMode_; }

    bool operator==(const CopyJobMediaSupportedType &other) const {
        return this == &other || (id_ == other.getId() &&
                    supportedMediaSource_ == other.getSupportedMediaSource() &&
                    duplex_ == other.getDuplex() &&
                    colorMode_ == other.getColorMode() );
    }
private:
    dune::imaging::types::MediaIdType id_ = dune::imaging::types::MediaIdType::ANY;
    std::set<dune::imaging::types::MediaSource> supportedMediaSource_;
    std::set<dune::imaging::types::Plex> duplex_;
    std::set<dune::imaging::types::ColorMode> colorMode_;
};

class ICopyJobConstraints  : public dune::scan::Jobs::Scan::IScanJobConstraints
{
public:
    /* Constraint for Copy */
    virtual void addPlexMode(dune::imaging::types::Plex plexMode) = 0;
    virtual std::vector<dune::imaging::types::Plex> getPlexMode() const = 0;
    virtual void addPlexBinding(dune::imaging::types::PlexBinding plexBinding) = 0;
    virtual std::vector<dune::imaging::types::PlexBinding> getPlexBinding() const = 0;
    virtual void addCollate(dune::copy::SheetCollate collate) = 0;
    virtual std::vector<dune::copy::SheetCollate> getCollate() const = 0;
    virtual void setMinCopies(int minCopies) = 0;
    virtual int getMinCopies() const = 0;
    virtual void setMaxCopies(int maxCopies) = 0;
    virtual int getMaxCopies() const = 0;
    virtual void setStepCopies(double stepCopies) = 0;
    virtual int getStepCopies() const = 0;
    virtual void addPrintQuality(dune::imaging::types::PrintQuality printQuality) = 0;
    virtual std::vector<dune::imaging::types::PrintQuality> getPrintQuality() const = 0;
    virtual void addMediaSupportedSize(CopyJobMediaSupportedSize mediaSupportedSize) = 0;
    virtual std::vector<CopyJobMediaSupportedSize> getMediaSupportedSizes() const = 0;
    virtual void addMediaSupportedType(CopyJobMediaSupportedType mediaSupportedType) = 0;
    virtual std::vector<CopyJobMediaSupportedType> getMediaSupportedTypes() const = 0;
    virtual void addMediaPrintSupportedSource(dune::imaging::types::MediaSource mediaPrintSupportedSource) = 0;
    virtual std::vector<dune::imaging::types::MediaSource> getMediaPrintSupportedSource() const = 0;
    virtual void addMediaPrintSupportedSize(dune::imaging::types::MediaSizeId mediaPrintSupportedSize) = 0;
    virtual std::vector<dune::imaging::types::MediaSizeId> getMediaPrintSupportedSize() const = 0;
    virtual void addMediaPrintSupportedType(dune::imaging::types::MediaIdType mediaPrintSupportedType) = 0;
    virtual std::vector<dune::imaging::types::MediaIdType> getMediaPrintSupportedType() const = 0;
    virtual void addCopyMargins(dune::imaging::types::CopyMargins copyMargins) = 0;
    virtual std::vector<dune::imaging::types::CopyMargins> getCopyMargins() const = 0;
    virtual void addPrintingOrder(dune::imaging::types::PrintingOrder printingOrder) = 0;
    virtual std::vector<dune::imaging::types::PrintingOrder> getPrintingOrder() const = 0;
    virtual void setMinRotation(int minRotation) = 0;
    virtual int getMinRotation() const = 0;
    virtual void setMaxRotation(int maxRotation) = 0;
    virtual int getMaxRotation() const = 0;
    virtual void setStepRotation(double stepRotation) = 0;
    virtual int getStepRotation() const = 0;
    virtual void addMediaFamily(dune::imaging::types::MediaFamily mediaFamily) = 0;
    virtual std::vector<dune::imaging::types::MediaFamily> getMediaFamily() const = 0;
    virtual void addAutoRotate(bool autoRotate) = 0;
    virtual std::vector<bool> getAutoRotate() const = 0;
    /**
     * @brief Adds a folding style.
     *
     * This is a pure virtual method that must be implemented by derived classes.
     * It's used to add a folding style to the copy job ticket.
     *
     * @param foldingStyle The folding style to be added. This should be a short integer.
     */
    virtual void addFoldingStyle( short foldingStyle ) = 0;
    /**
     * @brief get the folding styles.
     *
     * This is a pure virtual method that must be implemented by derived classes.
     * It's used to retrieve all the folding styles added to the copy job ticket.
     *
     * @return A vector of short integers representing the folding styles.
     */
    virtual std::vector<short> getFoldingStyles() const = 0;
    virtual void addMediaDestinations(dune::imaging::types::MediaDestinationId mediaDestinationId) = 0;
    virtual std::vector<dune::imaging::types::MediaDestinationId> getMediaDestinations() const = 0;
    virtual void addStapleOption(dune::imaging::types::StapleOptions stapleOption) = 0;
    virtual std::vector<dune::imaging::types::StapleOptions> getStapleOption() const = 0;
    virtual void addPunchOption(dune::imaging::types::PunchingOptions punchOption) = 0;
    virtual std::vector<dune::imaging::types::PunchingOptions> getPunchOption() const = 0;
    virtual void addFoldOption(dune::imaging::types::FoldingOptions foldOption) = 0;
    virtual std::vector<dune::imaging::types::FoldingOptions> getFoldOption() const = 0;
    virtual void setMinSheetsPerSetForCFold(int minSheetsPerSetForCFold) = 0;
    virtual int getMinSheetsPerSetForCFold() const = 0;
    virtual void setMaxSheetsPerSetForCFold(int maxSheetsPerSetForVFold)  = 0;
    virtual int getMaxSheetsPerSetForCFold() const = 0;
    virtual void setMinSheetsPerSetForVFold(int minSheetsPerSetForCFold)  = 0;
    virtual int getMinSheetsPerSetForVFold() const = 0;
    virtual void setMaxSheetsPerSetForVFold(int maxSheetsPerSetForVFold)  = 0;
    virtual int getMaxSheetsPerSetForVFold() const = 0;
    virtual std::vector<dune::imaging::types::BookletMakingOptions> getBookletMakerOption() const = 0;
    virtual void addBookletMakerOption(dune::imaging::types::BookletMakingOptions bookletMakerOption) = 0;
    virtual void setMinSheetsPerSetForFoldAndStitch(int minSheetsPerSetForFoldAndStitch) = 0;
    virtual int getMinSheetsPerSetForFoldAndStitch() const = 0;
    virtual void setMaxSheetsPerSetForFoldAndStitch(int maxSheetsPerSetForFoldAndStitch) = 0;
    virtual int getMaxSheetsPerSetForFoldAndStitch() const = 0;
    virtual std::vector<bool> getDeviceSetsFoldAndStitchSheetsEnabled() const = 0;
    virtual void addDeviceSetsFoldAndStitchSheetsEnabled(bool deviceSetsFoldAndStitchSheetsEnabled) =0;
    virtual dune::copy::Jobs::Copy::CopyJobMediaSupportedType* findCopyJobMediaSupportedType(dune::imaging::types::MediaIdType mediaType) =0;
    virtual dune::copy::Jobs::Copy::CopyJobMediaSupportedSize* findCopyJobMediaSupportedSize(dune::imaging::types::MediaSizeId mediaSize)=0;
    virtual std::vector<dune::imaging::types::JobOffsetMode> getJobOffsetMode() const = 0;
    virtual void addJobOffsetMode(dune::imaging::types::JobOffsetMode jobOffsetMode) = 0;
};

}}}} // namespace dune::copy::Jobs::Copy

#endif