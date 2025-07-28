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
        +purpose:Simple print job of urf B6 Color 600 from *B6_Color_600.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:B6_Color_600.urf=c1bf52be1f1eae402a6a66de224a153e23a2c94067b73d6e90a1abaec36470fb
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_b6_color_600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_b6_color_600_page
            +guid:afb84ada-8721-490e-b65e-45f62904aa8c
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=jis_b6_128x182mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_b6_color_600_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('jis_b6_128x182mm', default):
            self.media.tray.configure_tray(default, 'jis_b6_128x182mm', 'stationery')
        elif self.media.tray.is_size_supported('custom', default):
            self.media.tray.configure_tray(default, 'custom', 'stationery')

        job_id = self.print.raw.start('c1bf52be1f1eae402a6a66de224a153e23a2c94067b73d6e90a1abaec36470fb')
        self.print.wait_for_job_completion(job_id)
        printjob.wait_verify_job_completion(jobid, timeout=120)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
