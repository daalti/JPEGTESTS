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
    +external_files:printfile38.urf=263bc758197002d61f7f41534d546cc9bbd6212c82697f8f3979100204713e92
    +test_classification:System
    +name:test_pdl_apvt_dft1_urf_mixedpageurf_RDB_devicegray_letter_nomedia_nospeci_file38
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_urf_mixedpageurf_RDB_devicegray_letter_nomedia_nospeci_file38
        +guid:febcf26e-27e4-48d6-8d5a-c7be17168263
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_urf_mixedpageurf_RDB_devicegray_letter_nomedia_nospeci_file38(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_urf_mixedpageurf_RDB_devicegray_letter_nomedia_nospeci_file38.test', '263bc758197002d61f7f41534d546cc9bbd6212c82697f8f3979100204713e92')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"