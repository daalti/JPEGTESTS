import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplexm1.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:duplexm1.obj=2642f51d4ae725be11414687afddf83399ccd4f72aa4c3b0d4fe0b9a4e568c8e
    +test_classification:System
    +name: test_pcl5_pcl_duplex_duplexm1
    +test:
        +title: test_pcl5_pcl_duplex_duplexm1
        +guid:f15a2815-051f-44c6-ab8d-9d22a1c22d08
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_duplex_duplexm1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2642f51d4ae725be11414687afddf83399ccd4f72aa4c3b0d4fe0b9a4e568c8e', timeout=600)
    outputsaver.save_output()
