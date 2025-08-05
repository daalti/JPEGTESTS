import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value orientation-requested_reverse-portrait
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter_Color_600.urf=6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f
    +name:test_ipp_urf_orientation_requested_reverse_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_orientation_requested_reverse_portrait
        +guid:85a8c42e-6ec9-4811-a784-92291e901233
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_orientation_requested_reverse_portrait(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')
    # orientation-requested: 5 = reverse-portrait
    ipp_test_attribs = {'document-format': 'image/urf', 'orientation-requested': 5}

    if 'reverse-portrait' not in printjob.capabilities.ipp.get('orientation-requested-supported'):
        logging.warning('Device does not support reverse-portrait as orientation-requested, setting fidelity to false...')
        ipp_test_attribs['ipp-attribute-fidelity'] = 'false'

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
