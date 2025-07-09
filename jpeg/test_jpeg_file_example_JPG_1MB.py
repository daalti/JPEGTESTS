import pytest
import logging
from dunetuf.print.print_common_types import MediaType, MediaOrientation


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple Print job of Jpeg file of 1MB from **
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_example_JPG_1MB.jpg=683a8528125ca09d8314435c051331de2b4c981c756721a2d12c103e8603a1d2
    +test_classification:System
    +name:test_jpeg_file_example_JPG_1MB
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_file_example_JPG_1MB
        +guid:cd57e46a-4c0a-4cd9-8fea-5a1f350f81d8
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
def test_jpeg_file_example_JPG_1MB(setup_teardown, printjob, outputsaver, print_emulation, configuration, tray):
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None

        # Check each tray for supported sizes
        for tray_id in installed_trays:
            system_tray_id = tray_id.lower().replace('tray', 'tray-')
            if tray.is_size_supported('anycustom', system_tray_id):
                selected_tray = tray_id
                print_emulation.tray.open(selected_tray)
                print_emulation.tray.load(selected_tray, "Custom", MediaType.Plain.name,
                                        media_orientation="Portrait")
                print_emulation.tray.close(selected_tray)
                break
                
        if selected_tray is None:
            raise ValueError("No tray found supporting anycustom size")
    else:
        default = tray.get_default_source()
        media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        elif tray.is_size_supported('custom', default) and media_width_maximum >= 527777 and media_length_maximum >= 351944 and  media_width_minimum <= 527777 and media_length_minimum <= 351944:
            tray.configure_tray(default, 'custom', 'stationery') 

    printjob.print_verify('683a8528125ca09d8314435c051331de2b4c981c756721a2d12c103e8603a1d2', timeout=300)
    outputsaver.save_output()
    tray.reset_trays()
    logging.info("Jpeg file example JPG 1MB Page - Print job completed successfully")
