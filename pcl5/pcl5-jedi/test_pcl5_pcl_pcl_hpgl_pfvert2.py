import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using pfvert2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pfvert2.obj=c91c34b2b9ce17e332880f7773372cfb19fdb208a4e894466a15fa4138b7fa73
    +test_classification:System
    +name: test_pcl5_pcl_pcl_hpgl_pfvert2
    +test:
        +title: test_pcl5_pcl_pcl_hpgl_pfvert2
        +guid:0eb62cda-43d3-4ccc-be22-71a5e5ad9f00
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pcl_hpgl_pfvert2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c91c34b2b9ce17e332880f7773372cfb19fdb208a4e894466a15fa4138b7fa73', timeout=900)
    outputsaver.save_output()
