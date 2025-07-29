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
        +purpose: Print job of file Venn1CMYK.rs **
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-152360
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Venn1CMYK.rs=2460d37ca59f6d731cd69e69f62e3f50846a1c7b80859d8172780a4f40064693
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_rs_Venn1CMYK_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:RasterStream
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_rs_Venn1CMYK
            +guid:2d7c5697-2f16-4879-8754-effbb83b0f2f
            +dut:
                +type:Simulator
                +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF & MediaInputInstalled=ROLL2 & MediaSizeSupported=iso_a1_594x841mm
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_rs_Venn1CMYK_file_then_succeeds(self):
        if self.media.is_size_supported('iso_a1_594x841mm', 'roll-2'):
            self.media.tray.configure_tray('roll-2', 'iso_a1_594x841mm', 'stationery')

        job_id = self.print.raw.start('2460d37ca59f6d731cd69e69f62e3f50846a1c7b80859d8172780a4f40064693')
        self.print.wait_for_job_completion(job_id)
        logging.info("RS Venn1CMYK - Print job completed successfully")
        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_page_count(Intents.printintent, 1)
        self.outputverifier.verify_collated_copies(Intents.printintent, 1)
        self.outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.a1)
        self.outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        self.outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
        self.outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        self.outputverifier.verify_media_source(Intents.printintent, MediaSource.roll2)
        self.outputverifier.verify_resolution(Intents.printintent, 600)
        self.outputsaver.save_output()
        self.outputverifier.outputsaver.operation_mode('NONE')
        self.media.tray.reset_trays()
