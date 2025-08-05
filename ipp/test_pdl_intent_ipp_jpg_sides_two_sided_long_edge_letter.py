import pytest
import logging
from dunetuf.print.output.intents import Intents, Plex, PlexBinding, MediaSize, ColorMode, MediaSource, ContentOrientation
from dunetuf.print.print_common_types import MediaType,MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value sides_two-sided-long-edge-letter.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:tn_PICT187.tiff=6131ebdb39b65bb399607852d86519758bcb129e27da6a0656f43dfb9e9ffab4
    +test_classification:System
    +name:test_pdl_intent_ipp_jpg_sides_two_sided_long_edge_letter
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_jpg_sides_two_sided_long_edge_letter
        +guid:77ccebda-6970-4323-8124-77b98bfd895f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & Duplexer=True & MediaSizeSupported=na_letter_8.5x11in & PrintColorMode=BlackOnly & MediaInputInstalled=Tray1

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_jpg_sides_two_sided_long_edge_letter(setup_teardown, printjob, outputsaver, outputverifier, print_emulation, tray):
    expected_media_size = MediaSize.letter
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None
        
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            
            if "Letter" in supported_sizes and MediaType.Plain.name in supported_types:
                selected_tray = tray_id
                expected_media_size = MediaSize.letter
                break
        
        if selected_tray is None:
            raise ValueError("No tray found supporting Letter size and Plain type paper")
            

        print_emulation.tray.open(selected_tray)
        print_emulation.tray.load(selected_tray, "Letter", MediaType.Plain.name,
                              media_orientation=MediaOrientation.Portrait.name)
        print_emulation.tray.close(selected_tray)

    ipp_test_attribs = {'document-format': 'image/jpeg', 'sides': 'two-sided-long-edge', 'print-scaling' : 'auto', 'media-size-name' : 'na_letter_8.5x11in', 'plex': 'duplex', 'print-color-mode': 'monochrome', 'copies':2, 'media-source': 'tray-1'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6131ebdb39b65bb399607852d86519758bcb129e27da6a0656f43dfb9e9ffab4')
    outputsaver.save_output()
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 2)
     # single page duplex job requests should be considered as simplex
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
