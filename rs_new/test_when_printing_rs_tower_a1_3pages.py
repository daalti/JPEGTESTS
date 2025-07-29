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
        +purpose:A3 rasterstream multiple pages (.rs) file print
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-14986
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:tower_a1_3pages.rs=ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_tower_a1_3pages_file_then_succeeds
        +test:
            +title:test_rs_tower_a1_3pages
            +guid:65b98f83-139e-4826-9362-c3ce717b3ffa
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=RasterStreamICF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_tower_a1_3pages_file_then_succeeds(self):
        job_id = self.print.raw.start('ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
