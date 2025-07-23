import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidNumColors-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidNumColors-1.pwg=9d97e6ca8ea335321c9f62e22aaca43006a2545b6f19a4ad940586d841d4c8d0
    +name:test_pwg_negative_ph_only_invalid_num_color_components_per_pixel_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_num_color_components_per_pixel_1
        +guid:2f4c5d64-fbce-4b83-b376-cca24119e164
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_num_color_components_per_pixel_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9d97e6ca8ea335321c9f62e22aaca43006a2545b6f19a4ad940586d841d4c8d0', 'FAILED')
    outputsaver.save_output()
