import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite 100x100 rgb Page from *100x100rgb.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:100x100rgb.jpg=d5ac022cb1f519bf43576315cd62acb7dd7ba4de26bcd229fc544023a5da12ab
    +test_classification:System
    +name:test_jpeg_testsuite_100x100rgb
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_100x100rgb
        +guid:0cb8ab3f-e8bb-4f5b-ab4e-16ee551ad172
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_100x100rgb(setup_teardown, printjob, outputsaver, tray):
    outputsaver.operation_mode('TIFF')

    default = tray.get_default_source()
    default_size = tray.get_default_size(default)

    if tray.is_size_supported(default_size, default):
        logging.info(f"Set paper tray <{default}> to paper size <{default_size}>")
        tray.configure_tray(default, default_size, 'stationery')

    printjob.print_verify('d5ac022cb1f519bf43576315cd62acb7dd7ba4de26bcd229fc544023a5da12ab', timeout=180)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

    logging.info("JPEG TestSuite 100x100 rgb Page - Print job completed successfully")
