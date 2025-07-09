import pytest
import logging
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel


class TestWhenPrintingJPEGFile:
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()
        cls.media = Media()
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
        cls.tcl.close()

    def setup_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Get media configuration
        self.default_configuration = self.media.get_media_configuration()

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
    +purpose:Jpeg test using **Low_Resolution.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Low_Resolution.jpg=c8c83c0ed7b494873b33ce156398af91d873f8317276b8055ccb0022d8f1b398
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_Low_Resolution_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_Low_Resolution_jpg_then_succeeds
        +guid:8f5ca910-fde2-4409-a7d2-c7e8a80fbdbe
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
    def test_when_Low_Resolution_jpg_then_succeeds(self):

        # Setting udw command for crc to true for generating pdl crc after print job done
        self.outputsaver.validate_crc_tiff(udw)
        if self.print_emulation.print_engine_platform == 'emulator':
            installed_trays = self.print_emulation.tray.get_installed_trays()

            for tray_id in installed_trays:
                if self.outputsaver.configuration.productname == "camden":
                    self.print_emulation.tray.load(tray_id, 'ThreeXFive', MediaType.Plain.name)
                else:
                    self.print_emulation.tray.load(tray_id, MediaSize.A4.name, MediaType.Plain.name)
        self.print.raw.start('c8c83c0ed7b494873b33ce156398af91d873f8317276b8055ccb0022d8f1b398')
        self.print.wait_for_job_completion()
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
