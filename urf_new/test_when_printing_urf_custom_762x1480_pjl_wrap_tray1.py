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
        +purpose:Simple print job of Custom 762x1480 PJLWrap Tray1 urf from *Custom_762x1480_PJLWrap_Tray1.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Custom_762x1480_PJLWrap_Tray2.urf=d5cfc4e96b956af45490a1235296dc0b951e16178b93cdfea303278ed00b31ac
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_custom_762x1480_pjl_wrap_tray1_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_custom_762x1480_pjl_wrap_tray1_page
            +guid:c9e5bede-1a2f-4323-be52-4b28088d76c2
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_custom_762x1480_pjl_wrap_tray1_file_then_succeeds(self):

        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('anycustom', default):
            self.media.tray.configure_tray(default, 'anycustom', 'stationery')
        else:
            self.media.tray.configure_tray(default, 'custom', 'stationery')

        job_id = self.print.raw.start('d5cfc4e96b956af45490a1235296dc0b951e16178b93cdfea303278ed00b31ac')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()

        logging.info("URF Custom 762x1480 PJLWrap Tray1 page - Print job completed successfully")
