/* -*- c++ -*- */
// 

#ifndef DUNE_COPY_JOBS_COPY_COPYJOB_STATIC_CONSTRAINTRULES_H
#define DUNE_COPY_JOBS_COPY_COPYJOB_STATIC_CONSTRAINTRULES_H

#include "ConstraintsGroup.h"
#include "ErrorManager.h"
#include "ICopyJobTicket.h"
#include "ICopyJobConstraints.h"
#include "com.hp.cdm.domain.glossary.version.1.easybuffers_autogen.h"
#include "com.hp.cdm.service.jobTicket.version.1_generated.h"
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"

using namespace dune::framework::data::constraints;
using namespace dune::cdm::glossary_1;
using namespace dune::cdm::jobTicket_1;

namespace dune { namespace copy { namespace Jobs { namespace Copy {
/**
 * @class CopyJobStaticConstraintRules
 * @brief This is the base class for copy job constraint rules. 
 *
 */
class CopyJobStaticConstraintRules 
{

public:

    static std::shared_ptr<Constraints> getPlexBindingConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getCopyMarginsConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getCopiesConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getPrintQualityConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getCollateConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getPrintingOrderConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getMediaFamilyConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getRotateConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getStapleOptionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getPunchOptionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getFoldOptionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getSheetsPerFoldSetForCFoldConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getSheetsPerFoldSetForVFoldConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getBookletMakerOptionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getSheetsPerFoldSetForFoldAndStitchConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getSheetsPerFoldSetForDeviceSetsFoldAndStitchSheetsEnabledConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getJobOffsetConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    
    // Next constraints are a workaround, must to be reviewed properly on a next iteration, to modify static constraints to be the standard, and next be overriden with the especific dynamic constraint
    // For the moment needs to be exist here support all static constraints on all products
    static std::shared_ptr<Constraints> getMediaPrintSupportedSource(std::vector<dune::imaging::types::MediaSource> mediaPrintSupportedSource, std::vector<dune::cdm::glossary_1::MediaSourceId> vecPosMediaSources);
    static std::shared_ptr<Constraints> getOutputPrintMediaConstraints(std::shared_ptr<ICopyJobTicket> jobTicket, dune::imaging::types::MediaDestinationId defaultMediaConstraint = dune::imaging::types::MediaDestinationId::DEFAULT);
    static std::shared_ptr<Constraints> getMediaSizeIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getMediaIdTypeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::vector<dune::cdm::glossary_1::MediaSize> getPossibleMediaSizes(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::vector<dune::cdm::glossary_1::MediaType> getPossibleMediaTypes(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getFoldingStyleIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getMediaSourceConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getPlexModeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket);
    static std::shared_ptr<Constraints> getCustomMediaXFeedDimensionConstraints();
    static std::shared_ptr<Constraints> getCustomMediaYFeedDimensionConstraints();
    static std::shared_ptr<Constraints> getScaleToOutputConstraints(std::vector<dune::cdm::glossary_1::MediaSourceId> enumPossibleValues, std::vector<dune::cdm::glossary_1::MediaSourceId> enumValidValues);
    static bool isStampEnabled(std::shared_ptr<ICopyJobTicket> jobTicket);
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif
