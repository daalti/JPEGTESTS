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
        +purpose: Print job of file Venn1RGB.rs **
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-152360
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Venn1RGB.rs=e4b093935481c7ec9e428194a9c7fa475558e18104bb66dfdd4736b81906f3a5
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_rs_Venn1RGB_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:RasterStream
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_rs_Venn1RGB
            +guid:ece8366d-c415-4095-8ebd-b6248f7134e9
            +dut:
                +type:Simulator
                +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF & MediaInputInstalled=ROLL1 & MediaSizeSupported=iso_a2_420x594mm
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_rs_Venn1RGB_file_then_succeeds(self):
        if self.media.is_size_supported('iso_a2_420x594mm', 'roll-1'):
            self.media.tray.configure_tray('roll-1', 'iso_a2_420x594mm', 'stationery')

        job_id = self.print.raw.start('e4b093935481c7ec9e428194a9c7fa475558e18104bb66dfdd4736b81906f3a5')
        self.print.wait_for_job_completion(job_id)
        logging.info("RS Venn1RGB - Print job completed successfully")
        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_page_count(Intents.printintent, 1)
        self.outputverifier.verify_collated_copies(Intents.printintent, 1)
        self.outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.a2)
        self.outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        self.outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
        self.outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        self.outputverifier.verify_media_source(Intents.printintent, MediaSource.roll1)
        self.outputverifier.verify_resolution(Intents.printintent, 600)
        self.outputsaver.save_output()
        self.outputverifier.outputsaver.operation_mode('NONE')
        self.media.tray.reset_trays()
