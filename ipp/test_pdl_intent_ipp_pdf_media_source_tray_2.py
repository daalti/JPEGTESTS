import pytest

from dunetuf.print.output.intents import Intents,  MediaSize, MediaSource, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value media_source_tray_2
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_pdl_intent_ipp_pdf_media_source_tray_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pdf_media_source_tray_2
        +guid:ccb8813b-0afa-4cae-90d5-ce8e14d96cca
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaInputInstalled=Tray2 & MediaSizeSupported=iso_a4_210x297mm & PrintColorMode=BlackOnly & Print=Normal

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_media_source_tray_2(setup_teardown, printjob, outputverifier, tray, outputsaver):
    outputsaver.operation_mode('TIFF')
    if tray.is_size_supported('iso_a4_210x297mm', 'tray-2'):
        tray.configure_tray('tray-2', 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {'document-format': 'application/pdf', 'media-source': 'tray-2', 'media': 'iso_a4_210x297mm', 'orientation-requested': 5, 'print-color-mode': 'monochrome', 'print-quality': 4, 'copies':1, 'media-type': 'stationery', 'sides': 'one-sided'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 5)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray2)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.reverselandscape)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    tray.reset_trays()
    outputsaver.operation_mode('NONE')
