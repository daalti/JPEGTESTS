import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using overpri_1.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:overpri_1.obj=5b81d8d80cef61012435a4d8e7359fbb9db8ec99c6b7acab4a14aee2b072e174
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_overpri_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_font_feature_overpri_1
        +guid:c28fb293-3ad9-4829-88ae-0952a4c3fb4a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_overpri_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5b81d8d80cef61012435a4d8e7359fbb9db8ec99c6b7acab4a14aee2b072e174', timeout=600)
    outputsaver.save_output()
