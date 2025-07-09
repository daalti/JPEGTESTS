from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver
from dunetuf.localization.LocalizationHelper import LocalizationHelper

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
    +purpose:Test print multiple jobs
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-6717
    +timeout:300
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:ProductQA
    +test_framework:TUF
    +external_files:lenna_without_resolution_info_EXIF_NONE.jpg=0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_lenna_without_resolution_info_EXIF_NONE_jpg_then_succeeds
    +test:
        +title:test_when_lenna_without_resolution_info_EXIF_NONE_jpg_then_succeeds
        +guid:6c612934-63be-4c52-a5ed-df7e85fb1b02
        +dut:
            +type:Simulator, Emulator
            +configuration:DocumentFormat=JPEG & PrintEngineType=Maia

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_lenna_without_resolution_info_EXIF_NONE_jpg_then_succeeds(self):


        # Go to Job Queue App screen
        spice.cleanSystemEventAndWaitHomeScreen()
        spice.main_app.get_home()
        spice.main_app.goto_job_queue_app()

        # Send job to print
        self.print.raw.start('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')

        # Get last job in queue by CDM
        queue = job.get_job_queue()
        first_job_id = queue[-1]["jobId"]

        # Send job to print
        self.print.raw.start('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')

        # Get last job in queue by CDM
        queue = job.get_job_queue()
        second_job_id = queue[-1]["jobId"]

        # Send job to print
        self.print.raw.start('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')

        # Get last job in queue by CDM
        queue = job.get_job_queue()
        third_job_id = queue[-1]["jobId"]

        #Wait for first job completion
        self.print.wait_for_job_completion()
        spice.job_ui.goto_job(first_job_id)
        assert spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(net,"cJobStateTypeCompleted", locale)

        #Wait for second job completion
        self.print.wait_for_job_completion()
        spice.job_ui.goto_job(second_job_id)
        assert spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(net,"cJobStateTypeCompleted", locale)

        #Wait for third job completion
        self.print.wait_for_job_completion()
        spice.job_ui.goto_job(third_job_id)
        assert spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(net,"cJobStateTypeCompleted", locale)

        # Go to homescreen
        spice.goto_homescreen()
