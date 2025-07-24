import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using missing.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:missing.pcl=43a1208db931e3d1428e2a3485fa2ee951288caa9e8e002eda3045592b6f1ea5
    +test_classification:System
    +name: test_pcl5_testfiles_raster_missing
    +test:
        +title: test_pcl5_testfiles_raster_missing
        +guid:fbb8d4da-2583-40eb-8fe4-120179f3a1b3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_missing(setup_teardown, printjob, outputsaver):
    printjob.print_verify('43a1208db931e3d1428e2a3485fa2ee951288caa9e8e002eda3045592b6f1ea5', timeout=600)
    outputsaver.save_output()
