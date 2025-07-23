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
        +purpose: simple print job of jpeg file of photoimages_exif2.3_exif2.3_dsci0018
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_Exif2.3_Exif2.3_DSCI0018.JPG=72f5dce85ec7f14f1e021c90fb981da4ee517bd9cc3d32f9855d409a75747b07
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_Exif2_3_Exif2_3_DSCI0018_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_exif2_3_exif2_3_dsci0018
            +guid:86003821-0b0c-4834-9314-3154674fafce
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_photoimages_Exif2_3_Exif2_3_DSCI0018_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=480000,
            length_max=360000,
            width_min=480000,
            length_min=360000
        )

        job_id = self.print.raw.start('72f5dce85ec7f14f1e021c90fb981da4ee517bd9cc3d32f9855d409a75747b07')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg photoimages_Exif2.3_Exif2.3_DSCI0018 file")