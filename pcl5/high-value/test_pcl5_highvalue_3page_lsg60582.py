import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 3Page_lsg60582.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-lsg60582.obj=a29fcaec4b06fc7413e07ba1e63f63c73df924bd35427563021f6dd0ad039bb2
    +test_classification:System
    +name: test_pcl5_highvalue_3page_lsg60582
    +test:
        +title: test_pcl5_highvalue_3page_lsg60582
        +guid:bb057107-828a-40b2-8e22-5330d1755e79
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

def test_pcl5_highvalue_3page_lsg60582(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a29fcaec4b06fc7413e07ba1e63f63c73df924bd35427563021f6dd0ad039bb2', timeout=600)
    outputsaver.save_output()
