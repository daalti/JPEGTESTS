import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 16Page_ttfontid.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:16Page-ttfontid.obj=eaca753aedea480a827b6a3cb28ea3a5ac87911b46b0fbdfcf43319d4ef14efa
    +test_classification:System
    +name: test_pcl5_lowvaluenew_16page_ttfontid
    +test:
        +title: test_pcl5_lowvaluenew_16page_ttfontid
        +guid:3b240dd2-8391-43e0-b0e8-5ffd6c7cbeae
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_16page_ttfontid(setup_teardown, printjob, outputsaver):
    printjob.print_verify('eaca753aedea480a827b6a3cb28ea3a5ac87911b46b0fbdfcf43319d4ef14efa', timeout=600)
    outputsaver.save_output()
