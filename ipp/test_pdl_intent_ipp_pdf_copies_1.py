import pytest

from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value copies_1.
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
    +name:test_pdl_intent_ipp_pdf_copies_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pdf_copies_1
        +guid:687c9acf-4116-4f47-a970-9b5dc11be1b7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & Print=Normal
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_copies_1(setup_teardown, printjob, outputverifier, outputsaver, tray, configuration, cdm):
    outputsaver.operation_mode('TIFF')
    default = tray.get_default_source()
    if tray.is_type_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_letter_8.5x11in', 'orientation-requested': 3, 'print-color-mode': 'color', 'print-quality': 4, 'copies':1, 'media-type': 'stationery', 'sides': 'one-sided'}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_letter_8.5x11in', 'orientation-requested': 3, 'print-color-mode': 'monochrome', 'print-quality': 4, 'copies':1, 'media-type': 'stationery', 'sides': 'one-sided'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputverifier.save_and_parse_output()
    
    expected_media_size = MediaSize.custom if 'roll' in default else MediaSize.letter
    outputverifier.verify_page_count(Intents.printintent, 5)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)

    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputsaver.operation_mode('NONE')
    if configuration.familyname != "designjet":
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        if cdm.device_feature_cdm.is_color_supported():
            outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
        else:
            outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)

        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    tray.reset_trays()