#include "CopyAppController.h"

#include "CopyInitView.h"
#include "CopyStartView.h"
#include "IResourceStoreFuture.h"
#include "ResourceStoreIdentifiers_generated.h"
#include "com_hp_cdm_service_jobManagement_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_models_generated.h"

namespace dune { namespace copy { namespace spice {
using namespace dune::spice::core;
using namespace dune::spice::jobTicket_1;
using namespace dune::spice::jobTicket_1::jobTicket;

CopyAppController::CopyAppController(IApplicationEngine *applicationEngine, QObject *parent)
    : ISpiceController(applicationEngine, parent), noOfCopies_(0)
{
}

CopyAppController::~CopyAppController()
{
}

void CopyAppController::copyInitialize()
{
    applicationEngine_->getSpiceStack()->push(
        qobject_cast<SpiceView *>(new CopyInitView(SpiceView::ViewPriority::App, this)));
}
void CopyAppController::startCopy()
{
    applicationEngine_->getSpiceStack()->push(
        qobject_cast<SpiceView *>(new CopyStartView(SpiceView::ViewPriority::App, this)));
    auto            resourceStore = applicationEngine_->getResourceStore();
    JobTicketModel *ticketModel = static_cast<JobTicketModel *>(
        resourceStore->createInstance(ResourceStoreTypes::Type::JOB_TICKET_1_JOB_TICKET)->getData());

    ticketModel->setTicketReference("defaults/copy");

    IResourceStoreFuture *future = resourceStore->create("/cdm/jobTicket/v1/tickets", ticketModel);
    connect(future, &IResourceStoreFuture::resolved, [](IResourceStoreFuture *futureRet) {
        QString tick = static_cast<JobTicketModel *>(futureRet->get()->getData())->getTicketId();
    });
    connect(future, &IResourceStoreFuture::rejected, []() {});
}

quint32 CopyAppController::getDefaultCopies()
{
    // TO DO :put the logic to get Default no of copies for the device from Copy Setting CDM service
    // currently hardcoding
    noOfCopies_ = 1;
    return noOfCopies_;
}

void CopyAppController::incrementCopies()
{
    // TO DO : get constraint on copies, check if noOfCopies more than max before setting
    // noOfCopies_ = (noOfCopies_ >= 9) ? 9 : noOfCopies_++;
}

void CopyAppController::decrementCopies()
{
    // TO DO : get constraint on copies, check if noOfCopies less than min before setting
    // noOfCopies_ = (noOfCopies_ <= 1) ? 1 : noOfCopies_--;
}

void CopyAppController::cancelCopy()
{
    // TO Do: provide the resource store interfae to cancel the job
}
}}}  // namespace dune::copy::spice
