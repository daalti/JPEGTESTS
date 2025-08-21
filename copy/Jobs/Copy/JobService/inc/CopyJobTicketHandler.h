#ifndef DUNE_JOB_COPYJOBTICKET_HANDLER_H
#define DUNE_JOB_COPYJOBTICKET_HANDLER_H

#include "JobTicketHandlerBase.h"



namespace dune { namespace copy { namespace Jobs { namespace Copy {
class ICopyJobTicket; //fwd declaration

/**
 * @brief class to handle Copy job tickets. 
 * @see IJobTicketHandler
 */
class CopyJobTicketHandler : public dune::job::JobTicketHandlerBase
{
public:
    /**
     * @brief Constructor
     *
     * @param ticket reference to the handled ticket
     * @param jobTicketEventSource Event to notify job ticket's changes
     * @param threadPool Pool to notify job ticket changes
     */
    CopyJobTicketHandler(dune::copy::Jobs::Copy::ICopyJobTicket& copyTicket, const JobTicketEvents& jobTicketEvents,
						dune::framework::core::ThreadPool* threadPool);

    /**
     * @name IJobTicketHandler methods.
     * @{
     */
    virtual DocumentSettings  getDocumentSettings() override;
    virtual MediaSettings     getMediaSettings() override;
    virtual InputDetails      getInputDetails() override;
    virtual ResultDetails     getResultDetails() override;
    virtual TimingDetails&    getTimingDetails() override;

    /**
     * @brief Remove a page ticket
     * @param pageId id of page to be removed
     */
    virtual void removePage(const dune::framework::core::Uuid& pageId) override;

    std::shared_ptr<dune::imaging::types::Margins> getMargins(dune::imaging::types::MediaSizeId mediaSize) override;    

protected:
    /**
     * @name JobTicketHandlerBase methods.
     * @{
     */
    void doSetDocumentSettings(const dune::job::IJobTicketHandler::DocumentSettings& documentSettings, const std::vector<DocumentSettingsProperties> propertiesToBeUpdated) override;
    void doSetMediaSettings(const MediaSettings& mediaSettings, const std::vector<MediaSettingsProperties> propertiesToBeUpdated) override;
    void doSetInputDetails(const InputDetails& inputDetails, const std::vector<InputDetailsProperties> propertiesToBeUpdated) override;
    void doSetResultDetails(const ResultDetails& resultDetails, const std::vector<ResultDetailsProperties> propertiesToBeUpdated) override;
    void doSetTimingDetails(const TimingDetails& timingDetails) override;
    /** @} */

private:
    /**
     * @brief Get/Set the Input Details from/to the ticket
     * 
     * @return InputDetails Input Details
     */
    InputDetails  getInputDetailsFromTicket();
    void setInputDetailsToTicket(const InputDetails& inputDetails, const std::vector<IJobTicketHandler::InputDetailsProperties> propertiesToBeUpdated);

    /**
     * @brief Get/Set the Result Details from/to the ticket
     * 
     * @return ResultDetails Result Details
     */
    ResultDetails getResultDetailsFromTicket();
    void setResultDetailsToTicket(const ResultDetails& resultDetails, const std::vector<ResultDetailsProperties> propertiesToBeUpdated);

    dune::copy::Jobs::Copy::ICopyJobTicket& copyTicket_;
    //Will be removed with DUNE-165676
    TimingDetails                           timingDetails_;  ///< Cached result details
};
}}}}

#endif  // DUNE_JOB_COPYJOBTICKET_HANDLER_H