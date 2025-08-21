////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyTicketGtestUtilities.cpp
 * @brief  Utilities for CopyJobTicket unit tests
 *
 * (C) Sampleright 2022 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "CopyTicketGtestUtilities.h"
#include "ConstraintsGroup.h"
using namespace dune::copy::Jobs::Copy;
using namespace dune::job;
using namespace dune::imaging::types;

std::unique_ptr<CopyJobTicket> CopyTicketsUtilities::createDefaultJobTicket()
{
    std::unique_ptr<CopyJobTicket> ticket{std::make_unique<CopyJobTicket>()};

    // Base job ticket values
    setAndVerifyBaseJobTicket(*ticket);

    // Set and verify Intent
    std::shared_ptr<ICopyJobIntent> intent = ticket->getIntent();
    setAndVerifyCopyJobIntent(*intent);

    // Set and verify Result
    setAndVerifyCopyJobResult(*ticket->getResult());

    // Set and verify pages
    setAndVerifyCopyPageTicket(*ticket);

    // Validate job ticket handler
    EXPECT_EQ(JobType::COPY, ticket->getType());
    EXPECT_NE(nullptr, ticket->getHandler());

    return ticket;
}

std::unique_ptr<CopyPageTicket> CopyTicketsUtilities::createDefaultPageTicket()
{
    std::unique_ptr<CopyPageTicket> pageTicket{std::make_unique<CopyPageTicket>()};

    // Set and verify page Id
    EXPECT_EQ(Uuid(), pageTicket->getPageId());
    pageTicket->setPageId(Uuid("2a6657a7-9a32-4da2-8ee6-44543d1c87ef"));
    EXPECT_EQ(Uuid("2a6657a7-9a32-4da2-8ee6-44543d1c87ef"), pageTicket->getPageId());
    EXPECT_EQ(0, pageTicket->getPreviewProgress());

    // Set and verify base page ticket
    setAndVerifyBasePageTicket(*pageTicket);

    // Return Ticket
    return pageTicket;
}

void CopyTicketsUtilities::setAndVerifyBaseJobTicket(IJobTicket& ticket)
{
    ticket.getJobTicketChanged();

    

    EXPECT_EQ(ticket.getJobId(), Uuid{});
    ticket.setJobId(Uuid("2a6657a7-9a32-4da2-8ee6-44543d1c87ef"));
    EXPECT_EQ(ticket.getJobId(), Uuid{"2a6657a7-9a32-4da2-8ee6-44543d1c87ef"});

    EXPECT_EQ(ticket.getJobName(), "");
    ticket.setJobName("JobName");
    EXPECT_EQ(ticket.getJobName(), "JobName");

    EXPECT_EQ(ticket.getJobServiceId(), JobServiceId::UNDEFINED);
    ticket.setJobServiceId(JobServiceId::COPY);
    EXPECT_EQ(ticket.getJobServiceId(), JobServiceId::COPY);

    
}

