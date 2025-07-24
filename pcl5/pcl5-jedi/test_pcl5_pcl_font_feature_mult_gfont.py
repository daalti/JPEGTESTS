import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using mult_gfont.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:mult_gfont.obj=85ea5840a6b4e6e115d6a2806d8f265cc4109b3facb493d765f4aff67611ba45
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_mult_gfont
    +test:
        +title: test_pcl5_pcl_font_feature_mult_gfont
        +guid:3f61817f-729c-4bb1-b779-16ec2605817b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_mult_gfont(setup_teardown, printjob, outputsaver):
    printjob.print_verify('85ea5840a6b4e6e115d6a2806d8f265cc4109b3facb493d765f4aff67611ba45', timeout=600)
    outputsaver.save_output()
