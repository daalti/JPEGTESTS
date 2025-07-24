import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using clrwheel.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:clrwheel.pcl=f15df1f18077bc61cdc3592c5b0d3277b1fe95bd426cf451b5915fc67e0cb9ef
    +test_classification:System
    +name: test_pcl5_testfiles_raster_clrwheel
    +test:
        +title: test_pcl5_testfiles_raster_clrwheel
        +guid:8b736fbe-cbba-4c62-b35d-906790b55ee5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_clrwheel(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f15df1f18077bc61cdc3592c5b0d3277b1fe95bd426cf451b5915fc67e0cb9ef', timeout=600)
    outputsaver.save_output()
