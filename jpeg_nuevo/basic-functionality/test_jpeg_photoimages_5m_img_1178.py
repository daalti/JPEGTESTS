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
    +purpose:simple print job of jpeg file of photoimages 5m img 1178
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_5M_IMG_1178.JPG=4c293c1631eab79a47d9f31a40f4b9792141a94487d7d2d58f373e58cf128595
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_5M_IMG_1178_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_photoimages_5M_IMG_1178_JPG_then_succeeds
        +guid:4c05e38f-c163-4664-84a7-b588c54c0569
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_5M_IMG_1178_JPG_then_succeeds(self):

        default = tray.get_default_source()
        media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        elif tray.is_size_supported('custom', default) and media_width_maximum >= 170666 and media_length_maximum >= 113777 and  media_width_minimum <= 170666 and media_length_minimum <= 113777:
            tray.configure_tray(default, 'custom', 'stationery')

        self.print.raw.start('4c293c1631eab79a47d9f31a40f4b9792141a94487d7d2d58f373e58cf128595', timeout=300)
        self.print.wait_for_job_completion()
        self.outputsaver.save_output()

        logging.info("Jpeg file example photoimages 5M IMG 1178 - Print job completed successfully")
