import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485293 Print_Quality-invalid print-quality- ipp-fidelity = false
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:360
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
    +test_classification:System
    +name:test_ipp_pclm_print_job_invalid_print_quality_fidelity_false
    +test:
        +title:test_ipp_pclm_print_job_invalid_print_quality_fidelity_false
        +guid:a11b7e50-6820-477d-9774-8df4b2b04d98
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
def test_ipp_pclm_print_job_invalid_print_quality_fidelity_false(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)

    ipp_test_file= "/code/tests/print/pdl/ipp/attributes/print-quality-invalid-values-fidelity-false.test"
    printjob.ipp_print(ipp_test_file, 'b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
