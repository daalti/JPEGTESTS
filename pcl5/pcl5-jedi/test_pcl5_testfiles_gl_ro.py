import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ro.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ro.pcl=577b0ae2e3d78cdd470d9b2538de6bb36b2847dc29022a73a230f257099b5ed4
    +test_classification:System
    +name: test_pcl5_testfiles_gl_ro
    +test:
        +title: test_pcl5_testfiles_gl_ro
        +guid:5cbd3932-b7b4-406c-8e51-77e66587f833
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_ro(setup_teardown, printjob, outputsaver):
    printjob.print_verify('577b0ae2e3d78cdd470d9b2538de6bb36b2847dc29022a73a230f257099b5ed4', timeout=600)
    outputsaver.save_output()
