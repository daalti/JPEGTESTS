import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using **Low_Resolution.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Low_Resolution.jpg=c8c83c0ed7b494873b33ce156398af91d873f8317276b8055ccb0022d8f1b398
    +test_classification:System
    +name:test_jpeg_low_resolution
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_low_resolution
        +guid:b7040e4a-02c1-494c-b845-52c49f0f93b5
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
def test_jpeg_low_resolution(setup_teardown, printjob, outputsaver,udw, print_emulation):
    # Setting udw command for crc to true for generating pdl crc after print job done
    outputsaver.validate_crc_tiff(udw)
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()

        for tray_id in installed_trays:
            if outputsaver.configuration.productname == "camden":
                print_emulation.tray.load(tray_id, 'ThreeXFive', MediaType.Plain.name)
            else:
                print_emulation.tray.load(tray_id, MediaSize.A4.name, MediaType.Plain.name)
    printjob.print_verify('c8c83c0ed7b494873b33ce156398af91d873f8317276b8055ccb0022d8f1b398')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
