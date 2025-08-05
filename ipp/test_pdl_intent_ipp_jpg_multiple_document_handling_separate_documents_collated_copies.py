import pytest
import logging
from dunetuf.print.output.intents import Intents, Plex, MediaSize, ColorMode, ColorRenderingType

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value multiple-document-handling_separate-documents-collated-copies.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_pdl_intent_ipp_jpg_multiple_document_handling_separate_documents_collated_copies
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_jpg_multiple_document_handling_separate_documents_collated_copies
        +guid:2af14755-69b2-4748-8d59-23263ba67f03
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_jpg_multiple_document_handling_separate_documents_collated_copies(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm, configuration):
    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'image/jpeg', 'multiple-document-handling': 'separate-documents-collated-copies', 'copies':1, 'media': 'na_letter_8.5x11in', 'print-color-mode': 'color'}
    else:
        ipp_test_attribs = {'document-format': 'image/jpeg', 'multiple-document-handling': 'separate-documents-collated-copies', 'copies':1, 'media': 'na_letter_8.5x11in', 'print-color-mode': 'monochrome'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()
    if tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"] >= 94500:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, "custom", 'stationery')

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    outputverifier.save_and_parse_output()

    expected_media_size = MediaSize.custom if 'roll' in default else MediaSize.letter
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    if configuration.familyname != "designjet":
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        if cdm.device_feature_cdm.is_color_supported():
            outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
        else:
            outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)

    tray.reset_trays()