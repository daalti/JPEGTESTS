import pytest
import logging
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.mapper import PrintMapper
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.configuration import Configuration


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
        cls.configuration = Configuration(cls.cdm)
        cls.print_mapper = PrintMapper(cls.cdm)
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

    def _update_media_input_config(self, default_tray, media_size, media_type):
        """Update media configuration for a specific tray."""
        media_input = self.media.get_media_configuration().get('inputs', [])

        for input_config in media_input:
            if input_config.get('mediaSourceId') == default_tray:
                if media_size == 'custom':
                    supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
                    capability = next(
                        (cap for cap in supported_inputs if cap.get('mediaSourceId') == default_tray),
                        {}
                    )
                    input_config['currentMediaWidth'] = capability.get('mediaWidthMaximum')
                    input_config['currentMediaLength'] = capability.get('mediaLengthMaximum')
                    input_config['currentResolution'] = capability.get('resolution')

                input_config['mediaSize'] = media_size
                input_config['mediaType'] = media_type

                self.media.update_media_configuration({'inputs': [input_config]})
                return

        logging.warning(f"No media input found for tray: {default_tray}")

    def _get_default_tray_and_media_sizes(self):
        """Get the default tray and its supported media sizes."""
        default_tray = self.media.get_default_source()
        supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
        media_sizes = next((inp.get('supportedMediaSizes', []) for inp in supported_inputs if inp.get('mediaSourceId') == default_tray), [])
        logging.info('Supported Media Sizes (%s): %s', default_tray, media_sizes)
        return default_tray, media_sizes
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178011 Simple print job of Jpeg Regression of untagged argb 100dpi Page from *untagged_argb_100dpi.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:400
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:untagged_argb_100dpi.jpg=d91801b4c08f2ed918a3cbf885a61c8721cace99b0e83a2f82e95660e2275704
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_untagged_argb_100dpi_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_regression_untagged_argb_100dpi
        +guid:dbf7757a-264e-4e71-8863-ba0115a9b456
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
        +ProA4:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_untagged_argb_100dpi_jpg_then_succeeds(self):

        if self.outputsaver.configuration.productname == "jupiter":
            self.outputsaver.operation_mode('CRC')
        else:
            self.outputsaver.operation_mode('TIFF')
        if self.print_emulation.print_engine_platform == 'emulator' and self.configuration.familyname == 'enterprise':
            installed_trays = self.print_emulation.tray.get_installed_trays()

            for tray_id in installed_trays:
                system_tray_id = tray_id.lower().replace('tray', 'tray-')
                if tray.is_size_supported('anycustom', system_tray_id):
                    self.print_emulation.tray.open(tray_id)
                    self.print_emulation.tray.load(tray_id, "Custom", MediaType.Plain.name,
                                              media_orientation="Portrait")
                    self.print_emulation.tray.close(tray_id)
                    break
        default_tray, media_sizes = self._get_default_tray_and_media_sizes()

        if 'any' in media_sizes:
            tray_test_name = self.print_mapper.get_media_input_test_name(default_tray)
            self.print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name)  # type: ignore
            self._update_media_input_config(default_tray, 'any', 'any')
        elif 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', 'stationery')
        else:
            self._update_media_input_config(default_tray, 'custom', 'stationery')
        self.outputsaver.validate_crc_tiff(udw) 
        job_id = self.print.raw.start('d91801b4c08f2ed918a3cbf885a61c8721cace99b0e83a2f82e95660e2275704',timeout=360)
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        if self.outputsaver.configuration.productname == "jupiter":
            expected_crc = ["0x9350fdc4"]    
            self.outputsaver.verify_output_crc(expected_crc)
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc() 
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')

        logging.info("JPEG Regression untagged argb 100dpi Page - Print job completed successfully")