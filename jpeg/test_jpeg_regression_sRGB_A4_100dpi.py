import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg Regression of sRGB A4 100dpi Page from *sRGB_A4_100dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:420
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:sRGB_A4_100dpi.jpg=1ba0f46f30adf9190185558010124bf32a1a432ba8aefd131d9c26bf9b050b09
    +test_classification:System
    +name:test_jpeg_regression_sRGB_A4_100dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_sRGB_A4_100dpi
        +guid:a7fd8c85-b874-4974-81d4-5b9cf7300603
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_regression_sRGB_A4_100dpi(setup_teardown, printjob, outputsaver,tray, udw):
    if outputsaver.configuration.productname == "jupiter":
        outputsaver.operation_mode('CRC')
    else:
        outputsaver.operation_mode('TIFF')
        outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, "anycustom", 'stationery')

    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('1ba0f46f30adf9190185558010124bf32a1a432ba8aefd131d9c26bf9b050b09',timeout=420)
    
    outputsaver.save_output()
    if outputsaver.configuration.productname == "jupiter":
        expected_crc = ["0x8e95a11b"]
        outputsaver.verify_output_crc(expected_crc)
    else:
        Current_crc_value = outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    logging.info("JPEG Regression sRGB A4 100dpi Page - Print job completed successfully")
