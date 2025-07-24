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
        +purpose: pcl5 basicfunctionality using 41Page_raster4.obj
        +test_tier: 1
        +is_manual:False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:320
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:41Page-raster4.obj=a9ebe3501d00fc02d9d6fdfe3b8c657263fcfec02bfc75e0f20e47dc138e743c
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_basicfunctionality_41page_raster4_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pcl5_basicfunctionality_41page_raster4
            +guid:a47947df-3eb1-4bf6-91da-7cba0a78f73c
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5
        
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_basicfunctionality_41page_raster4_file_then_succeeds(self):
        job_id = self.print.raw.start('a9ebe3501d00fc02d9d6fdfe3b8c657263fcfec02bfc75e0f20e47dc138e743c')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
