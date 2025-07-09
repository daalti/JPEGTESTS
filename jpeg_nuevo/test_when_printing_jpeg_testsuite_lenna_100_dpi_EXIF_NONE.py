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
    +purpose:Simple print job of Jpeg TestSuite lenna 100 dpi EXIF NONE Page from *lenna_100_dpi_EXIF_NONE.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_100_dpi_EXIF_NONE.jpg=cc7efdcc505cf95c913aeafa9886ad5a4f2c31b4afefd35d9c9f5fd60f4368d3
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_lenna_100_dpi_EXIF_NONE_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_lenna_100_dpi_EXIF_NONE_jpg_then_succeeds
        +guid:c4b3457d-fff3-4988-83be-663dc9fc7610
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_lenna_100_dpi_EXIF_NONE_jpg_then_succeeds(self):

        self.outputsaver.validate_crc_tiff(udw)
        default = tray.get_default_source()
        default_size = tray.get_default_size(default)

        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, "anycustom", 'stationery')

        else:
            tray.configure_tray(default, 'custom', 'stationery')

        self.print.raw.start('cc7efdcc505cf95c913aeafa9886ad5a4f2c31b4afefd35d9c9f5fd60f4368d3', timeout=180)
        self.print.wait_for_job_completion()
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("JPEG TestSuite lenna 100 dpi EXIF NONE Page - Print job completed successfully")
