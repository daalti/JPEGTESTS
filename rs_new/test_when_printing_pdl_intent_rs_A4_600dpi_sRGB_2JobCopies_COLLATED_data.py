import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, MediaType, MediaSource
from dunetuf.print.new.output.output_verifier import OutputVerifier

class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        cls.outputverifier = OutputVerifier(cls.outputsaver)

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
        +purpose: Simple print from a rasterstream (A4_600dpi_sRGB_2JobCopies_COLLATED.rs) file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-152360
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A4_600dpi_sRGB_2JobCopies_COLLATED.rs=8cb230878e51ead194983adb7aceb9a8768f4fcae3aa8040987124e9f89cd690
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_rs_A4_600dpi_sRGB_2JobCopies_COLLATED_data_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:RasterStream
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_rs_A4_600dpi_sRGB_2JobCopies_COLLATED_data
            +guid:f046ff77-4c80-4db2-a7b5-85cce2aa0429
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=RasterStreamICF & DeviceClass=LFP & MediaInputInstalled=ROLL1 & MediaSizeSupported=iso_a4_210x297mm
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_rs_A4_600dpi_sRGB_2JobCopies_COLLATED_data_file_then_succeeds(self):
        if self.media.is_size_supported('iso_a4_210x297mm', 'roll-1'):
            self.media.tray.configure_tray('roll-1', 'iso_a4_210x297mm', 'stationery')

        job_id = self.print.raw.start('8cb230878e51ead194983adb7aceb9a8768f4fcae3aa8040987124e9f89cd690')
        self.print.wait_for_job_completion(job_id)
        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_page_count(Intents.printintent, 2)
        self.outputverifier.verify_collated_copies(Intents.printintent, 2)
        self.outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
        self.outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        self.outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
        self.outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        self.outputverifier.verify_media_source(Intents.printintent, MediaSource.roll1)
        self.outputverifier.verify_resolution(Intents.printintent, 600)
        self.outputverifier.outputsaver.operation_mode('NONE')
        self.media.tray.reset_trays()
