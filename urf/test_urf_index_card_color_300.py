import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Index Card Color 300 from *Indexcard_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Indexcard_Color_300.urf=5fef36bdeec92327d3dab4cb05f4dfe4d9ea795e9470f8a3c86b06dac33a559a
    +name:test_urf_index_card_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_card_color_300_page
        +guid:d77cdba3-8a09-449b-8eeb-5ec31d64db2d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=om_small-photo_100x150mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_card_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_small-photo_100x150mm', default):
        tray.configure_tray(default, 'om_small-photo_100x150mm', 'stationery')

    printjob.print_verify('5fef36bdeec92327d3dab4cb05f4dfe4d9ea795e9470f8a3c86b06dac33a559a')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Index Card Color 300 Page - Print job completed successfully")
