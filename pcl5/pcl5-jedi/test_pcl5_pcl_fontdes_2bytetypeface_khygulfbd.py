import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khygulfbd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khygulfbd.obj=f8549634e915fad8a93987dff3c41b377b09cb401e3996fd4ac0523d083ccf28
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khygulfbd
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khygulfbd
        +guid:c1ad97c8-3f08-45e4-bc25-31f0fda5823f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khygulfbd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f8549634e915fad8a93987dff3c41b377b09cb401e3996fd4ac0523d083ccf28', timeout=600)
    outputsaver.save_output()
