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
    +purpose: pcl5 highvalue using 10Page_hg30gc01.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:10Page-hg30gc01.obj=9e38d25f543a21176fb91e6543f8aba6aec6dc0d4526ef0c3989cf38e2a0a4b1
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_10page_hg30gc01_file_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_10page_hg30gc01
        +guid:b1bb484b-0b80-4b80-bbaa-be0816e46b3f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_highvalue_10page_hg30gc01_file_then_succeeds(self):
            # This file create 4 jobs with total of 9 pages.
            job_id = self.print.raw.start('9e38d25f543a21176fb91e6543f8aba6aec6dc0d4526ef0c3989cf38e2a0a4b1')
            self.print.wait_for_job_completion(job_id)
            self.outputsaver.save_output()
