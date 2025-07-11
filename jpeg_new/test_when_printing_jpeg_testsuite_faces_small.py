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
        +purpose:Simple print job of Jpeg TestSuite faces small Page from *faces_small.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:faces_small.jpg=19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_faces_small_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_faces_small
            +guid:609c5a86-495a-4e17-a0dc-3cdc85daca8c
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
    def test_when_using_faces_small_jpg_then_succeeds(self):

        tray, media_sizes = self.media.get_source_and_media_sizes('tray-1')
        if self.print_emulation.print_engine_platform == 'emulator' and self.configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            if 'anycustom' in media_sizes:
                self.print_emulation.tray.open(tray1)
                self.print_emulation.tray.load(tray1, MediaSize.Custom.name, MediaType.Plain.name)
                self.print_emulation.tray.close(tray1)
        else:
            default_tray, media_sizes = self.media.get_source_and_media_sizes()
            if 'anycustom' in media_sizes:
                self.media.tray.configure(default_tray, 'anycustom', 'stationery')
            else:
                self.media.tray.configure(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("JPEG TestSuite faces small Page - Print job completed successfully")