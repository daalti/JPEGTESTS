import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a PCLm file using attribute value output_bin_face_down with fidelity true
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
    +name:test_ipp_pclm_output_bin_face_down_fedility_false
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_output_bin_face_down_fedility_false
        +guid:da949be3-588a-407d-97fa-3ce807c72c57
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_output_bin_face_down_fedility_false(setup_teardown, printjob, outputverifier, tray, outputsaver):
    outputsaver.operation_mode('TIFF')
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8_5x11in', default):
        tray.configure_tray(default, 'na_letter_8_5x11in', 'stationery')

    ipp_test_attribs = {'document-format': 'application/PCLm', 'output-bin': 'face-down', 'ipp-attribute-fidelity': 'false'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')
    outputverifier.save_and_parse_output()
    outputsaver.operation_mode('NONE')



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485269 IPP test for printing a PCLm file using attribute value output-bin[Face-Down] ipp-fidelity[false]
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
    +name:test_ipp_pclm_output_bin_face_down_fedility_false_pclm_letter_600_cjpeg_h64_pgcnt1_rgb
    +test:
        +title:test_ipp_pclm_output_bin_face_down_fedility_false_pclm_letter_600_cjpeg_h64_pgcnt1_rgb
        +guid:d5927ea4-d3eb-4a71-b31d-d87f5fc0d24c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaPath=FaceDown
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_output_bin_face_down_fedility_false_pclm_letter_600_cjpeg_h64_pgcnt1_rgb(setup_teardown, printjob, outputverifier, tray, outputsaver, udw, reset_tray):
    outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8_5x11in', default):
        tray.configure_tray(default, 'na_letter_8_5x11in', 'stationery')

    ipp_test_attribs = {'document-format': 'application/PCLm', 'output-bin': 'face-down', 'ipp-attribute-fidelity': 'false'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    printjob.ipp_print(ipp_test_file, 'b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')

    outputverifier.save_and_parse_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    logging.info("Verify output CRC successfully")
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
