import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using scsfangx.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:scsfangx.obj=e78be68b0c70476078124d5f8100e8e00f081293868c8dd0265d2a0d8e8044d4
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_scsfangx
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_scsfangx
        +guid:fd141b80-6ce2-424e-ac8a-15fcfaabe02e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_scsfangx(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e78be68b0c70476078124d5f8100e8e00f081293868c8dd0265d2a0d8e8044d4', timeout=600)
    outputsaver.save_output()
