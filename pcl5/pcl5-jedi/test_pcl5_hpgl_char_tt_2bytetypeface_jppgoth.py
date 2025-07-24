import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using jppgoth.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jppgoth.obj=0ef7318db51bab26f95f69706aa4e90797269b7c83950d3c37bc35f902aab54d
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_jppgoth
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_jppgoth
        +guid:c30f4d9e-823c-4b78-ba12-afeb1a9191b9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_jppgoth(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0ef7318db51bab26f95f69706aa4e90797269b7c83950d3c37bc35f902aab54d', timeout=600)
    outputsaver.save_output()
