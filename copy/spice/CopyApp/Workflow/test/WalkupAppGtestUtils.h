#ifndef WALKUPAPP_GTEST_UTILS_H
#define WALKUPAPP_GTEST_UTILS_H

////////////////////////////////////////////////////////////////////////////////
/**
 * @file WalkupAppGtestUtils.cpp
 * @brief Utitlity methods used by Send, Copy and Fax View GTests
 * @author hector.sanchez-gonzalez@hp.com
 * @date Nov 10th, 2020
 *
 * (C) Copyright 2020 HP Development Company, L.P.
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "com_hp_cdm_service_jobTicket_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_qmlRegistration_generated.h"
#include "com_hp_cdm_service_overlay_version_1_sharedTypes_overlay_models_generated.h"
#include "com_hp_cdm_service_overlay_version_1_sharedTypes_overlay_qmlRegistration_generated.h"
#include "com_hp_cdm_service_scan_version_1_models_generated.h"
#include "QQuickItem"
#include "SpiceWorkflowFixture.h"

using namespace dune::spice::jobTicket_1;
using namespace dune::spice::jobTicket_1::jobTicket;
using namespace dune::spice::overlay_1;
using namespace dune::spice::scan_1;

#include <memory>


namespace WalkupAppGtestUtils {

enum ScanStatusModelType
{
    MDF = 0,
    ADF,
    FLATBED
};

/**
 * @brief fillDefaultCopyJobTicketModel fills jobTicketModel received with default valid info
 *  for copy job ticket. If some different info is needed change it on client
 * @param jobTicketModel ticket model to be filled  with valid data
 */
void fillDefaultCopyJobTicketModel(std::shared_ptr<JobTicketModel> &jobTicketModel, QString ticketId);

/**
 * @brief fillScanStatusModel fills scanStatus model valid and needed info
 *  for scanStatusModel used on copy app
 * @param scanModelType determine type of model to be filled, depends of input path model model is different filled
 * @param scanStatusModel model to be fille with valid data
 * @return true if model were set, or false if model type is not valid and then model is not filled
 */
bool fillDefaultScanStatusModel(ScanStatusModelType scanModelType, std::shared_ptr<StatusModel> scanStatusModel);

/**
 * @brief fillDefaultScanModel fills ScanModel received with default valid info.
 *  If some different value is needed change it on client.
 * @param scanModel model to be filled with valid data
 */
void fillDefaultScanModel(ScanModel* scanModel, bool isMultipage = false);

/**
 * @brief fillDefaultPrintModel fills PrintModel received with default valid info.
 *  If some different value is needed change it on client.
 * @param printModel model to be filled with valid data
 */
void fillDefaultPrintModel(PrintModel* printModel);

/**
 * @brief fillDefaultPrfillDefaultImageModificationsintModel fills ImageModificationsModel received with default valid info.
 *  If some different value is needed change it on client.
 * @param printModel model to be filled with valid data
 */
void fillDefaultImageModifications( ImageModificationsModel* model );

/**
 * @brief compareSpiceButtonProperties executes EXPECTED_EQ for properties "visible" "enabled" and StrindId shown as text
 * @param spiceButton object to compare with params received
 * @param visible expected value for comparation with visible button property
 * @param enabled expected value for comparation with enabled button property
 * @param stringId expected textId for comparation with stringId button property
 */
void compareSpiceButtonProperties( QQuickItem* spiceButton, bool visible, bool enabled, QString stringId = "" );

/**
 * @brief compareButtonStringId executes EXPECTED_EQ for StrindId shown as text
 * @param spiceButton visual button to compare
 * @param stringId strind id expected in the button as "cCopy" naming format, for example
 */
void compareButtonStringId(QQuickItem* spiceButton, QString stringId);

/**
 * @brief Create a Instance Of Job Ticket object and set behaviour
 * @param mockIResourceStore the mock resources store
 * @param ticketId of jobticket
 */
void createInstanceOfJobTicket(MockIResourceStore* mockIResourceStore, QString ticketId);

/**
 * @brief register the fake resource of jobTicketModel
 * @param mockIResourceStore the mock resources store
 * @param ticketId of jobTicket
 */

void registerJobTicket(MockIResourceStore* mockIResourceStore, QString ticketId);

}  // namespace WalkupAppGtestUtils

#endif  // WALKUPAPP_GTEST_UTILS_H
