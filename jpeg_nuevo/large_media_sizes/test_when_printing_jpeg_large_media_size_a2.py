from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, MediaSizeID, get_media_source

A2_WIDTH_IN_INCH = 420000 / 25400
A2_HEIGHT_IN_INCH = 594000 / 25400

class TestWhenPrintingJPEGFile:
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()
        cls.media = Media()
        cls.outputsaver = OutputSaver()

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
    +purpose:Jpeg test using A2-150-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A2-150-L.jpg=0c0c9cb7efafcd92862dc8f5bc3f4162b22c5fd073474314e61a186ac57213b0
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_A2_150_L_jpg_then_succeeds_8
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_A2_150_L_jpg_then_succeeds_8
        +guid:04f78c4f-3f82-445d-b46b-f41263064867
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A2_150_L_jpg_then_succeeds(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        self.print.raw.start('0c0c9cb7efafcd92862dc8f5bc3f4162b22c5fd073474314e61a186ac57213b0')
        self.print.wait_for_job_completion()
        outputverifier.save_and_parse_output()

        expected_media_size = MediaSize.letter
        if tray.rolls is not None:
            expected_media_size = MediaSize.custom
            job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
            expected_width = round(A2_HEIGHT_IN_INCH * job_resolution)
            expected_height = round(A2_WIDTH_IN_INCH * job_resolution)
            outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
            outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A2_150_L_jpg_then_succeeds_8
        +guid:05c40791-e440-4e8a-b1b4-79eae10d66c2
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A2_150_L_jpg_then_succeeds_2(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        self.print.raw.start('d3aa431d8e5e8642c464c5847a85870e24a18548a48434a17d18bfbee779beef')
        self.print.wait_for_job_completion()
        media_source = get_media_source(tray.rolls[0])

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.verify_media_source(Intents.printintent, media_source)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A2_150_L_jpg_then_succeeds_8
        +guid:d4f75e96-6461-4529-9145-2da2389072f5
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A2_150_L_jpg_then_succeeds_3(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        self.print.raw.start('5d3834edeb0fe10dc8a3f6efe0f775f1ca834efbaa6c1e774bb9b7f69534c1df')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.verify_media_source(Intents.printintent, media_source)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A2_150_L_jpg_then_succeeds_8
        +guid:3639d7d8-711f-41b6-914d-582d513df19b
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A2_150_L_jpg_then_succeeds_4(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        self.print.raw.start('0c3df6b2d0193e7a5513153c1c9c4302d17b07e27954d905e5e7e158e7a2b387')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.verify_media_source(Intents.printintent, media_source)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A2_150_L_jpg_then_succeeds_8
        +guid:42d6e855-85eb-44ff-b622-24870ec6f9fb
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A2_150_L_jpg_then_succeeds_5(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        self.print.raw.start('dd8e1d2006c6aa7b9fb430afe9c86f8b613b7b668e44bf78b1639a94a1d747a9')
        self.print.wait_for_job_completion()
        outputverifier.save_and_parse_output()

        expected_media_size = MediaSize.letter
        # expecting large media sizes to be printed on rolls
        if tray.rolls is not None:
            expected_media_size = MediaSize.custom
            job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
            autorotate_enabled = outputverifier.get_intent(Intents.printintent)[0].autorotate_enable
            #verify a2 dimensions
            expected_width = round(A2_WIDTH_IN_INCH * job_resolution)
            expected_height = round(A2_HEIGHT_IN_INCH * job_resolution)
            if autorotate_enabled:
                expected_height, expected_width = expected_width, expected_height

            outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
            outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A2_150_L_jpg_then_succeeds_8
        +guid:704e6657-d22f-4854-830d-7f8646e5d6c8
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A2_150_L_jpg_then_succeeds_6(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        self.print.raw.start('2434111e88da7bf86923ededbe8bab58f445c57573a70d149f51e8c4b84b5d55')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.verify_media_source(Intents.printintent, media_source)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A2_150_L_jpg_then_succeeds_8
        +guid:c34a8bbd-1557-4efb-bdaa-07e9e7441528
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A2_150_L_jpg_then_succeeds_7(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        self.print.raw.start('4586844286746a4283fb829956e33d39452f64c977f7516614818926cc42bf07')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.verify_media_source(Intents.printintent, media_source)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A2_150_L_jpg_then_succeeds_8
        +guid:62d2ce33-23ad-48d8-8688-f3d9de5a9cf4
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A2_150_L_jpg_then_succeeds_8(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        self.print.raw.start('2f75e1aa07692c43d6e4de5a0fab8bab6e85bac95689caa2a42143c4292656f7')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.verify_media_source(Intents.printintent, media_source)
        outputverifier.self.outputsaver.operation_mode('NONE')
