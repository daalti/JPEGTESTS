import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 job with landscape orientation in late rotation support product
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-188868
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:test_pcl5_orientation_landscape.prn=ecca56a0ced0e36a48c8498f152a1db77f3c3cfc84e47531c731637c39fa943c
    +test_classification:System
    +name: test_pcl5_1page_landscape_job
    +test:
        +title: test_pcl5_1page_landscape_job
        +guid:ed9d1b7e-5a30-486a-93f0-7a8e880a37aa
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_1page_landscape_job(setup_teardown, printjob,udw,outputsaver, outputverifier):
    printjob.print_verify('ecca56a0ced0e36a48c8498f152a1db77f3c3cfc84e47531c731637c39fa943c')
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
