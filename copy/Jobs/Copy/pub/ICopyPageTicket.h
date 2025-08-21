#ifndef DUNE_COPY_JOBS_ICOPY_PAGE_TICKET_H
#define DUNE_COPY_JOBS_ICOPY_PAGE_TICKET_H

////////////////////////////////////////////////////////////////////////////////
/**
 * @file  ICopyPageTicket.h
 * @brief Copy Page Ticket interface
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "CopyPageTicket_generated.h"
#include "IImagingIntent.h"
#include "IPageTicket.h"
#include "PrintIntents.h"
#include "ScanDataTypes.h"
#include "CopyPageIntent.h"
#include "CopyPageResult.h"

// forward declaration
namespace dune { namespace job {
class IPageTicketHandler;
}}  // namespace dune::job

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * @class ICopyPageTicket
 * @brief Base interface for the CopyPageTicket
 */
class ICopyPageTicket : public dune::job::IPageTicket
{
  public:
    using FbT = CopyPageTicketFbT;

    /**
     * @brief Destroy the ICopyPageTicket object
     */
    virtual ~ICopyPageTicket() = default;

    /**
     * @brief Set the Print Intent object
     * @param printIntent
     */
    virtual void setPrintIntent(std::shared_ptr<dune::print::engine::PrintIntents> printIntent) = 0;

    /**
     * @brief Set the Imaging intent object
     * @param imagingIntent
     */
    virtual void setImagingIntent(std::shared_ptr<dune::imaging::types::IImagingIntent> imagingIntent) = 0;

    /**
     * @brief Set the Scan Intent object
     * @param scanPageIntent
     */
    virtual void setScanIntent(std::shared_ptr<dune::scan::types::ScanTicketStruct> scanPageIntent) = 0;

    /**
     * @brief Get the Page Intent object
     * 
     * @return std::shared_ptr<dune::job::CopyPageIntent> 
     */
    virtual std::shared_ptr<dune::job::CopyPageIntent> getPageIntent() const = 0;

    /**
     * @brief Get the Page Result object
     * 
     * @return std::shared_ptr<dune::job::CopyPageResult> 
     */
    virtual std::shared_ptr<dune::job::CopyPageResult> getPageResult() const = 0;
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif  // DUNE_COPY_JOBS_ICOPY_PAGE_TICKET_H
