import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using srcHeight0.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:srcHeight0.pcl=7698cecd6060947d21333ee92ed39ac66a9990ba8eee6a983ea7478080702a50
    +test_classification:System
    +name: test_pcl5_testfiles_raster_srcheight0
    +test:
        +title: test_pcl5_testfiles_raster_srcheight0
        +guid:ac132f1e-b0cb-43ab-b55b-81ecc23992b8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_srcheight0(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7698cecd6060947d21333ee92ed39ac66a9990ba8eee6a983ea7478080702a50', timeout=600)
    outputsaver.save_output()
