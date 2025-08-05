import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSource, MediaSize, ContentOrientation, ColorMode, NeutralAxisType, HalftoneType, PlexSide, TrappingLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value orientation_landscape
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_pdl_intent_ipp_pdf_orientation_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pdf_orientation_landscape
        +guid:710f9adf-99b1-4855-a54e-472ef8428d7b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_orientation_landscape(setup_teardown, printjob, outputsaver, outputverifier, cdm, configuration, tray):
    outputsaver.operation_mode('TIFF')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'orientation-requested': 4, 'print-color-mode': 'color', 'copies':2, 'media': 'na_letter_8.5x11in'}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'orientation-requested': 4, 'print-color-mode': 'monochrome', 'copies':2, 'media': 'na_letter_8.5x11in'}

    if 'landscape' not in printjob.capabilities.ipp.get('orientation-requested-supported'):
        logging.warning('Device does not support landscape as orientation-requested, setting fidelity to false...')
        ipp_test_attribs['ipp-attribute-fidelity'] = 'false'

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    outputverifier.save_and_parse_output()

    expected_media_size = MediaSize.letter

    default_source = tray.get_default_source()
    if default_source in tray.rolls:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        #verify letter dimensions
        expected_width = round(215900 / 25400 * job_resolution)
        expected_height = round(279400 / 25400 * job_resolution)

        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 2)
    outputverifier.verify_page_count(Intents.printintent, 5)
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    if configuration.familyname != "designjet":
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_vector_obj_neutral_axis_intent(Intents.printintent, NeutralAxisType.neutral_k_only)
        outputverifier.verify_text_obj_halftone_intent(Intents.printintent, HalftoneType.clustered_dot_0)
        outputverifier.verify_vector_obj_halftone_intent(Intents.printintent, HalftoneType.clustered_dot_0)
        outputverifier.verify_plex_side(Intents.printintent, PlexSide.first)
        if configuration.productname.strip().split('/')[0] in ["lotus", "cherry", "knoxygen", "marconi", "moreto", "kebin", "victoria", "sandune", "victoriaplus", "beam", "busch", "dagger", "tachi"]:
            outputverifier.verify_color_trap_level(Intents.printintent, TrappingLevel.off_0)
        else:
            outputverifier.verify_color_trap_level(Intents.printintent, TrappingLevel.level_2)