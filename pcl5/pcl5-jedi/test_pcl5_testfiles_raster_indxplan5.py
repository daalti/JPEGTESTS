import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using indxplan5.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:indxplan5.pcl=f344d4efa9e6d003314fd96348e001f94b3eadf40d73bdafaa9c9b68587d4bc2
    +test_classification:System
    +name: test_pcl5_testfiles_raster_indxplan5
    +test:
        +title: test_pcl5_testfiles_raster_indxplan5
        +guid:7715fbdb-56e2-4aea-b592-32a2f617d94b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_indxplan5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f344d4efa9e6d003314fd96348e001f94b3eadf40d73bdafaa9c9b68587d4bc2', timeout=600)
    outputsaver.save_output()
