import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only resolution up scale phase1-1 from *PwgPhOnly-ResUpScalePhase1-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-ResUpScalePhase1-1.pwg=ad5facb8beef4c5265ae42283c4d9ab56ef6f92864d94a0557bc41a5f14e26b9
    +name:test_pwg_ph_only_resolution_up_scale_phase1_1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_resolution_up_scale_phase1_1_page
        +guid:5d3c742d-e13f-4abb-b7e1-a66cf4463b80
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_resolution_up_scale_phase1_1_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ad5facb8beef4c5265ae42283c4d9ab56ef6f92864d94a0557bc41a5f14e26b9')
    outputsaver.save_output()

    logging.info("PWG Ph Only ResUp Scale Phase1-1 - Print job completed successfully")
