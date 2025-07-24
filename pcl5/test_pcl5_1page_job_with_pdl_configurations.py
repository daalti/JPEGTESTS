import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 job using pdl configurations from job overidding front panel
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-94044
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:test_pcl5_withPdlConfigurations.prn=edea21fe4183c8973e6d679560175ce675ab259cd7a93810fec0736e3d704293
    +test_classification:System
    +name: test_pcl5_1page_job_with_pdl_configurations
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_1page_job_with_pdl_configurations
        +guid:eec75068-549b-48b0-8e4b-673fd1a0dbe7
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

def test_pcl5_1page_job_with_pdl_configurations(setup_teardown, printjob,udw,outputsaver, outputverifier):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('edea21fe4183c8973e6d679560175ce675ab259cd7a93810fec0736e3d704293')
    outputverifier.save_and_parse_output()
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')

    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
