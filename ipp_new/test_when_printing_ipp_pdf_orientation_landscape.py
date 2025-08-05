import logging

from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

class TestWhenPrintingFileFromIPP(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""
        # no-op unless the legacy file had a matching teardown
        pass

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
        self.media.reset_inputs()

        tear_down_output_saver(self.outputsaver)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:C51669439 IPP test for printing a pdf file using attribute value orientation_landscape
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:180
            +asset:PDL_New
            +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pdf_orientation_landscape_file_then_succeeds
        +test:
            +title:test_ipp_pdf_orientation_landscape
                    +guid:23c54e1b-17fd-417e-ab5a-6611e6cc8110
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PDF & PrintProtocols=IPP
        +overrides:
            +Home:
                +is_manual:False
                +timeout:300
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pdf_orientation_landscape_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_file = self.print.ipp.generate_test_file_path()
        job_id = self.print.ipp.start(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
        self.print.wait_for_job_completion(job_id)
