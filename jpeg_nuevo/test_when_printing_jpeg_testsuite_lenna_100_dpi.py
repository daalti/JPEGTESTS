import pytest
import logging
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver


class TestWhenPrintingJPEGFile:
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()
        cls.media = Media()
        cls.outputsaver = OutputSaver()

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def setup_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Get media configuration
        self.default_configuration = self.media.get_media_configuration()

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
    +purpose:Simple print job of Jpeg TestSuite lenna 100 dpi Page from *lenna_100_dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:300
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_100_dpi.jpg=7a2e13bafa3b09a94ae8a5c92592c36f3104d8eb862dd121f505fd11262fc242
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_lenna_100_dpi_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_100_dpi
        +guid:bf4b00c1-2d94-4a9d-b290-5cf503901b45
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_lenna_100_dpi_jpg_then_succeeds(self):

        self.outputsaver.operation_mode('TIFF')

        default = tray.get_default_source()
        default_size = tray.get_default_size(default)

        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, "anycustom", 'stationery')

        else:
            tray.configure_tray(default, 'custom', 'stationery')

        job_id = self.print.raw.start('7a2e13bafa3b09a94ae8a5c92592c36f3104d8eb862dd121f505fd11262fc242', timeout=300)
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')

        logging.info("JPEG TestSuite lenna 100 dpi Page - Print job completed successfully")
