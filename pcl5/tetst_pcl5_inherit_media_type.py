import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, MediaType, MediaSource


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test for pcl5 for inherit media type from tray functionality
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-13650
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:tray1_a4_notype_pcl5.prn=5ac9906a9fe61f103123109d5b147e5618a7cfd9f7faee8d4a8918849ab98a28
    +test_classification:System
    +name: test_pcl5_inherit_media_type
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_inherit_media_type
        +guid:9a621884-d16e-422d-8f23-2fe1311a8410
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & MediaType=Bond & MediaInputInstalled=Tray1 & MediaSizeSupported=iso_a4_210x297mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_inherit_media_type(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('iso_a4_210x297mm', 'tray-1') and tray.is_type_supported('stationery-bond', 'tray-1'):
        tray.configure_tray('tray-1', 'iso_a4_210x297mm', 'stationery-bond')

    printjob.print_verify('5ac9906a9fe61f103123109d5b147e5618a7cfd9f7faee8d4a8918849ab98a28')
    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    outputverifier.verify_media_type(Intents.printintent, MediaType.bond)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)

    outputsaver.save_output()
    tray.reset_trays()
