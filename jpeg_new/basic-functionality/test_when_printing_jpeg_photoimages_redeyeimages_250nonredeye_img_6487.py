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
        +purpose:simple print job of jpeg file of photoimages redeyeimages 250nonredeye img 6487
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_Redeyeimages_250Nonredeye_IMG_6487.JPG=1497ed339f914418a8fb1329a1117c3668266884fbef99901ec6dcfaa73631de
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_photoimages_Redeyeimages_250Nonredeye_IMG_6487_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_redeyeimages_250nonredeye_img_6487
            +guid:6032cca8-110a-4b57-9ff8-2df671d1518d
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_photoimages_Redeyeimages_250Nonredeye_IMG_6487_file_then_succeeds(self):

        job_id = self.print.raw.start('1497ed339f914418a8fb1329a1117c3668266884fbef99901ec6dcfaa73631de')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg file example photoimages Redeyeimages 250Nonredeye IMG 6487 - Print job completed successfully")