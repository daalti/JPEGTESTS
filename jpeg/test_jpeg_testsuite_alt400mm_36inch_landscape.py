import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite alt400mm 36inch landscape Page from *alt400mm_36inch_landscape.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:alt400mm_36inch_landscape.jpg=8cb2e40ad94a931c43c9c6253ef7f367aa54cabf7b96a09a581c5b621fd00902
    +test_classification:System
    +name:test_jpeg_testsuite_alt400mm_36inch_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_alt400mm_36inch_landscape
        +guid:bf36a4cf-b5ec-46b5-a0a0-6502e0d00987
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
def test_jpeg_testsuite_alt400mm_36inch_landscape(setup_teardown, udw,printjob, outputsaver, print_emulation):
    outputsaver.validate_crc_tiff(udw)
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()
        for tray_id in installed_trays:
            print_emulation.tray.load(tray_id, MediaSize.A4.name, MediaType.Plain.name)
    printjob.print_verify('8cb2e40ad94a931c43c9c6253ef7f367aa54cabf7b96a09a581c5b621fd00902', timeout=180)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("JPEG TestSuite alt400mm 36inch landscape Page - Print job completed successfully")
