import pytest
import logging

from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using **2686.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:2686.jpg=e7a41c713330895d538595fbf74af4f7ac88a25424abb103beb3872d54cc0bfa
    +test_classification:System
    +name:test_jpeg_2686
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_2686
        +guid:c0d0ce10-f15a-4132-9f7e-64971518607d
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
def test_jpeg_2686(setup_teardown, printjob, outputsaver,udw, print_emulation, configuration, tray):
    if print_emulation.print_engine_platform == 'emulator':
        tray1 = MediaInputIds.Tray1.name
        if tray.is_size_supported('anycustom', 'tray-1'):
            print_emulation.tray.open(tray1)
            print_emulation.tray.load(tray1, 'Custom', MediaType.Plain.name)
            print_emulation.tray.close(tray1)

    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('e7a41c713330895d538595fbf74af4f7ac88a25424abb103beb3872d54cc0bfa')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
