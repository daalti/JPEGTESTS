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
        +purpose:Simple print job of Urf Hagaki Color 600 from *Hagaki_Color_600.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Hagaki_Color_600.urf=f273961965cdd305347a75c09b20b4203d7df0b43f6c5c93f5761871d12c7d50
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_hagaki_color_600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_hagaki_color_600_page
            +guid:08865595-5feb-4330-b11e-2864293f88cf
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=jpn_hagaki_100x148mm
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_hagaki_color_600_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('jpn_hagaki_100x148mm', default):
            self.media.tray.configure_tray(default, 'jpn_hagaki_100x148mm', 'stationery')
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('f273961965cdd305347a75c09b20b4203d7df0b43f6c5c93f5761871d12c7d50')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
    
        logging.info("URF Hagaki Color 600 page - Print job completed successfully")
