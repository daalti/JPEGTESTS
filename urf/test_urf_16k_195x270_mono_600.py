import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **16k_195x270_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:16k_195x270_Mono_600.urf=9982f0dd041e10e98e326a09e7d6346470a41446ed801793eca521a0385bfc10
    +name:test_urf_16k_195x270_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_16k_195x270_mono_600
        +guid:5666b341-fab9-42c5-aa51-49304737894a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=om_16k_195x270mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_16k_195x270_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_16k_195x270mm', default):
        tray.configure_tray(default, 'om_16k_195x270mm', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('9982f0dd041e10e98e326a09e7d6346470a41446ed801793eca521a0385bfc10')
    outputsaver.save_output()
    tray.reset_trays()
