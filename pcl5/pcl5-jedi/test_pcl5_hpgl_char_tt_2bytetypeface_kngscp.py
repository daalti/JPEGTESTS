import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using kngscp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kngscp.obj=7cdc9243bb636a76a2b10a662d06b181c07fd3bcbc752f38de8fb43f66731751
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_kngscp
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_kngscp
        +guid:9207871a-a9aa-4c07-a278-32f22b9bf296
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_kngscp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7cdc9243bb636a76a2b10a662d06b181c07fd3bcbc752f38de8fb43f66731751', timeout=600)
    outputsaver.save_output()
