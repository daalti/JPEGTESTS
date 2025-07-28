import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 16k 195x270 Color 600 page from *16k_195x270_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:16k_195x270_Color_600.urf=b1a7209f4e103e9c63dd48243032e7b167ee7ac06f414db6b4d6d6b731460304
    +name:test_urf_16k_195x270_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_16k_195x270_color_600_page
        +guid:1564b286-37de-4e3c-9318-e8c6b8436c40
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=om_16k_195x270mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_16k_195x270_color_600_page(setup_teardown, printjob, outputsaver, tray, print_emulation):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(
            trayid="all",
            media_size=MediaSize.Size16K195x270.name,
            media_type=MediaType.Plain.name,
            orientation=MediaOrientation.Default.name,
            level=TrayLevel.Full.name
        )
    elif tray.is_size_supported('om_16k_195x270mm', default):
        tray.configure_tray(default, 'om_16k_195x270mm', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
    printjob.print_verify('b1a7209f4e103e9c63dd48243032e7b167ee7ac06f414db6b4d6d6b731460304')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 16k 195x270 Color 600 page - Print job completed successfully")
