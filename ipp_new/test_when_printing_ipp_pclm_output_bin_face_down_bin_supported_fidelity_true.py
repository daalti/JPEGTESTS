import logging

from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

class TestWhenPrintingFileFromIPP(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""
        # no-op unless the legacy file had a matching teardown
        pass

    def teardown_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Reset media configuration to default
        self.media.update_media_configuration(self.default_configuration)
        self.media.reset_inputs()

        tear_down_output_saver(self.outputsaver)
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:C30485271 IPP test for printing a JPG file using attribute value output-bin[Face-Down] output-bin[supported] ipp-fidelity[True]
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_output_bin_face_down_bin_supported_fidelity_true_file_then_succeeds
        +test:
            +title:test_ipp_pclm_output_bin_face_down_bin_supported_fidelity_true
            +guid:4c7ce08c-1ad0-458a-b9e6-c626ad4b5b2f
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
    def test_when_using_ipp_pclm_output_bin_face_down_bin_supported_fidelity_true_file_then_succeeds(self):
        job.bookmark_jobs()
        self.outputsaver.validate_crc_tiff()
        
        test_file = "/code/tests/print/pdl/ipp/attributes/output-bin-face-down-supported-ipp-fidelity-true.test"
        pirnt_file = self.print.get_file("b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8")
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
        
        self.outputsaver.save_and_parse_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        logging.info("Verify output CRC successfully")
        self.outputsaver.operation_mode('NONE')
