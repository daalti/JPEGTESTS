import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using tchpml.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tchpml.obj=5ac4abe2f5d7ecab3ea5fb25428b15c1a172bcf04c8f5951596818706c320deb
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_tchpml
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_tchpml
        +guid:6d5cb24a-274d-4e45-933e-1a587a4e15d4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_tchpml(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5ac4abe2f5d7ecab3ea5fb25428b15c1a172bcf04c8f5951596818706c320deb', timeout=600)
    outputsaver.save_output()
