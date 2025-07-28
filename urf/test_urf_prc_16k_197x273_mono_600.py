import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Prc_16k_197x273_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Prc_16k_197x273_Mono_600.urf=8205bc919ea8a5375e974a16f463212cf3783367f242a14285147b677bac519d
    +name:test_urf_prc_16k_197x273_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_prc_16k_197x273_mono_600
        +guid:4b6a3c2f-1fa5-4a7f-bc58-123fe272b58f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=roc_16k_7.75x10.75in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_prc_16k_197x273_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('roc_16k_7.75x10.75in', default):
        tray.configure_tray(default, 'roc_16k_7.75x10.75in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('8205bc919ea8a5375e974a16f463212cf3783367f242a14285147b677bac519d')
    outputsaver.save_output()
    tray.reset_trays()
