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

        +purpose: IPP test for printing a PWG file using attribute value print_resolution_1200x1200
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-240989
        +timeout:300
            +asset:PDL_New
            +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:renderFile1200DPI.pwg=ae052609931c411c0b472ea4e7a887122a5c45270a61d146e567213a00222a3d
        +test_classification:System
            +name:TestWhenPrintingIPPFile::test_when_using_ipp_pwgraster_print_resolution_1200dpi_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PWGRaster
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_pwgraster_print_resolution_1200dpi
                +guid:481557e4-f8a8-4c77-bfd3-0db92f49ac0b
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & PrintResolution=Print1200 & MediaSizeSupported=iso_a4_210x297mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pwgraster_print_resolution_1200dpi_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_file = self.print.ipp.generate_test_file_path()
        job_id = self.print.ipp.start(ipp_test_file, 'ae052609931c411c0b472ea4e7a887122a5c45270a61d146e567213a00222a3d')
        self.print.wait_for_job_completion(job_id)
