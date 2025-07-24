import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using textpars.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:textpars.obj=d4e53d341fc36bfbccd05c11933993853239d1f5301b46e760943ea0be72d5a0
    +test_classification:System
    +name: test_pcl5_pcl_parsing_textpars
    +test:
        +title: test_pcl5_pcl_parsing_textpars
        +guid:7db57e9b-543a-4b10-bbcc-4e9fc1df236d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_parsing_textpars(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d4e53d341fc36bfbccd05c11933993853239d1f5301b46e760943ea0be72d5a0', timeout=600)
    outputsaver.save_output()
