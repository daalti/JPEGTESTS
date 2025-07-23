import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-Orientation-2.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-Orientation-2.pwg=555c7a547d698ada566577a22253818e0dcc29fb8bdfaad1e41671f72f7bb9b2
    +name:test_pwg_cloud_print_orientation_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_orientation_2
        +guid:f29e1daf-5a0b-4dde-9305-63a718a34437
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_orientation_2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('555c7a547d698ada566577a22253818e0dcc29fb8bdfaad1e41671f72f7bb9b2', 'FAILED')
    outputsaver.save_output()
