import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using cttudssm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cttudssm.obj=babd6644bad28b59c53f2accda16ef891c88d0ff1c0fe6a9e7a5b553faca9331
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_cttudssm
    +test:
        +title: test_pcl5_pcl_pclcolor_cttudssm
        +guid:272a4e42-2c46-49c3-ae86-ce0b286939a0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_cttudssm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('babd6644bad28b59c53f2accda16ef891c88d0ff1c0fe6a9e7a5b553faca9331', timeout=600)
    outputsaver.save_output()
