import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
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
        +purpose: simple print job of jpeg file of photoimages 10 corrupt dpof a1
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_10_corrupt_DPOF_a1.jpg=150c0425c6a2ab2de1209cd09587ba4b2a8d0a0f7de0e0b7adb5a1947ae6db34
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_photoimages_10_corrupt_DPOF_a1_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_10_corrupt_dpof_a1
            +guid:de14aafa-1efb-402e-8b4e-fdccc7695564
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_10_corrupt_DPOF_a1_jpg_then_succeeds(self):

        capabilities = self.media.get_media_capabilities()
        media_width_maximum = capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = capabilities["supportedInputs"][0]["mediaLengthMinimum"]

        default_tray, media_sizes = self.media.get_source_and_media_sizes()

        if 'anycustom' in media_sizes:
            self.media.tray.configure(default_tray, 'anycustom', 'stationery')
        elif 'custom' in media_sizes and media_width_maximum >= 48611 and media_length_maximum >= 55555 and  media_width_minimum <= 48611  and media_length_minimum <= 55555:
            self.media.tray.configure(default_tray, 'custom', 'stationery')
        job_id = self.print.raw.start('150c0425c6a2ab2de1209cd09587ba4b2a8d0a0f7de0e0b7adb5a1947ae6db34')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Jpeg photoimages 10 corrupt DPOF a1 file")