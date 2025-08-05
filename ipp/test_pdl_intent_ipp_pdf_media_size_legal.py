import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaType, MediaSource, ContentOrientation, ColorMode, ContentOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value media_size_legal
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_pdl_intent_ipp_pdf_media_size_legal
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pdf_media_size_legal
        +guid:36043e6b-de35-4b01-a899-622a1894292c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_legal_8.5x14in & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_media_size_legal(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')
    if tray.is_size_supported('na_legal_8.5x14in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_legal_8.5x14in', 'stationery')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_legal_8.5x14in', 'media-type': 'stationery', 'copies':4, 'orientation-requested': 3, 'print-color-mode': 'color', 'media-source': 'tray-1'}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_legal_8.5x14in', 'media-type': 'stationery', 'copies':4, 'orientation-requested': 3, 'print-color-mode': 'monochrome', 'media-source': 'tray-1'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982', timeout=240)
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 5)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 4)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.legal)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()