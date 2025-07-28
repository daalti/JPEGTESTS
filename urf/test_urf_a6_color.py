import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf A6 Color from *A6_Color.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A6_Color.urf=32c329c82614c8f7d8c6b0e1408450af24a05c70c267fb821419cbde73dc3e39
    +name:test_urf_a6_color_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a6_color_page
        +guid:33cb4e93-fdeb-413d-9692-c34e9503e877
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_a6_105x148mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a6_color_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a6_105x148mm', default):
        tray.configure_tray(default, 'iso_a6_105x148mm', 'stationery')

    printjob.print_verify('32c329c82614c8f7d8c6b0e1408450af24a05c70c267fb821419cbde73dc3e39')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF A6 Color page - Print job completed successfully")
