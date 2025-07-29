import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
import time

collate = "uncollated"
colorMode = "color"
copies = 1
mediaSource = "auto"
mediaSize = "custom"
mediaType = "custom"
plexMode =  "simplex"
duplexBinding = "oneSided"
printQuality = "normal"

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
        +purpose: Simple print from a rasterstream (.rs) file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-14986
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:a3.rs=b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_a3_checking_job_ticket_file_then_succeeds
        +test:
            +title:test_rs_a3_checking_job_ticket
            +guid:f59b4e57-a086-4833-af05-00440f192692
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=RasterStreamICF
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_a3_checking_job_ticket_file_then_succeeds(self):
        # Start the print job
        job_id = self.print.raw.start('b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617')
        self.print.wait_for_job_completion(job_id)

        # Wait until the job end without problems
        job.wait_for_job_completion_cdm(jobid, timeout=700)

        # Get the ticket
        job_queue = cdm.get("/cdm/jobManagement/v1/history")
        links = {key:value for (key,value) in job_queue["jobList"][-1].items() if key == "links"}
        cdm_ticket = [x["href"] for x in links["links"] if x["rel"] == "jobTicket"]

        # Getting the information of the ticket
        job_ticket = cdm.get(cdm_ticket[0])

        is_simulator = udw.mainUiApp.ControlPanel.isSimulator()
        if not is_simulator:
            global mediaType
            mediaType = "stationery"

        check_job_ticket(job_ticket)

        self.outputsaver.save_output()


def check_job_ticket(ticket):

    assert ticket["dest"]["print"]["collate"] == collate
    assert ticket["dest"]["print"]["colorMode"] == colorMode
    assert ticket["dest"]["print"]["copies"] == copies
    assert ticket["dest"]["print"]["mediaSource"] == mediaSource
    assert ticket["dest"]["print"]["mediaSize"] == mediaSize
    assert ticket["dest"]["print"]["mediaType"] == mediaType
    assert ticket["dest"]["print"]["plexMode"] == plexMode
    assert ticket["dest"]["print"]["printQuality"] == printQuality
