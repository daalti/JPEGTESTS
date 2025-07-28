import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Dl_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Dl_Mono_600.urf=d48b22ad326fe57c18c989c681819f8a85c66888c7c0db8f948aff9d3924bbed
    +name:test_urf_dl_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_dl_mono_600
        +guid:70e1591f-9588-49cc-8919-b92ab237d530
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_dl_110x220mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_dl_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_dl_110x220mm', default):
        tray.configure_tray(default, 'iso_dl_110x220mm', 'stationery')

    printjob.print_verify('d48b22ad326fe57c18c989c681819f8a85c66888c7c0db8f948aff9d3924bbed')
    outputsaver.save_output()
    tray.reset_trays()
