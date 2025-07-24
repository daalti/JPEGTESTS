import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ft20_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ft20_300.obj=f95fcbe94c96ed028b8e0fc2b9a4a179b87d71fcfee7df97117d159be40bbc32
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_fntdes20_ft20_300
    +test:
        +title: test_pcl5_pcl_fontf_bt_fntdes20_ft20_300
        +guid:95dcdbb0-3297-4929-9922-df032bf43d55
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_fntdes20_ft20_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f95fcbe94c96ed028b8e0fc2b9a4a179b87d71fcfee7df97117d159be40bbc32', timeout=600)
    outputsaver.save_output()
