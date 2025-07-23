import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print resolution up scale phase2-13 from *PwgCloudPrint-ResUpScalePhase2-13.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ResUpScalePhase2-13.pwg=449c80c848e1cff57c4e1e58defc551459c69e2643ccd95cebb6b5e8aa9557cd
    +name:test_pwg_cloud_print_resolution_up_scale_phase2_13_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_resolution_up_scale_phase2_13_page
        +guid:445750c4-d026-4919-94cf-3808a88550db
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_resolution_up_scale_phase2_13_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('449c80c848e1cff57c4e1e58defc551459c69e2643ccd95cebb6b5e8aa9557cd')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Resolution Up Scale Phase2-13completed successfully")
