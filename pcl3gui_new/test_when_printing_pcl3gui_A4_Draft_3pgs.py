import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


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
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job of a A4 draft 3-page PCL3GUI file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15284
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:MinumC_A4_P_FD_3pgs.pcl=96d3cab1cd5359404517a12076f2ad8613e4ecea8b071062905785af40e8edce
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_A4_Draft_3pgs_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3gui_A4_draft_3pgs
            +guid:b21bd767-6d4d-4032-b503-2322e4ff2bc3
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl3gui_A4_Draft_3pgs_file_then_succeeds(self):
        self.media.tray.reset_trays()

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('96d3cab1cd5359404517a12076f2ad8613e4ecea8b071062905785af40e8edce')

        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()

        logging.info("PCL3GUI A4 draft 3-pagecompleted successfully")
