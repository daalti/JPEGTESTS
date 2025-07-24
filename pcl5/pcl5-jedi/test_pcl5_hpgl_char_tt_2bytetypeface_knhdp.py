import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knhdp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knhdp.obj=dd5718d66bcb4f66f5d6dfad7aa97f8e89eecec88d9950ae32a5060b94cd4e2f
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knhdp
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knhdp
        +guid:e533b034-361c-43ef-a7fa-61a374bd2297
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knhdp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dd5718d66bcb4f66f5d6dfad7aa97f8e89eecec88d9950ae32a5060b94cd4e2f', timeout=600)
    outputsaver.save_output()
