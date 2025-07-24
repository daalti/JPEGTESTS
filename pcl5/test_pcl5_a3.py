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
    +external_files:a3.pcl=e2a95201a4d9f98aec6bff6e71e7422153a31dda8659c4f066858a98c9106b36
    +name:test_pcl5_a3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_a3
        +guid:37edb6f9-b801-4e5b-b615-ac55a8a1e87e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_a3(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('e2a95201a4d9f98aec6bff6e71e7422153a31dda8659c4f066858a98c9106b36')
    outputsaver.save_output()