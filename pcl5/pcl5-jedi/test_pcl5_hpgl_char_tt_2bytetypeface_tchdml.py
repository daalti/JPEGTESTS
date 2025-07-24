import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using tchdml.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tchdml.obj=1519f9c8f62a20fed5914c635276044dbfb6ecddd345c62c444582a947c600d3
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_tchdml
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_tchdml
        +guid:cb87e2e7-d004-48bf-9e91-5b1b75b6223d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_tchdml(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1519f9c8f62a20fed5914c635276044dbfb6ecddd345c62c444582a947c600d3', timeout=600)
    outputsaver.save_output()
