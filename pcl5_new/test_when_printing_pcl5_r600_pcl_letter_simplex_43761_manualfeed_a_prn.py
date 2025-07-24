import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from time import sleep


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
        +purpose:Adding new system tests for PCL5 missing coverage
        +test_tier:1
        +is_manual:False
        +test_classification:1
        +reqid:DUNE-197464
        +timeout:240
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:R600_pcl_letter_Simplex_43761-Manualfeed_a.prn=1969fa9cbf3b1882b73456c9d013270c534d1938f9ff072268716f8d0499d4cf
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_r600_pcl_letter_simplex_43761_manualfeed_a_prn_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl5_r600_pcl_letter_simplex_43761_manualfeed_a_prn
            +guid:01ecdde0-0438-4bcc-b6f2-6482ddbfebe0
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCL5 & MediaInputInstalled=ManualFeed
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_r600_pcl_letter_simplex_43761_manualfeed_a_prn_file_then_succeeds(self):
        default = self.media.get_default_source()
        jobid = self.print.raw.start("1969fa9cbf3b1882b73456c9d013270c534d1938f9ff072268716f8d0499d4cf")

        media.wait_for_alerts('mediaManualLoadFlow')
        self.media.tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
        tray.load_media(default)
        sleep(5)
        printjob.wait_verify_job_completion(jobid)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
