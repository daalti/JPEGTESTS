import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg Regression of 3Dgirls JFIF nounits without EXIF Page from *3Dgirls_JFIF_nounits_without_EXIF.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:3Dgirls_JFIF_nounits_without_EXIF.jpg=07010aa839653b2355047c770f6f3631997e0e9172537141d42d185c34f39a1d
    +test_classification:System
    +name:test_jpeg_regression_3Dgirls_JFIF_nounits_without_EXIF
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_3Dgirls_JFIF_nounits_without_EXIF
        +guid:2e4c1fe2-dd29-45e0-ba3c-c1fd5cc50f22
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_regression_3Dgirls_JFIF_nounits_without_EXIF(setup_teardown, printjob, outputsaver):
    printjob.print_verify('07010aa839653b2355047c770f6f3631997e0e9172537141d42d185c34f39a1d', timeout=180)
    outputsaver.save_output()

    logging.info("JPEG Regression 3Dgirls JFIF nounits without EXIF Page - Print job completed successfully")
