import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt5_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt5_300.obj=8339f0740154a03037615697f2a9a0cd10f9bdd386bf987deeca3607a8fee466
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt5_300
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt5_300
        +guid:cb9532cd-e0b8-4abe-8bdd-1716e3191083
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt5_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8339f0740154a03037615697f2a9a0cd10f9bdd386bf987deeca3607a8fee466', timeout=600)
    outputsaver.save_output()
