import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 7Page_fl20gc01.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:7Page-fl20gc01.obj=217ee2d6b813c0e62ff44eb573dcf92b3512ebbddaea4091f5da0bad03b33cd5
    +test_classification:System
    +name: test_pcl5_highvalue_7page_fl20gc01
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_7page_fl20gc01
        +guid:66a96cb1-58d6-41b4-90e8-8ae1681dc2e1
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

def test_pcl5_highvalue_7page_fl20gc01(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('217ee2d6b813c0e62ff44eb573dcf92b3512ebbddaea4091f5da0bad03b33cd5',expected_jobs=3,timeout=240)
    outputsaver.save_output()
