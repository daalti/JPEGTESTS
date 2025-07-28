import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **iso_sra3_320x450mm_Mono.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:iso_sra3_320x450mm_Mono.urf=e2e0013e6e94dddc64355cf125ab3ba8918cdf4a604472f95c22fd87d2e5edd3
    +name:test_urf_iso_sra3_320x450mm_mono
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_iso_sra3_320x450mm_mono
        +guid:776fc145-ee6c-4309-8ae8-3baf96c3b191
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_iso_sra3_320x450mm_mono(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e2e0013e6e94dddc64355cf125ab3ba8918cdf4a604472f95c22fd87d2e5edd3')
    outputsaver.save_output()
