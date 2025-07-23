import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only resolution up scale phase1-4 from *PwgPhOnly-ResUpScalePhase1-4.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-ResUpScalePhase1-4.pwg=e12f2e48048fa7b436b47d2c167f05491a1ae96491113a3bc44c98f3e0fa6598
    +name:test_pwg_ph_only_resolution_up_scale_phase1_4_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_resolution_up_scale_phase1_4_page
        +guid:cb3954d3-a0bf-4754-9f6a-72aab46b8ef9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_resolution_up_scale_phase1_4_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e12f2e48048fa7b436b47d2c167f05491a1ae96491113a3bc44c98f3e0fa6598')
    outputsaver.save_output()

    logging.info("PWG Ph Only ResUp Scale Phase1-4 - Print job completed successfully")
