import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaType, ColorMode, PrintQuality
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media_size_A4_borderless
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-161515
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_Borderless.urf=6c166fdd93283833d7081553642786b0623ad120792fbbea6fa60631d0049984
    +name:test_ipp_urf_A4_borderless
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_A4_borderless
        +guid:97330c82-593d-4e70-ac4d-444403dec135
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & EngineFirmwareFamily=DoX

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_A4_borderless(setup_teardown, printjob, outputverifier, outputsaver, udw, tray):
    outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {
        'document-format': 'image/urf', 
        'media': 'iso_a4_210x297mm', 
        'sides': 'two-sided-long-edge', 
        'media-bottom-margin': 0, 
        'media-left-margin': 0, 
        'media-right-margin': 0, 
        'media-top-margin': 0, 
        'x-dimension':21000,
        'y-dimension':29700, 
        'ipp-attribute-fidelity': 'False', 
        'media-type': 'stationery'
    }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    printjob.ipp_print(ipp_test_file, '6c166fdd93283833d7081553642786b0623ad120792fbbea6fa60631d0049984')

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_print_quality(Intents.printintent, 1)
    outputsaver.operation_mode('NONE')

    Current_crc_value = outputsaver.get_crc()
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    tray.reset_trays()