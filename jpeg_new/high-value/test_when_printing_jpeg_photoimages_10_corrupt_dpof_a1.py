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
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_10_corrupt_DPOF_a1_file_then_succeeds
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
    def test_when_using_photoimages_10_corrupt_DPOF_a1_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=48611,
            length_max=55555,
            width_min=48611,
            length_min=55555
        )
        job_id = self.print.raw.start('150c0425c6a2ab2de1209cd09587ba4b2a8d0a0f7de0e0b7adb5a1947ae6db34')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Jpeg photoimages 10 corrupt DPOF a1 file")