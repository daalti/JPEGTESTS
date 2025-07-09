import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite faces small Page from *faces_small.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:faces_small.jpg=19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc
    +test_classification:System
    +name:test_jpeg_testsuite_faces_small
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_faces_small
        +guid:77fe8d51-ee76-4e6f-801e-0c3756aa9555
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
def test_jpeg_testsuite_faces_small(setup_teardown, printjob, outputsaver, tray, print_emulation, configuration):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        tray1 = MediaInputIds.Tray1.name
        if tray.is_size_supported('anycustom', 'tray-1'):
            print_emulation.tray.open(tray1)
            print_emulation.tray.load(tray1, MediaSize.Custom.name, MediaType.Plain.name)
            print_emulation.tray.close(tray1)
    else:
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        else:
            tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("JPEG TestSuite faces small Page - Print job completed successfully")
