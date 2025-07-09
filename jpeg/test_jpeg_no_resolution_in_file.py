import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test jpeg job when no resolution in specified in file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-215024
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:road_nores.jpeg=116ef2798a4d195fd1e3ea20d81af3b8c20373587e119d10a6ff0f0d70ee6f86
    +test_classification:System
    +name:test_jpeg_no_resolution_in_file
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_no_resolution_in_file
        +guid:c6ab3f3c-5f86-4d7d-b17d-f44829404c84
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & EngineFirmwareFamily=DoX & PrintResolution=Print300

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_no_resolution_in_file(setup_teardown, printjob, outputverifier, tray, media,outputsaver, udw):
    tray.reset_trays()
    default_tray = tray.get_default_source()
    if tray.is_size_supported('custom', default_tray):
        tray.configure_tray(default_tray, 'custom', 'stationery')

    outputsaver.validate_crc_tiff(udw)

    printjob.print_verify('116ef2798a4d195fd1e3ea20d81af3b8c20373587e119d10a6ff0f0d70ee6f86', 'SUCCESS', 300, 1)
    outputverifier.save_and_parse_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    outputverifier.verify_resolution(Intents.printintent, 600)
    outputverifier.verify_page_width(Intents.printintent, 3000)
    outputverifier.verify_page_height(Intents.printintent, 3749)
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

