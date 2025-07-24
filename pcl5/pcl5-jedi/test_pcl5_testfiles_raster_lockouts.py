import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using lockouts.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:lockouts.pcl=a7fe0d613d55065efcd15743c0b9498ddc0f11e71a0aa5abe346e0d6266afff6
    +test_classification:System
    +name: test_pcl5_testfiles_raster_lockouts
    +test:
        +title: test_pcl5_testfiles_raster_lockouts
        +guid:eaee84e1-bd4e-4949-8f97-7e02ee2050a1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_raster_lockouts(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a7fe0d613d55065efcd15743c0b9498ddc0f11e71a0aa5abe346e0d6266afff6', timeout=600)
    outputsaver.save_output()
