import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

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
    $$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job of PCL3GUI file mixed_page_size_simplex.pcl
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-150896
        +timeout:500
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:mixed_page_size_simplex.pcl=51f63659cec5a0d8c3b93c64d21a8cae8b8f88f6aa5020f6fa782a861f284b70
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3_mixed_media_size_simplex_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3_mixed_media_size_simplex
            +guid:62ef9670-5b6e-41f0-a364-5c6fa2e2893a
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCL3GUI & PrintEngineFormat=A0
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3_mixed_media_size_simplex_file_then_succeeds(self):
        # Adding the metadata PrintEngineFormat=A0 to run on large fomrat devices that have roll media support.
        # This is mainly done to avoid running on devices like Moreto, MarconiHiPDL etc. which also have PCL3GUI support.

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('51f63659cec5a0d8c3b93c64d21a8cae8b8f88f6aa5020f6fa782a861f284b70')

        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 4)
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
        if configuration.familyname != "designjet":
            outputverifier.verify_plex(Intents.printintent, Plex.simplex)
