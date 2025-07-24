import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:IPP test for printing a pcl5 basicfunctionality using 3Page-tr_tt.obj with attribute value
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-148958
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:3Page-tr_tt.obj=e5ef10052d66481d7a965a8fcc2f13277ac1e06316a525d09ec6aa647b2b135e
    +test_classification:System
    +name: test_pdl_intent_ipp_pcl5_basicfunctionality_3page_tr_tt
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pdl_intent_ipp_pcl5_basicfunctionality_3page_tr_tt
        +guid:0c68490d-c121-4685-aec2-abff6b22894f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & PrintColorMode=BlackOnly & Print=Normal & MediaType=Plain & MediaInputInstalled=Tray1 & PrintResolution=Print600

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_intent_ipp_pcl5_basicfunctionality_3page_tr_tt(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('na_index-4x6_4x6in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_index-4x6_4x6in', 'stationery')

    ipp_test_attribs = {'document-format': 'application/vnd.hp-PCL5', 'media': 'na_index-4x6_4x6in', 'print-color-mode': 'monochrome', 'print-quality': 4, 'copies':1, 'media-source': 'tray-1', 'media-type': 'stationery' , 'resolution': '600x600dpi', 'orientation-requested': 3, 'sides': 'one-sided'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'e5ef10052d66481d7a965a8fcc2f13277ac1e06316a525d09ec6aa647b2b135e')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 3)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.photo4x6)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
