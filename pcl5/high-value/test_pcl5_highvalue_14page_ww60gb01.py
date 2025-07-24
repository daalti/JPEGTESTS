import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 14Page_ww60gb01.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:420
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:14Page-ww60gb01.obj=73140e3ba3a85dfcd0cacbcfa3126f612f158ecfdd03ad055492046f38252b3c
    +test_classification:System
    +name: test_pcl5_highvalue_14page_ww60gb01
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_14page_ww60gb01
        +guid:0c113bd9-2afd-407b-a190-56ed31730299
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_14page_ww60gb01(setup_teardown, printjob, outputsaver):
    printjob.print_verify('73140e3ba3a85dfcd0cacbcfa3126f612f158ecfdd03ad055492046f38252b3c',timeout=300,expected_jobs=3)
    outputsaver.save_output()
