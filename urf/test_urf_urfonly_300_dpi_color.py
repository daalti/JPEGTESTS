import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of URF ONLY 300 dpi Color Page from *URFONLY300dpiColor.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:URFONLY300dpiColor.urf=220dcce1b931685a6564c8aa1223ff56f8781d21c4414c01c21094fa0974f4a5
    +name:test_urf_only_300_dpi_color_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_only_300_dpi_color_page
        +guid:48c52276-7205-43ea-97c3-ca1bb402aa20
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_only_300_dpi_color_page(setup_teardown, printjob, outputsaver, tray):
    # file size  Width:215900 & Height:279400 in microns, should configure tray with na_letter_8.5x11in 
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('220dcce1b931685a6564c8aa1223ff56f8781d21c4414c01c21094fa0974f4a5')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF ONLY 300 dpi Color Page- Print job completed successfully")
