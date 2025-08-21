/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPYJOB_CONSTRAINT_H
#define DUNE_COPY_JOBS_COPY_COPYJOB_CONSTRAINT_H

#include "ICopyJobConstraints.h"
#include "ScanJobConstraint.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {
/**
 * @class CopyJobConstraint
 * @brief Copy Job Constraint
 *
 */
class CopyJobConstraint : public dune::scan::Jobs::Scan::ScanJobConstraint<ICopyJobConstraints>
{
private:
    /* Constraint for Copy */
    std::vector<dune::imaging::types::Plex> plexMode_;
    std::vector<dune::imaging::types::PlexBinding> plexBinding_;
    std::vector<dune::copy::SheetCollate> collate_;
    int minCopies_{1};
    int maxCopies_{999};
    double stepCopies_{1.0};
    std::vector<dune::imaging::types::PrintQuality> printQuality_;
    std::vector<CopyJobMediaSupportedSize> mediaSupportSize_;
    std::vector<CopyJobMediaSupportedType> mediaSupportType_;
    std::vector<dune::imaging::types::MediaSource> mediaPrintSupportedSource_;
    std::vector<dune::imaging::types::MediaSizeId> mediaPrintSupportedSize_;
    std::vector<dune::imaging::types::MediaIdType> mediaPrintSupportedType_;
    std::vector<dune::imaging::types::CopyMargins> copyMargins_;
    std::vector<dune::imaging::types::PrintingOrder> printingOrder_;
    int minRotation_{0};
    int maxRotation_{270};
    double stepRotation_{90};
    std::vector<dune::imaging::types::MediaFamily> mediaFamily_;
    std::vector<bool> autoRotate_;
    std::vector<short> foldingStyles_;
    std::vector<dune::imaging::types::MediaDestinationId> printMediaDestinations_;
    std::vector<dune::imaging::types::StapleOptions> stapleOption_;
    std::vector<dune::imaging::types::PunchingOptions> punchOption_;
    std::vector<dune::imaging::types::FoldingOptions> foldOption_;
    std::vector<dune::imaging::types::BookletMakingOptions> bookletMakerOption_;
    std::vector<dune::imaging::types::JobOffsetMode> jobOffsetMode_;
    int minSheetsPerSetForCFold_{1};
    int maxSheetsPerSetForCFold_{3};
    int minSheetsPerSetForVFold_{1};
    int maxSheetsPerSetForVFold_{5};
    int minSheetsPerSetForFoldAndStitch_{1};
    int maxSheetsPerSetForFoldAndStitch_{25};
    std::vector<bool> deviceSetsFoldAndStitchSheetsEnabled_;

public:
    CopyJobConstraint();
    /* Constraint for Copy */
    inline void addPlexMode(dune::imaging::types::Plex plexMode) override { addValueOnVector(plexMode_, plexMode); }
    inline std::vector<dune::imaging::types::Plex> getPlexMode() const override{ return plexMode_; }
    inline void addPlexBinding(dune::imaging::types::PlexBinding plexBinding) override { addValueOnVector(plexBinding_, plexBinding); }
    inline std::vector<dune::imaging::types::PlexBinding> getPlexBinding() const override { return plexBinding_; }
    inline void addCollate(dune::copy::SheetCollate collate) override { addValueOnVector(collate_, collate); }
    inline std::vector<dune::copy::SheetCollate> getCollate() const override { return collate_; }
    inline void setMinCopies(int minCopies) override { minCopies_ = minCopies; }
    inline int getMinCopies() const override { return minCopies_; }
    inline void setMaxCopies(int maxCopies) override { maxCopies_ = maxCopies; }
    inline int getMaxCopies() const override { return maxCopies_; }
    inline void setStepCopies(double stepCopies) override { stepCopies_ = stepCopies; }
    inline int getStepCopies() const override { return stepCopies_; }
    inline void addPrintQuality(dune::imaging::types::PrintQuality printQuality) override { addValueOnVector(printQuality_, printQuality); }
    inline std::vector<dune::imaging::types::PrintQuality> getPrintQuality() const override { return printQuality_; }
    inline void addMediaSupportedSize(CopyJobMediaSupportedSize mediaSupportedSize) override { addValueOnVector(mediaSupportSize_, mediaSupportedSize); }
    inline std::vector<CopyJobMediaSupportedSize> getMediaSupportedSizes() const override { return mediaSupportSize_; }
    inline void addMediaSupportedType(CopyJobMediaSupportedType mediaSupportedType) override { addValueOnVector(mediaSupportType_, mediaSupportedType); }
    inline std::vector<CopyJobMediaSupportedType> getMediaSupportedTypes() const override { return mediaSupportType_; }
    inline void addMediaPrintSupportedSource(dune::imaging::types::MediaSource mediaPrintSupportedSource) override { addValueOnVector(mediaPrintSupportedSource_, mediaPrintSupportedSource); }
    inline std::vector<dune::imaging::types::MediaSource> getMediaPrintSupportedSource() const override { return mediaPrintSupportedSource_; }
    inline void addMediaPrintSupportedSize(dune::imaging::types::MediaSizeId mediaPrintSupportedSize) override { addValueOnVector(mediaPrintSupportedSize_, mediaPrintSupportedSize); }
    inline std::vector<dune::imaging::types::MediaSizeId> getMediaPrintSupportedSize() const override { return mediaPrintSupportedSize_; }
    inline void addMediaPrintSupportedType(dune::imaging::types::MediaIdType mediaPrintSupportedType) override { addValueOnVector(mediaPrintSupportedType_, mediaPrintSupportedType); }
    inline std::vector<dune::imaging::types::MediaIdType> getMediaPrintSupportedType() const override { return mediaPrintSupportedType_; }
    inline void addCopyMargins(dune::imaging::types::CopyMargins copyMargins) override { addValueOnVector(copyMargins_, copyMargins); }
    inline std::vector<dune::imaging::types::CopyMargins> getCopyMargins() const override { return copyMargins_; }
    inline void addPrintingOrder(dune::imaging::types::PrintingOrder printingOrder) override { addValueOnVector(printingOrder_, printingOrder); }
    inline std::vector<dune::imaging::types::PrintingOrder> getPrintingOrder() const override { return printingOrder_; }
    inline void setMinRotation(int minRotation) override { minRotation_ = minRotation; }
    inline int getMinRotation() const override { return minRotation_; }
    inline void setMaxRotation(int maxRotation) override { maxRotation_ = maxRotation; }
    inline int getMaxRotation() const override { return maxRotation_; }
    inline void setStepRotation(double stepRotation) override { stepRotation_ = stepRotation; }
    inline int getStepRotation() const override { return stepRotation_; }
    inline void addMediaFamily(dune::imaging::types::MediaFamily mediaFamily) override { addValueOnVector(mediaFamily_, mediaFamily); }
    inline std::vector<bool> getAutoRotate() const override { return autoRotate_; }
    inline void addAutoRotate(bool autoRotate) override { addValueOnVector(autoRotate_, autoRotate); }
    inline std::vector<short> getFoldingStyles() const override{ return foldingStyles_;}
    inline void addFoldingStyle( short foldingStyles ){ addValueOnVector( foldingStyles_, foldingStyles );}
    inline std::vector<dune::imaging::types::MediaFamily> getMediaFamily() const override { return mediaFamily_; }
    inline void addMediaDestinations(dune::imaging::types::MediaDestinationId mediaDestinationId) override { addValueOnVector(printMediaDestinations_,mediaDestinationId); }
    inline std::vector<dune::imaging::types::MediaDestinationId> getMediaDestinations() const override { return printMediaDestinations_; }
    inline std::vector<dune::imaging::types::StapleOptions> getStapleOption() const override { return stapleOption_; }
    inline void addStapleOption(dune::imaging::types::StapleOptions stapleOption) override { addValueOnVector(stapleOption_, stapleOption); }
    inline std::vector<dune::imaging::types::PunchingOptions> getPunchOption() const override { return punchOption_; }
    inline void addPunchOption(dune::imaging::types::PunchingOptions punchOption) override { addValueOnVector(punchOption_, punchOption); }
    inline std::vector<dune::imaging::types::FoldingOptions> getFoldOption() const override { return foldOption_; }
    inline void addFoldOption(dune::imaging::types::FoldingOptions foldOption) override { addValueOnVector(foldOption_, foldOption); }
    inline void setMinSheetsPerSetForCFold(int minSheetsPerSetForCFold) override { minSheetsPerSetForCFold_ = minSheetsPerSetForCFold; }
    inline int getMinSheetsPerSetForCFold() const override { return minSheetsPerSetForCFold_; }
    inline void setMaxSheetsPerSetForCFold(int maxSheetsPerSetForCFold) override { maxSheetsPerSetForCFold_ = maxSheetsPerSetForCFold; }
    inline int getMaxSheetsPerSetForCFold() const override { return maxSheetsPerSetForCFold_; }
    inline void setMinSheetsPerSetForVFold(int minSheetsPerSetForVFold) override { minSheetsPerSetForVFold_ = minSheetsPerSetForVFold; }
    inline int getMinSheetsPerSetForVFold() const override { return minSheetsPerSetForVFold_; }
    inline void setMaxSheetsPerSetForVFold(int maxSheetsPerSetForVFold) override { maxSheetsPerSetForVFold_ = maxSheetsPerSetForVFold; }
    inline int getMaxSheetsPerSetForVFold() const override { return maxSheetsPerSetForVFold_; }
    inline std::vector<dune::imaging::types::BookletMakingOptions> getBookletMakerOption() const override { return bookletMakerOption_; }
    inline void addBookletMakerOption(dune::imaging::types::BookletMakingOptions bookletMakerOption) override { addValueOnVector(bookletMakerOption_, bookletMakerOption); }
    inline void setMinSheetsPerSetForFoldAndStitch(int minSheetsPerSetForFoldAndStitch) override { minSheetsPerSetForFoldAndStitch_ = minSheetsPerSetForFoldAndStitch; }
    inline int getMinSheetsPerSetForFoldAndStitch() const override { return minSheetsPerSetForFoldAndStitch_; }
    inline void setMaxSheetsPerSetForFoldAndStitch(int maxSheetsPerSetForFoldAndStitch) override { maxSheetsPerSetForFoldAndStitch_ = maxSheetsPerSetForFoldAndStitch; }
    inline int getMaxSheetsPerSetForFoldAndStitch() const override { return maxSheetsPerSetForFoldAndStitch_; }
    inline std::vector<bool> getDeviceSetsFoldAndStitchSheetsEnabled() const override { return deviceSetsFoldAndStitchSheetsEnabled_; }
    inline void addDeviceSetsFoldAndStitchSheetsEnabled(bool deviceSetsFoldAndStitchSheetsEnabled) override { addValueOnVector(deviceSetsFoldAndStitchSheetsEnabled_, deviceSetsFoldAndStitchSheetsEnabled); }
    dune::copy::Jobs::Copy::CopyJobMediaSupportedType* findCopyJobMediaSupportedType(dune::imaging::types::MediaIdType mediaType) override;
    dune::copy::Jobs::Copy::CopyJobMediaSupportedSize* findCopyJobMediaSupportedSize(dune::imaging::types::MediaSizeId mediaSize) override;
    inline std::vector<dune::imaging::types::JobOffsetMode> getJobOffsetMode() const override { return jobOffsetMode_; }    
    inline void addJobOffsetMode(dune::imaging::types::JobOffsetMode jobOffsetMode) override { addValueOnVector(jobOffsetMode_, jobOffsetMode); }
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif