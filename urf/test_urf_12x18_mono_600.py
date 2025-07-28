import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **12x18_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:12x18_Mono_600.urf=ed9fb6f78f95df077af995b496dde5eac5a52c2c65c7ee7a453663751d1ff638
    +name:test_urf_12x18_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_12x18_mono_600
        +guid:5b95c71f-484d-4fc1-a3de-16eb610371e4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_12x18_mono_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ed9fb6f78f95df077af995b496dde5eac5a52c2c65c7ee7a453663751d1ff638')
    outputsaver.save_output()
