import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tgen_ac_9.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tgen_ac_9.obj=60e5dceab3916f4e6db2bd3f1c10001ee69925815a35ecc6ddd055c75d242d48
    +test_classification:System
    +name: test_pcl5_pcl_arb_clipping_tgen_ac_9
    +test:
        +title: test_pcl5_pcl_arb_clipping_tgen_ac_9
        +guid:eb50b306-a5c3-47e1-9ea2-33e3329a8628
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_arb_clipping_tgen_ac_9(setup_teardown, printjob, outputsaver):
    printjob.print_verify('60e5dceab3916f4e6db2bd3f1c10001ee69925815a35ecc6ddd055c75d242d48', timeout=600)
    outputsaver.save_output()
