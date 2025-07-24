import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 5Page_sm_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-sm_tt.obj=10f12116305378aa119c82440fc0a5bd89c311646b55308668b288bc41e60f02
    +test_classification:System
    +name: test_pcl5_highvalue_5page_sm_tt
    +test:
        +title: test_pcl5_highvalue_5page_sm_tt
        +guid:0409395a-8c3f-49ba-bf86-f0af0c6974eb
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

def test_pcl5_highvalue_5page_sm_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('10f12116305378aa119c82440fc0a5bd89c311646b55308668b288bc41e60f02', timeout=600)
    outputsaver.save_output()
