import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg Regression of BGR A4 100dpi Page from *BGR_A4_100dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:420
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:BGR_A4_100dpi.jpg=04e30e1847278cbccc57f4ac8cc64e657922b47be63fd42874311b453c629f7b
    +test_classification:System
    +name:test_jpeg_regression_BGR_A4_100dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_BGR_A4_100dpi
        +guid:c0c1526c-a963-4c63-ba36-41ea55829cd7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_regression_BGR_A4_100dpi(setup_teardown, printjob, outputsaver, tray, print_emulation, print_mapper, udw):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, "anycustom", 'stationery')
    elif tray.is_size_supported('any', default):
        tray_test_name = print_mapper.get_media_input_test_name(default)
        print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name)
        tray.configure_tray(default, 'any', 'any')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('04e30e1847278cbccc57f4ac8cc64e657922b47be63fd42874311b453c629f7b',timeout=420)
    outputsaver.save_output()
    tray.reset_trays()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("JPEG Regression BGR A4 100dpi Page - Print job completed successfully")
