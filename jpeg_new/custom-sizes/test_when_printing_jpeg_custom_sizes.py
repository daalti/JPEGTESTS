from dunetuf.print.output.intents import Intents, MediaSize
import logging
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.metadata import get_ip, get_emulation_ip
from dunetuf.cdm import get_cdm_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.udw import TclSocketClient
from dunetuf.emulation.print import PrintEmulation
from dunetuf.print.print_common_types import MediaInputIds,  MediaType
from dunetuf.configuration import Configuration
from dunetuf.print.new.output.output_verifier import OutputVerifier
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
        cls.outputverifier = OutputVerifier(cls.outputsaver)

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
        +name:TestWhenPrintingJPEGFile::test_when_using_CS300X200_150_L_file_then_succeeds
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
    def test_when_using_CS300X200_150_L_file_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()
        default_tray = self.media.get_default_source()
        self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('98b2abe4245f479ed174d858e18953abd74f50c131b1accb82141c9c190657c0')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using CS(300X200)-231-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:CS300X200-231-L.jpg=cda4d59f5ef4aa6c7b7a1ab26a50ce25e3dede1ab33db39c8ea1dfe9cd81a4b1
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_CS300X200_231_L_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_custom_size_300x200_231_landscape
            +guid:1df711df-ebf3-4634-977e-140345662b53
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    def test_when_using_CS300X200_231_L_file_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')
        default_tray = self.media.get_default_source()
        self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)


        job_id = self.print.raw.start('cda4d59f5ef4aa6c7b7a1ab26a50ce25e3dede1ab33db39c8ea1dfe9cd81a4b1')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')



    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using CS(300X200)-300-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:CS300X200-300-L.jpg=e764a78f35cd170ec6be58b5b3b528d0beb822e7165d79f0bef48ddb8be4f50b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_CS300X200_300_L_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_custom_size_300x200_300_landscape
            +guid:807972b7-2ba5-4dc3-a6c7-041542a6a715
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    def test_when_using_CS300X200_300_L_file_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        default_tray = self.media.get_default_source()

        self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('e764a78f35cd170ec6be58b5b3b528d0beb822e7165d79f0bef48ddb8be4f50b')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using CS(300X200)-600-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:CS300X200-600-L.jpg=da2f863844d9803c20e43af79113f5dc247548f79daccc3f8c34be97374d4f6f
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_CS300X200_600_L_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_custom_size_300x200_600_landscape
            +guid:3b4a60fc-1f2a-417e-bf1e-4b1328782fdc
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    def test_when_using_CS300X200_600_L_file_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        default_tray = self.media.get_default_source()
        self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('da2f863844d9803c20e43af79113f5dc247548f79daccc3f8c34be97374d4f6f')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using cs(200X300)-600-P.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:cs200X300-600-P.jpg=8e3bb43894bdac34f661ab3b93d9494468671f0677715dc315108c3873f54658
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_CS300X200_600_P_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_custom_size_200X300_600_portrait
            +guid:320cb2cb-8aca-4247-a8fb-20f3b082e76e
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

    def test_when_using_CS300X200_600_P_file_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')
        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)
        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            media_sizes = self.media.get_media_sizes('tray-1')
            if "anycustom" in media_sizes:
                self.media.tray.load(tray1, self.media.MediaSize.Custom, self.media.MediaType.Plain, need_open=True)

        else:
            self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)
        
        job_id = self.print.raw.start('8e3bb43894bdac34f661ab3b93d9494468671f0677715dc315108c3873f54658')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using cs(200X300)-150-P.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:cs200X300-150-P.jpg=d5c61c429865ee5df8b12690ad9e017b724e8aad1d2d562a5daafac7f5b14c5e
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_CS300X200_150_P_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_custom_size_200x300_150_portrait
            +guid:6dab437b-db2f-4e4f-86a3-73fe7be88bba
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

    def test_when_using_CS300X200_150_P_file_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()
        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)

        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            media_sizes = self.media.get_media_sizes('tray-1')
            if "anycustom" in media_sizes:
                self.media.tray.load(tray1, self.media.MediaSize.Custom, self.media.MediaType.Plain, need_open=True)
        else:
            self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('d5c61c429865ee5df8b12690ad9e017b724e8aad1d2d562a5daafac7f5b14c5e')
        self.print.wait_for_job_completion(job_id)
        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using cs(200X300)-231-P.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:cs200X300-231-P.jpg=fdddf6538a2e6bb0830aa6b022da3f7c3f50d00bbb0ee82d9b3417f76307e519
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_CS300X200_231_P_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_custom_size_200x300_231_portrait
            +guid:d6ee3661-ddd7-4308-a132-16550ee69a53
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

    def test_when_using_CS300X200_231_P_file_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()
        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)
        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            media_sizes = self.media.get_media_sizes('tray-1')
            if "anycustom" in media_sizes:
                self.media.tray.load(tray1, self.media.MediaSize.Custom, self.media.MediaType.Plain, need_open=True)
        else:
            self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('fdddf6538a2e6bb0830aa6b022da3f7c3f50d00bbb0ee82d9b3417f76307e519')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using cs(200X300)-300-P.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:cs200X300-300-P.jpg=c27a6a5933434299e7cb8ec2804bbf807c4f7adcbbdaa5bc39e7a91bc5082ac2
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_CS300X200_300_P_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_custom_size_200x300_300_portrait
            +guid:2dc1eb03-a584-41dc-a055-7e0a68f0f543
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    def test_when_using_CS300X200_300_P_file_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        default_tray = self.media.get_default_source()       
        self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('c27a6a5933434299e7cb8ec2804bbf807c4f7adcbbdaa5bc39e7a91bc5082ac2')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')