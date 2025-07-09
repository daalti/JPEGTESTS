import pytest
import logging

from dunetuf.print.print_common_types import MediaSize, MediaType


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of jpg5
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:jpg5.jpg=9d133dde6eb25f2e326e6b72839242a8727e0cf1b64b882f4935a73d1f3cae14
    +test_classification:System
    +name:test_jpeg_jpg5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_jpg5
        +guid:1d35b0df-5cca-437b-8a03-9e485eb87117
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
def test_jpeg_jpg5(setup_teardown, printjob, outputsaver, tray, print_emulation):
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None

        for tray_id in installed_trays:
            system_tray_id = tray_id.lower().replace('tray', 'tray-')
            if tray.is_size_supported('anycustom', system_tray_id):
                selected_tray = tray_id
                break

        if selected_tray is None:
            raise ValueError("No tray found supporting anycustom in enterprise emulator")

        print_emulation.tray.open(selected_tray)
        print_emulation.tray.load(selected_tray, MediaSize.Custom.name, MediaType.Plain.name)
        print_emulation.tray.close(selected_tray)

    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]

    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 453333 and media_length_maximum >= 340000 and  media_width_minimum <= 453333 and media_length_minimum <= 340000:
        tray.configure_tray(default, 'custom', 'stationery') 
    
    printjob.print_verify('9d133dde6eb25f2e326e6b72839242a8727e0cf1b64b882f4935a73d1f3cae14')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("Jpeg photoimages resolution tif tif1024x768 file")
