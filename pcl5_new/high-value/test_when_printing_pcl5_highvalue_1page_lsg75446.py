import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.print_common_types import MediaOrientation, TrayLevel
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
        +purpose: pcl5 highvalue using 1Page_lsg75446.obj
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:1Page-lsg75446.obj=5204ace0373a691e6fe20204ec0d089d8385b8f4b4b22d9fc39a9ec2bd6af1b3
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_1page_lsg75446_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pcl5_highvalue_1page_lsg75446
            +guid:fbbe16f5-38b6-4814-8634-758f56c3f629
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_highvalue_1page_lsg75446_file_then_succeeds(self):
        default = self.media.get_default_source()
        if self.get_platform() == 'emulator':
            self.media.tray.setup_tray(trayid="all", media_size=MediaSize.A4.name, media_type=MediaType.Plain.name,
                                        orientation=MediaOrientation.Default.name, level=TrayLevel.Full.name)


        elif self.media.is_size_supported('iso_a4_210x297mm', default):
            self.media.tray.configure_tray(default, 'iso_a4_210x297mm','stationery')

        job_id = self.print.raw.start('5204ace0373a691e6fe20204ec0d089d8385b8f4b4b22d9fc39a9ec2bd6af1b3')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
