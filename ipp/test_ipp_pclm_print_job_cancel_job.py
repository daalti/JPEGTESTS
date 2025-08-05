import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485275 IPP test for print-job and cancel-job
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:540
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
    +test_classification:System
    +name:test_ipp_pclm_print_job_cancel_job
    +test:
        +title:test_ipp_pclm_print_job_cancel_job
        +guid:0ab8dfce-87e5-48ff-9ea8-b2811138fd0d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:540
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_job_cancel_job(setup_teardown, printjob, outputsaver, udw, job):
    job.bookmark_jobs()
    outputsaver.validate_crc_tiff(udw)

    print_job_test_file = "/code/tests/print/pdl/ipp/attributes/print-job.test"
    cancel_job_text_file = "/code/tests/print/pdl/ipp/attributes/cancel-job.test"
    pirnt_file = printjob.get_file("b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8")
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, print_job_test_file, pirnt_file)
    logging.info(f"Ipp print output content is: <{decoded_output}>")
    assert returncode == 0, f'Unexpected IPP response: {returncode}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert decoded_output[1] == '', "There is error output for Ipp Print."
    # Different printer has different new jobs, such MarconiHiPDL generate 1 new job, but VictoriaPlus generate 2 new jobs.
    job.wait_for_no_active_jobs()
    new_job = job.get_newjobs()
    for job_info in new_job:
        logging.info(f"check job {job_info} status is success")
        assert job_info['completionState'] == 'success'
    logging.info("The print-job test executed successfully")

    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, cancel_job_text_file, pirnt_file)
    logging.info(f"Ipp print output content is: <{decoded_output}>")
    assert returncode == 0, f'Unexpected IPP response: {returncode}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert decoded_output[1] == '', "There is error output for Ipp Print."
    # Different printer has different new jobs, such MarconiHiPDL generate 1 new job, but VictoriaPlus generate 2 new jobs.
    job.wait_for_no_active_jobs()
    new_job = job.get_newjobs()
    for job_info in new_job:
        logging.info(f"check job {job_info} status is success")
        assert job_info['completionState'] == 'success'
    logging.info("The cancel-job test executed successfully")

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    logging.info("Verify output CRC successfully")
    outputsaver.operation_mode('NONE')
