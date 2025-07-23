import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print resolution up scale phase2-11 from *PwgCloudPrint-ResUpScalePhase2-11.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ResUpScalePhase2-11.pwg=b183486585196e3b50bf96c0a3e0ed9d6b4fce16a7217142890faa0566e13f53
    +name:test_pwg_cloud_print_resolution_up_scale_phase2_11_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_resolution_up_scale_phase2_11_page
        +guid:90953d0c-3b70-4483-bab6-15ef8e114c37
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_resolution_up_scale_phase2_11_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b183486585196e3b50bf96c0a3e0ed9d6b4fce16a7217142890faa0566e13f53')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Resolution Up Scale Phase2-11completed successfully")
