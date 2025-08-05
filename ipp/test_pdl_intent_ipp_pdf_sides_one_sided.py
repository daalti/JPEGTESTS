import pytest
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, Plex, MediaSize, MediaSource, ColorMode, ColorRenderingType, ContentOrientation, PlexBinding, PlexSide, PrintQuality

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value sides_one_sided
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
    +name:test_pdl_intent_ipp_pdf_sides_one_sided
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pdf_sides_one_sided
        +guid:be79e0fa-4af1-49d5-be71-cd8ddf3166d2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & Print=Best & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_sides_one_sided(setup_teardown, printjob, outputsaver, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'sides': 'one-sided', 'media': 'na_letter_8.5x11in', 'orientation-requested': 3, 'print-color-mode': 'color', 'copies':2, 'print-quality': print_quality_high}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'sides': 'one-sided', 'media': 'na_letter_8.5x11in', 'orientation-requested': 3, 'print-color-mode': 'monochrome', 'copies':2, 'print-quality': print_quality_high}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 5)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 2)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)

    outputverifier.verify_plex_side(Intents.printintent, PlexSide.first)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[print_quality_high]])
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
