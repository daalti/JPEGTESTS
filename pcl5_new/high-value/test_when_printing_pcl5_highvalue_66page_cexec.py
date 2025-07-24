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
        +purpose: pcl5 highvalue using 66Page_cexec.obj
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:900
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:66Page-cexec.obj=1813aef5904a3536308dd913ebe77a7880851c2ab90aa7a56de747e0e3cab63b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_66page_cexec_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pcl5_highvalue_66page_cexec
            +guid:16c1a026-4485-41b8-a782-78d7c05ca040
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
    def test_when_using_pcl5_highvalue_66page_cexec_file_then_succeeds(self):
        default = self.media.get_default_source()
        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            installed_trays = self.media.tray.get_installed_trays()
            for tray_id in installed_trays:
                supported_sizes = self.media.tray.get_supported_media_sizes(tray_id, edge='short')
                supported_types = self.media.tray.get_supported_media_types(tray_id)
                if MediaSize.Executive.name in supported_sizes and MediaType.Plain.name in supported_types:
                    self.media.tray.capacity_unlimited(tray_id)
                    self.media.tray.load(tray_id, MediaSize.Executive.name, MediaType.Plain.name)
                    logging.info(f"Emulator: Loaded {tray_id} with Executive and Plain")
        elif self.media.is_size_supported('na_executive_7.25x10.5in', default):
            self.media.tray.configure_tray(default, 'na_executive_7.25x10.5in','stationery')
        job_id = self.print.raw.start('1813aef5904a3536308dd913ebe77a7880851c2ab90aa7a56de747e0e3cab63b')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
