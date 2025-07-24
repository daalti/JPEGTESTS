import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kdotcpy.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kdotcpy.obj=6d11e8076569a514ac9eb3ffa1bd53e38140626db15cbb418ec5703f974fad50
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kdotcpy
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kdotcpy
        +guid:769d8dc4-9a09-4151-a7c5-014a13dcb2de
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kdotcpy(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6d11e8076569a514ac9eb3ffa1bd53e38140626db15cbb418ec5703f974fad50', timeout=600)
    outputsaver.save_output()
