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
        +purpose: IPP test for printing a document from mac and using attribute value media type heavyglossy and media size Letter
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-124180
        +timeout:240
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:jpeg_vnd_landscape_photo.bin=94ad1df3591e7534f52c1ba7b471b592c139a15ee89a3c7ddba94455c008fedb
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_pdl_airprint_mac_mediasize_letter_heavyglossy_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_airprint_mac_mediasize_letter_heavyglossy
            +guid:22fe9b48-d832-4eae-a68f-541f8fe9504c
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & Print=Best & MediaInputInstalled=Tray1 & MediaType=HeavyGlossy111-130g
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_airprint_mac_mediasize_letter_heavyglossy_file_then_succeeds(self):
        ipp_test_attribs = {}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)

        job_id = self.print.ipp.start(ipp_test_file, '94ad1df3591e7534f52c1ba7b471b592c139a15ee89a3c7ddba94455c008fedb')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
