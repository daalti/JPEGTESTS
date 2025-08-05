import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, Plex, ContentOrientation, ColorRenderingType, PrintQuality, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value sides_tow-sided-short-edge
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-131696
    +timeout:250
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:LetterUSVND5p.urf=a381c0d4a54e009d86dfba20d0cc8a2d79f24f2da69e17ed66662bb953d82fbf
    +name:test_pdl_intent_ipp_urf_sides_two_sided_short_edge
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_urf_sides_two_sided_short_edge
        +guid:ef1d31c0-4ca5-4686-8d3e-3c8a92f663ca
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & Duplexer=True & Print=Normal
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_urf_sides_two_sided_short_edge(setup_teardown, printjob, outputsaver, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')
    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'image/urf', 'sides': 'two-sided-short-edge', 'media': 'na_letter_8.5x11in','print-color-mode': 'color', 'orientation-requested': 3, 'print-quality': 4}
    else:
        ipp_test_attribs = {'document-format': 'image/urf', 'sides': 'two-sided-short-edge', 'media': 'na_letter_8.5x11in','print-color-mode': 'monochrome', 'orientation-requested': 3, 'print-quality': 4}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'a381c0d4a54e009d86dfba20d0cc8a2d79f24f2da69e17ed66662bb953d82fbf', timeout=200)
    outputverifier.save_and_parse_output()
    # 5 page two-sided job is a page count of 6
    outputverifier.verify_page_count(Intents.printintent, 6)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)

    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')