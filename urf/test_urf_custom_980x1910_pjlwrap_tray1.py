import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Custom_980x1910_PJLWrap_Tray1.urf job will fail due to incorrect colorspace value
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Custom_980x1910_PJLWrap_Tray1.urf=b55f88499721acb61749f6efeb4b582b686051e992ef02622b0eed71e0c9ed1c
    +name:test_urf_custom_980x1910_pjlwrap_tray1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_custom_980x1910_pjlwrap_tray1
        +guid:b7b08c2c-506d-4eab-b219-aa5fd63dede4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaInputInstalled=Tray1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_custom_980x1910_pjlwrap_tray1(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('b55f88499721acb61749f6efeb4b582b686051e992ef02622b0eed71e0c9ed1c',expected_job_state="FAILED")
    outputsaver.save_output()
    tray.reset_trays()
