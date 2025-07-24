import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 32Page_logp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:32Page-logp.obj=7396939fa4fa58d49c43468b95a4595add6eb257bbd6b135880876fa6058fc97
    +test_classification:System
    +name: test_pcl5_lowvaluenew_32page_logp
    +test:
        +title: test_pcl5_lowvaluenew_32page_logp
        +guid:e3979030-83dc-4795-9d47-15280c97c21b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_32page_logp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7396939fa4fa58d49c43468b95a4595add6eb257bbd6b135880876fa6058fc97', timeout=600)
    outputsaver.save_output()
