import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 48Page_fp_comb.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:48Page-fp_comb.obj=046a07d4482fc952d44b16eb927605d3318027ea25b291a1f63a9fad4bd78fc4
    +test_classification:System
    +name: test_pcl5_highvalue_48page_fp_comb
    +test:
        +title: test_pcl5_highvalue_48page_fp_comb
        +guid:8727c760-b2ed-4f25-82ee-9bb1b65dfca0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_48page_fp_comb(setup_teardown, printjob, outputsaver):
    printjob.print_verify('046a07d4482fc952d44b16eb927605d3318027ea25b291a1f63a9fad4bd78fc4', timeout=600)
    outputsaver.save_output()
