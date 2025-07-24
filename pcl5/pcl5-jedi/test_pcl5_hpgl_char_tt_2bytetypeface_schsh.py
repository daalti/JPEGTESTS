import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using schsh.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:schsh.obj=62f1b7db75ec72753d3a67dd9b044b45afe1ae59eb372c57e7571f301f66983f
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_schsh
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_schsh
        +guid:80662994-70e6-4e5b-be6d-38af17b91fb0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_schsh(setup_teardown, printjob, outputsaver):
    printjob.print_verify('62f1b7db75ec72753d3a67dd9b044b45afe1ae59eb372c57e7571f301f66983f', timeout=600)
    outputsaver.save_output()
