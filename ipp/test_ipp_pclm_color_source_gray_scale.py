import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177631 Ipp test for printing a PCLm file using attribute value print-color-mode_process-monochrome
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-58957
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_GRAY__JPG_Source.pdf=321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0
    +name:test_ipp_pclm_color_source_gray_scale
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_color_source_gray_scale
        +guid:7bf758cf-6406-465c-9ce0-4f2e5bf5ae2e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_color_source_gray_scale(setup_teardown, printjob, outputverifier, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    ipp_test_attribs = {'document-format': 'application/PCLm', 'print-color-mode': 'monochrome'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0')
    outputverifier.save_and_parse_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
