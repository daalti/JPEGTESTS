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
        +purpose:Simple print job of urf 5x7 color 600 page from *5x7_Color_600.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:5x7_Color_600.urf=71131a0deaaa360492a204f4633b602ef1bcb1a742acfbaa50636c77938b2d08
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_5x7_color_600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_5x7_color_600_page
            +guid:622ec9b5-a22c-41a6-95d4-7fbf7e54d5f7
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=na_5x7_5x7in

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_5x7_color_600_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('na_index_5x7_5x7in', default):
            self.media.tray.configure_tray(default, 'na_index_5x7_5x7in', 'stationery')
        elif self.media.tray.is_size_supported('na_5x7_5x7in', default):
            self.media.tray.configure_tray(default, 'na_5x7_5x7in', 'stationery')
        elif self.media.tray.is_size_supported('custom', default):
            self.media.tray.configure_tray(default, 'custom', 'stationery')

        job_id = self.print.raw.start('71131a0deaaa360492a204f4633b602ef1bcb1a742acfbaa50636c77938b2d08')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()

        logging.info("URF 5x7 color 600 page - Print job completed successfully")
