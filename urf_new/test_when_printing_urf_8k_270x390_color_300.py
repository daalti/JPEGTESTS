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
        +purpose:Simple print job of urf 8k_270x390 Color 300 page from *8k_270x390_Color_300.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:8k_270x390_Color_300.urf=fb0c516176512a33ca11734be94840db5d9097685216ce69e09f7104a85dbcfd
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_8k_270x390_color_300_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_8k_270x390_color_300_page
            +guid:c8292e35-8b98-4576-a23e-9b0d2cb1be91
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_8k_270x390_color_300_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('om_8k_270x390mm', default):
            self.media.tray.configure_tray(default, 'om_8k_270x390mm', 'stationery')

        job_id = self.print.raw.start('fb0c516176512a33ca11734be94840db5d9097685216ce69e09f7104a85dbcfd')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()

        logging.info("URF 8k_270x390 Color 300 page - Print job completed successfully")
