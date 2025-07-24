import pytest
import logging
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing pcl5 highvalue using 1Page-clip_pm.obj with attribute value
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-148958
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-clip_pm.obj=4a0f46abc1cb3616c725f8c255dfa89a07b84110e37a4f74a8f7f265daa6752b
    +test_classification:System
    +name: test_pdl_intent_ipp_pcl5_highvalue_1page_clip_pm
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pdl_intent_ipp_pcl5_highvalue_1page_clip_pm
        +guid:9abb2ed3-a4c7-475a-8359-9c28092314f6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & PrintProtocols=IPP & MediaSizeSupported=na_monarch_3.875x7.5in & PrintColorMode=Color & Print=Best & MediaType=Plain & MediaInputInstalled=Tray1 & PrintResolution=Print600
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pcl5_highvalue_1page_clip_pm(setup_teardown, printjob, outputsaver, outputverifier, tray):
    if tray.is_size_supported('na_monarch_3.875x7.5in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_monarch_3.875x7.5in', 'stationery')
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    ipp_test_attribs = {'document-format': 'application/vnd.hp-PCL5', 'media': 'na_monarch_3.875x7.5in','print-color-mode': 'color', 'print-quality': print_quality_high, 'copies':2, 'sides': 'one-sided', 'media-source': 'tray-1', 'orientation-requested': 3, 'media-type': 'stationery', 'resolution': '600x600dpi'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '4a0f46abc1cb3616c725f8c255dfa89a07b84110e37a4f74a8f7f265daa6752b',timeout=300)
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 2)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.monarchenvelope)
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
