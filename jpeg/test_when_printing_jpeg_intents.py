from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.mapper import PrintMapper
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation

import logging

class TestWhenPrintingJPEGFile():
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
        """Clean up shared test resources."""
        pass

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
        """Update media configuration for a specific tray.
        
        Args:
            default_tray: Default tray identifier
            media_size: Media size to set
            media_type: Media type to set
        """
        media_input = self.media.get_media_configuration().get('inputs', [])
        
        for input_config in media_input:
            if input_config.get('mediaSourceId') == default_tray:
                # Handle custom media size configuration
                if media_size == 'custom':
                    supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
                    capability = next(
                        (cap for cap in supported_inputs if cap.get('mediaSourceId') == default_tray),
                        {}
                    )
                    input_config['currentMediaWidth'] = capability.get('mediaWidthMaximum')
                    input_config['currentMediaLength'] = capability.get('mediaLengthMaximum')
                    input_config['currentResolution'] = capability.get('resolution')
                
                # Update media properties
                input_config['mediaSize'] = media_size
                input_config['mediaType'] = media_type
                
                # Update configuration and return early
                self.media.update_media_configuration({'inputs': [input_config]})
                return
        
        logging.warning(f"No media input found for tray: {default_tray}")

    def _get_default_tray_and_media_sizes(self):
        """Get the default tray and its supported media sizes.
        
        Returns:
            tuple: (default_tray, media_sizes) where default_tray is the default source
                   and media_sizes is a list of supported media sizes for that tray
        """
        default_tray = self.media.get_default_source()
        supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
        media_sizes = next((input.get('supportedMediaSizes', []) for input in supported_inputs if input.get('mediaSourceId') == default_tray), [])
        logging.info('Supported Media Sizes (%s): %s', default_tray, media_sizes)
        return default_tray, media_sizes

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job of Jpeg TestSuite taggedRGB Page from *taggedRGB.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:300
        +asset:PDL_Print
        +delivery_team:PDLJobPQ
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:parrots_Progressive_Interlaced.jpg=dfcaa88adf10d6833f97280b5a58893db02845db6c41495cd324ccb1145bda9a
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_jpeg_testsuite_taggedRGB
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_taggedRGB
            +guid:e8210d69-3af4-4178-8b74-4e83ccf5851c
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
    def test_jpeg_testsuite_taggedRGB(self):

        default_tray, media_sizes = self._get_default_tray_and_media_sizes()

        if 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', 'stationery')
        elif 'any' in media_sizes:
            tray_test_name = self.print_mapper.get_media_input_test_name(default_tray)
            self.print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name) # type: ignore
            self._update_media_input_config(default_tray, 'any', 'any')
        else:
            self._update_media_input_config(default_tray, 'custom', 'stationery')

        self.outputsaver.validate_crc_tiff() 
        job_id = self.print.raw.start('dfcaa88adf10d6833f97280b5a58893db02845db6c41495cd324ccb1145bda9a')

        # Wait for copy job to complete
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc() 
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"