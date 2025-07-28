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
        +purpose:Simple print job of cumulative urf from *cumulative.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:cumulative.urf=35fa00f34c142dfedb608319e364efe600d48292b83382b7e1768e1bc65b8f24
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_cumulative_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_cumulative_page
            +guid:4425e84c-855e-4c8f-8006-3b03ba426237
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_cumulative_file_then_succeeds(self):
        # TODO: In case of failure in the future, check for media size requested, load if supported
        job_id = self.print.raw.start('35fa00f34c142dfedb608319e364efe600d48292b83382b7e1768e1bc65b8f24')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("URF Cumulative page - Print job completed successfully")
