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
        +purpose: IPP test for printing a Web Page from Safari and using attribute value mediasize A4
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-124180
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:mac_safari.bin=6296b3512b0ef547d0a8af8a725a04275b31c5522c038ef3ec70eb63fa6904b4
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_pdl_airprint_mac_safari_mediasize_A4_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_airprint_mac_safari_mediasize_A4
            +guid:5f1cfbbe-9495-4d81-9d91-f9b8ef7f6bb5
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & PrintColorMode=BlackOnly & Print=Normal & Duplexer=True & MediaInputInstalled=Tray1
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_airprint_mac_safari_mediasize_A4_file_then_succeeds(self):
        ipp_test_attribs = {}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)

        job_id = self.print.ipp.start(ipp_test_file, '6296b3512b0ef547d0a8af8a725a04275b31c5522c038ef3ec70eb63fa6904b4')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
