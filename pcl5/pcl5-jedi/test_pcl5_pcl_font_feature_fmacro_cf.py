import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fmacro_cf.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:fmacro_cf.obj=fdd2646e64ed67ae4bc2223e65099055091c3e3fd70942498f8969ffbaf5a1f2
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_fmacro_cf
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_font_feature_fmacro_cf
        +guid:2c5d19b9-f46b-4f91-a922-988da6e5c8b9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_fmacro_cf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fdd2646e64ed67ae4bc2223e65099055091c3e3fd70942498f8969ffbaf5a1f2', timeout=600)
    outputsaver.save_output()
