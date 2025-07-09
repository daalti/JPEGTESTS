import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg Regression of untagged cmyk swop 100dpi Page from *untagged_cmyk_swop_100dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:untagged_cmyk_swop_100dpi.jpg=4f9f5dd2775a1a4a733a6a21830b4b257bab151d6971ee664e482c67013d7cda
    +test_classification:System
    +name:test_jpeg_regression_untagged_cmyk_swop_100dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_untagged_cmyk_swop_100dpi
        +guid:13d0851b-20f1-491f-9b93-de1c584138b5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_regression_untagged_cmyk_swop_100dpi(setup_teardown, printjob, outputsaver, tray, udw):
    if outputsaver.configuration.productname == "jupiter":
        outputsaver.operation_mode('CRC')
    else:
        outputsaver.operation_mode('TIFF')
        outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    default_size = tray.get_default_size(default)

    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, "anycustom", 'stationery')

    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('4f9f5dd2775a1a4a733a6a21830b4b257bab151d6971ee664e482c67013d7cda',timeout=180)
    
    outputsaver.save_output()
    if outputsaver.configuration.productname == "jupiter":
        expected_crc = ["0x1408b886"]
        outputsaver.verify_output_crc(expected_crc)
    else:
        Current_crc_value = outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    logging.info("JPEG Regression untagged cmyk swop 100dpi Page - Print job completed successfully")
