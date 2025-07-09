import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna 20dpcm Page from *lenna_20dpcm.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_20dpcm.jpg=be12e5937c270ec1d6690cc50cd3e42b1123f0d0fe04a6540e8c3ef19374c305
    +test_classification:System
    +name:test_jpeg_testsuite_lenna_20dpcm
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_20dpcm
        +guid:26a3ea1f-86bc-4764-aebb-b987f7d601fb
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_lenna_20dpcm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('be12e5937c270ec1d6690cc50cd3e42b1123f0d0fe04a6540e8c3ef19374c305', timeout=180)
    outputsaver.save_output()

    logging.info("JPEG TestSuite lenna 20dpcm Page - Print job completed successfully")
