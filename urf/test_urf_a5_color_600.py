import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf A5 Color 600 from *A5_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A5_Color_600.urf=66a70b02f29cfc9a5c4ec43e4527ac51d359e9c10cbb7d6ab68ed14c7417f6a4
    +name:test_urf_a5_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a5_color_600_page
        +guid:441dfce3-6941-480c-aa4f-474b68a93690
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_a5_148x210mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a5_color_600_page(setup_teardown, printjob, outputsaver, tray, print_emulation):
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        print_emulation.tray.setup_tray(trayid="all", media_size=MediaSize.A5.name, media_type=MediaType.Plain.name,
                                    orientation=MediaOrientation.Default.name, level=TrayLevel.Full.name)

    elif tray.is_size_supported('iso_a5_148x210mm', default):
        tray.configure_tray(default, 'iso_a5_148x210mm', 'stationery')

    printjob.print_verify('66a70b02f29cfc9a5c4ec43e4527ac51d359e9c10cbb7d6ab68ed14c7417f6a4')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF A5 Color 600 page - Print job completed successfully")
