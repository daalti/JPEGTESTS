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
        +purpose:URF test using **Number_9_Mono_600.urf
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-18912
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Number_9_Mono_600.urf=3e091270125d982ed891f73d6f3705cb1d2a664e0a7dc11cfe6ab9cde1c78d2b
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_number_9_mono_600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_number_9_mono_600
            +guid:f66cbf0c-f051-4d91-8940-1c95fb46ccbb
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-9_3.875x8.875in &  MediaInputInstalled=Tray3
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_number_9_mono_600_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('na_number-9_3.875x8.875in', default):
            self.media.tray.configure_tray(default, 'na_number-9_3.875x8.875in', 'stationery')
        elif self.media.tray.is_size_supported('custom', default):
            self.media.tray.configure_tray(default, 'custom', 'stationery')
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('3e091270125d982ed891f73d6f3705cb1d2a664e0a7dc11cfe6ab9cde1c78d2b')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
