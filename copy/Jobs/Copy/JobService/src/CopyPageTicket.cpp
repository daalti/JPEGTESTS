////////////////////////////////////////////////////////////////////////////////
/**
 * @file  CopyPageTicket.cpp
 * @brief Copy Page Ticket
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "CopyPageTicket.h"

#include "common_debug.h"

#include "CopyPageTicket_TraceAutogen.h"



namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyPageTicket::CopyPageTicket(dune::framework::core::ThreadPool*                   threadPool /*= nullptr*/,
                               std::shared_ptr<dune::imaging::types::PageMetaInfoT> pageMetaInfo /*= nullptr*/)
    : PageTicket(pageMetaInfo),
      handler_{nullptr},
      pageIntent_{std::make_shared<dune::job::CopyPageIntent>()},
      pageResult_{std::make_shared<dune::job::CopyPageResult>()}
{
    CHECKPOINTD("CopyPageTicket::CopyPageTicket() threadPool: %p", threadPool);
    handler_ = std::make_shared<CopyPageTicketHandler>(*this, pageTicketChanged_);
}

std::unique_ptr<CopyPageTicket> CopyPageTicket::clone(bool resetResult) const
{
    CHECKPOINTD("CopyPageTicket::clone()");
    std::unique_ptr<CopyPageTicket> copyPageTicket{std::make_unique<CopyPageTicket>()};
    copyPageTicket->deserializeFromFb(*serializeToFb());

    copyPageTicket->setPageId(dune::framework::core::Uuid::createUuid());

    if (resetResult)
    {
        CHECKPOINTA("CopyPageTicket:: Rerun clone print Intents");
        copyPageTicket->getPageResult()->getPrintPageResult()->setCompletedCopies(0);
        copyPageTicket->getPageResult()->getPrintPageResult()->setEstimatedPrintTime(0);
        copyPageTicket->getPageResult()->getPrintPageResult()->setPrinted(false);
        if(printIntent_)
        {
            auto printIntents = std::static_pointer_cast<dune::print::engine::PrintIntents>(printIntent_);
            copyPageTicket->setPrintIntent(std::make_shared<dune::print::engine::PrintIntents>(*(printIntents.get())));
        }
        
    }

    return copyPageTicket;
}

std::shared_ptr<dune::job::IPageTicketHandler> CopyPageTicket::getHandler()
{
    return handler_;
}

std::unique_ptr<CopyPageTicketFbT> CopyPageTicket::serializeToFb() const
{
    CHECKPOINTD("CopyPageTicket::serializeToFb()");

    std::unique_ptr<CopyPageTicketFbT> ticketFbT{std::make_unique<CopyPageTicketFbT>()};
    ticketFbT->base = serializeBase();

    if(pageIntent_)
    {
        ticketFbT->intent = pageIntent_->serializeToFb();
    }
    if(pageResult_)
    {
        ticketFbT->result = pageResult_->serializeToFb();
    }
    return ticketFbT;
}

void CopyPageTicket::deserializeFromFb(const CopyPageTicketFbT& copyPageTicketFb)
{
    CHECKPOINTD("CopyPageTicket::deserializeFromFb()");
    deserializeBase(*copyPageTicketFb.base);

    if (pageIntent_ && copyPageTicketFb.intent)
    {
        pageIntent_->deserializeFromFb(*copyPageTicketFb.intent);
    }
    if (pageResult_ && copyPageTicketFb.result)
    {
        pageResult_->deserializeFromFb(*copyPageTicketFb.result);
    }

    handler_ = std::make_shared<CopyPageTicketHandler>(*this, pageTicketChanged_);
}

void CopyPageTicket::setPrintIntent(std::shared_ptr<dune::print::engine::PrintIntents> printIntent) 
{
    printIntent_ = printIntent;
}

void CopyPageTicket::setImagingIntent(std::shared_ptr<dune::imaging::types::IImagingIntent> imagingIntent)
{
    imagingIntent_ = imagingIntent;
}

void CopyPageTicket::setScanIntent(std::shared_ptr<dune::scan::types::ScanTicketStruct> scanIntent)
{
    scanIntent_ = scanIntent;
}

std::shared_ptr<dune::job::IIntent> CopyPageTicket::getIntent(dune::job::IntentType intentType) const
{
    //Return the proper intent depending of the intent type
    switch(intentType)
    {
        case dune::job::IntentType::PRINT:
            CHECKPOINTC("CopyPageTicket::getIntent  Get print intent");
            return printIntent_;

        case dune::job::IntentType::IMAGING:
            CHECKPOINTC("CopyPageTicket::getIntent Get color intent");
            return imagingIntent_;

        case dune::job::IntentType::SCAN:
            CHECKPOINTC("CopyPageTicket::getIntent Get scan intent");
            return scanIntent_;
        //default return is needed to avoid return-type compiler error
        default:
            return nullptr;
    }
}

}}}}  // namespace dune::copy::Jobs
