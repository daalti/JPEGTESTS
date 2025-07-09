import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna without resolution info Page from *lenna_without_resolution_info.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:420
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_without_resolution_info.jpg=e1ed76315e7bfc2c48c28b1efb0fbd0a3b28c333583ce6b477cfcc7da495042c
    +test_classification:System
    +name:test_jpeg_testsuite_lenna_without_resolution_info
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_without_resolution_info
        +guid:b9805b92-6490-4a44-b6d5-c9ad72c04e04
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_lenna_without_resolution_info(setup_teardown, printjob, outputsaver,tray, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, "anycustom", 'stationery')

    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('e1ed76315e7bfc2c48c28b1efb0fbd0a3b28c333583ce6b477cfcc7da495042c',timeout=420)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("JPEG TestSuite lenna without resolution info Page - Print job completed successfully")
