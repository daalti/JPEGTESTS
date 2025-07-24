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
        +purpose: pcl5 highvalue using 6Page_rasarro3.obj
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:900
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:6Page-rasarro3.obj=0ec97836048ae4555fe0279e538d6b3d179ceda7c7085d181d450b2c4fa00d6d
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_6page_rasarro3_file_then_succeeds
        +test:
            +title: test_pcl5_highvalue_6page_rasarro3
            +guid:d40092fb-0210-47a0-b10d-617673e44818
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
    def test_when_using_pcl5_highvalue_6page_rasarro3_file_then_succeeds(self):
        default = self.media.get_default_source()
        if self.get_platform() == 'emulator':
            self.media.tray.setup_tray(
                trayid="all",
                media_size=MediaSize.Legal.name,
                media_type=MediaType.Plain.name,
                orientation=MediaOrientation.Default.name,
                level=TrayLevel.Full.name,
            )
        elif self.media.is_size_supported('na_legal_8.5x14in', default):
            self.media.tray.configure_tray(default, 'na_legal_8.5x14in','stationery')
        job_id = self.print.raw.start('0ec97836048ae4555fe0279e538d6b3d179ceda7c7085d181d450b2c4fa00d6d')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
