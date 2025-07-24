import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using rp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:rp.obj=f82f08a4b4b32028a49eb501fef19d6b393d5a8ce961feeb0c66d1b788c03064
    +test_classification:System
    +name: test_pcl5_hpgl_cfgstat_rp
    +test:
        +title: test_pcl5_hpgl_cfgstat_rp
        +guid:d074d586-d3c2-4b8b-88e6-8ede0c5384b1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_cfgstat_rp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f82f08a4b4b32028a49eb501fef19d6b393d5a8ce961feeb0c66d1b788c03064', timeout=600)
    outputsaver.save_output()
