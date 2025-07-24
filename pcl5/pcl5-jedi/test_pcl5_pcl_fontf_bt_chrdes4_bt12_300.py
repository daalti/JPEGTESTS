import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using bt12_300.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bt12_300.obj=cc7359b742740e172e387a271d73d667072c0da2ca2777048c515ccd80555fed
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_chrdes4_bt12_300
    +test:
        +title: test_pcl5_pcl_fontf_bt_chrdes4_bt12_300
        +guid:970e8cdf-915e-42ed-9a60-d320f37bc708
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_chrdes4_bt12_300(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cc7359b742740e172e387a271d73d667072c0da2ca2777048c515ccd80555fed', timeout=600)
    outputsaver.save_output()
