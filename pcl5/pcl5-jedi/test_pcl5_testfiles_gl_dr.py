import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using dr.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dr.pcl=b0ba83933bd1e03102333c383d3e639ebedb237c5507887dadd9d0962bb9cf4b
    +test_classification:System
    +name: test_pcl5_testfiles_gl_dr
    +test:
        +title: test_pcl5_testfiles_gl_dr
        +guid:925cb169-169b-45c5-99b3-543097a090be
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_dr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b0ba83933bd1e03102333c383d3e639ebedb237c5507887dadd9d0962bb9cf4b', timeout=600)
    outputsaver.save_output()
