from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver
from dunetuf.print.output_verifier import OutputVerifier
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, MediaSizeID, get_media_source

A1_WIDTH_IN_INCH = 594000 / 25400
A1_HEIGHT_IN_INCH = 841000 / 25400
class TestWhenPrintingJPEGFile:
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()
        cls.media = Media()
        cls.outputsaver = OutputSaver()
        cls.outputverifier = OutputVerifier(cls.outputsaver)

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
    +purpose:Jpeg test using A1-150-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-150-L.jpg=6b9fb0bfbd3dac81fc5f48347ddd337f30a1ad03e2af9bb541ec251142ca024d
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_A1_150_L_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_A1_150_L_jpg_then_succeeds
        +guid:3690d1a6-2f13-40f1-80cc-e128aab04af9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A1_150_L_jpg_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        self.print.raw.start('6b9fb0bfbd3dac81fc5f48347ddd337f30a1ad03e2af9bb541ec251142ca024d')
        self.print.wait_for_job_completion()
        self.outputverifier.save_and_parse_output()

        expected_media_size = MediaSize.letter
        #expecting large media sizes to be printed on rolls
        if tray.rolls is not None:
            expected_media_size = MediaSize.custom

        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size)

        self.outputverifier.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-231-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-231-L.jpg=0268b87aa87b04ac03087e8c414f083298dc60ffc655882839b25e98702fe906
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_A1_231_L_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_A1_231_L_jpg_then_succeeds
        +guid:d64580ce-20a5-43ab-8dce-1c6c53cc8c69
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A1_231_L_jpg_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        self.print.raw.start('0268b87aa87b04ac03087e8c414f083298dc60ffc655882839b25e98702fe906')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        self.outputverifier.verify_media_source(Intents.printintent, media_source)
        self.outputverifier.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-600-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-600-L.jpg=c4ec10f90c24466ce65a838d090a7297d47b83cc1b287b22a7ba468392983ce2
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_A1_600_L_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_A1_600_L_jpg_then_succeeds
        +guid:afd50e49-80ed-492b-9262-fd26a5eb657e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A1_600_L_jpg_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        self.print.raw.start('c4ec10f90c24466ce65a838d090a7297d47b83cc1b287b22a7ba468392983ce2')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        self.outputverifier.verify_media_source(Intents.printintent, media_source)
        self.outputverifier.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-150-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-150-P.jpg=4fa0a710aa32e40d244748ff4ffd60c3d1d440d31003ad5c898c0c93f1aab914
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_A1_150_P_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_A1_150_P_jpg_then_succeeds
        +guid:60e331b5-72f6-4ab0-abe7-c997f5a2d51a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A1_150_P_jpg_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        self.print.raw.start('4fa0a710aa32e40d244748ff4ffd60c3d1d440d31003ad5c898c0c93f1aab914')
        self.print.wait_for_job_completion()
        self.outputverifier.save_and_parse_output()
        expected_media_size = MediaSize.letter
        # expecting large media sizes to be printed on rolls
        if tray.rolls is not None:
            expected_media_size = MediaSize.custom
            job_resolution = self.outputverifier.get_intent(Intents.printintent)[0].resolution
            autorotate_enabled = self.outputverifier.get_intent(Intents.printintent)[0].autorotate_enable
            # verify A1 dimensions
            expected_width = round(A1_WIDTH_IN_INCH * job_resolution)
            expected_height = round(A1_HEIGHT_IN_INCH * job_resolution)

            if autorotate_enabled:
                expected_height, expected_width = expected_width, expected_height

            self.outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
            self.outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        self.outputverifier.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-231-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-231-P.jpg=9c3125a439ca88db6e0df33be1cbb786ad07e320e6c1a3a02876f614baf1a89c
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_A1_231_P_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_A1_231_P_jpg_then_succeeds
        +guid:c310a4c3-7f48-4c54-99ab-4152c5725c73
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A1_231_P_jpg_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        self.print.raw.start('9c3125a439ca88db6e0df33be1cbb786ad07e320e6c1a3a02876f614baf1a89c')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        self.outputverifier.verify_media_source(Intents.printintent, media_source)
        self.outputverifier.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-300-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-300-P.jpg=c00d2dfa17efe5d98c11979cdbc18b514f04d4462cd3fe79eeecfcb107d94e22
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_A1_300_P_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_A1_300_P_jpg_then_succeeds
        +guid:e2662d99-8aab-4858-9a38-5a534c572b25
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A1_300_P_jpg_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        self.print.raw.start('c00d2dfa17efe5d98c11979cdbc18b514f04d4462cd3fe79eeecfcb107d94e22')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        self.outputverifier.verify_media_source(Intents.printintent, media_source)
        self.outputverifier.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-600-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-600-P.jpg=194d330ac173675bf2b0e445cc1a42971bc90cf67fb7503d0d860938680dc75f
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_A1_600_P_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_A1_600_P_jpg_then_succeeds
        +guid:17ae7ea3-0611-4c43-8945-48956d9c3758
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A1_600_P_jpg_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        self.print.raw.start('194d330ac173675bf2b0e445cc1a42971bc90cf67fb7503d0d860938680dc75f')
        self.print.wait_for_job_completion()

        media_source = get_media_source(tray.rolls[0])

        self.outputverifier.save_and_parse_output()
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        self.outputverifier.verify_media_source(Intents.printintent, media_source)
        self.outputverifier.outputsaver.operation_mode('NONE')




    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-72-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-72-P.jpg=546bd634cfc1d42f3a3f2cb2067061599d02f89fc07e0f8e9b9f98eba977c760
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_A1_72_P_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_A1_72_P_jpg_then_succeeds
        +guid:32d0135a-74ea-49d1-9302-58d103880125
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_A1_72_P_jpg_then_succeeds(self):

        self.outputverifier.outputsaver.operation_mode('TIFF')

        self.print.raw.start('546bd634cfc1d42f3a3f2cb2067061599d02f89fc07e0f8e9b9f98eba977c760')
        self.print.wait_for_job_completion()
        self.outputverifier.save_and_parse_output()

        expected_media_size = MediaSize.letter
        if tray.rolls is not None:
            expected_media_size = MediaSize.custom
            job_resolution = self.outputverifier.get_intent(Intents.printintent)[0].resolution
            autorotate_enabled = self.outputverifier.get_intent(Intents.printintent)[0].autorotate_enable
            # verify A1 dimensions
            expected_width = round(A1_WIDTH_IN_INCH * job_resolution)
            expected_height = round(A1_HEIGHT_IN_INCH * job_resolution)

            if autorotate_enabled:
                expected_height, expected_width = expected_width, expected_height

            self.outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
            self.outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)


        self.outputverifier.verify_media_size(Intents.printintent, expected_media_size)
        self.outputverifier.outputsaver.operation_mode('NONE')
