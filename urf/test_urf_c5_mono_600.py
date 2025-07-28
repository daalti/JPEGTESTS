import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **C5_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:C5_Mono_600.urf=817c669b413377b39224828c48945a5ec186f1f083ba7565a5205534107b4358
    +name:test_urf_c5_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_c5_mono_600
        +guid:be896aa1-5c97-40e9-b316-a289abc39c20
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_c5_162x229mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_c5_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
    media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
    if tray.is_size_supported('iso_c5_162x229mm', default):
        tray.configure_tray(default, 'iso_c5_162x229mm', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 63766 and media_length_maximum >= 90150 and  media_width_minimum <= 63766 and media_length_minimum <= 90150:
        tray.configure_tray(default, 'custom', 'stationery') 

    printjob.print_verify('817c669b413377b39224828c48945a5ec186f1f083ba7565a5205534107b4358')
    outputsaver.save_output()
    tray.reset_trays()
