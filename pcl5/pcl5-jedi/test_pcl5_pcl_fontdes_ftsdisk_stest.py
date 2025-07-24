import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using stest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:stest.obj=eccbfee9387480daa8bb4fd470c1d19b53c18ff9a68d326740836bf9357f1412
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_stest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_stest
        +guid:62bf72f3-fcc5-43e3-a644-e833860aa3bc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_stest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('eccbfee9387480daa8bb4fd470c1d19b53c18ff9a68d326740836bf9357f1412', timeout=600)
    outputsaver.save_output()
