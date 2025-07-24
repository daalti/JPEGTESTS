import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 font using Cambria.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:Cambria.pcl=d64282aa399e6726a555bd0a9bffe974e21328aa014ff0d37e82c142b79ae521
    +test_classification:System
    +name: test_pcl5_font_vista8_symbolset_cambria
    +test:
        +title: test_pcl5_font_vista8_symbolset_cambria
        +guid:ae003f00-5a4e-4ecb-ab72-240298861818
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_font_vista8_symbolset_cambria(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d64282aa399e6726a555bd0a9bffe974e21328aa014ff0d37e82c142b79ae521', timeout=600)
    outputsaver.save_output()
