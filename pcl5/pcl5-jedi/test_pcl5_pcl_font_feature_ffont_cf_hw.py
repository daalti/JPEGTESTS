import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ffont_cf_hw.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:ffont_cf_hw.obj=278b1cfca8fd44965c7defe545ddd79755b8386f438fe8347b2d6332d0738b5a
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_ffont_cf_hw
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_font_feature_ffont_cf_hw
        +guid:4096d2c6-a8ed-49a6-b91a-9ce688b84c17
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_ffont_cf_hw(setup_teardown, printjob, outputsaver):
    printjob.print_verify('278b1cfca8fd44965c7defe545ddd79755b8386f438fe8347b2d6332d0738b5a', timeout=600)
    outputsaver.save_output()
