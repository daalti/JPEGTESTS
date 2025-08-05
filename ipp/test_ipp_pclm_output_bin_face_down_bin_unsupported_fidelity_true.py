import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485270 IPP test for printing a JPG file using attribute value output-bin[Face-Down] output-bin[notsupported] ipp-fidelity[True]
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
    +name:test_ipp_pclm_output_bin_face_down_bin_unsupported_fidelity_true
    +test:
        +title:test_ipp_pclm_output_bin_face_down_bin_unsupported_fidelity_true
        +guid:36760a3d-d0d9-48dd-8b72-854be585f825
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
def test_ipp_pclm_output_bin_face_down_bin_unsupported_fidelity_true(setup_teardown, printjob, outputverifier, outputsaver, tray, udw, reset_tray):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8_5x11in', default):
        tray.configure_tray(default, 'na_letter_8_5x11in', 'stationery')

    test_file = "/code/tests/print/pdl/ipp/attributes/output-bin-face-down-unsupported-ipp-fidelity-true.test"
    printjob.ipp_print(test_file, 'b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')
    
    outputverifier.save_and_parse_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    logging.info("Verify output CRC successfully")
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
