import pytest
import os
import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value output_bin_face_down
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_ipp_jpg_output_bin_face_down
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_output_bin_face_down
        +guid:9ce373d8-e729-4a8e-a869-49b20607b649
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaPath=FaceDown

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_output_bin_face_down(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
    
    attribute_file = os.path.join('/code','tests','print','pdl','ipp','attributes', 'get-printer-attributes.test')
    return_code, decoded_response = execute_ipp_cmd(printjob.ip_address, attribute_file,  '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')

    # extract supported values
    output_bin_supported = []
    for line in decoded_response[0].split('\n'):
        if 'output-bin-supported' in line:
            output_bin_supported = line.split('=')[1].strip().split(',')
            break
    logging.info(f"output-bin-supported: {output_bin_supported}")

    if 'face-down' in output_bin_supported:
        logging.info(f"face-down is supported")
        ipp_test_attribs = {'document-format': 'application/pdf', 'output-bin': 'face-down'}
    else:
        logging.info(f"face-down is not supported")
        ipp_test_attribs = {'document-format': 'application/pdf'}

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
