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

        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        default_size = self.media.get_default_size(default_tray)

        if default_size in media_sizes:
            self.media.tray.configure(default_tray, default_size, 'stationery')

        job_id = self.print.raw.start('3fd5bf0f2e753f3c417e81304a978e7264095c000a6c5f63e90500dbd2797129')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Jpeg file example photoimages 1PhotoDPOFTestforBAT hp945 Vader DCIM 100HP945 HPIM0069 - Print job completed successfully")