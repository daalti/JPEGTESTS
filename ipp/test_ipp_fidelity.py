import pytest
import logging


ATTRIBUTES = {
    'output-bin': 'dummy-tray',
    'resolution': '1234x1234dpi',
    'print-quality': 100,
    'copies': 100,
    'page-ranges': '0-0',
    'orientation-requested': 100,
    'sides': 'dummySide',
    'multiple-document-handling': 'dummpyDoc',
    'scaling': 'dummyFit',
    'print-color-mode': 'dummyColor',
    'output-mode': 'dummyOutputMode',
    'print-content-optimize': 'dummyOptimizer',
    'print-rendering-intent': 'dummyRendering',
    'media': 'dummyMedia',
    'media-source': 'dummyMediaSource',
    'media-type': 'dummyMediaType',
    'media-top-margin': 'dummyTopMargin',
    'media-bottom-margin': 'dummyBottomMargin',
    'media-left-margin': 'dummyLeftMargin',
    'media-right-margin': 'dummyRightMargin'
}


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test with fidelity true and invalid values
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_ipp_fidelity_true
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_fidelity_true
        +guid:138a0ac4-fede-44dd-b925-77266e14d718
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_fidelity_true(setup_teardown, printjob):
    for key, value in ATTRIBUTES.items():
        ipp_test_attribs = {'document-format': 'application/pdf', 'ipp-attribute-fidelity': 'true', key: value}
        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

        try:
            logging.info('Verifying fidelity with attribute: %s', key)

            printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
            assert False, f'Test was expectd to fail with {key} as {value}'
        except AssertionError as exp:
            if 'Unexpected IPP response' in str(exp):
                logging.info('Test failed as expected with %s as %s', key, value)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test with fidelity false and invalid values
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:900
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_ipp_fidelity_false
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_fidelity_false
        +guid:3de7ddd8-c9f9-4b04-a0f1-fb465a016dbf
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_fidelity_false(setup_teardown, printjob):
    no_exception = []
    unpexecpted_ipp_error = []
    non_ipp_exception = []

    expected_error = {
        'page-ranges': 'client-error-bad-request'
    }

    for key, value in ATTRIBUTES.items():
        logging.info('Verifying fidelity with attribute: %s', key)

        try:
            ipp_test_attribs = {'document-format': 'application/pdf', 'ipp-attribute-fidelity': 'false', key: value}
            ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

            printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')

            # There was not AssertionError, indicating the successful command
            # execution. Ensure attribute is not part of the expected_error.
            if key in expected_error.keys():
                no_exception.append(key)

        except AssertionError as exp:
            if 'Unexpected IPP response' in str(exp):
                # Check if attribute is part of the expected_error, check for
                # the IPP error response. Capture the attribute if the error
                # response does not match with what's expected. If the attribute
                # is not part of the expected_error, simply log and continue.
                if key in expected_error.keys():
                    if expected_error[key] in str(exp):
                        logging.debug(f'Found expected error "{expected_error[key]}" for attribute "{key}" with fidelity as false')
                    else:
                        logging.debug(f'Expected error "{expected_error[key]}" for attribute "{key}" with fidelity as false was not found!')
                        unpexecpted_ipp_error.append(key)
                else:
                   logging.debug(f'No error response is expected for attribute "{key}" with fidelity as false')
                   non_ipp_exception.append(key)
            else:
                # Capture the attribute if the assertion error is coming from
                # somewhere else or does not match the 'Unexpected IPP response'.
                logging.debug(f'Expected IPP response exception was not found for "{key}" with fidelity as false')
                non_ipp_exception.append(key)

    assert len(no_exception) == 0, 'No expceptions were found for following attributes: {no_exception}'
    assert len(unpexecpted_ipp_error) == 0, 'Unexpected error response for following attributes: {unpexecpted_ipp_error}'
    assert len(non_ipp_exception) == 0, 'Unexpected IPP response exception for following attributes: {non_ipp_exception}'