import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jpminchx.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jpminchx.obj=fc7f11462113124a74eeeebe8f886e66ad7a914a0634f9ab70ce51f4d631eac4
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_jpminchx
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_jpminchx
        +guid:d7266f82-d04c-422f-af34-59db88c36962
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_jpminchx(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fc7f11462113124a74eeeebe8f886e66ad7a914a0634f9ab70ce51f4d631eac4', timeout=600)
    outputsaver.save_output()
