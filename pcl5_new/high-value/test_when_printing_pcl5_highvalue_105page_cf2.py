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
        +purpose: pcl5 highvalue using 105Page_cf2.obj
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:1500
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:105Page-cf2.obj=d31350e23fd4d553e2c31bff37d41b00921c8530348705300b1e058d5f3cdfc5
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_105page_cf2_file_then_succeeds
        +test:
            +title: test_pcl5_highvalue_105page_cf2
            +guid:78e66020-a051-4599-ace1-94c1bd397a71
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
    def test_when_using_pcl5_highvalue_105page_cf2_file_then_succeeds(self):
        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            installed_trays = self.media.tray.get_installed_trays()
            selected_tray = None

            for tray_id in installed_trays:
                supported_sizes = self.media.tray.get_supported_media_sizes(tray_id, edge='short')
                supported_types = self.media.tray.get_supported_media_types(tray_id)

                if MediaSize.Letter.name in supported_sizes and MediaType.Plain.name in supported_types:
                    selected_tray = tray_id
                    break

            if selected_tray is None:
                raise ValueError("No tray found supporting Letter size and Plain type paper")

            self.media.tray.capacity_unlimited(selected_tray)
            self.media.tray.open(selected_tray)
            self.media.tray.load(selected_tray, MediaSize.Letter.name, MediaType.Plain.name,
                                  media_orientation=MediaOrientation.Portrait.name)
            self.media.tray.close(selected_tray)

        job_id = self.print.raw.start('d31350e23fd4d553e2c31bff37d41b00921c8530348705300b1e058d5f3cdfc5')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
