import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C51669439 IPP test for printing a pdf file using attribute value orientation_landscape
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:180
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_ipp_pdf_orientation_landscape
    +test:
        +title:test_ipp_pdf_orientation_landscape
        +guid:162cc890-0f0b-4cec-b61d-048fc6ce4ff1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pdf_orientation_landscape(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    # orientation-requested: 4 = landscape
    ipp_test_attribs = {'document-format': 'application/pdf', 'orientation-requested': 4}

    if 'landscape' not in printjob.capabilities.ipp.get('orientation-requested-supported'):
        logging.warning('Device does not support landscape as orientation-requested, setting fidelity to false...')
        ipp_test_attribs['ipp-attribute-fidelity'] = 'false'

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info(f"Validate current crc <{Current_crc_value}> with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
