import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Fire Letter Landscape from *Fire_Letter_Landscape.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Fire_Letter_Landscape.urf=bb7a23ef6e64d35e1c87946fb314df3c3871319f855aa4c7e89e0cc5951e8d74
    +name:test_urf_fire_letter_landscape_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_fire_letter_landscape_page
        +guid:60be4890-7567-4f3a-aa34-d775bef65315
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
def test_urf_fire_letter_landscape_page(setup_teardown, printjob, outputsaver, udw,tray, print_emulation):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(
            trayid="all",
            media_size=MediaSize.Letter.name,
            media_type=MediaType.Plain.name,
            orientation=MediaOrientation.Default.name,
            level=TrayLevel.Full.name
        )
    elif tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
    printjob.print_verify('bb7a23ef6e64d35e1c87946fb314df3c3871319f855aa4c7e89e0cc5951e8d74')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF Fire Letter Landscape page - Print job completed successfully")
