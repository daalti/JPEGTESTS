import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf A4 Color 300 from *A4_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_Color_300.urf=16f1c874037c57f7633b6a6c8e3e9bf362b0630d977c01e1c8c46d1cfa6d8cd3
    +name:test_urf_a4_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a4_color_300_page
        +guid:402b0c7f-1b35-4e62-8131-0dd3321c554e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a4_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('16f1c874037c57f7633b6a6c8e3e9bf362b0630d977c01e1c8c46d1cfa6d8cd3')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF A4 Color 300 page - Print job completed successfully")
