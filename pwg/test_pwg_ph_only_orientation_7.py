import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-Orientation-7.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-Orientation-7.pwg=a1938f36ad382b152c3016f4c4c7cbf0954dd2aa28a877ef8b114f66be638245
    +name:test_pwg_ph_only_orientation_7
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_orientation_7
        +guid:c53a4cfd-dd27-44e7-8279-6913b27b62ce
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_orientation_7(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    printjob.print_verify('a1938f36ad382b152c3016f4c4c7cbf0954dd2aa28a877ef8b114f66be638245')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
