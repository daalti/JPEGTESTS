import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_duplexm8.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-duplexm8.obj=b6f6c285bf773694662dbbd99e7d2662df7216046b6c9661c24119d92c11e235
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_duplexm8
    +test:
        +title: test_pcl5_lowvaluenew_1page_duplexm8
        +guid:a14319e7-e24a-4507-bd3e-2a4bc3509543
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_duplexm8(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b6f6c285bf773694662dbbd99e7d2662df7216046b6c9661c24119d92c11e235', timeout=600)
    outputsaver.save_output()
