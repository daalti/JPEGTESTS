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
        +purpose:URF test using **om_small_photo_100x150mm_Mono.urf
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-18912
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:om_small_photo_100x150mm_Mono.urf=02e9a7f9c9d6481ef8b88580dcb4ebb2dc458f4ec9e12ba172a9da648fb10c90
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_om_small_photo_100x150mm_mono_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_om_small_photo_100x150mm_mono
            +guid:1a1fa0f8-0d2e-4523-938b-1d6df219c42d
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=om_small-photo_100x150mm
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_om_small_photo_100x150mm_mono_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('om_small-photo_100x150mm', default):
            self.media.tray.configure_tray(default, 'om_small-photo_100x150mm', 'stationery')
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('02e9a7f9c9d6481ef8b88580dcb4ebb2dc458f4ec9e12ba172a9da648fb10c90')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
