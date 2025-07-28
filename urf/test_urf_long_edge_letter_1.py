import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Long-Edge-Letter_1.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Long-Edge-Letter_1.urf=886543f11e310f6076126566206fe86ebfb473d74309fa54bc3b017d8cb2fc17
    +name:test_urf_long_edge_letter_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_long_edge_letter_1
        +guid:5a331e7b-1565-408e-8e61-fc38372fc556
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_long_edge_letter_1(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"] >= 150000:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, "custom", 'stationery')

    printjob.print_verify('886543f11e310f6076126566206fe86ebfb473d74309fa54bc3b017d8cb2fc17')
    outputsaver.save_output()
    tray.reset_trays()
