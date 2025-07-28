import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **A5_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A5_Mono_600.urf=d31ef931188041d2c7a93d823b704d0d88fb318106ef85487838b15cc1eeebca
    +name:test_urf_a5_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a5_mono_600
        +guid:a4cdbdba-18b4-414c-9317-7b5bd33f885b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_a5_148x210mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a5_mono_600(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a5_148x210mm', default):
        tray.configure_tray(default, 'iso_a5_148x210mm', 'stationery')

    printjob.print_verify('d31ef931188041d2c7a93d823b704d0d88fb318106ef85487838b15cc1eeebca')
    outputsaver.save_output()
    tray.reset_trays()
