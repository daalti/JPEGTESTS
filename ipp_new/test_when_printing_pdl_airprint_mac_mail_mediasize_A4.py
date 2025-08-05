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
        +purpose: IPP test for printing a Email from Mac and using attribute value media size A4
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-124180
        +timeout:240
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:mac_mail.bin=087b82a070ac66ca8cc81aa1f7fc3d7baec41e47a160d58f07232839616dd22f
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_pdl_airprint_mac_mail_mediasize_A4_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_airprint_mac_mail_mediasize_A4
            +guid:e64393b2-b7b1-46dd-8b37-c5b99d951c7f
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & Print=Normal & Duplexer=True & MediaInputInstalled=Tray1
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_airprint_mac_mail_mediasize_A4_file_then_succeeds(self):
        ipp_test_attribs = {}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)

        job_id = self.print.ipp.start(ipp_test_file, '087b82a070ac66ca8cc81aa1f7fc3d7baec41e47a160d58f07232839616dd22f')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
