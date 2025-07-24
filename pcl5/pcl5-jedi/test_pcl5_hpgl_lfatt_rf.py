import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using rf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rf.obj=0489e2221e87404fdeb83d44efcf2b6d1675d9c192f6c9091f319d13392b48e6
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_rf
    +test:
        +title: test_pcl5_hpgl_lfatt_rf
        +guid:39585602-9567-47b0-b693-0f063b82861d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_rf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0489e2221e87404fdeb83d44efcf2b6d1675d9c192f6c9091f319d13392b48e6', timeout=600)
    outputsaver.save_output()
