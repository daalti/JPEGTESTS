import pytest

from dunetuf.print.output.intents import Intents,  MediaSize, MediaSource, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value print_color_mode_process_monochrome
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
    +name:test_pdl_intent_ipp_pdf_print_color_mode_process_monochrome
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pdf_print_color_mode_process_monochrome
        +guid:e5673b88-081e-44eb-9fe1-0b91d39ec3e3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & PrintColorMode=GrayScale & MediaSizeSupported=na_letter_8.5x11in & Print=Normal & MediaInputInstalled=Tray1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_print_color_mode_process_monochrome(setup_teardown, printjob, outputverifier, outputsaver):
    outputsaver.operation_mode('TIFF')
    ipp_test_attribs = {'document-format': 'application/pdf', 'print-color-mode': 'process-monochrome', 'media': 'na_letter_8.5x11in', 'orientation-requested': 6, 'print_quality': 4, 'color_rendering_type': 'office_rgb', 'plex': 'simplex', 'copies':3, 'media-type': 'stationery'}

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 5)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 3)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.grayscale)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.reverseportrait)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputsaver.operation_mode('NONE')
