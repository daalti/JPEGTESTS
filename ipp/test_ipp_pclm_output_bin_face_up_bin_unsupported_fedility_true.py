import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value output_bin_face_up
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-58957
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23
    +test_classification:System
    +name:test_ipp_pclm_output_bin_face_up_bin_unsupported_fedility_true
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_output_bin_face_up_bin_unsupported_fedility_true
        +guid:1a4e61be-cc89-4395-97ec-b160d8067024
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaPath=FaceUp

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_output_bin_face_up_bin_unsupported_fedility_true(setup_teardown, printjob, outputverifier):
    ipp_test_attribs = {'document-format': 'application/PCLm', 'output-bin': 'face-up', 'bin': 'unsupported', 'ipp-attribute-fidelity': 'true'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')
    outputverifier.save_and_parse_output()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485283 IPP test for printing a pdf file using attribute value output-bin[Face-Up] bin:[unsupported] ipp-fidelity[true]
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:120
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
    +test_classification:System
    +name:test_ipp_pclm_output_bin_face_up_bin_unsupported_fidelity_true_pclm_letter_600_cjpeg_h64_pgcnt1_rgb
    +test:
        +title:test_ipp_pclm_output_bin_face_up_bin_unsupported_fidelity_true_pclm_letter_600_cjpeg_h64_pgcnt1_rgb
        +guid:fb6b469d-3185-4919-bbaf-1cc9e89c0b58
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaPath=FaceUp
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_output_bin_face_up_bin_unsupported_fidelity_true_pclm_letter_600_cjpeg_h64_pgcnt1_rgb(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)

    test_file = "/code/tests/print/pdl/ipp/attributes/output-bin_face-up_unsupported_ipp-fidelity-true.test"
    printjob.ipp_print(test_file, 'b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
