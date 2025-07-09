import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna 100 dpi CMYK Page from *lenna_100_dpi_CMYK.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_100_dpi_CMYK.jpg=d96f65dbf236961108f2c22f547afc056967c2e26ff5928631108966bdb779c3
    +test_classification:System
    +name:test_jpeg_testsuite_lenna_100_dpi_CMYK
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_100_dpi_CMYK
        +guid:bcd5a7dc-8602-4cca-831e-703ae4f14acc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_lenna_100_dpi_CMYK(setup_teardown, printjob,udw,outputsaver, tray):
    outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    default_size = tray.get_default_size(default)

    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, "anycustom", 'stationery')

    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('d96f65dbf236961108f2c22f547afc056967c2e26ff5928631108966bdb779c3', timeout=300)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("JPEG TestSuite lenna 100 dpi CMYK Page - Print job completed successfully")
