/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_FORCESETS_H
#define DUNE_COPY_JOBS_COPY_FORCESETS_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   ForceSets.h
 * @brief ForceSets
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include <memory>
#include "ScanTypes_generated.h"
#include "typeMappers.h"
#include "ICopyJobTicket.h"
#include "com.hp.cdm.service.jobTicket.version.1.sharedTypes.jobTicket.easybuffers_autogen.h"
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"
#include "IScanConstraints.h"

namespace dune { namespace cdm { namespace jobTicket_1 { 
class JobTicketTable;
class Resolutions;
}}}

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class ICopyJobTicket;

using JobTicketTable = dune::cdm::jobTicket_1::JobTicketTable;

class ForceSets
{
public:
    /**
     * @brief Checks and applies force sets
     *
     */
    static void checkAndApplyScanMediaSourceForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable,std::shared_ptr<ICopyJobTicket> ticket);
    static void checkAndApplyPrintQualityForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<ICopyJobTicket> ticket);
    static void checkAndApplyMediaTypeForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<ICopyJobTicket> ticket);
    static void checkAndApplyTwoPagesPerSheetForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, bool isPatch);

    static void checkAndApplyForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> currentConstraintsGroup, dune::scan::IScanConstraints* scanConstraints);

    static void setHighestResolution(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<ICopyJobTicket> ticket);

    static void setResolution(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, dune::cdm::jobTicket_1::Resolutions res);

    static bool ScannerHasADFDuplex(std::shared_ptr<ICopyJobTicket> ticket);
};

}}}}  // namespace dune::copy::Jobs::Copy
#endif
