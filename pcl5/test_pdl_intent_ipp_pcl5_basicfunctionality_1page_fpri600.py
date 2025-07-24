import pytest
import logging
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:IPP test for printing a pcl5 basic functionality using 1Page-fpri600.obj with attribute value
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-148958
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-fpri600.obj=980cabbf08033824f1375b2ffc25963578d63833a42e3a1d20321495d35186b4
    +test_classification:System
    +name: test_pdl_intent_ipp_pcl5_basicfunctionality_1page_fpri600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pdl_intent_ipp_pcl5_basicfunctionality_1page_fpri600
        +guid:872f8b11-cb16-4dde-9879-1663abf72268
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & PrintColorMode=Color & Print=Best & MediaType=HPTri-foldBrochureGlossy150g & MediaInputInstalled=Tray1 & PrintResolution=Print600
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pcl5_basicfunctionality_1page_fpri600(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('na_index-4x6_4x6in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_index-4x6_4x6in', 'com.hp-trifold-brochure-glossy-150gsm')
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    ipp_test_attribs = {'document-format': 'application/vnd.hp-PCL5', 'media': 'na_index-4x6_4x6in', 'print-color-mode': 'color', 'print-quality': print_quality_high, 'copies':2, 'sides': 'one-sided', 'media-source': 'tray-1', 'media-type': 'com.hp-trifold-brochure-glossy-150gsm' , 'orientation-requested': 4, 'resolution': '600x600dpi'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '980cabbf08033824f1375b2ffc25963578d63833a42e3a1d20321495d35186b4')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 2)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.photo4x6)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[print_quality_high]])
    outputverifier.verify_media_type(Intents.printintent, MediaType.hptrifoldglossy150g)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
