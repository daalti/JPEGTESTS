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
        """Update media configuration for a specific tray."""
        media_input = self.media.get_media_configuration().get('inputs', [])

        for input_config in media_input:
            if input_config.get('mediaSourceId') == default_tray:
                if media_size == 'custom':
                    supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
                    capability = next(
                        (cap for cap in supported_inputs if cap.get('mediaSourceId') == default_tray),
                        {}
                    )
                    input_config['currentMediaWidth'] = capability.get('mediaWidthMaximum')
                    input_config['currentMediaLength'] = capability.get('mediaLengthMaximum')
                    input_config['currentResolution'] = capability.get('resolution')

                input_config['mediaSize'] = media_size
                input_config['mediaType'] = media_type

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
    +purpose:Simple print job of jpeg_sRGB_A4_600dpi
    +test_tier:1
    +is_manual:True
    +reqid:DUNE-18107
    +timeout:300
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:sRGB_A4_600dpi.jpg=86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_sRGB_A4_600dpi_jpg_then_succeeds
    +test:
        +title:test_jpeg_sRGB_A4_600dpi
        +guid:07072c6f-336c-488b-82bd-c1053f546e91
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_sRGB_A4_600dpi_jpg_then_succeeds(self):

        self.outputsaver.operation_mode('TIFF')

        default_tray, media_sizes = self._get_tray_and_media_sizes()

        if 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', 'stationery')

        else:
            self._update_media_input_config(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')

        logging.info("Jpeg sRGB_A4_600dpi- Print job completed successfully")
