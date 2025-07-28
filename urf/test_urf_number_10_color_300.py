import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Number-10 Color 300 Page from *Number-10_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Number-10_Color_300.urf=d330bb78d2b203ee7fe74dcc1d7d734333deb4f6e3f17f123c8ccfd1af1bb785
    +name:test_urf_number_10_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_number_10_color_300_page
        +guid:a1b23660-08d3-4582-aeb5-941c3d35a2da
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-10_4.125x9.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_number_10_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_number-10_4.125x9.5in', default):
        tray.configure_tray(default, 'na_number-10_4.125x9.5in', 'stationery')

    printjob.print_verify('d330bb78d2b203ee7fe74dcc1d7d734333deb4f6e3f17f123c8ccfd1af1bb785')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Number-10 Color 300 Page - Print job completed successfully")
