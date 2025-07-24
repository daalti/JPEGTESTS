import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using enhlogop.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:enhlogop.obj=118686439021b79e473bc08fd0e0f94c697363e32b2317656ec2ac38c4abd8ed
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_enhlogop
    +test:
        +title: test_pcl5_pcl_pclcolor_enhlogop
        +guid:061807ed-7c07-4000-b7ab-e4d0ccb5001c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_enhlogop(setup_teardown, printjob, outputsaver):
    printjob.print_verify('118686439021b79e473bc08fd0e0f94c697363e32b2317656ec2ac38c4abd8ed', timeout=600)
    outputsaver.save_output()
