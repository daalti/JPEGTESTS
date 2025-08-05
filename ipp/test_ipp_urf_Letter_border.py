import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaType
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media_size_Letter
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-61790
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:filemBiwTh.urf=37c799f2b4c300ddc159bc3fa9f02d40307aec0cff94361ac6f830131361aa1c
    +name:test_ipp_urf_Letter_border
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_Letter_border
        +guid:d9de529b-a447-4449-9226-559b49ef9b76
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_Letter_border(setup_teardown, printjob, outputverifier, outputsaver, udw, tray):
    outputsaver.validate_crc_tiff(udw) 

    default = tray.get_default_source()
    if tray.is_media_combination_supported(default, 'na_letter_8.5x11in', 'stationery'):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

        ipp_test_attribs = {
            'document-format': 'image/urf', 
            'media': 'na_letter_8.5x11in', 
            'sides': 'one-sided',
            'media-bottom-margin': 499, 
            'media-left-margin': 499, 
            'media-right-margin': 499, 
            'media-top-margin': 499, 
            'x-dimension':21590,
            'y-dimension':27940, 
            'ipp-attribute-fidelity': 'False', 
            'media-type': 'stationery'
        }

        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
        printjob.ipp_print(ipp_test_file, '37c799f2b4c300ddc159bc3fa9f02d40307aec0cff94361ac6f830131361aa1c')

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
        outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        outputsaver.operation_mode('NONE')

        Current_crc_value = outputsaver.get_crc()
        assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    else:
        logging.info('Media size na_letter_8.5x11in is not supported by the printer')
    
    tray.reset_trays()

