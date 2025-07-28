import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 16k 184x260 Color 600 page from *16k_184x260_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:16k_184x260_Color_600.urf=f2d9d2c68fdda890cfc266c4ba541540749a8a5255f51a576315775f520274a7
    +name:test_urf_16k_184x260_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_16k_184x260_color_600_page
        +guid:3a5d91a3-88cc-4fa0-b036-02e07f8d4caa
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=om_16k_184x260mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_16k_184x260_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_16k_184x260mm', default):
        tray.configure_tray(default, 'om_16k_184x260mm', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('f2d9d2c68fdda890cfc266c4ba541540749a8a5255f51a576315775f520274a7')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 16k 184x260 Color 600 page - Print job completed successfully")
