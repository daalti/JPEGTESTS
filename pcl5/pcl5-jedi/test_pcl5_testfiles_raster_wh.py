import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using wh.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:wh.pcl=d3f82c7ef977f4d90527c49d1fbcc1cde96a9fedbeeda1cbc0905d9b3eda1192
    +test_classification:System
    +name: test_pcl5_testfiles_raster_wh
    +test:
        +title: test_pcl5_testfiles_raster_wh
        +guid:258e9861-a689-4f64-bf1d-7244d6bb844e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_wh(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d3f82c7ef977f4d90527c49d1fbcc1cde96a9fedbeeda1cbc0905d9b3eda1192', timeout=600)
    outputsaver.save_output()
