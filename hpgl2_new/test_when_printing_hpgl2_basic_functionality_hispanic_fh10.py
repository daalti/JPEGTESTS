import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
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
        +purpose:HPGL2 basic functionality test using **hispanic_fh10.hpg
        +test_tier:1
        +is_manual:False
        +reqid:Dune-45716   
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:hispanic_fh10.hpg=f43706cd4d4c6cee399c0830f348a06d806ea378b22028321c4384dd0166ad96
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_hpgl2_basic_functionality_hispanic_fh10_file_then_succeeds
        +test:
            +title:test_hpgl2_basic_functionality_hispanic_fh10
            +guid:1942fae5-8c81-4a5d-9c4e-4ce5b4eab571
            +dut:
                +type:Simulator,Emulator,Engine
                +configuration: DocumentFormat=HPGL2
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_hpgl2_basic_functionality_hispanic_fh10_file_then_succeeds(self):
        job_id = self.print.raw.start('f43706cd4d4c6cee399c0830f348a06d806ea378b22028321c4384dd0166ad96')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("hispanic_fh10 Page - Print job completed successfully")
