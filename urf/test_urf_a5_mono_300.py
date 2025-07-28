import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **A5_Mono_300.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A5_Mono_300.urf=f1c8ad7c7973ddb47ec9f6daba18dcc9c7ade2aec4010a1d3d91d82b34620a32
    +name:test_urf_a5_mono_300
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a5_mono_300
        +guid:dd8992d3-37e7-4f2a-9c46-fc38483e7d3f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_a5_148x210mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a5_mono_300(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a5_148x210mm', default):
        tray.configure_tray(default, 'iso_a5_148x210mm', 'stationery')

    printjob.print_verify('f1c8ad7c7973ddb47ec9f6daba18dcc9c7ade2aec4010a1d3d91d82b34620a32')
    outputsaver.save_output()
    tray.reset_trays()
