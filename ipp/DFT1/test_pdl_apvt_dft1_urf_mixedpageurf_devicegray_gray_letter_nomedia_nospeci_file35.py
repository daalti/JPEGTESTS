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
    +external_files:printfile34.urf=0514c9e48db3d6c186299abb95f57bd7c9c289aaed1af0660e1450ab44efaad5
    +test_classification:System
    +name:test_pdl_apvt_dft1_urf_mixedpageurf_devicegray_gray_letter_nomedia_nospeci_file35
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_urf_mixedpageurf_devicegray_gray_letter_nomedia_nospeci_file35
        +guid:6f2a08a3-443e-4300-92ce-008ace9c52ed
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_urf_mixedpageurf_devicegray_gray_letter_nomedia_nospeci_file35(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_urf_mixedpageurf_devicegray_gray_letter_nomedia_nospeci_file35.test', '0514c9e48db3d6c186299abb95f57bd7c9c289aaed1af0660e1450ab44efaad5')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"