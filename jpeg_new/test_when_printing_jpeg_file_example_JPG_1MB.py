import logging
from dunetuf.print.print_common_types import MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaType
from dunetuf.configuration import Configuration
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)
        cls.configuration = Configuration(cls.cdm)


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
        +purpose: Simple Print job of Jpeg file of 1MB from **
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:file_example_JPG_1MB.jpg=683a8528125ca09d8314435c051331de2b4c981c756721a2d12c103e8603a1d2
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_file_example_JPG_1MB_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_file_example_JPG_1MB
            +guid:c0307457-53e0-485b-ad44-5be21ea3eadb
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_file_example_JPG_1MB_file_then_succeeds(self):

        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            installed_trays = self.media.tray.get()
            selected_tray = None

            # Check each tray for supported sizes
            for tray_id in installed_trays:
                system_tray_id = tray_id.lower().replace('tray', 'tray-')
                media_sizes = self.media.get_media_sizes(system_tray_id)
                if "anycustom" in media_sizes:
                    selected_tray = tray_id
                    self.media.tray.load(selected_tray, self.media.MediaSize.Custom, self.media.MediaType.Plain, media_orientation="Portrait", need_open=True)
                    break

            if selected_tray is None:
                raise ValueError("No tray found supporting anycustom size")
        else:
            self.load_custom_tray(527777, 351944, 527777, 351944)

        job_id = self.print.raw.start('683a8528125ca09d8314435c051331de2b4c981c756721a2d12c103e8603a1d2')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Jpeg file example JPG 1MB Page - Print job completed successfully")