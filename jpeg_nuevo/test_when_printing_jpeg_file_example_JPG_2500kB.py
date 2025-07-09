import logging
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.media.media_handling import MediaHandling
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
        cls.media_handling = MediaHandling()

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

    def _update_media_input_config(self, default_tray, media_size, media_type):
        """Update media configuration for a specific tray.
        
        Args:
            default_tray: Default tray identifier
            media_size: Media size to set
            media_type: Media type to set
        """
        media_input = self.media.get_media_configuration().get('inputs', [])
        
        for input_config in media_input:
            if input_config.get('mediaSourceId') == default_tray:
                # Handle custom media size configuration
                if media_size == 'custom':
                    supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
                    capability = next(
                        (cap for cap in supported_inputs if cap.get('mediaSourceId') == default_tray),
                        {}
                    )
                    input_config['currentMediaWidth'] = capability.get('mediaWidthMaximum')
                    input_config['currentMediaLength'] = capability.get('mediaLengthMaximum')
                    input_config['currentResolution'] = capability.get('resolution')
                
                # Update media properties
                input_config['mediaSize'] = media_size
                input_config['mediaType'] = media_type
                
                # Update configuration and return early
                self.media.update_media_configuration({'inputs': [input_config]})
                return
        
        logging.warning(f"No media input found for tray: {default_tray}")

    def _get_tray_and_media_sizes(self, tray = None):
        """Get the default tray and its supported media sizes.
        
        Returns:
            tuple: (default_tray, media_sizes) where default_tray is the default source
                   and media_sizes is a list of supported media sizes for that tray
        """
        if tray is None:
            tray = self.media.get_default_source()
        supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
        media_sizes = next((input.get('supportedMediaSizes', []) for input in supported_inputs if input.get('mediaSourceId') == tray), [])
        logging.info('Supported Media Sizes (%s): %s', tray, media_sizes)
        return tray, media_sizes
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

        self.outputsaver.validate_crc_tiff()

        default = self.media.get_default_source()
        default_tray, media_sizes = self._get_tray_and_media_sizes()
        if 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', default_tray)
        elif 'na_letter_8.5x11in' in media_sizes:
            self._update_media_input_config(default_tray, 'na_letter_8.5x11in', 'stationery')

        # Not using print_verify for a reason
        # We want to handle media mismatch alert on roll products before job completion
        job_id = self.print.raw.start('b6630f7d0ff76f53f21b472f0d383b41a0b8a730a29282f12db435dc390dfdeb')

        # This jpeg job has large dimensions
        # On non-roll products, it will print on Letter
        media_configuration = self.media.get_media_configuration().get('inputs', [])
        media_soruces = [tray.get('mediaSourceId') for tray in media_configuration]

        if 'main-roll' in media_soruces:
            # On Beam, it will print on main-roll after out of range media check clipping target size leading to a prompt
            self.media_handling.wait_for_alerts('mediaMismatchUnsupportedSize', 100)
            # Handle the prompt displayed to user to continue printing
            self.media_handling.alert_action('mediaMismatchUnsupportedSize', 'continue')
        elif 'roll-1' in media_soruces:
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
