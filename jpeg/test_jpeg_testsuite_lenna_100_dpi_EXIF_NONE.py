import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna 100 dpi EXIF NONE Page from *lenna_100_dpi_EXIF_NONE.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_100_dpi_EXIF_NONE.jpg=cc7efdcc505cf95c913aeafa9886ad5a4f2c31b4afefd35d9c9f5fd60f4368d3
    +test_classification:System
    +name:test_jpeg_testsuite_lenna_100_dpi_EXIF_NONE
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_100_dpi_EXIF_NONE
        +guid:9ae65615-d55e-4844-97cf-20b6ec411cfe
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_lenna_100_dpi_EXIF_NONE(setup_teardown, printjob, outputverifier, outputsaver,udw,tray):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    default_size = tray.get_default_size(default)

    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, "anycustom", 'stationery')

    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('cc7efdcc505cf95c913aeafa9886ad5a4f2c31b4afefd35d9c9f5fd60f4368d3', timeout=180)
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("JPEG TestSuite lenna 100 dpi EXIF NONE Page - Print job completed successfully")
