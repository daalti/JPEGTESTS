import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **8k_260x368_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8k_260x368_Mono_600.urf=c8c007e8f552f6a970c4529b5ba79e8edc0a8bb3a35ec06146adc8707c7f8d7f
    +name:test_urf_8k_260x368_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_8k_260x368_mono_600
        +guid:70cb3ee8-0b0c-430c-86b0-b42988d5a4a5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_8k_260x368_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]

    if tray.is_size_supported('om_8k_260x368mm', default):
        tray.configure_tray(default, 'om_8k_260x368mm', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum > 102350 and media_length_maximum > 144867:
        tray.configure_tray(default, 'custom', 'stationery')
    
    printjob.print_verify('c8c007e8f552f6a970c4529b5ba79e8edc0a8bb3a35ec06146adc8707c7f8d7f')
    outputsaver.save_output()
    tray.reset_trays()
