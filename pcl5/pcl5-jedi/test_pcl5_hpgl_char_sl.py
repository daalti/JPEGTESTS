import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sl.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sl.obj=8c80b332b15c890ca521e6aecf21882a3aaeb41819f1c2efc16e3ffd58fd8554
    +test_classification:System
    +name: test_pcl5_hpgl_char_sl
    +test:
        +title: test_pcl5_hpgl_char_sl
        +guid:361836f8-0db0-40ad-bde7-8c0888cdc605
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_sl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8c80b332b15c890ca521e6aecf21882a3aaeb41819f1c2efc16e3ffd58fd8554', timeout=600)
    outputsaver.save_output()
