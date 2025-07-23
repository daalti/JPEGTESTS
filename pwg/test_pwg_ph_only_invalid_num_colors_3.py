import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidNumColors-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidNumColors-3.pwg=fa4c7f9a623ff7e0e6a46cd84e100f83f4a152569a57e5dbb8e97909ac7fda2d
    +name:test_pwg_negative_ph_only_invalid_num_color_components_per_pixel_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_num_color_components_per_pixel_3
        +guid:e4f0dc5d-e716-41d6-acb2-9589ff5633a3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_negative_ph_only_invalid_num_color_components_per_pixel_3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fa4c7f9a623ff7e0e6a46cd84e100f83f4a152569a57e5dbb8e97909ac7fda2d', 'FAILED')
    outputsaver.save_output()
    outputsaver.clear_output()
