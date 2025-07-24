import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 19Page_fontcomp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:19Page-fontcomp.obj=5d0a7ea034b50ea1e30834f78274de5d86c93661823aaffc19290009764113a2
    +test_classification:System
    +name: test_pcl5_highvalue_19page_fontcomp
    +test:
        +title: test_pcl5_highvalue_19page_fontcomp
        +guid:34344d93-dc73-4402-bbe8-ba550a397c0a
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

def test_pcl5_highvalue_19page_fontcomp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5d0a7ea034b50ea1e30834f78274de5d86c93661823aaffc19290009764113a2', timeout=600)
    outputsaver.save_output()
