import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ttudssd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ttudssd.obj=10f165a616fc705412d7d09411f76b9dd94042dc01e6713f3211b5532a25c67c
    +test_classification:System
    +name: test_pcl5_pcl_symset_ttudssd
    +test:
        +title: test_pcl5_pcl_symset_ttudssd
        +guid:68ad8fc7-3f98-4224-be28-cf7bdd8ac5cd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_symset_ttudssd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('10f165a616fc705412d7d09411f76b9dd94042dc01e6713f3211b5532a25c67c', timeout=600)
    outputsaver.save_output()
