import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg file of 500kB from *file_example_JPG_500kB.jpg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_example_JPG_500kB.jpg=838e346997ab5f2dd6745e9e536de6f9cd68965088354597f2fba016ad40ab2c
    +name:test_jpeg_file_example_JPG_500kB
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_file_example_JPG_500kB
        +guid:ceb870e9-8be4-446a-9bb0-1aec6b948acf
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_file_example_JPG_500kB(setup_teardown, printjob, outputsaver):
    printjob.print_verify('838e346997ab5f2dd6745e9e536de6f9cd68965088354597f2fba016ad40ab2c')
    outputsaver.save_output()

    logging.info("Jpeg file example JPG 500kB Page - Print job completed successfully")
