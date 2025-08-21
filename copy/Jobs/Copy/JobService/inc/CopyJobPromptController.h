#ifndef DUNE_COPY_JOBS_COPY_JOB_PROMPT_CONTROLLER_H
#define DUNE_COPY_JOBS_COPY_JOB_PROMPT_CONTROLLER_H
////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobPromptController.h
 * @brief  Implements copy job PromptController
 * @date   February 17, 2021
 *
 * (C) Copyright 2021 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "IPromptController.h"
#include "IJobManagerAlertProvider.h"
#include "DuneCdmAlerts_1_Autogen.h"
#include "ICopyJobTicket.h"
#include "IScanCommonPromptController.h"


namespace dune { namespace copy { namespace Jobs { namespace Copy {

using namespace dune::job;
using dune::copy::Jobs::Copy::Product;

class CopyJobPromptController : public IPromptController
{
  public:
    /**
     * @brief Recalculates the prompting needs
     *
     * Use this method only at the beginning of a scanning segment.
     *
     * @param[in] sourceOrigin true if the method is triggered by the user, false if the method is triggered
     * when the pipeline is done
     *
     * @return Prompt type to display. None if we don't want to display any prompt.
     */
    PromptType getNewPromptToDisplay(bool sourceOrigin, const std::string& pipelineSectionDoneName = "") override final;

    /**
     * @brief Display prompt on UI
     *
     * @return void
     */
    void displayPrompt(PromptType promptType, PromptCallback callback) override final;

    /**
     * @brief Cancel prompt ignoring job callback.
     *
     * @return void
     */
    void cancelPrompt() override final;

    /**
     * @brief Construct a new Copy Job Prompt Controller
     *
     * @param[in] ticket reference to an IJobTicket interface.
     * @param[in] jobManagerCdmAdapter Interface to the JobManagerCdmAdapter functionality.
     */
    CopyJobPromptController(std::shared_ptr<ICopyJobTicket> jobTicket,
                            dune::job::cdm::IJobManagerAlertProvider* jobManagerAlertProvider,
                            Product prePrintConfiguration, bool multiPageSupportedFromFlatbed);

    void onPromptResponse(dune::cdm::alert_1::Category category,
                          std::shared_ptr<dune::cdm::jobManagement_1::JobManagementAlertsActionDataT> alertAction);

    /**
     * @brief Get the Prompt object.
     * Only for testing purpose, this method is not in the interface and the framework will not use it.
     *
     * @return PromptType required prompt to post
     */
    PromptType getPrompt();

  private:
    std::shared_ptr<ICopyJobTicket>               jobTicket_{nullptr};
    dune::job::cdm::IJobManagerAlertProvider*     jobManagerAlertProvider_{nullptr};
    std::vector<PromptType>                       prompts_;
    PromptCallback                                jobCallback_{nullptr};
    uint32_t                                      alertID_{0};
    Product                                       prePrintConfiguration_{Product::HOME_PRO}; ///< Print configuration value
    bool                                          userRespondedToPrompt_{false};
    bool                                          multiPageSupportedFromFlatbed_{false};
    std::shared_ptr<dune::scan::Jobs::Scan::IScanCommonPromptController>   scanCommonPromptController_;
    std::string                                   idCardPromptSide_{"back"};
};

}}}}  // namespace dune::copy::Jobs::Copy
#endif
