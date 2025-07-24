import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ra.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ra.obj=41d853ea0e97c85c2f3b6c5f1d97678f7a3070a06543578102a97916a3a044ed
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_ra
    +test:
        +title: test_pcl5_hpgl_polygon_ra
        +guid:72fa91bd-1c49-4b1e-9cae-8c2198397c8f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_ra(setup_teardown, printjob, outputsaver):
    printjob.print_verify('41d853ea0e97c85c2f3b6c5f1d97678f7a3070a06543578102a97916a3a044ed', timeout=600)
    outputsaver.save_output()
