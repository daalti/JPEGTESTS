import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using underline.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:underline.pcl=9c4900b0d1b61033f61b6df77786bbc84594637c4f0053e36c3ae56bb97bf3fe
    +test_classification:System
    +name: test_pcl5_testfiles_misc_underline
    +test:
        +title: test_pcl5_testfiles_misc_underline
        +guid:6b1c7ce0-1137-4b23-a16c-14b5ec8abecd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_underline(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9c4900b0d1b61033f61b6df77786bbc84594637c4f0053e36c3ae56bb97bf3fe', timeout=600)
    outputsaver.save_output()
