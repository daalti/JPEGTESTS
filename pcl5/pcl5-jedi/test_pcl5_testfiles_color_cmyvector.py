import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using cmyVector.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cmyVector.pcl=d36f8d2cb6474d55c7609273364cc865cec762c47d617723b094cda79db46b62
    +test_classification:System
    +name: test_pcl5_testfiles_color_cmyvector
    +test:
        +title: test_pcl5_testfiles_color_cmyvector
        +guid:5bd14f2b-f945-4dc1-a76a-c57074fb87df
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_color_cmyvector(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d36f8d2cb6474d55c7609273364cc865cec762c47d617723b094cda79db46b62', timeout=600)
    outputsaver.save_output()
