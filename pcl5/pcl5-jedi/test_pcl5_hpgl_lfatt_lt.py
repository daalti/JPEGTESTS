import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using lt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:lt.obj=c60377868accb74df9119bcde7ced3adf194b90231ef694b2605b750c9246574
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_lt
    +test:
        +title: test_pcl5_hpgl_lfatt_lt
        +guid:200cb47b-ea30-497a-81e0-e121da1fb0ec
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_lt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c60377868accb74df9119bcde7ced3adf194b90231ef694b2605b750c9246574', timeout=600)
    outputsaver.save_output()
