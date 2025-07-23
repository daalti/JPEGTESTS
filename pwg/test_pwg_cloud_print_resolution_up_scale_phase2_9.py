import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print resolution up scale phase2-9 from *PwgCloudPrint-ResUpScalePhase2-9.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ResUpScalePhase2-9.pwg=50d88787aa538037aef45624809af6b332ebb41a2fa0310eb1ea5c5e4b43f69d
    +name:test_pwg_cloud_print_resolution_up_scale_phase2_9_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_resolution_up_scale_phase2_9_page
        +guid:b5cb4edd-89e0-4ef1-8e9c-db1371ad8224
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_resolution_up_scale_phase2_9_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('50d88787aa538037aef45624809af6b332ebb41a2fa0310eb1ea5c5e4b43f69d')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Resolution Up Scale Phase2-9completed successfully")
