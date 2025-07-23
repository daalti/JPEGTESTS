import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.media.media_handling import MediaHandling
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
        +purpose: simple print job of jpeg file of photoimages_panoramaimages_hpr837_1m-2m_sr016231
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:240
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_panoramaimages_HPR837_1M-2M_SR016231.JPG=0f014240fbd5c018fc18aaf6ed0c8c1d0bc3adfb0a046db1a661008df3a6dccb
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_panoramaimages_HPR837_1M_2M_SR016231_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_panoramaimages_hpr837_1m_2m_sr016231
            +guid:4990a66c-375e-4e2a-b6f1-5b1f7d6edf4f
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_photoimages_panoramaimages_HPR837_1M_2M_SR016231_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=41066,
            length_max=91200,
            width_min=41066,
            length_min=91200)

        job_id = self.print.raw.start('0f014240fbd5c018fc18aaf6ed0c8c1d0bc3adfb0a046db1a661008df3a6dccb')

        # Handle media size mismatch alert
        try:
            self.media_handling.wait_for_alerts('mediaMismatchSizeFlow', timeout=30)
            self.media_handling.alert_action("mediaMismatchSizeFlow", "continue")
        except:
            logging.info("No mismatch alert, job printing")

        self.print.wait_for_job_completion(job_id)
        logging.info('Print job completed with expected job status!')

        self.outputsaver.save_output()

        logging.info("Jpeg photoimages_panoramaimages_HPR837_1M-2M_SR016231 file")