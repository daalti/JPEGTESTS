import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

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
        +purpose:simple print job of jpeg file of photoimages differentfilesize 4m 211canon img 0002
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_differentfilesize_4M_211CANON_IMG_0002.JPG=ff074792fba217f14d2fad33955f22c5f86095d72f43e6037837701715fa21ea
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_differentfilesize_4M_211CANON_IMG_0002_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_differentfilesize_4m_211canon_img_0002
            +guid:9765359c-f1b6-4ef1-9b79-783b6ca0f840
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_photoimages_differentfilesize_4M_211CANON_IMG_0002_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=202666,
            length_max=152000,
            width_min=202666,
            length_min=152000)

        job_id = self.print.raw.start('ff074792fba217f14d2fad33955f22c5f86095d72f43e6037837701715fa21ea')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg file example photoimages differentfilesize 4M 211CANON IMG 0002 - Print job completed successfully")