import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 1Page_duplx5d.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-duplx5d.obj=ed2b7dee720012f53a97ae9da0088a81f946df6ae77140cb014e2a00e1855a81
    +test_classification:System
    +name: test_pcl5_lowvaluenew_1page_duplx5d
    +test:
        +title: test_pcl5_lowvaluenew_1page_duplx5d
        +guid:873f2fef-57c6-4140-b96d-c9a9fdde4b84
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_1page_duplx5d(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ed2b7dee720012f53a97ae9da0088a81f946df6ae77140cb014e2a00e1855a81', timeout=600)
    outputsaver.save_output()
