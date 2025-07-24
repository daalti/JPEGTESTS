import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using moreplane.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:moreplane.pcl=c335174fff32285a9b13db50507f36b0345f9460c519b18adf052db02374183b
    +test_classification:System
    +name: test_pcl5_testfiles_raster_moreplane
    +test:
        +title: test_pcl5_testfiles_raster_moreplane
        +guid:7e97f705-3c2a-47cd-b2be-fe4443022741
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_moreplane(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c335174fff32285a9b13db50507f36b0345f9460c519b18adf052db02374183b', timeout=600)
    outputsaver.save_output()
