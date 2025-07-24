import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30474176 pcl5 highvalue using 59Page_lsg52951.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:59Page-lsg52951.obj=7a12bc56ebf53ac34cb0b4a19664ac052d26d2e829c79dba9d687454c7e36558
    +test_classification:System
    +name: test_pcl5_highvalue_59page_lsg52951
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_59page_lsg52951
        +guid:e6d98802-e6c6-4caf-9106-3f2364c68004
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:720
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_59page_lsg52951(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('7a12bc56ebf53ac34cb0b4a19664ac052d26d2e829c79dba9d687454c7e36558', timeout=720)
    outputsaver.save_output()
