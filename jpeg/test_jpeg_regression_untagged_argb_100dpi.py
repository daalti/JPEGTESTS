import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178011 Simple print job of Jpeg Regression of untagged argb 100dpi Page from *untagged_argb_100dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:400
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:untagged_argb_100dpi.jpg=d91801b4c08f2ed918a3cbf885a61c8721cace99b0e83a2f82e95660e2275704
    +test_classification:System
    +name:test_jpeg_regression_untagged_argb_100dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_untagged_argb_100dpi
        +guid:3cdc0469-695f-4457-b905-9deba0669064
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
        +ProA4:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_regression_untagged_argb_100dpi(setup_teardown, printjob, outputsaver,tray, print_emulation, print_mapper, udw, reset_tray, configuration):
    if outputsaver.configuration.productname == "jupiter":
        outputsaver.operation_mode('CRC')
    else:
        outputsaver.operation_mode('TIFF')
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        installed_trays = print_emulation.tray.get_installed_trays()

        for tray_id in installed_trays:
            system_tray_id = tray_id.lower().replace('tray', 'tray-')
            if tray.is_size_supported('anycustom', system_tray_id):
                print_emulation.tray.open(tray_id)
                print_emulation.tray.load(tray_id, "Custom", MediaType.Plain.name,
                                          media_orientation="Portrait")
                print_emulation.tray.close(tray_id)
                break
    default = tray.get_default_source()
    if tray.is_size_supported('any', default):
        tray_test_name = print_mapper.get_media_input_test_name(default)
        print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name)
        tray.configure_tray(default, 'any', 'any')
    elif tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, "anycustom", 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')
    outputsaver.validate_crc_tiff(udw) 
    printjob.print_verify('d91801b4c08f2ed918a3cbf885a61c8721cace99b0e83a2f82e95660e2275704',timeout=360)

    outputsaver.save_output()
    if outputsaver.configuration.productname == "jupiter":
        expected_crc = ["0x9350fdc4"]    
        outputsaver.verify_output_crc(expected_crc)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    logging.info("JPEG Regression untagged argb 100dpi Page - Print job completed successfully")