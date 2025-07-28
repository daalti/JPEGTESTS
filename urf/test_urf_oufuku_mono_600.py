import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Oufuku_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Oufuku_Mono_600.urf=0867686df0b88a1eeb94e4eeeb1f5919de8145ff7b408bbd45f396696a16afe2
    +name:test_urf_oufuku_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_oufuku_mono_600
        +guid:3b5810d6-ee1c-4066-8cbe-0d9a3a86fbcd
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=jpn_oufuku_148x200mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_oufuku_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('jpn_oufuku_148x200mm', default):
        tray.configure_tray(default, 'jpn_oufuku_148x200mm', 'stationery')
    elif tray.is_size_supported("com.hp.ext.mediaSize.jpn_oufuku_148x200mm.rotated", default):
        tray.configure_tray(default, "com.hp.ext.mediaSize.jpn_oufuku_148x200mm.rotated", "stationery")
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('0867686df0b88a1eeb94e4eeeb1f5919de8145ff7b408bbd45f396696a16afe2')
    outputsaver.save_output()
    tray.reset_trays()
