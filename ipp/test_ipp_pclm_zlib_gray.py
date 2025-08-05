import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177669 Ipp test for printing a PCLm file using attribute value media-size_letter
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-58957
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_czlib_H64_PgCnt1_GRAY__JPG_Source.pdf=dcee22fecadef3c2ee97d22b68301ba5a7450e52f81617044a6fad7f5612b5df
    +name:test_ipp_pclm_zlib_gray
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_zlib_gray
        +guid:a83e21ac-fcaf-4d88-a9ed-55ac2eb6ce6f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_zlib_gray(setup_teardown, printjob, outputsaver, tray, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw) 
    ipp_test_attribs = {'document-format': 'application/PCLm', 'ipp-attribute-fidelity': 'true'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, 'dcee22fecadef3c2ee97d22b68301ba5a7450e52f81617044a6fad7f5612b5df')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
