import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using pc_ct.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pc_ct.obj=6d37f40f554cd73d454c0fc3aff44854e85f264e33e215c4b0df5b10ccc39526
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_pc_ct
    +test:
        +title: test_pcl5_pcl_pclcolor_pc_ct
        +guid:6f965e06-fc01-4892-9341-f62c6131598d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_pc_ct(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6d37f40f554cd73d454c0fc3aff44854e85f264e33e215c4b0df5b10ccc39526', timeout=600)
    outputsaver.save_output()
