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
        +purpose:Simple print job of a 4x6 photo normal one page PCL3GUI file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15284
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Lily_4x6_HPPhoto_N.pcl=948e77bea01535a5f11cc8ab95ab562a2cb42dcff3d4431fe0fc44bd79ca8ba1
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_4x6_Pht_N_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3gui_4x6_Pht_N
            +guid:58978da9-ac07-470d-b9e2-2f0589ce3684
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI & MediaType=HPPhotoPapers & MediaSizeSupported=na_index-4x6_4x6in
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl3gui_4x6_Pht_N_file_then_succeeds(self):
        default = self.media.tray.get_default_source()

        if self.media.tray.is_media_combination_supported(default, 'na_index-4x6_4x6in', 'com.hp-photographic-glossy'):
            self.media.tray.configure_tray(default, 'na_index-4x6_4x6in', 'com.hp-photographic-glossy')

            self.outputsaver.validate_crc_tiff()

            job_id = self.print.raw.start('948e77bea01535a5f11cc8ab95ab562a2cb42dcff3d4431fe0fc44bd79ca8ba1')

            self.print.wait_for_job_completion(job_id)

            self.outputsaver.save_output()
            self.media.tray.reset_trays()

            logging.info("PCL3GUI 4x6 photo normal one pagecompleted successfully")
        else:
            logging.info("PCL3GUI 4x6 photo normal media combination NOT supported")
