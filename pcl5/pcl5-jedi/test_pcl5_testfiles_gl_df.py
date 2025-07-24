import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using df.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:df.pcl=a3979c2f7c4cdbb895358315fd39360ec4f15a59ccf1ac213bbfb2b87263b90b
    +test_classification:System
    +name: test_pcl5_testfiles_gl_df
    +test:
        +title: test_pcl5_testfiles_gl_df
        +guid:52e3b29f-c535-4a43-b83c-63ae45579a7e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_df(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a3979c2f7c4cdbb895358315fd39360ec4f15a59ccf1ac213bbfb2b87263b90b', timeout=600)
    outputsaver.save_output()
