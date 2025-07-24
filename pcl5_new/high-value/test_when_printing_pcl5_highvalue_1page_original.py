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
        +purpose: pcl5 highvalue using 1Page_Original.prn
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:1Page-Original.prn=9b3eab0da0d187f3992d76f387c8e95c7ab2607b7ff5df84bec30ea11c8be90d
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_1page_original_file_then_succeeds
        +test:
            +title: test_pcl5_highvalue_1page_original
            +guid:194102f7-d23d-4325-9c20-8e88faa51e2c
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
    def test_when_using_pcl5_highvalue_1page_original_file_then_succeeds(self):

        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            # Get list of installed trays
            installed_trays = self.media.tray.get_installed_trays()
            selected_tray = None

            # Check each tray for A4/Plain support
            for tray_id in installed_trays:
                supported_sizes = self.media.tray.get_supported_media_sizes(tray_id, edge='short')
                supported_types = self.media.tray.get_supported_media_types(tray_id)

                # Check if this tray supports A4 and Plain
                if MediaSize.A4.name in supported_sizes and MediaType.Plain.name in supported_types:
                    selected_tray = tray_id
                    break

            if selected_tray is None:
                raise ValueError("No tray found supporting A4 size and Plain type paper")

            # Open and load the selected tray
            self.media.tray.open(selected_tray)
            self.media.tray.load(selected_tray, MediaSize.A4.name, MediaType.Plain.name,
                                    media_orientation=MediaOrientation.Portrait.name)
            self.media.tray.close(selected_tray)
        else:

            # Original code for non-emulator case
            default = self.media.get_default_source()
            if self.media.is_size_supported('iso_a4_210x297mm', default):
                self.media.tray.configure_tray(default, 'iso_a4_210x297mm', 'any')

        job_id = self.print.raw.start('9b3eab0da0d187f3992d76f387c8e95c7ab2607b7ff5df84bec30ea11c8be90d')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
