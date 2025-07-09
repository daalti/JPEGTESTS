
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

    def teardown_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:C52178010 Simple print job of Jpeg TestSuite parrots Progressive Interlaced Page from *parrots_Progressive_Interlaced.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:660
        +asset:PDL_Print
        +delivery_team:PDLJobPQ
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:parrots_Progressive_Interlaced.jpg=dfcaa88adf10d6833f97280b5a58893db02845db6c41495cd324ccb1145bda9a
        +test_classification:System
        +name:test_jpeg_testsuite_parrots_Progressive_Interlaced
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_parrots_Progressive_Interlaced
            +guid:5dc2bce6-1d50-44ef-9a9f-205e344d1cc6
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
        +overrides:
            +Home:
                +is_manual:False
                +timeout:660
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_jpeg_testsuite_parrots_Progressive_Interlaced(self, setup_teardown, printjob, outputsaver, tray, print_emulation, print_mapper, udw, reset_tray):
        # Print file size : width 10.67 inches and height 7.11 inches
        default = tray.get_default_source()
        supported_inputs = self.media.get_media_capabilities().get('supportedInputs', [])
        media_sizes = next((input.get('supportedMediaSizes', []) for input in supported_inputs if tray.get('mediaSourceId') == default), [])
        logging.info('Supported Media Sizes (%s): %s', default, media_sizes)

        if 'anycustom' in media_sizes:
            input = self.media.get_media_configuration().get('inputs', [])
            for media_input in input:
                if media_input.get('mediaSourceId') == default:
                    media_input['mediaSize'] = 'anycustom'
                    media_input['mediaType'] = 'stationery'
                    self.media.update_media_configuration(media_input)
        elif 'any' in media_sizes:
            tray_test_name = print_mapper.get_media_input_test_name(default)
            self.print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name)
            input = self.media.get_media_configuration().get('inputs', [])
            for media_input in input:
                if media_input.get('mediaSourceId') == default:
                    media_input['mediaSize'] = 'any'
                    media_input['mediaType'] = 'any'
                    self.media.update_media_configuration(media_input)
        else:
            input = self.media.get_media_configuration().get('inputs', [])
            for media_input in input:
                if media_input.get('mediaSourceId') == default:
                    media_input['mediaSize'] = 'custom'
                    media_input['mediaType'] = 'stationery'
                    self.media.update_media_configuration(media_input)

        outputsaver.validate_crc_tiff(udw) 
        printjob.print_verify('dfcaa88adf10d6833f97280b5a58893db02845db6c41495cd324ccb1145bda9a', timeout=600)
        outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = outputsaver.get_crc() 
        logging.info("Validate current crc with master crc")
        assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        tray.reset_trays()
        logging.info("JPEG TestSuite parrots Progressive Interlaced Page - Print job completed successfully")


