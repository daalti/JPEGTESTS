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
        +purpose: simple print job of jpeg file of photoimages_exif2.3_exif2.3_dsci0013
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_Exif2.3_Exif2.3_DSCI0013.JPG=d1792461f8ef786f54d0bca2872e939d679f59bf169dd0a66ebbeb1a53ac289a
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_Exif2_3_Exif2_3_DSCI0013_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_exif2_3_exif2_3_dsci0013
            +guid:6931fbe7-1be5-45f8-9bd1-caddc7dd37b1
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_photoimages_Exif2_3_Exif2_3_DSCI0013_file_then_succeeds(self):

        self.load_custom_tray(
            width_max=480000,
            length_max=360000,
            width_min=480000,
            length_min=360000
        )

        job_id = self.print.raw.start('d1792461f8ef786f54d0bca2872e939d679f59bf169dd0a66ebbeb1a53ac289a')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg photoimages_Exif2.3_Exif2.3_DSCI0013 file")