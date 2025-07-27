import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a 4X6 glossy 4-page simplex borderlesson 1page per sheet  PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-150020
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:4X6_borderlesson_1pagespersheet.prn=a85d10c75c0e389d69940b5e550e202804fde6d9f997a041b35cbd5cb0e7ad49
    +name:test_pdl_intent_pcl3gui_4X6_borderlesson_1pagespersheet
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_4X6_borderlesson_1pagespersheet
        +guid:49912c72-97b1-408b-8eb0-5ede5166a57d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & PrintColorMode=GrayScale & Print=Normal & MediaType=HPTri-foldBrochurepaper-Glossy & PrintResolution=Print1200

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_4X6_borderlesson_1pagespersheet(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('na_index-4x6_4x6in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_index-4x6_4x6in', 'com.hp-trifold-brochure-glossy-180gsm')

    printjob.print_verify('a85d10c75c0e389d69940b5e550e202804fde6d9f997a041b35cbd5cb0e7ad49')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 4)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.photo4x6)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.grayscale)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.trifold_brochure_glossy)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    outputverifier.verify_resolution(Intents.printintent, 1200)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
