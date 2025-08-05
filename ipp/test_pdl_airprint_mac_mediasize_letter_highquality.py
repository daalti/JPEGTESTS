import pytest
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, Plex, PlexBinding, MediaType, ContentOrientation, MediaSource

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a PDF document from mac using attribute value media type heavyglossy and media size Letter
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-124180
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:testfile.bin=c3a8f6aa768ea4ffe60008c855e32ca922f625eeecdf1c5d3582b371acfcd7ae
    +test_classification:System
    +name:test_pdl_airprint_mac_mediasize_letter_highquality
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_airprint_mac_mediasize_letter_highquality
        +guid:4d0e854f-4266-4969-b6e3-2fddb852e8e8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & Print=Best & MediaInputInstalled=Tray1 & MediaType=HeavyGlossy111-130g
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_airprint_mac_mediasize_letter_highquality(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default) and tray.is_type_supported('com.hp.heavy-glossy', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'com.hp.heavy-glossy')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_letter_8.5x11in', 'print-color-mode': 'color', 'print-quality': print_quality_high, 'sides': 'one-sided', 'multiple-document-handling': 'separate-documents-collated-copies', 'orientation-requested': 3, 'media-type': 'com.hp.heavy-glossy', 'media-source': 'tray-1'}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_letter_8.5x11in', 'print-color-mode': 'monochrome', 'print-quality': print_quality_high, 'sides': 'one-sided', 'multiple-document-handling': 'separate-documents-collated-copies', 'orientation-requested': 3, 'media-type': 'com.hp.heavy-glossy', 'media-source': 'tray-1'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'c3a8f6aa768ea4ffe60008c855e32ca922f625eeecdf1c5d3582b371acfcd7ae')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 3)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[print_quality_high]])
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_media_type(Intents.printintent, MediaType.heavyglossy)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()