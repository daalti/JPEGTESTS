import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using fn.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fn.pcl=454bc3615d2e10c0c23f77e350edadccaa51b9132722df35ca04c1006e08ca2a
    +test_classification:System
    +name: test_pcl5_allocidcoverage_fn
    +test:
        +title: test_pcl5_allocidcoverage_fn
        +guid:0e33f788-a220-4ac9-a16c-741a7b4fa639
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_fn(setup_teardown, printjob, outputsaver):
    printjob.print_verify('454bc3615d2e10c0c23f77e350edadccaa51b9132722df35ca04c1006e08ca2a', timeout=600)
    outputsaver.save_output()