void CopyTicketsUtilities::setAndVerifyBasePageTicket(IPageTicket& pageTicket)
{
    EXPECT_EQ(MediaSizeId::ANY, pageTicket.getMediaSize());
    pageTicket.setMediaSize(MediaSizeId::A0);
    EXPECT_EQ(MediaSizeId::A0, pageTicket.getMediaSize());

    // Get and compare Layers
    EXPECT_FALSE(pageTicket.hasLayer());

    IPageTicket::Layer expectedLayer{};
    expectedLayer.layerId = LayerId::CMYK_FRONT;
    expectedLayer.progress = 100;
    expectedLayer.highResPreview = IPageTicket::Preview{"HighResPath2", 200, 200, 200, 100};
    expectedLayer.lowResPreview = IPageTicket::Preview{"LowResPreview2", 200, 200, 100, 100};
    pageTicket.setLayer(expectedLayer);

    EXPECT_TRUE(pageTicket.hasLayer());
    const auto& layer{pageTicket.getLayer(expectedLayer.layerId)};
    EXPECT_EQ(expectedLayer.layerId, layer.layerId);
    EXPECT_EQ(expectedLayer.progress, layer.progress);
    EXPECT_EQ(expectedLayer.highResPreview.path, layer.highResPreview.path);
    EXPECT_EQ(expectedLayer.highResPreview.widthPx, layer.highResPreview.widthPx);
    EXPECT_EQ(expectedLayer.highResPreview.heightPx, layer.highResPreview.heightPx);
    EXPECT_EQ(expectedLayer.highResPreview.resolution, layer.highResPreview.resolution);
    EXPECT_EQ(expectedLayer.lowResPreview.path, layer.lowResPreview.path);
    EXPECT_EQ(expectedLayer.lowResPreview.widthPx, layer.lowResPreview.widthPx);
    EXPECT_EQ(expectedLayer.lowResPreview.heightPx, layer.lowResPreview.heightPx);
    EXPECT_EQ(expectedLayer.lowResPreview.resolution, layer.lowResPreview.resolution);


    // Get and compare HighResPreview
    EXPECT_TRUE(pageTicket.getHighResPreview().path.empty());

    IPageTicket::Preview expectedHighResPreview;
    expectedHighResPreview.path = "ExpectedHighResPreview";
    expectedHighResPreview.widthPx = 24;
    expectedHighResPreview.heightPx = 48;
    expectedHighResPreview.progress = 100;
    expectedHighResPreview.resolution = 200;
    pageTicket.setHighResPreview(expectedHighResPreview);

    IPageTicket::Preview highResPreview = pageTicket.getHighResPreview();
    EXPECT_EQ(expectedHighResPreview.path, highResPreview.path);
    EXPECT_EQ(expectedHighResPreview.widthPx, highResPreview.widthPx);
    EXPECT_EQ(expectedHighResPreview.heightPx, highResPreview.heightPx);
    EXPECT_EQ(expectedHighResPreview.resolution, highResPreview.resolution);

    // Get and compare LowResPreview
    EXPECT_TRUE(pageTicket.getLowResPreview().path.empty());

    IPageTicket::Preview expectedLowResPreview;
    expectedLowResPreview.path = "ExpectedLowResPreview";
    expectedLowResPreview.widthPx = 24;
    expectedLowResPreview.heightPx = 48;
    expectedLowResPreview.progress = 100;
    expectedLowResPreview.resolution = 100;
    pageTicket.setLowResPreview(expectedLowResPreview);

    IPageTicket::Preview lowResPreview = pageTicket.getLowResPreview();
    EXPECT_EQ(expectedLowResPreview.path, lowResPreview.path);
    EXPECT_EQ(expectedLowResPreview.widthPx, lowResPreview.widthPx);
    EXPECT_EQ(expectedLowResPreview.heightPx, lowResPreview.heightPx);
    EXPECT_EQ(expectedLowResPreview.resolution, lowResPreview.resolution);
}

void CopyTicketsUtilities::setAndVerifyCopyJobIntent(ICopyJobIntent& jobIntent)
{
    //TODO use this method to set and verify the copy job intent
    
}

void CopyTicketsUtilities::setAndVerifyCopyJobResult(ICopyJobResult& jobResult)
{
    EXPECT_EQ(0, jobResult.getCompletedImpressions());
    jobResult.setCompletedImpressions(1);
    EXPECT_EQ(1, jobResult.getCompletedImpressions());

    EXPECT_EQ(0, jobResult.getCompletedCopies());
    jobResult.setCompletedCopies(2);
    EXPECT_EQ(2, jobResult.getCompletedCopies());
}

void CopyTicketsUtilities::setAndVerifyCopyPageTicket(ICopyJobTicket& ticket)
{
    EXPECT_EQ(0, ticket.getPagesIds(PageOrder::CREATION).size());

    // Add Page
    Uuid pageId(Uuid::createUuid());
    EXPECT_NE(nullptr, ticket.addPage(pageId));

    // Get and verify added page
    std::shared_ptr<ICopyPageTicket> pageTicket{ticket.getCopyPageTicket(pageId)};
    EXPECT_NE(nullptr, pageTicket);

    // Set and verify page
    EXPECT_EQ(pageId, pageTicket->getPageId());
    EXPECT_EQ(0, pageTicket->getPreviewProgress());

    // Set and verify base page ticket
    setAndVerifyBasePageTicket(*pageTicket);
}

