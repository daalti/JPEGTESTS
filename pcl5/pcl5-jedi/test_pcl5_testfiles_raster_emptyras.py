import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using emptyras.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:emptyras.obj=c1f8809417463e83041a75c78fa80c15d68e5a475ee74c523054e0b7bfb37a6d
    +test_classification:System
    +name: test_pcl5_testfiles_raster_emptyras
    +test:
        +title: test_pcl5_testfiles_raster_emptyras
        +guid:a26b5932-86db-4f78-94b5-6dca1f508b9c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_emptyras(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c1f8809417463e83041a75c78fa80c15d68e5a475ee74c523054e0b7bfb37a6d', timeout=600)
    outputsaver.save_output()
