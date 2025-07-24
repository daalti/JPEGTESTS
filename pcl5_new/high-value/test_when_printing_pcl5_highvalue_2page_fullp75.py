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
        +purpose: pcl5 highvalue using 2Page_fullp75.obj
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:2Page-fullp75.obj=a7c12839b6aedd8ebead9578139358bc3fd6d9ce8bf919549401537503f4b48e
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_2page_fullp75_file_then_succeeds
        +test:
            +title: test_pcl5_highvalue_2page_fullp75
            +guid:8a0027a2-5835-4400-aa3b-4d58c0a16639
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
    def test_when_using_pcl5_highvalue_2page_fullp75_file_then_succeeds(self):
        default = self.media.get_default_source()
        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            print ("emulator execution")
            # Get list of installed trays
            installed_trays = self.media.tray.get_installed_trays()
            selected_tray = None

            # Check each tray for Legal/Plain support
            for tray_id in installed_trays:
                supported_sizes = self.media.tray.get_supported_media_sizes(tray_id, edge='short')
                supported_types = self.media.tray.get_supported_media_types(tray_id)

                # Check if this tray supports Legal and Plain
                if MediaSize.Legal.name in supported_sizes and MediaType.Plain.name in supported_types:
                    selected_tray = tray_id
                    break

            if selected_tray is None:
                raise ValueError("No tray found supporting Legal size and Plain type paper")

            # Open and load the selected tray
            self.media.tray.open(selected_tray)
            self.media.tray.load(selected_tray, MediaSize.Legal.name, MediaType.Plain.name,
                                    media_orientation=MediaOrientation.Portrait.name)
            self.media.tray.close(selected_tray)
        else:
            if self.media.is_size_supported('na_legal_8.5x14in', default):
                self.media.tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')
        job_id = self.print.raw.start('a7c12839b6aedd8ebead9578139358bc3fd6d9ce8bf919549401537503f4b48e')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
