import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidRes-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidRes-2.pwg=372ca4aaca3caa3825b88a143936fcde0299039b0b115aa6d575e6af703abad0
    +name:test_pwg_negative_ph_only_invalid_resolution_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_resolution_2
        +guid:bae47f8c-a873-4285-b350-ac11f88ceb58
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_resolution_2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('372ca4aaca3caa3825b88a143936fcde0299039b0b115aa6d575e6af703abad0', 'FAILED')
    outputsaver.save_output()
