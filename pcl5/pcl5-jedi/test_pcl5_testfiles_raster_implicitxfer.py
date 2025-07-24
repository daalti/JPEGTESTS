import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using implicitxfer.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:implicitxfer.pcl=c522874feab6a87ca0d0da0add092e639a9dc49323a00a652a967d68e8471837
    +test_classification:System
    +name: test_pcl5_testfiles_raster_implicitxfer
    +test:
        +title: test_pcl5_testfiles_raster_implicitxfer
        +guid:ecc15df7-5ea1-4c1b-82df-7309be007ade
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_implicitxfer(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c522874feab6a87ca0d0da0add092e639a9dc49323a00a652a967d68e8471837', timeout=600)
    outputsaver.save_output()
