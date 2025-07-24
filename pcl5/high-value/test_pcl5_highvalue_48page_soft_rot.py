import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C51669606 pcl5 highvalue using 48Page_soft_rot.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:48Page-soft_rot.obj=7c93e4c009c58be7b035b8d635ec1bc9faa28af994b6747602210a3fd258899d
    +test_classification:System
    +name: test_pcl5_highvalue_48page_soft_rot
    +test:
        +title: test_pcl5_highvalue_48page_soft_rot
        +guid:805d586c-a3bb-418b-8755-9282a9566f35
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_48page_soft_rot(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7c93e4c009c58be7b035b8d635ec1bc9faa28af994b6747602210a3fd258899d', timeout=600)
    outputsaver.save_output()
