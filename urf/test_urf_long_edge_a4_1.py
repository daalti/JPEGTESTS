import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Long-Edge-A4_1.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Long-Edge-A4_1.urf=a80deb51d59072964d865a32d070a3eef1657ec459bdaf2d665024ce1bcee396
    +name:test_urf_long_edge_a4_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_long_edge_a4_1
        +guid:e384b54a-310c-4943-9aee-95de5c8508ac
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_long_edge_a4_1(setup_teardown, printjob, outputsaver, tray):
    outputsaver.operation_mode('TIFF')

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('a80deb51d59072964d865a32d070a3eef1657ec459bdaf2d665024ce1bcee396')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
