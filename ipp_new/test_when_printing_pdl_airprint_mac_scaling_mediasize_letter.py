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
        +purpose: IPP test for printing a pdf file 
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-191063
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Mixed_Page_Size_Region_4p_v3.pdf=e5bc714378e67161a25aa8f23dec3472dc40c5cb70473915bb55cb76e813f662
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_pdl_airprint_mac_scaling_mediasize_letter_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_airprint_mac_scaling_mediasize_letter
            +guid:3d0b83a8-ff52-4890-9e7d-314e57127a64
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & MediaInputInstalled=Tray1
        +overrides:
            +Home:
                +is_manual:False
                +timeout:360
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_airprint_mac_scaling_mediasize_letter_file_then_succeeds(self):
        ipp_test_attribs = {}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)

        job_id = self.print.ipp.start(ipp_test_file, 'e5bc714378e67161a25aa8f23dec3472dc40c5cb70473915bb55cb76e813f662')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
