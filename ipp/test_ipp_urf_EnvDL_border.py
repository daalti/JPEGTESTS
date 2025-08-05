import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaType
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media_size_Envelope_DL
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-185216
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DL.urf=0c6fda1e26ac577fab41f56f05bd7f1ecdfb17e0d8c7029f729895bcff461213
    +name:test_ipp_urf_EnvDL_border
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_EnvDL_border
        +guid:1355b017-9962-4ca3-b194-858c22127d3e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaSizeSupported=iso_dl_110x220mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_EnvDL_border(setup_teardown, printjob, outputverifier, outputsaver, udw, tray):
    outputsaver.validate_crc_tiff(udw) 

    default = tray.get_default_source()
    if tray.is_media_combination_supported(default, 'iso_dl_110x220mm', 'stationery'):
        tray.configure_tray(default, 'iso_dl_110x220mm', 'stationery')

        ipp_test_attribs = {
            'document-format': 'image/urf', 
            'media': 'iso_dl_110x220mm', 
            'sides': 'one-sided',
            'media-bottom-margin': 296, 
            'media-left-margin': 296, 
            'media-right-margin': 296, 
            'media-top-margin': 296, 
            'x-dimension':11000,
            'y-dimension':22000, 
            'ipp-attribute-fidelity': 'False', 
            'media-type': 'stationery'
        }

        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
        printjob.ipp_print(ipp_test_file, '0c6fda1e26ac577fab41f56f05bd7f1ecdfb17e0d8c7029f729895bcff461213')

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.dlenvelope)
        outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        outputsaver.operation_mode('NONE')

        Current_crc_value = outputsaver.get_crc()
        assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    else:
        logging.info('Media size iso_dl_110x220mm is not supported in the default tray')    

    tray.reset_trays()