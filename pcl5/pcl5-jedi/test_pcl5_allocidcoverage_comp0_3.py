import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using comp0_3.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:comp0-3.pcl=4d1e0fa2faaf0fd4cdad6c105debf5f58f3a936a52b3c8c47a64675bb49e8460
    +test_classification:System
    +name: test_pcl5_allocidcoverage_comp0_3
    +test:
        +title: test_pcl5_allocidcoverage_comp0_3
        +guid:76fbcd8b-7821-474f-928c-7aedece487b7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_comp0_3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4d1e0fa2faaf0fd4cdad6c105debf5f58f3a936a52b3c8c47a64675bb49e8460', timeout=600)
    outputsaver.save_output()
