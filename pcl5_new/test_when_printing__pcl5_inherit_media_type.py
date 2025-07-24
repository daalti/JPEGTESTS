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
        +purpose:test for pcl5 for inherit media type from tray functionality
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-13650
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:tray1_a4_notype_pcl5.prn=5ac9906a9fe61f103123109d5b147e5618a7cfd9f7faee8d4a8918849ab98a28
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using__pcl5_inherit_media_type_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pcl5_inherit_media_type
            +guid:e14e4bfd-e3ed-4ab4-a3cb-6c978dc6de3d
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5 & MediaType=Bond & MediaInputInstalled=Tray1 & MediaSizeSupported=iso_a4_210x297mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using__pcl5_inherit_media_type_file_then_succeeds(self):
        if self.media.is_size_supported('iso_a4_210x297mm', 'tray-1') and tray.is_type_supported('stationery-bond', 'tray-1'):
            self.media.tray.configure_tray('tray-1', 'iso_a4_210x297mm', 'stationery-bond')

        job_id = self.print.raw.start('5ac9906a9fe61f103123109d5b147e5618a7cfd9f7faee8d4a8918849ab98a28')
        self.print.wait_for_job_completion(job_id)
        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
        outputverifier.verify_media_type(Intents.printintent, MediaType.bond)
        outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)

        self.outputsaver.save_output()
        self.media.tray.reset_trays()
