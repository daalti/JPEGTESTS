import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pr.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pr.obj=1e93cdc36d17ad332a1eca70f7a0b31a9aea85290855e989b80224b2afb19b0c
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pr
    +test:
        +title: test_pcl5_hpgl_vector_pr
        +guid:fe96daf3-8701-463b-b1a2-b07ac000ef7b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1e93cdc36d17ad332a1eca70f7a0b31a9aea85290855e989b80224b2afb19b0c', timeout=600)
    outputsaver.save_output()
