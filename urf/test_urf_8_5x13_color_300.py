import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 8_5x13 color 300 page from *8_5x13_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8_5x13_Color_300.urf=df0ad3eee183375bd2f24ff7e5794783527f7182fb1e502970b93a4c9e140f40
    +name:test_urf_8_5x13_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_8_5x13_color_300_page
        +guid:84b04b4b-0266-4a42-96ff-ef1c2e9890aa
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_8_5x13_color_300_page(setup_teardown, printjob, print_emulation, configuration, outputsaver,udw,tray):
    outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('na_foolscap_8.5x13in', default):
        if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            print_emulation.tray.open(tray1)
            print_emulation.tray.load(tray1, MediaSize.EightPointFiveByThirteen.name, MediaType.Plain.name)
            print_emulation.tray.close(tray1)
        else:
            tray.configure_tray(default, 'na_foolscap_8.5x13in', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 85000 and media_length_maximum >= 130000 and  media_width_minimum <= 85000 and media_length_minimum <= 130000:
        tray.configure_tray(default, 'custom', 'stationery')
    

    printjob.print_verify('df0ad3eee183375bd2f24ff7e5794783527f7182fb1e502970b93a4c9e140f40')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF 8_5x13 Color 300 page - Print job completed successfully")
