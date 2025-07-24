import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 job with Font download command support 
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-191473
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files: targetfiles_maser_test.sentry.pcl=7ddc731ae41dde0fd48341f224d1010f4fd20423512d4d250381629734a5b9ca
    +test_classification:System
    +name: test_pcl5_font_download_command
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_font_download_command
        +guid: 8673cc79-b942-4569-9b62-472fa7d2b00e
        +dut:
            +type: Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_font_download_command(setup_teardown, printjob,udw,outputsaver, outputverifier):
    printjob.print_verify('7ddc731ae41dde0fd48341f224d1010f4fd20423512d4d250381629734a5b9ca',expected_job_state='SUCCESS',timeout=600)
    
