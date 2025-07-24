import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 font using camcal_underline_res.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:camcal_underline_res.obj=b4995099a645973c3229dc7cbf87c6a2cbed6c1d6f6a1bd3f9f29356aa106087
    +test_classification:System
    +name: test_pcl5_font_vista8_camcal_underline_res
    +test:
        +title: test_pcl5_font_vista8_camcal_underline_res
        +guid:ba8d878c-b302-44e3-9e9d-5b6414c2aadc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_font_vista8_camcal_underline_res(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b4995099a645973c3229dc7cbf87c6a2cbed6c1d6f6a1bd3f9f29356aa106087', timeout=600)
    outputsaver.save_output()
