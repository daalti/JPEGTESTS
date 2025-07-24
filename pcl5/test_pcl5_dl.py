import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:dl.pcl=ebe1f946cda65072265ab698b1be1f0c4c220925a30a52be45d96cd60963e3ed
    +name:test_pcl5_dl
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_dl
        +guid:312fa5ea-9d85-4706-b9e4-daf3d0a696ba
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_dl(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('iso_dl_110x220mm','tray-1'):
        tray.configure_tray('tray-1', 'iso_dl_110x220mm', 'any')
    printjob.print_verify_multi('ebe1f946cda65072265ab698b1be1f0c4c220925a30a52be45d96cd60963e3ed')
    outputsaver.save_output() 