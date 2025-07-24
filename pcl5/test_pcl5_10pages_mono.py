import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaType, MediaSize, ColorMode

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Pcl5 letter Page from 10pgs_Letter_Plain.prn file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-223392
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:10pgs_Letter_Plain.prn=81b00eaa2f06be2bdf7b27f025c6b703da3c600b4fdb28a06086f0bb4236af47
    +name:test_pcl5_10pages_mono
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_10pages_mono
        +guid:fabecba8-5e24-4d70-88d2-143b9463aa76
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_10pages_mono(setup_teardown, printjob, outputverifier, outputsaver, udw, tray):
    outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    if tray.is_media_combination_supported(default, 'na_letter_8.5x11in', 'stationery'):
         tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
         printjob.print_verify('81b00eaa2f06be2bdf7b27f025c6b703da3c600b4fdb28a06086f0bb4236af47')

         outputverifier.save_and_parse_output()
         outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
         outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
         outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
         outputsaver.operation_mode('NONE')

         Current_crc_value = outputsaver.get_crc()
         assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    else:
        logging.info('Media size na_letter_8.5x11in is not supported in the default tray')    

    tray.reset_trays()