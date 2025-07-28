import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **B5_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:B5_Mono_600.urf=2aba8aadb9e1c542d49af08b2cb4daa61e5a14c330632ad9d5146b33d3497cdd
    +name:test_urf_b5_mono_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_b5_mono_600_page
        +guid:1e6d2cd8-b7b8-4802-99b4-2603d16ca81d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_b5_176x250mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_b5_mono_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_b5_176x250mm', default):
        tray.configure_tray(default, 'iso_b5_176x250mm', 'stationery')

    printjob.print_verify('2aba8aadb9e1c542d49af08b2cb4daa61e5a14c330632ad9d5146b33d3497cdd')
    outputsaver.save_output()
    tray.reset_trays()
