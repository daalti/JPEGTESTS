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
        +purpose: pcl5 lowvaluenew using 45Page_lineterm.obj
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:45Page-lineterm.obj=2015dd02b31ae61c02b0ff2013400c6417e8e53cb44d7cdb1e66bab6bd267db9
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_lowvaluenew_45page_lineterm_file_then_succeeds
        +test:
            +title: test_pcl5_lowvaluenew_45page_lineterm
            +guid:48b832f3-f66c-4e22-82fe-5aa2ae0f66f6
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_lowvaluenew_45page_lineterm_file_then_succeeds(self):
        job_id = self.print.raw.start('2015dd02b31ae61c02b0ff2013400c6417e8e53cb44d7cdb1e66bab6bd267db9')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
