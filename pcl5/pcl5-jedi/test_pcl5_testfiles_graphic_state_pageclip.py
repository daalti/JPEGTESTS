import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using PageClip.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:PageClip.pcl=8ee06ba8d25ba3f1899f2065eb5d694abfb59153c493545796676261f0d7ab5e
    +test_classification:System
    +name: test_pcl5_testfiles_graphic_state_pageclip
    +test:
        +title: test_pcl5_testfiles_graphic_state_pageclip
        +guid:a03c81b1-cbfa-4779-9013-fdb491534d1c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_graphic_state_pageclip(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8ee06ba8d25ba3f1899f2065eb5d694abfb59153c493545796676261f0d7ab5e', timeout=600)
    outputsaver.save_output()
