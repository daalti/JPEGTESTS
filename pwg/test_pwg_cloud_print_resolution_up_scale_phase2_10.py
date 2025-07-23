import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print resolution up scale phase2-10 from *PwgCloudPrint-ResUpScalePhase2-10.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ResUpScalePhase2-10.pwg=2db8056eefa5a72b885e76181720b013f14a4fce311cc76acb008d2e71e51cc6
    +name:test_pwg_cloud_print_resolution_up_scale_phase2_10_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_resolution_up_scale_phase2_10_page
        +guid:2fad0798-42a2-4026-8fac-fd4aa75f5435
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_resolution_up_scale_phase2_10_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2db8056eefa5a72b885e76181720b013f14a4fce311cc76acb008d2e71e51cc6')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Resolution Up Scale Phase2-10completed successfully")
