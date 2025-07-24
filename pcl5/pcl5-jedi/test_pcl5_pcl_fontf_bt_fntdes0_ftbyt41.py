import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ftbyt41.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ftbyt41.obj=f28315372fdce01ff046e9c50c7b916d47ffea5a3331bd3b4c1619805b664e31
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_fntdes0_ftbyt41
    +test:
        +title: test_pcl5_pcl_fontf_bt_fntdes0_ftbyt41
        +guid:bb2d39dc-6d0a-442f-82b8-584803cb4eda
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_fntdes0_ftbyt41(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f28315372fdce01ff046e9c50c7b916d47ffea5a3331bd3b4c1619805b664e31', timeout=600)
    outputsaver.save_output()
