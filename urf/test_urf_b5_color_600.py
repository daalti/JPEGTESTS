import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf B5 Color 600 from *B5_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:B5_Color_600.urf=50d6152543c50c657b440f0f7adac94c2518b01fb928f261aa688f53b69094f6
    +name:test_urf_b5_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_b5_color_600_page
        +guid:85c64952-b100-4d11-be60-ac2021a3f54f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_b5_176x250mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_b5_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_b5_176x250mm', default):
        tray.configure_tray(default, 'iso_b5_176x250mm', 'stationery')

    printjob.print_verify('50d6152543c50c657b440f0f7adac94c2518b01fb928f261aa688f53b69094f6')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF B5 Color 600 page - Print job completed successfully")
