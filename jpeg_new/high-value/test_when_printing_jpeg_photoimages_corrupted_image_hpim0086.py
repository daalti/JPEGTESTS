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
        +purpose: simple print job of jpeg file of photoimages corrupted image hpim0086
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_Corrupted_image_HPIM0086.JPG=344788233baa04baf642da4985648ad970fbb293285be13529ac743264435ad6
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_Corrupted_image_HPIM0086_file_then_fails
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_corrupted_image_hpim0086
            +guid:715f880a-12ea-49bd-b6fd-3a6c93554f5d
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_photoimages_Corrupted_image_HPIM0086_file_then_fails(self):

        job_id = self.print.raw.start('344788233baa04baf642da4985648ad970fbb293285be13529ac743264435ad6')
        self.print.wait_for_state(job_id, ["completed"])
        self.job_history.wait_for_jobs()
        history = self.job_history.get()
        assert history[0]["completionState"] == "failed"
        self.outputsaver.save_output()

        logging.info("Jpeg photoimages Corrupted image HPIM0086 file")