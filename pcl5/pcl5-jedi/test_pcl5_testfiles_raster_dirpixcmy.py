import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using dirpixcmy.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dirpixcmy.pcl=39379ac984fd1a3e75d3a93796dfd6b0b03b6a882f45998db00830d18b1bfe87
    +test_classification:System
    +name: test_pcl5_testfiles_raster_dirpixcmy
    +test:
        +title: test_pcl5_testfiles_raster_dirpixcmy
        +guid:f83d095f-bcc1-49a9-adb6-f9dc68ff25f9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_dirpixcmy(setup_teardown, printjob, outputsaver):
    printjob.print_verify('39379ac984fd1a3e75d3a93796dfd6b0b03b6a882f45998db00830d18b1bfe87', timeout=600)
    outputsaver.save_output()
