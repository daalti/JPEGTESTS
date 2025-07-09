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

    def _get_default_tray_and_media_sizes(self):
        """Get the default tray and its supported media sizes."""
        default_tray = self.media.get_default_source()
        supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
        media_sizes = next((inp.get('supportedMediaSizes', []) for inp in supported_inputs if inp.get('mediaSourceId') == default_tray), [])
        logging.info('Supported Media Sizes (%s): %s', default_tray, media_sizes)
        return default_tray, media_sizes
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages 1photodpoftestforbat hp945 vader dcim 100hp945 hpim0069
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_1PhotoDPOFTestforBAT_hp945_Vader_DCIM_100HP945_HPIM0069.JPG=3fd5bf0f2e753f3c417e81304a978e7264095c000a6c5f63e90500dbd2797129
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_1PhotoDPOFTestforBAT_hp945_Vader_DCIM_100HP945_HPIM0069_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_fitest_jpeg_photoimages_1photodpoftestforbat_hp945_vader_dcim_100hp945_hpim0069le_example_jpg_100kb
        +guid:3c5f241f-09aa-487b-b573-5259331cd0f9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_1PhotoDPOFTestforBAT_hp945_Vader_DCIM_100HP945_HPIM0069_JPG_then_succeeds(self):

        default_tray, media_sizes = self._get_default_tray_and_media_sizes()
        default_size = self.media.get_default_size(default_tray)

        if default_size in media_sizes:
            self._update_media_input_config(default_tray, default_size, 'stationery')

        job_id = self.print.raw.start('3fd5bf0f2e753f3c417e81304a978e7264095c000a6c5f63e90500dbd2797129')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Jpeg file example photoimages 1PhotoDPOFTestforBAT hp945 Vader DCIM 100HP945 HPIM0069 - Print job completed successfully")
