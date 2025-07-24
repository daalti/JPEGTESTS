import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_duplx_bf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-duplx_bf.obj=85b933333b555ec8747df5292de44ce118586691e4b7c72c41561aba8b628959
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_duplx_bf
    +test:
        +title: test_pcl5_lowvaluenew_1page_duplx_bf
        +guid:64296337-20d3-4854-811e-1545c550ea65
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_duplx_bf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('85b933333b555ec8747df5292de44ce118586691e4b7c72c41561aba8b628959', timeout=600)
    outputsaver.save_output()
