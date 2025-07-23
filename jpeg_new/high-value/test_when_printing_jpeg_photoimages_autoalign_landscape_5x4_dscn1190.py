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
        +purpose: simple print job of jpeg file of photoimages autoalign landscape 5x4 dscn1190
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_AutoAlign_Landscape_5x4_DSCN1190.JPG=f7cc84d7e8c40f5fe3c9c95959a2bc8e69506f260865051c9d979db0ccc5128b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_AutoAlign_Landscape_5x4_DSCN1190_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_autoalign_landscape_5x4_dscn1190
            +guid:06648c5b-1c22-4e1b-93b4-4e198aa32885
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_photoimages_AutoAlign_Landscape_5x4_DSCN1190_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=68266,
            length_max=51200,
            width_min=68266,
            length_min=51200)

        job_id = self.print.raw.start('f7cc84d7e8c40f5fe3c9c95959a2bc8e69506f260865051c9d979db0ccc5128b')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Jpeg photoimages AutoAlign Landscape 5x4 DSCN1190 file")