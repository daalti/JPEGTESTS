import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **mono.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:mono.urf=59949942edd605120fe09ad784bf19641afa5805e905376787b1ff21131cef67
    +name:test_urf_mono
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_mono
        +guid:2260cfb2-d382-415c-888e-d5db8e7cf11d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_mono(setup_teardown, printjob, outputsaver):
    printjob.print_verify('59949942edd605120fe09ad784bf19641afa5805e905376787b1ff21131cef67')
    outputsaver.save_output()
