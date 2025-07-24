import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using indxplan1.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:indxplan1.pcl=ad92d2936d017b0b0c5b36e5a5aa93d137a3f1e69fbba9bd19065dfc4c9091e6
    +test_classification:System
    +name: test_pcl5_testfiles_raster_indxplan1
    +test:
        +title: test_pcl5_testfiles_raster_indxplan1
        +guid:e379d15c-b8ae-45a5-b3fe-c82a5c5bc89d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_indxplan1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ad92d2936d017b0b0c5b36e5a5aa93d137a3f1e69fbba9bd19065dfc4c9091e6', timeout=600)
    outputsaver.save_output()
