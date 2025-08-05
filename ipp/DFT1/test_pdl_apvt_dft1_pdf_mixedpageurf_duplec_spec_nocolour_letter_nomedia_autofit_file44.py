import pytest
import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd
import os

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile44.pdf=85673d632d5e743bc6c62d7502f06a38dc48cb0ac1939f7e99143fbe04bab83c
    +test_classification:System
    +name:test_pdl_apvt_dft1_pdf_mixedpageurf_duplec_spec_nocolour_letter_nomedia_autofit_file44
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_pdf_mixedpageurf_duplec_spec_nocolour_letter_nomedia_autofit_file44
        +guid:eff4fd2d-e537-47b4-a85a-fdede2188928
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PDF & PrintProtocols=IPP & Certifications=AirPrint & Duplexer=True

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_pdf_mixedpageurf_duplec_spec_nocolour_letter_nomedia_autofit_file44(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)

    attribute_file = os.path.join('/code','tests','print','pdl','ipp','attributes', 'get-printer-attributes.test')
    return_code, decoded_response = execute_ipp_cmd(printjob.ip_address, attribute_file,  '85673d632d5e743bc6c62d7502f06a38dc48cb0ac1939f7e99143fbe04bab83c')

    # extract supported values
    margin_supported = []
    for line in decoded_response[0].split('\n'):
        if 'media-bottom-margin-supported' in line:
            margin_supported = line.split('=')[1].strip().split(',')
            break
    logging.info(f"output-bin-supported: {margin_supported}")

    if '296' in margin_supported:
        logging.info(f"supported margin is 296")
        printjob.ipp_print_using_attribute_file('dft1_pdf_mixedpageurf_duplec_spec_nocolour_letter_nomedia_autofit_file44_margin296.test', '85673d632d5e743bc6c62d7502f06a38dc48cb0ac1939f7e99143fbe04bab83c')
    elif '423' in margin_supported:
        logging.info(f"supported margin is 423")
        printjob.ipp_print_using_attribute_file('dft1_pdf_mixedpageurf_duplec_spec_nocolour_letter_nomedia_autofit_file44.test', '85673d632d5e743bc6c62d7502f06a38dc48cb0ac1939f7e99143fbe04bab83c')
    else:
        logging.info("no test file with supported margin exist, please add one")
        return

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"