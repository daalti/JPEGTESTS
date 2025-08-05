import pytest
import logging
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, MediaSize, Plex, ColorMode, ContentOrientation, ColorRenderingType, PrintQuality, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value sides_two-sided-long-edge
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
    +name:test_pdl_intent_ipp_urf_sides_two_sided_long_edge
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_urf_sides_two_sided_long_edge
        +guid:fa61d218-b41f-4715-b746-4b0370cb1717
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & Duplexer=True & PrintColorMode=BlackOnly & Print=Best & MediaSizeSupported=Letter
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_urf_sides_two_sided_long_edge(setup_teardown, printjob, outputsaver, outputverifier):
    outputsaver.operation_mode('TIFF')
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    ipp_test_attribs = {'document-format': 'image/urf', 'sides': 'two-sided-long-edge', 'media': 'na_letter_8.5x11in','print-color-mode': 'monochrome', 'orientation-requested': 3, 'print-quality': print_quality_high}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'a381c0d4a54e009d86dfba20d0cc8a2d79f24f2da69e17ed66662bb953d82fbf', timeout=200)
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 6)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[print_quality_high]])
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
