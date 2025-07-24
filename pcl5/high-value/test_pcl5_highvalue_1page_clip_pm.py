import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_clip_pm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-clip_pm.obj=4a0f46abc1cb3616c725f8c255dfa89a07b84110e37a4f74a8f7f265daa6752b
    +test_classification:System
    +name: test_pcl5_highvalue_1page_clip_pm
    +test:
        +title: test_pcl5_highvalue_1page_clip_pm
        +guid:f3e4dc30-ba84-45e5-9bcd-329144b8167b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_1page_clip_pm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4a0f46abc1cb3616c725f8c255dfa89a07b84110e37a4f74a8f7f265daa6752b')
    outputsaver.save_output()
