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
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_lessthan3MegaPixelphoto_DSCN4744_file_then_succeeds
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
    def test_when_using_photoimages_lessthan3MegaPixelphoto_DSCN4744_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=40000,
            length_max=53333,
            width_min=40000,
            length_min=53333)

        job_id = self.print.raw.start('6666d5ccbf4fb13317b183faa35e96f7050b1e29f6161cfd28050accebf64e17')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Jpeg photoimages_lessthan3MegaPixelphoto_DSCN4744 file")