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
    +external_files:printfile17.pdf=b845606ab651f776ced2da15dca0499fe59f13459c7028764052ebc35cd43118
    +test_classification:System
    +name:test_pdl_apvt_dft1_pdf_600dpi_normal_letter_nomedia_notspeci_fit_file21
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_pdf_600dpi_normal_letter_nomedia_notspeci_fit_file21
        +guid:90759a7e-f164-40db-ae93-db12c597352b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PDF & PrintProtocols=IPP & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_pdf_600dpi_normal_letter_nomedia_notspeci_fit_file21(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_pdf_600dpi_normal_letter_nomedia_notspeci_fit_file22.test', 'b845606ab651f776ced2da15dca0499fe59f13459c7028764052ebc35cd43118')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"