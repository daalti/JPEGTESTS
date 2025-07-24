import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ffont_cf.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:ffont_cf.obj=2536aef0c2d4a9d93d79c77f23328dce84017419f126202bec530f8a7faa79fa
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_ffont_cf
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_font_feature_ffont_cf
        +guid:7983a20c-ab34-49c5-855c-65371f8338af
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_ffont_cf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2536aef0c2d4a9d93d79c77f23328dce84017419f126202bec530f8a7faa79fa', timeout=600)
    outputsaver.save_output()
