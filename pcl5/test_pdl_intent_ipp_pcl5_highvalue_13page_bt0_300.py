import pytest
import logging
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pcl5 highvalue using 13Page-bt0_300.obj with attribute value
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-148958
    +timeout:660
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:13Page-bt0_300.obj=6d3db5e306905991d140cfe463aaecca8be45633175a850cad41c241028597c3
    +test_classification:System
    +name: test_pdl_intent_ipp_pcl5_highvalue_13page_bt0_300
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pdl_intent_ipp_pcl5_highvalue_13page_bt0_300
        +guid:04270362-791f-4d01-a804-f05783aeab17
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & PrintColorMode=Color & Print=Best & MediaType=Plain & MediaInputInstalled=Tray1 & PrintResolution=Print600 & EngineFirmwareFamily=Canon
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pcl5_highvalue_13page_bt0_300(setup_teardown, printjob, outputsaver, outputverifier, tray):
    if tray.is_size_supported('na_index-4x6_4x6in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_index-4x6_4x6in', 'stationery')
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    ipp_test_attribs = {'document-format': 'application/vnd.hp-PCL5', 'media': 'na_index-4x6_4x6in', 'print-color-mode': 'color', 'print-quality': print_quality_high, 'copies':2, 'sides': 'one-sided', 'media-source': 'tray-1', 'media-type': 'stationery' , 'orientation-requested': 3, 'resolution': '600x600dpi'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6d3db5e306905991d140cfe463aaecca8be45633175a850cad41c241028597c3', timeout=700)
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 13)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 2)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.photo4x6)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[print_quality_high]])
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
