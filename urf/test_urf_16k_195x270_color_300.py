import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 16k 195x270 Color 300 page from *16k_195x270_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:16k_195x270_Color_300.urf=0fb6b1d2a8b82db31e9ea14c51396a24bf84b6d61852e4c4b949b3bfcbcc09df
    +name:test_urf_16k_195x270_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_16k_195x270_color_300_page
        +guid:fb52c939-b4a4-48a5-b2ba-8ce4332c464e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=om_16k_195x270mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_16k_195x270_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_16k_195x270mm', default):
        tray.configure_tray(default, 'om_16k_195x270mm', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
        
    printjob.print_verify('0fb6b1d2a8b82db31e9ea14c51396a24bf84b6d61852e4c4b949b3bfcbcc09df')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 16k 195x270 Color 300 page - Print job completed successfully")
