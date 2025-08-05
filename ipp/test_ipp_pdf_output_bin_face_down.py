import pytest
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd
import logging
import os


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value output_bin_face_down
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_ipp_pdf_output_bin_face_down
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pdf_output_bin_face_down
        +guid:076a6291-8c95-4d3c-9fd6-420a3f692d0f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaPath=FaceDown

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pdf_output_bin_face_down(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    attribute_file = os.path.join('/code','tests','print','pdl','ipp','attributes', 'get-printer-attributes.test')
    return_code, decoded_response = execute_ipp_cmd(printjob.ip_address, attribute_file,  '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')

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
    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
