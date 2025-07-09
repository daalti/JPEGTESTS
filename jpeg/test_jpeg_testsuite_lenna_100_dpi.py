import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna 100 dpi Page from *lenna_100_dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_100_dpi.jpg=7a2e13bafa3b09a94ae8a5c92592c36f3104d8eb862dd121f505fd11262fc242
    +test_classification:System
    +name:test_jpeg_testsuite_lenna_100_dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_100_dpi
        +guid:62970693-3b40-4f3e-917c-48c2c4c81e26
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_lenna_100_dpi(setup_teardown, printjob, outputsaver, tray):
    outputsaver.operation_mode('TIFF')

    default = tray.get_default_source()
    default_size = tray.get_default_size(default)

    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, "anycustom", 'stationery')

    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('7a2e13bafa3b09a94ae8a5c92592c36f3104d8eb862dd121f505fd11262fc242', timeout=300)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    logging.info("JPEG TestSuite lenna 100 dpi Page - Print job completed successfully")
