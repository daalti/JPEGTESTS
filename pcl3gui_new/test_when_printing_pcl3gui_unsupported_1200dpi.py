import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import MediaType


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
        +purpose:Testing PCL3GUI of unsupported print resolution
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-154408
        +timeout:6000
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Colorwheel1200DPI_withmargins.prn=eb0b8f5835ab0f8eecb47186dfd78c2bee6364288cf1e4abc5aef5cdbaebea19
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_unsupported_1200dpi_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3gui_unsupported_1200dpi_beam
            +guid:d16e7674-a48f-4cd4-896e-1c02193f0a62
            +dut:
                +type:Simulator
                +configuration:DeviceClass=LFP & DocumentFormat=PCL3GUI & EngineFirmwareFamily=DoX
            
        
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    # NOTE: Need a different test for Beam because CRC differs due to scaling missalignmet from 32 vs 64 bits computation
    def test_when_using_pcl3gui_unsupported_1200dpi_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        printjob.print_verify_multi('eb0b8f5835ab0f8eecb47186dfd78c2bee6364288cf1e4abc5aef5cdbaebea19','SUCCESS', 1, 6000)
        logging.info("Colorwheel1200DPI - Print job completed successfully")

        # Read and verify that obtained checksums are the expected ones
        expected_crc = ["0x85124cc4"]
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("Colorwheel1200DPI - Checksum(s) verified successfully")


    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
            +purpose:Testing PCL3GUI of unsupported print resolution on Jupiter
            +test_tier:1
            +is_manual:False
            +reqid:DUNE-154408
            +timeout:6000
            +asset:PDL_Print
            +delivery_team:PDLJobPQ
            +feature_team:PDLSolns
            +test_framework:TUF
            +external_files:Colorwheel1200DPI_withmargins.prn=eb0b8f5835ab0f8eecb47186dfd78c2bee6364288cf1e4abc5aef5cdbaebea19
            +test_classification:System
            +name:test_pcl3gui_unsupported_1200dpi_jupiter
            +categorization:
                +segment:Platform
                +area:Print
                +feature:PDL
                +sub_feature:PCL3GUI
                +interaction:Headless
                +test_type:Positive
            +test:
                +title:test_pcl3gui_unsupported_1200dpi_jupiter
                +guid:795f124f-1346-48c1-b5dc-b4a9a5d760ad
                +dut:
                    +type:Simulator
                    +configuration:DeviceClass=LFP & DocumentFormat=PCL3GUI & EngineFirmwareFamily=Maia
                
            
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
        """
    # NOTE: Need a different test for Jupiter because CRC differs due to scaling missalignmet from 32 vs 64 bits computation
    def test_when_using_pcl3gui_unsupported_1200dpi_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        printjob.print_verify_multi('eb0b8f5835ab0f8eecb47186dfd78c2bee6364288cf1e4abc5aef5cdbaebea19','SUCCESS', 1, 6000)
        logging.info("Colorwheel1200DPI - Print job completed successfully")

        # Read and verify that obtained checksums are the expected ones
        expected_crc = ["0x93777e48"]
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("Colorwheel1200DPI - Checksum(s) verified successfully")

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
            +purpose:Testing PCL3GUI of unsupported print resolution on Jupiter
            +test_tier:1
            +is_manual:False
            +reqid:DUNE-259375
            +timeout:300
            +asset:PDL_Print
            +delivery_team:PDLJobPQ
            +feature_team:PDLSolns
            +test_framework:TUF
            +external_files:OutPut.prn=a2ce1494ee95a4a029baa5f8f5194a05b7991248184eff921a7dc9fd5f3ce966
            +test_classification:System
            +name:test_pcl3gui_unsupported_media_type_1200dpi_jupiter
            +categorization:
                +segment:Platform
                +area:Print
                +feature:PDL
                +sub_feature:PCL3GUI
                +interaction:Headless
                +test_type:Positive
            +test:
                +title:test_pcl3gui_unsupported_media_type_1200dpi_jupiter
                +guid:2b0724c0-ac87-4bea-9a08-2a4c5788ecfd
                +dut:
                    +type:Simulator
                    +configuration:DeviceClass=LFP & DocumentFormat=PCL3GUI & MediaInputInstalled=ROLL1
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
        """
    def test_when_using_pcl3gui_unsupported_1200dpi_file_then_succeeds(self):

        if self.media.tray.is_type_supported(MediaType.photographicglossy, 'roll-1'):
            self.media.tray.configure_tray('roll-1', 'custom', MediaType.photographicglossy)

        ipp_test_attribs = {
            'document-format': 'application/vnd.hp-PCL', 
            'media-bottom-margin': 300, 
            'media-left-margin': 300, 
            'media-right-margin': 300, 
            'media-top-margin': 300, 
            'x-dimension':27940,
            'y-dimension':21590,
            'media-type':'auto',
            'print-quality' : 5,
            'resolution' : '1200x1200dpi',
            'media-source':'roll-1'
        }

        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
        printjob.ipp_print(ipp_test_file, 'a2ce1494ee95a4a029baa5f8f5194a05b7991248184eff921a7dc9fd5f3ce966')
        self.outputsaver.save_output()
