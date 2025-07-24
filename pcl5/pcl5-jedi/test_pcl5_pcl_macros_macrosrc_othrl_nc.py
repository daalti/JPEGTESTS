import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using othrl_nc.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:othrl_nc.obj=8bea6498737b0738c19aba5636fcc3aa7a4cafd1219c3281a0c66cc2c76b04dc
    +test_classification:System
    +name: test_pcl5_pcl_macros_macrosrc_othrl_nc
    +test:
        +title: test_pcl5_pcl_macros_macrosrc_othrl_nc
        +guid:b15599e4-b69f-4e52-bdb7-d176682d5ffd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_macros_macrosrc_othrl_nc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8bea6498737b0738c19aba5636fcc3aa7a4cafd1219c3281a0c66cc2c76b04dc', timeout=600)
    outputsaver.save_output()
