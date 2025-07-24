import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using mcrob_nc.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:mcrob_nc.obj=54b5faf9aea5ce067847098d94e3deb8cb23d9df056e6f78de672bc263175ccb
    +test_classification:System
    +name: test_pcl5_pcl_macros_macrosrc_mcrob_nc
    +test:
        +title: test_pcl5_pcl_macros_macrosrc_mcrob_nc
        +guid:c998bb3c-b6f1-4c9c-9bde-25528faf7901
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_macros_macrosrc_mcrob_nc(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('54b5faf9aea5ce067847098d94e3deb8cb23d9df056e6f78de672bc263175ccb')
    outputsaver.save_output()
