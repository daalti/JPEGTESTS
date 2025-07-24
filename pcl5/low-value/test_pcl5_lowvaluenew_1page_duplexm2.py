import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_duplexm2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-duplexm2.obj=855dec6b7c970e8eed375c8de9118c00e4e42cd7759702f2a79b830dbe6c9229
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_duplexm2
    +test:
        +title: test_pcl5_lowvaluenew_1page_duplexm2
        +guid:8cf9328a-aebe-4b7a-8beb-abb3f3a9683b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_duplexm2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('855dec6b7c970e8eed375c8de9118c00e4e42cd7759702f2a79b830dbe6c9229', timeout=600)
    outputsaver.save_output()
