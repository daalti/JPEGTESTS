import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using plotsize.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:plotsize.pcl=50020c736ed07c5ae65843a87bf8d3dedf965ac71c131b0eaa5071004d42bf84
    +test_classification:System
    +name: test_pcl5_testfiles_misc_plotsize
    +test:
        +title: test_pcl5_testfiles_misc_plotsize
        +guid:ec57e7fb-054e-42e4-82e4-b8599c5d6707
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_plotsize(setup_teardown, printjob, outputsaver):
    printjob.print_verify('50020c736ed07c5ae65843a87bf8d3dedf965ac71c131b0eaa5071004d42bf84', timeout=600)
    outputsaver.save_output()
