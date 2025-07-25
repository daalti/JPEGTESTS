import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media_handling import MediaHandling
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        cls.media_handling = MediaHandling()

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
        tear_down_output_saver(self.outputsaver)

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
        +name:TestWhenPrintingJPEGFile::test_when_using_file_example_JPG_2500kB_file_then_succeeds
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
    def test_when_using_file_example_JPG_2500kB_file_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()

        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)
        if "anycustom" in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.AnyCustom, default_tray)
        elif "na_letter_8.5x11in" in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.Letter, self.media.MediaType.Stationery)

        # Not using print_verify for a reason
        # We want to handle media mismatch alert on roll products before job completion
        job_id = self.print.raw.start('b6630f7d0ff76f53f21b472f0d383b41a0b8a730a29282f12db435dc390dfdeb')

        # This jpeg job has large dimensions
        # On non-roll products, it will print on Letter
        media_configuration = self.media.get_media_configuration().get('inputs', [])
        media_sources = [tray.get('mediaSourceId') for tray in media_configuration]

        if self.media.MediaInputIds.MainRoll in media_sources:
            # On Beam, it will print on main-roll after out of range media check clipping target size leading to a prompt
            self.media_handling.wait_for_alerts('mediaMismatchUnsupportedSize', 100)
            # Handle the prompt displayed to user to continue printing
            self.media_handling.alert_action('mediaMismatchUnsupportedSize', 'continue')
        elif self.media.MediaInputIds.Roll1 in media_sources:
            # Apply same workaround for multi-roll products, alert is mediaMismatchSizeFlow
            self.media_handling.wait_for_alerts('mediaMismatchSizeFlow', 100)
            self.media_handling.alert_action("mediaMismatchSizeFlow", "continue")

        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("Jpeg file example JPG 2500kB Page - Print job completed successfully")