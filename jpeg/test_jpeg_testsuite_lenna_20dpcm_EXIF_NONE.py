import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna 20dpcm EXIF NONE Page from *lenna_20dpcm_EXIF_NONE.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_20dpcm_EXIF_NONE.jpg=cb6e516bebfbd46c2e719ebb1bb3c7f4d49cefb80977a40cc167073712f7ba24
    +test_classification:System
    +name:test_jpeg_testsuite_lenna_20dpcm_EXIF_NONE
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_20dpcm_EXIF_NONE
        +guid:0954d322-681a-4edc-ab9d-734cd1c42229
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_lenna_20dpcm_EXIF_NONE(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    default_size = tray.get_default_size(default)

    if tray.is_size_supported(default_size, default):
        logging.info(f"Set paper tray <{default}> to paper size <{default_size}>")
        tray.configure_tray(default, default_size, 'stationery')

    printjob.print_verify('cb6e516bebfbd46c2e719ebb1bb3c7f4d49cefb80977a40cc167073712f7ba24', timeout=180)
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("JPEG TestSuite lenna 20dpcm EXIF NONE Page - Print job completed successfully")
