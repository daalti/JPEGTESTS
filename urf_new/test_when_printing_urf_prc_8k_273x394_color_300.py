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
        +purpose:Simple print job of Urf Prc 8k 273x394 Color 300 Page from *Prc_8k_273x394_Color_300.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Prc_8k_273x394_Color_300.urf=ec7d87c728ddf6f9ca94c420362888e2e53c979220ce1d09b0166c63aa0d0f62
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_prc_8k_273x394_color_300_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_prc_8k_273x394_color_300_page
            +guid:5a3ce60e-a738-4807-8c17-2bd0f024e851
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_prc_8k_273x394_color_300_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('roc_8k_10.75x15.5in', default):
            self.media.tray.configure_tray(default, 'roc_8k_10.75x15.5in', 'stationery')
        elif self.media.tray.is_size_supported('custom', default) and self.media.tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"] >= 150000:
            # the size of print file should in max/min custom size of printer supported, then could set custom size
            self.media.tray.configure_tray(default, "custom", 'stationery')
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('ec7d87c728ddf6f9ca94c420362888e2e53c979220ce1d09b0166c63aa0d0f62')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
    
        logging.info("URF Prc 8k 273x394 Color 300 Page - Print job completed successfully")
