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
        +purpose:Simple print job of Urf Oufuku Color 300 Page from *Oufuku_Color_300.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:240
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Oufuku_Color_300.urf=f744f31f05b1b2e6737867f0a3a8d70d076c077d9d8dde6a8f5e6de2ce07ac1f
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_oufuku_color_300_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_oufuku_color_300_page
            +guid:adf6ad22-97bc-4c7a-86fc-5a30ae5403f5
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=jpn_oufuku_148x200mm
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_oufuku_color_300_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        default_size = self.media.tray.get_default_size(default)
    
        if self.media.tray.is_size_supported('jpn_oufuku_148x200mm', default):
            self.media.tray.configure_tray(default, 'jpn_oufuku_148x200mm', 'stationery')
        
        elif self.media.tray.is_size_supported("com.hp.ext.mediaSize.jpn_oufuku_148x200mm.rotated", default):
            self.media.tray.configure_tray(default, "com.hp.ext.mediaSize.jpn_oufuku_148x200mm.rotated", "stationery")
            
        elif self.media.tray.is_size_supported('custom', default):
            self.media.tray.configure_tray(default, 'custom', 'stationery')
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('f744f31f05b1b2e6737867f0a3a8d70d076c077d9d8dde6a8f5e6de2ce07ac1f')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
    
        logging.info("URF Oufuku Color 300 Page - Print job completed successfully")
