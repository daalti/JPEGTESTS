import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplx5c.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:duplx5c.obj=2a3914c70ac0278769747ed884b085473018be5dcdd78e8c70720ac911623eba
    +test_classification:System
    +name: test_pcl5_pcl_duplex_duplx5c
    +test:
        +title: test_pcl5_pcl_duplex_duplx5c
        +guid:ee451dd2-2490-43b0-87f1-91ac0bc61877
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_duplex_duplx5c(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2a3914c70ac0278769747ed884b085473018be5dcdd78e8c70720ac911623eba', timeout=600)
    outputsaver.save_output()
