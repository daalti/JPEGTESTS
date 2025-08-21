#ifndef DUNE_COPY_JOBS_DETAILS_PROVIDER_H
#define DUNE_COPY_JOBS_DETAILS_PROVIDER_H

////////////////////////////////////////////////////////////////////////////////
/**
 * @file  CopyJobDetailsProvider.h
 * @brief Provider of details of a copy job
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "ICopyJobService.h"
#include "IJobDetailsProvider.h"
#include "IPageTicket.h"
#include "IScanPipeline.h"
#include "StatsHelper.h"
#include "IDateTime.h"

namespace dune { namespace job {
class IJobTicketResourceManager;
}}  // namespace dune::job


namespace dune { namespace copy { namespace Jobs { namespace Copy {

class ICopyPageTicket;

using PrintInfoDetails = dune::job::StatsDetails::PrintInfoDetails;
using PrintSettingsDetails = PrintInfoDetails::PrintSettingsDetails;
using ISettings = dune::print::engine::ISettings;
using MediaRequestedDetails = PrintInfoDetails::MediaRequestedDetails;
using MediaInputDetails = PrintInfoDetails::MediaInputDetails;
using JobInfoDetails = dune::job::StatsDetails::JobInfoDetails;
using PrintedSheetInfoDetails =  PrintInfoDetails::SheetSetDetails;
using StatsInfoDetails = dune::job::StatsDetails::StatsInfoDetails;
using IScanPipeline = dune::scan::Jobs::Scan::IScanPipeline;
using IDateTime = dune::framework::core::time::IDateTime;

/**
 * @brief Provider of details of a copy job
 */
class CopyJobDetailsProvider : public dune::job::IJobDetailsProvider
{
  public:
    /**
     * @brief Construct a new Copy Job Details Provider object
     *
     * @param jobService Service associated to COPY jobs
     * @param jobTicketResourceManager Manager of JobTickets
     */
    CopyJobDetailsProvider(ICopyJobService* jobService, dune::job::IJobTicketResourceManager* jobTicketResourceManager,
                           ISettings* interfaceISettings, IScanPipeline* scanPipeline, IDateTime* dateTime);

    /**
     * @name IJobDetailsProvider methods.
     * @{
     */
    std::pair<bool, StatsInfoDetails> populateJobDetails(const Uuid& jobTicketUuid, dune::security::ac::IAccessControl* accessControl) override;
    PagesDetails populatePagesDetails(const Uuid& jobTicketUuid) const override;
    PageDetails  populatePageDetails(const Uuid& jobTicketUuid, const Uuid& pageUuid) const override;
    /** @} */

  protected:
    /**
     * @brief Set the Stats Helper object
     */
    void setStatsHelper(std::shared_ptr<dune::print::JobAccounting::StatsHelper> helper);

  private:
    /**
     * @brief Get the Copy Job Ticket loading to cache if needed
     *
     * @param jobTicketUuid Uuid of the job ticket
     * @return std::shared_ptr<ICopyJobTicket> Copy Job Ticket
     */
    std::shared_ptr<ICopyJobTicket> getCopyJobTicket(const Uuid jobTicketUuid) const;

    /**
     * @brief Generates the job details with basic info
     *
     * @param jobTicketUuid Uuid of the job ticket
     * @return StatsInfoDetails the job details with basic info
     */
    static StatsInfoDetails generateEmptyJobDetails(const Uuid& jobTicketUuid);

    /**
     * @brief Generates the pages details with basic info
     *
     * @return PagesDetails the pages details with basic info
     */
    static PagesDetails generateEmptyPagesDetails();

    /**
     * @brief Generates the page details with basic info
     *
     * @param pageId Uuid of the page
     * @return PageDetails the page details with basic info
     */
    static PageDetails generateEmptyPageDetails(const Uuid& pageId);

    /**
     * @brief Generates the job details of a copy job through its copy job ticket
     *
     * @param copyJobTicket copy Job Ticket
     * @return StatsInfoDetails job details of a COPY job
     */
    StatsInfoDetails generateJobDetails(ICopyJobTicket& copyJobTicket, dune::security::ac::IAccessControl* accessControl );

