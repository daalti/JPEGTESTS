import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177659 Ipp test for printing a PCLm file using attribute value media-size_letter
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-58957
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_GRAY__Blank_PNG_Source.pdf=7e0798c32b24bce14ca8c65fbbf8f6672506e2c047ce24ebc6eb2d2f8d66449c
    +name:test_ipp_pclm_jpeg_blank_page_gray
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_jpeg_blank_page_gray
        +guid:e844de60-fbab-4ec8-8921-8e7632044208
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
def test_ipp_pclm_jpeg_blank_page_gray(setup_teardown, outputverifier, printjob, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    ipp_test_attribs = {'document-format': 'application/PCLm', 'ipp-attribute-fidelity': 'true'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '7e0798c32b24bce14ca8c65fbbf8f6672506e2c047ce24ebc6eb2d2f8d66449c')
    outputverifier.save_and_parse_output()
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
