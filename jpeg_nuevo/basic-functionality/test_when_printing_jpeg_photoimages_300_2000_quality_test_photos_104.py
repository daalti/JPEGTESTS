import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from jpeg_nuevo.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
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
    +purpose:simple print job of jpeg file of photoimages 300 2000 quality test photos 104
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_300_2000_Quality_Test_Photos_104.jpg=f98149047349fc2c16b7702ddf9f624a6094f335ad113a699e3dd88bc85c41f8
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_300_2000_Quality_Test_Photos_104_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_300_2000_quality_test_photos_104
        +guid:dd1412b8-ebc6-4723-8232-15f103b431c2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_300_2000_Quality_Test_Photos_104_jpg_then_succeeds(self):

        job_id = self.print.raw.start('f98149047349fc2c16b7702ddf9f624a6094f335ad113a699e3dd88bc85c41f8')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg file example photoimages 300 2000 Quality Test Photos 104 - Print job completed successfully")