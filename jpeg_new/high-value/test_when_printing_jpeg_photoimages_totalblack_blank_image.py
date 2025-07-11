import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting

from dunetuf.print.print_common_types import MediaSize, MediaType


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)
        cls.udw = get_underware_instance(cls.ip_address)
        engine_simulator_ip = get_emulation_ip()
        cls.tcl = TclSocketClient(cls.ip_address, 9104)
        if engine_simulator_ip == 'None':
            logging.debug('Instantiating PrintEmulation: no engineSimulatorIP specified, was -eip not set to emulator/simulator emulation IP?')
            engine_simulator_ip = None
        logging.info('Instantiating PrintEmulation with %s', engine_simulator_ip)
        cls.print_emulation = PrintEmulation(cls.cdm, cls.udw, cls.tcl, engine_simulator_ip)

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
    
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: simple print job of jpeg file of photoimages_totalblack_blank_image
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_TotalBlack_Blank_image.JPG=3de1610f16b15c0e583399fed0580633c25758ab0ce4f8ebecda9836f21f6fc2
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_photoimages_TotalBlack_Blank_image_JPG_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_totalblack_blank_image
            +guid:51a7c5f9-ef3f-448c-bc12-1fc5818cba45
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
    def test_when_photoimages_TotalBlack_Blank_image_JPG_then_succeeds(self):

        if self.print_emulation.print_engine_platform == 'emulator':
            installed_trays = self.print_emulation.tray.get_installed_trays()
            selected_tray = None

            for tray_id in installed_trays:
                system_tray_id = tray_id.lower().replace('tray', 'tray-')
                tray, media_sizes = self.media.get_source_and_media_sizes(system_tray_id)
                if 'anycustom' in media_sizes:
                    selected_tray = tray_id
                    break

            if selected_tray is None:
                raise ValueError("No tray found supporting anycustom in enterprise emulator")

            self.print_emulation.tray.open(selected_tray)
            self.print_emulation.tray.load(selected_tray, MediaSize.Custom.name, MediaType.Plain.name)
            self.print_emulation.tray.close(selected_tray)

        job_id = self.print.raw.start('3de1610f16b15c0e583399fed0580633c25758ab0ce4f8ebecda9836f21f6fc2')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg photoimages_TotalBlack_Blank_image file")