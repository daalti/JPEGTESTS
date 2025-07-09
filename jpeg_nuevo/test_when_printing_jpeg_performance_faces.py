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
    +purpose:Simple print job of Jpeg Performance faces Page from *faces.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:faces.jpg=d625c95d10545cc5aa1e4ce2f276a7d423c1aa96a683a581a4bc243ee93393a2
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_faces_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_performance_faces
        +guid:7fe748d6-cbf8-41e4-b0d6-06cd98031b60
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_faces_jpg_then_succeeds(self):

        job_id = self.print.raw.start('d625c95d10545cc5aa1e4ce2f276a7d423c1aa96a683a581a4bc243ee93393a2')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("JPEG Performance faces Page - Print job completed successfully")