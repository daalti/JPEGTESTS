import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Dl Color 600  urf from *Dl_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Dl_Color_600.urf=3731ffdf27c9e2cca62860026056429caed469a82c8a7563c7d786f1aff7cb26
    +name:test_urf_dl_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_dl_color_600_page
        +guid:d85b5962-16ec-4aaf-b20d-84714c123ab1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_dl_110x220mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_dl_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_dl_110x220mm', default):
        tray.configure_tray(default, 'iso_dl_110x220mm', 'stationery')

    printjob.print_verify('3731ffdf27c9e2cca62860026056429caed469a82c8a7563c7d786f1aff7cb26')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Dl Color 600 page - Print job completed successfully")
