import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only whx bitmap page-3 from *PwgPhOnly-WxHBitmap-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-WxHBitmap-3.pwg=9317c85e664d74480bf5d515af2d88bd463f9f87e73642d7c9b052834ed4c2fa
    +name:test_pwg_ph_only_wxh_bitmap_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_wxh_bitmap_3
        +guid:eef30d87-2ad6-4865-bb5b-d238c74fc3a0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_wxh_bitmap_3(setup_teardown, printjob, outputsaver, tray, print_emulation, configuration):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            if "A4" in supported_sizes and "Plain" in supported_types:
                print_emulation.tray.open(tray_id)
                print_emulation.tray.load(tray_id, "A4", "Plain",
                                    media_orientation=MediaOrientation.Portrait.name)
                print_emulation.tray.close(tray_id)
                break
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('9317c85e664d74480bf5d515af2d88bd463f9f87e73642d7c9b052834ed4c2fa')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("PWG Ph Only Whx Bitmap-3completed successfully!")
