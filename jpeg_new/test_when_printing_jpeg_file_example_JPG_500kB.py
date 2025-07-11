import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
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
        +purpose:Simple print job of Jpeg file of 500kB from *file_example_JPG_500kB.jpg
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:file_example_JPG_500kB.jpg=838e346997ab5f2dd6745e9e536de6f9cd68965088354597f2fba016ad40ab2c
        +name:TestWhenPrintingJPEGFile::test_when_file_example_JPG_500kB_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_file_example_JPG_500kB
            +guid:df3a34de-baa2-426a-9ced-3c26994f2de5
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_file_example_JPG_500kB_jpg_then_succeeds(self):

        job_id = self.print.raw.start('838e346997ab5f2dd6745e9e536de6f9cd68965088354597f2fba016ad40ab2c')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg file example JPG 500kB Page - Print job completed successfully")