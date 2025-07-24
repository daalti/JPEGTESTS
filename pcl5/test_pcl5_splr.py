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
    +external_files:splr.pcl=0de90cd6ad7c1995326cd790cb8ccc0e7445e736fe3564d04d10585f9f853ac8
    +name:test_pcl5_splr
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_splr
        +guid:156a6439-2506-4c3d-a9c1-9a87fec667ee
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_splr(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('0de90cd6ad7c1995326cd790cb8ccc0e7445e736fe3564d04d10585f9f853ac8')
    outputsaver.save_output() 