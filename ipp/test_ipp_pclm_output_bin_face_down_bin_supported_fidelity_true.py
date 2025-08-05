import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485271 IPP test for printing a JPG file using attribute value output-bin[Face-Down] output-bin[supported] ipp-fidelity[True]
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
    +name:test_ipp_pclm_output_bin_face_down_bin_supported_fidelity_true
    +test:
        +title:test_ipp_pclm_output_bin_face_down_bin_supported_fidelity_true
        +guid:89c1824c-e43a-4310-860a-a0028c6af124
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
def test_ipp_pclm_output_bin_face_down_bin_supported_fidelity_true(setup_teardown, printjob, job, outputverifier, outputsaver, tray, udw, reset_tray):
    job.bookmark_jobs()
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8_5x11in', default):
        tray.configure_tray(default, 'na_letter_8_5x11in', 'stationery')

    test_file = "/code/tests/print/pdl/ipp/attributes/output-bin-face-down-supported-ipp-fidelity-true.test"
    pirnt_file = printjob.get_file("b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8")
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, test_file, pirnt_file)
    logging.info(f"Ipp print output content is: <{decoded_output}>")
    assert returncode == 0, f'Unexpected IPP response: {returncode}'
    assert "[PASS]" or "[SKIP]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert decoded_output[1] == '', "There is error output for Ipp Print."

    # Different printer has different new jobs, such MarconiHiPDL generate 1 new job, but Selene generate 2 new jobs.
    job.wait_for_no_active_jobs()
    new_job = job.get_newjobs()
    for job_info in new_job:
        logging.info(f"check job {job_info} status is success")
        assert job_info['completionState'] == 'success'

    outputverifier.save_and_parse_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    logging.info("Verify output CRC successfully")
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
