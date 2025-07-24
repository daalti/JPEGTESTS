import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pd.obj=480ccb94d5789edbaa26fb3702c953a7a8f0006fc49005e878ef1b411d2bcf63
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pd
    +test:
        +title: test_pcl5_hpgl_vector_pd
        +guid:c975cd49-2d36-4fc2-abb0-b7ae41757b86
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('480ccb94d5789edbaa26fb3702c953a7a8f0006fc49005e878ef1b411d2bcf63', timeout=600)
    outputsaver.save_output()
