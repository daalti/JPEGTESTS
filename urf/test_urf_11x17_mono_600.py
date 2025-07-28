import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **11x17_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:11x17_Mono_600.urf=e9f6af3ed37c5d898c27de91f5620c6700b597634946d65c1d81d9bc4da8a4fe
    +name:test_urf_11x17_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_11x17_mono_600
        +guid:ef51adb7-9f30-4256-a92c-30fe4027f14f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_11x17_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_ledger_11x17in', default):
        tray.configure_tray(default, 'na_ledger_11x17in', 'stationery')
    
    printjob.print_verify('e9f6af3ed37c5d898c27de91f5620c6700b597634946d65c1d81d9bc4da8a4fe')
    outputsaver.save_output()
    tray.reset_trays()
