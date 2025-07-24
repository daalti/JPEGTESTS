import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using pges.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pges.pcl=47f25f20925832b19155adb30bc6d64865ee6adde0afa58ac1f7d04cac287d37
    +test_classification:System
    +name: test_pcl5_testfiles_color_pges
    +test:
        +title: test_pcl5_testfiles_color_pges
        +guid:9c1b24e5-14d8-4c38-a52f-e655f44ba2e7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_color_pges(setup_teardown, printjob, outputsaver):
    printjob.print_verify('47f25f20925832b19155adb30bc6d64865ee6adde0afa58ac1f7d04cac287d37', timeout=600)
    outputsaver.save_output()
