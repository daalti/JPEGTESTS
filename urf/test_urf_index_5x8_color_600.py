import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Index 5x8 Color 600 from *Index_5x8_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Index_5x8_Color_600.urf=55bb9ae41931e38bcf18c6fa23e9f0c51d4bb89dc51ce6bab34c1af1c80cb811
    +name:test_urf_index_5x8_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_5x8_color_600_page
        +guid:c2cd18c6-d963-41fd-a96e-05c054c05942
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-5x8_5x8in

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_5x8_color_600_page(setup_teardown, printjob, outputsaver, tray, print_emulation):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(
            trayid="all",
            media_size=MediaSize.FiveXEight.name,
            media_type=MediaType.Plain.name,
            orientation=MediaOrientation.Default.name,
            level=TrayLevel.Full.name
        )
    elif tray.is_size_supported('na_index-5x8_5x8in', default):
        tray.configure_tray(default, 'na_index-5x8_5x8in', 'stationery')

    printjob.print_verify('55bb9ae41931e38bcf18c6fa23e9f0c51d4bb89dc51ce6bab34c1af1c80cb811')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Index 5x8 Color 600 Page - Print job completed successfully")
