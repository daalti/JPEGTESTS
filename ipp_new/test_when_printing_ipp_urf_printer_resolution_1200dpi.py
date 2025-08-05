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
        +purpose:C51669447 Ipp test for printing a URF file using attribute value printer-resolution_1200dpi
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-47064
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A4_Color_600.urf=2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_urf_printer_resolution_1200dpi_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_urf_printer_resolution_1200dpi
            +guid:d469d8e3-a681-48da-948c-a604cccd7293
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & PrintProtocols=IPP & PrintResolution=Print1200
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_urf_printer_resolution_1200dpi_file_then_succeeds(self):
        ipp_test_attribs = {}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)

        job_id = self.print.ipp.start(ipp_test_file, '2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
