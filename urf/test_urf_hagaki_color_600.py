import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Hagaki Color 600 from *Hagaki_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Hagaki_Color_600.urf=f273961965cdd305347a75c09b20b4203d7df0b43f6c5c93f5761871d12c7d50
    +name:test_urf_hagaki_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_hagaki_color_600_page
        +guid:e34a6e0e-8a83-4c69-b2fb-87c6de115d34
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=jpn_hagaki_100x148mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_hagaki_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('jpn_hagaki_100x148mm', default):
        tray.configure_tray(default, 'jpn_hagaki_100x148mm', 'stationery')

    printjob.print_verify('f273961965cdd305347a75c09b20b4203d7df0b43f6c5c93f5761871d12c7d50')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Hagaki Color 600 page - Print job completed successfully")
