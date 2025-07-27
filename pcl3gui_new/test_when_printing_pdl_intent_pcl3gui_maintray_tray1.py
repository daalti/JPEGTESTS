import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import Intents, MediaSource


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
        +purpose:Simple print job of Pcl3gui and ensure the PDL setting the tray which is installed in the printer
        +test_tier:3
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-145007
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Letter-Plain-Marconi_Hi-tray_1.prn=78f135c0c44424edd57be3c4f5758f628893c7400eab009686f1e7c32268769a
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_pcl3gui_maintray_tray1_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_pcl3gui_maintray_tray1
            +guid:a59f83ed-8ae8-4561-a25a-ad0902f0d92d
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCL3GUI
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pdl_intent_pcl3gui_maintray_tray1_file_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('78f135c0c44424edd57be3c4f5758f628893c7400eab009686f1e7c32268769a')

        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()

        if self.media.tray.is_tray_supported('main'):
            outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
        elif self.media.tray.is_tray_supported('tray-1'):
            outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
        elif self.media.tray.is_tray_supported('main-roll'):
            outputverifier.verify_media_source(Intents.printintent, MediaSource.mainRoll)
        elif self.media.tray.is_tray_supported('roll-1'):
            outputverifier.verify_media_source(Intents.printintent, MediaSource.roll1)
        else :
            assert(0)
        #!!! Or avoid running in jupiter if this is only for tray
        self.media.tray.reset_trays()
        self.outputsaver.save_output()
