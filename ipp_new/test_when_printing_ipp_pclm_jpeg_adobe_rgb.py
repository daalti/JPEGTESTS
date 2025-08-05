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
        +purpose:C52177661 Ipp test for printing a PCLm file using attribute value media-size_letter
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-58957
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_ADOBE-RGB__JPG_Source.pdf=39fe1b8bf99dcce812e8ad2dda3eceab4104f7949d65c1eccd792ad8a29bf3d3
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_jpeg_adobe_rgb_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCLm
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_pclm_jpeg_adobe_rgb
            +guid:d542889a-4451-49b4-8d81-285e49017905
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
        +overrides:
            +Home:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_jpeg_adobe_rgb_file_then_succeeds(self):
        self.outputsaver.operation_mode('TIFF')
        self.outputsaver.validate_crc_tiff()
        ipp_test_attribs = {'document-format': 'application/PCLm', 'ipp-attribute-fidelity': 'true'}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)
        
        job_id = self.print.ipp.start(ipp_test_file, '39fe1b8bf99dcce812e8ad2dda3eceab4104f7949d65c1eccd792ad8a29bf3d3')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_and_parse_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')
        
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:C30485369 BlankPage-JPEG(ADOBE-RGB) PCLm
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_ADOBE-RGB__Blank_PNG_Source.pdf=b2c5a5fe2a7e2ab45618cd1a41f6e466e153b999ec2eaf13e2b365eea0d84142
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_jpeg_adobe_rgb_file_then_succeeds
        +test:
            +title:test_ipp_pclm_jpeg_blank_page_adobe_rgb
            +guid:7ecb29c4-07e7-4505-af2f-97ce207c66c9
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
        +overrides:
            +Home:
                +is_manual:False
                +timeout:360
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_jpeg_adobe_rgb_file_then_succeeds(self):
        job.bookmark_jobs()
        self.outputsaver.validate_crc_tiff()
        
        print_file = self.print.get_file('b2c5a5fe2a7e2ab45618cd1a41f6e466e153b999ec2eaf13e2b365eea0d84142')
        ipp_test_file = '/code/tests/print/pdl/ipp/attributes/pclm_blank.test'
        
        returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, ipp_test_file , print_file)
        assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
        assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
        assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
        assert decoded_output[1] == '', "There is error output for Ipp Print."
        
        job.wait_for_no_active_jobs()
        new_job = job.get_newjobs()
        assert len(new_job) == 1, f"failed check job numbers"
        assert new_job[0]['completionState'] == 'success', "print job is not success"
        
        self.outputsaver.save_and_parse_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
