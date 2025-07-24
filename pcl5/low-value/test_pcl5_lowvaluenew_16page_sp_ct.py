import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 16Page_sp_ct.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:16Page-sp_ct.obj=892e9cf01bef6147300bef961636a1fa312e1fbb8fbe6186970eb7543ff66608
    +test_classification:System
    +name: test_pcl5_lowvaluenew_16page_sp_ct
    +test:
        +title: test_pcl5_lowvaluenew_16page_sp_ct
        +guid:41684f00-68dc-4201-9822-b93d6fb8cba3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_16page_sp_ct(setup_teardown, printjob, outputsaver):
    printjob.print_verify('892e9cf01bef6147300bef961636a1fa312e1fbb8fbe6186970eb7543ff66608', timeout=600)
    outputsaver.save_output()
