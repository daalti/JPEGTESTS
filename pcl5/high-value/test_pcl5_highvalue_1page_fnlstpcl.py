import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_fnlstpcl.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-fnlstpcl.obj=d678eb55804b489c107ce21e6b682ee68cd52167d7c32217f196bf7f02a69208
    +test_classification:System
    +name: test_pcl5_highvalue_1page_fnlstpcl
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_fnlstpcl
        +guid:4e8ce777-8339-47ac-963d-ed66818a5fee
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

def test_pcl5_highvalue_1page_fnlstpcl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d678eb55804b489c107ce21e6b682ee68cd52167d7c32217f196bf7f02a69208', timeout=600)
    outputsaver.save_output()
