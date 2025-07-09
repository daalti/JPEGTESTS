import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of autoalign 0921fromhp autoalign landscape 3x2 dsc 0967
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:autoAlign_0921fromHP_AutoAlign_Landscape_3x2_DSC_0967.JPG=9a0f8feea5185a818537425da9affc905d0ef63c4ef0f675b564fdda4728385b
    +test_classification:System
    +name:test_jpeg_autoalign_0921fromhp_autoalign_landscape_3x2_dsc_0967
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_autoalign_0921fromhp_autoalign_landscape_3x2_dsc_0967
        +guid:61422719-2a40-4272-b5f6-8c7fed592c21
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_autoalign_0921fromhp_autoalign_landscape_3x2_dsc_0967(setup_teardown, print_emulation, configuration,printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            if tray.is_size_supported('custom', 'tray-1'):
                print_emulation.tray.open(tray1)
                print_emulation.tray.load(tray1, MediaSize.Custom.name, MediaType.Plain.name)
                print_emulation.tray.close(tray1)
        else:
            tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('9a0f8feea5185a818537425da9affc905d0ef63c4ef0f675b564fdda4728385b')
    outputsaver.save_output()

    logging.info("Jpeg autoAlign 0921fromHP AutoAlign Landscape 3x2 DSC 0967 file")
