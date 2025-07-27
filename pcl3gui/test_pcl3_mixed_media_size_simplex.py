import pytest
import logging

from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of PCL3GUI file mixed_page_size_simplex.pcl
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-150896
    +timeout:500
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:mixed_page_size_simplex.pcl=51f63659cec5a0d8c3b93c64d21a8cae8b8f88f6aa5020f6fa782a861f284b70
    +test_classification:System
    +name:test_pcl3_mixed_media_size_simplex
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3_mixed_media_size_simplex
        +guid:3caf9946-9fe3-46d8-a34e-81af000e0677
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL3GUI & PrintEngineFormat=A0

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl3_mixed_media_size_simplex(setup_teardown, printjob, outputsaver, tray, outputverifier, configuration):
    # Adding the metadata PrintEngineFormat=A0 to run on large fomrat devices that have roll media support.
    # This is mainly done to avoid running on devices like Moreto, MarconiHiPDL etc. which also have PCL3GUI support.

    printjob.print_verify('51f63659cec5a0d8c3b93c64d21a8cae8b8f88f6aa5020f6fa782a861f284b70',timeout=500)
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 4)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    if configuration.familyname != "designjet":
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
