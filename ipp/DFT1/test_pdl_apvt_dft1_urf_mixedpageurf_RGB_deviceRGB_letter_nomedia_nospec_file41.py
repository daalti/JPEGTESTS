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
    +external_files:printfile41.urf=ce888f61f9d976a27d18627bd83bf78deadb7591e7a4fda431f84b6f322cdcc3
    +test_classification:System
    +name:test_pdl_apvt_dft1_urf_mixedpageurf_RGB_gray_letter_nomedia_nospeci_file41
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft1_urf_mixedpageurf_RGB_gray_letter_nomedia_nospeci_file41
        +guid:a1a6c49f-e647-4447-8220-19d99efe84d1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_apvt_dft1_urf_mixedpageurf_RGB_gray_letter_nomedia_nospeci_file41(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft1_urf_mixedpageurf_RGB_gray_letter_nomedia_nospeci_file41.test', 'ce888f61f9d976a27d18627bd83bf78deadb7591e7a4fda431f84b6f322cdcc3')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"