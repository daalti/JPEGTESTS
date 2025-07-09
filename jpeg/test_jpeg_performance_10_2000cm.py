import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg Performance of 10_2000cm Page from *10_2000cm.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:10_2000cm.jpg=c99290a709203b35b2e7c8520e9764b1648ec79354af4bddfa7aa14b52848dad
    +test_classification:System
    +name:test_jpeg_performance_10_2000cm
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_performance_10_2000cm
        +guid:e2ff79eb-71a4-4742-8c10-960d35f30b20
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=Letter

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_performance_10_2000cm(setup_teardown, printjob, outputsaver, tray, media):

    # Not using print_verify for a reason
    # We want to handle media mismatch alert on design products before job completion
    jobid = printjob.start_print('c99290a709203b35b2e7c8520e9764b1648ec79354af4bddfa7aa14b52848dad')
    # for non design products total test timeout will be 240
    # for design 300
    printjob.wait_verify_job_completion(jobid, timeout=240)

    logging.info("JPEG Performance 10_2000cm Page - Print job completed successfully")
