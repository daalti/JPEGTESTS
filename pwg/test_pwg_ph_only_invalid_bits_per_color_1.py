import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidBitsPerClr-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidBitsPerClr-1.pwg=4a65a997ba719712a51a86086b337e66d79224490c0556c1113dac7978ffce96
    +name:test_pwg_negative_ph_only_invalid_bits_per_color_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_bits_per_color_1
        +guid:df8be439-74eb-4aad-ad32-0073cb738923
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
def test_pwg_negative_ph_only_invalid_bits_per_color_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4a65a997ba719712a51a86086b337e66d79224490c0556c1113dac7978ffce96', 'FAILED')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
