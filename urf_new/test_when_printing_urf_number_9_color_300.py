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
        +purpose:Simple print job of Urf Number-9 Color 300 Page from *Number_9_Color_300.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Number_9_Color_300.urf=172c7648223464af65a2f763b13603a4c2f22ecd066552e80fe23aef66cc6d29
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_number_9_color_300_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_number_9_color_300_page
            +guid:844d3ebc-0ed7-4df8-91f6-42927bcd85e1
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-9_3.875x8.875in &  MediaInputInstalled=Tray3
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_number_9_color_300_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('anycustom', default):
            self.media.tray.configure_tray(default, 'anycustom', 'stationery')
        else:
            self.media.tray.configure_tray(default, 'custom', 'stationery')
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('172c7648223464af65a2f763b13603a4c2f22ecd066552e80fe23aef66cc6d29')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
    
        logging.info("URF Number_9 Color 300 Page - Print job completed successfully")
