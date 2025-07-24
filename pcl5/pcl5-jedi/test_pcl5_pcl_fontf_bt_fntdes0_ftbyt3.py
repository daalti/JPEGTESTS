import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ftbyt3.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ftbyt3.obj=fedf6767aeeac933097c0c0b55367734cb7f6735c9f09faea23c8f15ac59aa0e
    +test_classification:System
    +name: test_pcl5_pcl_fontf_bt_fntdes0_ftbyt3
    +test:
        +title: test_pcl5_pcl_fontf_bt_fntdes0_ftbyt3
        +guid:9679870e-a590-44d3-9487-f147b605b102
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_bt_fntdes0_ftbyt3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fedf6767aeeac933097c0c0b55367734cb7f6735c9f09faea23c8f15ac59aa0e', timeout=600)
    outputsaver.save_output()
