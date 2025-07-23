import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidColorspace-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidColorspace-2.pwg=610e0d6981d976d211fe2b49f00e9c6f25ff13d7cdcd8c67315aef6e286e8ea0
    +name:test_pwg_negative_ph_only_invalid_color_space_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_color_space_2
        +guid:07dc1e39-8ae8-499c-819d-062f10f1a561
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
def test_pwg_negative_ph_only_invalid_color_space_2(setup_teardown, printjob, outputsaver, udw,tray):
    tray.reset_trays()
    printjob.print_verify('610e0d6981d976d211fe2b49f00e9c6f25ff13d7cdcd8c67315aef6e286e8ea0', 'FAILED')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
