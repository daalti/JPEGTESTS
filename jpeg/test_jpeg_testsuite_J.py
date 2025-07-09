import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite J Page from *J.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:J.jpg=010f60d2927a35d0235490136ef9f4953b7ee453073794bcaf153d20a64544ea
    +test_classification:System
    +name:test_jpeg_testsuite_J
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_J
        +guid:d7c07c9f-7cac-44ae-9fa6-c40862b9465d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_J(setup_teardown, printjob, outputsaver, tray, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    default_size = tray.get_default_size(default)

    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, "anycustom", 'stationery')

    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('010f60d2927a35d0235490136ef9f4953b7ee453073794bcaf153d20a64544ea',timeout = 180)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("JPEG TestSuite J Page - Print job completed successfully")
