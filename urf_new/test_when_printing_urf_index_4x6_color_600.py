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
        +purpose:Simple print job of Urf Index 4x6 Color 600 from *Index_4x6_Color_600.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Index_4x6_Color_600.urf=c854b57aa379fe8f9cfaddda4515b9c38075507d0ea795620b824db667b7e60d
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_index_4x6_color_600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_index_4x6_color_600_page
            +guid:3dc1ef25-1248-4fbd-ba00-8f88c696ea52
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-4x6_4x6in
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_index_4x6_color_600_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('na_index-4x6_4x6in', default):
            self.media.tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('c854b57aa379fe8f9cfaddda4515b9c38075507d0ea795620b824db667b7e60d')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
    
        logging.info("URF Index 4x6 Color 600 Page - Print job completed successfully")
