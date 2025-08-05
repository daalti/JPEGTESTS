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
        +purpose:Ipp test for printing a URF file using attribute value print-content-optimize_text_and_graphics
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-58957
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__Graphics.pdf=5d2c2739f4126a4a74d3a9da7d3d261255f572999dd4abd3957f734561c0c240
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_content_optimize_text_and_graphics_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCLm
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_pclm_print_content_optimize_text_and_graphics
            +guid:e1184599-c57d-46a5-9e65-cb2ea945c3a0
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_print_content_optimize_text_and_graphics_file_then_succeeds(self):
        self.outputsaver.operation_mode('TIFF')
        ipp_test_attribs = {'document-format': 'image/urf', 'print-content-optimize': 'text-and-graphics'}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)
        
        job_id = self.print.ipp.start(ipp_test_file, '5d2c2739f4126a4a74d3a9da7d3d261255f572999dd4abd3957f734561c0c240')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_and_parse_output()
        self.outputsaver.operation_mode('NONE')
        
        
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:C30485386 Print_Content_Optimize-optimize-text-and-graphics
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__TextGraphicsColor.pdf=8a10be5fa5db739b4454c82329533a2e030d79d1bd285fff0620e3aadc32980b
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_content_optimize_text_and_graphics_file_then_succeeds
        +test:
            +title:test_ipp_pclm_print_pclm_letter_600_cjpeg_h64_pgcnt1_rgb_text_graphics_color
            +guid:a2dc4dee-671f-4c07-9c86-156b8df70c0c
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCLm & PrintProtocols=IPP
        +overrides:
            +Home:
                +is_manual:False
                +timeout:300
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_print_content_optimize_text_and_graphics_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        
        print_file = self.print.get_file('8a10be5fa5db739b4454c82329533a2e030d79d1bd285fff0620e3aadc32980b')
        ipp_test_file = "/code/tests/print/pdl/ipp/attributes/print-content-optimize-text-and-graphics.test"
        
        returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, ipp_test_file , print_file)
        assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
        assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
        assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
        assert "print-content-optimize (keyword) = text-and-graphics" in decoded_output[0], "Text and Graphics should not be seen for the listed attribute."
        assert decoded_output[1] == '', "There is error output for Ipp Print."
        
        self.outputsaver.save_and_parse_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
