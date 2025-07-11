from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from dunetuf.print.output_verifier import OutputVerifier
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, MediaSizeID, get_media_source
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting

A0_WIDTH_IN_INCH = 841000 / 25400.0
A0_HEIGHT_IN_INCH = 1189000 / 25400.0
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
        +purpose:Jpeg test using A0-150-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:800
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A0-150-L.jpg=513d5fdcf318c017102091023daee87d2fa69ace1bfbb8b62aec8f81cd0ddcca
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A0_150_L_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a0_150_landscape
            +guid:965fed24-0a35-4c5c-a83d-b108936c6bb6
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A0_150_L_jpg_then_succeeds(self):

        job_id = self.print.raw.start('513d5fdcf318c017102091023daee87d2fa69ace1bfbb8b62aec8f81cd0ddcca')
        self.print.wait_for_job_completion(job_id)

        #TODO: CHECK THIS
        #media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type: ignore
        #self.outputverifier.verify_media_source(Intents.printintent, media_source)


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A0-231-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A0-231-L.jpg=83c9b8a78e0aa5ee8c3dffa99eb67744678c9d1a53048675bb2ce2493e3e4b14
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A0_231_L_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a0_231_landscape
            +guid:e20def0e-7c7e-428e-809c-7c1a96080d81
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A0_231_L_jpg_then_succeeds(self):

        job_id = self.print.raw.start('83c9b8a78e0aa5ee8c3dffa99eb67744678c9d1a53048675bb2ce2493e3e4b14')
        self.print.wait_for_job_completion(job_id)
        self.outputverifier.save_and_parse_output()

        #TODO: CHECK THIS
        #media_source = get_media_source(tray.rolls[0])

        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)#type: ignore
        #self.outputverifier.verify_media_source(Intents.printintent, media_source)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A0-300-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A0-300-L.jpg=2d582a10f32bfcbdb87a7a8fbc8b97c28712c7f125b2e91b146340426f90237d
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A0_300_L_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a0_300_landscape
            +guid:8e4e4146-1e70-441d-9845-603827ae030d
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A0_300_L_jpg_then_succeeds(self):

        job_id = self.print.raw.start('2d582a10f32bfcbdb87a7a8fbc8b97c28712c7f125b2e91b146340426f90237d')
        self.print.wait_for_job_completion(job_id)

        #TODO: CHECK THIS
        #media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        #self.outputverifier.verify_media_source(Intents.printintent, media_source)


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A0-600-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A0-600-L.jpg=7cb450b01b282a6ce2117eb3357f9c72335996e96639de9ccf8ad60ae80ddd29
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A0_600_Large_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a0_600_landscape
            +guid:e9523f80-fdbf-4805-aea8-eaaf1e28fbd8
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A0_600_Large_jpg_then_succeeds(self):

        job_id = self.print.raw.start('7cb450b01b282a6ce2117eb3357f9c72335996e96639de9ccf8ad60ae80ddd29')
        self.print.wait_for_job_completion(job_id)

        #TODO: CHECK THIS
        #media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom) #type:ignore
        #self.outputverifier.verify_media_source(Intents.printintent, media_source)


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Jpeg test using A0-72-L.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A0-72-L.jpg=9b43011721bb31f222ba23e8830d8e3487b12bfd342fd52813f06ef3c35d03fd
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_A0_72_L_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_large_media_size_a0_72_landscape
            +guid:5d81b3b1-6957-4823-bcf0-87cb01d141a0
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A0_72_L_jpg_then_succeeds(self):

        expected_media_size = MediaSize.letter
        job_id = self.print.raw.start('9b43011721bb31f222ba23e8830d8e3487b12bfd342fd52813f06ef3c35d03fd')
        self.print.wait_for_job_completion(job_id)
        self.outputverifier.save_and_parse_output()

        # expecting large media sizes to be printed on rolls
        inputs = self.media.get_media_configuration().get('inputs', [])
        rolls = [mediaSource.get('mediaSourceId') for mediaSource in inputs if mediaSource.get('inputType') == "continuousRoll"]
        if rolls is not None:
            expected_media_size = MediaSize.custom
            job_resolution = self.outputverifier.get_intent(Intents.printintent)[0].resolution
            # verify A0 dimensions. Landscape width too large, so image will be rotated
            expected_width = round(A0_WIDTH_IN_INCH * job_resolution)
            expected_height = round(A0_HEIGHT_IN_INCH * job_resolution)
            self.outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
            self.outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size) #type:ignore