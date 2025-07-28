import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **C6_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:C6_Mono_600.urf=80bbebf2a5a707eb8010d1bbdd09d791acb578b55022c34e8f0635235a55c55a
    +name:test_urf_c6_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_c6_mono_600
        +guid:d44263c0-a61e-4b67-9b4c-770d408692e5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_c6_114x162mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_c6_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_c6_114x162mm', default):
        tray.configure_tray(default, 'iso_c6_114x162mm', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('80bbebf2a5a707eb8010d1bbdd09d791acb578b55022c34e8f0635235a55c55a')
    outputsaver.save_output()
    tray.reset_trays()
