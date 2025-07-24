import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_verifier import OutputVerifier
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
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
        tear_down_output_saver(self.outputsaver)
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:PCL5 high value test using **ptchgmt.cht
        +test_tier: 1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-156300
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework:TUF
        +external_files:ptchgmt.cht=61229fda64e53a2de3d5a8034db5e0917464e4f0d5d163e35f55e602532d1a48
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_conf_hv_ptchgmt_file_then_succeeds
        +test:
            +title:test_pcl5_conf_hv_ptchgmt
            +guid:acffec7f-1bd9-441b-acd0-4388805af68a
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_conf_hv_ptchgmt_file_then_succeeds(self):
        job_id = self.print.raw.start('61229fda64e53a2de3d5a8034db5e0917464e4f0d5d163e35f55e602532d1a48')
        self.print.wait_for_job_completion(job_id)
        # self.outputverifier.save_and_parse_output()
        udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
        if(int(udw_result)):
            job_id = self.print.raw.start('61229fda64e53a2de3d5a8034db5e0917464e4f0d5d163e35f55e602532d1a48')
            self.print.wait_for_job_completion(job_id)
        else:
            job_id = self.print.raw.start('61229fda64e53a2de3d5a8034db5e0917464e4f0d5d163e35f55e602532d1a48')
            self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
