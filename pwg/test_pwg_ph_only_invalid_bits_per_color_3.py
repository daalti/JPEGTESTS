import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidBitsPerClr-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidBitsPerClr-3.pwg=6d6803045a3fcb9f80f0e971f0df8924f94e20c6aba39005cf65b6c895c905a0
    +name:test_pwg_negative_ph_only_invalid_bits_per_color_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_bits_per_color_3
        +guid:886de657-8798-4fc5-bfcc-696aa405bf5d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_bits_per_color_3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6d6803045a3fcb9f80f0e971f0df8924f94e20c6aba39005cf65b6c895c905a0', 'FAILED')
    outputsaver.save_output()
