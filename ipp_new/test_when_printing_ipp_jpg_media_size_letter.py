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
        +purpose: IPP test for printing a JPG file using attribute value media_size_letter
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-47064
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_jpg_media_size_letter_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_jpg_media_size_letter
            +guid:5501ea19-26b4-496e-8c7e-32e991422b07
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_jpg_media_size_letter_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_attribs = {'document-format': 'image/jpeg', 'media': 'na_letter_8.5x11in'}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)



        job_id = self.print.ipp.start(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
        self.print.wait_for_job_completion(job_id)
        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 1)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

