////////////////////////////////////////////////////////////////////////////////
/**
 * @file WalkupAppGtestUtils.cpp
 * @brief Utitlity methods used by Send, Copy and Fax View GTests
 * @author hector.sanchez-gonzalez@hp.com
 * @date Nov 10th, 2021
 *
 * (C) Copyright 2020 HP Development Company, L.P.
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "WalkupAppGtestUtils.h"
#include "gtest/gtest.h"
#include "com_hp_cdm_service_jobTicket_version_1_models_generated.h"
#include "MockIResourceStore.h"

void WalkupAppGtestUtils::fillDefaultCopyJobTicketModel(std::shared_ptr<JobTicketModel> &jobTicketModel, QString ticketId)
{
    assert( jobTicketModel != nullptr );

    jobTicketModel->setTicketId(ticketId);

    DestModel *dstModel = new DestModel();
    SrcModel  *srcModel = new SrcModel();

    PipelineOptionsModel *pipelineOptionsModel = new PipelineOptionsModel();

    ScalingModel* scalingModel = new ScalingModel();
    scalingModel->setYScalePercent(100);
    scalingModel->setXScalePercent(100);
    scalingModel->setScaleToFitEnabled(dune::spice::glossary_1::FeatureEnabled::FeatureEnabled::true_);
    pipelineOptionsModel->setScaling(scalingModel);

    ScanModel* scanModel = new ScanModel();
    // Copy is always multipage so 2nd param is always true
    fillDefaultScanModel( scanModel, true );

    PrintModel* printModel = new PrintModel();
    fillDefaultPrintModel(printModel);

    ImageModificationsModel *imageModificationsModel = new ImageModificationsModel();
    fillDefaultImageModifications(imageModificationsModel);

    WatermarkDetailsModel* watermarkDetailsModel = new WatermarkDetailsModel();
    pipelineOptionsModel->setWatermark( watermarkDetailsModel );

    ScanStampLocationModel* scanStampTopLeftModel = new ScanStampLocationModel();
    scanStampTopLeftModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::topLeft);
    ScanStampLocationModel* scanStampTopCenterModel = new ScanStampLocationModel();
    scanStampTopCenterModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::topCenter);
    ScanStampLocationModel* scanStampTopRightModel = new ScanStampLocationModel();
    scanStampTopRightModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::topRight);
    ScanStampLocationModel* scanStampBottomLeftModel = new ScanStampLocationModel();
    scanStampBottomLeftModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::bottomLeft);
    ScanStampLocationModel* scanStampBottomCenterModel = new ScanStampLocationModel();
    scanStampBottomCenterModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::bottomCenter);
    ScanStampLocationModel* scanStampBottomRightModel = new ScanStampLocationModel();
    scanStampBottomRightModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::bottomRight);

    pipelineOptionsModel->setStampTopLeft(scanStampTopLeftModel);
    pipelineOptionsModel->setStampTopCenter(scanStampTopCenterModel);
    pipelineOptionsModel->setStampTopRight(scanStampTopRightModel);
    pipelineOptionsModel->setStampBottomLeft(scanStampBottomLeftModel);
    pipelineOptionsModel->setStampBottomCenter(scanStampBottomCenterModel);
    pipelineOptionsModel->setStampBottomRight(scanStampBottomRightModel);

    srcModel->setScan(scanModel);
    dstModel->setPrint(printModel);
    pipelineOptionsModel->setImageModifications( imageModificationsModel );

    jobTicketModel->setDest(dstModel);
    jobTicketModel->setSrc(srcModel);
    jobTicketModel->setPipelineOptions(pipelineOptionsModel);

}

void WalkupAppGtestUtils::fillDefaultScanModel(ScanModel* scanModel, bool isMultipage)
{
    assert( scanModel != nullptr );

    scanModel->setColorMode(dune::spice::jobTicket_1::ColorModes::ColorModes::autoDetect);
    scanModel->setPlexMode(dune::spice::glossary_1::PlexMode::PlexMode::simplex);
    scanModel->setMediaSize(dune::spice::glossary_1::MediaSize::MediaSize::iso_a4_210x297mm);
    scanModel->setResolution(dune::spice::jobTicket_1::Resolutions::Resolutions::e300Dpi);

    if (isMultipage)
    {
        scanModel->setScanCaptureMode(dune::spice::jobTicket_1::ScanCaptureMode::ScanCaptureMode::jobBuild);
    }
}

void WalkupAppGtestUtils::fillDefaultPrintModel(PrintModel* printModel)
{
    assert( printModel != nullptr );

    printModel->setCopies(1);
    printModel->setMediaSource(dune::spice::glossary_1::MediaSourceId::MediaSourceId::auto_);
    printModel->setPlexMode(dune::spice::glossary_1::PlexMode::PlexMode::simplex);
    printModel->setCollate(dune::spice::jobTicket_1::CollateModes::CollateModes::collated);
    printModel->setMediaType(dune::spice::glossary_1::MediaType::MediaType::custom);
}

void WalkupAppGtestUtils::fillDefaultImageModifications( ImageModificationsModel* model )
{
    assert( model != nullptr );

    model->setSharpness(1);
    model->setBackgroundCleanup(2);
    model->setExposure(5);
    model->setContrast(1);
    model->setBlankPageSuppressionEnabled( dune::spice::glossary_1::FeatureEnabled::FeatureEnabled::false_ );
    model->setPagesPerSheet( dune::spice::jobTicket_1::PagesPerSheet::PagesPerSheet::oneUp );
}

bool WalkupAppGtestUtils::fillDefaultScanStatusModel(ScanStatusModelType scanModelType, std::shared_ptr<StatusModel> scanStatusModel)
{
    assert( scanStatusModel != nullptr );

    if( scanModelType == MDF )
    {
        MdfModel*     mdfModel = new MdfModel();
        mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::loaded);

        scanStatusModel->setMdf(mdfModel);
    }
    else if( scanModelType == ADF )
    {
        AdfModel*     adfModel = new AdfModel();

        scanStatusModel->setAdf(adfModel);

    }
    else if( scanModelType == FLATBED )
    {
        FlatbedModel* flatbedModel = new FlatbedModel();

        scanStatusModel->setFlatbed(flatbedModel);
    }
    else
    {
        return false;
    }

    return true;
}

void WalkupAppGtestUtils::compareButtonStringId(QQuickItem* spiceButton, QString stringId)
{
    auto nameTextObjectVar = spiceButton->property("textObject");
    ASSERT_TRUE(nameTextObjectVar.isValid());
    ASSERT_TRUE(!nameTextObjectVar.isNull());

    auto nameTextObject = nameTextObjectVar.value<QObject*>();
    ASSERT_NE(nameTextObject, nullptr);

    EXPECT_EQ(nameTextObject->property("text"), QVariant(stringId));
}

void WalkupAppGtestUtils::compareSpiceButtonProperties( QQuickItem* spiceButton, bool visible, bool enabled, QString stringId )
{
    //Check Is visible
    EXPECT_EQ(spiceButton->property("visible").toBool(), visible);
    EXPECT_EQ(spiceButton->property("enabled").toBool(), enabled);

    if( !stringId.isEmpty())
    {
        compareButtonStringId(spiceButton, stringId);
    }
}

void WalkupAppGtestUtils::createInstanceOfJobTicket(MockIResourceStore* mockIResourceStore, QString ticketId)
{
    std::shared_ptr<JobTicketModel> jobTicketModel;
    jobTicketModel = mockIResourceStore->setCreateBehaviour<JobTicketModel>(
        new JobTicketModel(), "/cdm/jobTicket/v1/tickets", "/cdm/jobTicket/v1/tickets", "ticketId");
    fillDefaultCopyJobTicketModel(jobTicketModel, ticketId);

    // jobTicketModels_.push_back(jobTicketModel);
}

void WalkupAppGtestUtils::registerJobTicket(MockIResourceStore* mockIResourceStore, QString ticketId)
{
    std::shared_ptr<JobTicketModel> jobTicketModel;
    jobTicketModel = mockIResourceStore->registerFakeResource<JobTicketModel>(
        new JobTicketModel(QStringLiteral("/cdm/jobTicket/v1/tickets/%1").arg(ticketId)));
    // fillJobTicketModel(jobTicketModel, ticketId);
    fillDefaultCopyJobTicketModel(jobTicketModel, ticketId);
}