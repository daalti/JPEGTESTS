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
    +purpose: simple print job of jpeg file of photoimages_panoramaimages_hpr927_5m_3
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_panoramaimages_HPR927_5M_3.JPG=e3e510bc084382297091821906875e620bc5bb1aa6f520e8b40ca86c699eb2e2
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_panoramaimages_HPR927_5M_3_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_panoramaimages_hpr927_5m_3
        +guid:07a319be-cfb0-44ab-ac0b-959946969215
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_panoramaimages_HPR927_5M_3_JPG_then_succeeds(self):


        job_id = self.print.raw.start('e3e510bc084382297091821906875e620bc5bb1aa6f520e8b40ca86c699eb2e2')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg photoimages_panoramaimages_HPR927_5M_3 file")