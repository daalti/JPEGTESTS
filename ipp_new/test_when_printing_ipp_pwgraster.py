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

        +purpose:ipp test for 1page letter sgray 8 300dpi
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-47064
        +timeout:180
            +asset:PDL_New
            +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:onepage-letter-sgray-8-300dpi.pwg=c1e5b49ce2c26854bae86cb347e19eaa8a722db01d49fe57f90c5b38787cd3ef
        +test_classification:System
            +name:TestWhenPrintingIPPFile::test_when_using_ipp_pwgraster_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PWGRaster
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_pwg_1page_letter_sgray_8_300dpi
                +guid:189593ad-11f8-4377-b83e-c5d2a339f858
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pwgraster_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_file = self.print.ipp.generate_test_file_path()
        job_id = self.print.ipp.start(ipp_test_file, 'c1e5b49ce2c26854bae86cb347e19eaa8a722db01d49fe57f90c5b38787cd3ef')
        self.print.wait_for_job_completion(job_id)
