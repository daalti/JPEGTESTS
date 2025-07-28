import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **iso_ra3_305x430mm_Mono.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:iso_ra3_305x430mm_Mono.urf=f238732b96681543b565f7cf66baf616f100392a119b85ba9eaa52fc45a327c1
    +name:test_urf_iso_ra3_305x430mm_mono
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_iso_ra3_305x430mm_mono
        +guid:b8e82743-b67e-4b5a-ac4d-cfa00dfc2e2b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_iso_ra3_305x430mm_mono(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f238732b96681543b565f7cf66baf616f100392a119b85ba9eaa52fc45a327c1')
    outputsaver.save_output()
