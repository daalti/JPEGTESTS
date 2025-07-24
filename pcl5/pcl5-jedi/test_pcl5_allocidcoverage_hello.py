import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using hello.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:hello.pcl=d8bb33a13b3dd0575411ff45377e258f2e970365e93351a0994b6619c2da7ed4
    +test_classification:System
    +name: test_pcl5_allocidcoverage_hello
    +test:
        +title: test_pcl5_allocidcoverage_hello
        +guid:fbc8b558-28c7-49ba-9c0f-38d204e7e6b3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_hello(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d8bb33a13b3dd0575411ff45377e258f2e970365e93351a0994b6619c2da7ed4', timeout=600)
    outputsaver.save_output()
