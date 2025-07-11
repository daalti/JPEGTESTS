from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, get_media_source
from dunetuf.print.output_verifier import OutputVerifier
import logging
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting

class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
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

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A3-150-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A3-150-L.jpg=44f6cf3630ed32881134bea9153428d57c69fde0efbe38da68a24e95ff2c68dc
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a3_150_landscape
            +guid:93b519fb-4c6f-4f60-ad8f-dd70ad4175b1
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm & MediaInputInstalled = Tray1

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        if 'iso_a3_297x420mm' in media_sizes:
            self.media.tray.configure(default_tray, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('44f6cf3630ed32881134bea9153428d57c69fde0efbe38da68a24e95ff2c68dc')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A3-231-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A3-231-L.jpg=98a7b77efdee8efca9bc37d2f93b6b081e78d7aa3d13ccea2260e25ef1eee317
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_2
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a3_231_landscape
            +guid:23664a85-3878-4388-884e-2b6d7fe45d10
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm & MediaInputInstalled = Tray1

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    def test_when_A3_150_L_jpg_then_succeeds_2(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        if 'iso_a3_297x420mm' in media_sizes:
            self.media.tray.configure(default_tray, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('98a7b77efdee8efca9bc37d2f93b6b081e78d7aa3d13ccea2260e25ef1eee317')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A3-300-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A3-300-L.jpg=d7d4d21b5d1b3269b57c3208c0e3272b162c439b1a9a40dd01981358dcd2eb62
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_3
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a3_300_landscape
            +guid:db63ab21-43c0-4819-80c2-93f10622470b
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm & EngineFirmwareFamily=Maia

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    def test_when_A3_150_L_jpg_then_succeeds_3(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        job_id = self.print.raw.start('d7d4d21b5d1b3269b57c3208c0e3272b162c439b1a9a40dd01981358dcd2eb62')
        self.print.wait_for_job_completion(job_id)

        #media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        #self.outputverifier.verify_media_source(Intents.printintent, media_source)
        self.outputverifier.outputsaver.operation_mode('NONE')

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A3-600-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files: A3-600-L.jpg=5ecd428b320c23d6f899cb26277f73ffbfdee376ad8625d1189ca6eff6140013
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_4
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a3_600_landscape
            +guid:76a8391b-a1ed-4ce4-acc7-6ccaeb8e825e
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    def test_when_A3_150_L_jpg_then_succeeds_4(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        job_id = self.print.raw.start('5ecd428b320c23d6f899cb26277f73ffbfdee376ad8625d1189ca6eff6140013')
        self.print.wait_for_job_completion(job_id)

        #media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        #self.outputverifier.verify_media_source(Intents.printintent, media_source)
        self.outputverifier.outputsaver.operation_mode('NONE')


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A3-150-P.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A3-150-P.jpg=52e22db4d0237e6cf053a243d10b49e773ca4a0e5dbc5ebae3f48c8e87cefeba
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_5
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a3_150_portrait
            +guid:2fafe0b2-4e0f-4b15-9d1a-317596055456
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    def test_when_A3_150_L_jpg_then_succeeds_5(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        if 'iso_a3_297x420mm' in media_sizes:
            self.media.tray.configure(default_tray, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('52e22db4d0237e6cf053a243d10b49e773ca4a0e5dbc5ebae3f48c8e87cefeba')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A3-231-P.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A3-231-P.jpg=8b9f79cd74a56bb19019053cd9500429069e2afa20932b0aad2acbb11c49a30e
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_6
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a3_231_portrait
            +guid:69ec5c9b-3b86-4ca7-bda9-e0660b1c1cc6
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """

    def test_when_A3_150_L_jpg_then_succeeds_6(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        if 'iso_a3_297x420mm' in media_sizes:
            self.media.tray.configure(default_tray, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('8b9f79cd74a56bb19019053cd9500429069e2afa20932b0aad2acbb11c49a30e')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A3-300-P.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A3-300-P.jpg=93caf9440369f33424aaeebe4c1238e86c29625d08e1cef696d837aad108bbc7
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_7
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a3_300_portrait
            +guid:a59ac9b0-5874-4f02-b77f-245943828fe0
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds_7(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        if 'iso_a3_297x420mm' in media_sizes:
            self.media.tray.configure(default_tray, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('93caf9440369f33424aaeebe4c1238e86c29625d08e1cef696d837aad108bbc7')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A3-600-P.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A3-600-P.jpg=d93ee93e25e90f605960ba6df9fd3ea2e0b0b733c5bfabebfa8a202b4fa771d2
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_8
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a3_600_portrait
            +guid:70154fb5-26a4-4bdc-86d7-d8420fbda99b
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds_8(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        if 'iso_a3_297x420mm' in media_sizes:
            self.media.tray.configure(default_tray, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('d93ee93e25e90f605960ba6df9fd3ea2e0b0b733c5bfabebfa8a202b4fa771d2')
        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size) #type:ignore
        self.outputverifier.outputsaver.operation_mode('NONE')