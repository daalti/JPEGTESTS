import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 10Page_qp60gb01.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:10Page-qp60gb01.obj=58a4b1abbf93755a9520265366d9b1b87f6d7d7c1ea0cb9b9337527905680dff
    +test_classification:System
    +name: test_pcl5_highvalue_10page_qp60gb01
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_10page_qp60gb01
        +guid:1f95dfc2-6e8c-4ae8-9033-124bb38f5083
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

def test_pcl5_highvalue_10page_qp60gb01(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('58a4b1abbf93755a9520265366d9b1b87f6d7d7c1ea0cb9b9337527905680dff', timeout=720,expected_jobs=5)
    outputsaver.save_output()
