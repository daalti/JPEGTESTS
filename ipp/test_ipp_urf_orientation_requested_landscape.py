import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value orientation-requested_landscape
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
    +name:test_ipp_urf_orientation_requested_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_orientation_requested_landscape
        +guid:9ef198cf-ac5c-456b-8285-721fd5d33250
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_orientation_requested_landscape(setup_teardown, printjob, outputsaver,udw):
    outputsaver.validate_crc_tiff(udw)
    # orientation-requested: 4 = landscape
    ipp_test_attribs = {'document-format': 'image/urf', 'orientation-requested': 4}

    if 'landscape' not in printjob.capabilities.ipp.get('orientation-requested-supported'):
        logging.warning('Device does not support landscape as orientation-requested, setting fidelity to false...')
        ipp_test_attribs['ipp-attribute-fidelity'] = 'false'

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"