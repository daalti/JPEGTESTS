import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using di.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:di.pcl=c37aa01ed2be359ec423e4cf70298a047558b5d84d525240a9902a30900e0f5a
    +test_classification:System
    +name: test_pcl5_testfiles_gl_di
    +test:
        +title: test_pcl5_testfiles_gl_di
        +guid:1cca2b71-b9f4-472f-b1e8-8a14ccafa8da
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_di(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c37aa01ed2be359ec423e4cf70298a047558b5d84d525240a9902a30900e0f5a', timeout=600)
    outputsaver.save_output()
