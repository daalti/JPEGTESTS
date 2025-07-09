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
    +purpose:Simple print job of Jpeg file of 100kB from *file_example_JPG_100kB.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:360
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_example_JPG_100kB.jpg=88aeb1f4467bd1e50cf624de972fbf3f40801632fedb64aaa7b1a8a9ef786fc6
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_file_example_JPG_100kB_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_file_example_JPG_100kB_jpg_then_succeeds
        +guid:3a24f23b-1250-4bc9-b1c8-524ded9ff218
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_file_example_JPG_100kB_jpg_then_succeeds(self):

        self.outputsaver.validate_crc_tiff(udw)
        default = tray.get_default_source()
        media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        elif tray.is_size_supported('custom', default) and media_width_maximum > 85000 and media_length_maximum >= 110000 and media_width_minimum < 85000 and media_length_minimum <= 110000:
            tray.configure_tray(default, 'custom', 'stationery')
        elif tray.is_size_supported('na_letter_8.5x11in', default):
            tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

        self.print.raw.start('88aeb1f4467bd1e50cf624de972fbf3f40801632fedb64aaa7b1a8a9ef786fc6', timeout=360)
        self.print.wait_for_job_completion()
        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("Jpeg file example JPG 100kB Page - Print job completed successfully")
