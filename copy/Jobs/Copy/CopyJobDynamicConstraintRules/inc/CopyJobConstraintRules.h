/* -*- c++ -*- */
// Base Class impl for the Constraint Rules flavors

#ifndef DUNE_COPY_JOBS_COPY_COPYJOB_CONSTRAINTRULES_H
#define DUNE_COPY_JOBS_COPY_COPYJOB_CONSTRAINTRULES_H

#include "ConstraintsGroup.h"
#include "ErrorManager.h"
#include "ICopyJobTicket.h"
#include "IMediaConstraints.h"
#include "com.hp.cdm.domain.glossary.version.1.easybuffers_autogen.h"
#include "com.hp.cdm.service.jobTicket.version.1_generated.h"
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"
#include "com.hp.cdm.service.overlay.version.1_generated.h"
#include "com.hp.cdm.service.overlay.version.1.sharedTypes.overlay_generated.h"
#include "com.hp.cdm.service.overlay.version.1.easybuffers_autogen.h"
#include "ICopyJobConstraints.h"

using namespace dune::framework::data::constraints;
using namespace dune::cdm::glossary_1;
using namespace dune::cdm::jobTicket_1;
using namespace dune::cdm::overlay_1;
using namespace dune::cdm::overlay_1::watermarkDetails;

namespace dune { namespace copy { namespace Jobs { namespace Copy {
/**
 * @class CopyJobConstraintRules
 * @brief This is the base class for copy job constraint rules. 
 *
 */
class CopyJobConstraintRules 
{
protected:    
    virtual std::vector<dune::cdm::glossary_1::MediaSize> getPossibleMediaSizes(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::vector<dune::cdm::glossary_1::MediaType> getPossibleMediaTypes(std::shared_ptr<ICopyJobTicket> jobTicket);

public:

    virtual std::shared_ptr<Constraints> getMediaSizeIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getMediaIdTypeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getMediaSourceConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getPlexModeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getOutputPrintMediaConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getPrintColorModeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getPagesPerSheetConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getScanCaptureModeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkTypeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkTextFontConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkTextSizeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkTextColorConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkOnlyFirstPageConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkRotate45Constraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkBackgroundColorConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkBackgroundPatternConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getWatermarkDarknessConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);

    virtual std::shared_ptr<Constraints> getMediaPrintSupportedSource(std::vector<dune::imaging::types::MediaSource> mediaPrintSupportedSource, std::vector<dune::cdm::glossary_1::MediaSourceId> vecPosMediaSources);
    virtual std::shared_ptr<Constraints> getMediaPrintSupportedSize(std::vector<dune::imaging::types::MediaSizeId> mediaPrintSupportedSize, std::vector<dune::cdm::glossary_1::MediaSize> vecPosMediaSizes);
    virtual std::shared_ptr<Constraints> getMediaPrintSupportedType(std::vector<dune::imaging::types::MediaIdType> mediaPrintSupportedType, std::vector<dune::cdm::glossary_1::MediaType> vecPosMediaTypes);
    virtual std::shared_ptr<Constraints> getInputMediaSizeIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket, std::shared_ptr<dune::framework::data::constraints::Constraints> mediaSizeIdConstraints);
    virtual std::shared_ptr<Constraints> getScaleSelectionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getCustomMediaXFeedDimension(dune::print::engine::constraints::IMediaConstraints *mediaConstraints);
    virtual std::shared_ptr<Constraints> getCustomMediaYFeedDimension(dune::print::engine::constraints::IMediaConstraints *mediaConstraints);
    virtual bool hasColorPermission(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual bool isColorRestricted(std::shared_ptr<ICopyJobTicket> jobTicket) = 0;
    bool checkIfColorIsNotRestricted(std::shared_ptr<ICopyJobTicket> jobTicket);

    virtual std::vector<dune::cdm::overlay_1::StampType> getStampContents(dune::cdm::overlay_1::StampLocation stampLocation, std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getStampLocationConstraints(dune::cdm::overlay_1::StampLocation stampLocation, std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getStampPolicyConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getStampTypeConstraints(dune::cdm::overlay_1::StampLocation stampLocation, std::shared_ptr<ICopyJobTicket> jobTicket, dune::imaging::types::StampPolicy stampPolicy);
    virtual std::shared_ptr<Constraints> getStampTextColorConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getStampTextFontConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getStampTextSizeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    virtual std::shared_ptr<Constraints> getStampPageNumberingStyleConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);

    virtual void updateScanContentOrientationConstraints(std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> scanConstraintsGroup, 
        std::shared_ptr<ICopyJobTicket> jobTicket);

    bool restrictColorPrint_ = false;
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif
