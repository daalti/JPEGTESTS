import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using PageCheckMono.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:PageCheckMono.pcl=2b7b204727a79b51b1b754b845887e6128216d137e78cfda4724c99aad28f8fc
    +test_classification:System
    +name: test_pcl5_testfiles_graphic_state_pagecheckmono
    +test:
        +title: test_pcl5_testfiles_graphic_state_pagecheckmono
        +guid:4ee5bb5d-60c8-42ca-b11c-c753014f0cad
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_graphic_state_pagecheckmono(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2b7b204727a79b51b1b754b845887e6128216d137e78cfda4724c99aad28f8fc', timeout=600)
    outputsaver.save_output()
