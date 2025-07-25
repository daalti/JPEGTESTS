from dunetuf.print.print_common_types import MediaSize, MediaType
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
        +purpose:PostScript high value test using **9587eb968f64f6d6fc20e5b3d0d71abc.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:9587eb968f64f6d6fc20e5b3d0d71abc.jpg=18f25bed0d24c7ed1203c867676b1d33903edcf6643c77989a31a85721f88357
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_9587eb968f64f6d6fc20e5b3d0d71abc_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_9587eb968f64f6d6fc20e5b3d0d71abc
            +guid:5eaa2431-40b3-422a-b98a-237b9bf715c6
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_9587eb968f64f6d6fc20e5b3d0d71abc_file_then_succeeds(self):

        job_id = self.print.raw.start('18f25bed0d24c7ed1203c867676b1d33903edcf6643c77989a31a85721f88357')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()