    /**
     * @brief Generates the pages details of a copy job through its Copy job ticket
     *
     * @param copyJobTicket Copy Job Ticket
     * @return PagesDetails page details of a copy job
     */
    static PagesDetails generatePagesDetails(ICopyJobTicket& copyJobTicket);

    /**
     * @brief Generates the page details of a copy job through its page ticket
     *
     * @param pageTicket Page Ticket
     * @param jobId id of the job
     * @return PageDetails page details of a copy job
     */
    static PageDetails generatePageDetails(const ICopyPageTicket& pageTicket, const Uuid& jobId);

    /**
     * @brief Map a Preview to CDM structure
     *
     * @param preview Preview to be converted
     * @param jobId Id of the job
     * @param pageId Id of the Page
     * @param highResPreview indicates if is a high resolution preview
     * @param layerName Layer Names (if has)
     * @return dune::cdm::jobManagement_1::ImageDescriptorTable CDM Preview
     */
    static dune::cdm::jobManagement_1::ImageDescriptorTable mapToCdm(const dune::job::IPageTicket::Preview& preview,
                                                                     const Uuid& jobId, const Uuid& pageId,
                                                                     bool highResPreview, const std::string& layerName = "");

    /**
     * @brief Map a Layer to CDM structure
     *
     * @param layer Layer to be converted
     * @param jobId Id of the job
     * @param pageId Id of the Page
     * @return page::layers::ItemTable CDM Layer
     */
    static dune::cdm::jobManagement_1::page::layers::ItemTable mapToCdm(const dune::job::IPageTicket::Layer& layer,
                                                                        const Uuid& jobId, const Uuid& pageId);

    /**
     * @brief Generate a Preview Id
     *
     * @param jobId Id of the job
     * @param pageId Id of the page
     * @param highResPreview True if high resolution preview, false if low resolution preview
     * @param layerName Layer Names (if has)
     * @return std::string Preview Id
     */
    static std::string generatePreviewId(const Uuid& jobId, const Uuid& pageId, bool highResPreview,
                                         const std::string& layerName = "");

    /**
     * @brief Generates the Printed Sheet info from the Print Job ticket
     *
     * @param copyJobIntent Copy Job intent
     * @return PrintedSheetInfoDetails Printed Sheet info from the Print Job ticket
     */
    PrintedSheetInfoDetails generatePrintedSheetInfo(const std::shared_ptr<ICopyJobIntent> copyJobIntent);

    /**
     * @brief Generates the Print Settings from the Print Job ticket
     *
     * @param copyJobIntent Copy Job intent
     * @return PrintSettingsDetails Print Settings from the Print Job ticket
     */
    PrintSettingsDetails generatePrintSettings(const std::shared_ptr<ICopyJobIntent> copyJobIntent);

    /**
     * @brief Get the Media Requested
     *
     * @param copyJobIntent Copy Job intent
     * @return MediaRequestedDetails media requested
     */
    MediaRequestedDetails getMediaRequested(const std::shared_ptr<ICopyJobIntent> copyJobIntent);

    /**
     * @brief Transform to string the LayerId enum
     *
     * @param layerId layerId to be translated
     * @return std::string LayerId to string
     */
    static std::string layerIdToString(dune::job::LayerId layerId);

    ICopyJobService*                     jobService_;                ///< Service associated to copy jobs
    dune::job::IJobTicketResourceManager* jobTicketResourceManager_;  ///< Manager of JobTickets
    ISettings*                            interfaceISettings_{nullptr};
    IScanPipeline*                        scanPipeline_{nullptr};

    std::shared_ptr<dune::print::JobAccounting::StatsHelper> statsHelper_;  ///< pointer to the statsHelper API
    IDateTime* dateTime_{nullptr};
};

}}}}  // namespace dune::copy::Jobs

#endif  // DUNE_COPY_JOBS_DETAILS_PROVIDER_H
