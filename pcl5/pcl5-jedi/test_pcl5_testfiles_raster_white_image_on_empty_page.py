import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using white_image_on_empty_page.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:white_image_on_empty_page.pcl=8c6dfb51143dc022c6bb7e69765636701f3235bf966bee91f9618b3d819e7f9b
    +test_classification:System
    +name: test_pcl5_testfiles_raster_white_image_on_empty_page
    +test:
        +title: test_pcl5_testfiles_raster_white_image_on_empty_page
        +guid:e111d44b-7dee-4ba7-a195-615c3f2eb5fa
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_white_image_on_empty_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8c6dfb51143dc022c6bb7e69765636701f3235bf966bee91f9618b3d819e7f9b', timeout=600)
    outputsaver.save_output()
