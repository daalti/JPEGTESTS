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
    +purpose: simple print job of jpeg file of photoimages_panoramaimages_hpr837_1m-2m_sr016231
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:240
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_panoramaimages_HPR837_1M-2M_SR016231.JPG=0f014240fbd5c018fc18aaf6ed0c8c1d0bc3adfb0a046db1a661008df3a6dccb
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_panoramaimages_HPR837_1M_2M_SR016231_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_photoimages_panoramaimages_HPR837_1M_2M_SR016231_JPG_then_succeeds
        +guid:4990a66c-375e-4e2a-b6f1-5b1f7d6edf4f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_panoramaimages_HPR837_1M_2M_SR016231_JPG_then_succeeds(self):


        default = tray.get_default_source()
        media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        elif tray.is_size_supported('custom', default) and media_width_maximum >= 41066  and media_length_maximum >= 91200 and  media_width_minimum <= 41066  and media_length_minimum <= 91200:
            tray.configure_tray(default, 'custom', 'stationery')
        jobid = self.print.raw.start('0f014240fbd5c018fc18aaf6ed0c8c1d0bc3adfb0a046db1a661008df3a6dccb')

        # Handle media size mismatch alert
        try:
            media.wait_for_alerts('mediaMismatchSizeFlow', timeout=30)
            media.alert_action("mediaMismatchSizeFlow", "continue")
        except:
            logging.info("No mismatch alert, job printing")

        printjob.wait_verify_job_completion(jobid, 'SUCCESS', 120)
        logging.info('Print job completed with expected job status!')

        self.outputsaver.save_output()

        logging.info("Jpeg photoimages_panoramaimages_HPR837_1M-2M_SR016231 file")
