import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using duplexm6.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:duplexm6.obj=e84565b2524d9a77e9d6cc9d7a846c4d80f4f6c2c81d2f00111ca48c891b59df
    +test_classification:System
    +name: test_pcl5_pcl_duplex_duplexm6
    +test:
        +title: test_pcl5_pcl_duplex_duplexm6
        +guid:eee87063-7692-4d50-a751-64b734b0cb0f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_duplex_duplexm6(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e84565b2524d9a77e9d6cc9d7a846c4d80f4f6c2c81d2f00111ca48c891b59df', timeout=600)
    outputsaver.save_output()
