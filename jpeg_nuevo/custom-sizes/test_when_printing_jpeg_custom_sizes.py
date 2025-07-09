from dunetuf.print.output.intents import Intents, MediaSize
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
from dunetuf.print.print_common_types import MediaInputIds,  MediaType, MediaOrientation
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
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using CS(300X200)-150-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:CS300X200-150-L.jpg=98b2abe4245f479ed174d858e18953abd74f50c131b1accb82141c9c190657c0
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_CS300X200_150_L_jpg_then_succeeds_8
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_custom_size_300x200_150_landscape
        +guid:812f63b9-ae8f-47d0-8bff-6b6642f0ce84
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_CS300X200_150_L_jpg_then_succeeds(self):

        self.outputsaver.validate_crc_tiff(udw)
        default = tray.get_default_source()
        default_size = tray.get_default_size(default)
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        else:
            tray.configure_tray(default, 'custom', 'stationery')

        job_id = self.print.raw.start('98b2abe4245f479ed174d858e18953abd74f50c131b1accb82141c9c190657c0')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_CS300X200_150_L_jpg_then_succeeds_8
        +guid:1df711df-ebf3-4634-977e-140345662b53
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_CS300X200_150_L_jpg_then_succeeds_2(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')
        default = tray.get_default_source()
        default_size = tray.get_default_size(default)
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        else:
            tray.configure_tray(default, 'custom', 'stationery')


        job_id = self.print.raw.start('cda4d59f5ef4aa6c7b7a1ab26a50ce25e3dede1ab33db39c8ea1dfe9cd81a4b1')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_CS300X200_150_L_jpg_then_succeeds_8
        +guid:807972b7-2ba5-4dc3-a6c7-041542a6a715
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_CS300X200_150_L_jpg_then_succeeds_3(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.custom

        default = tray.get_default_source()
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
            expected_media_size = MediaSize.custom
        else:
            tray.configure_tray(default, 'custom', 'stationery')
            expected_media_size = MediaSize.custom

        job_id = self.print.raw.start('e764a78f35cd170ec6be58b5b3b528d0beb822e7165d79f0bef48ddb8be4f50b')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_CS300X200_150_L_jpg_then_succeeds_8
        +guid:3b4a60fc-1f2a-417e-bf1e-4b1328782fdc
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_CS300X200_150_L_jpg_then_succeeds_4(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.custom

        default = tray.get_default_source()
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
            expected_media_size = MediaSize.custom
        else:
            tray.configure_tray(default, 'custom', 'stationery')
            expected_media_size = MediaSize.custom

        job_id = self.print.raw.start('da2f863844d9803c20e43af79113f5dc247548f79daccc3f8c34be97374d4f6f')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_CS300X200_150_L_jpg_then_succeeds_8
        +guid:320cb2cb-8aca-4247-a8fb-20f3b082e76e
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_CS300X200_150_L_jpg_then_succeeds_5(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')
        expected_media_size = MediaSize.custom
        default = tray.get_default_source()
        if self.print_emulation.print_engine_platform == 'emulator' and self.configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            if tray.is_size_supported('anycustom', 'tray-1'):
                self.print_emulation.tray.open(tray1)
                self.print_emulation.tray.load(tray1, "Custom", MediaType.Plain.name)
                self.print_emulation.tray.close(tray1)
        else:
            if tray.is_size_supported('anycustom', default):
                tray.configure_tray(default, 'anycustom', 'stationery')
                expected_media_size = MediaSize.custom
            else:
                tray.configure_tray(default, 'custom', 'stationery')
                expected_media_size = MediaSize.custom

        job_id = self.print.raw.start('8e3bb43894bdac34f661ab3b93d9494468671f0677715dc315108c3873f54658')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_CS300X200_150_L_jpg_then_succeeds_8
        +guid:6dab437b-db2f-4e4f-86a3-73fe7be88bba
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_CS300X200_150_L_jpg_then_succeeds_6(self):

        self.outputsaver.validate_crc_tiff(udw)
        default = tray.get_default_source()
        default_size = tray.get_default_size(default)

        if self.print_emulation.print_engine_platform == 'emulator' and self.configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            if tray.is_size_supported('anycustom', 'tray-1'):
                self.print_emulation.tray.open(tray1)
                self.print_emulation.tray.load(tray1, "Custom", MediaType.Plain.name)
                self.print_emulation.tray.close(tray1)
        else:
            if tray.is_size_supported('anycustom', default):
                tray.configure_tray(default, 'anycustom', 'stationery')
            else:
                tray.configure_tray(default, 'custom', 'stationery')

        job_id = self.print.raw.start('d5c61c429865ee5df8b12690ad9e017b724e8aad1d2d562a5daafac7f5b14c5e')
        self.print.wait_for_job_completion(job_id)
        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_CS300X200_150_L_jpg_then_succeeds_8
        +guid:d6ee3661-ddd7-4308-a132-16550ee69a53
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_CS300X200_150_L_jpg_then_succeeds_7(self):

        self.outputsaver.validate_crc_tiff(udw)
        default = tray.get_default_source()
        default_size = tray.get_default_size(default)
        if self.print_emulation.print_engine_platform == 'emulator' and self.configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            if tray.is_size_supported('anycustom', 'tray-1'):
                self.print_emulation.tray.open(tray1)
                self.print_emulation.tray.load(tray1, "Custom", MediaType.Plain.name)
                self.print_emulation.tray.close(tray1)
        else:
            if tray.is_size_supported('anycustom', default):
                tray.configure_tray(default, 'anycustom', 'stationery')
            else:
                tray.configure_tray(default, 'custom', 'stationery')

        job_id = self.print.raw.start('fdddf6538a2e6bb0830aa6b022da3f7c3f50d00bbb0ee82d9b3417f76307e519')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_CS300X200_150_L_jpg_then_succeeds_8
        +guid:2dc1eb03-a584-41dc-a055-7e0a68f0f543
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_CS300X200_150_L_jpg_then_succeeds_8(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.custom

        default = tray.get_default_source()
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
            expected_media_size = MediaSize.custom
        else:
            tray.configure_tray(default, 'custom', 'stationery')
            expected_media_size = MediaSize.custom

        job_id = self.print.raw.start('c27a6a5933434299e7cb8ec2804bbf807c4f7adcbbdaa5bc39e7a91bc5082ac2')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')
