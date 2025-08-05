import pytest
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, ColorMode, PrintQuality, Plex, PlexBinding, MediaType, ContentOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a document from mac and using attribute value media size_4x6 and media type_heavyglossy
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-124180
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:4x6_portrait.bin=88475fbbbd66f3d1e03aa8356cc67523a7bf956570d00825aa11b8c199278f9b
    +test_classification:System
    +name:test_pdl_airprint_mac_mediasize_4x6
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_airprint_mac_mediasize_4x6
        +guid:22f0a5c3-6278-41a1-88ef-faa6061edf04
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & Print=Best & MediaInputInstalled=Tray1 & MediaType=HeavyGlossy111-130g
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_airprint_mac_mediasize_4x6(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'com.hp.heavy-glossy')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_index-4x6_4x6in', 'print-color-mode': 'color', 'print-quality': print_quality_high, 'sides': 'one-sided', 'multiple-document-handling': 'separate-documents-collated-copies', 'orientation-requested': 3, 'media-source': 'tray-1', 'media-type': 'com.hp.heavy-glossy'}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_index-4x6_4x6in', 'print-color-mode': 'monochrome', 'print-quality': print_quality_high, 'sides': 'one-sided', 'multiple-document-handling': 'separate-documents-collated-copies', 'orientation-requested': 3, 'media-source': 'tray-1', 'media-type': 'com.hp.heavy-glossy'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '88475fbbbd66f3d1e03aa8356cc67523a7bf956570d00825aa11b8c199278f9b')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.photo4x6)
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