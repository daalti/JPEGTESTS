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
        +purpose:URF test using **JISB4_Mono.urf
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-18912
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:JISB4_Mono.urf=c11e8d325bb4e020402ab593f6a15119f332daa6a7c6155d0f6ec7f0b6102ba6
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_jisb4_mono_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_jisb4_mono
            +guid:646b7a7f-7d47-4a7d-ad9d-06aa2101bd69
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_jisb4_mono_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
    
        if self.media.tray.is_size_supported('jis_b4_257x364mm', default):
            self.media.tray.configure_tray(default, 'jis_b4_257x364mm', 'stationery')
        
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('c11e8d325bb4e020402ab593f6a15119f332daa6a7c6155d0f6ec7f0b6102ba6')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
