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
        +purpose: IPP test for printing a pdf file using attribute value sides_two_sided_long_edge
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-129624
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_pdl_intent_ipp_pdf_sides_two_sided_long_edge_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PDF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_ipp_pdf_sides_two_sided_long_edge
            +guid:8207cde2-7336-4237-b79f-1a9dc998589a
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PDF & PrintProtocols=IPP & Duplexer=True & MediaSizeSupported=na_letter_8.5x11in & MediaInputInstalled=Tray2
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_ipp_pdf_sides_two_sided_long_edge_file_then_succeeds(self):
        ipp_test_attribs = {}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)

        job_id = self.print.ipp.start(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
