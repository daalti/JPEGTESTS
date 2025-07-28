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
        +purpose:Simple print job of Urf Quartz Page from *Quartz.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Quartz.urf=a3696c8f81d2fafe6d0934e4a70ee6e485a6043f4ec7de1c0627843d68d09968
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_quartz_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_quartz_page
            +guid:ccc31509-8d68-45c9-910c-de24e960796c
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_quartz_file_then_succeeds(self):
        # TODO: In case of failure in the future, check for media size requested, load if supported
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('a3696c8f81d2fafe6d0934e4a70ee6e485a6043f4ec7de1c0627843d68d09968')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
    
        logging.info("URF Quartz Page - Print job completed successfully")
