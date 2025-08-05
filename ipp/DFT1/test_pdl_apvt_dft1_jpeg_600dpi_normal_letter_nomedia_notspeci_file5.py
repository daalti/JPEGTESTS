import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile5.jpg=951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4
    +test_classification:System
    +name:test_pdl_apvt_dft1_jpeg_600dpi_normal_letter_nomedia_notspeci_file5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_jpeg_600dpi_normal_letter_nomedia_notspeci_file5
        +guid:43ea41e8-2c91-4582-8e90-800d9dbe95c1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_jpeg_600dpi_normal_letter_nomedia_notspeci_file5(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_jpeg_600dpi_normal_letter_nomedia_notspeci_file5.test', '951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"