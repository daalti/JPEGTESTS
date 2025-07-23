import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

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
        tear_down_output_saver(self.outputsaver)
    """$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg hs_letter_color_one_page *Hs_LTR_Color_1pg.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:Hs_LTR_Color_1pg.pwg=6ca956aa09ba67fc5cbf45117681e76bf5022d8bd825e558b85615805ecf3b44
    +name:TestWhenPrintingJPEGFile::test_when_using_pwg_hs_letter_color_one_page_file_then_succeeds
    +test:
        +title:test_pwg_hs_letter_color_one_page
        +guid:2fe2f628-a026-48ad-9214-5b15ed79099e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
$$$$$_END_TEST_METADATA_DECLARATION_$$$$"""
    def test_when_using_pwg_hs_letter_color_one_page_file_then_succeeds(self):
        job_id = self.print.raw.start('6ca956aa09ba67fc5cbf45117681e76bf5022d8bd825e558b85615805ecf3b44')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
