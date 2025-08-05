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
        +purpose:C51669540 IPP test for printing a JPG file using attribute value media_size_A4
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:sRGB_A4_600dpi.jpg=86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b
        +test_classification:System    
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_jpg_media_size_a4_file_then_succeeds
        +test:
            +title:test_ipp_jpg_media_size_a4
            +guid:6fce2194-a2d7-4cdd-91ce-f6886b539c28
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & MediaSizeSupported=A4 & PrintProtocols=IPP
        +overrides:
            +Home:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_jpg_media_size_a4_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()

        ipp_test_attribs = {'document-format': 'image/jpeg', 'media-size-name': 'iso_a4_210x297mm'}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)

        job_id = self.print.ipp.start(ipp_test_file, '86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b')
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        logging.info(f"Validate current crc <{Current_crc_value}> with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

