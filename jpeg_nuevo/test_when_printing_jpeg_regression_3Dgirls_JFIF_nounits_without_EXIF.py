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
    +purpose:Simple print job of Jpeg Regression of 3Dgirls JFIF nounits without EXIF Page from *3Dgirls_JFIF_nounits_without_EXIF.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:3Dgirls_JFIF_nounits_without_EXIF.jpg=07010aa839653b2355047c770f6f3631997e0e9172537141d42d185c34f39a1d
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_3Dgirls_JFIF_nounits_without_EXIF_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_3Dgirls_JFIF_nounits_without_EXIF
        +guid:447e6d61-9e0a-4ba8-b036-6fa67b57d011
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_3Dgirls_JFIF_nounits_without_EXIF_jpg_then_succeeds(self):

        job_id = self.print.raw.start('07010aa839653b2355047c770f6f3631997e0e9172537141d42d185c34f39a1d')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("JPEG Regression 3Dgirls JFIF nounits without EXIF Page - Print job completed successfully")