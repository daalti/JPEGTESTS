import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidColorspace-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidColorspace-3.pwg=f912057b20f81fec781dc3a1432aba08a8b8e8d70d2346298b8aba4b18e75537
    +name:test_pwg_negative_ph_only_invalid_color_space_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_color_space_3
        +guid:152c4caf-3e67-47d6-ad6a-281b3a00d237
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_color_space_3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f912057b20f81fec781dc3a1432aba08a8b8e8d70d2346298b8aba4b18e75537', 'SUCCESS')
    outputsaver.save_output()
