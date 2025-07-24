
import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Testing cancel of pcl5 jobs 
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-236978
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:66Page-pixel.obj=36342bd755c3212a1782f3f9a1afc6b11910e9dfed1102b4815d01ad532b2bd3
    +test_classification:System
    +name: test_pcl5_job_cancel
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_job_cancel
        +guid:2d2d9235-e6e5-4298-b34b-22e6bc73e14b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5   
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_job_cancel(printjob):
    logging.debug("Perform print job")
    jobid = printjob.start_print('36342bd755c3212a1782f3f9a1afc6b11910e9dfed1102b4815d01ad532b2bd3')

    logging.info('Canceling print job')
    printjob.job.cancel_active_jobs()

    logging.info('Waiting for job cancellation')
    jobstate = printjob.wait_for_job_completion(jobid,120)
    assert 'CANCELED' in jobstate, "Unexpected final job state - {0}".format(jobstate)