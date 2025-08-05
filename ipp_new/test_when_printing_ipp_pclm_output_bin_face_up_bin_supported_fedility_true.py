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
        +purpose: IPP test for printing a JPG file using attribute value output_bin_face_up
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-58957
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_output_bin_face_up_bin_supported_fedility_true_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCLm
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_pclm_output_bin_face_up_bin_supported_fedility_true
            +guid:09ce481b-165e-4f66-9fe9-30e9c7ee7000
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & MediaPath=FaceUp
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_output_bin_face_up_bin_supported_fedility_true_file_then_succeeds(self):
        ipp_test_attribs = {'document-format': 'application/PCLm', 'output-bin': 'face-up', 'bin': 'supported', 'ipp-attribute-fidelity': 'false'}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)
        
        job_id = self.print.ipp.start(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_and_parse_output()
        
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:C30485284 IPP test for printing a pdf file using attribute value output-bin[Face-Up] bin:[supported] ipp-fidelity[true]
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
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_output_bin_face_up_bin_supported_fedility_true_file_then_succeeds
        +test:
            +title:test_ipp_pclm_output_bin_face_up_bin_supported_fidelity_true_pclm_letter_600_cjpeg_h64_pgcnt1_rgb
            +guid:1e22d9b7-010d-4ba8-94d1-6b9169dbcb6f
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
    def test_when_using_ipp_pclm_output_bin_face_up_bin_supported_fedility_true_file_then_succeeds(self):
        job.bookmark_jobs()
        self.outputsaver.validate_crc_tiff()
        
        test_file_path = "/code/tests/print/pdl/ipp/attributes/output-bin_face-up_supported_ipp-fidelity-true.test"
        pirnt_file = self.print.get_file("b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8")
        returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, test_file_path, pirnt_file)
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
        
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')
