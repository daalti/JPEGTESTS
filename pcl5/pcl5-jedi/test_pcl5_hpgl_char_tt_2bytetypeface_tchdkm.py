import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using tchdkm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tchdkm.obj=0b3af0b92aae0d5f18674b67eb8c87e324a46dce57bb6f155bb0ca53c9c76310
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_tchdkm
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_tchdkm
        +guid:aa80180c-233a-48b1-b1e8-0bef0925d9e6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_tchdkm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0b3af0b92aae0d5f18674b67eb8c87e324a46dce57bb6f155bb0ca53c9c76310', timeout=600)
    outputsaver.save_output()
