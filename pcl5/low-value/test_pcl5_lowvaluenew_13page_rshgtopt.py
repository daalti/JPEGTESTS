import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 13Page_rshgtopt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:13Page-rshgtopt.obj=da4765a87574048f74fbd80146009ea05c7ba13bb1c6bfdbf40f1a7bb81c487e
    +test_classification:System
    +name: test_pcl5_lowvaluenew_13page_rshgtopt
    +test:
        +title: test_pcl5_lowvaluenew_13page_rshgtopt
        +guid:ac1d7f81-8b0d-4784-99db-3a9784126edb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_13page_rshgtopt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('da4765a87574048f74fbd80146009ea05c7ba13bb1c6bfdbf40f1a7bb81c487e', timeout=600)
    outputsaver.save_output()
