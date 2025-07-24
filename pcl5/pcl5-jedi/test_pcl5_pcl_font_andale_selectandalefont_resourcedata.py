import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using selectandalefont_resourcedata.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:selectandalefont_resourcedata.obj=3c1d3b80028227b3c898b588995b30ee09563222b900c11d220ed59f5430c34e
    +test_classification:System
    +name: test_pcl5_pcl_font_andale_selectandalefont_resourcedata
    +test:
        +title: test_pcl5_pcl_font_andale_selectandalefont_resourcedata
        +guid:36c46817-951b-4de5-9f30-9691ff5b58ca
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_andale_selectandalefont_resourcedata(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3c1d3b80028227b3c898b588995b30ee09563222b900c11d220ed59f5430c34e', timeout=600)
    outputsaver.save_output()
