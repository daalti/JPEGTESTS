import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 job with landscape orientation in late rotation support product
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-196321
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:2pgs_Letter_Plain_PUNCH_LEFT_2PT_US_engT1_exB1_for_PAPERSIZEPROBLEM.prn=bbfb00aac7de4e314baf9dc162a1f771fe519d3c513686a27c6bca03d15463d9
    +test_classification:System
    +name: test_pcl5_2pgs_Letter_Plain_Landscape_job
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_2pgs_Letter_Plain_Landscape_job
        +guid:552c6a11-0401-4c88-864a-b3dfd25fdd2a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_2pgs_Letter_Plain_Landscape_job(setup_teardown, printjob,udw,outputsaver, outputverifier):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('bbfb00aac7de4e314baf9dc162a1f771fe519d3c513686a27c6bca03d15463d9')
    outputverifier.save_and_parse_output()
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)


