import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding


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
        +purpose: pcl5 job with landscape orientation in late rotation support product
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-188868
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:test_pcl5_orientation_landscape.prn=ecca56a0ced0e36a48c8498f152a1db77f3c3cfc84e47531c731637c39fa943c
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_1page_landscape_job_file_then_succeeds
        +test:
            +title: test_pcl5_1page_landscape_job
            +guid:22ac3b86-0566-4387-b887-51055e729c21
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_1page_landscape_job_file_then_succeeds(self):
        job_id = self.print.raw.start('ecca56a0ced0e36a48c8498f152a1db77f3c3cfc84e47531c731637c39fa943c')
        self.print.wait_for_job_completion(job_id)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
