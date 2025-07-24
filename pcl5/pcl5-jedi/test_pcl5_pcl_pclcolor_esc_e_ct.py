import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using esc_e_ct.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:esc_e_ct.obj=8abe203d6c3123e8e56849864ab4959501faf2ecc8b342305b91e23547b14d11
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_esc_e_ct
    +test:
        +title: test_pcl5_pcl_pclcolor_esc_e_ct
        +guid:1796d207-41b2-4603-87c3-53b9de7282c9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_esc_e_ct(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8abe203d6c3123e8e56849864ab4959501faf2ecc8b342305b91e23547b14d11', timeout=600)
    outputsaver.save_output()
