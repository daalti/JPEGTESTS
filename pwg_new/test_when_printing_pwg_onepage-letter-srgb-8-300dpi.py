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
    +purpose:Simple print job of pwg onepage letter srgb 8-300dpi page from *onepage-letter-srgb-8-300dpi.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:300
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:onepage-letter-srgb-8-300dpi.pwg=f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e
    +name:TestWhenPrintingJPEGFile::test_when_using_pwg_onepage-letter-srgb-8-300dpi_file_then_succeeds
    +test:
        +title:test_pwg_onepage_letter_srgb_8_300dpi
        +guid:50a1b604-ece6-4040-b0fa-cf5070be5691
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
$$$$$_END_TEST_METADATA_DECLARATION_$$$$"""
    def test_when_using_pwg_onepage-letter-srgb-8-300dpi_file_then_succeeds(self):
        job_id = self.print.raw.start('f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
