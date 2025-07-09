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

from dunetuf.print.print_common_types import MediaSize, MediaType


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
    +purpose: simple print job of jpeg file of jpg5
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:jpg5.jpg=9d133dde6eb25f2e326e6b72839242a8727e0cf1b64b882f4935a73d1f3cae14
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_jpg5_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_jpg5_jpg_then_succeeds
        +guid:1320982a-cffd-4554-9413-b986ff364f6f
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
    def test_when_jpg5_jpg_then_succeeds(self):

        if self.print_emulation.print_engine_platform == 'emulator':
            installed_trays = self.print_emulation.tray.get_installed_trays()
            selected_tray = None

            for tray_id in installed_trays:
                system_tray_id = tray_id.lower().replace('tray', 'tray-')
                if tray.is_size_supported('anycustom', system_tray_id):
                    selected_tray = tray_id
                    break

            if selected_tray is None:
                raise ValueError("No tray found supporting anycustom in enterprise emulator")

            self.print_emulation.tray.open(selected_tray)
            self.print_emulation.tray.load(selected_tray, MediaSize.Custom.name, MediaType.Plain.name)
            self.print_emulation.tray.close(selected_tray)

        default = tray.get_default_source()
        media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]

        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')

        elif tray.is_size_supported('custom', default) and media_width_maximum >= 453333 and media_length_maximum >= 340000 and  media_width_minimum <= 453333 and media_length_minimum <= 340000:
            tray.configure_tray(default, 'custom', 'stationery') 

        self.print.raw.start('9d133dde6eb25f2e326e6b72839242a8727e0cf1b64b882f4935a73d1f3cae14')
        self.print.wait_for_job_completion()
        self.outputsaver.save_output()

        logging.info("Jpeg photoimages resolution tif tif1024x768 file")
