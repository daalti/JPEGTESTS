import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Tabloid Color 300 Page from *Tabloid_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Tabloid_Color_300.urf=688be70092975382c2927439f8cea9827337dd2c4a28b7ee2572fe1671eeb2b4
    +name:test_urf_tabloid_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_tabloid_color_300_page
        +guid:5b1113f9-661b-41fe-be8d-5ac4c403fdfe
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_tabloid_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_arch-b_12x18in', default):
        tray.configure_tray(default, 'na_arch-b_12x18in', 'stationery')
    elif tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('688be70092975382c2927439f8cea9827337dd2c4a28b7ee2572fe1671eeb2b4')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Tabloid Color 300 Page - Print job completed successfully")
