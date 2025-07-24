import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using lsg55412.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:lsg55412.obj=0f04a706f7794ffb35058ace08612db5764ab4fd909bdce10c65ae2b332d298c
    +test_classification:System
    +name: test_pcl5_pcl_cpedefects_lsg55412
    +test:
        +title: test_pcl5_pcl_cpedefects_lsg55412
        +guid:06f14c59-6939-4ab9-9d1b-027381abdc2b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_cpedefects_lsg55412(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('0f04a706f7794ffb35058ace08612db5764ab4fd909bdce10c65ae2b332d298c', timeout=600,expected_jobs=4)
    outputsaver.save_output()
