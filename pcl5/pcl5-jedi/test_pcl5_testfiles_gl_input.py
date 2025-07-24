import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using input.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:input.pcl=50cc738162680136f573b87a4b1b32b11b959a14ba30a5e7836969435798a3fd
    +test_classification:System
    +name: test_pcl5_testfiles_gl_input
    +test:
        +title: test_pcl5_testfiles_gl_input
        +guid:0261dbfb-54a7-4653-abd2-911db62dd072
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_input(setup_teardown, printjob, outputsaver):
    printjob.print_verify('50cc738162680136f573b87a4b1b32b11b959a14ba30a5e7836969435798a3fd', timeout=600)
    outputsaver.save_output()
