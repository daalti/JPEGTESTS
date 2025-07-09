import logging
from dunetuf.print.output_saver import OutputSaver
from jpeg_nuevo.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.outputsaver = OutputSaver()

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

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages_lessthan3megapixelphoto_dscn4744
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_lessthan3MegaPixelphoto_DSCN4744.JPG=6666d5ccbf4fb13317b183faa35e96f7050b1e29f6161cfd28050accebf64e17
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_lessthan3MegaPixelphoto_DSCN4744_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_lessthan3megapixelphoto_dscn4744
        +guid:d00203e7-7a10-4578-8681-6c3b9c5cd61f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_lessthan3MegaPixelphoto_DSCN4744_JPG_then_succeeds(self):

        capabilities = self.media.get_media_capabilities()
        media_width_maximum = capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = capabilities["supportedInputs"][0]["mediaLengthMinimum"]

        default_tray, media_sizes = self._get_tray_and_media_sizes()

        if 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', 'stationery')
        elif 'custom' in media_sizes and media_width_maximum >= 40000 and media_length_maximum >= 53333 and  media_width_minimum <= 40000  and media_length_minimum <= 53333:
            self._update_media_input_config(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('6666d5ccbf4fb13317b183faa35e96f7050b1e29f6161cfd28050accebf64e17')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()        logging.info("Jpeg photoimages_lessthan3MegaPixelphoto_DSCN4744 file")
