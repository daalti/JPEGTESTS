import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using comp55.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:comp55.pcl=11b6921f3e46932ceb2c24c857963952cdb0927b072261b7126ce803231fe9ef
    +test_classification:System
    +name: test_pcl5_testfiles_raster_comp55
    +test:
        +title: test_pcl5_testfiles_raster_comp55
        +guid:8d19417e-3049-47e9-b81e-8e7f67622673
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_comp55(setup_teardown, printjob, outputsaver):
    printjob.print_verify('11b6921f3e46932ceb2c24c857963952cdb0927b072261b7126ce803231fe9ef', timeout=600)
    outputsaver.save_output()
