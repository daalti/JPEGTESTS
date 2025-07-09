import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite DemoImages Page from *DemoImages.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DemoImages.jpg=3c685134a542d477374788bb6a3f1027cd8f433d49a0255b2ac7f5246bd7010c
    +test_classification:System
    +name:test_jpeg_testsuite_DemoImages
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_DemoImages
        +guid:ec7a02f8-1101-4e41-8d52-738b75331274
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_DemoImages(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3c685134a542d477374788bb6a3f1027cd8f433d49a0255b2ac7f5246bd7010c', timeout=180)
    outputsaver.save_output()

    logging.info("JPEG TestSuite DemoImages Page - Print job completed successfully")
