import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 job using default pdl configurations from front panel
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-94044
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:test_pcl5_withoutPdlConfigurations.prn=9bb630ac7c088eb5ea4d99a98e021f3419386831cd5db73991e3bf321a69953a
    +test_classification:System
    +name: test_pcl5_1page_job_without_pdl_configurations
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_1page_job_without_pdl_configurations
        +guid:18306ae3-7a35-44d5-bd3b-f0889bf90590
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

def test_pcl5_1page_job_without_pdl_configurations(setup_teardown, printjob,udw,outputsaver, outputverifier):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('9bb630ac7c088eb5ea4d99a98e021f3419386831cd5db73991e3bf321a69953a')
    outputverifier.save_and_parse_output()
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')

    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
