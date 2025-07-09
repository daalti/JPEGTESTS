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
    +purpose: simple print job of jpeg file of photoimages autoalign landscape 5x4 dscn1190
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_AutoAlign_Landscape_5x4_DSCN1190.JPG=f7cc84d7e8c40f5fe3c9c95959a2bc8e69506f260865051c9d979db0ccc5128b
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_AutoAlign_Landscape_5x4_DSCN1190_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_photoimages_AutoAlign_Landscape_5x4_DSCN1190_JPG_then_succeeds
        +guid:06648c5b-1c22-4e1b-93b4-4e198aa32885
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_AutoAlign_Landscape_5x4_DSCN1190_JPG_then_succeeds(self):

        default = tray.get_default_source()

        media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        elif tray.is_size_supported('custom', default) and media_width_maximum >= 68266 and media_length_maximum >= 51200 and  media_width_minimum <= 68266  and media_length_minimum <= 51200:
            tray.configure_tray(default, 'custom', 'stationery')
        self.print.raw.start('f7cc84d7e8c40f5fe3c9c95959a2bc8e69506f260865051c9d979db0ccc5128b')
        self.print.wait_for_job_completion()
        self.outputsaver.save_output()
        logging.info("Jpeg photoimages AutoAlign Landscape 5x4 DSCN1190 file")
