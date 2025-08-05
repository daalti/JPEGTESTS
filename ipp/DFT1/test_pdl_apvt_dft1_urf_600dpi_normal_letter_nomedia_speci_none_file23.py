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
    +external_files:printfile23.urf=2e28f247e5127bccef4c8d63fdd04a2574248f81f105e15bee72cbbf07836672
    +test_classification:System
    +name:test_pdl_apvt_dft1_urf_600dpi_normal_letter_nomedia_speci_none_file23
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_urf_600dpi_normal_letter_nomedia_speci_none_file23
        +guid:d64a2e0e-47ed-47b1-8679-175cee051d1a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PDF & PrintProtocols=IPP & Certifications=AirPrint


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_urf_600dpi_normal_letter_nomedia_speci_none_file23(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_urf_600dpi_normal_letter_nomedia_speci_none_file23.test', '2e28f247e5127bccef4c8d63fdd04a2574248f81f105e15bee72cbbf07836672')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"