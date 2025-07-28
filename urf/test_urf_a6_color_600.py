import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf A6 Color 600 from *A6_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A6_Color_600.urf=1ad9ca94bbddcb23179645dcafc6a0ee69bcb0c83ab4ac19b32772b6a839ab52
    +name:test_urf_a6_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a6_color_600_page
        +guid:7073a687-6199-4bbd-962e-8f0aeadd3583
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_a6_105x148mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a6_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a6_105x148mm', default):
        tray.configure_tray(default, 'iso_a6_105x148mm', 'stationery')

    printjob.print_verify('1ad9ca94bbddcb23179645dcafc6a0ee69bcb0c83ab4ac19b32772b6a839ab52')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF A6 Color 600 page - Print job completed successfully")
