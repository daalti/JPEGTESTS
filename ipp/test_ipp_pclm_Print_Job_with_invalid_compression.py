import pytest
import logging

from dunetuf.print.output.intents import Intents


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a PCLm file **
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-58957
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23
    +test_classification:System
    +name:test_ipp_pclm_validate_printjob
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_validate_printjob
        +guid:07bc390f-fa8e-45e7-ab11-dc2264048d16
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_validate_printjob(setup_teardown, printjob, outputverifier, outputsaver):
    outputsaver.operation_mode('TIFF')
    expected_error="client-error-compression-not-supported"
    try:
        ipp_test_attribs = {'document-format': 'application/PCLm', 'compression': '"NotSupported"','ipp-attribute-fidelity': 'false'}
        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

        printjob.ipp_print(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')

    except AssertionError as exp:
        if 'Unexpected IPP response' in str(exp):
            if expected_error in str(exp):
                logging.debug(f'Found expected error "{expected_error}" for attribute "compression" with fidelity as false')
            else:
                assert False, f'Not found expected error "{expected_error}" for attribute "compression" with fidelity as false'
    outputsaver.operation_mode('NONE')

