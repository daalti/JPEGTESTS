import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Index Card Color 600 from *Indexcard_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Indexcard_Color_600.urf=d52108bb42ce44ae759f45163262688f87b83dc6111cc0d199fb067601de1e9d
    +name:test_urf_index_card_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_card_color_600_page
        +guid:7f68960b-ee24-475f-820f-cbda9fcc8ac8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=om_small-photo_100x150mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_card_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_small-photo_100x150mm', default):
        tray.configure_tray(default, 'om_small-photo_100x150mm', 'stationery')

    printjob.print_verify('d52108bb42ce44ae759f45163262688f87b83dc6111cc0d199fb067601de1e9d')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Index Card Color 600 Page - Print job completed successfully")
