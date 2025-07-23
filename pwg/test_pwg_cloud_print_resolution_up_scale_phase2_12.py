import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print resolution up scale phase2-12 from *PwgCloudPrint-ResUpScalePhase2-12.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ResUpScalePhase2-12.pwg=5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e
    +name:test_pwg_cloud_print_resolution_up_scale_phase2_12_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_resolution_up_scale_phase2_12_page
        +guid:8fce3ebd-a4f9-479b-9a92-913f7f1f52b2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_resolution_up_scale_phase2_12_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Resolution Up Scale Phase2-12completed successfully")
