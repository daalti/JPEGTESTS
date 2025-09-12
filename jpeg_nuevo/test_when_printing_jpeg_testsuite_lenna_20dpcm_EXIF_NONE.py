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

    def _get_tray_and_media_sizes(self):
        """Get the default tray and its supported media sizes."""
        default_tray = self.media.get_default_source()
        supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
        media_sizes = next((inp.get('supportedMediaSizes', []) for inp in supported_inputs if inp.get('mediaSourceId') == default_tray), [])
        logging.info('Supported Media Sizes (%s): %s', default_tray, media_sizes)
        return default_tray, media_sizes
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna 20dpcm EXIF NONE Page from *lenna_20dpcm_EXIF_NONE.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:200
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_20dpcm_EXIF_NONE.jpg=cb6e516bebfbd46c2e719ebb1bb3c7f4d49cefb80977a40cc167073712f7ba24
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_lenna_20dpcm_EXIF_NONE_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_20dpcm_EXIF_NONE
        +guid:394c3a98-5cbf-411b-a464-572970c2a347
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_lenna_20dpcm_EXIF_NONE_jpg_then_succeeds(self):

        default_tray, media_sizes = self._get_tray_and_media_sizes()
        default_size = self.media.get_default_size(default_tray)

        if default_size in media_sizes:
            logging.info(f"Set paper tray <{default_tray}> to paper size <{default_size}>")
            self._update_media_input_config(default_tray, default_size, 'stationery')

        job_id = self.print.raw.start('cb6e516bebfbd46c2e719ebb1bb3c7f4d49cefb80977a40cc167073712f7ba24', timeout=180)
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("JPEG TestSuite lenna 20dpcm EXIF NONE Page - Print job completed successfully")
