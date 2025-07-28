import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf C6 Color 600 from *C6_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:C6_Color_600.urf=a4cd6e2e67a604cc2101a7414ad32021fd27007b66367f0c43e60cb4af2ac352
    +name:test_urf_c6_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_c6_color_600_page
        +guid:3689dc37-6cbd-4cc1-b5a2-9df52a7e8e28
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_c6_114x162mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_c6_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_c6_114x162mm', default):
        tray.configure_tray(default, 'iso_c6_114x162mm', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('a4cd6e2e67a604cc2101a7414ad32021fd27007b66367f0c43e60cb4af2ac352')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF C6 Color 600 page - Print job completed successfully")
