import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ad.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ad.obj=5c5898f35aa6b04d8038f56c0e4d31d7914706288001f565b4b85026d3bdeddf
    +test_classification:System
    +name: test_pcl5_hpgl_char_ad
    +test:
        +title: test_pcl5_hpgl_char_ad
        +guid:47952a1d-778c-48a1-b390-02caf3bd18f3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_ad(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5c5898f35aa6b04d8038f56c0e4d31d7914706288001f565b4b85026d3bdeddf', timeout=600)
    outputsaver.save_output()
