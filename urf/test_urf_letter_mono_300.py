import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Letter_Mono_300.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter_Mono_300.urf=880fc1d0aecef52967afdb68cc3d2f441cf5dde14ba6e39fb00831c7198e2927
    +name:test_urf_letter_mono_300
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_letter_mono_300
        +guid:4b53385f-5244-49d0-a89e-d3316ed9cc8f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_letter_mono_300(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('880fc1d0aecef52967afdb68cc3d2f441cf5dde14ba6e39fb00831c7198e2927')
    outputsaver.save_output()
    tray.reset_trays()
