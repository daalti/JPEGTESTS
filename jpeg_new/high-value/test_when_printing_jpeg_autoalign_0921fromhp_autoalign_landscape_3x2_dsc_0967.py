import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation
from dunetuf.configuration import Configuration
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting

class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)
        cls.udw = get_underware_instance(cls.ip_address)
        cls.configuration = Configuration(cls.cdm)
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
        +purpose: simple print job of jpeg file of autoalign 0921fromhp autoalign landscape 3x2 dsc 0967
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:autoAlign_0921fromHP_AutoAlign_Landscape_3x2_DSC_0967.JPG=9a0f8feea5185a818537425da9affc905d0ef63c4ef0f675b564fdda4728385b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_autoAlign_0921fromHP_AutoAlign_Landscape_3x2_DSC_0967_JPG_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_autoalign_0921fromhp_autoalign_landscape_3x2_dsc_0967
            +guid:8c73fa82-b3a5-4139-bd77-237385f01490
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
    def test_when_autoAlign_0921fromHP_AutoAlign_Landscape_3x2_DSC_0967_JPG_then_succeeds(self):

        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        if 'anycustom' in media_sizes:
            if self.print_emulation.print_engine_platform == 'emulator' and self.configuration.familyname == 'enterprise':
                tray1 = MediaInputIds.Tray1.name
                tray, media_sizes = self.media.get_source_and_media_sizes('tray-1')
                if 'custom' in media_sizes:
                    self.print_emulation.tray.open(tray1)
                    self.print_emulation.tray.load(tray1, MediaSize.Custom.name, MediaType.Plain.name)
                    self.print_emulation.tray.close(tray1)
            else:
                self.media.tray.configure(default_tray, 'anycustom', 'stationery')
        else:
            self.media.tray.configure(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('9a0f8feea5185a818537425da9affc905d0ef63c4ef0f675b564fdda4728385b')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg autoAlign 0921fromHP AutoAlign Landscape 3x2 DSC 0967 file")