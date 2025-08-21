////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyTicketGtestUtilities.h
 * @brief  Utilities for CopyJobTicket unit tests
 *
 * (C) Sampleright 2022 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////
#include "CopyJobTicket.h"

using namespace dune::copy::Jobs::Copy;
using namespace dune::job;
using namespace dune::imaging::types;

class CopyTicketsUtilities
{
  public:
    static std::unique_ptr<CopyJobTicket>  createDefaultJobTicket();
    static std::unique_ptr<CopyPageTicket> createDefaultPageTicket();

    static void setAndVerifyBaseJobTicket(IJobTicket& ticket);
    static void setAndVerifyBasePageTicket(IPageTicket& pageTicket);
    static void setAndVerifyCopyJobIntent(ICopyJobIntent& jobIntent);
    static void setAndVerifyCopyJobResult(ICopyJobResult& jobResult);
    static void setAndVerifyCopyPageTicket(ICopyJobTicket& ticket);

    static void compareCopyJobTicket(ICopyJobTicket& expectedTicket, ICopyJobTicket& ticket);
    static void compareCopyJobResult(ICopyJobResult& expectedJobResult, ICopyJobResult& jobResult);
    static void compareCopyPageTicket(const ICopyPageTicket& expectedTicket, const ICopyPageTicket& ticket);
    static void compareBaseJobTickets(const IJobTicket& expectedTicket, const IJobTicket& ticket);
    static void compareBasePageTickets(const IPageTicket& expectedTicket, const IPageTicket& ticket);
};

