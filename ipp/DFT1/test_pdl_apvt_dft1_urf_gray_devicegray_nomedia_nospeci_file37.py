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
    +external_files:printfile36.urf=2e3b9551bc751cbb84364dfbb98eca4acbdd9c08cb2ba9c71b7aa7eb51082422
    +test_classification:System
    +name:test_pdl_apvt_dft1_urf_mixedpageurf_gray_devicegray_nomedia_nospeci_file37
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_urf_mixedpageurf_gray_devicegray_nomedia_nospeci_file37
        +guid:533aa7a6-b485-4673-8e49-c37247720b22
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_urf_mixedpageurf_gray_devicegray_nomedia_nospeci_file37(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_urf_mixedpageurf_gray_devicegray_letter_nomedia_nospeci_file37.test', '2e3b9551bc751cbb84364dfbb98eca4acbdd9c08cb2ba9c71b7aa7eb51082422')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"