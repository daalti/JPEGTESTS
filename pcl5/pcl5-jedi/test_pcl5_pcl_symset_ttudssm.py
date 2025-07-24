import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ttudssm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ttudssm.obj=72d26444e9bdc23ecf6939cc936149e3a5fd8a26e385e32a22929b25e4b5cec8
    +test_classification:System
    +name: test_pcl5_pcl_symset_ttudssm
    +test:
        +title: test_pcl5_pcl_symset_ttudssm
        +guid:2569e9b2-647d-49b4-8382-702454e88fba
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_symset_ttudssm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('72d26444e9bdc23ecf6939cc936149e3a5fd8a26e385e32a22929b25e4b5cec8', timeout=600)
    outputsaver.save_output()
