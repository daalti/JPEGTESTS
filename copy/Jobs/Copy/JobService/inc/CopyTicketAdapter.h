/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_TICKETADAPTER_H
#define DUNE_COPY_JOBS_COPY_TICKETADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyTicketAdapter.h
 * @date   Tue, 06 Aug 2019 12:14:22 +0530
 * @brief  Adapter class between Job Management and copy to serialize/deserialize
 *         information of ticket.
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ConstraintsGroup.h"
#include "ICopyJobTicket.h"
#include "ITicketAdapter.h"
#include "JobServiceFactory.h"
#include "IJobConstraints.h"
#include "ICopyJobDynamicConstraintRules.h"
#include "ICopyAdapter.h"
#include "ILocaleProvider.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using dune::framework::core::Uuid;
using dune::job::IJobService;
using dune::job::TicketAdapterBase;
using namespace dune::framework::component;
using dune::ws::cdm::ErrorItemT;

/**
 * @brief
 *
 */
class CopyTicketAdapter : public TicketAdapterBase<ICopyJobTicket>
{
public:

    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> getConstraints() override;
    
    CopyTicketAdapter(std::shared_ptr<ICopyJobTicket>&              copyJobTicket,
                  dune::job::JobServiceFactory<ICopyJobTicket>* jobService);

    // Easy buffer API
    bool supportsEasyBuffers() const override { return true; }
    std::shared_ptr<JobTicketTable> serializeIntoTable() override;
    std::tuple<bool, dune::ws::cdm::ErrorItemT> deserializeFromTable(
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable,
                                                   bool& isTicketModified) override;
    std::unique_ptr<dune::cdm::jobTicket_1::PrintTable> serializePrintInfoTable(std::shared_ptr<ICopyJobIntent> intent);
    std::tuple<bool, dune::ws::cdm::ErrorItemT>         deserializePrintInfoTable(
                const dune::cdm::jobTicket_1::PrintTable* printDataTable, std::shared_ptr<ICopyJobIntent>&& intent,
                CopyTicketAdapter* ticketAdapter, bool& isTicketModified, bool skipValidationErrorReport = false,
                std::shared_ptr<ICopyJobIntent> defaultJobIntent = nullptr);

    std::unique_ptr<dune::cdm::jobTicket_1::print::SheetsPerFoldSetTable> serializeSheetsPerFoldSet(std::shared_ptr<ICopyJobIntent> intent);                                                

    ~CopyTicketAdapter();

    inline void setCopyJobConstraintsHelper(dune::copy::Jobs::Copy::IJobConstraints* helper) { copyJobConstraintsHelper_ = helper; }
    inline dune::copy::Jobs::Copy::IJobConstraints* getCopyJobConstraintsHelper(void) const { return copyJobConstraintsHelper_; }
    inline void setCopyDynamicConstraintsHelper(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules* helper) { copyDynamicConstraintsHelper_ = helper; }
    inline dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules* getCopyDynamicConstraintsHelper(void) const { return copyDynamicConstraintsHelper_; }
    inline void setCopyConfigurationHelper(dune::copy::cdm::ICopyAdapter* helper) { copyConfigurationHelper_ = helper; }
    inline dune::copy::cdm::ICopyAdapter* getCopyConfigurationHelper(void) const { return copyConfigurationHelper_; }
    bool supportsProperty(const std::string& propertyName) override;

    /**
     * @brief Setter for staticConstrainsAreCached_ private variable.
     *
     * @param val the value to be set.
     */
    void setStaticConstrainsAreCached(const bool val);

    /**
     * @brief Setter for validateTicketOnSerialization_ private variable.
     *
     * @param val the value to be set.
     */
    void setValidateTicketOnSerialization(const bool value);
    
    /**
     * @brief Setter for localeProvider_ private variable.
     *
     * @param localeProvider the value to be set.
     */
    void setLocaleProvider(dune::localization::ILocaleProvider* localeProvider);
    
    dune::imaging::types::ColorMode getFallbackColorMode( std::vector<dune::imaging::types::ColorMode> options);

    std::tuple<bool, dune::ws::cdm::ErrorItemT> deserializeFromTableWithRules(
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& isTicketModified,
        bool skipValidationErrorReport = false, std::shared_ptr<ICopyJobIntent> defaultJobIntent = nullptr);

  private:
    /**
     * @brief Method to update current dynamic constraints
     * @return std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>
     */
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> updateConstraints(
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable = nullptr);

    /**
     * @brief Internal method that will deserialize updatedJobTicketTable in current job ticket
     * @param updatedJobTicketTable job ticket table received from cdm
     * @param isTicketModified parameter as reference to notify change
     * @return std::tuple<bool, dune::ws::cdm::ErrorItemT> error result if apply
     */
    std::tuple<bool, dune::ws::cdm::ErrorItemT> internalDeserializeFromTable(
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& isTicketModified,
        bool skipValidationErrorReport = false, std::shared_ptr<ICopyJobIntent> defaultJobIntent = nullptr);

    friend class ForceSets;

	dune::copy::Jobs::Copy::IJobConstraints* copyJobConstraintsHelper_{nullptr};
	dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules* copyDynamicConstraintsHelper_{ nullptr};
	dune::copy::cdm::ICopyAdapter* copyConfigurationHelper_{ nullptr };
	std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup_{nullptr};
	std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> lastConstraintsGroup_{nullptr};

	bool staticConstrainsAreCached_{false};
    /**
     * @brief Variable to notify that ticket will be checked in serialization method
     */
    bool validateTicketOnSerialization_{false};
	dune::localization::ILocaleProvider* localeProvider_{nullptr};
};

}}}}  // namespace dune::copy::Jobs::Copy
#endif