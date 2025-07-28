import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Prc 16k 197x273 Color 600 Page from *Prc_16k_197x273_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Prc_16k_197x273_Color_600.urf=211000dcc06d6a686ab6c96f9aa8b30507c012cba603656b77be7888ff6d4834
    +name:test_urf_prc_16k_197x273_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_prc_16k_197x273_color_600_page
        +guid:8976b7f3-3633-4423-b4a3-a4ce8f74f1f1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=roc_16k_7.75x10.75in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_prc_16k_197x273_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('roc_16k_7.75x10.75in', default):
        tray.configure_tray(default, 'roc_16k_7.75x10.75in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('211000dcc06d6a686ab6c96f9aa8b30507c012cba603656b77be7888ff6d4834')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Prc 16k 197x273 Color 600 Page - Print job completed successfully")
