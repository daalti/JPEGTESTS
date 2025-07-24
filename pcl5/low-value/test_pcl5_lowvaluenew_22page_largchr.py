import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 22Page_largchr.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:22Page-largchr.obj=6d1c1a6bb72628895ff2a557ea6d5a4c1a00a6fa569c0c18e7e604e45c6be234
    +test_classification:System
    +name: test_pcl5_lowvaluenew_22page_largchr
    +test:
        +title: test_pcl5_lowvaluenew_22page_largchr
        +guid:5ce9d448-b7eb-4c09-bc68-db4f9ecdb9d8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_22page_largchr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6d1c1a6bb72628895ff2a557ea6d5a4c1a00a6fa569c0c18e7e604e45c6be234', timeout=600)
    outputsaver.save_output()
