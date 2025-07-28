import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **8k_270x390_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8k_270x390_Mono_600.urf=25013017c91bfc24a738ca3f1a6dae7dbc0fec84654dfb212e8f2e2291b3b7b8
    +name:test_urf_8k_270x390_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_8k_270x390_mono_600
        +guid:28c184cd-5677-4fd0-9f6d-aa633edf9aa6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_8k_270x390_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]

    if tray.is_size_supported('om_8k_270x390mm', default):
        tray.configure_tray(default, 'om_8k_270x390mm', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 106284 and media_length_maximum >= 153534:
        tray.configure_tray(default, 'custom', 'stationery')
    
    printjob.print_verify('25013017c91bfc24a738ca3f1a6dae7dbc0fec84654dfb212e8f2e2291b3b7b8')
    outputsaver.save_output()
    tray.reset_trays()
