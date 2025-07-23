from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.spice import Spice
from dunetuf.metadata import get_qmltest_port, get_screen_capture, get_ip
from dunetuf.network.net import Network
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        port = get_qmltest_port()
        screen_capture = get_screen_capture()
        cls.ip_address = get_ip()
        cls.spice = Spice(cls.ip_address, port, screen_capture)
        cls.net = Network(cls.ip_address)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def teardown_method(self):
        """Clean up resources after each test."""
        self.spice.cleanSystemEventAndWaitHomeScreen()
        self.spice.wait_ready()
        self.spice.goto_homescreen()

        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Reset media configuration to default
        self.media.update_media_configuration(self.default_configuration)
        tear_down_output_saver(self.outputsaver)
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
        +name:TestWhenPrintingJPEGFile::test_when_using_using_lenna_without_resolution_info_EXIF_NONE_file_then_succeeds
        +test:
            +title:test_jpeg_print_multiple_jobs
            +guid:6c612934-63be-4c52-a5ed-df7e85fb1b02
            +dut:
                +type:Simulator, Emulator
                +configuration:DocumentFormat=JPEG & PrintEngineType=Maia

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_using_lenna_without_resolution_info_EXIF_NONE_file_then_succeeds(self):


        # Go to Job Queue App screen
        self.spice.cleanSystemEventAndWaitHomeScreen()
        self.spice.main_app.get_home()
        self.spice.main_app.goto_job_queue_app()

        # Send job to print
        job_id_1 = self.print.raw.start('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')

        # Send job to print
        job_id_2 = self.print.raw.start('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')

        # Send job to print
        job_id_3 = self.print.raw.start('0bfd0d031132cc8326b33ae0aaeff9df4d1fe2ddcf42c208c2842a80ae922c19')

        #Wait for first job completion
        self.print.wait_for_job_completion(job_id_1)
        self.spice.job_ui.goto_job(job_id_1)
        assert self.spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(self.net,"cJobStateTypeCompleted", "en")

        #Wait for second job completion
        self.print.wait_for_job_completion(job_id_2)
        self.spice.job_ui.goto_job(job_id_2)
        assert self.spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(self.net,"cJobStateTypeCompleted", "en")

        #Wait for third job completion
        self.print.wait_for_job_completion(job_id_3)
        self.spice.job_ui.goto_job(job_id_3)
        assert self.spice.job_ui.recover_job_status() == LocalizationHelper.get_string_translation(self.net,"cJobStateTypeCompleted", "en")