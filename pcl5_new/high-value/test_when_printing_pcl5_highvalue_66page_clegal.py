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
        +purpose: pcl5 highvalue using 66Page_clegal.obj
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:900
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:66Page-clegal.obj=6bd52cbabaf17018c6532f32e854e6bd60559c3777d66c94bc00eee25fc785d4
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_66page_clegal_file_then_succeeds
        +test:
            +title: test_pcl5_highvalue_66page_clegal
            +guid:689c35aa-a8b6-49f4-a24e-7b8e848df9d2
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:900
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_highvalue_66page_clegal_file_then_succeeds(self):
        default = self.media.get_default_source()
        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            installed_trays = self.media.tray.get_installed_trays()
            for tray_id in installed_trays:
                supported_sizes = self.media.tray.get_supported_media_sizes(tray_id, edge='short')
                supported_types = self.media.tray.get_supported_media_types(tray_id)
                if MediaSize.Legal.name in supported_sizes and MediaType.Plain.name in supported_types:
                    self.media.tray.capacity_unlimited(tray_id)
                    self.media.tray.load(tray_id, MediaSize.Legal.name, MediaType.Plain.name)
        elif self.media.is_size_supported('na_legal_8.5x14in', default):
            self.media.tray.configure_tray(default, 'na_legal_8.5x14in','stationery')
        job_id = self.print.raw.start('6bd52cbabaf17018c6532f32e854e6bd60559c3777d66c94bc00eee25fc785d4')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