void CopyTicketsUtilities::compareCopyJobTicket(ICopyJobTicket& expectedTicket, ICopyJobTicket& ticket)
{
    // Compare job ticket data
    compareBaseJobTickets(expectedTicket, ticket);
    compareCopyJobResult(*expectedTicket.getResult(), *ticket.getResult());

    // Compare page tickets data
    auto pagesIds{expectedTicket.getPagesIds(PageOrder::CREATION)};
    for (const Uuid& pageId : pagesIds)
    {
        compareCopyPageTicket(*expectedTicket.getCopyPageTicket(pageId),
                                *ticket.getCopyPageTicket(pageId));
    }
}

void CopyTicketsUtilities::compareCopyJobResult(ICopyJobResult& expectedJobResult, ICopyJobResult& jobResult)
{
    EXPECT_EQ(expectedJobResult.getCompletedCopies(), jobResult.getCompletedCopies());
    EXPECT_EQ(expectedJobResult.getCompletedImpressions(), jobResult.getCompletedImpressions());
    EXPECT_EQ(expectedJobResult.areAllPagesDiscovered(), jobResult.areAllPagesDiscovered());
}

void CopyTicketsUtilities::compareCopyPageTicket(const ICopyPageTicket& expectedTicket,
                                                   const ICopyPageTicket& ticket)
{
    compareBasePageTickets(expectedTicket, ticket);
}

void CopyTicketsUtilities::compareBaseJobTickets(const IJobTicket& expectedTicket, const IJobTicket& ticket)
{
    EXPECT_EQ(expectedTicket.getJobId(), ticket.getJobId());
    EXPECT_EQ(expectedTicket.getJobName(), ticket.getJobName());
}

void CopyTicketsUtilities::compareBasePageTickets(const IPageTicket& expectedTicket, const IPageTicket& ticket)
{
    EXPECT_EQ(expectedTicket.getMediaSize(), ticket.getMediaSize());

    IPageTicket::Preview expectedHighResPreview = expectedTicket.getHighResPreview();
    IPageTicket::Preview highResPreview = ticket.getHighResPreview();
    EXPECT_EQ(expectedHighResPreview.path, highResPreview.path);
    EXPECT_EQ(expectedHighResPreview.widthPx, highResPreview.widthPx);
    EXPECT_EQ(expectedHighResPreview.heightPx, highResPreview.heightPx);
    EXPECT_EQ(expectedHighResPreview.resolution, highResPreview.resolution);

    IPageTicket::Preview expectedLowResPreview = expectedTicket.getLowResPreview();
    IPageTicket::Preview lowResPreview = ticket.getLowResPreview();
    EXPECT_EQ(expectedLowResPreview.path, lowResPreview.path);
    EXPECT_EQ(expectedLowResPreview.widthPx, lowResPreview.widthPx);
    EXPECT_EQ(expectedLowResPreview.heightPx, lowResPreview.heightPx);
    EXPECT_EQ(expectedLowResPreview.resolution, lowResPreview.resolution);

    EXPECT_EQ(expectedTicket.hasLayer(), ticket.hasLayer());
    std::vector<LayerId> layerIds{expectedTicket.getLayersIds()};
    for (const LayerId& layerId : layerIds)
    {
        const IPageTicket::Layer& expectedLayer{expectedTicket.getLayer(layerId)};
        const IPageTicket::Layer& layer{ticket.getLayer(layerId)};
        EXPECT_EQ(expectedLayer.layerId, layer.layerId);
        EXPECT_EQ(expectedLayer.progress, layer.progress);
        EXPECT_EQ(expectedLayer.highResPreview.path, layer.highResPreview.path);
        EXPECT_EQ(expectedLayer.highResPreview.widthPx, layer.highResPreview.widthPx);
        EXPECT_EQ(expectedLayer.highResPreview.heightPx, layer.highResPreview.heightPx);
        EXPECT_EQ(expectedLayer.highResPreview.resolution, layer.highResPreview.resolution);
        EXPECT_EQ(expectedLayer.lowResPreview.path, layer.lowResPreview.path);
        EXPECT_EQ(expectedLayer.lowResPreview.widthPx, layer.lowResPreview.widthPx);
        EXPECT_EQ(expectedLayer.lowResPreview.heightPx, layer.lowResPreview.heightPx);
        EXPECT_EQ(expectedLayer.lowResPreview.resolution, layer.lowResPreview.resolution);
    }
}
