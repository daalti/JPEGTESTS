import pytest
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, ColorRenderingType, ContentOrientation, MediaType, Plex, PlexBinding, PrintQuality

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a PCLm file using attribute value media-size_letter
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-129624
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_ADOBE-RGB__Blank_PNG_Source.pdf=b2c5a5fe2a7e2ab45618cd1a41f6e466e153b999ec2eaf13e2b365eea0d84142
    +name:test_pdl_intent_ipp_pclm_blank_page_adobe_rgb
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pclm_blank_page_adobe_rgb
        +guid:efddbc80-95e4-4063-9abf-ccb6507667d4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & Print=Normal
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pclm_blank_page_adobe_rgb(setup_teardown, printjob, outputverifier, outputsaver, cdm):
    outputsaver.operation_mode('TIFF')
    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/PCLm', 'ipp-attribute-fidelity': 'true', 'copies':1, 'media': 'na_letter_8.5x11in', 'print-color-mode': 'color', 'orientation-requested': 3, 'media-type': 'stationery', 'print_quality': 4, 'sides': 'one-sided'}
    else:
        ipp_test_attribs = {'document-format': 'application/PCLm', 'ipp-attribute-fidelity': 'true', 'copies':1, 'media': 'na_letter_8.5x11in', 'print-color-mode': 'monochrome', 'orientation-requested': 3, 'media-type': 'stationery', 'print_quality': 4, 'sides': 'one-sided'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'b2c5a5fe2a7e2ab45618cd1a41f6e466e153b999ec2eaf13e2b365eea0d84142')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)

    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputsaver.operation_mode('NONE')
