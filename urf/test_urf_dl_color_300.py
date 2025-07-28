import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Dl Color 300  urf from *Dl_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Dl_Color_300.urf=45f687341d7b5c2289235ee932a1df84105076073760554466da56e5892e1d23
    +name:test_urf_dl_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_dl_color_300_page
        +guid:195a705c-2e43-434b-b0e8-c671df764808
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_dl_110x220mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_dl_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_dl_110x220mm', default):
        tray.configure_tray(default, 'iso_dl_110x220mm', 'stationery')

    printjob.print_verify('45f687341d7b5c2289235ee932a1df84105076073760554466da56e5892e1d23')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Dl Color 300 page - Print job completed successfully")
