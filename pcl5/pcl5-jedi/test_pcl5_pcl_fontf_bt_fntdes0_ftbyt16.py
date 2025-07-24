import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ftbyt16.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ftbyt16.obj=adfe6d5886ef26fff2faa715e3a5df52da1097eca9d13c9dea10e69c45fa62b3
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_fntdes0_ftbyt16
    +test:
        +title: test_pcl5_pcl_fontf_bt_fntdes0_ftbyt16
        +guid:7fbfaa2c-0f43-4502-8bd0-bf25d0187a49
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_fntdes0_ftbyt16(setup_teardown, printjob, outputsaver):
    printjob.print_verify('adfe6d5886ef26fff2faa715e3a5df52da1097eca9d13c9dea10e69c45fa62b3', timeout=600)
    outputsaver.save_output()
