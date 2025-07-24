import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_plaintext.obj
    +test_tier: 1
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-plaintext.obj=edd23f11d767cd153a0a7e20fd218698017099fff3b0ac897e7f7428dff47cff
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_plaintext
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_lowvaluenew_1page_plaintext
        +guid:3ad008a4-eece-4824-b5b7-1c01da0e0dcf
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_plaintext(setup_teardown, printjob, outputsaver):
    # Update the test expectaion correclty if the new features are added to PCL5 which support Text and ASCII printing
    printjob.print_verify('edd23f11d767cd153a0a7e20fd218698017099fff3b0ac897e7f7428dff47cff',expected_job_state='SUCCESS', timeout=240)
    outputsaver.save_output()
