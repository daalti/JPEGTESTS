import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 app using aptest_2.obj
    +test_tier: 3
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:360
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:aptest_2.obj=e5002a538d0fa1b3573f28fa4b7f1987b5ce3bb672201b34e17a0cc919b908f2
    +test_classification:System
    +name: test_pcl5_app_aptest_2
    +test:
        +title: test_pcl5_app_aptest_2
        +guid:f989ba1b-36fc-4725-a2e1-9b91d2d0c29e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_app_aptest_2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e5002a538d0fa1b3573f28fa4b7f1987b5ce3bb672201b34e17a0cc919b908f2', timeout=360, expected_jobs=7)
    outputsaver.save_output()
