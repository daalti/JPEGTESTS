import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tgen_ac_8.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tgen_ac_8.obj=a0998856dacc41b98ae45491820260579360a0732509ba5f50fa1f7730195992
    +test_classification:System
    +name: test_pcl5_pcl_arb_clipping_tgen_ac_8
    +test:
        +title: test_pcl5_pcl_arb_clipping_tgen_ac_8
        +guid:d2338320-01aa-40d6-bcc6-68d902113f45
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_arb_clipping_tgen_ac_8(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a0998856dacc41b98ae45491820260579360a0732509ba5f50fa1f7730195992', timeout=600)
    outputsaver.save_output()
