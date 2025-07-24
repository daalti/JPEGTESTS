import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 15Page_aptest_2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:15Page-aptest_2.obj=6e4b3dc8e7b805ff87bdd4b14ab1fdc488cc9c9392875a5237cd97d54820433b
    +test_classification:System
    +name: test_pcl5_highvalue_15page_aptest_2
    +test:
        +title: test_pcl5_highvalue_15page_aptest_2
        +guid:eca299cf-26ca-4c09-8a50-cd580a23756e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_highvalue_15page_aptest_2(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('6e4b3dc8e7b805ff87bdd4b14ab1fdc488cc9c9392875a5237cd97d54820433b',expected_jobs=3)
    outputsaver.save_output()
