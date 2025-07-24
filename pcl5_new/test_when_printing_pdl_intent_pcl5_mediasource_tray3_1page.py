import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import Intents, MediaSize, MediaType, MediaSource


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
        +purpose:Print a PCL5 test file with media source command specified with tray3 and ensure PDL is processing the job with tray3
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-183335
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:Tray3.prn=3310656b796a1c221d51b6b7c9794cbcb5544e45b17100f0c702b36d39a84218
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_pcl5_mediasource_tray3_1page_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pdl_intent_pcl5_mediasource_tray3_1page
            +guid:85b829bd-f634-4427-a9e9-30a3805c5386
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5 & MediaInputInstalled=Tray3 & MediaSizeSupported=na_letter_8.5x11in

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_pcl5_mediasource_tray3_1page_file_then_succeeds(self):
        if tray.is_tray_supported('tray-3') and self.media.is_size_supported('na_letter_8.5x11in', 'tray-3'):
            self.media.tray.configure_tray('tray-3', 'na_letter_8.5x11in', 'stationery')
            job_id = self.print.raw.start('3310656b796a1c221d51b6b7c9794cbcb5544e45b17100f0c702b36d39a84218')
            self.print.wait_for_job_completion(job_id)
            outputverifier.save_and_parse_output()
            outputverifier.verify_page_count(Intents.printintent, 1)
            outputverifier.verify_collated_copies(Intents.printintent, 1)
            outputverifier.verify_uncollated_copies(Intents.printintent, 1)
            outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
            outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
            outputverifier.verify_media_source(Intents.printintent, MediaSource.tray3)
            self.outputsaver.save_output()
            self.outputsaver.operation_mode('NONE')
            self.media.tray.reset_trays()
