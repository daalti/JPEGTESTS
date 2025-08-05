import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485295 Print_Quality-unsupported printer-resolution
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
    +name:test_ipp_pclm_print_job_print_quality_unsupported_printer_resolution_ipp_fidelity_true
    +test:
        +title:test_ipp_pclm_print_job_print_quality_unsupported_printer_resolution_ipp_fidelity_true
        +guid:57e42754-367a-4840-8551-9e1e86a38fff
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
def test_ipp_pclm_print_job_print_quality_unsupported_printer_resolution_ipp_fidelity_true(setup_teardown, printjob, outputsaver, job):
    job.bookmark_jobs()
    print_file = printjob.get_file('b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')
    test_file_path = "/code/tests/print/pdl/ipp/attributes/print-quality-unsupported-printer-resolution.test"
    
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, test_file_path, print_file)
    assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
    assert decoded_output[1] == '', "There is error output for Ipp Print."
    logging.info("The file not printed, Crc is null. No need to check CRC for this case.")
    job.wait_for_no_active_jobs()
    new_job = job.get_newjobs()
    assert len(new_job) == 0, f"there is new job print {new_job}"
