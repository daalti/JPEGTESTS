import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using dv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dv.obj=4e3e54ac90a45a1ddab95979ec0268bcd2af698b06473a5c1642e3295526a022
    +test_classification:System
    +name: test_pcl5_hpgl_char_dv
    +test:
        +title: test_pcl5_hpgl_char_dv
        +guid:67964320-6639-40ca-8b91-032b601e6f55
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_dv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4e3e54ac90a45a1ddab95979ec0268bcd2af698b06473a5c1642e3295526a022', timeout=600)
    outputsaver.save_output()
