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
        +purpose:HPGL2 basic functionality test using **sc4-cmyk.plt
        +test_tier:1
        +is_manual:False
        +reqid:Dune-45716
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:sc4-cmyk.plt=4018acd649646fb0f86395f7b24be029f8e68edb5ea569026744e99158449248
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_hpgl2_basic_functionality_sc4_cmyk_file_then_succeeds
        +test:
            +title:test_hpgl2_basic_functionality_sc4_cmyk
            +guid:c01acbbc-df0c-4f30-83ff-9c41fdc4fdeb
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=HPGL2
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_hpgl2_basic_functionality_sc4_cmyk_file_then_succeeds(self):
        job_id = self.print.raw.start('4018acd649646fb0f86395f7b24be029f8e68edb5ea569026744e99158449248')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("sc4-cmyk Page - Print job completed successfully")
