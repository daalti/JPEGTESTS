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
    +external_files:printfile39.urf=c199a6c1fea8d8313010c9812d965f7fc5448ad548e3c1ebabb096c6ca1f87fa
    +test_classification:System
    +name:test_pdl_apvt_dft1_urf_mixedpageurf_RGB_deviceRGB_letter_nomedia_nospeci_file40
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_urf_mixedpageurf_RGB_deviceRGB_letter_nomedia_nospeci_file40
        +guid:af8ad48a-0001-4569-8f88-2de44c49502b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & Certifications=AirPrint


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_urf_mixedpageurf_RGB_deviceRGB_letter_nomedia_nospeci_file40(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_urf_mixedpageurf_RGB_deviceRGB_letter_nomedia_nospeci_file40.test', 'c199a6c1fea8d8313010c9812d965f7fc5448ad548e3c1ebabb096c6ca1f87fa')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"