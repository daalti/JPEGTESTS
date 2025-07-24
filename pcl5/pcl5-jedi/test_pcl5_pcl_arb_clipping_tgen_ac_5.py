import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tgen_ac_5.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tgen_ac_5.obj=b3725fe73cf460faafc53b222f8d6e178593040695fa744b230496e667d57ca9
    +test_classification:System
    +name: test_pcl5_pcl_arb_clipping_tgen_ac_5
    +test:
        +title: test_pcl5_pcl_arb_clipping_tgen_ac_5
        +guid:cc0a4666-0b9f-4ab2-bee1-aea692d6a7e7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_arb_clipping_tgen_ac_5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b3725fe73cf460faafc53b222f8d6e178593040695fa744b230496e667d57ca9', timeout=600)
    outputsaver.save_output()
