import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using patcntrl.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:patcntrl.obj=a21442e6e84e622bc3593ec8d74b8b560d9478290aecc3417c3e10c177700711
    +test_classification:System
    +name: test_pcl5_pcl_printmod_patcntrl
    +test:
        +title: test_pcl5_pcl_printmod_patcntrl
        +guid:d5984c4f-27db-4fb3-b405-d4ec7d0f82bf
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_printmod_patcntrl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a21442e6e84e622bc3593ec8d74b8b560d9478290aecc3417c3e10c177700711', timeout=600)
    outputsaver.save_output()
