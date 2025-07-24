import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using patCtl.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:patCtl.pcl=be5acdd987557414974c42df898191a128582f063f7c511450a955d30b0ad6da
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_patctl
    +test:
        +title: test_pcl5_testfiles_pattern_patctl
        +guid:cc9721a7-ad06-46d2-a8ee-beeaac861349
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_patctl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('be5acdd987557414974c42df898191a128582f063f7c511450a955d30b0ad6da',timeout=600)
    outputsaver.save_output()
