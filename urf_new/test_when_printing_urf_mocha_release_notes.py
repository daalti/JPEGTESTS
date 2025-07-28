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

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job of Urf Mocha Release Notes Page from *MochaReleaseNotes.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:MochaReleaseNotes.urf=4f58e92c69b089c787efe90ed9a9bec69a58e90d3a128c4b0ca9d1e1dd4208de
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_mocha_release_notes_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_mocha_release_notes_page
            +guid:94d8f254-5603-4e5e-bc76-b9f1b409b9bc
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_mocha_release_notes_file_then_succeeds(self):
        # TODO: In case of failure in the future, check for media size requested, load if supported
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('4f58e92c69b089c787efe90ed9a9bec69a58e90d3a128c4b0ca9d1e1dd4208de')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
    
        logging.info("URF Mocha Release Notes Page - Print job completed successfully")
