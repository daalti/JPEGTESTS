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
        +purpose: pcl5 lowvaluenew using 2Page_fullp100.obj
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:2Page-fullp100.obj=438e71f9989037ea7ecd4e8b8e31d99463d470df605e450aa6f8bdafa83551fc
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_lowvaluenew_2page_fullp100_file_then_succeeds
        +test:
            +title: test_pcl5_lowvaluenew_2page_fullp100
            +guid:d3eddcd8-e401-4023-8b51-488e16e4be7c
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_lowvaluenew_2page_fullp100_file_then_succeeds(self):
        default = self.media.get_default_source()
        if self.media.is_size_supported('na_legal_8.5x14in', default):
            self.media.tray.configure_tray(default, 'na_legal_8.5x14in','stationery')
        job_id = self.print.raw.start('438e71f9989037ea7ecd4e8b8e31d99463d470df605e450aa6f8bdafa83551fc')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
