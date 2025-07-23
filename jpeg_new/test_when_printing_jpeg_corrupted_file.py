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
        +purpose: Simple Print job of Jpeg file of 1MB from **
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:DatastreamCorrupted.JPG=8569b17b86977b3f02e3c5194d6436df02662bc5724f929f007a1a4626a9f122
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_DatastreamCorrupted_then_fails
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_corrupted_file
            +guid:92595892-ed06-4f78-947d-b24e9a8c7d45
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


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_DatastreamCorrupted_then_fails(self):

        #TODO: Ares cannot run this test right now.
        job_id = self.print.raw.start('8569b17b86977b3f02e3c5194d6436df02662bc5724f929f007a1a4626a9f122')
        self.print.wait_for_state(job_id, ["completed"])
        self.job_history.wait_for_jobs()
        history = self.job_history.get()
        assert history[0]["completionState"] == "failed"
        self.outputsaver.save_output()
        self.outputsaver.clear_output()
        logging.info("Jpeg corrupted file")