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
        +purpose: simple print job of jpeg file of cr222024_photo
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:CR222024_photo.JPG=4491f594e123d85879be3d23a3b8d8c94eee91510d5cdc3e25bf882309110211
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_CR222024_photo_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_cr222024_photo
            +guid:2eb64f85-8796-4a5b-857d-eeb079942bc4
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_CR222024_photo_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=80000,
            length_max=110000,
            width_min=80000,
            length_min=110000)

        job_id = self.print.raw.start('4491f594e123d85879be3d23a3b8d8c94eee91510d5cdc3e25bf882309110211')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Jpeg CR222024_photo")