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
    +purpose: simple print job of jpeg file of photoimages resolution jpg jpg1760x1168
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_resolution_jpg_jpg1760x1168.JPG=bfd5bb0ee2970dbf4280705c8d15cc4c9d839d0ece7f87cb8fffe38fe0fc5c79
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_resolution_jpg_jpg1760x1168_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_resolution_jpg_jpg1760x1168
        +guid:1928246c-40e1-4b93-8bd2-554815719a77
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=custom

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    #TODO: UPDATE THE TEST
    def test_when_photoimages_resolution_jpg_jpg1760x1168_JPG_then_succeeds(self):

        self.outputsaver.operation_mode('TIFF')
        self.media.get_media_capabilities()
        selected_media_source = ''
        for tray_capabilities in self.media.get_media_capabilities()["supportedInputs"]:
            selected_media_source = tray_capabilities['mediaSourceId']
            if tray.is_media_combination_supported(selected_media_source, "custom", "stationery"):
                if tray_capabilities['mediaWidthMinimum'] <= 233000 and tray_capabilities['mediaWidthMaximum'] >= 233000 and tray_capabilities['mediaLengthMinimum'] <= 155000 and tray_capabilities['mediaLengthMaximum'] >= 155000:
                    tray.configure_tray(selected_media_source, "custom", 'stationery',width=233000, length=155000)
                    logging.info(f"media source {selected_media_source} selected")
                    break
                else:
                    logging.info(f"media source {selected_media_source} does not support the required media size")
                    selected_media_source = ''
            else:
                logging.info(f"media source {selected_media_source} not supported")
                selected_media_source = ''

        if selected_media_source == '':
            logging.info("No custom tray found")
            return

        job_id = self.print.raw.start('bfd5bb0ee2970dbf4280705c8d15cc4c9d839d0ece7f87cb8fffe38fe0fc5c79')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')

        logging.info("Jpeg photoimages resolution jpg jpg1760x1168 file")
