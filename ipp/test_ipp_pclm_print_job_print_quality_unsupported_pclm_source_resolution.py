import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485294 Print_Quality-unsupported pclm-source-resolution
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
    +name:test_ipp_pclm_print_job_print_quality_unsupported_pclm_source_resolution
    +test:
        +title:test_ipp_pclm_print_job_print_quality_unsupported_pclm_source_resolution
        +guid:20ff7908-d1c5-4cda-b6c7-32b5756e6afc
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
def test_ipp_pclm_print_job_print_quality_unsupported_pclm_source_resolution(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)

    print_file = printjob.get_file('b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')
    test_tile_path = "/code/tests/print/pdl/ipp/attributes/print-quality-unsupported-pclm-source-resolution.test"
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, test_tile_path , print_file)
    
    assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
    assert decoded_output[1] == '', "There is error output for Ipp Print."
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
