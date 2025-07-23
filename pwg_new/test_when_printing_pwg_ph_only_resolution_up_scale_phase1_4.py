
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

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
        tear_down_output_saver(self.outputsaver)

"""$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only resolution up scale phase1-4 from *PwgPhOnly-ResUpScalePhase1-4.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-ResUpScalePhase1-4.pwg=e12f2e48048fa7b436b47d2c167f05491a1ae96491113a3bc44c98f3e0fa6598
    +name:TestWhenPrintingJPEGFile::test_when_using_pwg_ph_only_resolution_up_scale_phase1_4_file_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_resolution_up_scale_phase1_4_page
        +guid:71b930aa-6e0b-4fd1-9bb7-2d26f4f3ee48
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$"""
    def test_when_using_pwg_ph_only_resolution_up_scale_phase1_4_file_then_succeeds(self):
        job_id = self.print.raw.start('e12f2e48048fa7b436b47d2c167f05491a1ae96491113a3bc44c98f3e0fa6598')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
