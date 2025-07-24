import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 3Page_rasptc2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-rasptc2.obj=3895273bb9c7449eb7d43722efa6eb5613d1d59d58dfccd33a1f282cca5f2a95
    +test_classification:System
    +name: test_pcl5_lowvaluenew_3page_rasptc2
    +test:
        +title: test_pcl5_lowvaluenew_3page_rasptc2
        +guid:46504721-69d6-4986-b86a-f35fdd44ba95
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_3page_rasptc2(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('3895273bb9c7449eb7d43722efa6eb5613d1d59d58dfccd33a1f282cca5f2a95', timeout=600,expected_jobs=3)
    outputsaver.save_output()
