import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation, TrayLevel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf A6 Color 300 from *A6_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A6_Color_300.urf=c4efce612a4a99c18ad578bef2cb859a975cb646a5df20e913585d34f5a074c3
    +name:test_urf_a6_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a6_color_300_page
        +guid:3b62e05b-3615-4987-9721-ec1c86bd6e73
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_a6_105x148mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a6_color_300_page(setup_teardown, printjob, outputsaver, tray, print_emulation):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(
            trayid="all",
            media_size=MediaSize.A6.name,
            media_type=MediaType.Plain.name,
            orientation=MediaOrientation.Default.name,
            level=TrayLevel.Full.name
        )
    elif tray.is_size_supported('iso_a6_105x148mm', default):
        tray.configure_tray(default, 'iso_a6_105x148mm', 'stationery')

    printjob.print_verify('c4efce612a4a99c18ad578bef2cb859a975cb646a5df20e913585d34f5a074c3')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF A6 Color 300 page - Print job completed successfully")
