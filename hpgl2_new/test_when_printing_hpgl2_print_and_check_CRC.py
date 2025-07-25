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
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: Print job file bolly.wood_fastOFF_150_18x25 and check CRC
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-5786
        +timeout:350
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ProductQA
        +test_framework:TUF
        +external_files:bolly.wood_fastOFF_150_18x25.hpgl2=26a6e9e184d4857fb9a798d433c5c246c452337ab40accd9d864fdd512b0f3d5
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_hpgl2_print_and_check_CRC_file_then_succeeds
        +test:
            +title:test_hpgl2_print_and_check_CRC
            +guid:ecaac291-e852-4d9e-8373-c8205bcf1b85
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=HPGL2
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_hpgl2_print_and_check_CRC_file_then_succeeds(self):
        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')
        job_id = self.print.raw.start('26a6e9e184d4857fb9a798d433c5c246c452337ab40accd9d864fdd512b0f3d5')
        self.print.wait_for_job_completion(job_id)
        logging.info("HPGL2 bolly.wood_fastOFF_150_18x25.hpgl2 - Print job completed successfully")

        if self.outputsaver.configuration.productname == "jupiter":
            crc_expected = ["0xa499de78"]
        elif self.outputsaver.configuration.productname.startswith("flare") or self.outputsaver.configuration.productname.startswith("beam"):
            crc_expected = ["0x5f9f981e"]
        else:
            assert False, f"Unsupported productname: {self.outputsaver.configuration.productname}"

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(crc_expected)
        logging.info("HPGL2 bolly.wood_fastOFF_150_18x25.hpgl2 - Checksum(s) verified successfully")

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: Print job file TEST.hpgl2 and check CRC
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-84162
        +timeout:350
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ProductQA
        +test_framework:TUF
        +external_files:TEST.hpgl2=db4c3bb79af4c432d7cc053df0166fd1f9b74bf394e254d604f07b6afe90022b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_cals_print_and_check_CRC_file_then_succeeds
        +test:
            +title:test_cals_print_and_check_CRC
            +guid:78e75e79-3235-4539-a46d-7a88ceb8a5c5
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=HPGL2
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_cals_print_and_check_CRC_file_then_succeeds(self):
        self.outputsaver.operation_mode('CRC')
        job_id = self.print.raw.start('db4c3bb79af4c432d7cc053df0166fd1f9b74bf394e254d604f07b6afe90022b')
        self.print.wait_for_job_completion(job_id)

        if self.outputsaver.configuration.productname == "jupiter":
            crc_expected = ["0x95b92559"]
        else:
            crc_expected = ["0x3b6f9d3e"]
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(crc_expected)
