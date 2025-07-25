from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.cdm import get_cdm_instance
from dunetuf.metadata import get_ip
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
 
 
 
class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)

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
        +purpose:Event code via JPEG verysmall.jpg file
        +test_tier: 1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-24060
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:verysmall.jpg=fc878bdbba4f8f6d58eaa76d28459fbbe4ef400a43eb85f43933245c3271a163
        +name:TestWhenPrintingJPEGFile::test_when_using_very_small_file_then_success_and_zero_warning_F0_01_08_1B_code
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_pdlmh_printableheight_zero
            +guid:a0e13168-7964-4f87-8609-8219ef68715f
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=JPEG & EngineFirmwareFamily=Canon
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_very_small_file_then_success_and_zero_warning_F0_01_08_1B_code(self):

        job_id = self.print.raw.start('fc878bdbba4f8f6d58eaa76d28459fbbe4ef400a43eb85f43933245c3271a163')
        self.print.wait_for_job_completion(job_id)
        event_code = "F0.01.08.1B"
        response = self.cdm.get_raw(self.cdm.WARNING_EVENT_LOG_ENDPOINT)
        warning_events = response.json().get("events", [])

        event_found = False

        if warning_events is None:
            print("Test Failed: Event code not found.")

        for event in warning_events:
            if event.get("eventCode") == event_code:
                event_found = True
                break 

        assert event_found, f"Test Failed: Event code {event_code} not found."
        print("Test Passed: Event code found.")