import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg Regression of SWOP A4 100dpi Page from *SWOP_A4_100dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:SWOP_A4_100dpi.jpg=42cf76c1cbe4f91f5f557ffd6670c3438ed8611c5956d3aefcdf5274e3c83193
    +test_classification:System
    +name:test_jpeg_regression_SWOP_A4_100dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_SWOP_A4_100dpi
        +guid:63ccc95a-b1b0-45b1-bc35-2d50fd4a83ca
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_regression_SWOP_A4_100dpi(setup_teardown, printjob, outputsaver, tray, udw):
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

    printjob.print_verify('42cf76c1cbe4f91f5f557ffd6670c3438ed8611c5956d3aefcdf5274e3c83193', timeout=120)
    
    outputsaver.save_output()
    if outputsaver.configuration.productname == "jupiter":
        expected_crc = ["0xec6ce0e1"]
        outputsaver.verify_output_crc(expected_crc)
    else:
        Current_crc_value = outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    logging.info("JPEG Regression SWOP A4 100dpi Page - Print job completed successfully")
