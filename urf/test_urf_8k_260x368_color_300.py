import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 8k_260x368 Color 300 page from *8k_260x368_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8k_260x368_Color_300.urf=e54f1ca434a5df8b16a2eda2246310d7da9f704172f22edf14a54aab7e803f4f
    +name:test_urf_8k_260x368_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_8k_260x368_color_300_page
        +guid:cf3f26d1-8afa-49a8-9cb7-34d04de35bde
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_8k_260x368_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_8k_260x368mm', default):
        tray.configure_tray(default, 'om_8k_260x368mm', 'stationery')

    printjob.print_verify('e54f1ca434a5df8b16a2eda2246310d7da9f704172f22edf14a54aab7e803f4f')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 8k_260x368 Color 300 page - Print job completed successfully")
