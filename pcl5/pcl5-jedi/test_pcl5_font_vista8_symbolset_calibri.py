import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 font using Calibri.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:Calibri.pcl=9035740c42051cdd90e3f715eaf3581f0c714c9722f02142b42dd4aad3b8d501
    +test_classification:System
    +name: test_pcl5_font_vista8_symbolset_calibri
    +test:
        +title: test_pcl5_font_vista8_symbolset_calibri
        +guid:2ac97f06-364e-4f61-960d-72e7b42ac966
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_font_vista8_symbolset_calibri(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9035740c42051cdd90e3f715eaf3581f0c714c9722f02142b42dd4aad3b8d501', timeout=600)
    outputsaver.save_output()
