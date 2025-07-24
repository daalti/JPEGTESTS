import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fmacro_cf_hw.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:fmacro_cf_hw.obj=62eda5337b7c2f0bf18898bf0e660b4e1c68befb22da2cbea6f65338993f9998
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_fmacro_cf_hw
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_font_feature_fmacro_cf_hw
        +guid:e8b8705b-cf76-4ab2-b254-91b811d730fe
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_fmacro_cf_hw(setup_teardown, printjob, outputsaver):
    printjob.print_verify('62eda5337b7c2f0bf18898bf0e660b4e1c68befb22da2cbea6f65338993f9998', timeout=600)
    outputsaver.save_output()
