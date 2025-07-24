import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 16Page_uline5.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:16Page-uline5.obj=8cd600a9aa0adaf05357f44d56e00755afe01d2f093584cb4c72591381baddcb
    +test_classification:System
    +name: test_pcl5_highvalue_16page_uline5
    +test:
        +title: test_pcl5_highvalue_16page_uline5
        +guid:76be291a-8a14-4617-b2a7-195a7d4d413d
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

def test_pcl5_highvalue_16page_uline5(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('8cd600a9aa0adaf05357f44d56e00755afe01d2f093584cb4c72591381baddcb',timeout=600)
    outputsaver.save_output()
