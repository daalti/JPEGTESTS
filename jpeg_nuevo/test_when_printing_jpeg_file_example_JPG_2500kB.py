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
    +purpose:Simple print job of Jpeg file of 2500kB from *file_example_JPG_2500kB.jpg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-17136
    +timeout:600
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_example_JPG_2500kB.jpg=b6630f7d0ff76f53f21b472f0d383b41a0b8a730a29282f12db435dc390dfdeb
    +name:TestWhenPrintingJPEGFile::test_when_file_example_JPG_2500kB_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_file_example_JPG_2500kB
        +guid:d170eef9-e35e-4423-8741-bad5d43dc363
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_file_example_JPG_2500kB_jpg_then_succeeds(self):

        self.outputsaver.validate_crc_tiff(udw)

        default = tray.get_default_source()
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        elif tray.is_size_supported('na_letter_8.5x11in', default):
            tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

        # Not using print_verify for a reason
        # We want to handle media mismatch alert on roll products before job completion
        jobid = job_id = self.print.raw.start('b6630f7d0ff76f53f21b472f0d383b41a0b8a730a29282f12db435dc390dfdeb')

        # This jpeg job has large dimensions
        # On non-roll products, it will print on Letter
        if 'main-roll' in tray.trays:
            # On Beam, it will print on main-roll after out of range media check clipping target size leading to a prompt
            media.wait_for_alerts('mediaMismatchUnsupportedSize', 100)
            # Handle the prompt displayed to user to continue printing
            media.alert_action('mediaMismatchUnsupportedSize', 'continue')
        elif 'roll-1' in tray.trays:
            # Apply same workaround for multi-roll products, alert is mediaMismatchSizeFlow
            media.wait_for_alerts('mediaMismatchSizeFlow', 100)
            media.alert_action("mediaMismatchSizeFlow", "continue")


        jobstate = printjob.wait_verify_job_completion(jobid, timeout=600)

        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("Jpeg file example JPG 2500kB Page - Print job completed successfully")
