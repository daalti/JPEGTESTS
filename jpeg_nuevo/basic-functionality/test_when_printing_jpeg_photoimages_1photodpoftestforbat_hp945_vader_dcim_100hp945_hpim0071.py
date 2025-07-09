import pytest
import logging
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver


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
    +purpose:simple print job of jpeg file of photoimages 1photodpoftestforbatm hp945 vader dcim 100hp945 hpim0071
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_1PhotoDPOFTestforBAT_hp945_Vader_DCIM_100HP945_HPIM0071.JPG=34d2105b65aaea33b7ab03e50e51f9a756f6d160514c26903c4595054d0efa62
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_photoimages_1PhotoDPOFTestforBAT_hp945_Vader_DCIM_100HP945_HPIM0071_JPG_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_photoimages_1PhotoDPOFTestforBAT_hp945_Vader_DCIM_100HP945_HPIM0071_JPG_then_succeeds
        +guid:1344c493-608a-4535-b74e-53b41103b73a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_1PhotoDPOFTestforBAT_hp945_Vader_DCIM_100HP945_HPIM0071_JPG_then_succeeds(self):

        self.print.raw.start('34d2105b65aaea33b7ab03e50e51f9a756f6d160514c26903c4595054d0efa62')
        self.print.wait_for_job_completion()
        self.outputsaver.save_output()

        logging.info("Jpeg file example photoimages 1PhotoDPOFTestforBAT hp945 Vader DCIM 100HP945 HPIM0071 - Print job completed successfully")
