import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from jpeg_nuevo.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.outputsaver = OutputSaver()

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
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite DemoImages Page from *DemoImages.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DemoImages.jpg=3c685134a542d477374788bb6a3f1027cd8f433d49a0255b2ac7f5246bd7010c
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_DemoImages_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_DemoImages
        +guid:ecff61d6-4ef3-4aa7-892b-aafdcc79474b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_DemoImages_jpg_then_succeeds(self):

        job_id = self.print.raw.start('3c685134a542d477374788bb6a3f1027cd8f433d49a0255b2ac7f5246bd7010c')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("JPEG TestSuite DemoImages Page - Print job completed successfully")