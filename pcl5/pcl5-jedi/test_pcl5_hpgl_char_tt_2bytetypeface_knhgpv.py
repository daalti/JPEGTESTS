import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knhgpv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knhgpv.obj=1f92baeb801ac2448e8e4b9491d67288461596f9e98101e9439644327dcce9c2
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knhgpv
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knhgpv
        +guid:0a0d050e-a948-42b5-a00d-2fc205f8299a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knhgpv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1f92baeb801ac2448e8e4b9491d67288461596f9e98101e9439644327dcce9c2', timeout=600)
    outputsaver.save_output()
