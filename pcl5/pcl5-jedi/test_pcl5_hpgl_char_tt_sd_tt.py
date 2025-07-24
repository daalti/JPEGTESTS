import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sd_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sd_tt.obj=5f0fd333cc8cce1ea8c1e027592844632d9b01de6652b7cfde8f0b9e13b350f4
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_sd_tt
    +test:
        +title: test_pcl5_hpgl_char_tt_sd_tt
        +guid:9f2ce1df-180f-4a68-a269-e89e19b79f10
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_sd_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5f0fd333cc8cce1ea8c1e027592844632d9b01de6652b7cfde8f0b9e13b350f4', timeout=600)
    outputsaver.save_output()
