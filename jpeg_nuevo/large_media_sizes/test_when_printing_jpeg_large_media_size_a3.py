from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, get_media_source


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
    +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_8
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

        outputverifier.self.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default = tray.get_default_source()
        if tray.is_size_supported('iso_a3_297x420mm', default):
            tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('44f6cf3630ed32881134bea9153428d57c69fde0efbe38da68a24e95ff2c68dc')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_8
        +guid:23664a85-3878-4388-884e-2b6d7fe45d10
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds_2(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default = tray.get_default_source()
        if tray.is_size_supported('iso_a3_297x420mm', default):
            tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('98a7b77efdee8efca9bc37d2f93b6b081e78d7aa3d13ccea2260e25ef1eee317')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_8
        +guid:db63ab21-43c0-4819-80c2-93f10622470b
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds_3(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        job_id = self.print.raw.start('d7d4d21b5d1b3269b57c3208c0e3272b162c439b1a9a40dd01981358dcd2eb62')
        self.print.wait_for_job_completion(job_id)

        media_source = get_media_source(tray.rolls[0])

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.verify_media_source(Intents.printintent, media_source)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_8
        +guid:76a8391b-a1ed-4ce4-acc7-6ccaeb8e825e
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds_4(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        job_id = self.print.raw.start('5ecd428b320c23d6f899cb26277f73ffbfdee376ad8625d1189ca6eff6140013')
        self.print.wait_for_job_completion(job_id)

        media_source = get_media_source(tray.rolls[0])

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.verify_media_source(Intents.printintent, media_source)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_8
        +guid:2fafe0b2-4e0f-4b15-9d1a-317596055456
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds_5(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default = tray.get_default_source()
        if tray.is_size_supported('iso_a3_297x420mm', default):
            tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('52e22db4d0237e6cf053a243d10b49e773ca4a0e5dbc5ebae3f48c8e87cefeba')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_8
        +guid:69ec5c9b-3b86-4ca7-bda9-e0660b1c1cc6
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds_6(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default = tray.get_default_source()
        if tray.is_size_supported('iso_a3_297x420mm', default):
            tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('8b9f79cd74a56bb19019053cd9500429069e2afa20932b0aad2acbb11c49a30e')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_8
        +guid:a59ac9b0-5874-4f02-b77f-245943828fe0
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds_7(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default = tray.get_default_source()
        if tray.is_size_supported('iso_a3_297x420mm', default):
            tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('93caf9440369f33424aaeebe4c1238e86c29625d08e1cef696d837aad108bbc7')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +asset:PDL_New
        +delivery_team:QualityGuild
        +name:TestWhenPrintingJPEGFile::test_when_A3_150_L_jpg_then_succeeds_8
        +guid:70154fb5-26a4-4bdc-86d7-d8420fbda99b
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A3_150_L_jpg_then_succeeds_8(self):

        outputverifier.self.outputsaver.operation_mode('TIFF')

        expected_media_size = MediaSize.letter

        default = tray.get_default_source()
        if tray.is_size_supported('iso_a3_297x420mm', default):
            tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
            expected_media_size = MediaSize.a3

        job_id = self.print.raw.start('d93ee93e25e90f605960ba6df9fd3ea2e0b0b733c5bfabebfa8a202b4fa771d2')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        outputverifier.self.outputsaver.operation_mode('NONE')
