import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_smallintverify.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-smallintverify.obj=c7cd9e8c2f40ec1bd78f7e858d26e01d3b5d9af7192a832332c2b90a07f11621
    +test_classification:System
    +name: test_pcl5_highvalue_1page_smallintverify
    +test:
        +title: test_pcl5_highvalue_1page_smallintverify
        +guid:c2e4d73b-3492-4f6a-8b34-b6742b1a15c7
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

def test_pcl5_highvalue_1page_smallintverify(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c7cd9e8c2f40ec1bd78f7e858d26e01d3b5d9af7192a832332c2b90a07f11621', timeout=600)
    outputsaver.save_output()
