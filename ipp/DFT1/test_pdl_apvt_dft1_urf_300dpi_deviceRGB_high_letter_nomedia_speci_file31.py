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
    +external_files:printfile31.urf=372681abf30791fa2a52eae63b680c2de807fb8c2e4584146a9dccab5513f6ca
    +test_classification:System
    +name:test_pdl_apvt_dft1_urf_300dpi_deviceRGB_High_letter_nomedia_speci_file31
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_urf_300dpi_deviceRGB_High_letter_nomedia_speci_file31
        +guid:7d2cb486-8e06-420f-98b5-4e059da74dc4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_urf_300dpi_deviceRGB_High_letter_nomedia_speci_file31(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_urf_300dpi_deviceRGB_High_letter_nomedia_speci_file31.test', '372681abf30791fa2a52eae63b680c2de807fb8c2e4584146a9dccab5513f6ca')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"