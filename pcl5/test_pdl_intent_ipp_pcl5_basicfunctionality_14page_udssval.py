import pytest
import logging
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing pcl5 basicfunctionality using 14Page-udssval.obj with attribute value
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-148958
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:14Page-udssval.obj=380b283d10af04c5211e83373bd2a8bc1e598bc5906d5d0bcf625b6d0737a124
    +test_classification:System
    +name: test_pdl_intent_ipp_pcl5_basicfunctionality_14page_udssval
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pdl_intent_ipp_pcl5_basicfunctionality_14page_udssval
        +guid:0dcedcb6-b5bb-4b23-ba5f-2028e0a9f0fb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & PrintColorMode=GrayScale & Print=Best & MediaType=Plain & MediaInputInstalled=Tray2 & PrintResolution=Print600 & Duplexer=True
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pcl5_basicfunctionality_14page_udssval(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('na_letter_8.5x11in', 'tray-2'):
        tray.configure_tray('tray-2', 'na_letter_8.5x11in', 'stationery')
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    ipp_test_attribs = {'document-format': 'application/vnd.hp-PCL5', 'media': 'na_letter_8.5x11in', 'print-color-mode': 'process-monochrome', 'print-quality': print_quality_high, 'copies':2, 'media-source': 'tray-2', 'media-type': 'stationery' , 'resolution': '600x600dpi', 'orientation-requested': 3, 'sides': 'two-sided-short-edge'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '380b283d10af04c5211e83373bd2a8bc1e598bc5906d5d0bcf625b6d0737a124', timeout=300)
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 28)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 2)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.grayscale)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[print_quality_high]])
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray2)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
