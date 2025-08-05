import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, ColorRenderingType, ContentOrientation, PrintQuality, Plex, PlexBinding, PlexSide, MediaType, NeutralAxisType, HalftoneType, TrappingLevel
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value media_size_A4
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-130719
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Landscape_DSC05055.jpg=f979b97722a48b5979b40e3ea827329dd651e2875b3807cdccda53a2c1b7cd6e
    +test_classification:System
    +name:test_pdl_intent_ipp_jpg_landscape_mainroll
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_jpg_landscape_mainroll
        +guid:7c414a60-8621-4ff9-80f3-891940706ec0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_jpg_landscape_mainroll(setup_teardown, printjob, outputsaver, tray, outputverifier, configuration, udw):
    ipp_test_attribs = {'document-format': 'image/jpeg', 'media-source': 'main-roll', 'print-color-mode': 'color'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'f979b97722a48b5979b40e3ea827329dd651e2875b3807cdccda53a2c1b7cd6e')
    outputsaver.save_output()
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    
    for page in outputverifier.get_intent(Intents.printintent):
            logging.debug('Page Height: %s and Page Width: %s on page %s', page.page_height, page.page_width, page.page_number)
            assert page.page_height > page.page_width, f'Unexpected output diemension'
    # CRC check
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
    tray.reset_trays()