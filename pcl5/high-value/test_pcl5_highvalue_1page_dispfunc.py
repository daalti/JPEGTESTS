import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_dispfunc.obj
    +test_tier: 3
    +is_manual:False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-dispfunc.obj=7964293818e8d6d402e7199a35017f471b823b4d73d4acc9d594454544a37d93
    +test_classification:System
    +name: test_pcl5_highvalue_1page_dispfunc
    +test:
        +title: test_pcl5_highvalue_1page_dispfunc
        +guid:8c8c6eba-d8e8-461a-bdd8-f1dfb4f1a6e2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_1page_dispfunc(setup_teardown, printjob, outputsaver):
    # Update the test expectaion correclty if the new features are added to PCL5 which support Text and ASCII printing
    printjob.print_verify('7964293818e8d6d402e7199a35017f471b823b4d73d4acc9d594454544a37d93', expected_job_state='SUCCESS',timeout=240)
    outputsaver.save_output()
