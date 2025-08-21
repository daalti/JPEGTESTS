#ifndef DUNE_COPY_JOBS_COPY_PAGE_TICKET_H
#define DUNE_COPY_JOBS_COPY_PAGE_TICKET_H

////////////////////////////////////////////////////////////////////////////////
/**
 * @file  CopyPageTicket.h
 * @brief Copy Page Ticket
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "CopyPageTicketHandler.h"
#include "CopyPageTicket_generated.h"
#include "ICopyPageTicket.h"
#include "PageTicket.h"
#include "CopyPageIntent.h"
#include "CopyPageResult.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * @class CopyPageTicket
 * @brief Base interface for the CopyPageTicket
 */
class CopyPageTicket : public dune::job::PageTicket<ICopyPageTicket>
{
  public:
    /**
     * @brief Construct a new CopyPageTicket object
     *
     * @param threadPool thread pool to notify changes
     */
    CopyPageTicket(dune::framework::core::ThreadPool*                   threadPool = nullptr,
                   std::shared_ptr<dune::imaging::types::PageMetaInfoT> pageMetaInfo = nullptr);

    /**
     * @name CopyPageTicket methods.
     *
     * @param resetResults Indicates if reset the page results
     */
    std::unique_ptr<CopyPageTicket> clone(bool resetResults) const;

    /**
     * @brief Get a Handler to the page ticket.
     * Handler will be provided to page resources to update the ticket during their execution
     * @return new handler
     */
    std::shared_ptr<dune::job::IPageTicketHandler> getHandler() override;

    //Note: Keep in mind that modifying these values while the job is ongoing can have unexpected consequences
    /**
     * @brief Get the Page Intent object
     * 
     * @return std::shared_ptr<dune::job::CopyPageIntent> 
     */
    inline std::shared_ptr<dune::job::CopyPageIntent> getPageIntent() const override { return pageIntent_; }

    /**
     * @brief Get the Page Result object
     * 
     * @return std::shared_ptr<dune::job::CopyPageResult> 
     */
    inline std::shared_ptr<dune::job::CopyPageResult> getPageResult() const override { return pageResult_; }

    /**
     * @}
     */

    /**
     * @brief Serialize / Deserialize Copy Page Ticket from/to FlatBuffer struct
     *
     * @return std::unique_ptr<CopyPageTicketFbT> Serialized Copy Page Ticket to FlatBuffer struct
     */
    std::unique_ptr<CopyPageTicketFbT> serializeToFb() const;
    void                                deserializeFromFb(const CopyPageTicketFbT& copyPageTicketFb);

    /**
     * @brief Set the Print Intent object
     * @param printIntent 
    */
    void setPrintIntent(std::shared_ptr<dune::print::engine::PrintIntents> printIntent) override;

    /**
     * @brief Set the Imaging Intent object
     * @param imagingIntent
     */
    void setImagingIntent(std::shared_ptr<dune::imaging::types::IImagingIntent> imagingIntent) override;

    /**
     * @brief Set the Scan Intent object
     * @param scanIntent 
     */
    void setScanIntent(std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent);

  /**
   * @brief Get the Intent object selected by the intent type
   * @param intentType 
   * @return std::shared_ptr<dune::job::IIntent> 
   */
    std::shared_ptr<dune::job::IIntent> getIntent(dune::job::IntentType intentType) const;

  private:
    std::shared_ptr<dune::job::IIntent>    printIntent_;    ///< Print intent object
    std::shared_ptr<dune::job::IIntent>    imagingIntent_;  ///< Imaging intent object
    std::shared_ptr<dune::job::IIntent>    scanIntent_;     ///< Scan intent object
    std::shared_ptr<CopyPageTicketHandler> handler_;        ///< Handler of the ticket
    std::shared_ptr<dune::job::CopyPageIntent> pageIntent_;  ///< Page Intent object
    std::shared_ptr<dune::job::CopyPageResult> pageResult_;  ///< Page Result object


};

}}}}  // namespace dune::copy::Jobs

#endif  // DUNE_COPY_JOBS_COPY_PAGE_TICKET_H
