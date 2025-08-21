#ifndef DUNE_JOB_COPY_PAGE_TICKET_HANDLER_H
#define DUNE_JOB_COPY_PAGE_TICKET_HANDLER_H

////////////////////////////////////////////////////////////////////////////////
/**
 * @file  CopyPageTicketHandler.h
 * @brief Dune Job Pipeline - PageTicket Handler
 *
 * (c) Copyright HP Inc. 2022. All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "PageTicketHandlerBase.h"
#include "ICopyPageTicket.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * @brief class to handle Page tickets.
 * @see CopyPageTicketHandler
 */
class CopyPageTicketHandler : public dune::job::PageTicketHandlerBase
{
  public:
    /**
     * @brief Constructor
     *
     * @param ticket reference to the handled ticket
     * @param jobTicketEventSource Event to notify job ticket's changes
     * @param threadPool Pool to notify job ticket changes
     */
    CopyPageTicketHandler(ICopyPageTicket& ticket, PageTicketEventSource& pageTicketEventSource);

    /**
     * @name IPageTicketHandler methods.
     * @{
     */
    dune::job::IPageTicketHandler::MediaSettings  getMediaSettings() const override;
    dune::job::IPageTicketHandler::InputDetails&  getInputDetails() override;
    dune::job::IPageTicketHandler::ResultDetails& getResultDetails() override;
    dune::job::IPageTicketHandler::TimingDetails& getTimingDetails() override;
    std::shared_ptr<dune::job::IIntent> getIntent(dune::job::IntentType intentType) const override;

    /**
     * @brief Set the directory store path of the page
     *
     * @param pageStorePath - string - Full directory path to store page data.
     */
    void        setPageStorePath(std::string pageStorePath) override;

    /**
     * @brief Get the directory store path of the page
     *
     */
    std::string getPageStorePath() const override;
    /**
     * @brief Set the file's memory handler
     *
     * @param fileHandle - uint32.
     */
    void setMemoryFileHandle(uint32_t fileHandle) override;

    /**
     * @brief Get the file's memory handler
     *
     */
    uint32_t getMemoryFileHandle() const override ;
    /** @} */

  private:
    /**
     * @name PageTicketHandlerBase methods.
     * @{
     */
    void doSetMediaSettings(const dune::job::IPageTicketHandler::MediaSettings& mediaSettings) override;
    void doSetInputDetails(const dune::job::IPageTicketHandler::InputDetails& inputDetails) override;
    void doSetResultDetails(const dune::job::IPageTicketHandler::ResultDetails& resultDetails) override;
    void doSetTimingDetails(const dune::job::IPageTicketHandler::TimingDetails& timingDetails) override;

    /**
     * @brief Get the Input Details from the ticket
     *
     * @return InputDetails Input Details
     */
    dune::job::IPageTicketHandler::InputDetails getInputDetailsFromTicket();

    /**
     * @brief Set the Input Details to the ticket
     *
     * @param InputDetails Input Details
     */
    void setInputDetailsToTicket(const dune::job::IPageTicketHandler::InputDetails& inputDetails);

    /**
     * @brief Get the Result Details from the ticket
     *
     * @return ResultDetails Result Details
     */
    dune::job::IPageTicketHandler::ResultDetails getResultDetailsFromTicket();

    /**
     * @brief Set the Result Details to the ticket
     *
     * @param ResultDetails Result Details
     */
    void setResultDetailsToTicket(const dune::job::IPageTicketHandler::ResultDetails& resultDetails);

    /**
     * @brief Get the Timing Details from the ticket
     *
     * @return TimingDetails Timing Details
     */
    dune::job::IPageTicketHandler::TimingDetails getTimingDetailsFromTicket();

    /**
     * @brief Set the Timing Details to the ticket
     *
     * @param TimingDetails Timing Details
     */
    void setTimingDetailsToTicket(const dune::job::IPageTicketHandler::TimingDetails& timingDetails);

    /** @} */

    ICopyPageTicket&                             ticket_;         ///< reference to the ticket to handle
    dune::job::IPageTicketHandler::InputDetails  inputDetails_;   ///< Cached input details
    dune::job::IPageTicketHandler::ResultDetails resultDetails_;  ///< Cached result details
    //Will be removed with DUNE-165676
    dune::job::IPageTicketHandler::TimingDetails timingDetails_;  ///< Cached result details
};
}}}}  // namespace dune::copy::Jobs

#endif  // DUNE_JOB_COPY_PAGE_TICKET_HANDLER_H
