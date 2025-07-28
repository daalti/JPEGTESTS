import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Executive Color 300 from *Executive_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Executive_Color_300.urf=09184ccd524a9216b6063098ef911e0212e8be0f877a802a6ff015606f9c74a3
    +name:test_urf_executive_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_executive_color_300_page
        +guid:707e8d5a-9675-408d-8448-ad544edfe462
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_executive_7.25x10.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_executive_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_executive_7.25x10.5in', default):
        tray.configure_tray(default, 'na_executive_7.25x10.5in', 'stationery')

    printjob.print_verify('09184ccd524a9216b6063098ef911e0212e8be0f877a802a6ff015606f9c74a3')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Executive Color 300 page - Print job completed successfully")
