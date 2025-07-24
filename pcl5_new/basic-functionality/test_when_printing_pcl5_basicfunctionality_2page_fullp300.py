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
            +purpose: pcl5 basicfunctionality using 2Page_fullp300.obj
            +test_tier: 1
            +is_manual: False
            +test_classification: 1
            +reqid: DUNE-37356
            +timeout:240
            +asset:PDL_New
            +delivery_team:QualityGuild
            +feature_team:PDLSolns
            +test_framework: TUF
            +external_files:2Page-fullp300.obj=10d382ba3e17406afec85c76bd74fdaea565782f0ab1114d7c4049c1408ea661
            +test_classification:System
            +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_basicfunctionality_2page_fullp300_file_then_succeeds
            +categorization:
                +segment:Platform
                +area:Print
                +feature:PDL
                +sub_feature:PCL5
                +interaction:Headless
                +test_type:Positive
            +test:
                +title: test_pcl5_basicfunctionality_2page_fullp300
                +guid:e5f8f8f6-12e4-4efe-9324-3c1c945cb1f2
                +dut:
                    +type:Simulator
                    +configuration: DocumentFormat=PCL5
            +overrides:
                +Enterprise:
                    +is_manual:False
                    +timeout:600
                    +test:
                        +dut:
                            +type:Emulator
        $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_basicfunctionality_2page_fullp300_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        default = self.media.get_default_source()
    
        if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            if self.media.is_size_supported('na_legal_8.5x14in', 'tray-1'):
                self.media.tray.open(tray1)
                self.media.tray.load(tray1, MediaSize.Legal.name, MediaType.Plain.name)
                self.media.tray.close(tray1)
        else:
            if self.media.is_size_supported('na_legal_8.5x14in', default):
                self.media.tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')
    
        job_id = self.print.raw.start('10d382ba3e17406afec85c76bd74fdaea565782f0ab1114d7c4049c1408ea661')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
