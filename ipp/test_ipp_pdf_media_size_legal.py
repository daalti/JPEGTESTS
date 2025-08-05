import logging
from dunetuf.print.output.intents import Intents, MediaSize


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C51669486 IPP test for printing a pdf file using attribute value media_size_legal
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
    +name:test_ipp_pdf_media_size_legal
    +test:
        +title:test_ipp_pdf_media_size_legal
        +guid:3bf8d613-a560-468a-8447-f8f7d811f7a0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_legal_8.5x14in
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pdf_media_size_legal(setup_teardown, reset_tray, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')

    ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_legal_8.5x14in'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 5)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.legal)
    Current_crc_value = outputsaver.get_crc()
    logging.info(f"Validate current crc <{Current_crc_value}> with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
