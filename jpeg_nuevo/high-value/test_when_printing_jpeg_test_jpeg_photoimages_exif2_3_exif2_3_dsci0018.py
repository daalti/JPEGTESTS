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
    +purpose: simple print job of jpeg file of photoimages_exif2.3_exif2.3_dsci0018
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_Exif2.3_Exif2.3_DSCI0018.JPG=72f5dce85ec7f14f1e021c90fb981da4ee517bd9cc3d32f9855d409a75747b07
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_Exif2_3_Exif2_3_DSCI0018_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_exif2_3_exif2_3_dsci0018
        +guid:86003821-0b0c-4834-9314-3154674fafce
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_Exif2_3_Exif2_3_DSCI0018_JPG_then_succeeds(self):

        capabilities = self.media.get_media_capabilities()
        media_width_maximum = capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = capabilities["supportedInputs"][0]["mediaLengthMinimum"]

        default_tray, media_sizes = self._get_tray_and_media_sizes()

        if 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', 'stationery')
        elif 'custom' in media_sizes and media_width_maximum >= 480000 and media_length_maximum >= 360000 and  media_width_minimum <= 480000 and media_length_minimum <= 360000:
            self._update_media_input_config(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('72f5dce85ec7f14f1e021c90fb981da4ee517bd9cc3d32f9855d409a75747b07')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg photoimages_Exif2.3_Exif2.3_DSCI0018 file")
