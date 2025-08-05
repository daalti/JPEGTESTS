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
    +name:test_ipp_pclm_output_bin_face_up_fedility_false
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_output_bin_face_up_fedility_false
        +guid:f8a218fd-506a-473b-9ee9-6e0f5410a542
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaPath=FaceUp

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_output_bin_face_up_fedility_false(setup_teardown, printjob, outputverifier,outputsaver):
    ipp_test_attribs = {'document-format': 'application/PCLm', 'output-bin': 'face-up', 'ipp-attribute-fidelity': 'false'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')
    outputverifier.save_and_parse_output()    
    #switch back to default operation mode
    outputsaver.operation_mode('NONE')
    #collect and verify crc
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485281 IPP test for printing a pdf file using attribute value output-bin[Face-Up] ipp-fidelity[false]
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
    +name:test_ipp_pclm_output_bin_face_up_fidelity_false_pclm_letter_600_cjpeg_h64_pgcnt1_rgb
    +test:
        +title:test_ipp_pclm_output_bin_face_up_fidelity_false_pclm_letter_600_cjpeg_h64_pgcnt1_rgb
        +guid:8f339735-4b58-4ac0-a9f9-5aeb3fab7c47
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
def test_ipp_pclm_output_bin_face_up_fidelity_false_pclm_letter_600_cjpeg_h64_pgcnt1_rgb(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
    ipp_test_attribs = {'document-format': 'application/PCLm', 'output-bin': 'face-up', 'ipp-attribute-fidelity': 'false'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
    printjob.ipp_print(ipp_test_file, 'b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')    
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
    tray.reset_trays()