import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import Intents, MediaSize, MediaType, MediaSource, Plex, PlexBinding


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
        +purpose:Print a PCL5 test file with media source command specified with tray1, plex command specified with duplex long edge and ensure PDL is processing the job with tray1 and producing duplex long edge output
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-183335, DUNE-187154
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:pcl5_duplex_longedge_tray1.prn=d375b13a581607e4562b116af4585f5523757f255463204a43a6ce654e2080c0
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_pcl5_duplex_longedge_mediasource_tray1_2page_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pdl_intent_pcl5_duplex_longedge_mediasource_tray1_2page
            +guid:331f6bea-8bd5-4ff0-8f7c-877ecc90771b
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5 & MediaInputInstalled=Tray1 & MediaSizeSupported=na_letter_8.5x11in & Duplexer=True

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_pcl5_duplex_longedge_mediasource_tray1_2page_file_then_succeeds(self):
        if tray.is_tray_supported('tray-1') and self.media.is_size_supported('na_letter_8.5x11in', 'tray-1'):
            self.media.tray.configure_tray('tray-1', 'na_letter_8.5x11in', 'stationery')
            job_id = self.print.raw.start('d375b13a581607e4562b116af4585f5523757f255463204a43a6ce654e2080c0')
            self.print.wait_for_job_completion(job_id)
            outputverifier.save_and_parse_output()
            outputverifier.verify_plex(Intents.printintent, Plex.duplex)
            outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
            outputverifier.verify_page_count(Intents.printintent, 2)
            outputverifier.verify_collated_copies(Intents.printintent, 1)
            outputverifier.verify_uncollated_copies(Intents.printintent, 1)
            outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
            outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
            outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
            self.outputsaver.save_output()
            self.outputsaver.operation_mode('NONE')
            self.media.tray.reset_trays()
