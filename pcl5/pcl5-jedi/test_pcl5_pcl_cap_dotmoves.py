import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using dotmoves.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dotmoves.obj=92e1cb9259f45953cbb80545c4abc6a31dbd46cd8db6ae9e3394a61063ecef8f
    +test_classification:System
    +name: test_pcl5_pcl_cap_dotmoves
    +test:
        +title: test_pcl5_pcl_cap_dotmoves
        +guid:f7153caf-dde4-41d8-be43-e22d500b4d23
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_cap_dotmoves(setup_teardown, printjob, outputsaver):
    printjob.print_verify('92e1cb9259f45953cbb80545c4abc6a31dbd46cd8db6ae9e3394a61063ecef8f', timeout=600)
    outputsaver.save_output()
