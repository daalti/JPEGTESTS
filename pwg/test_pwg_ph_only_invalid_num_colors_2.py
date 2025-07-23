import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job to verify invalid/negetive test case from *PwgPhOnly-InvalidNumColors-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-InvalidNumColors-2.pwg=ede85e012b660dc4bf952f03efdd3f0926d2b9f14161e87389b75911b70e926a
    +name:test_pwg_negative_ph_only_invalid_num_color_components_per_pixel_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Negative
    +test:
        +title:test_pwg_negative_ph_only_invalid_num_color_components_per_pixel_2
        +guid:2cd82f88-7756-46ec-8e76-9b272fc61290
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
def test_pwg_negative_ph_only_invalid_num_color_components_per_pixel_2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ede85e012b660dc4bf952f03efdd3f0926d2b9f14161e87389b75911b70e926a', 'FAILED')
    outputsaver.save_output()
