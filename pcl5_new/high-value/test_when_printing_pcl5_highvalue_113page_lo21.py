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
    +purpose: pcl5 highvalue using 113Page_lo21.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:113Page-lo21.obj=9ae0a6055af4d69fabfcd671fb62056e1c7bd7c88f9569e8216e5c80d57fd803
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_113page_lo21_file_then_succeeds
    +test:
        +title: test_pcl5_highvalue_113page_lo21
        +guid:d59eb54b-df76-461c-8ee7-f026a80855b6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_highvalue_113page_lo21_file_then_succeeds(self):
            job_id = self.print.raw.start('9ae0a6055af4d69fabfcd671fb62056e1c7bd7c88f9569e8216e5c80d57fd803')
            self.print.wait_for_job_completion(job_id)
            self.outputsaver.save_output()
