import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using srcWidth0.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:srcWidth0.pcl=c18632a46d1e649caa0ca3c6188fe1fea8308a6a961fb6ed55004669b5a30240
    +test_classification:System
    +name: test_pcl5_testfiles_raster_srcwidth0
    +test:
        +title: test_pcl5_testfiles_raster_srcwidth0
        +guid:48a385de-0f3e-4190-b176-640b688eb33a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_srcwidth0(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c18632a46d1e649caa0ca3c6188fe1fea8308a6a961fb6ed55004669b5a30240', timeout=600)
    outputsaver.save_output()
