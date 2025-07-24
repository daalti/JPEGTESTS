import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 9Page_rastyopt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:9Page-rastyopt.obj=1a53a4238c15fa00c8616a702f57caa93887098642937a6b63d301f6729d5ee3
    +test_classification:System
    +name: test_pcl5_lowvaluenew_9page_rastyopt
    +test:
        +title: test_pcl5_lowvaluenew_9page_rastyopt
        +guid:0b473cf6-3561-43cd-8138-10eca0743dc5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_9page_rastyopt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1a53a4238c15fa00c8616a702f57caa93887098642937a6b63d301f6729d5ee3', timeout=600)
    outputsaver.save_output()
