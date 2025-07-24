import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knhgsf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knhgsf.obj=8289934308ad3d77dd0a2aed5d2d2f784e26dddfebb8207ff1c94dd006daba02
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knhgsf
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knhgsf
        +guid:291e4c0d-0ddc-4fb4-b304-3a671d8d0ad3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knhgsf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8289934308ad3d77dd0a2aed5d2d2f784e26dddfebb8207ff1c94dd006daba02', timeout=600)
    outputsaver.save_output()
