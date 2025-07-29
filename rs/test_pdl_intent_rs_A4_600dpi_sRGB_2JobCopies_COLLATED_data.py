import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, MediaType, MediaSource

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple print from a rasterstream (A4_600dpi_sRGB_2JobCopies_COLLATED.rs) file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-152360
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_600dpi_sRGB_2JobCopies_COLLATED.rs=8cb230878e51ead194983adb7aceb9a8768f4fcae3aa8040987124e9f89cd690
    +test_classification:System
    +name:test_pdl_intent_rs_A4_600dpi_sRGB_2JobCopies_COLLATED_data
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_rs_A4_600dpi_sRGB_2JobCopies_COLLATED_data
        +guid:85b0bf06-2c48-43fa-917d-4f74c0170a6e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=RasterStreamICF & DeviceClass=LFP & MediaInputInstalled=ROLL1 & MediaSizeSupported=iso_a4_210x297mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_rs_A4_600dpi_sRGB_2JobCopies_COLLATED_data(setup_teardown, printjob, outputsaver, outputverifier, tray):
    if tray.is_size_supported('iso_a4_210x297mm', 'roll-1'):
        tray.configure_tray('roll-1', 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('8cb230878e51ead194983adb7aceb9a8768f4fcae3aa8040987124e9f89cd690')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 2)
    outputverifier.verify_collated_copies(Intents.printintent, 2)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.roll1)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputverifier.outputsaver.operation_mode('NONE')
    tray.reset_trays()
