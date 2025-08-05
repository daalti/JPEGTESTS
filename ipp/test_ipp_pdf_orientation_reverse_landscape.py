import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value orientation_reverse_landscape
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
    +name:test_ipp_pdf_orientation_reverse_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pdf_orientation_reverse_landscape
        +guid:f47ed70c-0bfe-4d33-b16f-f9efe9b5d903
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pdf_orientation_reverse_landscape(setup_teardown, printjob, udw,outputsaver):
    outputsaver.validate_crc_tiff(udw)
    # orientation-requested: 6 = reverse-landscape
    ipp_test_attribs = {'document-format': 'application/pdf', 'orientation-requested': 6}

    if 'reverse-landscape' not in printjob.capabilities.ipp.get('orientation-requested-supported'):
        logging.warning('Device does not support reverse-landscape as orientation-requested, setting fidelity to false...')
        ipp_test_attribs['ipp-attribute-fidelity'] = 'false'

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
