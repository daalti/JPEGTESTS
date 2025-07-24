import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ttselfon.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ttselfon.obj=10fb99827ed24a6c6094581cdc56e6cad138c1550a9970e1a14821a42be6a351
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ttselfon
    +test:
        +title: test_pcl5_pcl_fontdes_ttselfon
        +guid:f4ccf55b-b15d-4c9f-b56a-0091e200e426
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ttselfon(setup_teardown, printjob, outputsaver):
    printjob.print_verify('10fb99827ed24a6c6094581cdc56e6cad138c1550a9970e1a14821a42be6a351', timeout=600)
    outputsaver.save_output()
