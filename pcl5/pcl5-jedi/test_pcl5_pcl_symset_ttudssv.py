import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ttudssv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ttudssv.obj=fead807e4aedacdd4328e0aa09238dde0659ecc5cae81caa8b9e29c1dac36fb9
    +test_classification:System
    +name: test_pcl5_pcl_symset_ttudssv
    +test:
        +title: test_pcl5_pcl_symset_ttudssv
        +guid:a7133780-c438-4f4c-be3c-63cd60b58973
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_symset_ttudssv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fead807e4aedacdd4328e0aa09238dde0659ecc5cae81caa8b9e29c1dac36fb9', timeout=600)
    outputsaver.save_output()
