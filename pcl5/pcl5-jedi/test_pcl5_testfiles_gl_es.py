import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using es.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:es.pcl=7fbd5cb5a30d22e5cbcf1bfa41a1c199e64c006fdd00a53e17035cc9c6c3a0c3
    +test_classification:System
    +name: test_pcl5_testfiles_gl_es
    +test:
        +title: test_pcl5_testfiles_gl_es
        +guid:1354753b-408f-4cdd-bb4e-e5aa6f018b66
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_es(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7fbd5cb5a30d22e5cbcf1bfa41a1c199e64c006fdd00a53e17035cc9c6c3a0c3', timeout=600)
    outputsaver.save_output()
