import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using pmpe.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pmpe.pcl=6391756a4c76528152d963dbf1ee537c9c4190404df6dd08a5983ce1e5ca77fc
    +test_classification:System
    +name: test_pcl5_testfiles_gl_pm_pe
    +test:
        +title: test_pcl5_testfiles_gl_pm_pe
        +guid:fe8030d5-5437-4a7a-9f04-5fec44c13904
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_pm_pe(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6391756a4c76528152d963dbf1ee537c9c4190404df6dd08a5983ce1e5ca77fc', timeout=600)
    outputsaver.save_output()
