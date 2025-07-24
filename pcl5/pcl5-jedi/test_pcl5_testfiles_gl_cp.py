import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using cp.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cp.pcl=e68a98bce18ec9e02b6111aa95643e0b5efb705addfdb52a122029b98c71cb05
    +test_classification:System
    +name: test_pcl5_testfiles_gl_cp
    +test:
        +title: test_pcl5_testfiles_gl_cp
        +guid:b2891b22-5b08-4ead-bb34-aeba20feab85
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_cp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e68a98bce18ec9e02b6111aa95643e0b5efb705addfdb52a122029b98c71cb05', timeout=600)
    outputsaver.save_output()
