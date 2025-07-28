import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf Com-10 Color 600 from *Com-10_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Com-10_Color_600.urf=a79c3047781d536af7c066818f2e861121e8d27a7d9ed5408d2fcbdbd0911294
    +name:test_urf_com_10_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_com_10_color_600_page
        +guid:d65224bf-98e1-4218-8e5e-23e1660a725c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-10_4.125x9.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_com_10_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_number-10_4.125x9.5in', default):
        tray.configure_tray(default, 'na_number-10_4.125x9.5in', 'stationery')

    printjob.print_verify('a79c3047781d536af7c066818f2e861121e8d27a7d9ed5408d2fcbdbd0911294')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Com-10 Color 600 page - Print job completed successfully")
