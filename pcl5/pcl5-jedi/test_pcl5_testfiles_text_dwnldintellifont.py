import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using dwnldIntellifont.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dwnldIntellifont.pcl=cdae612fd4ba73f2a9d3021208ac8cef3548f3a0745d6a620b3ace21d1e95327
    +test_classification:System
    +name: test_pcl5_testfiles_text_dwnldintellifont
    +test:
        +title: test_pcl5_testfiles_text_dwnldintellifont
        +guid:a05ea749-225f-43a0-939e-00fee6f44d3f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_text_dwnldintellifont(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cdae612fd4ba73f2a9d3021208ac8cef3548f3a0745d6a620b3ace21d1e95327', timeout=600)
    outputsaver.save_output()
