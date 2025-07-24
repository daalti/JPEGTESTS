import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using indxplan2.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:indxplan2.pcl=055b7fbb0f71d3c7fc04f5a2ce6e72a05e6f599f7bfc25f7e8104b8147f4f630
    +test_classification:System
    +name: test_pcl5_testfiles_raster_indxplan2
    +test:
        +title: test_pcl5_testfiles_raster_indxplan2
        +guid:a1c26d40-a3b7-4bfe-bca3-fbbb887d905b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_indxplan2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('055b7fbb0f71d3c7fc04f5a2ce6e72a05e6f599f7bfc25f7e8104b8147f4f630', timeout=600)
    outputsaver.save_output()
