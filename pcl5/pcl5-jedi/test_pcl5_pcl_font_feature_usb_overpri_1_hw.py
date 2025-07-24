import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_overpri_1_hw.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:usb_overpri_1_hw.obj=92a96bbec4dc8947e6aff15071440925a04aa2de599982f3196b645ac39d4129
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_overpri_1_hw
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_font_feature_usb_overpri_1_hw
        +guid:51acea0c-0754-48f4-9ba3-920943e442ff
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_overpri_1_hw(setup_teardown, printjob, outputsaver):
    printjob.print_verify('92a96bbec4dc8947e6aff15071440925a04aa2de599982f3196b645ac39d4129', expected_jobs=2, timeout=600)
    outputsaver.save_output()
