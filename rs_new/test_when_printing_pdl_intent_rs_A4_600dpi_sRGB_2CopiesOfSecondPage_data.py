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
        +purpose: Simple print from a rasterstream (A4_600dpi_sRGB_2CopiesOfSecondPage.rs) file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-152360
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A4_600dpi_sRGB_2CopiesOfSecondPage.rs=bc4a70b25fe5631639032e85890a6f4d054144b06b9c43b297f6b3da183ef4d7
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_rs_A4_600dpi_sRGB_2CopiesOfSecondPage_data_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:RasterStream
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_rs_A4_600dpi_sRGB_2CopiesOfSecondPage_data
            +guid:4b6dffdf-8552-463a-995c-e56c212ac7a8
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=RasterStreamICF & DeviceClass=LFP & MediaInputInstalled=ROLL1 & MediaSizeSupported=custom
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_rs_A4_600dpi_sRGB_2CopiesOfSecondPage_data_file_then_succeeds(self):

        job_id = self.print.raw.start('bc4a70b25fe5631639032e85890a6f4d054144b06b9c43b297f6b3da183ef4d7')
        self.print.wait_for_job_completion(job_id)
        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_page_count(Intents.printintent, 2)
        self.outputverifier.verify_collated_copies(Intents.printintent, 1)
        self.outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        self.outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        self.outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
        self.outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        self.outputverifier.verify_media_source(Intents.printintent, MediaSource.roll1)
        self.outputverifier.verify_resolution(Intents.printintent, 600)
        self.outputsaver.save_output()
