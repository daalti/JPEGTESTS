import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jpminch.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jpminch.obj=db8dba0a0df1ed397cdafca148654bbe422722d98ec85e358470713cd5e8dabf
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_jpminch
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_jpminch
        +guid:4a019d28-a728-4aad-a618-912c72a606f6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_jpminch(setup_teardown, printjob, outputsaver):
    printjob.print_verify('db8dba0a0df1ed397cdafca148654bbe422722d98ec85e358470713cd5e8dabf', timeout=600)
    outputsaver.save_output()
